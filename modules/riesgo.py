"""
Módulo de análisis de riesgo financiero y sectorial
Incluye cálculos de volatilidad, VaR y clasificaciones cualitativas
Autor: Valentina Bailon Cano
"""

import streamlit as st
import numpy as np
import pandas as pd
from typing import Optional
from datetime import datetime
from .utils_export import exportar_pdf, exportar_docx

def calcular_volatilidad(df: pd.DataFrame, empresa: str) -> float:
    for col in df.columns:
        if col[0] == empresa and 'Revenue' in col[1]:
            serie = df[col].dropna().values
            return np.std(serie) / np.mean(serie) if len(serie) > 2 else 0
    return 0

def calcular_var(df: pd.DataFrame, empresa: str, alpha: float = 0.05) -> float:
    for col in df.columns:
        if col[0] == empresa and 'Free Cash Flow' in col[1]:
            serie = pd.Series(df[col].dropna().values)
            return -serie.quantile(alpha) if not serie.empty else 0
    return 0

def clasificar_riesgo_sector(sector: str) -> str:
    riesgo_bajo = ['Utilities', 'Healthcare', 'Telecommunications']
    riesgo_alto = ['Tech', 'Financials', 'Energy']
    if sector in riesgo_bajo:
        return '🟢 Bajo'
    elif sector in riesgo_alto:
        return '🔴 Alto'
    return '🟡 Medio'

def mostrar_analisis_riesgo(fin_df, meta_df, empresa_sel):
    st.subheader('🧮 Análisis de Riesgo')
    sector = meta_df[meta_df.iloc[:, 0] == empresa_sel].iloc[0, 2]
    pais = meta_df[meta_df.iloc[:, 0] == empresa_sel].iloc[0, 3]
    volatilidad = calcular_volatilidad(fin_df, empresa_sel)
    var_95 = calcular_var(fin_df, empresa_sel)
    st.markdown(f'**Sector:** {sector} | **País:** {pais}')
    st.markdown(f'- Riesgo sectorial estimado: {clasificar_riesgo_sector(sector)}')
    st.markdown(f'- Volatilidad histórica (ingresos): `{volatilidad:.2%}`')
    st.markdown(f'- Value at Risk (95%): `{var_95:,.2f}` € (basado en distribución empírica)')
    st.caption('Nota: Se recomienda aplicar stress test simulando caídas del 20% en ingresos o subidas del 10% en costes.')
