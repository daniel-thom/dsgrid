(project-explanations)=

# Explanations

This page explains concepts related to dsgrid projects.

## What is a Project?

A dsgrid project is a **distributed dataset** - a collection of independently
registered datasets that together describe energy demand for a specific region
and timeframe.

For example, the StandardScenarios project combines:

- ResStock (residential buildings)
- ComStock (commercial buildings)
- TEMPO (transportation/EV charging)
- AEO growth factors

Each dataset maintains its own dimensions and data, but the project defines
how they can be combined through dimension mappings.

## Dimension Categories

Projects use three categories of dimensions:

### Base Dimensions

Base dimensions are the **core dimensions** of a project. They define expectations
that all datasets must meet (either directly or through mappings).

- One base dimension per dimension type
- Datasets map their dimensions to base dimensions
- Base dimensions define the "common language" for the project

### Supplemental Dimensions

Supplemental dimensions provide **alternative views** for queries:

- State-level geography (aggregated from counties)
- Annual time (aggregated from hourly)
- Fuel-type groupings

Base-to-supplemental mappings enable aggregations and transformations in queries.

### Dataset Dimensions

Each dataset has its own dimensions that may differ from base dimensions:

- Different geographic granularity
- Different sector classifications
- Different time resolutions

Dataset-to-project mappings reconcile these differences.

## Project Configuration

Key elements of a project config (`project.json5`):

- **project_id**: Unique identifier
- **datasets**: List of expected datasets with requirements
- **base_dimensions**: Core dimensions for the project
- **supplemental_dimensions**: Alternative aggregation dimensions
- **dimension_mappings**: Base-to-supplemental mappings

### Required Dimensions

For each dataset, specify what dimension records it must provide:

```javascript
required_dimensions: {
  single_dimensional: {
    sector: {
      base: ['res'],  // Must provide 'res' sector
    },
    subsector: {
      supplemental: [
        {
          name: 'Subsectors by Sector Collapsed',
          record_ids: ['residential_subsectors'],
        },
      ],
    },
  },
}
```

## Derived Datasets

Derived datasets are created by querying and combining existing datasets.
They enable:

- **Growth projections**: Apply growth factors to base year data
- **Combinations**: Merge datasets (e.g., buildings = residential + commercial)
- **Pre-aggregations**: Create commonly-needed aggregated views

Derived datasets are registered and submitted like regular datasets but are
created from project queries rather than external data sources.

## Query Process

When querying a project:

1. **Project-map datasets**: Transform each dataset to project dimensions
2. **Combine datasets**: Union or apply expressions
3. **Apply filters**: Pre or post-mapping filters
4. **Aggregate**: Transform to supplemental dimensions
5. **Output**: Write results to filesystem

See {doc}`/dataset_mapping_query/explanations` for detailed query process.

## When Spark is Needed

**Spark IS required for:**

- Running project queries
- Creating derived datasets
- Submitting datasets to projects

**Spark is NOT required for:**

- Registering project configuration
- Viewing project metadata
- Small-scale testing

For large projects on NREL HPC, plan for multi-node Spark clusters.
See {doc}`/software_reference/apache_spark`.

## Project Repository Organization

Recommended directory structure:

```
project_repo/
├── dsgrid_project/
│   ├── project.json5
│   ├── datasets/
│   │   ├── benchmark/
│   │   ├── historical/
│   │   └── modeled/
│   │       └── dataset_name/
│   │           ├── dataset.json5
│   │           ├── dimension_mappings.json5
│   │           ├── dimensions/
│   │           └── dimension_mappings/
│   ├── dimensions/
│   │   ├── base/
│   │   └── supplemental/
│   ├── dimension_mappings/
│   │   └── base_to_supplemental/
│   └── derived_datasets/
│       └── query_files.json5
└── README.md
```

This structure:

- Organizes datasets by type (benchmark, historical, modeled)
- Keeps project-level configs separate from dataset configs
- Enables version control for all configurations
