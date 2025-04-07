import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
from decimal import Decimal

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do MySQL
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT')),
    'database': os.getenv('MYSQL_DATABASE'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD')
}

# Adiciona configuração SSL se necessário
if os.getenv('MYSQL_SSL', 'false').lower() == 'true':
    db_config['ssl_disabled'] = False
else:
    db_config['ssl_disabled'] = True

def get_prices():
    """Obtém os preços do LME da API."""
    url_base = "https://lme.gorilaxpress.com/cotacao"
    data_link = "2cf4ff0e-8a30-48a5-8add-f4a1a63fee10/json"

    response = requests.get(f"{url_base}/{data_link}/")
    return response.json()["results"]

def create_table(cursor):
    """Cria a tabela para armazenar os preços do LME."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS lme_prices (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data DATE,
        cobre DECIMAL(10, 2),
        zinco DECIMAL(10, 2),
        aluminio DECIMAL(10, 2),
        chumbo DECIMAL(10, 2),
        estanho DECIMAL(10, 2),
        niquel DECIMAL(10, 2),
        dolar DECIMAL(10, 4),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY unique_date (data)
    )
    """
    cursor.execute(create_table_query)

def get_last_date(cursor):
    """Obtém a última data registrada no banco de dados."""
    query = "SELECT MAX(data) FROM lme_prices"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result and result[0] else None

def insert_data(cursor, prices_data, last_date):
    """Insere os dados na tabela, apenas registros mais recentes que a última data."""
    insert_query = """
    INSERT INTO lme_prices (data, cobre, zinco, aluminio, chumbo, estanho, niquel, dolar)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        cobre = VALUES(cobre),
        zinco = VALUES(zinco),
        aluminio = VALUES(aluminio),
        chumbo = VALUES(chumbo),
        estanho = VALUES(estanho),
        niquel = VALUES(niquel),
        dolar = VALUES(dolar)
    """
    
    new_records = 0
    updated_records = 0
    
    # Obtém a data atual
    today = datetime.now().date()
    
    for price in prices_data:
        # Converte a data para objeto datetime
        current_date = datetime.strptime(price["data"], "%Y-%m-%d").date()
        
        # Ignora o dia atual
        if current_date >= today:
            print(f"Ignorando dados do dia atual: {current_date}")
            continue
            
        # Verifica se a data é mais recente que a última data no banco
        if last_date is None or current_date > last_date:
            values = (
                current_date,
                float(price["cobre"]),
                float(price["zinco"]),
                float(price["aluminio"]),
                float(price["chumbo"]),
                float(price["estanho"]),
                float(price["niquel"]),
                float(price["dolar"])
            )
            cursor.execute(insert_query, values)
            new_records += 1
    
    return new_records, updated_records

def main():
    try:
        print("Conectando ao banco de dados MySQL...")
        print(f"Host: {db_config['host']}, Port: {db_config['port']}, Database: {db_config['database']}")
        
        # Conecta ao MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        print("Conexão estabelecida com sucesso!")
        
        # Cria a tabela se não existir
        print("Criando tabela se não existir...")
        create_table(cursor)
        
        # Obtém a última data registrada
        last_date = get_last_date(cursor)
        print(f"Última data registrada: {last_date}")
        
        # Obtém os dados do LME
        print("Obtendo dados do LME...")
        prices_data = get_prices()
        print(f"Obtidos {len(prices_data)} registros do LME")
        
        # Insere os dados no MySQL
        print("Inserindo dados no MySQL...")
        new_records, updated_records = insert_data(cursor, prices_data, last_date)
        
        # Commit das alterações
        conn.commit()
        print(f"Dados exportados com sucesso para o MySQL!")
        print(f"Novos registros inseridos: {new_records}")
        print(f"Registros atualizados: {updated_records}")
        
    except mysql.connector.Error as err:
        print(f"Erro de MySQL: {err}")
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Usuário ou senha incorretos.")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database não existe.")
        else:
            print(f"Erro: {err}")
    except Exception as e:
        print(f"Erro ao exportar dados: {e}")
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    main() 