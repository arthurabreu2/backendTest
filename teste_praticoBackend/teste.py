import yfinance as yf
import mysql.connector

# Símbolo
symbol = "PETR4.SA"

# Acessar os dados da API
dados = yf.Ticker(symbol)
# Acessar os dividendos
dividends = dados.dividends.reset_index()

# Criar a base de dados
# CREATE DATABASE db_yfinance
# USE db_yfinance

# Conectar ao banco de dados MySQL
db_connection = mysql.connector.connect(
    host="127.0.0.1", user="root", password="brasil01", database="db_yfinance"
)

# Criar tabela para os dividendos (se ainda não existir)
create_table_query = """
CREATE TABLE IF NOT EXISTS dividend_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20),
    date DATE,
    dividends FLOAT
)
"""
cursor = db_connection.cursor()
cursor.execute(create_table_query)
db_connection.commit()

# Preparar os dados para serem inseridos no banco de dados
insert_query = "INSERT INTO dividend_data (symbol, date, dividends) VALUES (%s, %s, %s)"
insert_data = []

for _, row in dividends.iterrows():
    insert_data.append((symbol, row["Date"].date(), row["Dividends"]))

# Inserir dados no banco de dados
cursor.executemany(insert_query, insert_data)
db_connection.commit()

# Fechar conexões
cursor.close()
db_connection.close()

print("Dados de dividendos inseridos no banco de dados.")
