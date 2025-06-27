"""
Módulo de generación de informes ejecutivos con GPT y exportación
Autor: Valentina Bailon Cano
"""

import streamlit as st
from datetime import datetime
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from modules.utils_export import exportar_pdf, exportar_docx
import os

load_dotenv()

def generar_informe_ia(fin_df, esg_df, empresa_sel):
    """
    Genera un informe estratégico con IA y permite descargarlo en PDF o Word.
    """
    st.subheader("📄 Informe Ejecutivo con IA")

    if st.button("Generar Informe Estratégico"):
        with st.spinner("Generando informe con inteligencia artificial..."):

            try:
                resumen = []
                for col in fin_df.columns:
                    if col[0] == empresa_sel:
                        valores = fin_df[col].dropna().values
                        resumen.append(f"{col[1]}: {valores[-1]}" if len(valores) > 0 else f"{col[1]}: No disponible")

                for col in esg_df.columns:
                    if col[0] == empresa_sel:
                        valores = esg_df[col].dropna().values
                        resumen.append(f"{col[1]}: {valores[-1]}" if len(valores) > 0 else f"{col[1]}: No disponible")

                prompt = f"""
Eres analista institucional. Redacta un informe profesional sobre {empresa_sel} basado en estos datos:

{chr(10).join(resumen)}

Incluye:
- Fortalezas y debilidades financieras
- Riesgos y oportunidades ESG
- Recomendación estratégica (tono neutro)
- Value at Risk y posibles escenarios futuros
"""

                client = OpenAI()

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Eres analista financiero especializado en ESG."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5
                )

                fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M')
                informe = f"**Informe generado el {fecha_hora}**\n\n" + response.choices[0].message.content
                st.markdown(informe)

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button("📥 Descargar PDF", data=open(exportar_pdf(informe, f"informe_{empresa_sel}.pdf"), "rb"),
                                       file_name=f"informe_{empresa_sel}.pdf")

                with col2:
                    st.download_button("📝 Descargar Word", data=open(exportar_docx(informe, f"informe_{empresa_sel}.docx"), "rb"),
                                       file_name=f"informe_{empresa_sel}.docx")

            except OpenAIError as e:
                st.error("⚠️ Error al conectar con la API de OpenAI.")
                st.exception(e)
            except Exception as ex:
                st.error("❌ Error inesperado al generar el informe.")
                st.exception(ex)
