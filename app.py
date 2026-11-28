import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Saúde Mental no Trabalho",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# DADOS DO PROJETO
# ============================================================

dados = pd.DataFrame({
    "Município": [
        "Florianópolis",
        "São Caetano do Sul",
        "Águas de São Pedro",
        "Jordão",
        "Itapicuru",
        "Olivença",
    ],
    "UF": [
        "SC",
        "SP",
        "SP",
        "AC",
        "BA",
        "AL",
    ],
    "IDHM": [
        0.847,
        0.862,
        0.854,
        0.469,
        0.486,
        0.538,
    ],
})


# Notificações por município e ano
notificacoes = pd.DataFrame({
    "Município": [
        "Florianópolis", "Florianópolis", "Florianópolis",
        "Florianópolis", "Florianópolis", "Florianópolis",

        "São Caetano do Sul", "São Caetano do Sul",
        "São Caetano do Sul", "São Caetano do Sul",
        "São Caetano do Sul", "São Caetano do Sul",

        "Águas de São Pedro", "Águas de São Pedro",
        "Águas de São Pedro", "Águas de São Pedro",
        "Águas de São Pedro", "Águas de São Pedro",

        "Jordão", "Jordão", "Jordão",
        "Jordão", "Jordão", "Jordão",

        "Itapicuru", "Itapicuru", "Itapicuru",
        "Itapicuru", "Itapicuru", "Itapicuru",

        "Olivença", "Olivença", "Olivença",
        "Olivença", "Olivença", "Olivença",
    ],
    "Ano": [
        2020, 2021, 2022, 2023, 2024, 2025,
        2020, 2021, 2022, 2023, 2024, 2025,
        2020, 2021, 2022, 2023, 2024, 2025,
        2020, 2021, 2022, 2023, 2024, 2025,
        2020, 2021, 2022, 2023, 2024, 2025,
        2020, 2021, 2022, 2023, 2024, 2025,
    ],
    "Notificações": [
        0, 0, 3, 13, 6, 51,
        0, 2, 3, 4, 7, 4,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 1,
        0, 0, 0, 0, 0, 1,
        0, 0, 0, 3, 0, 0,
    ],
})


# ============================================================
# POPULAÇÃO ANUAL
# ============================================================

populacao = pd.DataFrame({
    "Município": [
        "Florianópolis", "Florianópolis", "Florianópolis",
        "Florianópolis", "Florianópolis", "Florianópolis",

        "São Caetano do Sul", "São Caetano do Sul",
        "São Caetano do Sul", "São Caetano do Sul",
        "São Caetano do Sul", "São Caetano do Sul",

        "Águas de São Pedro", "Águas de São Pedro",
        "Águas de São Pedro", "Águas de São Pedro",
        "Águas de São Pedro", "Águas de São Pedro",

        "Jordão", "Jordão", "Jordão",
        "Jordão", "Jordão", "Jordão",

        "Itapicuru", "Itapicuru", "Itapicuru",
        "Itapicuru", "Itapicuru", "Itapicuru",

        "Olivença", "Olivença", "Olivença",
        "Olivença", "Olivença", "Olivença",
    ],
    "Ano": [
        2020, 2021, 2022, 2023, 2024, 2025,
        2020, 2021, 2022, 2023, 2024, 2025,
        2020, 2021, 2022, 2023, 2024, 2025,
        2020, 2021, 2022, 2023, 2024, 2025,
        2020, 2021, 2022, 2023, 2024, 2025,
        2020, 2021, 2022, 2023, 2024, 2025,
    ],
    "População": [
        515000, 516000, 537000, 550000, 576000, 587000,
        162000, 162000, 165000, 166000, 172000, 171000,
        2780, 2800, 2850, 2900, 3390, 3450,
        8500, 8600, 8700, 9000, 9200, 11216,
        32500, 33000, 33500, 34000, 35000, 39162,
        10800, 10900, 11100, 11257, 11500, 11500,
    ],
})


# ============================================================
# PREPARAÇÃO DOS DADOS
# ============================================================

df = notificacoes.merge(
    dados,
    on="Município",
    how="left"
)

df = df.merge(
    populacao,
    on=["Município", "Ano"],
    how="left"
)

df["Taxa_100mil"] = (
    df["Notificações"] /
    df["População"] *
    100_000
)


# ============================================================
# TÍTULO
# ============================================================

st.title("📊 Saúde Mental Relacionada ao Trabalho")

st.markdown(
    """
    ### Notificações de Transtornos Mentais Relacionados ao Trabalho

    **SINAN/DATASUS — Municípios selecionados — 2020 a 2025**

    Este painel apresenta uma análise exploratória das notificações
    registradas nos municípios selecionados no projeto.
    """
)


# ============================================================
# FILTROS
# ============================================================

st.sidebar.header("🔎 Filtros")

municipios = ["Todos"] + sorted(df["Município"].unique().tolist())

municipio_selecionado = st.sidebar.selectbox(
    "Município",
    municipios
)

anos = sorted(df["Ano"].unique())

anos_selecionados = st.sidebar.multiselect(
    "Ano",
    anos,
    default=anos
)


# Aplicação dos filtros
df_filtrado = df[
    df["Ano"].isin(anos_selecionados)
]

if municipio_selecionado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["Município"] == municipio_selecionado
    ]


# ============================================================
# INDICADORES
# ============================================================

total_notificacoes = df_filtrado["Notificações"].sum()

municipios_com_registro = (
    df_filtrado.loc[
        df_filtrado["Notificações"] > 0,
        "Município"
    ].nunique()
)

ano_pico = (
    df_filtrado.groupby("Ano")["Notificações"]
    .sum()
    .idxmax()
    if not df_filtrado.empty
    else "-"
)

taxa_media = (
    df_filtrado["Notificações"].sum()
    / df_filtrado["População"].sum()
    * 100_000
    if df_filtrado["População"].sum() > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total de notificações",
    int(total_notificacoes)
)

col2.metric(
    "Municípios com registros",
    municipios_com_registro
)

col3.metric(
    "Ano com mais notificações",
    ano_pico
)

col4.metric(
    "Taxa por 100 mil (média)",
    f"{taxa_media:.2f}"
)


st.divider()


# ============================================================
# GRÁFICO 1 — DISTRIBUIÇÃO POR MUNICÍPIO
# ============================================================

st.subheader(
    "1. Distribuição Total de Notificações por Município"
)

grafico_municipio = (
    df_filtrado
    .groupby("Município", as_index=False)["Notificações"]
    .sum()
    .sort_values("Notificações", ascending=True)
)

fig1 = px.bar(
    grafico_municipio,
    x="Notificações",
    y="Município",
    orientation="h",
    text="Notificações",
    labels={
        "Notificações": "Número de notificações",
        "Município": ""
    },
)

fig1.update_traces(
    textposition="outside"
)

fig1.update_layout(
    height=450,
    yaxis={"categoryorder": "total ascending"},
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# ============================================================
# GRÁFICO 2 — EVOLUÇÃO ANUAL
# ============================================================

st.subheader(
    "2. Evolução Anual das Notificações"
)

evolucao = (
    df_filtrado
    .groupby(["Ano", "Município"], as_index=False)
    ["Notificações"]
    .sum()
)

fig2 = px.line(
    evolucao,
    x="Ano",
    y="Notificações",
    color="Município",
    markers=True,
    labels={
        "Ano": "Ano",
        "Notificações": "Notificações",
        "Município": "Município"
    },
)

fig2.update_layout(
    height=500
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ============================================================
# GRÁFICO 3 — HEATMAP
# ============================================================

st.subheader(
    "3. Distribuição das Notificações por Município e Ano"
)

heatmap = (
    df_filtrado
    .pivot_table(
        index="Município",
        columns="Ano",
        values="Notificações",
        aggfunc="sum",
        fill_value=0
    )
)

fig3 = px.imshow(
    heatmap,
    text_auto=True,
    aspect="auto",
    labels={
        "x": "Ano",
        "y": "Município",
        "color": "Notificações"
    },
)

fig3.update_layout(
    height=450
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# ============================================================
# GRÁFICO 4 — TAXA POR 100 MIL
# ============================================================

st.subheader(
    "4. Taxa Média de Notificações por 100.000 Habitantes"
)

taxas = (
    df_filtrado
    .groupby(
        ["Município", "IDHM"],
        as_index=False
    )
    .agg(
        Notificações=("Notificações", "sum"),
        População=("População", "sum")
    )
)

taxas["Taxa_100mil"] = (
    taxas["Notificações"]
    / taxas["População"]
    * 100_000
)

taxas = taxas.sort_values(
    "Taxa_100mil",
    ascending=True
)

fig4 = px.bar(
    taxas,
    x="Taxa_100mil",
    y="Município",
    orientation="h",
    text=taxas["Taxa_100mil"].round(2),
    labels={
        "Taxa_100mil": "Notificações por 100.000 habitantes",
        "Município": ""
    },
)

fig4.update_traces(
    textposition="outside"
)

fig4.update_layout(
    height=450
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


# ============================================================
# GRÁFICO 5 — IDHM × TAXA
# ============================================================

st.subheader(
    "5. IDHM × Taxa de Notificações"
)

scatter = (
    df_filtrado
    .groupby(
        ["Município", "UF", "IDHM"],
        as_index=False
    )
    .agg(
        Notificações=("Notificações", "sum"),
        População=("População", "sum")
    )
)

scatter["Taxa_100mil"] = (
    scatter["Notificações"]
    / scatter["População"]
    * 100_000
)

fig5 = px.scatter(
    scatter,
    x="IDHM",
    y="Taxa_100mil",
    size="Notificações",
    text="Município",
    hover_name="Município",
    hover_data={
        "UF": True,
        "IDHM": ":.3f",
        "Notificações": True,
        "Taxa_100mil": ":.2f",
    },
    labels={
        "IDHM": "IDHM (2010)",
        "Taxa_100mil": "Taxa por 100.000 habitantes",
        "Notificações": "Notificações"
    },
)

fig5.update_traces(
    textposition="top center"
)

fig5.update_layout(
    height=550
)

st.plotly_chart(
    fig5,
    use_container_width=True
)


# ============================================================
# NOTA METODOLÓGICA
# ============================================================

st.divider()

st.warning(
    """
    **Nota metodológica:** as notificações do SINAN representam
    registros identificados e notificados pelos serviços de saúde
    e não necessariamente a totalidade dos casos existentes.

    As taxas apresentadas utilizam a população residente como
    denominador, e não a população trabalhadora. Municípios com
    poucos registros podem apresentar taxas instáveis.
    """
)

st.caption(
    "Fonte: Elaborado pelos autores com base nos dados do DATASUS/SINAN e IBGE (2026)."
)
