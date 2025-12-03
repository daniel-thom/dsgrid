(dataset-registration-prerequisites)=

# Prerequisites

Before registering a dataset with dsgrid, ensure you have the following.

## Software Requirements

1. **dsgrid installed**: Follow {doc}`/getting_started/installation`

2. **dsgrid configured**: Point to your registry

   ```console
   $ dsgrid config create sqlite:///path/to/registry.db
   ```

## Data Requirements

Your data must be in one of the supported formats:

### File Formats

- **Parquet** (recommended): Columnar format, efficient for large datasets
- **CSV**: Supported but not recommended for large datasets

### Data Structure

dsgrid supports two table schemas:

1. **One-table format**: All data and dimensions in a single file
2. **Two-table format** (standard): Separate files for time-series data and dimension lookups

See {doc}`explanations/input_formats` for detailed format specifications.

### Dimension Requirements

Your dataset must define values for all eight dsgrid dimension types:

- scenario
- model_year
- weather_year
- geography
- time
- sector
- subsector
- metric

Dimensions can be "trivial" (single element) if your data doesn't vary along that
dimension.

## Project Requirements (Optional)

If you plan to submit your dataset to a project, you should:

1. **Know the target project**: Identify which project you're submitting to
2. **Review project requirements**: Check what dimension records the project expects
3. **Plan dimension mappings**: Determine what mappings are needed between your
   dimensions and the project's base dimensions

You can register a dataset without a project, but you'll need mappings when you
later submit to a project.

## Computational Resources

### For Registration Only

Dataset registration involves metadata operations and data validation. For small
datasets, a personal computer is sufficient.

### For Large Datasets

Large datasets may require:

- More memory for validation
- Apache Spark for data operations

See {doc}`/software_reference/apache_spark` for Spark setup if needed.
