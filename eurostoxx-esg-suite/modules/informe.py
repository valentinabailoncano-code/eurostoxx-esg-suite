"""
Módulo de generación de informes ejecutivos con GPT-4 y exportación
Autor: Valentina Bailon Cano
"""

import streamlit as st
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from modules.utils_export import exportar_pdf, exportar_docx


def generar_informe_ia(fin_df, esg_df, empresa_sel):
    """
    Genera un informe estratégico con IA y permite descargarlo en PDF o Word.
    """
    st.subheader("📄 Informe Ejecutivo con IA")

    if st.button("Generar Informe Estratégico"):

        # Extraemos los datos financieros y ESG más recientes
        resumen = []
        for col in fin_df.columns:
            if col[0] == empresa_sel:
                valores = fin_df[col].dropna().values
                resumen.append(f"{col[1]}: {valores[-1]}" if len(valores) > 0 else f"{col[1]}: No disponible")

        for col in esg_df.columns:
            if col[0] == empresa_sel:
                valores = esg_df[col].dropna().values
                resumen.append(f"{col[1]}: {valores[-1]}" if len(valores) > 0 else f"{col[1]}: No disponible")

        # Construimos el prompt personalizado
        prompt = f"""
Actúa como estratega institucional en JP Morgan. Redacta un informe profesional en español sobre {empresa_sel}, usando estos datos:
{chr(10).join(resumen)}

Incluye: fortalezas, debilidades, ESG, riesgos, recomendación y considera distribución empírica para el VaR.
Sugiere posibles escenarios de stress test y añade contexto sectorial.
"""

        # Cliente OpenAI moderno
        client = OpenAI()

        # Llamada a GPT-4
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un estratega senior de banca privada."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        # Fecha y hora del informe
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M')
        informe = f"**Informe generado el {fecha_hora}**\n\n" + response.choices[0].message.content

        # Mostrar y exportar
        st.markdown(informe)
        col1, col2 = st.columns(2)

        with col1:
            st.download_button("📥 PDF", data=open(exportar_pdf(informe, f"informe_{empresa_sel}.pdf"), "rb"),
                               file_name=f"informe_{empresa_sel}.pdf")

        with col2:
            st.download_button("📝 Word", data=open(exportar_docx(informe, f"informe_{empresa_sel}.docx"), "rb"),
                               file_name=f"informe_{empresa_sel}.docx")
