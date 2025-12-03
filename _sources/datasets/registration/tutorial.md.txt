(dataset-registration-tutorial)=

# Tutorial

This tutorial walks through creating and registering a dsgrid dataset, following the
example of the TEMPO dataset from the [StandardScenarios project](https://github.com/dsgrid/dsgrid-project-StandardScenarios).

```{note}
You can register a dataset without connecting it to a project. When registering
standalone, dimension mapping information is not required.
```

## Step 1: Create the Dataset Configuration

Create a `dataset.json5` file with basic metadata:

```javascript
{
  dataset_id: "tempo_conus_2022",
  dataset_type: "modeled",
  data_source: "tempo",
  sector_description: "transportation",
  description: "CONUS 2022 TEMPO county-level results for PEV charging.",
  origin_creator: "Arthur Yip",
  origin_organization: "NREL",
  origin_contributors: [
    "Arthur Yip",
    "Brian Bush",
  ],
  origin_project: "dsgrid CONUS 2022",
  origin_date: "Dec 21 2021",
  origin_version: "dsgrid",
  source: "https://github.com/repo/commit/abc123",
  data_classification: "low",
  tags: [
    "transportation",
    "tempo",
  ],
}
```

## Step 2: Choose a Data Format

Select either the one-table or two-table format. See {doc}`explanations/input_formats`
for details on each format.

This example uses the **two-table format** with:

- Time: Representative period format (hourly data for one week per month)
- Metric: Record IDs pivoted as columns
- Geography, Subsector, Model Year, Scenario: Stored in lookup table
- Sector, Weather Year: Trivial dimensions

Add the table schema to your `dataset.json5`:

```javascript
trivial_dimensions: [
  "sector",
  "weather_year",
],
use_project_geography_time_zone: true,
table_schema: {
  data_schema: {
    data_schema_type: "standard",
    table_format: {
      format_type: "pivoted",
      pivoted_dimension_type: "metric",
    },
  },
  data_file: {
    path: "./load_data.parquet",
  },
  lookup_data_file: {
    path: "./load_data_lookup.parquet",
  },
},
```

## Step 3: Define Dimensions

For each non-trivial dimension, either:

1. **Reference an existing dimension** if it matches one already in the registry
2. **Define a new dimension** with a records file

Example dimension definition:

```javascript
dimensions: [
  {
    "class": "County",
    type: "geography",
    name: "ACS County 2018",
    file: "dimensions/counties.csv",
    description: "American Community Survey US counties, 2018.",
  },
]
```

The dimension records file (`dimensions/counties.csv`) lists each record:

```text
id,name
01001,Autauga County
01003,Baldwin County
...
```

## Step 4: Create Data Files

Create your Parquet data files according to the chosen format.

**load_data.parquet** (time-series with pivoted metrics):

    +-----------+----+-----+---------+---------+---------+
    |day_of_week|hour|month|  L1andL2|     DCFC|       id|
    +-----------+----+-----+---------+---------+---------+
    |          0|   0|   12|484.81393|405.39902|109450511|
    |          0|   1|   12|150.94759|      0.0|109450511|
    ...

**load_data_lookup.parquet** (dimension records with ID linkage):

    +---------+--------------------+----------+--------+------------------+
    |geography|           subsector|model_year|      id|          scenario|
    +---------+--------------------+----------+--------+------------------+
    |    06085|Single_Driver+Low...|      2022| 1060853|ldv_sales_evs_2035|
    ...

```{warning}
All dimension columns must be strings, including columns that look like numbers
(e.g., `model_year`). FIPS county codes must preserve leading zeros.
```

## Step 5: Register the Dataset

Register your dataset with the CLI:

```console
$ dsgrid registry datasets register \
    --log-message "Register TEMPO dataset" \
    dataset.json5
```

For large datasets requiring Spark:

```console
$ spark-submit --master=spark://<master>:7077 \
    $(which dsgrid-cli.py) registry datasets register \
    --log-message "Register TEMPO dataset" \
    dataset.json5
```

## Handling Missing Dimension Combinations

If your dataset lacks data for certain dimension combinations (e.g., building types
that don't exist in certain regions), you must declare these as missing associations.

See {doc}`explanations/checking_validity` for the iterative workflow to identify
and declare missing associations.

## Next Steps

- To submit this dataset to a project, see {doc}`/datasets/submittal/index`
- For more on dimension requirements, see {doc}`explanations/required_dimensions`
- For data format details, see {doc}`explanations/input_formats`
