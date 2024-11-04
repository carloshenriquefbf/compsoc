import os
from datetime import datetime
import pandas as pd
import zipfile

codigo_municipio = '5853'

colunas_estabelecimentos = ['cnpj_basico','cnpj_ordem', 'cnpj_dv','matriz_filial',
              'nome_fantasia',
              'situacao_cadastral','data_situacao_cadastral',
              'motivo_situacao_cadastral',
              'nome_cidade_exterior',
              'pais',
              'data_inicio_atividades',
              'cnae_fiscal',
              'cnae_fiscal_secundaria',
              'tipo_logradouro',
              'logradouro',
              'numero',
              'complemento','bairro',
              'cep','uf','municipio',
              'ddd1', 'telefone1',
              'ddd2', 'telefone2',
              'ddd_fax', 'fax',
              'correio_eletronico',
              'situacao_especial',
              'data_situacao_especial']

def zip_ref(filepath):
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        filename = file_list[0]
        return zip_ref.open(filename)

def process_file(file_path):
    try:
        df_estabelecimentos = pd.read_csv(zip_ref(file_path), delimiter=';', encoding='ISO-8859-1', names=colunas_estabelecimentos, dtype=str)
        df_estabelecimentos = df_estabelecimentos[df_estabelecimentos['municipio'] == codigo_municipio]
        df_estabelecimentos = df_estabelecimentos.where(pd.notnull(df_estabelecimentos), None)

        return df_estabelecimentos
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

root_directory = './files/Estabelecimentos'
final_df = pd.DataFrame()

for root, dirs, files in os.walk(root_directory):
    for file_name in files:
        if file_name.endswith('.zip'):
            file_path = os.path.join(root, file_name)
            print(f"Processing file {file_path}...")
            current_df = process_file(file_path)
            final_df = pd.concat([final_df, current_df])
            print(f"Done! {file_path}.")

final_df.to_csv('final_df.csv', index=False)