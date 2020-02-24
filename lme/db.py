import os
from urllib import parse

from sqlalchemy import create_engine

from lme.prices import get_data_from_quandl

parse.uses_netloc.append("postgres")
DB_URL = parse.urlparse(os.environ["DATABASE_URL"])


def update_database():
    todo_periodo = get_data_from_quandl()

    engine = create_engine(
        "postgresql+psycopg2://"
        + DB_URL.username
        + ":"
        + DB_URL.password
        + "@"
        + DB_URL.hostname
        + "/"
        + DB_URL.path[1:]
    )

    connection = engine.connect()
    todo_periodo.to_sql("cotacao_lme", connection, if_exists="replace")
    connection.close()


def get_from_database():
    pass
