
import pandas as pd

def cargar_datos():
    fin = pd.read_excel("data/DATOS_EUROSTOXX50.xlsx", sheet_name="Financiero", header=[0, 1])
    esg = pd.read_excel("data/DATOS_EUROSTOXX50.xlsx", sheet_name="ESG", header=[0, 1])
    meta = pd.read_excel("data/DATOS_EUROSTOXX50.xlsx", sheet_name="Sector")
    return fin, esg, meta
