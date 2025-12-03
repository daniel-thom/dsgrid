(creating-config-files)=

# Creating Config Files

This page explains how to create the configuration files required for dataset
registration.

## Dataset Configuration (dataset.json5)

The dataset configuration file defines your dataset's metadata, dimensions, and
data schema.

### Basic Structure

```javascript
{
  // Required metadata
  dataset_id: "my_dataset_2024",
  dataset_type: "modeled",           // "modeled", "historical", or "benchmark"
  data_source: "my_model",
  sector_description: "residential",
  description: "Description of this dataset",

  // Origin information
  origin_creator: "Your Name",
  origin_organization: "Your Organization",
  origin_contributors: ["Name 1", "Name 2"],
  origin_project: "Project Name",
  origin_date: "2024-01-15",
  origin_version: "1.0",
  source: "https://github.com/...",
  data_classification: "low",

  // Optional tags for searchability
  tags: ["residential", "electricity"],

  // Trivial dimensions (single-element)
  trivial_dimensions: ["weather_year"],

  // Dimension definitions (see below)
  dimensions: [...],
  dimension_references: [...],

  // Data file schema (see below)
  table_schema: {...},
}
```

### Dataset Types

- **modeled**: Output from energy models (ResStock, ComStock, etc.)
- **historical**: Based on historical measurements or surveys
- **benchmark**: Reference datasets for comparison

### Defining Dimensions

You can define dimensions inline or reference existing ones.

**Inline dimension definition:**

```javascript
dimensions: [
  {
    "class": "County",
    type: "geography",
    name: "My Counties",
    file: "dimensions/counties.csv",
    description: "Counties in my dataset",
  },
  {
    "class": "Sector",
    type: "sector",
    name: "Transportation",
    file: "dimensions/sector.csv",
    description: "Transportation sector only",
  },
]
```

**Reference to existing dimension:**

```javascript
dimension_references: [
  {
    dimension_type: "model_year",
    dimension_id: "model_year_2010_2050",
  },
]
```

### Table Schema

The `table_schema` section defines your data file structure:

```javascript
table_schema: {
  data_schema: {
    data_schema_type: "standard",    // "standard" or "one_table"
    table_format: {
      format_type: "pivoted",        // "pivoted" or "unpivoted"
      pivoted_dimension_type: "metric",
    },
  },
  data_file: {
    path: "./load_data.parquet",
  },
  lookup_data_file: {                // required for "standard" schema
    path: "./load_data_lookup.parquet",
  },
}
```

## Dimension Records Files

Each dimension needs a records file (CSV) defining its elements.

### Basic Format

Minimum required columns: `id` and `name`.

```text
id,name
01001,Autauga County
01003,Baldwin County
01005,Barbour County
```

### Additional Columns

Add columns for supplemental information:

```text
id,name,state,population
01001,Autauga County,AL,58805
01003,Baldwin County,AL,231767
01005,Barbour County,AL,25223
```

Metric dimensions often include unit information:

```text
id,name,fuel_id,unit
electricity_heating,Electric Heating,electricity,kWh
natural_gas_heating,Natural Gas Heating,natural_gas,therms
```

### Time Dimensions

Time dimensions typically don't need records files because values are generated
programmatically. Instead, configure time parameters in the dimension definition:

```javascript
dimensions: [
  {
    type: "time",
    "class": "Time",
    name: "Hourly 2012",
    time_type: "datetime",
    datetime_format: {
      start: "2012-01-01 00:00:00",
      end: "2012-12-31 23:00:00",
      frequency: "H",
      time_zone: "UTC",
    },
  },
]
```

## Dimension Mappings Configuration

When submitting to a project with different dimensions, create a
`dimension_mappings.json5` file.

### Structure

```javascript
[
  {
    description: "My geography to project geography",
    file: "dimension_mappings/geo_mapping.csv",
    dimension_type: "geography",
    mapping_type: "many_to_one_aggregation",
  },
  {
    description: "My model years to project model years",
    file: "dimension_mappings/year_mapping.csv",
    dimension_type: "model_year",
    mapping_type: "many_to_many_explicit_multipliers",
  },
]
```

### Mapping Types

**many_to_one_aggregation**:
Multiple source records map to one target record. Values are summed.

```text
from_id,to_id
01001,01001
02013,          # null means exclude
```

**many_to_many_explicit_multipliers**:
Records can map to multiple targets with explicit fractions.

```text
from_id,to_id,from_fraction
2018,2018,1.0
2018,2019,0.5
2020,2019,0.5
2020,2020,1.0
```

## Directory Organization

Recommended structure for your dataset files:

    my_dataset/
    ├── dataset.json5
    ├── dimension_mappings.json5      # if submitting to project
    ├── load_data.parquet
    ├── load_data_lookup.parquet      # if using two-table format
    ├── dimensions/
    │   ├── geography.csv
    │   ├── sector.csv
    │   ├── subsector.csv
    │   └── metric.csv
    └── dimension_mappings/
        ├── geo_mapping.csv
        └── year_mapping.csv

## Example Configurations

Full examples are available in the StandardScenarios repository:

- [TEMPO dataset config](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/dsgrid_project/datasets/modeled/tempo)
- [ResStock dataset config](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/dsgrid_project/datasets/modeled/resstock)
- [Historical EIA dataset config](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/dsgrid_project/datasets/historical)
