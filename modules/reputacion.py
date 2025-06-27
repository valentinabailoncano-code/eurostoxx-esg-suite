"""
Módulo de análisis reputacional y noticias relevantes
Autor: Valentina Bailon Cano
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import os

load_dotenv()


def buscar_noticias(empresa: str, max_noticias: int = 3):
    """
    Busca titulares relevantes de una empresa en Google News.
    """
    query = f"{empresa} noticias"
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        bloques = soup.select(".dbsr")[:max_noticias]

        noticias = []
        for b in bloques:
            titulo = b.select_one('.nDgy9d')
            link = b.a['href'] if b.a else None
            if titulo and link:
                noticias.append(f"- [{titulo.text}]({link})")

        return noticias

    except requests.exceptions.RequestException:
        return None


def mostrar_reputacion(empresa_sel):
    """
    Muestra titulares + resumen reputacional con IA
    """
    st.subheader("🗞️ Reputación y Noticias")

    if st.button("Consultar Noticias Relevantes"):
        with st.spinner("Buscando titulares y analizando reputación..."):

            noticias = buscar_noticias(empresa_sel)

            if noticias is None:
                st.error("❌ No se pudieron obtener noticias. Revisa tu conexión o vuelve a intentarlo más tarde.")
                return

            if not noticias:
                st.warning("⚠️ No se encontraron titulares recientes sobre esta empresa.")
                return

            st.markdown("### 📰 Titulares recientes:")
            st.markdown("\n".join(noticias))

            try:
                resumen_prompt = f"Redacta un análisis reputacional institucional (máx 5 líneas) sobre estas noticias recientes de {empresa_sel}:\n\n{chr(10).join(noticias)}"

                client = OpenAI()
                rep = client.chat.completions.create(
                    model='gpt-3.5-turbo',
                    messages=[
                        {'role': 'system', 'content': 'Eres analista reputacional institucional.'},
                        {'role': 'user', 'content': resumen_prompt}
                    ]
                )

                st.markdown("### 🤖 Resumen Reputacional IA:")
                st.success(rep.choices[0].message.content)

            except OpenAIError as e:
                st.error("⚠️ Error al usar OpenAI para generar el resumen.")
                st.exception(e)
