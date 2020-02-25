from datetime import datetime, timedelta

from lme.prices import get_latest_values_date, last_weeks


def test_prices_last_week_content(capsys):
    fim = get_latest_values_date()

    dia_semana = fim.isoweekday()
    semana_numero = fim.strftime("%U")

    if semana_numero == "00":
        fim = datetime.now() - timedelta(days=fim.isoweekday())

    if dia_semana == 1:
        fim = datetime.now() - timedelta(days=3)

    last_weeks(1)
    captured = capsys.readouterr()
    assert f'Semana do ano: {semana_numero}' in captured.out
    assert f'Fim: {fim.strftime("%d-%m-%Y")}' in captured.out
