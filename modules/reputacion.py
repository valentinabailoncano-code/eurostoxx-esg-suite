"""
Módulo de análisis reputacional y noticias relevantes
Autor: Valentina Bailon Cano
"""

import requests
from bs4 import BeautifulSoup
import streamlit as st
import openai

def buscar_noticias(empresa: str, max_noticias: int = 3):
    """
    Busca titulares relevantes en Google News.
    """
    query = f"{empresa} noticias"
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error("Error al obtener noticias. Intenta de nuevo más tarde.")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    blocks = soup.select(".dbsr")[:max_noticias]
    return [f"- [{b.select_one('.nDgy9d').text}]({b.a['href']})" for b in blocks if b.select_one(".nDgy9d")]

def mostrar_reputacion(empresa_sel):
    """
    Sección reputacional: titulares + resumen ESG automático
    """
    st.subheader("🗞️ Reputación y Noticias")
    if st.button("Consultar Noticias Relevantes"):
        noticias = buscar_noticias(empresa_sel)
        st.markdown("\n".join(noticias))
        if noticias:
            resumen_prompt = f"Resumen ESG reputacional sobre estas noticias de {empresa_sel} en español en máximo 5 líneas:\n{chr(10).join(noticias)}"
            rep = openai.ChatCompletion.create(
                model='gpt-4',
                messages=[
                    {'role': 'system', 'content': 'Analista reputacional institucional.'},
                    {'role': 'user', 'content': resumen_prompt}
                ]
            )
            st.markdown(rep.choices[0].message['content'])

def analizar_noticias(noticias: list, empresa: str) -> str:
    # Aquí podrías usar GPT o análisis de sentimiento para generar un resumen reputacional
    # Por ejemplo:
    resumen_prompt = f"Resumen ESG reputacional sobre estas noticias de {empresa} en español en máximo 5 líneas:\n{chr(10).join(noticias)}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Analista reputacional institucional."},
            {"role": "user", "content": resumen_prompt}
        ]
    )

    return response.choices[0].message["content"]
