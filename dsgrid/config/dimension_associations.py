import itertools
import logging
from pathlib import Path
from typing import Dict

from pyspark.sql.types import StringType

from dsgrid.dimension.base_models import DimensionType
from dsgrid.exceptions import DSGInvalidDimensionAssociation
from dsgrid.utils.spark import read_dataframe


logger = logging.getLogger(__name__)


class DimensionAssociations:
    """Interface to a project's dimension associations"""

    def __init__(self, associations: Dict):
        # This has the format {(DimensionType1, DimensionType2, ..., DimensionTypeN): df}
        # The keys are sorted by DimensionType so that the caller's order doesn't matter.
        self._associations = associations

    def __bool__(self):
        return bool(self._associations)

    def __len__(self):
        return len(self._associations)

    @classmethod
    def load(cls, path: Path, association_files):
        """Load dimension associations from a path.

        Parameters
        ----------
        path: Path
        association_files : list
            List of filenames with paths relative to path

        Returns
        -------
        DimensionAssociations

        """
        associations = {}
        for association_file in association_files:
            filename = path / association_file
            records = read_dataframe(filename, cache=True)
            for column in records.columns:
                tmp = column + "tmp_name"
                records = (
                    records.withColumn(tmp, records[column].cast(StringType()))
                    .drop(column)
                    .withColumnRenamed(tmp, column)
                )
            types = tuple(DimensionType(x) for x in sorted(records.columns))
            associations[types] = records
            logger.debug("Loaded dimension associations from %s %s", path, records.columns)

        return cls(associations)

    def get_associations(self, *dimensions):
        """Return the records for this dimension association.

        Parameters
        ----------
        dimensions : tuple
            Any number of instances of DimensionType

        Returns
        -------
        pyspark.sql.DataFrame | None
            Returns None if there is no table matching dimensions.

        """
        # Try a direct match and then check for a subset.
        table = self._associations.get(tuple(sorted(dimensions)))
        if table is not None:
            return table

        caller_dims = set(dimensions)
        for association_dims, table in self._associations.items():
            if not caller_dims.difference(association_dims):
                # This assumes that if there are multiple matches, all tables have the same data.
                return table.select(*(x.value for x in dimensions))

        return None

    def get_filtered_associations(self, filter_dim, filter_value, *dimensions):
        """Return the records for this dimension association filtered by another dimension with
        a specific value.

        Parameters
        ----------
        filter_dim: DimensionType
        filter_value: DimensionType
        dimensions : tuple
            Any number of instances of DimensionType

        Returns
        -------
        pyspark.sql.DataFrame | None

        Examples
        --------
        >>> da = DimensionAssociations(Path("src_dir"), ["a1.csv", "a2.csv", "a3.csv"]
        >>> da.get_filtered_associations(
        ...     DimensionType.METRIC,
        ...     DimensionType.SUBSECTOR,
        ...     filter_dim=DimensionType.DATA_SOURCE,
        ...     filter_value="comstock",
        ... ).show(n=2)
        +--------------------+------------+
        |              metric|   subsector|
        +--------------------+------------+
        |district_cooling_...|   warehouse|
        |district_cooling_...|small_office|
        +--------------------+------------+

        """
        table = self.get_associations(*dimensions)
        if table is None:
            return None

        filter_col = filter_dim.value
        for dimension in dimensions:
            tmp = self.get_associations(filter_dim, dimension)
            if tmp is None:
                raise DSGInvalidDimensionAssociation(
                    f"No association is stored for {filter_dim} and {dimension}"
                )
            table = (
                table.join(tmp, dimension.value)
                .filter(f"{filter_col} = '{filter_value}'")
                .drop(filter_col)
            )
        return table

    def get_associations_by_data_source(self, data_source, *dimensions):
        """Return the records for this dimension association filtered a data source.

        Parameters
        ----------
        data_source: str
            Record for DimensionType.DATA_SOURCE
        dimensions : tuple
            Any number of instances of DimensionType

        Returns
        -------
        pyspark.sql.DataFrame | None

        """
        return self.get_filtered_associations(DimensionType.DATA_SOURCE, data_source, *dimensions)

    def has_associations(self, *dimensions):
        """Return True if these dimension associations are stored.

        Parameters
        ----------
        dimensions : tuple
            Any number of instances of DimensionType

        Returns
        -------
        bool

        """
        return self.get_associations(*dimensions) is not None

    def iter_associations(self):
        """Yields the stored dimension types with their association tables as a tuple."""
        for dimensions, table in self._associations.items():
            yield dimensions, table

    def get_full_join_by_data_source(self, data_source):
        tables = []
        for dims, val in self._associations.items():
            if DimensionType.DATA_SOURCE in dims:
                continue
            table = self.get_associations_by_data_source(data_source, *dims)
            tables.append(table)

        table = tables[0]
        if len(tables) > 1:
            for other in tables[1:]:
                on_columns = list(set(other.columns).intersection(table.columns))
                if on_columns:
                    table = table.join(other, on=on_columns, how="cross")
                else:
                    table = table.join(other, how="cross")
        return table
