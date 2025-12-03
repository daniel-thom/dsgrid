(dataset-registration-reference)=

# Reference

Reference materials for dataset registration.

## CLI Commands

### Register a Dataset

```console
$ dsgrid registry datasets register [OPTIONS] CONFIG_FILE
```

Options:

- `-l, --log-message TEXT`: Log message for the registration (required)
- `-D, --data-base-dir PATH`: Base directory for data files
- `-M, --missing-associations-base-dir PATH`: Base directory for missing
  associations files

Example:

```console
$ dsgrid registry datasets register \
    -l "Register my dataset" \
    -D /path/to/data \
    dataset.json5
```

### List Registered Datasets

```console
$ dsgrid registry datasets list
```

### Show Dataset Details

```console
$ dsgrid registry datasets show DATASET_ID
```

## Configuration Schemas

See the data models reference for complete schema documentation:

- {ref}`dataset-config`
- {ref}`dimension-config`
- {ref}`dimension-reference`

## Data Format Reference

### Supported Data Types

For CSV files, these data types can be specified:

- `BOOLEAN`: Boolean
- `INT`, `INTEGER`: 4-byte integer
- `TINYINT`: 1-byte integer
- `SMALLINT`: 2-byte integer
- `BIGINT`: 8-byte integer
- `FLOAT`: 4-byte float
- `DOUBLE`: 8-byte float
- `STRING`, `TEXT`, `VARCHAR`: String
- `TIMESTAMP_TZ`: Timestamp with time zone
- `TIMESTAMP_NTZ`: Timestamp without time zone

### Time Format Reference

**DateTime dimensions**:

- Parquet: `TIMESTAMP` logical type, adjusted to UTC
- Spark: `TimestampType`

**Representative period (one_week_per_month_by_hour)**:

- `month`: 1-12 (January = 1)
- `day_of_week`: 0-6 (Monday = 0)
- `hour`: 0-23 (midnight = 0)

## Example Repositories

### StandardScenarios Project

https://github.com/dsgrid/dsgrid-project-StandardScenarios

Contains examples of:

- Historical datasets
- Modeled datasets (TEMPO, ResStock, ComStock)
- Dimension mappings
- Project configuration

### Dataset Examples

- [TEMPO dataset](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/tempo_project)
- [ResStock dataset](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/dsgrid_project/datasets/modeled/resstock)
- [EIA historical dataset](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/dsgrid_project/datasets/historical)
