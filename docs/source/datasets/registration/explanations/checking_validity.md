(checking-validity)=

# Checking Validity

dsgrid validates datasets during registration to ensure data consistency and
completeness. This page explains the validation process and how to handle errors.

## What dsgrid Validates

During registration, dsgrid checks:

1. **Dimension consistency**: Values in data files match dimension records
2. **Required combinations**: All expected dimension combinations have data or are
   declared as missing
3. **Data format**: Files conform to the declared schema
4. **Metadata completeness**: Required configuration fields are present

## Running Validation

Validation occurs automatically during registration:

```console
$ dsgrid registry datasets register \
    --log-message "Register my dataset" \
    dataset.json5
```

For large datasets, use Spark:

```console
$ spark-submit --master=spark://<master>:7077 \
    $(which dsgrid-cli.py) registry datasets register \
    --log-message "Register my dataset" \
    dataset.json5
```

## Common Validation Errors

### Dimension Record Mismatch

Data files contain values not in your dimension records.

**Error**: `Found geography values not in dimension: ['99999', '00000']`

**Solution**: Either add the missing records to your dimension file or fix the
data values.

### Missing Dimension Combinations

Expected dimension combinations don't have data.

**Error**: `Missing dimension combinations detected`

**Solution**: Either fix data gaps or declare them as missing associations
(see below).

### Type Mismatch

Column data types don't match expectations.

**Error**: `Column 'geography' expected string, got int64`

**Solution**: Explicitly specify column types in your configuration:

```javascript
data_file: {
  path: "load_data.csv",
  columns: [
    {
      name: "geography",
      data_type: "STRING",
    },
  ],
}
```

## Missing Associations

Datasets may legitimately lack data for certain dimension combinations. For example,
a building model might not have data for building types that don't exist in certain
regions.

Instead of failing validation, you can declare these combinations as **missing
associations**.

### Iterative Workflow

1. **Attempt registration** without declaring missing associations:

   ```console
   $ dsgrid registry datasets register -l "Test registration" dataset.json5
   ```

2. **Review the output** if registration fails. dsgrid writes:

   - `<dataset_id>__missing_dimension_record_combinations.parquet`: All missing
     combinations
   - `./missing_associations/`: Per-dimension CSV files with minimal patterns

3. **Analyze the patterns**. dsgrid logs patterns explaining the gaps:

       Pattern 1: geography | subsector = 01001 | large_hotel (150 missing rows)
       Pattern 2: subsector = warehouse (3000 missing rows)

4. **Choose your approach**:

   - Use the generated Parquet file (comprehensive but large)
   - Use the per-dimension CSVs (compact, easier to review)
   - Create custom files based on your understanding

5. **Declare missing associations** in your configuration:

   ```javascript
   table_schema: {
     data_schema: { ... },
     data_file: { path: "load_data.parquet" },
     missing_associations: [
       "./missing_associations",
     ],
   }
   ```

6. **Re-run registration**:

   ```console
   $ dsgrid registry datasets register -l "Register with missing" dataset.json5
   ```

### Missing Associations File Format

Files can be CSV or Parquet with columns for dimension types (excluding time).

**Full format** (all dimensions):

    +---------+------+-----------+--------+----------+------------+
    |geography|sector|  subsector|  metric|model_year|weather_year|
    +---------+------+-----------+--------+----------+------------+
    |    01001|   com|large_hotel|heating |      2020|        2018|

**Minimal format** (only varying dimensions):

    +---------+-----------+
    |geography|  subsector|
    +---------+-----------+
    |    01001|large_hotel|

### Using Directories

Create separate files for different dimension combinations:

    missing_associations/
    ├── geography__subsector.csv
    └── subsector__metric.csv

### Custom Base Directories

Specify different base directories for missing association files:

```console
$ dsgrid registry datasets register dataset.json5 \
    -l "Register dataset" \
    -M /path/to/missing/files
```

## Validation Tips

### Start Small

Test with a subset of your data first to catch configuration issues early.

### Use Explicit Types

Always specify column data types for CSV files to avoid type inference issues.

### Review Dimension Files

Ensure dimension record files match exactly what's in your data. Common issues:

- Extra whitespace
- Case sensitivity
- Missing leading zeros in numeric codes

### Check Time Zones

Verify timestamp handling:

- Parquet timestamps should be UTC
- Time zone configuration should match your data

### Preserve Data Types

When preparing data:

- Keep geography codes as strings (preserve leading zeros)
- Keep model_year/weather_year as strings or integers (be consistent)
