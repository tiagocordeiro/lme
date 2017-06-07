lme
===

Cotação London Metal Exchange usando Quandl
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: https://travis-ci.org/tiagocordeiro/lme.svg?branch=master
    :target: https://travis-ci.org/tiagocordeiro/lme

.. image:: https://pyup.io/repos/github/tiagocordeiro/lme/shield.svg
    :target: https://pyup.io/repos/github/tiagocordeiro/lme/
    :alt: Updates

.. image:: https://pyup.io/repos/github/tiagocordeiro/lme/python-3-shield.svg
    :target: https://pyup.io/repos/github/tiagocordeiro/lme/
    :alt: Python 3

.. image:: https://img.shields.io/badge/LME-Cobre-green.svg
    :target: https://www.quandl.com/data/LME/PR_CU-Copper-Prices
    :alt: Cobre

.. image:: https://img.shields.io/badge/LME-Zinco-green.svg
    :target: https://www.quandl.com/data/LME/PR_ZI-Zinc-Prices
    :alt: Zinco

.. image:: https://img.shields.io/badge/LME-Aluminio-green.svg
    :target: https://www.quandl.com/data/LME/PR_AL-Aluminum-Prices
    :alt: Alumínio

.. image:: https://img.shields.io/badge/LME-Chumbo-green.svg
    :target: https://www.quandl.com/data/LME/PR_PB-Lead-Prices
    :alt: Chumbo

.. image:: https://img.shields.io/badge/LME-Estanho-green.svg
    :target: https://www.quandl.com/data/LME/PR_TN-Tin-Prices
    :alt: Estanho

.. image:: https://img.shields.io/badge/LME-Niquel-green.svg
    :target: https://www.quandl.com/data/LME/PR_NI-Nickel-Prices
    :alt: Níquel

`Quandl <https://www.quandl.com/>`__

-  Register an account on Quandl
-  After logging in, click on Me and then Account settings to find the API key

`Quandl in Github <https://github.com/quandl/quandl-python>`__


Instalando o pacote via pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   $ pip install lme


Utilizando o pacote no console
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   >>> from lme.cotacao import *
   >>> cotacaoAtualizada() # baixa a cotação atualizada
   Cotação atualizada...
   >>> cotacaoPeriodo(4) # gera no console e arquivos da cotação do período
   ╔═════════════════════════════════╦════════════════════╦═════════════════╗
   ║ Semana do ano: 20               ║ Início: 15-05-2017 ║ Fim: 19-05-2017 ║
   ╚═════════════════════════════════╩════════════════════╩═════════════════╝
                 Cobre    Zinco  Aluminio   Chumbo   Estanho   Niquel  Dolar
   Data
   2017-05-15 5,586.00 2,568.50  1,899.50 2,131.50 20,100.00 9,310.00   3.18
   2017-05-16 5,584.00 2,517.00  1,915.00 2,084.00 19,905.00 9,015.00   3.11
   2017-05-17 5,575.00 2,561.00  1,928.00 2,102.00 20,055.00 9,165.00   3.10
   2017-05-18 5,490.00 2,462.00  1,905.00 2,052.00 20,650.00 9,005.00   3.13
   2017-05-19 5,596.00 2,569.00  1,938.00 2,088.00 20,550.00 9,180.00   3.37
   ═════════════════════════════════════════════════════════════════════════
                 Cobre    Zinco  Aluminio   Chumbo   Estanho   Niquel  Dolar
   Média:     5,566.20 2,535.50  1,917.10 2,091.50 20,252.00 9,135.00   3.18
   ...
