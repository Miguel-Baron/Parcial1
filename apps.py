import boto3
import requests
import datetime
import csv
from io import StringIO
from bs4 import BeautifulSoup


def download_file():
    url = ('https://casas.mitula.com.co/searchRE/'
       'nivel3-Chapinero/nivel2-Bogotá/'
       'nivel1-Cundinamarca/q-Bogotá-Chapinero')

    # Descargar el archivo
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    return response


def f():
    now = datetime.datetime.now()
    date_string = now.strftime('%Y-%m-%d')

    # Concatenar la cadena formateada con la extensión del archivo
    file_name = f'{date_string}.html'

    bucket_name = 'landing-casas'
    response = download_file()
    content = response.content

    # Configurar el cliente de S3
    s3 = boto3.client('s3')

    # Subir el archivo a S3
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=content
    )

    return 200


def f2():
    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket('landing-casas')
    obj = s3_bucket.Object(f"{datetime.datetime.now().strftime('%Y-%m-%d')}.html")
    body = obj.get()['Body'].read()

    # Pasar el contenido HTML de la respuesta HTTP GET a un objeto BeautifulSoup
    soup = BeautifulSoup(body, 'html.parser')

    # Buscar los elementos HTML que contienen la información de cada casa
    casas = soup.find_all('div', {'class': 'card-list-item'})

    # Crear una lista vacía para almacenar la información de cada casa
    data = []

    # Iterar sobre cada casa y extraer su información
    for casa in casas:
        # Extraer información de la casa
        barrio = casa.find('h2', {'class': 'card-title'}).text.strip()
        valor = casa.find('span', {'class': 'card-price'}).text.strip()
        detalles = casa.find_all('li', {'class': 'card-feature'})
        num_habitaciones = detalles[0].text.strip()
        num_banos = detalles[1].text.strip()
        mts2 = detalles[2].text.strip()

        # Agregar la información de la casa a la lista de datos
        data.append([
            datetime.date.today(),
            barrio,
            valor,
            num_habitaciones,
            num_banos,
            mts2
        ])

    csv_data = StringIO()
    writer = csv.writer(csv_data)
    for row in data:
        writer.writerow(row)
    csv_string = csv_data.getvalue()

    # Subir el archivo CSV a un bucket de S3
    s3_client = boto3.client('s3')
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}.csv"
    s3_client.put_object(
        Body=csv_string.encode('utf-8'),
        Bucket='casas-final',
        Key=filename
    )

    return 200


def download_html(url):
    response = requests.get(url)

    return response
