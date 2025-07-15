import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

comodities = ['CL=F', 'GC=F', 'SI=F']

DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def buscar_dados_comodities(simbolo, periodo='5d', intervalo='1d'):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
    dados = dados.copy()
    dados['simbolo'] = simbolo
    return dados

def buscar_todos_dados_comodities(comodities):
    todos_dados = []
    for simbolo in comodities:
        dados = buscar_dados_comodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)

def salvar_no_banco(df, schema='public'):
    df.to_sql('commodities', engine, if_exists='replace', index=True, index_label='Date', schema=schema)

if __name__ == "__main__":
    dados_concatedados = buscar_todos_dados_comodities(comodities)
    salvar_no_banco(dados_concatedados, schema='public')