import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Mapa Geográfico - Dashboard de Terremotos", layout="wide")

st.title("🗺️ Mapa Geográfico de Terremotos e Tsunamis")

st.markdown("""
Esta página apresenta a **distribuição espacial** dos eventos sísmicos no planeta, 
permitindo visualizar padrões geográficos e a proximidade com zonas de risco.
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
# SIDEBAR - FILTROS
# ========================================

st.sidebar.subheader("🎚️ Filtros do Mapa")

# Filtro de Magnitude
min_mag = float(df['magnitude'].min())
max_mag = float(df['magnitude'].max())
magnitude_range = st.sidebar.slider(
    "Magnitude Mínima",
    min_value=min_mag,
    max_value=max_mag,
    value=min_mag,
    step=0.1,
    key="mag_map"
)

# Filtro de Tsunami
show_tsunami_only = st.sidebar.checkbox("Mostrar apenas eventos com tsunami", value=False, key="tsunami_map")

# Aplicar filtros
df_map = df[df['magnitude'] >= magnitude_range].copy()

if show_tsunami_only:
    df_map = df_map[df_map['tsunami'] == 1]

st.markdown("---")

# ========================================
# GRÁFICO 4: MAPA GEOGRÁFICO COM SCATTER GEO (PLOTLY)
# ========================================

st.subheader("📊 Gráfico 4: Mapa de Distribuição Geográfica")

st.markdown(f"""
Este mapa interativo mostra a localização de **{len(df_map)} eventos** sísmicos ao redor do mundo. 
O tamanho dos marcadores representa a magnitude, e a cor indica se houve tsunami.
Você pode fazer zoom, deslocar e passar o mouse para ver detalhes.
""")

if len(df_map) > 0:
    # Preparar dados para o mapa
    df_map_plot = df_map.copy()
    df_map_plot['Tsunami'] = df_map_plot['tsunami'].apply(lambda x: '🌊 Com Tsunami' if x == 1 else '❌ Sem Tsunami')
    
    try:
        fig_map = px.scatter_geo(
            df_map_plot,
            lat='latitude',
            lon='longitude',
            color='Tsunami',
            size='magnitude',
            hover_name='Year',
            hover_data={
                'magnitude': ':.2f',
                'depth': ':.2f',
                'latitude': ':.2f',
                'longitude': ':.2f',
                'Year': True,
                'Month': True,
                'tsunami': False,
                'Tsunami': True
            },
            title='Mapa de Distribuição de Terremotos e Tsunamis',
            color_discrete_map={
                '❌ Sem Tsunami': '#2ca02c',
                '🌊 Com Tsunami': '#d62728'
            },
            projection='natural earth'
        )
        
        fig_map.update_layout(
            height=600,
            geo=dict(
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)',
                projection_type='natural earth',
                showlakes=True,
                lakecolor='rgb(255, 255, 255)',
                showcountries=True,
                countrycolor='rgb(204, 204, 204)'
            ),
            legend=dict(
                title='Status do Tsunami',
                x=0.01,
                y=0.99
            ),
            hovermode='closest'
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar mapa: {str(e)}")
else:
    st.warning("Nenhum evento encontrado com os filtros selecionados.")

st.markdown("---")

# ========================================
# GRÁFICO 5: DENSIDADE DE EVENTOS POR REGIÃO
# ========================================

st.subheader("📊 Gráfico 5: Densidade de Eventos Sísmicos")

st.markdown("""
Este mapa de densidade mostra as regiões com maior concentração de eventos sísmicos, 
ajudando a identificar as zonas de maior atividade geológica.
""")

if len(df_map) > 0:
    try:
        fig_density = px.density_mapbox(
            df_map,
            lat='latitude',
            lon='longitude',
            z='magnitude',
            radius=15,
            center=dict(lat=0, lon=0),
            zoom=0,
            mapbox_style='open-street-map',
            title='Densidade de Magnitude dos Terremotos',
            color_continuous_scale='Viridis',
            hover_data={
                'magnitude': ':.2f',
                'latitude': ':.2f',
                'longitude': ':.2f'
            }
        )
        
        fig_density.update_layout(
            height=600,
            hovermode='closest'
        )
        
        st.plotly_chart(fig_density, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar mapa de densidade: {str(e)}")
else:
    st.warning("Nenhum evento encontrado com os filtros selecionados.")

st.markdown("---")

# ========================================
# ESTATÍSTICAS GEOGRÁFICAS
# ========================================

st.subheader("📊 Estatísticas Geográficas")

if len(df_map) > 0:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Eventos", len(df_map))
    
    with col2:
        st.metric("Latitude Média", f"{df_map['latitude'].mean():.2f}°")
    
    with col3:
        st.metric("Longitude Média", f"{df_map['longitude'].mean():.2f}°")
    
    with col4:
        st.metric("Eventos com Tsunami", int(df_map['tsunami'].sum()))
    
    st.markdown("---")
    
    # Tabela com informações dos eventos
    st.subheader("📋 Detalhes dos Eventos Exibidos")
    
    cols_display = ['magnitude', 'depth', 'latitude', 'longitude', 'Year', 'Month', 'tsunami']
    df_display = df_map[cols_display].head(50).copy()
    df_display.columns = ['Magnitude', 'Profundidade (km)', 'Latitude', 'Longitude', 'Ano', 'Mês', 'Tsunami']
    
    st.dataframe(df_display, use_container_width=True, height=400)
    
    # Opção de download
    csv = df_map.to_csv(index=False)
    st.download_button(
        label="📥 Baixar dados do mapa (CSV)",
        data=csv,
        file_name="terremotos_tsunamis_mapa.csv",
        mime="text/csv"
    )
else:
    st.info("Nenhum evento encontrado com os filtros selecionados.")

st.markdown("---")

st.info("💡 Dica: Ajuste os filtros no menu lateral para explorar diferentes regiões e magnitudes!")
