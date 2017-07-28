import csv
import json


def converte_csv2json():
    with open('cotacoes/cotacao-atual.csv') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with open('cotacoes/cotacao-atual.json', 'w') as f:
        json.dump(rows, f)
