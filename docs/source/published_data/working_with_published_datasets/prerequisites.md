(published-data-prerequisites)=

# Prerequisites

Before working with published dsgrid datasets, ensure you have the following set up.

## Installation

Follow the {doc}`/getting_started/installation` guide to install dsgrid.

For most published data access, the basic installation is sufficient:

```console
$ pip install dsgrid-toolkit
```

## Configuration

Configure dsgrid to point to the registry containing the published data:

```console
$ dsgrid config create sqlite:///path/to/registry.db
```

For NREL users accessing the shared registry:

```console
$ dsgrid config create sqlite:////projects/dsgrid/standard-scenarios.db
```

Verify your configuration by listing available projects:

```console
$ dsgrid registry projects list
```

## Computational Resources

### For Browsing Only

No special computational resources are needed to browse the registry or view
dataset metadata. A personal computer is sufficient.

### For Data Access and Queries

Depending on the dataset size and your query complexity:

- **Small datasets**: Personal computer is sufficient
- **Large datasets or complex queries**: NREL HPC (Kestrel) with Spark cluster

See {doc}`/software_reference/apache_spark` for Spark setup if needed.

## Access Credentials

### NREL Internal Users

Access to the shared registry and data files requires an NREL HPC account.

### External Users

Published data on OEDI (Open Energy Data Initiative) is publicly accessible:

- **TEMPO data**: ``s3://nrel-pds-dsgrid/tempo/``

For more details on data access, see {doc}`/published_data/published_datasets`.
