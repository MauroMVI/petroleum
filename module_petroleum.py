import requests
import zipfile
import io
import csv



def download_data(url, save_path):
    with requests.get(url, stream=True) as r:
        print(f"Status code: {r.status_code}")
        with io.BytesIO(r.content) as bf:
            with zipfile.ZipFile(bf) as zf:
                zf.extract(filename)




url = 'https://sih.hidrocarburos.gob.mx/downloads/PRODUCCION_POZOS.zip'
filename = 'POZOS_COMPILADO.csv'
save_path = '/petroleum/data'
download_data(url, filename)