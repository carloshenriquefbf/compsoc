# CompSoc

## Overview

This is a repository for UFRJ's Computers and Society (COS471) class.

## Baixando os dados

O arquivo `export.py` baixa todos os arquivos da pasta do governo. O formato dos arquivos é descrito no arquivo `cnpj_metadados.pdf`, disponibilizado pelo governo.

## Importando os dados

O arquivo `mining-db.py` importa os dados de um dado município para um banco de dados. O código do municipio pode ser encontrado no arquivo `codigo_siafi.pdf`, disponibilizado pelo governo.

O arquivo `mining-df.py` gera um arquivo `final_df.csv` que contém os dados do municípios escolhido.