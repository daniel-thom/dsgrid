(published-data-tutorial)=

# Tutorial

This tutorial walks through finding and accessing published dsgrid data.

## Browsing the Registry

### Using the CLI

List all available projects:

```console
$ dsgrid registry projects list
```

List all datasets:

```console
$ dsgrid registry datasets list
```

Filter dimensions by type:

```console
$ dsgrid registry dimensions list -f Type==geography
```

List all components at once:

```console
$ dsgrid registry list
```

### Using a Different Registry

Browse a different registry by specifying the URL:

```console
$ dsgrid -u sqlite:///path/to/other-registry.db registry list
```

### Using the Project Viewer

dsgrid provides a web-based project viewer for browsing the registry interactively.

1. Set environment variables:

```console
$ export DSGRID_REGISTRY_DATABASE_URL=sqlite:///path/to/registry.db
$ export DSGRID_QUERY_OUTPUT_DIR=api_query_output
$ export DSGRID_API_SERVER_STORE_DIR=.
```

2. Start the API server:

```console
$ uvicorn dsgrid.api.app:app
```

3. Start the project viewer:

```console
$ python dsgrid/apps/project_viewer/app.py
```

## Accessing Data Files

### OEDI (Public Access)

TEMPO data is publicly available on OEDI:

```console
$ aws s3 ls s3://nrel-pds-dsgrid/tempo/ --no-sign-request
```

Download specific files:

```console
$ aws s3 cp s3://nrel-pds-dsgrid/tempo/path/to/file.parquet . --no-sign-request
```

### NREL Kestrel

On NREL's Kestrel HPC, data is available at multiple aggregation levels in the
shared filesystem.

## Next Steps

- To run queries on published data, see {doc}`/dataset_mapping_query/index`
- To visualize data, see {doc}`/software_reference/index`
- To understand the data structure, see {doc}`/getting_started/dsgrid_fundamentals`
