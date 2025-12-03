(dataset-submittal-explanations)=

# Explanations

This page explains concepts related to dataset submittal.

## Registration vs Submittal

**Registration** catalogs a dataset with dsgrid:

- Records metadata (dimensions, format, origin)
- Validates data file structure
- Stores dataset in the registry

**Submittal** connects a dataset to a project:

- Validates against project requirements
- Registers dimension mappings
- Makes dataset available for project queries

You can register without submitting (useful for testing or standalone datasets),
but submittal requires prior registration.

## When Spark is Needed

Submittal requires Apache Spark because it involves:

- Reading and validating large data files
- Checking dimension mappings across all records
- Verifying project requirement coverage

For large datasets, use an appropriate Spark cluster on NREL HPC.

See {doc}`/software_reference/apache_spark` for setup guidance.

## Project Requirements

Projects define requirements that submitted datasets must meet.

### Required Dimensions

Projects specify which dimension records each dataset must provide.

Example from a project config:

```JavaScript
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

This means:

- Dataset must map to sector record `trans`
- Dataset subsectors must map to the supplemental dimension

### Dimension Mapping Requirements

For dimensions that differ from project base dimensions, you must provide
mappings that:

1. Cover all records in your dataset
2. Map to valid project dimension records
3. Use an appropriate mapping type

## How Validation Works

During submittal, dsgrid performs these checks:

1. **Schema validation**: Config files match expected structure
2. **Dimension validation**: Records exist and are valid
3. **Mapping validation**: All mappings resolve correctly
4. **Data validation**: Data matches declared dimensions
5. **Requirement validation**: Project requirements are satisfied

### Validation Order

1. Register dimension mappings (if new)
2. Validate dataset dimensions map correctly
3. Validate data content against dimensions
4. Check project requirements

If any step fails, the entire submittal is rolled back.

## Offline vs Online Mode

dsgrid supports different submission modes:

**Offline mode** (recommended for testing):

- Validates without modifying the registry
- Useful for checking configurations before committing
- Can be run without full Spark cluster

**Online mode**:

- Modifies the registry
- Registers mappings and dataset submission
- Requires full validation pass

## Testing Workflows

For large or complex datasets:

1. **Validate config files first**:

   ```console
   $ dsgrid registry datasets validate dataset.json5
   ```

2. **Test with subset data**: Create a smaller test dataset to catch issues
   before processing full data

3. **Use checkpointing**: For mapping operations, use mapping plans with
   persistence (see {doc}`/datasets/mapping_query/tutorial/data_mapping`)

4. **Iterate on mappings**: Verify mappings cover all cases before submittal

## Common Issues

### Missing Dimension Records

Dataset contains dimension values not in dimension records.

**Solution**: Add missing records to dimension files or fix data.

### Unmapped Records

Some dataset records don't have mappings to project dimensions.

**Solution**: Add mappings or map to `null` to exclude.

### Type Mismatches

Column types don't match expectations (e.g., integer geography codes).

**Solution**: Explicitly specify types in config (see {doc}`/datasets/registration/explanations/input_formats`).

### Requirement Mismatch

Dataset doesn't cover required project dimension records.

**Solution**: Review project requirements and ensure mappings produce
required records.
