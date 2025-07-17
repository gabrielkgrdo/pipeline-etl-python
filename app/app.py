import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv
import plotly.express as px

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as variáveis do arquivo .env
DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

# Criar a URL de conexão do banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criar o engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

def obter_dados():
    query = f"""
    Select 
        data,
        simbolo,
        valor_fechamento,
        acao,
        quantidade,
        valor,
        ganho
    FROM
        public.dm_commodities;
    """
    df = pd.read_sql(query, engine)
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df = df.dropna(subset=['data'])
    return df

df = obter_dados()

st.set_page_config(page_title="Dashboard de Commodities", layout="wide")

st.title("📈 Análise de Commodities")

symbols = df["simbolo"].unique()
selected_symbols = st.multiselect("Selecionar símbolos:", options=symbols, default=list(symbols))

min_date = df["data"].min().date()
max_date = df["data"].max().date()
date_range = st.date_input("Selecionar intervalo de datas:", value=[min_date, max_date], min_value=min_date, max_value=max_date)

df_filtrado = df[
    (df["simbolo"].isin(selected_symbols)) &
    (df["data"] >= pd.to_datetime(date_range[0])) &
    (df["data"] <= pd.to_datetime(date_range[1]))
]

df_filtrado = df_filtrado.sort_values(by=["simbolo", "data"])
df_filtrado["ganho_acumulado"] = df_filtrado.groupby("simbolo")["ganho"].cumsum()

total_transacoes = len(df_filtrado)
total_valor = df_filtrado['valor'].sum()
ganho_liquido = df_filtrado['ganho'].sum()

st.markdown("### 📌 Indicadores")
col1, col2, col3 = st.columns(3)

col1.metric("📦 Total de Transações", f"{total_transacoes}")
col2.metric("💰 Valor Movimentado", f"R$ {total_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col3.metric("📈 Ganho Líquido", f"R$ {ganho_liquido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.subheader("📊 Quantidade negociada por data")
fig1 = px.bar(df_filtrado, x="data", y="quantidade", color="acao", barmode="group",
              facet_col="simbolo", title="Quantidade negociada")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("💰 Valor movimentado por dia")
fig2 = px.line(df_filtrado, x="data", y="valor", color="simbolo", line_group="acao",
               title="Valor movimentado")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📈 Ganho/perda acumulado")
fig3 = px.area(df_filtrado, x="data", y="ganho_acumulado", color="simbolo",
               title="Ganho acumulado")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("📋 Tabela de dados filtrados")
st.dataframe(df_filtrado.sort_values(by="data"))