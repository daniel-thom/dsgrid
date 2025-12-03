# dsgrid Documentation

**dsgrid** (Demand-Side Grid) is an open-source toolkit for assembling and managing
bottom-up demand-side datasets for grid modeling and planning. It enables the compilation
of high-resolution load datasets suitable for forward-looking power system analyses.

For more information and completed work products, see the
[NREL dsgrid page](https://www.nrel.gov/analysis/dsgrid.html).

```{note}
dsgrid is under active development and does not yet have a formal package release.
Details listed here are subject to change.
```

## Getting Started

New to dsgrid? Start with {doc}`getting_started/dsgrid_fundamentals` to understand the
core concepts, then choose the section below that matches your goals.

::::{grid} 2
:gutter: 3

:::{grid-item-card} Working with Published Data
:link: published_data/index
:link-type: doc

Find and download datasets, explore available data, and use published dsgrid outputs.

*For data users who want to access existing datasets.*
:::

:::{grid-item-card} Datasets
:link: datasets/index
:link-type: doc

Register datasets, map and query data, and submit datasets to projects.

*For dataset submitters and analysts working with data.*
:::

:::{grid-item-card} Managing Projects
:link: projects/index
:link-type: doc

Create projects, coordinate dataset submissions, run queries, and create derived
datasets.

*For project coordinators who manage dsgrid projects.*
:::

:::{grid-item-card} Software Reference
:link: software_reference/index
:link-type: doc

CLI commands, software architecture, data models, and Apache Spark guidance.

*For developers and advanced users.*
:::

::::

## Additional Resources

- {doc}`publications` -- Research papers and related publications
- {doc}`citation` -- How to cite dsgrid and attribute data
- {doc}`contact` -- Get in touch with the team

## Indices and Tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`

```{toctree}
:maxdepth: 2
:hidden:
:caption: Contents

getting_started/index
published_data/index
datasets/index
projects/index
software_reference/index
publications
citation
contact
```
