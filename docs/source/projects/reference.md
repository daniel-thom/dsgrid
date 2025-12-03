(project-reference)=

# Reference

Reference materials for project coordinators.

## CLI Commands

### Register a Project

```console
$ dsgrid registry projects register [OPTIONS] CONFIG_FILE
```

Options:

- `-l, --log-message TEXT`: Log message (required)

Example:

```console
$ dsgrid registry projects register \
    -l "Register my project" \
    project.json5
```

### List Projects

```console
$ dsgrid registry projects list
```

### Show Project Details

```console
$ dsgrid registry projects show PROJECT_ID
```

### Run Project Query

```console
$ dsgrid query project run [OPTIONS] QUERY_FILE
```

Options:

- `-o, --output PATH`: Output directory (required)
- `--persist-intermediate-table / --no-persist-intermediate-table`: Cache tables

Example:

```console
$ spark-submit --master=spark://$(hostname):7077 \
    $(which dsgrid-cli.py) query project run query.json5 \
    -o query_output
```

### Create Query Template

```console
$ dsgrid query project create [OPTIONS]
```

Generate a template query file for a project.

### Create Derived Dataset Config

```console
$ dsgrid query project create-derived-dataset-config QUERY_OUTPUT_DIR OUTPUT_DIR
```

Generate config files from query output.

## Data Model References

See the data models section for complete schema documentation:

- {ref}`project-config`
- {ref}`dataset-config`
- {ref}`dimension-config`
- {ref}`dimension-mapping-config`

## Project Repositories

Active dsgrid projects:

### StandardScenarios

- **Repository**: https://github.com/dsgrid/dsgrid-project-StandardScenarios
- **Contents**: Multi-sector US energy demand projections
- **Datasets**: ResStock, ComStock, TEMPO, AEO growth factors

### Industrial Energy Futures (IEF)

- **Repository**: https://github.com/dsgrid/dsgrid-project-IEF
- **Contents**: Industrial sector energy modeling

## Example Files

### Project Configuration

[StandardScenarios project.json5](https://github.com/dsgrid/dsgrid-project-StandardScenarios/blob/main/dsgrid_project/project.json5)

### Query Files

[Derived dataset queries](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/dsgrid_project/derived_datasets)

### Dimension Files

[Project dimensions](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/dsgrid_project/dimensions)

### Dimension Mappings

[Base-to-supplemental mappings](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/dsgrid_project/dimension_mappings)
