(required-dimensions)=

# Required Dimensions

Every dsgrid dataset must define values for all eight dimension types. This page
explains dimension requirements and how to handle different scenarios.

## Dimension Types

dsgrid requires these dimension types for every dataset:

scenario
: What scenario is being described (if any). For historical data, use a trivial
  dimension with a single record like "historical" or "baseline".

model_year
: What historical or future year is being described. Can be a single year or
  range of years.

weather_year
: What year's weather patterns are being used. Often the same as model_year for
  historical data, or a fixed year (e.g., 2012) for projections.

geography
: What geographic entity is being summarized. Common choices include:

  - Counties (FIPS codes)
  - States
  - Census divisions
  - Custom regions

time
: How within-year data is provided. Options include:

  - DateTime (hourly timestamps)
  - Annual (one value per year)
  - Representative period (e.g., one week per month)

sector
: High-level categorization: Commercial, Residential, Industrial, Transportation.

subsector
: Specific types within a sector: building types, industries, transportation modes.

metric
: What is being measured: energy by end-use, population, stock counts, etc.

## Trivial Dimensions

Not all dimensions need to vary in your dataset. A **trivial dimension** has only
one record.

Examples:

- Historical data typically has a trivial `scenario` dimension
- Annual datasets may have trivial `weather_year`
- Sector-specific data has a trivial `sector` dimension

Declaring trivial dimensions in `dataset.json5`:

```javascript
trivial_dimensions: [
  "sector",
  "weather_year",
],
```

Trivial dimensions are not stored in data files but must be defined in the
dimension configuration.

## Dimension Records

Each dimension (except time) requires a records table, usually a CSV file, with
at minimum `id` and `name` columns:

```text
id,name
com,Commercial
res,Residential
ind,Industrial
trans,Transportation
```

Additional columns can provide supplemental information:

```text
id,name,fuel_id,unit
electricity_heating,Electric Heating,electricity,kWh
natural_gas_heating,Natural Gas Heating,natural_gas,therms
```

## Project Requirements

When submitting to a project, your dataset must meet the project's dimension
requirements. Projects specify:

Base Dimensions
: The dimensions all datasets must map to.

Required Records
: Specific records your dataset must provide (possibly after mapping).

Check the project's `required_dimensions` section to understand what's expected.

Example project requirement:

```javascript
required_dimensions: {
  single_dimensional: {
    sector: {
      base: ["trans"],
    },
    subsector: {
      supplemental: [
        {
          name: "Subsectors by Sector Collapsed",
          record_ids: ["transportation_subsectors"],
        },
      ],
    },
  }
}
```

This tells you:

- The dataset must provide sector record `trans`
- Subsector records must map to the `transportation_subsectors` supplemental dimension

## Identifying Required Records

To find what records a project expects:

**Using the CLI:**

```console
$ dsgrid registry projects show <project-id>
```

**Using the Project Viewer:**

Start the project viewer (see {doc}`/published_data/working_with_published_datasets/tutorial`)
and filter the dimension tables.

**Inspecting the repository:**

Browse the project's dimension files in its GitHub repository. For example:

[StandardScenarios dimensions](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/dsgrid_project/dimensions)

## Dimension Matching

Your dataset dimensions can either:

1. **Match exactly**: Use the same dimension ID as the project
2. **Map to the project**: Define mappings from your records to project records

If your dimension differs from the project, you'll need to create dimension
mappings. See {doc}`/datasets/mapping_query/index` for mapping details.
