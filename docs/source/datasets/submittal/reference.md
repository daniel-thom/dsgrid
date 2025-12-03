(dataset-submittal-reference)=

# Reference

Reference materials for dataset submittal.

## CLI Commands

### Register and Submit (Combined)

```console
$ dsgrid registry projects register-and-submit-dataset [OPTIONS] CONFIG_FILE
```

Options:

- `-p, --project-id TEXT`: Project ID to submit to (required)
- `-m, --dimension-mapping-file PATH`: Dimension mappings config file
- `-l, --log-message TEXT`: Log message (required)
- `-D, --data-base-dir PATH`: Base directory for data files
- `-M, --missing-associations-base-dir PATH`: Base directory for missing associations

Example:

```console
$ spark-submit --master=spark://<master>:7077 \
    $(which dsgrid-cli.py) registry projects register-and-submit-dataset \
    -p dsgrid_conus_2022 \
    -m dimension_mappings.json5 \
    -l "Register and submit dataset" \
    dataset.json5
```

### Submit Previously Registered Dataset

```console
$ dsgrid registry projects submit-dataset [OPTIONS]
```

Options:

- `-p, --project-id TEXT`: Project ID (required)
- `-d, --dataset-id TEXT`: Dataset ID (required)
- `-m, --dimension-mapping-file PATH`: Dimension mappings config file
- `-l, --log-message TEXT`: Log message (required)

Example:

```console
$ spark-submit --master=spark://<master>:7077 \
    $(which dsgrid-cli.py) registry projects submit-dataset \
    -p dsgrid_conus_2022 \
    -d my-dataset-id \
    -m dimension_mappings.json5 \
    -l "Submit dataset to project"
```

### List Project Datasets

```console
$ dsgrid registry projects show PROJECT_ID
```

## Dimension Mappings Config

The dimension mappings configuration file (`dimension_mappings.json5`) defines
mappings from dataset dimensions to project dimensions.

### Structure

```JavaScript
[
  {
    description: "Description of the mapping",
    file: "path/to/mapping_records.csv",
    dimension_type: "geography",           // or other dimension type
    mapping_type: "many_to_one_aggregation",  // see types below
  },
]
```

### Mapping Types

- `one_to_one_explicit`: Direct 1:1 mapping
- `many_to_one_aggregation`: Many source to one target (sum values)
- `many_to_many_explicit_multipliers`: Many-to-many with fractions

See {doc}`/datasets/mapping_query/explanations` for detailed mapping type descriptions.

### Mapping Records Files

CSV files with mapping records:

**For aggregation mappings**:

```text
from_id,to_id
source_record,target_record
```

**For multiplier mappings**:

```text
from_id,to_id,from_fraction
source_record,target_record,fraction
```

## Data Model References

See the data models section for complete schema documentation:

- {ref}`dataset-config`
- {ref}`dimension-mapping-config`
- {ref}`project-config`

## Example Repositories

### StandardScenarios Project

- [TEMPO dataset submission](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/dsgrid_project/datasets/modeled/tempo)
- [Dataset dimension mappings examples](https://github.com/dsgrid/dsgrid-project-StandardScenarios/blob/main/dsgrid_project/datasets/modeled/tempo/dimension_mappings.json5)
