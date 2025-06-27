"""
Módulo de visualización de indicadores clave (financieros y ESG)
Autor: Valentina Bailon Cano
"""

import streamlit as st

def mostrar_indicadores(fin_df, esg_df, empresa_sel):
    """
    Muestra las métricas financieras y ESG más recientes de una empresa.
    """
    st.subheader(f"📊 Indicadores clave de {empresa_sel}")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Financieros**")
        for col in fin_df.columns:
            if col[0] == empresa_sel:
                val = fin_df[col].dropna().values[-1]
                st.write(f"{col[1]}: {val}")

    with col2:
        st.markdown("**ESG**")
        for col in esg_df.columns:
            if col[0] == empresa_sel:
                val = esg_df[col].dropna().values[-1]
                st.write(f"{col[1]}: {val}")


def mostrar_metricas_empresa(fin_df, esg_df, empresa_sel):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Financieros**")
        for col in fin_df.columns:
            if col[0] == empresa_sel:
                serie = fin_df[col].dropna().values
                if len(serie) > 0:
                    st.write(f"{col[1]}: {serie[-1]}")
                else:
                    st.write(f"{col[1]}: No disponible")

    with col2:
        st.markdown("**ESG**")
        for col in esg_df.columns:
            if col[0] == empresa_sel:
                serie = esg_df[col].dropna().values
                if len(serie) > 0:
                    st.write(f"{col[1]}: {serie[-1]}")
                else:
                    st.write(f"{col[1]}: No disponible")

