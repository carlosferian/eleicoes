import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk

# Configurações da página
st.set_page_config(
    page_title="Resultados Eleitorais de 1947",
    page_icon="🗳️",
    layout="wide",
)

# Adicionar CSS personalizado para estilos adicionais
st.markdown(
    """
    <style>
    /* Estilos gerais para divisões mais marcantes */
    .section {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 2px solid #e0e0e0;
    }
    /* Fundo para destacar os cards */
    .card-container {
        background-color: transparent;
        padding: 20px 0;
        margin-bottom: 20px;
    }
    /* Estilo dos cards para modo claro */
    @media (prefers-color-scheme: light) {
        .card {
            border-radius: 10px;
            background-color: #F8F9FA;
            padding: 30px;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            color: #000000;
        }
        .card-title {
            font-size: 22px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
        }
        .card-value {
            font-size: 40px;
            font-weight: bold;
            color: #007BFF;
            margin-bottom: 5px;
        }
        .card-desc {
            font-size: 16px;
            color: #666666;
        }
    }
    /* Estilo dos cards para modo escuro */
    @media (prefers-color-scheme: dark) {
        .card {
            border-radius: 10px;
            background-color: #2C2F33;
            padding: 30px;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
            text-align: center;
            color: #FFFFFF;
        }
        .card-title {
            font-size: 22px;
            font-weight: bold;
            color: #FFFFFF;
            margin-bottom: 10px;
        }
        .card-value {
            font-size: 40px;
            font-weight: bold;
            color: #FFD700;
            margin-bottom: 5px;
        }
        .card-desc {
            font-size: 16px;
            color: #CCCCCC;
        }
    }
    /* Alinhamento das colunas dos cards */
    .card-row {
        display: flex;
        justify-content: center;
    }
    /* Ajuste para colunas dos cards em telas menores */
    @media (max-width: 768px) {
        .card-row {
            flex-direction: column;
            align-items: center;
        }
        .card {
            width: 80%;
        }
    }
    /* Estilo para a tabela */
    .dataframe thead tr th {
        text-align: center;
        font-weight: bold;
    }
    .dataframe tbody tr td {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título e descrição
st.title("Resultados Eleitorais Históricos - 1947")
st.markdown("""
### Explore os dados da eleição histórica de 1947!
Compare os resultados de dois candidatos simultaneamente e veja o desempenho de ambos em diferentes visualizações.
""")

# Carregar dados
df = pd.read_csv('governadores_1947_decimal.csv')

# Garantir que 'VOTOS' seja numérico
df['VOTOS'] = pd.to_numeric(df['VOTOS'], errors='coerce')

# Sidebar para seleção de candidatos e filtro de cidades
st.sidebar.header("Filtros")

# Filtro de cidades - mostrando todas como opção, mas nenhuma selecionada por padrão
cidade_selecionada = st.sidebar.selectbox(
    "Selecione uma Cidade (deixe vazio para mostrar todas)",
    options=[''] + sorted(df['UF: PARANÁ'].unique()),  # Nenhuma cidade selecionada por padrão
    index=0  # 'Nenhuma' como padrão
)

# Filtro de candidatos - permite escolher dois candidatos, impedindo duplicação
candidato_1 = st.sidebar.selectbox("Selecione o Primeiro Candidato", options=df['CANDIDATO'].unique())

# Filtrar o segundo candidato para impedir que seja igual ao primeiro
candidatos_disponiveis = df['CANDIDATO'].unique().tolist()
candidatos_disponiveis.remove(candidato_1)

candidato_2 = st.sidebar.selectbox("Selecione o Segundo Candidato", options=candidatos_disponiveis)

# Filtrar os dados para os candidatos selecionados e cidade, se selecionada
if cidade_selecionada:
    df_filtrado = df[df['UF: PARANÁ'] == cidade_selecionada]
else:
    df_filtrado = df  # Se nenhuma cidade for selecionada, exibir todas

df_candidato_1 = df_filtrado[df_filtrado['CANDIDATO'] == candidato_1]
df_candidato_2 = df_filtrado[df_filtrado['CANDIDATO'] == candidato_2]

# Exibir os votos totais para cada candidato em cards personalizados
total_votos_1 = df_candidato_1['VOTOS'].sum()
total_votos_2 = df_candidato_2['VOTOS'].sum()

# Container para destacar os cards
st.markdown('<div class="card-container">', unsafe_allow_html=True)
st.markdown('<div class="card-row">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">{candidato_1}</div>
        <div class="card-value">{int(total_votos_1):,}</div>
        <div class="card-desc">Total de Votos</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">{candidato_2}</div>
        <div class="card-value">{int(total_votos_2):,}</div>
        <div class="card-desc">Total de Votos</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Divisão marcante
st.markdown('<div class="section"></div>', unsafe_allow_html=True)

# Juntar os dados de ambos os candidatos para o tooltip
df_merged = pd.merge(
    df_candidato_1,
    df_candidato_2,
    on=['ZONAS', 'UF: PARANÁ', 'LATITUDE_DECIMAL', 'LONGITUDE_DECIMAL'],
    how='outer',
    suffixes=('_1', '_2')
)

# Preencher NaNs com zero para votos
df_merged['VOTOS_1'] = df_merged['VOTOS_1'].fillna(0)
df_merged['VOTOS_2'] = df_merged['VOTOS_2'].fillna(0)

# Mapa interativo - Localização geográfica dos votos para ambos os candidatos com cores distintas
st.subheader("Mapa Geográfico dos Votos por Candidato")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_merged,
    get_position='[LONGITUDE_DECIMAL, LATITUDE_DECIMAL]',
    get_radius=5000,
    get_fill_color=[255, 0, 0, 160],
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=-24.5,
    longitude=-51.5,
    zoom=7,
    pitch=40,
)

# Adicionar o tooltip no objeto Deck
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "html": (
            "<b>Local: </b> {UF: PARANÁ}<br>"
            f"<b>{candidato_1}</b>: {{VOTOS_1}} votos<br>"
            f"<b>{candidato_2}</b>: {{VOTOS_2}} votos<br>"
            "<b>Zona: </b> {ZONAS}"
        ),
        "style": {"color": "white"},
    },
)

st.pydeck_chart(r)

# Divisão marcante
st.markdown('<div class="section"></div>', unsafe_allow_html=True)

# Gráfico de barras empilhadas - Comparação dos votos por cidade
st.subheader("Comparação de Votos por Cidade")
df_comparacao = pd.concat([df_candidato_1, df_candidato_2])

grafico_barras = alt.Chart(df_comparacao).mark_bar().encode(
    x=alt.X(r'UF\: PARANÁ:N', title="Cidades"),  # Escapando adequadamente o nome da coluna
    y=alt.Y('VOTOS:Q', title="Total de Votos"),
    color='CANDIDATO:N',
    tooltip=[r'UF\: PARANÁ:N', 'VOTOS:Q', 'CANDIDATO:N', 'ZONAS:N']
).properties(
    width='container',
    height=400
).configure_axis(
    labelAngle=-45
)

st.altair_chart(grafico_barras, use_container_width=True)

# Divisão marcante
st.markdown('<div class="section"></div>', unsafe_allow_html=True)

# Gráfico de linhas - Desempenho por Zonas Eleitorais
st.subheader("Desempenho por Zonas Eleitorais")

grafico_linhas = alt.Chart(df_comparacao).mark_line(point=True).encode(
    x='ZONAS:N',
    y='VOTOS:Q',
    color='CANDIDATO:N',
    tooltip=['ZONAS:N', 'VOTOS:Q', 'CANDIDATO:N']
).properties(
    width='container',
    height=400
)

st.altair_chart(grafico_linhas, use_container_width=True)

# Divisão marcante
st.markdown('<div class="section"></div>', unsafe_allow_html=True)

# Exibir os dados filtrados como tabela, omitindo dados georreferenciados e o índice
st.subheader("Dados Filtrados")

# Selecionar colunas relevantes e reorganizar
columns_to_display = ['UF: PARANÁ', 'ZONAS', 'CANDIDATO', 'VOTOS']
df_filtrado_tabela = df_comparacao[columns_to_display]

# Resetar o índice para remover o índice original
df_filtrado_tabela = df_filtrado_tabela.reset_index(drop=True)

# Estilizar a tabela e ajustar a largura
st.dataframe(df_filtrado_tabela.style.set_properties(**{'text-align': 'center'}), use_container_width=True)

# Footer
st.markdown("""
---
Feito com 💻 e 📊 por pesquisadores da história eleitoral.
""")
