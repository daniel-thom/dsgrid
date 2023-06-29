************************
Create a derived dataset
************************
In this tutorial you will learn how to query a dsgrid project to produce and register a derived
dataset. The tutorial uses the comstock_conus_2022_projected derived dataset from
`dsgrid-project-StandardScenarios <https://github.com/dsgrid/dsgrid-project-StandardScenarios>`_
as an example.

You can run all commands in this tutorial except the last one on NREL's HPC Eagle cluster (the
dataset is already registered).

The ``comstock_conus_2022_reference`` dataset has load data for a single year. The query in this
tutorial applies the ``aeo2021_reference_commercial_energy_use_growth_factors`` dataset to project
the load values through 2050.

Steps
=====
ssh to a login node to begin the tutorial.

1. Follow the instructions at :ref:`how-to-run-dsgrid-eagle` if you have not already done so.

2. Copy the query file for this derived dataset from `github
<https://github.com/dsgrid/dsgrid-project-StandardScenarios/blob/main/dsgrid_project/derived_datasets/comstock_conus_2022_projected.json5>`_.

3. Run the query. TODO: follow example from dsgrid-project-StandardScenarios
   dsgrid_project/build_registry/build_registry.sh
