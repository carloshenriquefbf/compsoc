# CompSoc
![License](https://img.shields.io/badge/License-MIT-blue.svg)

## Overview

This is a repository for UFRJ's Computers and Society (COS471) class.

## Baixando os dados

O arquivo `baixar_arquivos.py` baixa todos os arquivos de estabelecimentos da url do governo desejada. O formato dos arquivos é descrito no arquivo `./docs/cnpj_metadados.pdf`, disponibilizado pelo governo.

## Importando os dados

O arquivo `criar_dataframe.py` lê todos os arquivos baixados e cria um dataframe pandas com todos os dados.
Nele é possível filtrar os dados por município ou UF. Os códigos SIAFI utilizados para isso estão disponíveis no arquivo `./docs/codigo_siafi.pdf`.

## Buscando CNAEs

O arquivo `buscar_cnaes.py` busca, a partir dos CNPJs disponibilizados pelo usuário num arquivo .csv (com a coluna 'cnpj'), os CNAEs de cada estabelecimento. O resultado é salvo em um arquivo .csv com o nome 'resultado.csv' com 3 colunas, 'cnpj', 'cnae_fiscal' e 'cnae_fiscal_secundaria'.

### Atenção

- Mais informações são disponibilizadas nas funções main de cada arquivo.

- Um arquivo com o dataframe de outubro de 2024 está disponível em `./docs/df_outubro_2024.csv`.
