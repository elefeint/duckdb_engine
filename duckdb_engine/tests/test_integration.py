import pandas as pd
from pytest import mark, raises
from sqlalchemy import text
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.exc import ProgrammingError


def test_integration(engine: Engine) -> None:
    with engine.connect() as conn:
        execute = (
            conn.exec_driver_sql if hasattr(conn, "exec_driver_sql") else conn.execute
        )
        params = ("test_df", pd.DataFrame([{"a": 1}]))
        execute("register", params)  # type: ignore[operator]

        conn.execute(text("select * from test_df"))


@mark.remote_data
def test_motherduck():
    engine = create_engine("duckdb:///md:motherdb?motherduck_token=motherduckdb_token")

    with raises(
        ProgrammingError,
        match="Jwt is not in the form of Header.Payload.Signature with two dots and 3 sections",
    ):
        with engine.connect() as conn:
            pass
