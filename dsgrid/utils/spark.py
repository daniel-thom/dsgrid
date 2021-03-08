"""Spark helper functions"""

import logging
import multiprocessing

from pyspark.sql import SparkSession


logger = logging.getLogger(__name__)


def init_spark(name, mem="5gb", num_cpus=None):
    """Initialize a SparkSession."""
    if num_cpus is None:
        num_cpus = multiprocessing.cpu_count()

    return SparkSession.builder \
        .master('local') \
        .appName(name) \
        .config('spark.executor.memory', mem) \
        .config("spark.cores.max", str(num_cpus)) \
        .getOrCreate()


def sql(query):
    """Run a SQL query with Spark.

    Parameters
    ----------
    query : str

    Returns
    -------
    pyspark.sql.DataFrame

    """
    return SparkSession.getActiveSession().sql(query)


def sql_from_sqlalchemy(query):
    """Run a SQL query with Spark where the query was generated by sqlalchemy.

    Parameters
    ----------
    query : sqlalchemy.orm.query.Query

    Returns
    -------
    pyspark.sql.DataFrame

    """
    logger.debug("sqlchemy query = %s", query)
    return sql(str(query).replace("\"", ""))
