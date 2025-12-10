import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Probabilidade por País - Dashboard de Terremotos", layout="wide")

st.title("🌍 Probabilidade de Terremotos e Tsunamis por País")

st.markdown("""
Esta página apresenta uma **análise comparativa** de risco geológico entre diferentes países, 
considerando a proximidade com grandes placas tectônicas e histórico de eventos sísmicos.
""")

# ========================================
# CARREGAR DADOS DE RISCO
# ========================================

try:
    df_risco = pd.read_csv("country_risk.csv")
except FileNotFoundError:
    st.error("Arquivo de dados de risco 'country_risk.csv' não encontrado.")
    st.stop()

# ========================================
# SIDEBAR - FILTROS
# ========================================

st.sidebar.subheader("🎚️ Filtros de Análise")

# Filtro de Risco Mínimo
risco_min = st.sidebar.slider(
    "Risco Mínimo de Terremoto",
    min_value=0,
    max_value=10,
    value=0,
    step=1,
    key="risco_min"
)

# Ordenação
sort_by = st.sidebar.selectbox(
    "Ordenar por",
    options=["Risco de Terremoto", "Risco de Tsunami", "Risco Combinado"],
    key="sort_by"
)

# Aplicar filtros
df_risco_filtered = df_risco[df_risco['Risco_Terremoto'] >= risco_min].copy()

# Calcular Risco Combinado
df_risco_filtered['Risco_Combinado'] = (df_risco_filtered['Risco_Terremoto'] + df_risco_filtered['Risco_Tsunami']) / 2

# Ordenar
if sort_by == "Risco de Terremoto":
    df_risco_filtered = df_risco_filtered.sort_values('Risco_Terremoto', ascending=False)
elif sort_by == "Risco de Tsunami":
    df_risco_filtered = df_risco_filtered.sort_values('Risco_Tsunami', ascending=False)
else:
    df_risco_filtered = df_risco_filtered.sort_values('Risco_Combinado', ascending=False)

st.markdown("---")

# ========================================
# ESTATÍSTICAS GERAIS
# ========================================

st.subheader("📊 Estatísticas Gerais de Risco")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Países", len(df_risco_filtered))

with col2:
    st.metric("Risco Máximo (Terremoto)", df_risco_filtered['Risco_Terremoto'].max())

with col3:
    st.metric("Risco Máximo (Tsunami)", df_risco_filtered['Risco_Tsunami'].max())

with col4:
    st.metric("Risco Médio Combinado", f"{df_risco_filtered['Risco_Combinado'].mean():.2f}")

st.markdown("---")

# ========================================
# GRÁFICO 6: BARRAS COMPARATIVAS (PLOTLY)
# ========================================

st.subheader("📊 Gráfico 6: Comparativo de Risco por País")

st.markdown("""
Este gráfico de barras mostra o **nível de risco de terremoto e tsunami** para cada país. 
Quanto mais alta a barra, maior o risco geológico. Você pode passar o mouse para ver valores exatos.
""")

if len(df_risco_filtered) > 0:
    try:
        # Derreter o DataFrame para facilitar a plotagem
        df_melted = df_risco_filtered.melt(
            id_vars='Pais',
            value_vars=['Risco_Terremoto', 'Risco_Tsunami'],
            var_name='Tipo_Risco',
            value_name='Nivel_Risco'
        )
        
        # Mapear nomes para português
        df_melted['Tipo_Risco'] = df_melted['Tipo_Risco'].map({
            'Risco_Terremoto': '🏔️ Risco de Terremoto',
            'Risco_Tsunami': '🌊 Risco de Tsunami'
        })
        
        fig_bar = px.bar(
            df_melted,
            x='Pais',
            y='Nivel_Risco',
            color='Tipo_Risco',
            barmode='group',
            title='Nível de Risco de Terremoto e Tsunami por País',
            labels={
                'Nivel_Risco': 'Nível de Risco (0-10)',
                'Pais': 'País',
                'Tipo_Risco': 'Tipo de Risco'
            },
            color_discrete_map={
                '🏔️ Risco de Terremoto': '#d62728',
                '🌊 Risco de Tsunami': '#1f77b4'
            },
            height=500
        )
        
        fig_bar.update_layout(
            xaxis_tickangle=-45,
            hovermode='x unified',
            legend=dict(
                title='Tipo de Risco',
                x=0.01,
                y=0.99
            ),
            xaxis_title='País',
            yaxis_title='Nível de Risco (0-10)'
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de barras: {str(e)}")
else:
    st.warning("Nenhum país encontrado com os filtros selecionados.")

st.markdown("---")

# ========================================
# GRÁFICO INTERATIVO: SCATTER PLOT
# ========================================

st.subheader("📊 Gráfico Interativo: Risco de Terremoto vs. Tsunami")

st.markdown("""
Este gráfico de dispersão mostra a **relação entre risco de terremoto e tsunami** para cada país. 
O tamanho do círculo representa o risco combinado. Passe o mouse para ver detalhes específicos.
""")

if len(df_risco_filtered) > 0:
    try:
        fig_scatter = px.scatter(
            df_risco_filtered,
            x='Risco_Terremoto',
            y='Risco_Tsunami',
            size='Risco_Combinado',
            color='Placa_Tectonica',
            hover_name='Pais',
            hover_data={
                'Risco_Terremoto': ':.1f',
                'Risco_Tsunami': ':.1f',
                'Risco_Combinado': ':.2f',
                'Placa_Tectonica': True
            },
            title='Relação entre Risco de Terremoto e Tsunami',
            labels={
                'Risco_Terremoto': 'Risco de Terremoto (0-10)',
                'Risco_Tsunami': 'Risco de Tsunami (0-10)',
                'Placa_Tectonica': 'Placa Tectônica'
            },
            height=500
        )
        
        fig_scatter.update_layout(
            hovermode='closest',
            xaxis=dict(range=[-0.5, 10.5]),
            yaxis=dict(range=[-0.5, 10.5]),
            legend=dict(
                title='Placa Tectônica',
                x=0.01,
                y=0.99
            ),
            xaxis_title='Risco de Terremoto (0-10)',
            yaxis_title='Risco de Tsunami (0-10)'
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de dispersão: {str(e)}")
else:
    st.warning("Nenhum país encontrado com os filtros selecionados.")

st.markdown("---")

# ========================================
# SELETIVA DE VISUALIZAÇÃO POR PAÍS
# ========================================

st.subheader("🔍 Seletiva de Visualização: Consulte Probabilidades por País")

st.markdown("""
Selecione um país abaixo para visualizar seus dados de risco detalhados de forma clara e organizada.
""")

if len(df_risco) > 0:
    # Seletiva de país
    pais_selecionado = st.selectbox(
        "Escolha um país para visualizar seus dados de risco:",
        options=df_risco['Pais'].sort_values().tolist(),
        key="pais_select"
    )
    
    # Obter dados do país selecionado
    dados_pais = df_risco[df_risco['Pais'] == pais_selecionado].iloc[0]
    
    # Exibir informações do país selecionado
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🏔️ Risco de Terremoto",
            f"{dados_pais['Risco_Terremoto']:.1f}/10"
        )
    
    with col2:
        st.metric(
            "🌊 Risco de Tsunami",
            f"{dados_pais['Risco_Tsunami']:.1f}/10"
        )
    
    with col3:
        risco_combinado = (dados_pais['Risco_Terremoto'] + dados_pais['Risco_Tsunami']) / 2
        st.metric(
            "📊 Risco Combinado",
            f"{risco_combinado:.2f}/10"
        )
    
    # Exibir placa tectônica
    st.info(f"**Placa Tectônica:** {dados_pais['Placa_Tectonica']}")
    
    # Criar visualização em barras horizontais
    st.subheader(f"📈 Análise Detalhada de Risco - {pais_selecionado}")
    
    fig_pais = go.Figure()
    
    fig_pais.add_trace(go.Bar(
        y=['Risco de Terremoto', 'Risco de Tsunami'],
        x=[dados_pais['Risco_Terremoto'], dados_pais['Risco_Tsunami']],
        orientation='h',
        marker=dict(
            color=['#d62728', '#1f77b4']
        ),
        text=[f"{dados_pais['Risco_Terremoto']:.1f}", f"{dados_pais['Risco_Tsunami']:.1f}"],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Nível: %{x:.1f}/10<extra></extra>'
    ))
    
    fig_pais.update_layout(
        title=f'Níveis de Risco Sísmico - {pais_selecionado}',
        xaxis_title='Nível de Risco (0-10)',
        yaxis_title='Tipo de Risco',
        height=400,
        showlegend=False,
        xaxis=dict(range=[0, 10])
    )
    
    st.plotly_chart(fig_pais, use_container_width=True)
else:
    st.warning("Nenhum país disponível para consulta.")

st.markdown("---")

# ========================================
# TABELA DE SELETIVA POR PAÍS
# ========================================

st.subheader("📋 Seletiva Completa: Probabilidade de Terremotos e Tsunamis por País")

st.markdown("""
A tabela abaixo apresenta uma **seletiva completa** dos países com seus respectivos níveis de risco. 
Os valores variam de 0 (sem risco) a 10 (risco máximo).
""")

if len(df_risco_filtered) > 0:
    # Preparar tabela para exibição
    df_display = df_risco_filtered[[
        'Pais',
        'Risco_Terremoto',
        'Risco_Tsunami',
        'Risco_Combinado',
        'Placa_Tectonica'
    ]].copy()
    
    df_display.columns = [
        'País',
        'Risco de Terremoto',
        'Risco de Tsunami',
        'Risco Combinado',
        'Placa Tectônica'
    ]
    
    # Formatar números
    df_display['Risco de Terremoto'] = df_display['Risco de Terremoto'].apply(lambda x: f"{x:.1f}")
    df_display['Risco de Tsunami'] = df_display['Risco de Tsunami'].apply(lambda x: f"{x:.1f}")
    df_display['Risco Combinado'] = df_display['Risco Combinado'].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(df_display, use_container_width=True, height=400)
    
    # Opção de download - Corrigida
    st.markdown("### 📥 Baixar Dados")
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        # Download da seletiva filtrada
        csv_filtrado = df_risco_filtered.to_csv(index=False)
        st.download_button(
            label="📊 Baixar Seletiva Filtrada (CSV)",
            data=csv_filtrado,
            file_name="probabilidade_risco_paises_filtrado.csv",
            mime="text/csv",
            key="btn_download_filtrado"
        )
    
    with col_btn2:
        # Download de todos os países
        csv_completo = df_risco.to_csv(index=False)
        st.download_button(
            label="📊 Baixar Todos os Países (CSV)",
            data=csv_completo,
            file_name="probabilidade_risco_paises_completo.csv",
            mime="text/csv",
            key="btn_download_completo"
        )
else:
    st.info("Nenhum país encontrado com os filtros selecionados.")

st.markdown("---")

# ========================================
# INFORMAÇÕES SOBRE PLACAS TECTÔNICAS
# ========================================

st.subheader("📖 Sobre as Placas Tectônicas")

with st.expander("Clique para expandir informações sobre placas tectônicas"):
    st.markdown("""
    ### Principais Placas Tectônicas e Riscos Sísmicos
    
    **🔹 Anel de Fogo do Pacífico**
    - Região de maior atividade sísmica do planeta
    - Abrange: Japão, Indonésia, Filipinas, Chile, México, Nova Zelândia
    - Responsável por ~90% dos terremotos mundiais
    - Alto risco tanto de terremotos quanto de tsunamis
    
    **🔹 Placa Euroasiática**
    - Abrange Europa, Ásia Central e Oriente Médio
    - Colisão com placas africana e indo-australiana causa terremotos
    - Países afetados: Turquia, Irã, Itália, Grécia
    - Risco moderado a alto
    
    **🔹 Placa Indo-Australiana**
    - Abrange Índia, Nepal, Indonésia e regiões adjacentes
    - Colisão com placa euroasiática causa terremotos frequentes
    - Risco muito alto em Nepal e Indonésia
    
    **🔹 Placa Sul-Americana**
    - Abrange América do Sul
    - Colisão com placa de Nazca causa terremotos no Chile e Peru
    - Brasil está em zona de baixo risco sísmico
    
    **🔹 Placa Norte-Americana**
    - Abrange América do Norte
    - Falhas sísmicas importantes: San Andreas (Califórnia)
    - Risco moderado em regiões específicas
    """)

st.markdown("---")

st.info("💡 Dica: Use a seletiva acima para consultar dados de risco específicos de cada país!")
