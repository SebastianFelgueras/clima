import requests
from multiprocessing.pool import ThreadPool
import pandas
import datetime

primer_dato = datetime.date(2022,12,27)# datetime.date(2017,11,27) Fecha de primera medicion
hoy = datetime.date.today()

fechas = pandas.date_range(primer_dato,hoy-datetime.timedelta(days=1),freq='d').to_list()

global base_guardado 
base_guardado = "datos_descargados"
global base 
base = "https://ssl.smn.gob.ar/dpd/descarga_opendata.php?file=observaciones/"
global nombres 
nombres = [f"datohorario{fecha.year}{fecha.month:02d}{fecha.day:02d}.txt" for fecha in fechas]

def download_url(file_name):

    url = base + file_name
 
    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        with open(f"{base_guardado}/{file_name}", 'wb') as f:
            for data in r:
                f.write(data)
    return url
 
print(max(fechas))

# Run 8 multiple threads. Each call will take the next element in urls list
results = ThreadPool(8).imap_unordered(download_url, nombres)
for r in results:
    print(r)