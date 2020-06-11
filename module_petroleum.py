import requests
import zipfile
import io
import csv



def download_zip(url, save_path):
    r = requests.get(url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extract(filename)



url = 'https://sih.hidrocarburos.gob.mx/downloads/PRODUCCION_POZOS.zip'
filename = 'POZOS_COMPILADO.csv'
save_path = '/home/mmvi/mexico/petroleum/data'
download_zip(url, filename)