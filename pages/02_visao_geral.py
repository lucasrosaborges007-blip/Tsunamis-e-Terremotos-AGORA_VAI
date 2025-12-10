import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Visão Geral - Dashboard de Terremotos", layout="wide")

st.title("📊 Visão Geral dos Dados Sísmicos")

st.markdown("""
Esta página apresenta um **resumo estatístico** dos dados de terremotos e tsunamis, 
incluindo distribuições, tendências e métricas principais.
""")

# Carregar dados
try:
    df = pd.read_csv("earthquake_data_tsunami.csv")
except FileNotFoundError:
    st.error("Arquivo de dados 'earthquake_data_tsunami.csv' não encontrado.")
    st.stop()

# ========================================
# SEÇÃO 1: RESUMO ESTATÍSTICO
# ========================================

st.subheader("📈 Resumo Estatístico")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Eventos", len(df))

with col2:
    st.metric("Magnitude Máxima", f"{df['magnitude'].max():.2f}")

with col3:
    st.metric("Magnitude Média", f"{df['magnitude'].mean():.2f}")

with col4:
    st.metric("Profundidade Média", f"{df['depth'].mean():.2f} km")

st.markdown("---")

# ========================================
# SEÇÃO 2: GRÁFICO 1 - DISTRIBUIÇÃO DE MAGNITUDE (HISTOGRAMA)
# ========================================

st.subheader("📊 Gráfico 1: Distribuição de Magnitude")

st.markdown("""
Este histograma mostra como os eventos sísmicos se distribuem por faixa de magnitude. 
A maioria dos eventos concentra-se em magnitudes menores, enquanto eventos de alta magnitude são mais raros.
""")

fig_magnitude = px.histogram(
    df,
    x='magnitude',
    nbins=30,
    title='Distribuição de Magnitude dos Terremotos',
    labels={'magnitude': 'Magnitude (Escala Richter)', 'count': 'Quantidade de Eventos'},
    color_discrete_sequence=['#1f77b4']
)

fig_magnitude.update_layout(
    height=400,
    hovermode='x unified',
    xaxis_title='Magnitude (Escala Richter)',
    yaxis_title='Quantidade de Eventos'
)

st.plotly_chart(fig_magnitude, use_container_width=True)

st.markdown("---")

# ========================================
# SEÇÃO 3: GRÁFICO 2 - DISTRIBUIÇÃO DE PROFUNDIDADE (BOX PLOT)
# ========================================

st.subheader("📊 Gráfico 2: Distribuição de Profundidade")

st.markdown("""
Este gráfico de caixa (box plot) ilustra a distribuição da profundidade dos terremotos. 
Eventos rasos (próximos à superfície) tendem a causar mais danos, enquanto eventos profundos são geralmente menos destrutivos.
""")

fig_depth = px.box(
    df,
    y='depth',
    title='Distribuição de Profundidade dos Terremotos',
    labels={'depth': 'Profundidade (km)'},
    color_discrete_sequence=['#ff7f0e']
)

fig_depth.update_layout(
    height=400,
    showlegend=False,
    yaxis_title='Profundidade (km)'
)

st.plotly_chart(fig_depth, use_container_width=True)

st.markdown("---")

# ========================================
# SEÇÃO 4: GRÁFICO 3 - EVENTOS COM E SEM TSUNAMI (PIZZA)
# ========================================

st.subheader("📊 Gráfico 3: Proporção de Eventos com Tsunami")

st.markdown("""
Este gráfico de pizza mostra a proporção de eventos sísmicos que geraram tsunamis em relação 
aos que não geraram. Tsunamis são eventos raros, ocorrendo apenas quando certas condições geológicas são atendidas.
""")

# Contar eventos com e sem tsunami
tsunami_counts = df['tsunami'].value_counts().reset_index()
tsunami_counts.columns = ['tsunami', 'count']
tsunami_counts['label'] = tsunami_counts['tsunami'].apply(
    lambda x: '🌊 Com Tsunami' if x == 1 else '🏔️ Sem Tsunami'
)

fig_tsunami = px.pie(
    tsunami_counts,
    values='count',
    names='label',
    title='Proporção de Eventos com Tsunami',
    color_discrete_sequence=['#d62728', '#2ca02c']
)

fig_tsunami.update_layout(height=400)

st.plotly_chart(fig_tsunami, use_container_width=True)

st.markdown("---")

# ========================================
# SEÇÃO 5: TABELA DE DADOS DESCRITIVOS
# ========================================

st.subheader("📋 Estatísticas Descritivas Detalhadas")

st.markdown("""
A tabela abaixo apresenta as estatísticas descritivas completas do conjunto de dados, 
incluindo contagem, média, desvio padrão, mínimo, quartis e máximo.
""")

st.dataframe(df.describe(), use_container_width=True)

st.markdown("---")

# ========================================
# SEÇÃO 6: INFORMAÇÕES SOBRE AS COLUNAS
# ========================================

st.subheader("📖 Legenda das Colunas")

with st.expander("Clique para expandir a legenda das colunas"):
    st.markdown("""
    **🔹 magnitude**
    - Representa a magnitude do terremoto na escala Richter
    - Quanto maior, mais energia foi liberada no evento
    
    **🔹 cdi — Community Decimal Intensity**
    - Intensidade percebida pela população, baseada em relatos
    - Valor subjetivo, porém útil para medir impacto humano
    
    **🔹 mmi — Modified Mercalli Intensity**
    - Intensidade medida de forma técnica, baseada em danos e efeitos observados
    - Escala geralmente vai de I a XII, mas aqui está numericamente codificada
    
    **🔹 sig — Significance**
    - Um índice numérico que indica a importância do evento
    - Quanto maior, maior o impacto combinado (magnitude, profundidade, etc.)
    
    **🔹 nst — Number of Stations**
    - Quantidade de estações sísmicas que registraram o evento
    - Mais estações = registros mais precisos
    
    **🔹 dmin — Distance to the Nearest Station**
    - Distância (em graus) até a estação sísmica mais próxima
    - Valores menores significam medições mais confiáveis
    
    **🔹 gap — Azimuthal Gap**
    - Representa "vazios" na distribuição das estações ao redor do epicentro
    - Gaps menores = melhor cobertura
    
    **🔹 depth**
    - Profundidade do terremoto em km
    - Eventos rasos tendem a causar mais danos na superfície
    
    **🔹 latitude / longitude**
    - Coordenadas exatas do epicentro
    
    **🔹 Month**
    - Ano e mês do evento
    - Usados para ordenação temporal
    
    **🔹 tsunami**
    - Indica se o terremoto gerou tsunami:
      - 0 = sem tsunami
      - 1 = tsunami registrado
    """)

st.markdown("---")

st.info("💡 Dica: Use o menu lateral para filtrar os dados e explorar diferentes aspectos dos eventos sísmicos.")
