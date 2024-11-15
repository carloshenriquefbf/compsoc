import requests
from bs4 import BeautifulSoup
import os
import argparse

def baixar_dados(
    url: str = 'https://arquivos.receitafederal.gov.br/cnpj/dados_abertos_cnpj/2024-11/',
    path: str = './files'
):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    os.makedirs(path, exist_ok=True)

    for link in links:
        if link.get('href').endswith('.zip') and 'Estabelecimentos' in link.get('href'):
            print(f'Baixando {link.get("href")}...')
            file_name = link.get('href')
            file_url = url + file_name
            full_path = os.path.join(path, file_name)

            with open(full_path, 'wb') as file:
                response = requests.get(file_url)
                file.write(response.content)
                print(f'{file_name} baixado.')

if __name__ == "__main__":
    """
    O objetivo deste script é baixar os arquivos .csv contendo informações sobre estabelecimentos.
    Esses arquivos são disponibilizados pela Receita Federal.
    Fonte: https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj

    Exemplo de uso:
    python3 baixar_arquivos.py --file ./files --url https://arquivos.receitafederal.gov.br/cnpj/dados_abertos_cnpj/2024-11/
    """

    parser = argparse.ArgumentParser(description=" ")
    parser.add_argument(
        "--url",
        help="URL dos arquivos. Default é utilizar arquivos de Novembro de 2024.",
        default="https://arquivos.receitafederal.gov.br/cnpj/dados_abertos_cnpj/2024-11/"
    )
    parser.add_argument(
        "--path",
        help="Local de download dos arquivos. Default é ./files",
        default="./files"
    )

    args = parser.parse_args()
    baixar_dados(args.url, args.path)