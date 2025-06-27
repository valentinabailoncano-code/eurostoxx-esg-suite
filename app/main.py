"""
App principal de la suite de análisis EURO STOXX 50
Desarrollado por Valentina Bailon Cano | Máster DS & IA - EVOLVE
"""

import sys
import os
import streamlit as st

# Aseguramos que el directorio raíz esté en el path
sys.path.append(os.path.abspath('.'))

# Importaciones desde los módulos personalizados
from modules.datos import cargar_datos, extraer_empresas
from modules.riesgo import calcular_volatilidad, calcular_var, clasificar_riesgo_sector
from modules.reputacion import mostrar_reputacion
from modules.informe import generar_informe_ia
from modules.utils_export import exportar_pdf, exportar_docx
from modules.visual import mostrar_metricas_empresa

# Configuración de la interfaz
st.set_page_config(page_title='EURO STOXX 50 | Risk & ESG AI Suite', layout='wide', page_icon='📊')
st.title('📊 Plataforma Institucional de Inteligencia Financiera - EURO STOXX 50')
st.markdown('''**Desarrollado por Valentina Bailon Cano**  
- Análisis financiero y sostenibilidad ESG.
- Value at Risk, estrés financiero y reputación pública.
- Informes ejecutivos automatizados en PDF y Word con IA.
''')

# Cargar datos
fin_df, esg_df, meta_df = cargar_datos()
empresas = extraer_empresas(fin_df)
empresa_sel = st.selectbox('Selecciona una empresa del índice:', empresas)

# Obtener nombre completo desde el meta_df (columna 1 = Company)
nombre_empresa = meta_df[meta_df.iloc[:, 0] == empresa_sel].iloc[0, 1]


# Visualización de indicadores clave
mostrar_metricas_empresa(fin_df, esg_df, empresa_sel)

# Análisis de riesgo (inline por ahora)
st.subheader("🧮 Análisis de Riesgo")
sector = meta_df[meta_df.iloc[:, 0] == empresa_sel].iloc[0, 2]
pais = meta_df[meta_df.iloc[:, 0] == empresa_sel].iloc[0, 3]
volatilidad = calcular_volatilidad(fin_df, empresa_sel)
var_95 = calcular_var(fin_df, empresa_sel)
st.markdown(f"**Sector:** {sector} | **País:** {pais}")
st.markdown(f"- Riesgo sectorial estimado: {clasificar_riesgo_sector(sector)}")
st.markdown(f"- Volatilidad histórica (ingresos): `{volatilidad:.2%}`")
st.markdown(f"- Value at Risk (95%): `{var_95:,.2f}` €")
st.caption("Se recomienda aplicar stress test simulando caídas de ingresos o subidas de costes.")

# Generar informe IA
generar_informe_ia(fin_df, esg_df, empresa_sel)

# Noticias y reputación con IA
mostrar_reputacion(nombre_empresa)

# Footer institucional
st.markdown('---')
st.image('assets/evolve_logo.png', width=130)
st.caption('Versión Enterprise · Valentina Bailon · Máster DS & IA · EVOLVE · 2025')
