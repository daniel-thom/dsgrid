(mapping-query-reference)=
# Reference

Reference materials for mapping and querying.

## CLI Commands

### Map Dataset to Project

```console
$ dsgrid query project map-dataset [OPTIONS] PROJECT_ID DATASET_ID
```

Options:

- `--mapping-plan PATH`: Mapping plan file (JSON5)
- `--checkpoint-file PATH`: Resume from checkpoint
- `--output-dir PATH`: Output directory for cached results

### Run Project Query

```console
$ dsgrid query project run [OPTIONS] PROJECT_ID QUERY_FILE
```

Options:

- `-o, --output PATH`: Output directory (required)
- `--persist-intermediate-table / --no-persist-intermediate-table`: Cache
  intermediate results (default: persist)

## Mapping Types Reference

| Type | Description |
|------|-------------|
| `one_to_one_explicit` | Direct 1:1 mapping between records |
| `many_to_one_aggregation` | Many source records to one target (sum values) |
| `many_to_many_explicit_multipliers` | Many-to-many with explicit fractions |

## Filter Types Reference

| Type | Description |
|------|-------------|
| `expression` | Column matches expression (`operator` + `value`) |
| `expression_raw` | Raw SQL expression |
| `column_operator` | Spark column operator (`isin`, `startswith`, etc.) |
| `subset` | Filter by subset dimension records |
| `supplemental_column_operator` | Filter by supplemental dimension |
| `between_column_operator` | Value between lower and upper bounds |

## Data Model References

See the data models section for complete schema documentation:

- {ref}`dataset_mapping-plan-reference`
- {ref}`dimension-mapping-config`
- {ref}`dimension-mapping-type`

## Example Repositories

### StandardScenarios Project

- [Dimension mappings](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/dsgrid_project/dimension_mappings)
- [Project config with base-to-supplemental mappings](https://github.com/dsgrid/dsgrid-project-StandardScenarios/blob/main/dsgrid_project/project.json5)
- [TEMPO dataset mappings](https://github.com/dsgrid/dsgrid-project-StandardScenarios/blob/main/dsgrid_project/datasets/modeled/tempo/dimension_mappings.json5)
