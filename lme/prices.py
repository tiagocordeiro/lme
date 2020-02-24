import os
from datetime import timedelta, datetime
from urllib import parse

import pandas as pd
import psycopg2
import quandl
from dotenv import load_dotenv

load_dotenv()

quandl.ApiConfig.api_key = os.environ.get("QUANDL_KEY")


def get_latest_values_date():
    """
    Return the last date that has all the values.
    :return: Timestamp
    """
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
    )

    query = """
            SELECT * FROM cotacao_lme
            WHERE cotacao_lme NOTNULL
            ORDER BY "Date" DESC LIMIT 1
            """

    values = pd.read_sql(query, conn)

    values.columns = [
        "Data",
        "Cobre",
        "Zinco",
        "Aluminio",
        "Chumbo",
        "Estanho",
        "Niquel",
        "Dolar",
    ]

    df = pd.DataFrame(values)

    df["Data"] = latest = pd.to_datetime(df["Data"], utc=True)

    df = df.set_index(df["Data"])
    df = df.drop("Data", axis=1)

    df.fillna(method="ffill", inplace=True)
    df.fillna(method="bfill", inplace=True)

    return latest[0]


def date_range_builder(weeks=4):
    """
    returns a dictionary with start and end dates for a period of weeks
    :param weeks: week amount, the default is 4
    :return: :class:`dict`
    :example:
    >>> from lme.prices import get_latest_values_date, date_range_builder
    >>> ultimo_periodo = date_range_builder()
    >>> type(ultimo_periodo)
    <class 'dict'>
    >>> ultimo_periodo['inicio']
    Timestamp('2020-01-24 00:00:00+0000', tz='UTC')
    """
    fim = get_latest_values_date()
    inicio = fim - timedelta(weeks=weeks)

    dia_semana = fim.isoweekday()
    semana_numero = fim.strftime("%U")

    if semana_numero == "00":
        fim = datetime.now() - timedelta(days=fim.isoweekday())

    if dia_semana == 1:
        fim = datetime.now() - timedelta(days=3)

    return {"inicio": inicio, "fim": fim}


def get_data_from_quandl():
    """
    Return dataframe of requested dataset from Quandl.
    :return: :class:`pandas.DataFrame`
    """
    todo_periodo = quandl.get(
        [
            "LME/PR_CU.2",
            "LME/PR_ZI.2",
            "LME/PR_AL.2",
            "LME/PR_PB.2",
            "LME/PR_TN.2",
            "LME/PR_NI.2",
            "BUNDESBANK/BBEX3_D_BRL_USD_CA_AB_000",
        ],
        start_date="2012-01-03",
        returns="pandas",
    )

    todo_periodo.columns = [
        "Cobre",
        "Zinco",
        "Aluminio",
        "Chumbo",
        "Estanho",
        "Niquel",
        "Dolar",
    ]

    return todo_periodo
