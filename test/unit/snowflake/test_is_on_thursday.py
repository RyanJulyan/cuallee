import snowflake.snowpark.functions as F  # type: ignore

from snowflake.snowpark import DataFrame  # type: ignore
from cuallee import Check, CheckLevel


def test_is_on_thursday(snowpark, configurations):
    df = snowpark.range(10).withColumn(
        "date", F.date_from_parts(2022, 1, F.col("id") + 1)
    )
    check = Check(CheckLevel.WARNING, "check_is_on_thursday")
    check.is_on_thursday("DATE")
    check.config = configurations
    rs = check.validate(df)
    assert isinstance(rs, DataFrame)
    assert rs.first().STATUS == "FAIL"
    assert rs.first().VIOLATIONS == 9, "Incorrect calulation of Thursday filters"
