import json
import os
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
import zipfile

Base = declarative_base()

class Estabelecimento(Base):
    __tablename__ = 'estabelecimentos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj_basico = Column(Text)
    cnpj_ordem = Column(Text)
    cnpj_dv = Column(Text)
    matriz_filial = Column(Text)
    nome_fantasia = Column(Text)
    situacao_cadastral = Column(Text)
    data_situacao_cadastral = Column(DateTime)
    motivo_situacao_cadastral = Column(Text)
    nome_cidade_exterior = Column(Text)
    pais = Column(Text)
    data_inicio_atividades = Column(DateTime)
    cnae_fiscal = Column(Text)
    cnae_fiscal_secundaria = Column(Text)
    tipo_logradouro = Column(Text)
    logradouro = Column(Text)
    numero = Column(Text)
    complemento = Column(Text)
    bairro = Column(Text)
    cep = Column(Text)
    uf = Column(Text)
    municipio = Column(Text)
    ddd1 = Column(Text)
    telefone1 = Column(Text)
    ddd2 = Column(Text)
    telefone2 = Column(Text)
    ddd_fax = Column(Text)
    fax = Column(Text)
    correio_eletronico = Column(Text)
    situacao_especial = Column(Text)
    data_situacao_especial = Column(DateTime)

engine = create_engine('postgresql://localhost:5432/cnpj')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

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

        for index, item in df_estabelecimentos.iterrows():
            #TODO: Fix date parsing
            # data_situacao_cadastral = datetime.strptime(str(item['data_situacao_cadastral']), '%Y%m%d') if item['data_situacao_cadastral'] else None
            # data_inicio_atividades = datetime.strptime(str(item['data_inicio_atividades']), '%Y%m%d') if item['data_inicio_atividades'] else None
            # data_situacao_especial = datetime.strptime(str(item['data_situacao_especial']), '%Y%m%d') if item['data_situacao_especial'] else None

            estabelecimento = Estabelecimento(
                cnpj_basico=item['cnpj_basico'],
                cnpj_ordem=item['cnpj_ordem'],
                cnpj_dv=item['cnpj_dv'],
                matriz_filial=item['matriz_filial'],
                nome_fantasia=item['nome_fantasia'],
                situacao_cadastral=item['situacao_cadastral'],
                data_situacao_cadastral=None,
                motivo_situacao_cadastral=item['motivo_situacao_cadastral'],
                nome_cidade_exterior=item['nome_cidade_exterior'],
                pais=item['pais'],
                data_inicio_atividades=None,
                cnae_fiscal=item['cnae_fiscal'],
                cnae_fiscal_secundaria=item['cnae_fiscal_secundaria'],
                tipo_logradouro=item['tipo_logradouro'],
                logradouro=item['logradouro'],
                numero=item['numero'],
                complemento=item['complemento'],
                bairro=item['bairro'],
                cep=item['cep'],
                uf=item['uf'],
                municipio=item['municipio'],
                ddd1=item['ddd1'],
                telefone1=item['telefone1'],
                ddd2=item['ddd2'],
                telefone2=item['telefone2'],
                ddd_fax=item['ddd_fax'],
                fax=item['fax'],
                correio_eletronico=item['correio_eletronico'],
                situacao_especial=item['situacao_especial'],
                data_situacao_especial=None
            )
            session.add(estabelecimento)
            session.commit()

        print(f'{df_estabelecimentos.shape[0]} rows imported.')

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

root_directory = './files/Estabelecimentos'

for root, dirs, files in os.walk(root_directory):
    for file_name in files:
        if file_name.endswith('.zip'):
            file_path = os.path.join(root, file_name)
            print(f"Processing file {file_path}...")
            process_file(file_path)
            print(f"Done! {file_path}.")

session.close()