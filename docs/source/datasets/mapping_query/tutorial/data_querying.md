(data-querying-tutorial)=
# Data Querying

This tutorial shows how to query dsgrid datasets using DuckDB and Python.

## Query Objectives

This tutorial demonstrates:

- Reading data from Kestrel filesystem and OEDI S3 bucket
- Filtering data by dimensions (model years, geography, scenario)
- Exporting results to pandas dataframe or CSV

## Prerequisites

- Python virtual environment
- DuckDB and pandas installed

```bash
$ python -m venv dsgrid-tutorial
$ source dsgrid-tutorial/bin/activate
$ pip install duckdb pandas
```

## Loading Data

### From NREL Kestrel

```python
import duckdb

tablename = "tbl"
data_dir = "/datasets/dsgrid/dsgrid-tempo-v2022"
dataset_name = "state_level_simplified"
filepath = f"{data_dir}/{dataset_name}"

duckdb.sql(f"""CREATE VIEW {tablename} AS SELECT *
             FROM read_parquet("{filepath}/table.parquet/**/*.parquet",
             hive_partitioning=true, hive_types_autocast=false)""")

# Inspect the table
duckdb.sql(f"DESCRIBE {tablename}")
duckdb.sql(f"SELECT * FROM {tablename} LIMIT 5").to_df()
```

### From OEDI (Public Access)

```python
import duckdb

tablename = "tbl"
data_dir = "s3://nrel-pds-dsgrid/tempo/tempo-2022/v1.0.0"
dataset_name = "state_level_simplified"
filepath = f"{data_dir}/{dataset_name}"

duckdb.sql(f"""CREATE TABLE {tablename} AS SELECT *
             FROM read_parquet('{filepath}/table.parquet/**/*.parquet',
             hive_partitioning=true, hive_types_autocast=false)""")
```

## Filtering Data

DuckDB can filter data while loading, avoiding the need to read all data:

```python
duckdb.sql(f"""CREATE TABLE {tablename} AS SELECT *
              FROM read_parquet('{filepath}/table.parquet/**/*.parquet',
              hive_partitioning=true, hive_types_autocast=false)
              WHERE state='MI' AND scenario='efs_high_ldv'
           """)
```

## Using Metadata for Queries

dsgrid datasets include a `metadata.json` file with dimension information.
You can use this to write queries that work across different datasets.

### Setup

````{tabs}
```{code-tab} bash Kestrel

pip install pydantic
```

```{code-tab} bash OEDI

pip install pydantic pyarrow
```
````

### Load Metadata

````{tabs}
```{code-tab} python Kestrel

from pathlib import Path
import sys

scripts_path = Path("/path/to/dsgrid/scripts")
sys.path.append(str(scripts_path))

from scripts.table_metadata import TableMetadata

dataset_path = "/datasets/dsgrid/dsgrid-tempo-v2022/state_level_simplified"
metadata_path = f"{dataset_path}/metadata.json"
table_metadata = TableMetadata.from_file(metadata_path)
```

```{code-tab} python OEDI

from pathlib import Path
import sys

scripts_path = Path("/path/to/dsgrid/scripts")
sys.path.append(str(scripts_path))

from scripts.table_metadata import TableMetadata

bucket = "nrel-pds-dsgrid"
filepath = "tempo/tempo-2022/v1.0.0/state_level_simplified/metadata.json"
table_metadata = TableMetadata.from_s3(bucket, filepath)
```
````

### Aggregation Example

Use metadata to build dynamic aggregation queries:

```python
group_by_dimensions = ['model_year', 'scenario', 'geography', 'subsector']
group_by_cols = []

for dimension in group_by_dimensions:
    group_by_cols.extend(table_metadata.list_columns(dimension))

group_by_str = ", ".join(group_by_cols)
value_column = table_metadata.value_column

duckdb.sql(f"""CREATE TABLE {tablename} AS
               SELECT SUM({value_column}) AS value_sum, {group_by_str}
               FROM read_parquet('{filepath}/table.parquet/**/*.parquet')
               GROUP BY {group_by_str}
                   """)
```

## Exporting Results

### To Pandas DataFrame

```python
dataframe = duckdb.sql(f"SELECT * FROM {tablename}").df()
```

### To CSV

```python
dataframe.to_csv('mydata.csv')
```

## Next Steps

- For more advanced queries on projects, see {doc}`/projects/index`
- For filtering options, see {doc}`../explanations`
- For mapping data to different dimensions, see {doc}`data_mapping`
