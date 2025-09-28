# -*- coding: utf-8 -*-
"""
Dashboard solAGire – versão organizada em tabs (Fase 1)
"""

import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
import plotly.express as px

# ================================
# Dados geográficos
# ================================
LOCALIZACAO = "Coimbra, Portugal"
LATITUDE = 40.2033
LONGITUDE = -8.4103
ALTITUDE = 100  # aprox. em metros

# ================================
# Função para gerar dados aleatórios
# ================================
def gerar_dados_aleatorios(n=50):
    """Gera um DataFrame com n registos simulados"""
    agora = dt.datetime.now()
    timestamps = [agora - dt.timedelta(minutes=30*i) for i in range(n)]
    df = pd.DataFrame({
        "timestamp": timestamps[::-1],

        # Variáveis ambientais
        "temp_ar": np.random.uniform(15, 35, n),
        "humidade_relativa": np.random.uniform(30, 90, n),
        "irradiancia": np.random.uniform(200, 1000, n),
        "humidade_solo": np.random.uniform(10, 60, n),

        # Variáveis do painel/sistema
        "tensao": np.random.uniform(200, 400, n),         # V
        "corrente": np.random.uniform(0, 20, n),          # A
        "potencia": np.random.uniform(0, 5000, n),        # W
        "temp_painel": np.random.uniform(20, 50, n),      # ºC
        "bateria": np.random.uniform(20, 100, n),         # %
        "inclinacao": np.random.randint(0, 90, n)         # º
    })
    return df


# ================================
# Carregar dados simulados
# ================================
df = gerar_dados_aleatorios()
ultimo = df.iloc[-1]





# ================================
# Layout principal
# ================================
st.set_page_config(page_title="Plataforma solAGire", layout="wide")
#st.title("☀️ Plataforma solAGire")
#st.markdown("Dashboard para monitorização do sistema agrovoltaico (dados simulados).")
#agora = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#st.markdown(f"🕒 **{agora}** | 📍 **{LOCALIZACAO}** (Lat: {LATITUDE}, Lon: {LONGITUDE}, Alt: {ALTITUDE}m)")


# Criar header com hora em tempo real
col_top1, col_top2, col_top3 = st.columns([6, 2, 2])
with col_top1:
    st.title("Plataforma SolarAGire")
    st.markdown("Dashboard para monitorização do sistema agrovoltaico (dados simulados).")
with col_top2:
    agora = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.markdown(f"🕒 **{agora}**")
with col_top3:
    # Rodapé com localização
    st.markdown("---")
    st.markdown(f"📍 Localização: **{LOCALIZACAO}** (Lat: {LATITUDE}, Lon: {LONGITUDE}, Alt: {ALTITUDE}m)")

# Criar tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Visão Geral", "🌱 Ambiente", "⚡ Sistema", "🎯 Inclinação", "🚨 Alertas"])

# ================================
# Tab 1: Visão Geral
# ================================
with tab1:
    st.header("Resumo Atual")
    col1, col2, col3 = st.columns(3)
    col1.metric("Potência (W)", f"{ultimo['potencia']:.1f}", delta_color="off")
    col2.metric("Temp. Painel (°C)", f"{ultimo['temp_painel']:.1f}")
    col3.metric("Bateria (%)", f"{ultimo['bateria']:.1f}")

    st.subheader("Produção (últimas 24h)")
    limite_tempo = ultimo["timestamp"] - dt.timedelta(hours=24)
    df_24h = df[df["timestamp"] >= limite_tempo]
    fig = px.line(df_24h, x="timestamp", y="potencia", title="Potência Gerada (W)")
    st.plotly_chart(fig, use_container_width=True)

# ================================
# Tab 2: Ambiente
# ================================
with tab2:
    st.header("Dados Ambientais")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Temp. ar (°C)", f"{ultimo['temp_ar']:.1f}")
    col2.metric("Humidade Relativa (%)", f"{ultimo['humidade_relativa']:.1f}")
    col3.metric("Irradiância (W/m²)", f"{ultimo['irradiancia']:.1f}")
    col4.metric("Humidade do Solo (%)", f"{ultimo['humidade_solo']:.1f}")

    st.subheader("Gráficos Ambientais (últimas 24h)")
    fig1 = px.line(df_24h, x="timestamp", y=["irradiancia", "temp_ar"], title="Irradiância vs Temp. Ar")
    fig2 = px.line(df_24h, x="timestamp", y=["humidade_relativa", "humidade_solo"], title="Humidade Ar vs Solo")
    col5, col6 = st.columns(2)
    col5.plotly_chart(fig1, use_container_width=True)
    col6.plotly_chart(fig2, use_container_width=True)

# ================================
# Tab 3: Sistema
# ================================
with tab3:
    st.header("Dados do Sistema")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Tensão (V)", f"{ultimo['tensao']:.1f}")
    col2.metric("Corrente (A)", f"{ultimo['corrente']:.1f}")
    col3.metric("Potência (W)", f"{ultimo['potencia']:.1f}")
    col4.metric("Temp. Painel (°C)", f"{ultimo['temp_painel']:.1f}")
    col5.metric("Bateria (%)", f"{ultimo['bateria']:.1f}")

# ================================
# Tab 4: Inclinação
# ================================
with tab4:
    st.header("Controlo de Inclinação")
    modo = st.radio("Modo de operação", ["Automático", "Manual"])
    nova_inclinacao = st.slider("Ajustar inclinação do painel", 0, 90, int(ultimo["inclinacao"]))
    st.write(f"Modo atual: {modo}")
    st.write(f"Inclinação selecionada: {nova_inclinacao}°")

    # Inclinação ideal (placeholder melhorado)
    dia_do_ano = dt.datetime.now().timetuple().tm_yday
    declinacao = 23.45 * np.sin(np.deg2rad((360/365) * (dia_do_ano - 81)))
    inclinacao_ideal = round(abs(LATITUDE - declinacao), 1)
    st.metric("Inclinação Ideal (°)", inclinacao_ideal)

# ================================
# Tab 5: Alertas
# ================================
with tab5:
    st.header("Alertas do Sistema")
    alertas = []
    if ultimo["humidade_solo"] < 15:
        alertas.append("⚠️ Humidade do solo muito baixa – ativar irrigação.")
    if ultimo["bateria"] < 30:
        alertas.append("🔋 Nível de bateria baixo.")
    if ultimo["irradiancia"] > 700 and ultimo["potencia"] < 1000:
        alertas.append("🧽 Possível sujidade nos painéis (irradiância alta mas baixa produção).")

    if alertas:
        for a in alertas:
            st.warning(a)
    else:
        st.success("✅ Sistema operacional sem alertas.")

