import pytest

from dsgrid.dataset.dataset_expression_handler import DatasetExpressionHandler, evaluate_expression
from dsgrid.utils.spark import get_spark_session

STACKED_DIMENSION_COLUMNS = ["county", "model_year"]
PIVOTED_COLUMNS = ["elec_cooling", "elec_heating"]


@pytest.fixture
def datasets():
    spark = get_spark_session()
    df1 = spark.createDataFrame(
        [
            {"county": "Jefferson", "model_year": "2030", "elec_cooling": 2, "elec_heating": 3},
            {"county": "Boulder", "model_year": "2030", "elec_cooling": 3, "elec_heating": 4},
            {"county": "Denver", "model_year": "2030", "elec_cooling": 5, "elec_heating": 6},
        ]
    )
    df2 = spark.createDataFrame(
        [
            {"county": "Jefferson", "model_year": "2030", "elec_cooling": 9, "elec_heating": 10},
            {"county": "Boulder", "model_year": "2030", "elec_cooling": 10, "elec_heating": 11},
            {"county": "Denver", "model_year": "2030", "elec_cooling": 11, "elec_heating": 12},
        ]
    )
    dataset1 = DatasetExpressionHandler(df1, STACKED_DIMENSION_COLUMNS, PIVOTED_COLUMNS)
    dataset2 = DatasetExpressionHandler(df2, STACKED_DIMENSION_COLUMNS, PIVOTED_COLUMNS)
    yield {"dataset1": dataset1, "dataset2": dataset2}


def test_dataset_expression_add(datasets):
    df = evaluate_expression("dataset1 + dataset2", datasets).df.cache()
    assert df.count() == 3
    assert df.filter("county == 'Jefferson'").collect()[0].elec_cooling == 11
    assert df.filter("county == 'Boulder'").collect()[0].elec_cooling == 13
    assert df.filter("county == 'Denver'").collect()[0].elec_heating == 18


def test_dataset_expression_mul(datasets):
    df = evaluate_expression("dataset1 * dataset2", datasets).df.cache()
    assert df.count() == 3
    assert df.filter("county == 'Jefferson'").collect()[0].elec_cooling == 18
    assert df.filter("county == 'Boulder'").collect()[0].elec_cooling == 30
    assert df.filter("county == 'Denver'").collect()[0].elec_heating == 72


def test_dataset_expression_sub(datasets):
    df = evaluate_expression("dataset2 - dataset1", datasets).df.cache()
    assert df.count() == 3
    assert df.filter("county == 'Jefferson'").collect()[0].elec_cooling == 7
    assert df.filter("county == 'Boulder'").collect()[0].elec_cooling == 7
    assert df.filter("county == 'Denver'").collect()[0].elec_heating == 6


def test_dataset_expression_union(datasets):
    df = evaluate_expression("dataset1 | dataset2", datasets).df.cache()
    assert df.count() == 6
    assert df.filter("county == 'Jefferson'").count() == 2
    assert df.filter("county == 'Boulder'").count() == 2
    assert df.filter("county == 'Denver'").count() == 2


def test_dataset_expression_combo(datasets):
    df = evaluate_expression("(dataset1 + dataset2) | (dataset1 * dataset2)", datasets).df.cache()
    assert df.count() == 6
    jefferson = df.filter("county == 'Jefferson'").cache()
    assert jefferson.count() == 2
    assert jefferson.collect()[0].elec_cooling == 11
    assert jefferson.collect()[1].elec_cooling == 18
    boulder = df.filter("county == 'Boulder'").cache()
    assert boulder.count() == 2
    assert boulder.collect()[0].elec_cooling == 13
    assert boulder.collect()[1].elec_cooling == 30
    denver = df.filter("county == 'Denver'").cache()
    assert denver.count() == 2
    assert denver.collect()[0].elec_heating == 18
    assert denver.collect()[1].elec_heating == 72
