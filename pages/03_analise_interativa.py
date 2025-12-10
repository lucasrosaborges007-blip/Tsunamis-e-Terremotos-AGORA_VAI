import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Análise Interativa - Dashboard de Terremotos", layout="wide")

st.title("🔍 Análise Interativa de Terremotos e Tsunamis")

st.markdown("""
Esta página oferece **filtros dinâmicos** e **gráficos interativos** para explorar 
os dados de terremotos e tsunamis de forma personalizada.
""")

# ========================================
# CARREGAR DADOS
# ========================================

try:
    df = pd.read_csv("earthquake_data_tsunami.csv")
except FileNotFoundError:
    st.error("Arquivo de dados 'earthquake_data_tsunami.csv' não encontrado.")
    st.stop()

# ========================================
# SIDEBAR - FILTROS INTERATIVOS
# ========================================

st.sidebar.subheader("🎚️ Filtros de Análise Interativa")

# Filtro 1: Magnitude
min_mag = float(df['magnitude'].min())
max_mag = float(df['magnitude'].max())
magnitude_range = st.sidebar.slider(
    "Magnitude (Escala Richter)",
    min_value=min_mag,
    max_value=max_mag,
    value=(min_mag, max_mag),
    step=0.1,
    key="mag_filter"
)

# Filtro 2: Profundidade
min_depth = float(df['depth'].min())
max_depth = float(df['depth'].max())
depth_range = st.sidebar.slider(
    "Profundidade (km)",
    min_value=min_depth,
    max_value=max_depth,
    value=(min_depth, max_depth),
    step=1.0,
    key="depth_filter"
)

# Filtro 3: Tsunami
tsunami_filter = st.sidebar.selectbox(
    "Filtrar por Tsunami",
    options=["Todos", "Com Tsunami", "Sem Tsunami"],
    key="tsunami_filter"
)

# Aplicar filtros
df_filtered = df[
    (df['magnitude'] >= magnitude_range[0]) & 
    (df['magnitude'] <= magnitude_range[1]) &
    (df['depth'] >= depth_range[0]) & 
    (df['depth'] <= depth_range[1])
]

if tsunami_filter == "Com Tsunami":
    df_filtered = df_filtered[df_filtered['tsunami'] == 1]
elif tsunami_filter == "Sem Tsunami":
    df_filtered = df_filtered[df_filtered['tsunami'] == 0]

# ========================================
# EXIBIR INFORMAÇÕES SOBRE FILTROS
# ========================================

st.markdown("---")
st.subheader("📊 Dados Filtrados")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Eventos Filtrados", len(df_filtered))

with col2:
    st.metric("Magnitude Máxima", f"{df_filtered['magnitude'].max():.2f}" if len(df_filtered) > 0 else "N/A")

with col3:
    st.metric("Eventos com Tsunami", int(df_filtered['tsunami'].sum()) if len(df_filtered) > 0 else 0)

st.markdown("---")

# ========================================
# GRÁFICO INTERATIVO 1: SCATTER PLOT (PLOTLY)
# ========================================

st.subheader("📊 Gráfico Interativo 1: Magnitude vs. Profundidade")

st.markdown("""
Este gráfico de dispersão mostra a relação entre a **magnitude** e a **profundidade** dos terremotos. 
A cor indica se o evento gerou tsunami ou não. O tamanho dos pontos representa a intensidade (sig).
Você pode passar o mouse para ver detalhes específicos e fazer zoom.
""")

if len(df_filtered) > 0:
    # Criar cópia para não alterar dados originais
    df_plot = df_filtered.copy()
    df_plot['Tsunami'] = df_plot['tsunami'].apply(lambda x: '🌊 Com Tsunami' if x == 1 else '❌ Sem Tsunami')
    
    fig_scatter = px.scatter(
        df_plot,
        x='magnitude',
        y='depth',
        color='Tsunami',
        size='sig',
        hover_data={
            'magnitude': ':.2f',
            'depth': ':.2f',
            'sig': ':.0f',
            'latitude': ':.2f',
            'longitude': ':.2f',
            'tsunami': False,
            'Tsunami': True
        },
        title='Relação entre Magnitude e Profundidade dos Terremotos',
        labels={
            'magnitude': 'Magnitude (Escala Richter)',
            'depth': 'Profundidade (km)',
            'sig': 'Significância'
        },
        color_discrete_map={
            '❌ Sem Tsunami': '#2ca02c',
            '🌊 Com Tsunami': '#d62728'
        }
    )
    
    fig_scatter.update_layout(
        height=500,
        hovermode='closest',
        legend=dict(title='Status do Tsunami'),
        xaxis_title='Magnitude (Escala Richter)',
        yaxis_title='Profundidade (km)'
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.warning("Nenhum evento encontrado com os filtros selecionados.")

st.markdown("---")

# ========================================
# GRÁFICO INTERATIVO 2: LINHA TEMPORAL (MATPLOTLIB + WIDGET)
# ========================================

st.subheader("📊 Gráfico Interativo 2: Evolução Temporal de Magnitude")

st.markdown("""
Este gráfico de linha mostra como a **magnitude máxima** dos terremotos evoluiu ao longo do tempo. 
Você pode selecionar o período de tempo desejado usando o slider abaixo.
""")

# Preparar dados temporais
if len(df_filtered) > 0:
    try:
        df_filtered_copy = df_filtered.copy()
        
        # Criar coluna de ano se não existir
        if 'Year' not in df_filtered_copy.columns:
            st.error("Coluna 'Year' não encontrada no arquivo de dados.")
        else:
            # Agrupar por ano e calcular magnitude máxima
            df_yearly = df_filtered_copy.groupby('Year')['magnitude'].agg(['max', 'mean', 'count']).reset_index()
            df_yearly.columns = ['year', 'max_mag', 'mean_mag', 'count']
            
            # Widget para seleção de período
            min_year = int(df_yearly['year'].min())
            max_year = int(df_yearly['year'].max())
            
            year_range = st.slider(
                "Selecione o período de anos",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year),
                step=1,
                key="year_range_filter"
            )
            
            # Filtrar dados por período selecionado
            df_yearly_filtered = df_yearly[
                (df_yearly['year'] >= year_range[0]) & 
                (df_yearly['year'] <= year_range[1])
            ]
            
            if len(df_yearly_filtered) > 0:
                # Criar figura com matplotlib
                fig, ax = plt.subplots(figsize=(12, 6))
                
                ax.plot(df_yearly_filtered['year'], df_yearly_filtered['max_mag'], 
                        marker='o', linewidth=2.5, markersize=8, label='Magnitude Máxima', color='#d62728')
                ax.plot(df_yearly_filtered['year'], df_yearly_filtered['mean_mag'], 
                        marker='s', linewidth=2.5, markersize=6, label='Magnitude Média', color='#1f77b4', linestyle='--')
                
                ax.set_xlabel('Ano', fontsize=12, fontweight='bold')
                ax.set_ylabel('Magnitude (Escala Richter)', fontsize=12, fontweight='bold')
                ax.set_title('Evolução Temporal da Magnitude dos Terremotos', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
                ax.legend(fontsize=10, loc='best')
                ax.set_xticks(df_yearly_filtered['year'].unique())
                
                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.warning("Nenhum dado disponível para o período selecionado.")
        
    except Exception as e:
        st.error(f"Erro ao processar dados temporais: {str(e)}")
else:
    st.warning("Nenhum evento encontrado com os filtros selecionados.")

st.markdown("---")

# ========================================
# TABELA DE DADOS FILTRADOS
# ========================================

st.subheader("📋 Tabela de Dados Filtrados")

st.markdown("""
A tabela abaixo mostra os primeiros 100 registros dos dados filtrados. 
Você pode ordenar clicando nos cabeçalhos das colunas.
""")

if len(df_filtered) > 0:
    # Selecionar colunas principais para exibição
    cols_to_display = ['magnitude', 'depth', 'latitude', 'longitude', 'Year', 'Month', 'tsunami']
    df_display = df_filtered[cols_to_display].head(100).copy()
    df_display.columns = ['Magnitude', 'Profundidade (km)', 'Latitude', 'Longitude', 'Ano', 'Mês', 'Tsunami']
    
    st.dataframe(df_display, use_container_width=True, height=400)
    
    # Opção de download
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="📥 Baixar dados filtrados (CSV)",
        data=csv,
        file_name="terremotos_tsunamis_filtrados.csv",
        mime="text/csv"
    )
else:
    st.info("Nenhum evento encontrado com os filtros selecionados.")

st.markdown("---")

st.info("💡 Dica: Ajuste os filtros no menu lateral para explorar diferentes subconjuntos de dados e descobrir padrões interessantes!")
