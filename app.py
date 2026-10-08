import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração visual da página
st.set_page_config(
    page_title="Dashboard de Clubes",
    page_icon="⚽",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0b0b0b;
}

    h1, h2, h3 {
        color: #ffffff;
    }

.stMetric {
    background-color: #242424;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #e10600;
}
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("Tabela_Clubes.csv")

# Remove espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()

# Transformar idade média em número
df["Idade_Media"] = df["Idade_Media"].str.replace(",", ".").astype(float)

st.title("⚽ Dashboard de Clubes")
st.caption("Análise dos clubes de futebol por ano, desempenho e características dos elencos.")

st.write(
    "Dashboard interativo com informações sobre vitórias, "
    "derrotas, empates, idade dos jogadores, valor dos elencos "
    "e saldo de gols dos clubes."
)
st.subheader("🏆 Clubes com mais vitórias")

st.divider()

st.subheader("📅 Filtro por ano")

anos = sorted(df["Ano"].unique())

ano_selecionado = st.selectbox(
    "Selecione um ano:",
    anos
)

df_filtrado = df[df["Ano"] == ano_selecionado]

# Filtro por clube
clubes = sorted(df_filtrado["Clubes"].unique())

clube_selecionado = st.selectbox(
    "Selecione um clube:",
    clubes
)

# Dados do clube selecionado
df_clube = df_filtrado[df_filtrado["Clubes"] == clube_selecionado]

# Indicadores do ano selecionado
col1, col2, col3, col4 = st.columns(4)

st.subheader("📊 Informações do clube")

st.dataframe(df_clube)

# Indicadores do clube selecionado
col1, col2, col3, col4 = st.columns(4)

col1.metric("Vitórias", int(df_clube["Vitorias"].sum()))
col2.metric("Derrotas", int(df_clube["Derrotas"].sum()))
col3.metric("Empates", int(df_clube["Empates"].sum()))
col4.metric("Saldo de gols", int(df_clube["Saldo"].sum()))

# Gráfico de desempenho do clube
st.subheader("📈 Desempenho do clube")

fig6 = px.bar(
    x=["Vitórias", "Derrotas", "Empates"],
    y=[
        int(df_clube["Vitorias"].sum()),
        int(df_clube["Derrotas"].sum()),
        int(df_clube["Empates"].sum())
    ],
    title=f"Desempenho do {clube_selecionado}",
    labels={
        "x": "Resultado",
        "y": "Quantidade"
    },
    color_discrete_sequence=["#e10600"]
)

st.plotly_chart(fig6, use_container_width=True)

# Informações financeiras e idade
st.subheader("💰 Valor e idade do elenco")

col1, col2 = st.columns(2)

col1.metric(
    "Valor do elenco",
    f"€ {df_clube['Valor_total'].sum():,.2f}"
)

col2.metric(
    "Idade média",
    f"{df_clube['Idade_Media'].mean():.1f} anos"
)

col1.metric("Clubes", df_filtrado["Clubes"].nunique())
col2.metric("Vitórias", df_filtrado["Vitorias"].sum())
col3.metric("Derrotas", df_filtrado["Derrotas"].sum())
col4.metric("Empates", df_filtrado["Empates"].sum())

top_vitorias = df_filtrado.groupby("Clubes")["Vitorias"].sum().sort_values(ascending=False).head(10)

fig = px.bar(
    top_vitorias,
    x=top_vitorias.index,
    y=top_vitorias.values,
    title="Top 10 clubes com mais vitórias",
    labels={
        "x": "Clube",
        "y": "Vitórias"
    },
    color_discrete_sequence=["#e10600"]
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Gráfico de idade média
st.subheader("👥 Idade média dos jogadores")

idade_media = df.groupby("Ano")["Idade_Media"].mean().reset_index()

fig3 = px.line(
    x=idade_media["Ano"],
    y=idade_media["Idade_Media"],
    title="Idade média dos jogadores por ano",
    labels={
        "x": "Ano",
        "y": "Idade média"
    },
    markers=True,
    color_discrete_sequence=["#e10600"]
)

st.plotly_chart(fig3, use_container_width=True)
# Gráfico de valor médio dos elencos
st.subheader("💰 Valor médio dos elencos")

valor_medio = df.groupby("Ano")["Valor_total"].mean().reset_index()

fig4 = px.line(
    x=valor_medio["Ano"],
    y=valor_medio["Valor_total"],
    title="Valor médio dos elencos por ano",
    labels={
        "x": "Ano",
        "y": "Valor médio"
    },
    markers=True,
    color_discrete_sequence=["#e10600"]
)

st.plotly_chart(fig4, use_container_width=True)
# Gráfico de saldo de gols
st.subheader("⚽ Clubes com maior saldo de gols")

saldo_clubes = df.groupby("Clubes")["Saldo"].mean().sort_values(
    ascending=False
).head(5)

fig5 = px.bar(
    x=saldo_clubes.index,
    y=saldo_clubes.values,
    title="Top 5 clubes por saldo de gols",
    labels={
        "x": "Clube",
        "y": "Saldo médio de gols"
    },
    color_discrete_sequence=["#e10600"]
)

st.plotly_chart(fig5, use_container_width=True)
# Tabela
st.subheader("📋 Dados dos clubes")
st.dataframe(df_filtrado)