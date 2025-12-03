(input-formats)=

# Input Formats

dsgrid supports multiple data formats to accommodate different dataset structures.
This page describes the supported formats and their requirements.

## File Formats

### Parquet (Recommended)

Apache Parquet is the recommended format for dsgrid datasets:

- Efficient columnar storage
- Built-in compression (Snappy recommended)
- Preserves data types
- Fast read performance

Recommendations:

- Target 128 MiB per Parquet file
- Enable Snappy compression
- Use appropriate precision (32-bit vs 64-bit floats)

### CSV

CSV files are supported but not recommended for large datasets:

- Type inference may cause issues (e.g., FIPS codes losing leading zeros)
- Slower read performance
- Larger file sizes

When using CSV, explicitly specify column data types in your configuration to
avoid type inference problems.

## Table Schemas

### One-Table Format

All metric data and dimension records are stored in a single file.

Structure:

    +-------------------+---------+------------------+--------------------+-------+
    |          timestamp|geography|          scenario|           subsector| value |
    +-------------------+---------+------------------+--------------------+-------|
    |2011-12-31 22:00:00|    01001|      efs_high_ldv|full_service_rest...|  1.234|
    |2011-12-31 22:00:00|    01001|      efs_high_ldv|      primary_school|  2.345|
    +-------------------+---------+------------------+--------------------+-------+

Configuration:

```javascript
table_schema: {
  data_schema: {
    data_schema_type: "one_table",
    table_format: {
      format_type: "unpivoted",
    },
  },
  data_file: {
    path: "load_data.parquet",
  },
}
```

### Two-Table Format (Standard)

Data is split into two files:

1. **load_data.parquet**: Time-series metric data with an `id` column
2. **load_data_lookup.parquet**: Dimension records linked by `id`

This format is more efficient for large datasets because:

- Time arrays can be shared across dimension combinations
- Dimension information isn't repeated for every timestamp

**load_data.parquet**:

    +-------------------+----+-------------------+--------------------+
    |          timestamp|  id|            heating|             cooling|
    +-------------------+----+-------------------+--------------------+
    |2012-01-01 00:00:00|9106| 0.2143171631469727|0.001987764734408426|
    |2012-01-01 01:00:00|9106| 0.3290653818000351|9.035294172606012E-5|
    +-------------------+----+-------------------+--------------------+

**load_data_lookup.parquet**:

    +---------+------+----------+-------+
    |geography|sector| subsector|     id|
    +---------+------+----------+-------+
    |    53061|   com|  Hospital|      1|
    |    53053|   com|  Hospital|      2|
    +---------+------+----------+-------+

Configuration:

```javascript
table_schema: {
  data_schema: {
    data_schema_type: "standard",
    table_format: {
      format_type: "pivoted",
      pivoted_dimension_type: "metric",
    },
  },
  data_file: {
    path: "./load_data.parquet",
  },
  lookup_data_file: {
    path: "./load_data_lookup.parquet",
  },
}
```

## Table Formats

### Pivoted

One dimension's record IDs become column names. Common for metric dimensions.

Benefits:

- Reduces row repetition
- Saves storage space

Example with pivoted metric:

    +-------------------+----+--------+--------+
    |          timestamp|  id| heating| cooling|
    +-------------------+----+--------+--------+
    |2012-01-01 00:00:00|   1|    1.23|    0.45|

### Unpivoted

All dimensions are columns, with a single `value` column.

Benefits:

- Simpler query structure
- Works when no sensible pivot dimension exists

Example:

    +-------------------+---------+--------+-------+
    |          timestamp|geography|  metric| value |
    +-------------------+---------+--------+-------+
    |2012-01-01 00:00:00|    01001| heating|   1.23|
    |2012-01-01 00:00:00|    01001| cooling|   0.45|

## Time Formats

### DateTime

Standard timestamps, typically hourly:

- Column type: `TIMESTAMP` (Parquet logical type)
- Must be adjusted to UTC in Parquet files
- Spark type: `TimestampType`

### Annual

One value per model year:

    [2020, 2021, 2022]

### Representative Period

Timestamps represent multiple periods. Supported format:

**one_week_per_month_by_hour**:

- One week of hourly data per month
- Times represent local time (no time zone)
- No daylight savings adjustments

Columns:

- `month`: 1-12 (January = 1)
- `day_of_week`: 0-6 (Monday = 0)
- `hour`: 0-23 (midnight = 0)

    +---+-----+-----------+----+-------+
    | id|month|day_of_week|hour| value |
    +---+-----+-----------+----+-------+
    |  1|    4|          0|   0|    1.0|
    |  1|    4|          0|   1|    1.0|

## Column Requirements

### Data Types

- Dimension columns (except `model_year`, `weather_year`): **string**
- `model_year`, `weather_year`: string or integer
- Metric values: float (32-bit or 64-bit)

Specifying column types explicitly:

```javascript
data_file: {
  path: "load_data.csv",
  columns: [
    {
      name: "geography",
      data_type: "STRING",
    },
    {
      name: "value",
      data_type: "FLOAT",
    },
  ],
}
```

### Custom Column Names

If your data uses different column names, map them to dsgrid dimension types:

```javascript
columns: [
  {
    name: "county",              // actual name in file
    dimension_type: "geography", // dsgrid dimension type
  },
  {
    name: "end_use",
    dimension_type: "metric",
  },
]
```

### Ignoring Columns

Drop columns that aren't needed:

```javascript
data_file: {
  path: "load_data.parquet",
  ignore_columns: ["internal_id", "notes"],
}
```
