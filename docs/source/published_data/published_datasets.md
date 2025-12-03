(published-datasets)=

# Published Datasets

This page lists published dsgrid datasets and projects.

## TEMPO County-level EV Charging Profiles

The TEMPO project provides hourly electric vehicle charging projections documented in a
2023 NREL technical report.

### Overview

- **Geographic scope**: 3,108 counties in the contiguous United States
- **Temporal coverage**: 2024-2050 projections (two-year intervals)
- **Weather year**: 2012 actual meteorological year (AMY)
- **Resolution**: 720 household and vehicle type combinations
- **Charging types**: L1 & L2 and DC Fast Charging (DCFC)
- **Unit**: Megawatt-hours (MWh)

### Adoption Scenarios

The dataset includes three adoption scenarios:

1. **AEO Reference Case**: Aligned with 2018 EIA Annual Energy Outlook projections
2. **EFS High Electrification**: Based on NREL's Electrification Futures Study
3. **All EV Sales by 2035**: Assumes 100% light-duty EV sales by 2035

### Access

Data is available on:

- **OEDI**: ``s3://nrel-pds-dsgrid/tempo/``
- **NREL Kestrel**: Available in multiple aggregation levels

For more details, see the [TEMPO project documentation](https://github.com/dsgrid/dsgrid-project-StandardScenarios/blob/main/tempo_project/README.md).

```{note}
The data represents a theoretical upper bound based on "ubiquitous charger access"
and "immediate charging" behavior. Vehicles are assumed to charge immediately after
trips complete, which reflects unrealistic charging frequency but establishes a
maximum bound.
```

## Project Repositories

Active dsgrid projects are maintained in GitHub repositories:

### StandardScenarios Project

The primary dsgrid project containing multiple sector models and scenarios.

- **Repository**: [dsgrid-project-StandardScenarios](https://github.com/dsgrid/dsgrid-project-StandardScenarios)
- **Contents**: Project configuration, dataset definitions, dimension mappings

### Industrial Energy Futures (IEF) Project

Project focused on industrial energy modeling.

- **Repository**: [dsgrid-project-IEF](https://github.com/dsgrid/dsgrid-project-IEF)

## Additional Datasets

The StandardScenarios project includes multiple source datasets:

### Historical Datasets

- EIA 861 Utility Customer Sales by State and Sector

### Modeled Datasets

- **ResStock**: Residential building energy use from NREL's ResStock model
- **ComStock**: Commercial building energy use from NREL's ComStock model
- **AEO Growth Factors**: Annual Energy Outlook-based growth projections

See the [StandardScenarios datasets directory](https://github.com/dsgrid/dsgrid-project-StandardScenarios/tree/main/dsgrid_project/datasets)
for the complete list of available datasets.
