import pandas as pd
import argparse
import re

def limpar_cnpj(cnpj):
    return re.sub(r'\D', '', cnpj)

def buscar_cnae(
    path_to_df: str,
    path_to_cnpj: str
):
    df = pd.read_csv(path_to_df, dtype=str)
    cnpj_df = pd.read_csv(path_to_cnpj, dtype=str)
    cnpj_df["cnpj_limpo"] = cnpj_df["cnpj"].apply(limpar_cnpj)

    df["cnpj_limpo"] = df["cnpj_basico"] + df["cnpj_ordem"] + df["cnpj_dv"]

    df = df[df["cnpj_limpo"].isin(cnpj_df["cnpj_limpo"])]

    df = pd.merge(df, cnpj_df, left_on="cnpj_limpo", right_on="cnpj_limpo", how="inner")

    colunas = [
        "cnpj",
        "cnae_fiscal",
        "cnae_fiscal_secundaria",
    ]

    df = df[colunas]

    df.to_csv("resultado.csv", index=False)

if __name__ == "__main__":
    """
    O objetivo deste script é buscar, a partir do .csv gerado pelo arquivo criar_dataframe.py, os CNAE
    dos CNPJs providos pelo usuário num segundo arquivo .csv. O resultado é salvo em um arquivo .csv chamado
    resultado.csv.

    Exemplo de uso:
    python3 buscar_cnaes.py --file1 df.csv --file2 cnpj.csv
    """

    parser = argparse.ArgumentParser(description=" ")
    parser.add_argument(
        "--file1",
        help="Local do arquivo .csv gerado pelo criar_dataframe.py"
    )
    parser.add_argument(
        "--file2",
        help="Local do arquivo .csv com os CNPJs.",
    )

    args = parser.parse_args()
    buscar_cnae(args.file1, args.file2)