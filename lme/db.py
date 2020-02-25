import os
from urllib import parse

from sqlalchemy import create_engine, MetaData, Table, Column, DateTime, Float

from lme.prices import get_data_from_quandl

parse.uses_netloc.append("postgres")
DB_URL = parse.urlparse(os.environ["DATABASE_URL"])

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


def update_database():
    todo_periodo = get_data_from_quandl()

    connection = engine.connect()
    todo_periodo.to_sql("cotacao_lme", connection, if_exists="replace")
    connection.close()


def create():
    meta = MetaData()

    cotacao_lme = Table(
        'cotacao_lme', meta,
        Column('Date', DateTime(timezone=False)),
        Column('Cobre', Float),
        Column('Zinco', Float),
        Column('Aluminio', Float),
        Column('Chumbo', Float),
        Column('Estanho', Float),
        Column('Niquel', Float),
        Column('Dolar', Float),
    )

    meta.create_all(engine)

    print(f'Tabela {cotacao_lme} criada')
    update_database()
    print('Cotação atualizada')
