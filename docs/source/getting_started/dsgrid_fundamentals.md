(dsgrid-fundamentals)=
# dsgrid Fundamentals

dsgrid is a tool for collecting and aligning datasets containing timeseries information
describing future energy use, especially electricity load, to be used in planning studies.

This page introduces the core concepts you need to understand to work with dsgrid effectively.

## Core Concepts

### Datasets

A dsgrid **dataset** describes energy use or another metric (e.g., population, stock of
certain assets, delivered energy service, growth rates) resolved over multiple dimensions.
Datasets can range in size from less than 1 megabyte to over 1 terabyte.

There are three types of datasets:

- **Benchmark**: Reference datasets for comparison
- **Historical**: Datasets based on historical data
- **Modeled**: Datasets produced by energy models (e.g., ResStock, ComStock)

Datasets are defined by configuration files that specify their attributes, dimensionality,
and file format characteristics. See {doc}`/datasets/registration/index` for details on
registering datasets.

### Dimensions

dsgrid datasets and projects are multi-dimensional. Every dataset must define values for
each of these dimension types:

- **scenario** -- What scenario is being described (if any)
- **model_year** -- What historical or future year is being described
- **weather_year** -- What year's weather patterns are being used
- **geography** -- What geographic entity is being summarized (e.g., counties, states)
- **time** -- Timestamps, annual indicators, or other time descriptors
- **sector** -- Commercial, Residential, Industrial, Transportation
- **subsector** -- Specific building types, industries, transportation modes
- **metric** -- Further breakdowns including energy end-uses

Any dimension can be "trivial" (single-element) if the data doesn't vary along that
dimension. For example, historical data typically has a trivial scenario dimension.

### Projects

A dsgrid **project** is a collection of datasets that describe energy demand for a
specific region over a specific timeframe. Projects define:

- **Base dimensions**: The common dimensions that all submitted datasets must map to
- **Supplemental dimensions**: Alternative resolutions available for queries
- **Dataset requirements**: What records each dataset must provide

Projects enable combining datasets from different sources (e.g., residential models,
commercial models, industrial data) into a coherent whole by defining mappings between
different dimension definitions.

### Dimension Mappings

Different data sources often define dimensions differently. For example:

- Census division data needs to be mapped to counties
- EIA building types need to map to ComStock building types
- "Residential", "res", and "Res." all refer to the same sector

**Dimension mappings** explicitly define these relationships, enabling dsgrid to
automatically transform and combine data from different sources.

Two types of mappings:

1. **Dataset-to-Project**: Maps a dataset's dimensions to a project's base dimensions
2. **Base-to-Supplemental**: Maps project base dimensions to supplemental dimensions for queries

### Queries and Derived Datasets

**Queries** transform and combine project data, applying:

- Dimension mappings to align datasets
- Filters to exclude unwanted records
- Aggregations to summarize across dimensions
- Output to supplemental dimensions

**Derived datasets** are created by combining multiple datasets through queries. They
enable operations like applying growth rates or calculating residuals.

## User Roles

Different users interact with dsgrid in different ways:

### Data Users

Data users access already-queried data or write custom queries. They typically:

- Find and download published datasets
- Run queries to extract specific views of the data
- Analyze query results

See {doc}`/published_data/index` to get started with published data.

### Dataset Submitters

Dataset submitters prepare and contribute data to dsgrid projects. They:

- Prepare data in dsgrid-compatible formats
- Define dimensions for their datasets
- Create dimension mappings to project base dimensions
- Test and submit datasets to projects

See {doc}`/datasets/registration/index` to learn about preparing datasets.

### Project Coordinators

Project coordinators manage dsgrid projects end-to-end. They:

- Create and configure projects
- Define base and supplemental dimensions
- Coordinate with dataset contributors
- Create derived datasets
- Run queries and publish data

See {doc}`/projects/index` for project management documentation.

## Technology Stack

dsgrid uses two key technologies:

### SQL Database (SQLite)

dsgrid registries store metadata and relationships between components (dimensions,
datasets, dimension mappings, projects, queries) in SQLite databases.

### Apache Spark

Because dsgrid data can be very large (terabytes), dsgrid uses Apache Spark for
data operations that require distributed computing across multiple nodes.

```{note}
Not all dsgrid operations require Spark. Many tasks can be performed on a
single machine. See the guidance below for when Spark is needed.
```

### When is Spark Needed?

**Spark is NOT needed for:**

- Registering datasets (metadata operations)
- Small-scale development and testing
- Working with single, small datasets
- Browsing the registry

**Spark IS needed for:**

- Submitting datasets to projects (data validation and mapping)
- Running queries on projects with large datasets
- Creating derived datasets
- Any operation involving large data transformations

See {doc}`/software_reference/apache_spark` for Spark setup instructions.

## Computational Environments

dsgrid supports two computational environments:

### Standalone (Personal Computer)

Suitable for:

- Small-scale development and testing
- Working with small datasets
- Very small dsgrid projects (no large datasets, little downscaling)

Note that use on standalone Windows machines is especially limited.

### NREL High Performance Computing (Kestrel)

For production work with large datasets, NREL's HPC provides:

- Shared registry access
- Apache Spark cluster capabilities
- Sufficient computational, memory, and disk resources

See {doc}`installation` for setup instructions in both environments.

## Next Steps

Depending on your goals:

- **Using published data**: Start with {doc}`/published_data/index`
- **Preparing a dataset**: See {doc}`/datasets/registration/index`
- **Running queries**: See {doc}`/datasets/mapping_query/index`
- **Managing a project**: See {doc}`/projects/index`
- **Installation**: Continue to {doc}`installation`
