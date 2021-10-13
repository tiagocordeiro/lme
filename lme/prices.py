from datetime import datetime
from decimal import Decimal

import requests
from rich.console import Console
from rich.table import Table


def get_prices():
    response = requests.get("https://lme.gorilaxpress.com/cotacao/2cf4ff0e-8a30-48a5-8add-f4a1a63fee10/json/")

    prices = response.json()["results"]

    title_icon = "[not italic]:chart_with_upwards_trend:[/]"

    table = Table(title=f"{title_icon} Cotação London Metal Exchange {title_icon}")

    table.add_column("Data", justify="center", style="cyan", no_wrap=True)
    table.add_column("Zinco", justify="center", style="magenta")
    table.add_column("Cobre", justify="center", style="red")
    table.add_column("Alumínio", justify="center", style="blue")
    table.add_column("Chumbo", justify="center", style="bright_cyan")
    table.add_column("Estanho", justify="center", style="bright_blue")
    table.add_column("Níquel", justify="center", style="bright_yellow")
    table.add_column("Dolar", justify="center", style="green")

    ultima_semana = datetime.strptime(prices[0]["data"], "%Y-%m-%d").strftime("%U")
    semana_dias = 0
    media_semana_zinco = 0
    media_semana_cobre = 0
    media_semana_aluminio = 0
    media_semana_chumbo = 0
    media_semana_estanho = 0
    media_semana_niquel = 0
    media_semana_dolar = 0

    for price in prices:
        _data = datetime.strptime(price["data"], "%Y-%m-%d").strftime("%d/%m/%Y")

        semana_numero = datetime.strptime(_data, "%d/%m/%Y").strftime("%U")

        if semana_numero != ultima_semana:
            table.add_row(f"Média Semana {int(semana_numero) - 1}",
                          str(round(Decimal(media_semana_zinco / semana_dias), ndigits=2)),
                          str(round(Decimal(media_semana_cobre / semana_dias), ndigits=2)),
                          str(round(Decimal(media_semana_aluminio / semana_dias), ndigits=2)),
                          str(round(Decimal(media_semana_chumbo / semana_dias), ndigits=2)),
                          str(round(Decimal(media_semana_estanho / semana_dias), ndigits=2)),
                          str(round(Decimal(media_semana_niquel / semana_dias), ndigits=2)),
                          str(round(Decimal(media_semana_dolar / semana_dias), ndigits=2)))

            ultima_semana = semana_numero
            semana_dias = 0
            media_semana_zinco = 0
            media_semana_cobre = 0
            media_semana_aluminio = 0
            media_semana_chumbo = 0
            media_semana_estanho = 0
            media_semana_niquel = 0
            media_semana_dolar = 0

        else:
            semana_dias += 1
            media_semana_zinco += float(price["zinco"])
            media_semana_cobre += float(price["cobre"])
            media_semana_aluminio += float(price["aluminio"])
            media_semana_chumbo += float(price["chumbo"])
            media_semana_estanho += float(price["estanho"])
            media_semana_niquel += float(price["niquel"])
            media_semana_dolar += float(price["dolar"])

            table.add_row(f'{_data}', price["zinco"], price["cobre"], price["aluminio"], price["chumbo"],
                          price["estanho"], price["niquel"], price["dolar"])

    console = Console()
    console.print(table, justify="center")


if __name__ == "__main__":
    get_prices()
