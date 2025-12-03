(apache-spark)=

# Apache Spark

This page describes Apache Spark concepts important for dsgrid users, including
when Spark is needed and how to configure it.

## When is Spark Needed?

**Spark IS required for:**

- Submitting datasets to projects
- Running project queries with large datasets
- Creating derived datasets
- Any operation that transforms large data files

**Spark is NOT required for:**

- Registering datasets (metadata only)
- Registering projects (metadata only)
- Browsing the registry
- Small-scale testing
- Querying published data directly with DuckDB

## Cluster Modes

### Local Mode

All Spark components run in a single process:

- Good for testing and development
- Not performant for real work
- Won't use all CPUs on your system

```console
$ pyspark
```

### Standalone Cluster

A manually started cluster that uses all available resources:

- Full performance
- Access to Spark UI for debugging
- Required for production dsgrid work

```console
$ pyspark --master=spark://$(hostname):7077
```

## Running on NREL Kestrel

### Quick Start

1. SSH to a login node and start a screen session:

```console
$ screen -S dsgrid
```

2. Create a dsgrid config file:

```console
$ dsgrid config create sqlite:////projects/dsgrid/standard-scenarios.db
```

3. Start a Spark cluster (see {ref}`how-to-start-spark-cluster-kestrel`)

4. Run dsgrid commands:

```console
$ spark-submit --master=spark://$(hostname):7077 \
    $(which dsgrid-cli.py) [command] [options]
```

### Starting a Spark Cluster on Kestrel

Install sparkctl:

```console
$ pip install "sparkctl[pyspark]"
```

Allocate compute nodes with fast local storage:

```console
$ salloc -t 01:00:00 -N1 --account=dsgrid --partition=nvme --mem=240G
```

Configure and start Spark:

```console
$ sparkctl configure --start
```

Set environment variables:

```console
$ export SPARK_CONF_DIR=$(pwd)/conf
$ export JAVA_HOME=/datasets/images/apache_spark/jdk-21.0.7
```

See the [sparkctl documentation](https://nrel.github.io/sparkctl/) for details.

### Spark UI

Monitor jobs at:

- Master: `http://<master_hostname>:8080`
- Jobs: `http://<master_hostname>:4040`

Create an SSH tunnel to access from your laptop:

```console
$ export COMPUTE_NODE=<compute_node_name>
$ ssh -L 4040:$COMPUTE_NODE:4040 -L 8080:$COMPUTE_NODE:8080 $USER@kestrel.hpc.nrel.gov
```

## Configuration Tuning

### Key Settings

**spark.sql.shuffle.partitions**

Formula:

```
num_partitions = max_shuffle_write_size / target_partition_size
```

Target partition size: 128-200 MB. Check Shuffle Write column in Spark UI.

**spark.executor.memory**

Set based on available memory and desired number of executors. More memory
per executor helps with large joins.

**spark.executor.cores**

Affects how many executors are created. Fewer cores per executor = more executors.

## Common Problems

### Job Seems Stuck

If most tasks complete but a few executors are slow:

1. Check `spark.sql.shuffle.partitions` setting
2. Increase executor memory
3. Check for data skew

Look for messages like:

```
INFO UnsafeExternalSorter: Thread 60 spilling sort data of 4.6 GiB to disk
```

This indicates insufficient memory.

### Running Out of Space

Set local directories appropriately:

```console
$ export SPARK_LOCAL_DIRS=/tmp/scratch
```

### Data Skew

When one dimension causes uneven data distribution (e.g., large vs small counties),
executors can become unbalanced.

dsgrid handles this for certain mapping types. Enable `handle_data_skew` in
mapping plans for problematic operations.

## Windows Users

Spark has limited Windows support. Recommended approaches:

1. Use Windows Subsystem for Linux (WSL2)
2. For local mode only, install winutils.exe from
   https://github.com/steveloughran/winutils

## Running dsgrid with Spark

### Using spark-submit

```console
$ spark-submit --master spark://$(hostname):7077 \
    $(which dsgrid-cli.py) \
    query project run \
    query.json5
```

### Using SPARK_CLUSTER Environment Variable

```console
$ export SPARK_CLUSTER=spark://$(hostname):7077
$ dsgrid query project run query.json5
```

### Interactive pyspark

```console
$ pyspark --master=spark://$(hostname):7077
```

IPython:

```console
$ export PYSPARK_DRIVER_PYTHON=ipython
$ pyspark --master=spark://$(hostname):7077
```

Jupyter:

```console
$ export PYSPARK_DRIVER_PYTHON=jupyter
$ export PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --port=8889"
$ pyspark --master=spark://$(hostname):7077
```

## For More Information

- [Apache Spark documentation](https://spark.apache.org/docs/latest/)
- [sparkctl documentation](https://nrel.github.io/sparkctl/)
- {ref}`spark-overview` (detailed technical reference)
