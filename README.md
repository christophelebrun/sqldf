# SQLdf
An API to run SQL (SQLite) queries on pandas.Dataframe objects.

## How it works
1) It create a virtual in-memory SQLite3 database at runtime
2) It convert the pd.Dataframe input(s) to SQL table(s)
3) It proceed the SQL query on the table(s)
4) It convert back the SQL table(s) to updated pd.Dataframe (s)

## Installation
With `pip`:

```
pip install sqldf -U
```

## Examples of use

```python
# Import libraries
import pandas as pd
from sqldf.sqldf import run

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
run(query)
```

```python
# Import libraries
import pandas as pd
import numpy as np
from sqldf.sqldf import run

# Create a dummy pd.Dataframe
df = pd.DataFrame({'col1': ['A', 'B', np.NaN, 'C', 'D'], 'col2': ['F', np.NaN, 'G', 'H', 'I']})

# Define a SQL (SQLite3) query
query = """
SELECT *
FROM df
WHERE col_1 ;
"""

# Run the query
df_view = run(query)
```
## Requirements
* 'pandas>=1.0'
