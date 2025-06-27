# 💼 EURO STOXX 50 | Risk & ESG Intelligence Suite

**Autor:** Valentina Bailon Cano  
**Máster en Data Science & IA – EVOLVE 2025**

![Streamlit](https://img.shields.io/badge/Framework-Streamlit-blue?logo=streamlit)
![OpenAI](https://img.shields.io/badge/Powered%20by-GPT--4-blueviolet?logo=openai)
![PDF Export](https://img.shields.io/badge/Export-PDF%20%7C%20Word-green)
![Status](https://img.shields.io/badge/Status-Enterprise%20Ready-brightgreen)

---

📊 Esta aplicación profesional permite el análisis integral de empresas del índice **EURO STOXX 50**, integrando:
- Indicadores financieros y ESG.
- Análisis de riesgo (volatilidad, VaR, clasificación sectorial).
- Reputación pública mediante scraping y resumen automático de noticias.
- Generación de informes ejecutivos en **PDF y Word con ayuda de IA** (GPT-4).

---

## 📁 Estructura del proyecto
- `app/` → interfaz principal de Streamlit (`main.py`)
- `modules/` → lógica modular del negocio (riesgo, datos, reputación, IA, exportación)
- `data/` → archivos de entrada como `Datos_STOXX50_.xlsx`
- `outputs/` → informes generados por el usuario
- `assets/` → imágenes, logos
- `.env.example` → plantilla para insertar tu clave de OpenAI
- `requirements.txt` → dependencias necesarias

## ⚙️ Cómo ejecutar
```bash
git clone https://github.com/tuusuario/eurostoxx-esg-risk-suite.git
cd eurostoxx-esg-risk-suite
cp .env.example .env  # o crea manualmente el .env
pip install -r requirements.txt
streamlit run app/main.py
```

## 🧠 Autoría y contexto académico
Desarrollado como proyecto final individual para el **Módulo 1 del Máster en Data Science & IA en EVOLVE**. Diseñado con enfoque enterprise para entornos de banca, consultoría o gestión de activos.

---
© 2025 Valentina Bailon Cano – Todos los derechos reservados
