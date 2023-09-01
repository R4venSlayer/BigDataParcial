from bs4 import BeautifulSoup
import boto3
import pandas as pd
import datetime
from io import BytesIO


def main():
    s3 = boto3.client('s3')
    bucket_name = 'khadajhinnnn'
    ruta = 'news/raw/'
    archivo_nombre = ruta+datetime.datetime.now().strftime('%Y-%m-%d')+'.html'
    response = s3.get_object(Bucket=bucket_name, Key=archivo_nombre)
    # Leer el contenido del objeto (archivo)
    contenido = response['Body'].read().decode('utf-8')

    soup = BeautifulSoup(contenido, 'html.parser')

    for span_etq in soup.find_all('span'):
        span_etq.extract()

    categoria = soup.find_all('div', class_='category-published')
    titulos = soup.find_all('h2', class_='title-container')
    enlaces = soup.find_all('a', class_='title page-link')

    lst_c = ['categoria']
    lst_t = ['titulo']
    lst_e = ['enlace']

    for c in categoria:
        lst_c.append(c.text)
    for t in titulos:
        lst_t.append(t.text)
    for e in enlaces:
        lst_e.append('https://eltiempo.com'+e['href'])

    lst = [lst_c, lst_t, lst_e]

    longitud = 41

    while len(lst_c) < longitud:
        lst_c.append(None)
    while len(lst_t) < longitud:
        lst_t.append(None)

    df = pd.DataFrame(lst[1:], columns=lst[0])
    fecha = datetime.datetime.now().strftime('%Y-%m-%d')
    df.to_csv(fecha+'.csv', index=False)
    # Obtener la fecha actual
    fecha_actual = datetime.datetime.now()
    año = fecha_actual.year
    mes = fecha_actual.month
    dia = fecha_actual.day

    name_file = f'{año:04d}-{mes:02d}-{dia:02d}'
    ruta_objeto = f'headlines/final/year={año}/month={mes:02d}/'+name_file+'.csv'

    s3 = boto3.client('s3')
    # Subir el archivo en memoria a S3
    
    archivo_m = BytesIO(contenido.encode('utf-8'))  

    s3.upload_fileobj(archivo_m, 'khadajhinnnn-b', ruta_objeto)

    print('Se ha subido correctamente el csv')


main()
