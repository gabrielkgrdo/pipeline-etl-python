import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

comodities = ['CL=F', 'GC=F', 'SI=F']

def buscar_dados_comodities(simbolo, periodo='5d', intervalo='1d'):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=periodo, interval=intervalo)[('Close')]
    dados['simbolo'] = simbolo
    return buscar_dados_comodities

def buscar_todos_dados_comodities():
    todos_dados = []
    for simbolo in comodities:
        dados = buscar_dados_comodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)

if __name__ == __main__:
    dados_concatedados = buscar_todos_dados_comodities(comodities)
    print(dados_concatedados)