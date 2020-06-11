import requests
import zipfile
import io
import csv



def download_zip(url, filename):
    r = requests.get(url)
    # z = zipfile.ZipFile(io.BytesIO(r.content))
    # with z.open(filename, 'r') as f:
    #     reader = zip.read(filename)
    #     for row in reader:
    #         print(row)



url = 'https://sih.hidrocarburos.gob.mx/downloads/PRODUCCION_POZOS.zip'
filename = 'POZOS_COMPILADO.csv'
download_zip(url, filename)