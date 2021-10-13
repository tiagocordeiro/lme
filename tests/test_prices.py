from lme.prices import get_prices


def test_get_prices(capsys):
    get_prices()
    captured = capsys.readouterr()
    assert f'Média Semana' in captured.out
