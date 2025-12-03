(data-mapping-tutorial)=
# Data Mapping

This tutorial shows how to map a dataset to a project's dimensions using dsgrid.

## Why Map Data?

Mapping transforms data from one dimension definition to another. Common use cases:

- Aggregating counties to states
- Interpolating between model years
- Aligning different sector classifications

Mapping before querying is beneficial because:

- Expensive Spark operations are performed once
- Cached results can be reused for multiple queries
- Easier to debug in isolation

## Prerequisites

- Dataset registered and submitted to a project
- dsgrid configured with registry location
- Apache Spark available (for large datasets)

See {doc}`/software_reference/apache_spark` for Spark setup.

## Basic Mapping

Map a dataset to project dimensions using the CLI:

```console
$ dsgrid query project map-dataset my-project-id my-dataset-id
```

This performs three Spark queries:

1. Map all non-time dimensions, apply scaling factors and unit conversions
2. Map the time dimension
3. Finalize (convert column names, add null rows as needed)

## Using a Mapping Plan

For large datasets (>10 GB), use a mapping plan to control the process and
enable checkpointing.

### Create a Plan File

Create `plan.json5`:

```javascript
{
  dataset_id: "my-dataset-id",
  mappings: [
    {
      name: "scenario",
    },
    {
      name: "model_year",
      persist: true,
    },
    {
      name: "geography",
      persist: true,
      handle_data_skew: true,
    },
  ],
}
```

### Planning Considerations

- **Order matters**: List operations that reduce data size first
- **Persist strategically**: Checkpoint before expensive or failure-prone operations
- **Handle data skew**: Enable for disaggregation operations that cause uneven
  data distribution

### Execute with Plan

```console
$ dsgrid query project map-dataset my-project-id my-dataset-id \
    --mapping-plan plan.json5
```

## Checkpointing and Recovery

When dsgrid persists an intermediate result, it creates a checkpoint file:

```console
2025-07-08 14:29:21,762 - INFO : Saved checkpoint in
/path/__dsgrid_scratch__/tmpgn_6xbst.json
```

If the job fails, resume from the checkpoint:

```console
$ dsgrid query project map-dataset my-project-id my-dataset-id \
    --mapping-plan plan.json5 \
    --checkpoint-file /path/__dsgrid_scratch__/tmpgn_6xbst.json
```

### Checkpoint File Contents

The checkpoint file records completed operations and the persisted table location:

```json
{
  "dataset_id": "my-dataset-id",
  "completed_operation_names": [
    "scenario",
    "model_year"
  ],
  "persisted_table_filename": "/path/__dsgrid_scratch__/tmpcrpladhx.parquet",
  "mapping_plan_hash": "558083c65760db8fc7bcbbaf48cc94fd1364198b941b6ad845213877d794200c",
  "timestamp": "2025-07-08T14:29:21.746195"
}
```

You can inspect the persisted table for debugging:

```python
import pyspark
spark = pyspark.sql.SparkSession.builder.getOrCreate()
df = spark.read.parquet("/path/__dsgrid_scratch__/tmpcrpladhx.parquet")
df.count()
df.rdd.getNumPartitions()
```

## Troubleshooting

### Large Dataset Failures

If mapping fails for large datasets:

1. Create a mapping plan with more checkpoints
2. List aggregation operations first
3. List disaggregation operations last
4. Enable `handle_data_skew` for operations causing failures

See {ref}`executors-spilling-to-disk` for identifying data skew issues.

### Memory Issues

Increase Spark memory settings:

- `spark.executor.memory`
- `spark.driver.memory`
- `spark.sql.shuffle.partitions` (may need to increase for very large datasets)

## Next Steps

- For query filtering options, see {doc}`../explanations`
- For project queries, see {doc}`/projects/index`
- For Spark configuration, see {doc}`/software_reference/apache_spark`
