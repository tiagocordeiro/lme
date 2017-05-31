#!/usr/bin/env python3
# coding: utf-8

from datetime import datetime, timedelta
import os
import pandas as pd
import sqlite3 as db
import pygal
import quandl


pd.options.display.float_format = '{:,.2f}'.format

pd.set_option('colheader_justify', 'right')

html_files = 'cotacoes'


def check_html_folder():
    if not os.path.exists(html_files):
        os.makedirs(html_files)


def cotacaoAtualizada():
    """ Pega a cotação atualizada da quandl
    :return: Salva arquivo cotacao-atual.csv e lme.db
    """
    check_html_folder()
    cnx = db.connect('lme.db')

    # Parametros de inicio e fim do periodo pode ser usado
    # now = datetime.now()
    # periodo = now - timedelta(days=120)
    #
    # start_date = periodo.strftime("%Y-%m-%d"),
    # end_date = now.strftime("%Y-%m-%d")

    merged_data = quandl.get(["LME/PR_CU.2", "LME/PR_ZI.2", "LME/PR_AL.2",
                              "LME/PR_PB.2", "LME/PR_TN.2", "LME/PR_NI.2",
                              "CURRFX/USDBRL.1"], start_date="2012-01-03",
                             returns="pandas")

    merged_data.columns = ['Cobre', 'Zinco', 'Aluminio', 'Chumbo',
                           'Estanho', 'Niquel', 'Dolar']

    merged_data.to_csv('cotacoes/cotacao-atual.csv', encoding='utf-8')

    merged_data.to_sql('cotacoes', cnx, if_exists='replace')

    cnx.commit()
    print("Cotação atualizada...")
    cnx.close()


def pegaCotacao():
    cnx = db.connect('lme.db')
    df = pd.read_sql_query("select * from cotacoes", cnx)
    cnx.close()
    return df


def cotacaoPeriodo(qt_semanas=4):
    """ Retorna a cotação dos metais na London Metal Exchange
    Ex: cotacao_periodo(5)
    :param qt_semanas: Padrão 4 semanas, incluindo a semana atual.
    :return: Gera arquivos html
    """
    cnx = db.connect('lme.db')

    if not os.path.exists(html_files):
        os.makedirs(html_files)

    hoje = datetime.now()

    diadasemana = hoje.isoweekday()

    if diadasemana == 1:
        hoje = datetime.now() - timedelta(weeks=1)
    else:
        pass

    semana01_inicio = hoje - timedelta(days=hoje.isoweekday() - 1)
    semana01_fim = semana01_inicio + timedelta(days=4)

    semanas = {}

    semanas[1] = (semana01_inicio, semana01_fim)

    for i in range(2, qt_semanas + 1):
        semanas[i] = (semanas[i - 1][0] - timedelta(weeks=1),
                      semanas[i - 1][1] - timedelta(weeks=1))

    # cotacaoatual = pd.read_csv('cotacao-atual.csv')
    cotacaoatual = pd.read_sql_query("select * from cotacoes", cnx)

    cotacaoatual.columns = ['Data', 'Cobre', 'Zinco', 'Aluminio', 'Chumbo',
                            'Estanho', 'Niquel', 'Dolar']

    df = pd.DataFrame(cotacaoatual)

    df['Data'] = pd.to_datetime(df['Data'])

    df = df.set_index(df['Data'])

    df = df.drop('Data', axis=1)

    df.fillna(method='ffill', inplace=True)

    datas = qt_semanas

    # Gera Gráfico com pygal
    # TODO gerar gráficos separados por metal

    periodo = df[semanas[qt_semanas][0].strftime("%Y-%m-%d"):
                 semana01_fim.strftime("%Y-%m-%d")].interpolate()

    periodo.fillna(periodo.mean(), inplace=True)

    serieslabels = periodo.index.date.tolist()

    periodo_grafico = pygal.Line(value_formatter=lambda x: '{} $'.format(x),
                                 show_x_labels=True, height=400,
                                 x_label_rotation=20)

    periodo_grafico.x_labels = map(lambda d: d.strftime('%d/%m/%Y'),
                                   serieslabels)

    for column_name, column in periodo.transpose().iterrows():
        periodo_grafico.add('%s' % (column_name),
                            pd.Series(periodo['%s' % (column_name)]),
                            formatter=lambda x: '{}USD/Ton'.format(x))

    periodo_grafico.render()

    periodo_grafico.render_to_file('cotacoes/periodo.svg')

    # imprime na tela
    for i in range(datas, 0, -1):
        print('\u2554' + ('\u2550' * 33) +
              '\u2566' + ('\u2550' * 20) +
              '\u2566' + ('\u2550' * 17) + '\u2557')

        print('\u2551 Semana do ano:', semanas[i][0].strftime("%U"), ' ' * 13,
              '\u2551 Início:', semanas[i][0].strftime("%d-%m-%Y"),
              '\u2551 Fim:', semanas[i][1].strftime("%d-%m-%Y"), '\u2551')

        print('\u255A' + ('\u2550' * 33) + '\u2569' + ('\u2550' * 20) +
              '\u2569' + ('\u2550' * 17) + '\u255D')

        print(df[semanas[i][0].strftime("%Y-%m-%d"):semanas[i][1].strftime(
            "%Y-%m-%d")])

        media_semana = df[semanas[i][0].strftime("%Y-%m-%d"):semanas[i][
            1].strftime("%Y-%m-%d")]

        media_semana = pd.DataFrame(media_semana.mean())

        media_semana_tela = media_semana
        media_semana_tela.rename(columns={0: 'Média:    '}, inplace=True)
        media_semana_pivot = pd.pivot_table(media_semana_tela,
                                            columns=['Cobre', 'Zinco',
                                                     'Aluminio', 'Chumbo',
                                                     'Estanho', 'Niquel',
                                                     'Dolar'])

        media_semana_pivot = media_semana_pivot[
            ['Cobre', 'Zinco', 'Aluminio', 'Chumbo', 'Estanho', 'Niquel',
             'Dolar']]

        print('\u2550' * 73)
        print(media_semana_pivot)
        print('\n')

    # Salva HTML Semana
    for i in range(datas, 0, -1):
        # Pode ser usado outro local para salvar os HTML
        # Ex: ../public_html/cotacoes/
        # versão com o número da semana do ano
        # fo = open('cotacoes/semana'
        # + str(semanas[i][0].strftime("%U")) + '.html', "w")
        fo = open('cotacoes/semana' + '{num:02d}'.format(num=i) + '.html', 'w')
        fo.write(df[semanas[i][0].strftime("%Y-%m-%d"):
                    semanas[i][1].strftime("%Y-%m-%d")].to_html(
                    classes=['semanal', 'table-striped', 'table-responsive']))
        fo.close()

    # Salva HTML da Média Semanal
    for i in range(datas, 0, -1):
        media_semana = df[semanas[i][0].strftime("%Y-%m-%d"):
                          semanas[i][1].strftime("%Y-%m-%d")]
        media_semana = pd.DataFrame(media_semana.mean())
        media_semana.rename(
            columns={0: 'Semana:' + semanas[i][0].strftime("%U")},
            inplace=True)
        media_semana_pivot = pd.pivot_table(media_semana,
                                            columns=['Cobre', 'Zinco',
                                                     'Aluminio', 'Chumbo',
                                                     'Estanho', 'Niquel',
                                                     'Dolar'])
        media_semana_pivot = media_semana_pivot[
            ['Cobre', 'Zinco', 'Aluminio', 'Chumbo', 'Estanho', 'Niquel',
             'Dolar']]
        # versão com número da semana do ano
        # fo = open('cotacoes/semana' + str(semanas[i][0].strftime("%U")) +
        #  'media.html', "w")
        fo = open('cotacoes/semana' + '{num:02d}'.format(num=i) + 'media.html',
                  'w')
        fo.write(media_semana_pivot.to_html(
            classes=['semanal', 'table-striped', 'table-responsive']))
        fo.close()

        # return 'exibindo {} semanas'.format(len(semanas))
        cnx.close()


if __name__ == '__main__':
    # cotacao = pegaCotacao()
    # print(cotacao)
    # cotacaoPeriodo(4)
    cotacaoAtualizada()
