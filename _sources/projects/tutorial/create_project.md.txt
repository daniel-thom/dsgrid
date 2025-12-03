(create-project-tutorial)=

# Create a Project

This tutorial shows how to create a dsgrid project, following the example of
[dsgrid-project-StandardScenarios](https://github.com/dsgrid/dsgrid-project-StandardScenarios).

## Prerequisites

- Understanding of {doc}`/getting_started/dsgrid_fundamentals`
- dsgrid installed (see {doc}`/getting_started/installation`)
- Planned datasets identified for your project

## Step 1: Create Repository Structure

Create a repository for your project configuration files. We recommend using git.

Follow the directory structure from {ref}`project-repo-organization`:

```
my_project/
├── dsgrid_project/
│   ├── datasets/
│   │   ├── benchmark/
│   │   ├── historical/
│   │   └── modeled/
│   ├── dimensions/
│   ├── dimension_mappings/
│   └── project.json5
└── README.md
```

## Step 2: Create Project Configuration

Create `dsgrid_project/project.json5` with basic metadata:

```javascript
{
  project_id: "my_project_2024",
  name: "My Project 2024",
  description: "Description of the project",
  datasets: [],
  dimensions: {
    base_dimensions: [],
    supplemental_dimensions: [],
  },
  dimension_mappings: {
    base_to_supplemental: [],
  },
}
```

## Step 3: Define Datasets

List the datasets that will comprise your project:

```javascript
datasets: [
  {
    dataset_id: 'comstock_reference_2022',
    dataset_type: 'modeled',
  },
  {
    dataset_id: 'resstock_conus_2022_reference',
    dataset_type: 'modeled',
  },
  {
    dataset_id: 'tempo_conus_2022',
    dataset_type: 'modeled',
  },
],
```

## Step 4: Define Base Dimensions

Base dimensions define the common dimensionality that all datasets must map to.

Inspect your datasets' dimensions to determine appropriate base dimensions.
Each base dimension needs:

- Dimension type (geography, sector, etc.)
- Name and description
- Records file (CSV)

Example base dimension definition:

```javascript
base_dimensions: [
  {
    "class": "County",
    type: "geography",
    name: "US Counties 2020 L48",
    file: "dimensions/base/counties.csv",
    description: "US counties in the lower 48 states",
  },
  {
    "class": "Sector",
    type: "sector",
    name: "Standard Sectors",
    file: "dimensions/base/sectors.csv",
    description: "Commercial, Residential, Industrial, Transportation",
  },
]
```

## Step 5: Define Supplemental Dimensions

Supplemental dimensions provide alternative aggregations for queries:

```javascript
supplemental_dimensions: [
  {
    "class": "State",
    type: "geography",
    name: "US States L48",
    file: "dimensions/supplemental/states.csv",
    description: "US states for aggregation",
  },
  {
    type: "metric",
    name: "End Uses by Fuel Type",
    file: "dimensions/supplemental/end_uses_by_fuel.csv",
    description: "End uses grouped by fuel",
  },
]
```

## Step 6: Create Base-to-Supplemental Mappings

Define mappings from base dimensions to supplemental dimensions:

```javascript
dimension_mappings: {
  base_to_supplemental: [
    {
      description: "Maps US Counties 2020 L48 to State",
      file: "dimension_mappings/base_to_supplemental/county_to_state.csv",
      mapping_type: "many_to_one_aggregation",
      from_dimension: {
        name: "US Counties 2020 L48",
        type: "geography",
      },
      to_dimension: {
        name: "US States L48",
        type: "geography",
      },
    },
  ],
}
```

Create the mapping records file (`county_to_state.csv`):

```text
from_id,to_id
01001,AL
01003,AL
01005,AL
```

## Step 7: Define Dataset Requirements

For each dataset, specify what dimension records it must provide:

```javascript
{
  dataset_id: 'resstock_conus_2022_reference',
  dataset_type: 'modeled',
  required_dimensions: {
    single_dimensional: {
      sector: {
        base: ['res'],
      },
      model_year: {
        base: ['2018'],
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
  },
}
```

## Step 8: Register the Project

Register your project with dsgrid:

```console
$ dsgrid registry projects register \
    --log-message "Register my project" \
    dsgrid_project/project.json5
```

## Next Steps

- Have dataset contributors submit their datasets
- Run queries to produce outputs
- Create derived datasets as needed
- See {doc}`query_project` for querying your project
