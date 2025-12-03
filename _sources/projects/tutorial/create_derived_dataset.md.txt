(create-derived-dataset-tutorial)=

# Create a Derived Dataset

This tutorial shows how to create and register a derived dataset from a project query.

Derived datasets are created by combining and transforming existing datasets through
queries. Common use cases:

- Apply growth factors to project data through time
- Create sector-specific aggregations
- Generate standardized output formats

This tutorial uses the `comstock_conus_2022_projected` derived dataset from
StandardScenarios as an example.

## Prerequisites

- NREL HPC access with Spark cluster capability
- Project with submitted datasets
- Query file for the derived dataset

## Step 1: Set Up Environment

SSH to Kestrel and start a Spark cluster with at least four compute nodes:

```console
$ # See {ref}`how-to-start-spark-cluster-kestrel`
```

Set environment variables:

```console
$ export SPARK_CLUSTER=spark://$(hostname):7077
$ export QUERY_OUTPUT_DIR=query-output
$ export DSGRID_CLI=$(which dsgrid-cli.py)
$ export NUM_PARTITIONS=2400
```

```{note}
The value of 2400 for NUM_PARTITIONS is based on experience with ~1 TB datasets.
Adjust based on your data size.
```

## Step 2: Create the Query File

The derived dataset query applies growth factors to project load data.

Copy or create the query file. Example from StandardScenarios:

[comstock_conus_2022_projected.json5](https://github.com/dsgrid/dsgrid-project-StandardScenarios/blob/main/dsgrid_project/derived_datasets/comstock_conus_2022_projected.json5)

## Step 3: Run the Query

Execute the query to create the derived dataset:

```console
$ spark-submit \
    --master ${SPARK_CLUSTER} \
    --conf spark.sql.shuffle.partitions=${NUM_PARTITIONS} \
    ${DSGRID_CLI} \
    query \
    project \
    run \
    comstock_conus_2022_projected.json5 \
    -o ${QUERY_OUTPUT_DIR}
```

This may take about an hour for large datasets.

## Step 4: Generate Config Files

Create configuration files for the derived dataset:

```console
$ spark-submit \
    --master ${SPARK_CLUSTER} \
    --conf spark.sql.shuffle.partitions=${NUM_PARTITIONS} \
    ${DSGRID_CLI} \
    query \
    project \
    create-derived-dataset-config \
    ${QUERY_OUTPUT_DIR}/comstock_conus_2022_projected \
    comstock-dd
```

This generates:

- `comstock-dd/dataset.json5`: Dataset configuration
- `comstock-dd/dimension_mapping_references.json5`: Mapping references

## Step 5: Review and Edit Configs

Review the generated files in `comstock-dd/` and edit as needed:

- Update metadata (description, contributors, etc.)
- Verify dimension references
- Check mapping references

## Step 6: Register the Derived Dataset

Register the derived dataset:

```console
$ spark-submit \
    --master ${SPARK_CLUSTER} \
    --conf spark.sql.shuffle.partitions=${NUM_PARTITIONS} \
    ${DSGRID_CLI} \
    registry \
    datasets \
    register \
    comstock-dd/dataset.json5 \
    -l "Register comstock_conus_2022_projected"
```

## Step 7: Submit to Project

Submit the derived dataset to the project:

```console
$ spark-submit \
    --master ${SPARK_CLUSTER} \
    --conf spark.sql.shuffle.partitions=${NUM_PARTITIONS} \
    ${DSGRID_CLI} \
    registry \
    projects \
    submit-dataset \
    -p dsgrid_conus_2022 \
    -d comstock_conus_2022_projected \
    -r comstock-dd/dimension_mapping_references.json5 \
    -l "Submit comstock_conus_2022_projected"
```

## Understanding Derived Datasets

Derived datasets differ from regular datasets:

- Created from queries on existing project data
- Dimensions often match project base dimensions (no mapping needed)
- Can combine multiple source datasets with operations (union, growth factors)
- Registered like regular datasets but with query-generated data

### Common Use Cases

**Growth factor projection**:

Apply annual growth factors to a base year dataset to generate projections
through 2050.

**Sector combinations**:

Combine residential and commercial datasets into a "buildings" derived dataset.

**Aggregated outputs**:

Create pre-aggregated datasets for common query patterns (e.g., state-level
annual totals).

## Next Steps

- Use derived datasets in subsequent queries
- See {doc}`query_project` for querying with derived datasets
- For data visualization, see {doc}`/software_reference/index`
