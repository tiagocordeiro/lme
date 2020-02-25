# LME

## Cotação London Metal Exchange usando Quandl
[![Build Status](https://travis-ci.org/tiagocordeiro/lme.svg?branch=master)](https://travis-ci.org/tiagocordeiro/lme)
[![Updates](https://pyup.io/repos/github/tiagocordeiro/lme/shield.svg)](https://pyup.io/repos/github/tiagocordeiro/lme/)
[![Python 3](https://pyup.io/repos/github/tiagocordeiro/lme/python-3-shield.svg)](https://pyup.io/repos/github/tiagocordeiro/lme/)
[![codecov](https://codecov.io/gh/tiagocordeiro/lme/branch/master/graph/badge.svg)](https://codecov.io/gh/tiagocordeiro/lme)
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/tiagocordeiro/lme/blob/master/LICENSE)

#### Requisitos básicos
Você precisa de uma conta (gratuita) na [Quandl](https://www.quandl.com)

-  Register an account on Quandl
-  After logging in, click on Me and then Account settings to find the API key

[Quandl in Github](https://github.com/quandl/quandl-python)

#### Instalando o pacote via pip
```
$ pip install lme
```

#### Utilizando o pacote no console

```
>>> from lme.prices import get_latest_values_date, date_range_builder
>>> ultimo_periodo = date_range_builder()
>>> type(ultimo_periodo)
<class 'dict'>
>>> ultimo_periodo['inicio']
Timestamp('...-...-... 00:00:00+0000', tz='UTC')

```

### Testes, contribuição e dependências de desenvolvimento
Para instalar as dependências de desenvolvimento
```
pip install -r requirements-dev.txt
```

Para rodar os testes
```
pytest -v --doctest-glob='*.md'
```

Para criar um relatório de cobertura de testes.
```
coverage run -m pytest -v --doctest-glob='*.md'
coverage html
```

Verificando o `Code style`
```
pycodestyle .
flake8 .
```
