from flask import Flask
import pickle
from datetime import date, timedelta
import requests
import sys
import numpy as np
 
sys.path.insert(0, '/home/sebastian/Documentos/sebastian/experimentos/clima/')
from modelo import ModeloSKL
import modelo
def partir(linea:str):
    #separadores = [9,15,21,26,34,39,44]
    if not linea[0].isdigit():
        return
    res = []
    res.append(linea[:9].strip())
    res.append(linea[9:15].strip())
    res.append(linea[15:21].strip())
    res.append(linea[21:26].strip())
    res.append(linea[26:34].strip())
    res.append(linea[34:39].strip())
    res.append(linea[39:44].strip())
    res.append(linea[44:].strip())
    return res

def procesar_archivo(contenido: str,hoy: date):
    data_aero = list(contenido.splitlines())[2:26]
    data_aero = list(map(partir,data_aero))
    if len(data_aero) != 24 or sum(map(lambda x: x[7] != 'AEROPARQUE AERO',data_aero)) != 0:
        return None
    data_aero.sort(key=lambda x: int(x[1]))
    data_aero = [list(map(lambda x: float(x),x[:-1])) for x in data_aero]
    data = []
    for l in data_aero:
        l[0] = float(hoy.day)
        l.insert(0,float(hoy.month))
        data.append(l)
    print(data)
    data = np.array(data).flatten().reshape(1,-1)
    return data



base = "https://ssl.smn.gob.ar/dpd/descarga_opendata.php?file=observaciones/"
global model

with open("modelo.mod","rb") as f:
    model: ModeloSKL = pickle.load(f)

app = Flask(__name__)

@app.route("/")
def predecir():
    hoy = date.today()
    archivo = f"datohorario{hoy.year}{hoy.month:02d}{hoy.day:02d}.txt"
    r = requests.get(base + archivo)
    if r.status_code != requests.codes.ok:
        return f"No fue posible conectarse con el SMN, error {r.status_code}"
    contenido = str(r.content,encoding="cp1252")
    if contenido.find("El archivo no existe.") != -1:
        hoy = hoy - timedelta(days=1)
        archivo = f"datohorario{hoy.year}{hoy.month:02d}{hoy.day:02d}.txt"
        r = requests.get(base + archivo)
        contenido = str(r.content,encoding="cp1252")
        if contenido.find("El archivo no existe.") != -1:
            return "No pudimos conseguir los datos actuales para hacer la predicción"

    data = procesar_archivo(contenido,hoy)
    if data is None:
        return f"Hubo un problema al parsear los datos del archivo descargado del SMN. Este fue el contenido: {contenido}"
    print(len(data))
    t = model.predecir(data)
    return f"Predicciones para el {hoy + timedelta(days=1)}<br/>Temperatura mínima: {t[0][0]}<br/>Temperatura máxima: {t[0][1]}"