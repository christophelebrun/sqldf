# SQLDF - Structured Query Language (SQL) on DataFrames (DF)
A simple way to run SQL (SQLite) queries on pandas.Dataframe objects.

## How it works
1) It create a virtual in-memory SQLite3 database at runtime
2) It convert the pd.Dataframe input(s) to SQL table(s)
3) It proceed the SQL query on the table(s)
4) It convert back the SQL table(s) to updated pd.Dataframe(s) if required
5) It returns the result of the query if required

## Requirements
* 'python' >= 3.5
* 'pandas' >= 1.0

## Installation
With `pip` (from PyPI repository):

```
pip install sqldf
```

## Examples of use

* SELECT query with WHERE condition
```python
# Import libraries
import pandas as pd
import numpy as np
import sqldf

# Create a dummy pd.Dataframe
df = pd.DataFrame({'col1': ['A', 'B', np.NaN, 'C', 'D'], 'col2': ['F', np.NaN, 'G', 'H', 'I']})

# Define a SQL (SQLite3) query
query = """
SELECT *
FROM df
WHERE col_1 IS NOT NULL;
"""

# Run the query
df_view = sqldf.run(query)
```

* UPDATE query that change inplace a pd.Dataframe
```python
# Import libraries
import pandas as pd
import sqldf

# Create a dummy pd.Dataframe
url = ('https://raw.github.com/pandas-dev/pandas/master/pandas/tests/data/tips.csv')
tips = pd.read_csv(url)

# Define a SQL (SQLite3) query
query = """
UPDATE tips
SET tip = tip*2
WHERE tip < 2;
"""

# Run the query
sqldf.run(query)
```

* More examples in the notebook:
[Demonstration notebook for SQLDF](https://github.com/christophelebrun/sqldf/blob/master/demo/SQLDF_demo.ipynb)