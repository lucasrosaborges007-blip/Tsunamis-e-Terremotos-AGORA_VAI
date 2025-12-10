import streamlit as st
import pandas as pd

# ========================================
# CONFIGURAÇÃO DA PÁGINA
# ========================================

st.set_page_config(
    page_title="Dashboard de Terremotos e Tsunamis",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# SIDEBAR - NAVEGAÇÃO E INFORMAÇÕES
# ========================================

st.sidebar.title("📊 Dashboard de Terremotos e Tsunamis")
st.sidebar.markdown("---")

# Seção de Informações
with st.sidebar.expander("ℹ️ Sobre o Dashboard", expanded=False):
    st.markdown("""
    ### 🎯 Objetivo
    Este dashboard permite explorar dados históricos de terremotos e eventos relacionados a tsunamis, 
    facilitando a descoberta de padrões, tendências e relações entre eventos sísmicos e a ocorrência de tsunamis.
    
    ### 📊 Funcionalidades
    - **Visão Geral:** Resumo estatístico e distribuição de dados
    - **Análise Interativa:** Filtros dinâmicos e gráficos personalizáveis
    - **Mapa Geográfico:** Visualização espacial dos eventos
    - **Probabilidade por País:** Análise de risco geológico por nação
    
    ### 🧭 Como Usar
    Use o menu lateral para acessar as diferentes páginas do dashboard. Os filtros afetam automaticamente 
    os gráficos e tabelas exibidas.
    """)

# Seção de Filtros Globais
st.sidebar.markdown("---")
st.sidebar.subheader("🎚️ Filtros Globais")

# Carregar dados
try:
    df = pd.read_csv("earthquake_data_tsunami.csv")
    
    # Filtro por Magnitude
    min_mag = float(df['magnitude'].min())
    max_mag = float(df['magnitude'].max())
    magnitude_range = st.sidebar.slider(
        "Magnitude (Escala Richter)",
        min_value=min_mag,
        max_value=max_mag,
        value=(min_mag, max_mag),
        step=0.1
    )
    
    # Filtro por Profundidade
    min_depth = float(df['depth'].min())
    max_depth = float(df['depth'].max())
    depth_range = st.sidebar.slider(
        "Profundidade (km)",
        min_value=min_depth,
        max_value=max_depth,
        value=(min_depth, max_depth),
        step=1.0
    )
    
    # Filtro por Tsunami
    tsunami_filter = st.sidebar.checkbox("Mostrar apenas eventos com tsunami", value=False)
    
except Exception as e:
    st.sidebar.error(f"Erro ao carregar dados: {e}")

# ========================================
# CONTEÚDO PRINCIPAL
# ========================================

st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.5em;
        color: #1f77b4;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #666;
        margin-bottom: 1em;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">🌍 Dashboard de Terremotos e Tsunamis</div>
<div class="subtitle">Explore dados sísmicos e de tsunamis de forma interativa</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Mensagem de boas-vindas
st.markdown("""
### 👋 Bem-vindo ao Dashboard!

Este painel interativo foi desenvolvido para facilitar a **exploração visual** de dados históricos de terremotos e tsunamis. 
Você pode:

- 📊 **Visualizar estatísticas** e distribuições de dados sísmicos
- 🔍 **Filtrar eventos** por magnitude, profundidade e ocorrência de tsunami
- 🗺️ **Explorar geograficamente** a distribuição dos eventos
- 📈 **Analisar tendências** ao longo do tempo
- 🌍 **Comparar riscos** entre diferentes países

### 🚀 Como Começar

Use o **menu lateral** para navegar entre as diferentes seções do dashboard:

1. **Visão Geral** - Resumo estatístico e gráficos iniciais
2. **Análise Interativa** - Filtros dinâmicos e visualizações personalizáveis
3. **Mapa Geográfico** - Visualização espacial dos eventos sísmicos
4. **Probabilidade por País** - Análise de risco geológico por nação

---
""")

# Exibir estatísticas rápidas
try:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total de Eventos", len(df))
    
    with col2:
        st.metric("📈 Magnitude Máxima", f"{df['magnitude'].max():.1f}")
    
    with col3:
        st.metric("🌊 Eventos com Tsunami", int(df['tsunami'].sum()))
    
    with col4:
        st.metric("📍 Profundidade Média", f"{df['depth'].mean():.1f} km")
        
except Exception as e:
    st.error(f"Erro ao exibir estatísticas: {e}")

st.markdown("""
---

### 📌 Dicas de Uso

- **Filtros Interativos:** Ajuste os controles no menu lateral para filtrar os dados conforme necessário
- **Gráficos Interativos:** Passe o mouse sobre os gráficos para ver detalhes adicionais
- **Zoom e Pan:** Em gráficos Plotly, você pode fazer zoom e deslocar a visualização
- **Exportar Dados:** Use as opções de download disponíveis em cada página

---

*Dashboard desenvolvido com Streamlit, Plotly e Pandas | Dados sísmicos históricos*
""")
