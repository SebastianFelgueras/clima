from flask import Flask
import pickle
from datetime import date, timedelta
import requests
import sys
 
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

def procesar_archivo(contenido: str):
    data_aero = list(contenido.splitlines())[2:26]
    data_aero = list(map(partir,data_aero))
    if len(data_aero) != 24 or sum(map(lambda x: x[7] != 'AEROPARQUE AERO',data_aero)) != 0:
        return "cambiaron el formato :("
    data_aero.sort(key=lambda x: int(x[1]))



base = "https://ssl.smn.gob.ar/dpd/descarga_opendata.php?file=observaciones/"
global modelo

with open("modelo.mod","rb") as f:
    modelo = pickle.load(f)

app = Flask(__name__)

@app.route("/")
def predecir():
    hoy = date.today()
    archivo = f"datohorario{hoy.year}{hoy.month:02d}{hoy.day:02d}.txt"
    r = requests.get(base + archivo)
    if r.status_code != requests.codes.ok:
        return "No fue posible conectarse con el SMN"
    contenido = str(r.content,encoding="cp1252")
    if contenido.find("El archivo no existe.") != -1:
        hoy = hoy - timedelta(days=1)
        archivo = f"datohorario{hoy.year}{hoy.month:02d}{hoy.day:02d}.txt"
        print(hoy)
        r = requests.get(base + archivo)
        contenido = str(r.content,encoding="cp1252")
    procesar_archivo(contenido)

    return f"Predicciones para el {hoy + timedelta(days=1)}<br/>{data_aero}"