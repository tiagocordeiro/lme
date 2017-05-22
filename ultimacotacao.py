#!/usr/bin/env python3
# coding: utf-8

import datetime
import quandl

quandl.ApiConfig.api_key = ''  # Register an account on Quandl


def cotacaoAtualizada():
    now = datetime.datetime.now()
    periodo = now - datetime.timedelta(days=90)

    merged_data = quandl.get(["LME/PR_CU.2",
                              "LME/PR_ZI.2",
                              "LME/PR_AL.2",
                              "LME/PR_PB.2",
                              "LME/PR_TN.2",
                              "LME/PR_NI.2",
                              "CURRFX/USDBRL.1"],
                             start_date=periodo.strftime("%Y-%m-%d"),
                             end_date=now.strftime("%Y-%m-%d"),
                             returns="pandas")

    merged_data.columns = ['Cobre', 'Zinco', 'Aluminio', 'Chumbo', 'Estanho',
                           'Niquel', 'Dolar']

    merged_data.to_csv('cotacao-atual.csv', encoding='utf-8')


if __name__ == '__main__':
    cotacaoAtualizada()
    print('Cotação Atualizada')
