import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

# Padrão de diretórios e caminhos utilizado no projeto
DIRETORIO_RAIZ = Path(__file__).resolve().parent.parent

PASTA_TERCEIRA_ETAPA = Path(__file__).resolve().parent
PASTA_DATA = DIRETORIO_RAIZ / "data"
PASTA_ETAPA3 = DIRETORIO_RAIZ / "reports" / "etapa_3"

PASTA_DATA.mkdir(parents=True, exist_ok=True)
PASTA_ETAPA3.mkdir(parents=True, exist_ok=True)

ARQUIVO_ENTRADA_NORM = PASTA_DATA / "nir_benchtop_data_norm.csv"
ARQUIVO_JSON_ATRIBUTOS = PASTA_TERCEIRA_ETAPA / "atributos_selecionados.json"
ARQUIVO_EXCEL = PASTA_ETAPA3 / "kmeans_reduzido_etapa3.xlsx"

DESCRITORES_BAYES_PADRAO = [
    "Bin_05",
    "Bin_07",
    "Bin_08",
    "Bin_09",
    "Bin_10",
    "Bin_11",
    "Bin_12",
]


def carregar_dados(
    caminho_arquivo: Path,
) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray, List[str], List[str]]:
    if not caminho_arquivo.exists():
        raise FileNotFoundError(
            f"Arquivo normalizado de entrada não encontrado: {caminho_arquivo}\n"
        )

    df = pd.read_csv(caminho_arquivo)
    colunas_bins = [col for col in df.columns if col.startswith("Bin_")]
    coluna_alvo = "Fibra"

    if coluna_alvo not in df.columns:
        raise ValueError(
            f"Coluna alvo '{coluna_alvo}' não encontrada no arquivo {caminho_arquivo}."
        )

    if not colunas_bins:
        raise ValueError(
            "Nenhuma coluna de atributo espectral (iniciando com 'Bin_') foi localizada."
        )

    X = df[colunas_bins].values
    y = df[coluna_alvo].values
    classes = sorted(list(np.unique(y)))

    return df, X, y, colunas_bins, classes


def obter_atributos_selecionados() -> List[str]:
    if ARQUIVO_JSON_ATRIBUTOS.exists():
        with open(ARQUIVO_JSON_ATRIBUTOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados.get("atributos_selecionados", DESCRITORES_BAYES_PADRAO)

    return DESCRITORES_BAYES_PADRAO


def executar_kmeans(
    X: np.ndarray, y: np.ndarray, classes: List[str]
) -> Dict[str, Any]:
    modelo = KMeans(n_clusters=len(classes), random_state=67, n_init=10)
    clusters = modelo.fit_predict(X)

    matriz_contingencia = pd.crosstab(
        pd.Series(y, name="Classe_Real"),
        pd.Series(clusters, name="Cluster"),
    ).reindex(columns=range(len(classes)), fill_value=0)

    row_ind, col_ind = linear_sum_assignment(matriz_contingencia.values, maximize=True)

    mapeamento = {}
    for r, c in zip(row_ind, col_ind):
        classe_real = matriz_contingencia.index[r]
        cluster_id = matriz_contingencia.columns[c]
        mapeamento[int(cluster_id)] = classe_real

    classes_preditas = np.array([mapeamento[int(cluster)] for cluster in clusters])

    matriz_confusao = pd.crosstab(
        pd.Series(y, name="Classe_Real"),
        pd.Series(classes_preditas, name="Classe_Predita"),
    ).reindex(index=classes, columns=classes, fill_value=0)

    acuracia = float(np.mean(classes_preditas == y))
    indice_rand_ajustado = float(adjusted_rand_score(y, clusters))

    return {
        "modelo": modelo,
        "clusters": clusters,
        "classes_reais": y,
        "matriz_contingencia": matriz_contingencia,
        "mapeamento": mapeamento,
        "classes_preditas": classes_preditas,
        "matriz_confusao": matriz_confusao,
        "acuracia": acuracia,
        "indice_rand_ajustado": indice_rand_ajustado,
    }


def registrar_resultado_kmeans(resultado: Dict[str, Any]) -> None:
    tabela_amostras = pd.DataFrame(
        {
            "Cluster": resultado["clusters"],
            "Classe_Real": resultado["classes_reais"],
            "Classe_Predita": resultado["classes_preditas"],
        }
    )
    tabela_mapeamento = pd.DataFrame(
        [
            {"Cluster": cluster, "Classe_Mapeada": classe}
            for cluster, classe in resultado["mapeamento"].items()
        ]
    )
    resumo_kmeans = pd.DataFrame(
        [
            {"Medida": "Acuracia", "Valor": resultado["acuracia"]},
            {
                "Medida": "Indice_Rand_Ajustado",
                "Valor": resultado["indice_rand_ajustado"],
            },
            {"Medida": "Inercia", "Valor": resultado["modelo"].inertia_},
        ]
    )

    with pd.ExcelWriter(ARQUIVO_EXCEL, engine="openpyxl") as escritor:
        resumo_kmeans.to_excel(escritor, sheet_name="KMeans_Resumo", index=False)
        resultado["matriz_contingencia"].to_excel(
            escritor, sheet_name="KMeans_Contingencia"
        )
        resultado["matriz_confusao"].to_excel(escritor, sheet_name="KMeans_Confusao")
        tabela_mapeamento.to_excel(escritor, sheet_name="KMeans_Mapeamento", index=False)
        tabela_amostras.to_excel(escritor, sheet_name="KMeans_Amostras", index=False)


def executar() -> None:
    df, _, y, _, classes = carregar_dados(ARQUIVO_ENTRADA_NORM)
    atributos_sel = obter_atributos_selecionados()
    X_reduzido = df[atributos_sel].values

    resultado_kmeans = executar_kmeans(X_reduzido, y, classes)
    registrar_resultado_kmeans(resultado_kmeans)

    print(f"K-means - acurácia: {resultado_kmeans['acuracia']:.6f}")
    print(
        "K-means - índice Rand ajustado: "
        f"{resultado_kmeans['indice_rand_ajustado']:.6f}"
    )
    print(f"K-means - resultados salvos em: {ARQUIVO_EXCEL}")


if __name__ == "__main__":
    executar()
