import requests
from bs4 import BeautifulSoup

url = 'https://arquivos.receitafederal.gov.br/cnpj/dados_abertos_cnpj/2024-10/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')

for link in links:
    if link.get('href').endswith('.zip'):
        file_name = link.get('href')
        file_url = url + file_name
        with open(file_name, 'wb') as file:
            response = requests.get(file_url)
            file.write(response.content)
            print(f'{file_name} downloaded')
