#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pandas as pd
import re
import sqlite3


def parse(query):
    """This function parse all clauses of the query."""
    
    # SQL keywords
    keywords = [
        "SELECT ",
        "DELETE ",
        "INSERT INTO ",
        "CREATE TABLE ",
        "UPDATE ",
        "FROM ",
        "INNER ",
        "LEFT ",
        "OUTER ",
        "CROSS ",
        "RIGHT ",
        "FULL ",
        "JOIN ",
        "ON ",
        "WHERE ",
        "GROUP BY ",
        "HAVING ",
        "PARTITION BY ",
        "ORDER BY ",
        "LIMIT ",
        "ALL ",
        "UNION ",
        "OFFSET ",
        "AS ",
        "SET ",
    ]
    
    # Split the query according to SQL keywords
    keywords = re.compile("|".join(keywords), re.IGNORECASE).findall(query)
    splitted_query = re.split("|".join(keywords), query)

    # Create a dict to store each clause
    parsed_query = dict()
    for i in range(len(keywords)):
        kw = keywords[i]
        try:
            parsed_query[kw.upper()].append(splitted_query[i+1].strip())
        except KeyError:
            parsed_query[kw.upper()] = [splitted_query[i+1].strip()]
        
    return parsed_query


def get_df_instances(query):
    """This function parse the query to find all defined instances of
    corresponding pd.DataFrame in the __main__ namespace."""

    import __main__

    splitted_query = query.split()
    df_set = set()

    # Looking if some pd.DataFrame exist with this name in __main__ namespace. 
    for s in splitted_query:
        s = s.strip(",; ")
        try:
            temp = eval("__main__." + s)
            if isinstance(temp, pd.DataFrame):
                df_set.add(s)
        except:
            pass

    return df_set


def clean(query):
    """This function clean an SQL query before parsing."""
    
    # Handle insecable spaces
    query = query.replace('\xa0', " ")
    
    # Remove multiline comments (from "/*" to "*/")
    while "/*" in query:
        l_string1, r_string1 = query.split("/*", 1)
        _, r_string2 = r_string1.split("*/", 1)
        query = l_string1 + r_string2
    
    # Remove 1 line comments starting with "--", until end of line
    pattern =r'--.+?\n'
    query = re.sub(pattern, '\n', query)
    pattern =r'--.+?$'
    query = re.sub(pattern, '', query)
    
    # Remove 1 line comments starting with "#" (MySQL), until end of line
    pattern = r'#.+?\n'
    query = re.sub(pattern, '\n', query)
    pattern = r'#.+?$'
    query = re.sub(pattern, '', query)
    
    # Replace the break of lines (\n) by spaces
    query = re.sub("\n", " ", query)
    
    # Remove the spaces and ";" at end of query
    query = query.rstrip("; ")
    
    return query


def run(query, verbose=0):

    import __main__

    # Parse all the clause of the query
    query = clean(query)
    parsed_query = parse(query)
    
    # Creation of an "in memory" DB
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()

    # Listing the input dataframes (already existing)
    df_to_virtualize = get_df_instances(query)
    
    # Virtualization of the input dataframes
    index_names = dict()
    for dataframe in df_to_virtualize:
        exec("global "+ dataframe)
        temp_df = eval("__main__."+dataframe)
        temp_df.to_sql(dataframe, conn)
        # Save the name of the index
        index_names[dataframe] = eval("__main__."+dataframe).index.name

    if verbose > 0:
        print("Virtualized pd.DataFrames:", df_to_virtualize)

    # Listing outputs dataframes
    df_to_create = set()
    for kw in [
        "CREATE TABLE ",
    ]:
        try:
            [df_to_create.add(x) for x in parsed_query[kw]]
        except KeyError:
            pass
    
    # Try to save results in a pd.Dataframe
    try:
        result_df = pd.read_sql(query, conn)
    # If it fails, just execute the query
    except TypeError:
        c.execute(query)
        result_df = None
    
    # Devirtualization into pd.Dataframes
    for virtual_df in (df_to_virtualize | df_to_create):
        exec("__main__."+virtual_df+"= pd.read_sql('SELECT * FROM {}'.format(virtual_df), conn)")
        exec("__main__."+virtual_df+".set_index('index', inplace=True)")
        # restore the name of the index
        exec("__main__."+virtual_df+".index.name = index_names[virtual_df]")
    
    if verbose > 0:
        print("De-virtualized pd.DataFrames:", (df_to_virtualize | df_to_create))
    
    # Commit the change and close connexion
    conn.commit()
    conn.close()
    
    # Return the result of the query as pd.Dataframe
    return result_df