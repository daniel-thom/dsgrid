(dataset-submittal-tutorial)=

# Tutorial

This tutorial walks through submitting a registered dataset to a dsgrid project.

## Prerequisites

Before submitting:

1. **Dataset registered**: Your dataset must be registered with dsgrid
   (see {doc}`/datasets/registration/index`)
2. **Project identified**: Know which project you're submitting to
3. **Dimension mappings prepared**: Create mappings for any dimensions that
   differ from the project's base dimensions
4. **Spark available**: Submittal requires Spark for data validation
   (see {doc}`/software_reference/apache_spark`)

## Option 1: Combined Register and Submit

If you haven't registered your dataset yet, you can register and submit in one step:

```console
$ spark-submit --master=spark://<master>:7077 \
    $(which dsgrid-cli.py) registry projects register-and-submit-dataset \
    --project-id my-project-id \
    --dimension-mapping-file dimension_mappings.json5 \
    --log-message "Register and submit my dataset" \
    dataset.json5
```

This command:

1. Registers the dataset
2. Registers any new dimension mappings
3. Submits the dataset to the project
4. Validates data against project requirements

## Option 2: Submit Previously Registered Dataset

If your dataset is already registered:

```console
$ spark-submit --master=spark://<master>:7077 \
    $(which dsgrid-cli.py) registry projects submit-dataset \
    --project-id my-project-id \
    --dataset-id my-dataset-id \
    --dimension-mapping-file dimension_mappings.json5 \
    --log-message "Submit my dataset to project"
```

## Preparing Dimension Mappings

Create a `dimension_mappings.json5` file for dimensions that need mapping:

```JavaScript
[
  {
    description: "My geography to project geography",
    file: "dimension_mappings/geo_mapping.csv",
    dimension_type: "geography",
    mapping_type: "many_to_one_aggregation",
  },
  {
    description: "My model years to project model years",
    file: "dimension_mappings/year_mapping.csv",
    dimension_type: "model_year",
    mapping_type: "many_to_many_explicit_multipliers",
  },
]
```

### Mapping Records

Create CSV files defining the mappings.

**many_to_one_aggregation** (e.g., counties to state):

```text
from_id,to_id
01001,01001
01003,01003
02013,          # null means exclude from project
```

**many_to_many_explicit_multipliers** (e.g., year interpolation):

```text
from_id,to_id,from_fraction
2018,2018,1.0
2018,2019,0.5
2020,2019,0.5
2020,2020,1.0
```

See {doc}`/datasets/mapping_query/explanations` for mapping type details.

## Understanding Validation

During submittal, dsgrid validates:

1. **Dimension coverage**: Dataset provides required dimension records
2. **Mapping validity**: All dataset records have valid mappings to project
3. **Data consistency**: Data values are consistent with declared dimensions

Validation can take significant time for large datasets (up to an hour on HPC).

## Handling Validation Errors

### Dimension Mismatch

If dimension records don't meet project requirements:

**Error**: `Dataset missing required dimension records`

**Solution**:

1. Check `required_dimensions` in the project config
2. Ensure your dimension mappings cover all required records
3. Add missing records or update mappings

### Mapping Coverage

If some dataset records don't have mappings:

**Error**: `Records without mappings found`

**Solution**:

1. Add mappings for uncovered records
2. Or map uncovered records to `null` (they'll be excluded)

## Testing Before Submittal

For large datasets, test incrementally:

1. **Test registration first** to catch config errors early
2. **Use a smaller data subset** for initial submittal tests
3. **Use mapping plans** for checkpointing (see {doc}`/datasets/mapping_query/tutorial/data_mapping`)

## After Successful Submittal

Once submitted, your dataset:

- Is available for project queries
- Can be mapped to project dimensions
- Can be included in derived datasets

To verify:

```console
$ dsgrid registry projects show my-project-id
```

This lists all datasets submitted to the project.

## Next Steps

- To query project data, see {doc}`/datasets/mapping_query/index`
- To map your dataset, see {doc}`/datasets/mapping_query/tutorial/data_mapping`
- For project management, see {doc}`/projects/index`
