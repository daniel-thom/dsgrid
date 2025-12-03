(mapping-query-explanations)=
# Explanations

This page explains key concepts for mapping and querying dsgrid data.

## Dimension Mappings

A dimension mapping defines how to transform data from one dimension definition
to another.

### Mapping Types

**many_to_one_aggregation**

Multiple source records map to one target record. Values are summed.

Example: Counties to state

```text
from_id,to_id
01001,AL
01003,AL
01005,AL
```

**many_to_many_explicit_multipliers**

Records can map to multiple targets with explicit fractions. Used for
interpolation or weighted disaggregation.

Example: Interpolating between years

```text
from_id,to_id,from_fraction
2018,2018,1.0
2018,2019,0.5
2020,2019,0.5
2020,2020,1.0
```

### Dataset-to-Project vs Base-to-Supplemental

**Dataset-to-Project mappings**:

- Map a dataset's dimensions to a project's base dimensions
- Declared when submitting a dataset to a project
- Applied when data is project-mapped

**Base-to-Supplemental mappings**:

- Map project base dimensions to supplemental (alternate) dimensions
- Defined in the project configuration
- Used in queries to aggregate or transform data

## Query Concepts

### Project Query Process

When running `dsgrid query project run`, dsgrid performs these steps:

1. **Check cache**: Look for cached results in `query_output/cached_tables`
2. **Project-map datasets**: For each dataset:

   - Check for cached project-mapped version
   - Pre-filter according to query filters
   - Map dimensions to project
   - Convert units
   - Cache result to `query_output/cached_project_mapped_datasets`

3. **Combine datasets**: Union all datasets (or use custom expression)
4. **Persist intermediate**: Write combined table to `cached_tables`
5. **Apply result filters**: Post-mapping filters
6. **Aggregate/disaggregate**: Apply dimension transformations
7. **Format output**: Replace IDs with names, sort columns
8. **Write result**: Save to `query_output/<query-name>`
9. **Run reports**: Execute any defined reports

### Pre-filtering vs Post-filtering

**Pre-filtering** (in `dimension_filters` of dataset model):

- Applied before project mapping
- Reduces data early, faster for one-time queries
- Cached result only includes filtered data

**Post-filtering** (in `result` model):

- Applied after project mapping and combining
- Project-mapped cache can be reused for different filters
- Better for multiple queries on same datasets

## Filter Types

dsgrid provides several filter types for queries.

### Expression Filter

Filter where a column matches an expression:

```javascript
dimension_filters: [
  {
    dimension_type: "geography",
    dimension_name: "county",
    operator: "==",
    value: "06037",
    filter_type: "expression",
  },
]
```

### Column Operator Filter

Filter using Spark SQL operators (`isin`, `startswith`, etc.):

```javascript
dimension_filters: [
  {
    dimension_type: "model_year",
    dimension_name: "model_year",
    column: "id",
    operator: "isin",
    value: ["2030", "2040", "2050"],
    filter_type: "column_operator",
  },
]
```

### Subset Filter

Filter using a predefined subset dimension:

```javascript
dimension_filters: [
  {
    dimension_type: "metric",
    dimension_query_names: ["electricity_end_uses"],
    filter_type: "subset",
  },
]
```

### Supplemental Filter

Filter using a supplemental dimension (e.g., filter counties by state):

```javascript
dimension_filters: [
  {
    dimension_type: "geography",
    dimension_name: "state",
    column: "id",
    operator: "isin",
    value: ["CO", "NM"],
    filter_type: "supplemental_column_operator",
  },
]
```

### Time Range Filter

Filter timestamps between two values:

```javascript
dimension_filters: [
  {
    dimension_type: "time",
    dimension_name: "time_est",
    column: "time_est",
    lower_bound: "2012-07-01 00:00:00",
    upper_bound: "2012-08-01 00:00:00",
    filter_type: "between_column_operator",
  },
]
```

```{note}
Multiple filters in an array are combined with AND logic.
```

## Caching Strategy

dsgrid caches intermediate results to improve performance and enable recovery.

### When to Persist

- **Always safer**: Persisting helps Spark complete jobs and enables recovery
- **Skip for one-time queries**: May save time and disk space

### Cache Locations

- `query_output/cached_project_mapped_datasets`: Individual mapped datasets
- `query_output/cached_tables`: Combined intermediate table
- `query_output/<query-name>`: Final query result

### Resuming from Cache

dsgrid automatically detects and uses cached results. To force re-computation,
delete the relevant cache directories.

## When Spark is Needed

**Spark IS needed for:**

- Mapping datasets to projects
- Running project queries with large datasets
- Creating derived datasets

**Spark is NOT needed for:**

- Direct queries on published data using DuckDB
- Small dataset operations
- Registry browsing and metadata operations

See {doc}`/software_reference/apache_spark` for Spark configuration guidance.
