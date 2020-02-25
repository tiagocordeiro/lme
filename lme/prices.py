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


def last_weeks(qt_semanas=4):
    """ Retorna a cotação dos metais na London Metal Exchange
    Ex: last_weeks(5)
    :param qt_semanas: Padrão 4 semanas, incluindo a semana atual.
    :return: Gera arquivos html
    """
    periodo_cotacao = date_range_builder(weeks=qt_semanas)
    hoje = periodo_cotacao["fim"]
    periodo = periodo_cotacao["inicio"]

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
            SELECT *
            FROM cotacao_lme
            WHERE "Date" BETWEEN %(inicio)s AND %(fim)s
            """

    query_params = {"inicio": periodo, "fim": hoje}

    cotacaoatual = pd.read_sql(query, conn, params=query_params)

    cotacaoatual.columns = [
        "Data",
        "Cobre",
        "Zinco",
        "Aluminio",
        "Chumbo",
        "Estanho",
        "Niquel",
        "Dolar",
    ]

    semana01_inicio = hoje - timedelta(days=hoje.isoweekday() - 1)
    semana01_fim = semana01_inicio + timedelta(days=4)

    semanas = {1: (semana01_inicio, semana01_fim)}

    for i in range(2, qt_semanas + 1):
        semanas[i] = (
            semanas[i - 1][0] - timedelta(weeks=1),
            semanas[i - 1][1] - timedelta(weeks=1),
        )

    df = pd.DataFrame(cotacaoatual)

    df["Data"] = pd.to_datetime(df["Data"])

    df = df.set_index(df["Data"])

    df = df.drop("Data", axis=1)

    datas = qt_semanas

    periodo = df[
              semanas[qt_semanas][0].strftime(
                  "%Y-%m-%d"): semana01_fim.strftime("%Y-%m-%d")
              ].interpolate()

    periodo.fillna(periodo.mean(), inplace=True)

    # imprime na tela
    for i in range(datas, 0, -1):
        print(
            "\u2554"
            + ("\u2550" * 33)
            + "\u2566"
            + ("\u2550" * 20)
            + "\u2566"
            + ("\u2550" * 17)
            + "\u2557"
        )

        print(
            "\u2551 Semana do ano:",
            semanas[i][0].strftime("%U"),
            " " * 13,
            "\u2551 Início:",
            semanas[i][0].strftime("%d-%m-%Y"),
            "\u2551 Fim:",
            semanas[i][1].strftime("%d-%m-%Y"),
            "\u2551",
        )

        print(
            "\u255A"
            + ("\u2550" * 33)
            + "\u2569"
            + ("\u2550" * 20)
            + "\u2569"
            + ("\u2550" * 17)
            + "\u255D"
        )

        print(
            df[semanas[i][0].strftime("%Y-%m-%d"): semanas[i][1].strftime(
                "%Y-%m-%d")]
        )

        media_semana = df[
                       semanas[i][0].strftime("%Y-%m-%d"): semanas[i][
                           1].strftime("%Y-%m-%d")
                       ]

        media_semana = pd.DataFrame(media_semana.mean())

        media_semana_tela = media_semana
        media_semana_tela.rename(columns={0: "Média:    "}, inplace=True)
        media_semana_pivot = pd.pivot_table(
            media_semana_tela,
            columns=[
                "Cobre",
                "Zinco",
                "Aluminio",
                "Chumbo",
                "Estanho",
                "Niquel",
                "Dolar",
            ],
        )

        media_semana_pivot = media_semana_pivot[
            ["Cobre", "Zinco", "Aluminio", "Chumbo", "Estanho", "Niquel",
             "Dolar"]
        ]

        print("\u2550" * 73)
        print(media_semana_pivot)
        print("\n")


if __name__ == "__main__":
    last_weeks(1)
