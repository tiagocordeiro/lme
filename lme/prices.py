from datetime import datetime
from decimal import Decimal

import requests
from rich.console import Console
from rich.table import Table


def media(valor, dias):
    return str(round(Decimal(valor / dias), ndigits=2))


def get_prices():
    url_base = "https://lme.gorilaxpress.com/cotacao"
    data_link = "2cf4ff0e-8a30-48a5-8add-f4a1a63fee10/json"

    response = requests.get(f"{url_base}/{data_link}/")

    prices = response.json()["results"]

    title_icon = "[not italic]:chart_with_upwards_trend:[/]"
    title_text = "Cotação London Metal Exchange"

    table = Table(title=f"{title_icon} {title_text} {title_icon}")

    table.add_column("Data", justify="center", style="cyan", no_wrap=True)
    table.add_column("Zinco", justify="center", style="magenta")
    table.add_column("Cobre", justify="center", style="red")
    table.add_column("Alumínio", justify="center", style="blue")
    table.add_column("Chumbo", justify="center", style="bright_cyan")
    table.add_column("Estanho", justify="center", style="bright_blue")
    table.add_column("Níquel", justify="center", style="bright_yellow")
    table.add_column("Dolar", justify="center", style="green")

    ultima_semana = datetime.strptime(prices[0]["data"], "%Y-%m-%d").strftime(
        "%U")
    dias = 0
    media_zinco = 0
    media_cobre = 0
    media_aluminio = 0
    media_chumbo = 0
    media_estanho = 0
    media_niquel = 0
    media_dolar = 0

    for price in prices:
        dia = datetime.strptime(price["data"], "%Y-%m-%d").strftime("%d/%m/%Y")

        semana_numero = datetime.strptime(dia, "%d/%m/%Y").strftime("%U")

        if semana_numero != ultima_semana:
            table.add_row(f"Média Semana {int(semana_numero) - 1}",
                          media(media_zinco, dias),
                          media(media_cobre, dias),
                          media(media_aluminio, dias),
                          media(media_chumbo, dias),
                          media(media_estanho, dias),
                          media(media_niquel, dias),
                          media(media_dolar, dias))

            ultima_semana = semana_numero
            dias = 0
            media_zinco = 0
            media_cobre = 0
            media_aluminio = 0
            media_chumbo = 0
            media_estanho = 0
            media_niquel = 0
            media_dolar = 0

        else:
            dias += 1
            media_zinco += float(price["zinco"])
            media_cobre += float(price["cobre"])
            media_aluminio += float(price["aluminio"])
            media_chumbo += float(price["chumbo"])
            media_estanho += float(price["estanho"])
            media_niquel += float(price["niquel"])
            media_dolar += float(price["dolar"])

            table.add_row(f'{dia}', price["zinco"], price["cobre"],
                          price["aluminio"], price["chumbo"],
                          price["estanho"], price["niquel"], price["dolar"])

    console = Console()
    console.print(table, justify="center")


if __name__ == "__main__":
    get_prices()
