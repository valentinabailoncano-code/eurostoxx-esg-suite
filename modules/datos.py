"""
Módulo de carga y extracción de datos financieros y ESG
Autor: Valentina Bailon Cano
"""

import pandas as pd
from typing import Tuple, List
import streamlit as st

@st.cache_data
def cargar_datos() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Carga los tres conjuntos de datos principales: financiero, ESG y metadatos.
    Returns:
        Tuple con tres DataFrames.
    """
    df_f = pd.read_excel('data/Datos_STOXX50_.xlsx', header=[0, 1])
    df_esg = pd.read_excel('data/Datos_STOXX50_.xlsx', sheet_name='ESG', header=[0, 1])
    df_meta = pd.read_excel('data/Datos_STOXX50_.xlsx', sheet_name='Sector')
    return df_f, df_esg, df_meta

def extraer_empresas(df: pd.DataFrame) -> List[str]:
    """
    Extrae las empresas únicas del primer nivel de columnas.
    Args:
        df: DataFrame financiero con columnas multinivel.
    Returns:
        Lista de nombres de empresas ordenados.
    """
    return sorted(set(col[0] for col in df.columns if isinstance(col[0], str)))
