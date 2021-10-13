# LME

## Cotação London Metal Exchange

![Deploy workflow](https://github.com/tiagocordeiro/lme/actions/workflows/python-app.yml/badge.svg)
[![Build Status](https://travis-ci.org/tiagocordeiro/lme.svg?branch=master)](https://travis-ci.org/tiagocordeiro/lme)
[![Updates](https://pyup.io/repos/github/tiagocordeiro/lme/shield.svg)](https://pyup.io/repos/github/tiagocordeiro/lme/)
[![Python 3](https://pyup.io/repos/github/tiagocordeiro/lme/python-3-shield.svg)](https://pyup.io/repos/github/tiagocordeiro/lme/)
[![codecov](https://codecov.io/gh/tiagocordeiro/lme/branch/master/graph/badge.svg)](https://codecov.io/gh/tiagocordeiro/lme)
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/tiagocordeiro/lme/blob/master/LICENSE)

#### Instalando o pacote via pip
```
$ pip install lme
```

#### Instalando via git
```
$ git clone https://github.com/tiagocordeiro/lme.git
```

#### Como rodar o projeto (clonando via git)
* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.

```
git clone https://github.com/tiagocordeiro/lme.git
cd lme
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python contrib/env_gen.py
```

#### Utilizando o pacote no terminal
```
$ python lme/prices.py 
╔═════════════════════════════════╦════════════════════╦═════════════════╗
║ Semana do ano: 07               ║ Início: 17-02-2020 ║ Fim: 21-02-2020 ║
╚═════════════════════════════════╩════════════════════╩═════════════════╝
             Cobre   Zinco  Aluminio  Chumbo  Estanho   Niquel   Dolar
Data                                                                  
2020-02-17  5802.0  2153.5    1678.5  1911.0  16630.0  13070.0  4.3157
2020-02-18  5728.0  2128.0    1681.0  1901.0  16520.0  12880.0  4.3471
2020-02-19  5745.5  2126.5    1686.0  1920.0  16550.0  12700.0  4.3728
2020-02-20  5730.0  2100.0    1687.0  1939.0  16600.0  12685.0  4.3873
2020-02-21  5702.0  2086.5    1677.0  1881.0  16525.0  12440.0  4.3924
═════════════════════════════════════════════════════════════════════════
             Cobre   Zinco  Aluminio  Chumbo  Estanho   Niquel    Dolar
Média:      5741.5  2118.9    1681.9  1910.4  16565.0  12755.0  4.36306
```

#### Python console
```
>>> from lme.prices import last_weeks
>>> last_weeks(2)
...
╔═════════════════════════════════╦════════════════════╦═════════════════╗
║ Semana do ano: 07               ║ Início: 17-02-2020 ║ Fim: 21-02-2020 ║
╚═════════════════════════════════╩════════════════════╩═════════════════╝
             Cobre   Zinco  Aluminio  Chumbo  Estanho   Niquel   Dolar
Data                                                                  
2020-02-17  5802.0  2153.5    1678.5  1911.0  16630.0  13070.0  4.3157
2020-02-18  5728.0  2128.0    1681.0  1901.0  16520.0  12880.0  4.3471
2020-02-19  5745.5  2126.5    1686.0  1920.0  16550.0  12700.0  4.3728
2020-02-20  5730.0  2100.0    1687.0  1939.0  16600.0  12685.0  4.3873
2020-02-21  5702.0  2086.5    1677.0  1881.0  16525.0  12440.0  4.3924
═════════════════════════════════════════════════════════════════════════
             Cobre   Zinco  Aluminio  Chumbo  Estanho   Niquel    Dolar
Média:      5741.5  2118.9    1681.9  1910.4  16565.0  12755.0  4.36306
```

#### Testes, contribuição e dependências de desenvolvimento
Para instalar as dependências de desenvolvimento
```
pip install -r requirements-dev.txt
```

#### Banco de dados para desenvolvimento com Docker
```
docker-compose up -d
```

Para rodar os testes
```
pytest
```

Para criar um relatório de cobertura de testes.
```
coverage run -m pytest -v
coverage html
```

Verificando o `Code style`
```
pycodestyle .
flake8 .
```

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### License
[MIT](https://github.com/tiagocordeiro/lme/blob/master/LICENSE)