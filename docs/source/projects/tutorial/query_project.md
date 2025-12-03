(query-project-tutorial)=

# Query a Project

This tutorial shows how to query a dsgrid project for aggregated data.

## Prerequisites

- Access to NREL HPC Kestrel (or equivalent Spark cluster)
- dsgrid installed and configured
- Project with submitted datasets

## Query Objectives

This example query will:

- Read data from multiple datasets
- Filter for specific model years
- Aggregate county-level data to state-level
- Aggregate by fuel type
- Aggregate hourly data to annual

## Step 1: Set Up Environment

SSH to a login node on Kestrel:

```console
$ ssh kestrel.hpc.nrel.gov
```

Follow the instructions at {ref}`how-to-run-dsgrid-kestrel` to set up your environment.

## Step 2: Create Query File

Create `query.json5` with your query definition:

```{note}
Use `dsgrid query project create --help` to generate a template query file.
```

```javascript
{
  "name": "load-per-state",
  "version": "0.1.0",
  "project": {
    "project_id": "dsgrid_conus_2022",
    "dataset": {
      "dataset_id": "load-per-state",
      "source_datasets": [
        {
          "dataset_id": "comstock_conus_2022_projected",
          "dataset_type": "standalone"
        },
        {
          "dataset_id": "resstock_conus_2022_projected",
          "dataset_type": "standalone"
        },
        {
          "dataset_id": "tempo_conus_2022_mapped",
          "dataset_type": "standalone"
        },
      ],
      "params": {
        "dimension_filters": [
          {
            "dimension_type": "model_year",
            "dimension_name": "model_year",
            "column": "id",
            "operator": "isin",
            "value": ["2030", "2040", "2050"],
            "filter_type": "DimensionFilterColumnOperatorModel"
          }
        ],
      }
    },
  },
  "result": {
    "replace_ids_with_names": false,
    "aggregations": [
      {
        "aggregation_function": "sum",
        "dimensions": {
          "geography": [{"dimension_name": "state"}],
          "metric": [{"dimension_name": "end_uses_by_fuel_type"}],
          "model_year": [{"dimension_name": "model_year"}],
          "scenario": [{"dimension_name": "scenario"}],
          "sector": [{"dimension_name": "sector"}],
          "subsector": [],
          "time": [
            {
              "dimension_name": "time_est",
              "function": "year",
              "alias": "year"
            }
          ],
          "weather_year": [{"dimension_name": "weather_2012"}]
        }
      }
    ],
    "reports": [],
    "column_type": "dimension_query_names",
    "dimension_filters": [],
  }
}
```

### Understanding the Query

- **source_datasets**: Datasets to include in the query
- **dimension_filters**: Pre-filter to model years 2030, 2040, 2050
- **aggregations**: Define output dimensions and aggregation functions
- **empty subsector array**: Drops the subsector dimension (sums across all)

## Step 3: Start Spark Cluster

Start a Spark cluster with at least two compute nodes:

```console
$ # See {ref}`how-to-start-spark-cluster-kestrel` for details
```

## Step 4: Run the Query

Activate your dsgrid environment and run:

```console
$ conda activate dsgrid
$ spark-submit --master=spark://$(hostname):7077 \
    $(which dsgrid-cli.py) query project run query.json5 \
    -o query_output
```

This query may take approximately 55 minutes.

## Step 5: Inspect Results

```console
$ pyspark --master=spark://$(hostname):7077
```

```python
>>> df = spark.read.load("query_output/load-per-state/table.parquet")
>>> df.sort("state", "scenario", "model_year").show()
```

## Additional Filter Example

To filter by specific fuel types, add to `params.dimension_filters`:

```javascript
{
  "dimension_type": "metric",
  "dimension_name": "end_uses_by_fuel_type",
  "column": "fuel_id",
  "value": ["electricity", "natural_gas"],
  "operator": "isin",
  "negate": false,
  "filter_type": "SupplementalDimensionFilterColumnOperatorModel"
}
```

See {doc}`/dataset_mapping_query/explanations` for more filter options.

## Next Steps

- For creating derived datasets, see {doc}`create_derived_dataset`
- For Tableau visualization, see {doc}`/software_reference/index`
