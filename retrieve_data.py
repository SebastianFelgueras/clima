import requests
from multiprocessing.pool import ThreadPool
global base_guardado 
base_guardado = "datos_descargados"
global base 
base = "https://ssl.smn.gob.ar/dpd/descarga_opendata.php?file=observaciones/"
global nombres 
nombres = []
for anio in [2017,2018,2019,2020,2021,2022]:
    for mes in range(1,13):
        for dia in range(1,31):
            if dia > 28 and mes == 2:
                continue
            elif mes in [4,6,9,11] and dia == 31:
                continue
            elif anio == 2017 and mes == 11 and dia <=25: #este es el último día sin datos
                continue
            elif anio == 2017 and mes < 11:
                continue
            nombres.append(f"datohorario{anio}{mes:02d}{dia:02d}.txt")

def download_url(file_name):

    url = base + file_name
 
    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        with open(f"{base_guardado}/{file_name}", 'wb') as f:
            for data in r:
                f.write(data)
    return url
 
 

# Run 8 multiple threads. Each call will take the next element in urls list
results = ThreadPool(8).imap_unordered(download_url, nombres)
for r in results:
    print(r)