from multiprocessing.pool import ThreadPool
import os
import csv

directorio_datos = os.scandir("datos_descargados")

headers = ["fecha", "hora", "temperatura", "humedad", "presion", "direccion_viento", "velocidad_viento", "estacion"]

# test = ["""28122022     3  -1.0   83   991.0   50    9     BASE SAN MARTIN                                     
# ""","""28122022    15  20.0   26          270   37     GOBERNADOR GREGORES AERO                            
# """, """22072022    10  24.5   59  1009.9   20   17     PRESIDENCIA ROQUE SAENZ PE""",                          
# """                                            �A AERO                               """,                  
# """                                                                                                    
# """]

def procesar(archivo):
    l = []
    with open(f"datos_descargados/{archivo.name}",mode="r",encoding="cp1252") as f:
        for line in f.readlines():
            s = partir(line)
            if s == None:
                continue
            l.append(s)
    return l
 

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

# [print(partir(i)) for i in test] 


# Run 8 multiple threads. Each call will take the next element in urls list
results = ThreadPool(8).imap_unordered(procesar, directorio_datos)
with open("clima_arg.csv","w") as a:
    writer = csv.writer(a)
    writer.writerow(headers)
    for result in results:
        writer.writerows(result)
    

