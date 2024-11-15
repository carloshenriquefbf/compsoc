import os
import pandas as pd
import zipfile
import argparse
from typing import Optional

def filtrar_municipio(df: pd.DataFrame, codigo_municipio: str) -> pd.DataFrame:
    return df[df["municipio"] == codigo_municipio]

def filtrar_uf(df: pd.DataFrame, codigo_uf: str) -> pd.DataFrame:
    return df[df["uf"] == codigo_uf]

def zip_ref(filepath: str) -> zipfile.ZipFile:
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        file_list = zip_ref.namelist()
        filename = file_list[0]
        return zip_ref.open(filename)

def processar_arquivo(
        path: str = "./files",
        filtro_municipio: Optional[bool] = False,
        filtro_uf: Optional[bool] = False,
        codigo_municipio: Optional[str] = None,
        codigo_uf: Optional[str] = None
) -> pd.DataFrame:
    colunas = [
        "cnpj_basico",
        "cnpj_ordem",
        "cnpj_dv",
        "matriz_filial",
        "nome_fantasia",
        "situacao_cadastral",
        "data_situacao_cadastral",
        "motivo_situacao_cadastral",
        "nome_cidade_exterior",
        "pais",
        "data_inicio_atividades",
        "cnae_fiscal",
        "cnae_fiscal_secundaria",
        "tipo_logradouro",
        "logradouro",
        "numero",
        "complemento",
        "bairro",
        "cep",
        "uf",
        "municipio",
        "ddd1",
        "telefone1",
        "ddd2",
        "telefone2",
        "ddd_fax",
        "fax",
        "correio_eletronico",
        "situacao_especial",
        "data_situacao_especial"
    ]

    try:
        df = pd.read_csv(zip_ref(path), delimiter=";", encoding="ISO-8859-1", names=colunas, dtype=str)

        if filtro_municipio:
            df = filtrar_municipio(df, codigo_municipio)

        if filtro_uf:
            df = filtrar_uf(df, codigo_uf)

        df = df.where(pd.notnull(df), None)

        return df
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {path}")
    except Exception as e:
        print(f"Erro processando arquivo {path}: {e}")

def criar_dataframe(
        path: str = "./files",
        filtro_municipio: Optional[bool] = False,
        filtro_uf: Optional[bool] = False,
        codigo_municipio: Optional[str] = None,
        codigo_uf: Optional[str] = None
):
    df = pd.DataFrame()

    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(".zip"):
                file_path = os.path.join(root, file_name)
                print(f"Processando arquivo {file_path}...")

                current_df = processar_arquivo(
                    file_path,
                    filtro_municipio,
                    filtro_uf,
                    codigo_municipio,
                    codigo_uf
                )

                df = pd.concat([df, current_df])

                print(f"Arquivo processado! {file_path}.")

    df.to_csv("df.csv", index=False)

if __name__ == "__main__":
    """
    O objetivo deste script é criar um DataFrame com as informações dos estabelecimentos.
    Há a possibilidade de filtrar por município e/ou UF. Os códigos de município são os códigos SIAFI e podem
    ser encontrados em ./docs/codigo_siafi.pdf.

    Exemplo de uso:
    python3 criar_dataframe.py --path ./files --filtrar_municipio True --codigo_municipio 5853
    """

    parser = argparse.ArgumentParser(description=" ")
    parser.add_argument(
        "--path",
        help="Local de download dos arquivos. Default é ./files",
        default="./files"
    )
    parser.add_argument(
        "--filtrar_municipio",
        help="Filtrar por município. Default é False.",
        default=False
    )
    parser.add_argument(
        "--filtrar_uf",
        help="Filtrar por UF. Default é False.",
        default=False
    )
    parser.add_argument(
        "--codigo_municipio",
        help="Código do município para filtrar.",
        default=None
    )
    parser.add_argument(
        "--codigo_uf",
        help="Código da UF para filtrar.",
        default=None
    )

    args = parser.parse_args()

    criar_dataframe(
        args.path,
        args.filtrar_municipio,
        args.filtrar_uf,
        args.codigo_municipio,
        args.codigo_uf
    )