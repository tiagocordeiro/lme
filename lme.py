#!/usr/bin/env python3
# coding: utf-8

from datetime import datetime, timedelta
import pandas as pd
import pygal

pd.options.display.float_format = '{:,.2f}'.format

pd.set_option('colheader_justify', 'right')

def cotacao_quatro_semanas():
    today = datetime.now()
    first_day = today - timedelta(days=today.isoweekday() - 1)
    last_day = first_day + timedelta(days=4)

    semana01_inicio = first_day
    semana01_fim = last_day

    semana02_inicio = semana01_inicio - timedelta(weeks=1)
    semana02_fim = semana02_inicio + timedelta(days=4)

    semana03_inicio = semana02_inicio - timedelta(weeks=1)
    semana03_fim = semana03_inicio + timedelta(days=4)

    semana04_inicio = semana03_inicio - timedelta(weeks=1)
    semana04_fim = semana04_inicio + timedelta(days=4)

    cotacaoatual = pd.read_csv('cotacao-atual.csv', sep=';')

    cotacaoatual.columns = ['Data', 'Cobre', 'Zinco', 'Aluminio', 'Chumbo', 'Estanho', 'Niquel', 'Dolar']

    df = pd.DataFrame(cotacaoatual)

    df['Data'] = pd.to_datetime(df['Data'])

    df = df.set_index(df['Data'])

    df = df.drop('Data', axis=1)

    periodo = df[semana04_inicio.strftime("%Y-%m-%d"):semana01_fim.strftime("%Y-%m-%d")].interpolate()

    serieslabels = periodo.index.date.tolist()

    periodo_grafico = pygal.Line(value_formatter=lambda x: '{} $'.format(x), show_x_labels=False)

    periodo_grafico.x_labels = map(lambda d: d.strftime('%d/%m/%Y'), serieslabels)

    for column_name, column in periodo.transpose().iterrows():
        periodo_grafico.add('%s' % (column_name), pd.Series(periodo['%s' % (column_name)]), formatter=lambda x: '{}USD/Ton'.format(x))

    periodo_grafico.render()

    periodo_grafico.render_to_file('periodo.svg')

    for i in range(4, 0, -1):
        print('\u2554' + ('\u2550' * 33) + '\u2566' + ('\u2550' * 20) + '\u2566' + ('\u2550' * 17) + '\u2557')
        print('\u2551 Semana do ano:', eval('semana0'+str(i)+ '_inicio').strftime("%U"), ' ' * 13,
              '\u2551 Início:', eval('semana0'+str(i)+ '_inicio').strftime("%d-%m-%Y"),
              '\u2551 Fim:', eval('semana0'+str(i)+ '_fim').strftime("%d-%m-%Y"), '\u2551')
        print('\u255A' + ('\u2550' * 33) + '\u2569' + ('\u2550' * 20) + '\u2569' + ('\u2550' * 17) + '\u255D')

        print(df[eval('semana0'+str(i)+ '_inicio').strftime("%Y-%m-%d"):eval('semana0'+str(i)+ '_fim').strftime("%Y-%m-%d")])

        media_semana = df[eval('semana0'+str(i)+ '_inicio').strftime("%Y-%m-%d"):eval('semana0'+str(i)+ '_fim').strftime("%Y-%m-%d")]
        media_semana = pd.DataFrame(media_semana.mean())

        media_semana_tela = media_semana
        media_semana_tela.rename(columns={0: 'Média:    '}, inplace=True)
        media_semana_pivot = pd.pivot_table(media_semana_tela,
                                        columns=['Cobre', 'Zinco', 'Aluminio', 'Chumbo', 'Estanho', 'Niquel', 'Dolar'])
        media_semana_pivot = media_semana_pivot[['Cobre', 'Zinco', 'Aluminio', 'Chumbo', 'Estanho', 'Niquel', 'Dolar']]
        print('\u2550' * 73)
        print(media_semana_pivot)
        print('\n')


if __name__ == '__main__':
    cotacao_quatro_semanas()
