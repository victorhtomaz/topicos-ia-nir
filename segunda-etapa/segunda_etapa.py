from pathlib import Path
import sys
from typing import Any, Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from scipy.optimize import linear_sum_assignment

if getattr(sys, 'frozen', False):
    DIRETORIO_RAIZ = Path(sys.executable).resolve().parent
else:
    DIRETORIO_RAIZ = Path(__file__).resolve().parent.parent

PASTA_DATA = DIRETORIO_RAIZ / "data"
PASTA_ETAPA2 = DIRETORIO_RAIZ / "reports" / "etapa_2"

PASTA_DATA.mkdir(parents=True, exist_ok=True)
PASTA_ETAPA2.mkdir(parents=True, exist_ok=True)

ARQUIVO_ENTRADA_NORM = PASTA_DATA / "nir_benchtop_data_norm.csv"
ARQUIVO_EXCEL = PASTA_ETAPA2 / "criterios_representacao_etapa2.xlsx"
ARQUIVO_HEATMAP_DIST = PASTA_ETAPA2 / "matriz_distancias_centroides.png"
ARQUIVO_HEATMAP_POND = PASTA_ETAPA2 / "matriz_distancias_ponderadas.png"
ARQUIVO_BARRAS_DISP = PASTA_ETAPA2 / "dispersao_intraclasse.png"


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
        raise ValueError(f"Coluna alvo '{coluna_alvo}' não encontrada no arquivo {caminho_arquivo}.")

    if not colunas_bins:
        raise ValueError("Nenhuma coluna de atributo espectral (iniciando com 'Bin_') foi localizada.")

    X = df[colunas_bins].values
    y = df[coluna_alvo].values
    classes = sorted(list(np.unique(y)))

    return df, X, y, colunas_bins, classes

def calcular_sdcm(X: np.ndarray, y: np.ndarray, classes: List[str]) -> Dict[str, Any]:
    c = len(classes)
    grupos = {classe: X[y == classe] for classe in classes}
 
    centroides = {}
    dispersoes = {}
    for classe in classes:
        Xc = grupos[classe]
        cm = np.mean(Xc, axis=0)
        centroides[classe] = cm
        dists = cdist(cm.reshape(1, -1), Xc, metric="euclidean")[0]
        dispersoes[classe] = np.mean(dists)
 
    matriz_centroides = np.vstack([centroides[cl] for cl in classes])
    D = cdist(matriz_centroides, matriz_centroides, metric="euclidean")
 
    SDCM = 0.0
    pares = []
    for i in range(c):
        for j in range(i + 1, c):
            d_ij = D[i, j]
            disp_soma = dispersoes[classes[i]] + dispersoes[classes[j]]
            d_pond = d_ij / disp_soma if disp_soma > 0 else 0.0
            SDCM += d_pond
            pares.append({
                "Classe_1": classes[i], "Classe_2": classes[j],
                "Dist_Centroides": d_ij,
                "Disp_1": dispersoes[classes[i]], "Disp_2": dispersoes[classes[j]],
                "Dist_Ponderada": d_pond,
            })
 
    return {
        "classes": classes,
        "centroides": centroides,
        "dispersoes": dispersoes,
        "matriz_distancias_centroides": D,
        "pares": pares,
        "SDCM": SDCM,
    }

def discriminante_fisher(X: np.ndarray, y: np.ndarray, classes: List[str]) -> Dict[str, Any]:
    m = np.mean(X, axis=0)
    n_atributos = X.shape[1]
 
    SW = np.zeros((n_atributos, n_atributos))
    SB = np.zeros((n_atributos, n_atributos))
 
    for classe in classes:
        Xc = X[y == classe]
        mc = np.mean(Xc, axis=0)
        n_c = Xc.shape[0]
 
        diffs = Xc - mc
        SW += diffs.T @ diffs
 
        diff_m = (mc - m).reshape(-1, 1)
        SB += n_c * (diff_m @ diff_m.T)
 
    try:
        det_SW = np.linalg.det(SW)
        det_SB = np.linalg.det(SB)
        J_det = det_SB / det_SW if det_SW != 0 else np.nan
    except np.linalg.LinAlgError:
        J_det = np.nan
 
    # J via traço(SW^-1 @ SB) - usa pseudo-inversa para maior estabilidade
    SW_inv = np.linalg.pinv(SW)
    J_trace = np.trace(SW_inv @ SB)
 
    return {
        "classes": classes,
        "SW": SW,
        "SB": SB,
        "J_det": J_det,
        "J_trace": J_trace,
    }

def gerar_relatorio_separabilidade(
    X: np.ndarray,
    y: np.ndarray,
    colunas_bins: List[str],
    classes: List[str],
) -> Tuple[float, float]:
    if len(classes) < 2:
        raise ValueError("A base precisa conter pelo menos duas classes para avaliar separabilidade.")

    resultado_distancias = calcular_sdcm(X, y, classes)
    resultado_fisher = discriminante_fisher(X, y, classes)

    # A nota de Fisher usada no relatório é o critério de traço:
    # quanto maior a dispersão entre classes em relação à intraclasse, melhor.
    nota_fisher = resultado_fisher["J_trace"]
    nota_distancias = resultado_distancias["SDCM"]

    resumo = pd.DataFrame(
        [
            {
                "Criterio": "Discriminante de Fisher",
                "Nota": nota_fisher,
            },
            {
                "Criterio": "Criterio das Distancias (SDCM)",
                "Nota": nota_distancias,
            },
        ]
    )

    centroides = pd.DataFrame.from_dict(
        resultado_distancias["centroides"], orient="index", columns=colunas_bins
    )
    centroides.index.name = "Classe"

    dispersoes = pd.DataFrame(
        [
            {"Classe": classe, "Dispersao_Intraclasse": dispersao}
            for classe, dispersao in resultado_distancias["dispersoes"].items()
        ]
    )
    pares = pd.DataFrame(resultado_distancias["pares"])
    fisher_detalhes = pd.DataFrame(
        [
            {"Medida": "J_det", "Valor": resultado_fisher["J_det"]},
            {"Medida": "J_trace", "Valor": resultado_fisher["J_trace"]},
        ]
    )

    with pd.ExcelWriter(ARQUIVO_EXCEL, engine="openpyxl") as escritor:
        resumo.to_excel(escritor, sheet_name="Resumo", index=False)
        dispersoes.to_excel(escritor, sheet_name="Dispersoes", index=False)
        pares.to_excel(escritor, sheet_name="Distancias", index=False)
        centroides.to_excel(escritor, sheet_name="Centroides")
        fisher_detalhes.to_excel(escritor, sheet_name="Fisher", index=False)
        pd.DataFrame(resultado_fisher["SW"], index=colunas_bins, columns=colunas_bins).to_excel(
            escritor, sheet_name="SW"
        )
        pd.DataFrame(resultado_fisher["SB"], index=colunas_bins, columns=colunas_bins).to_excel(
            escritor, sheet_name="SB"
        )

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        resultado_distancias["matriz_distancias_centroides"],
        xticklabels=classes,
        yticklabels=classes,
        annot=True,
        fmt=".3f",
        cmap="YlGnBu",
    )
    plt.title("Distâncias entre centroides das classes")
    plt.xlabel("Classe")
    plt.ylabel("Classe")
    plt.tight_layout()
    plt.savefig(ARQUIVO_HEATMAP_DIST, dpi=200)
    plt.close()

    matriz_ponderada = np.zeros_like(resultado_distancias["matriz_distancias_centroides"])
    for par in resultado_distancias["pares"]:
        i = classes.index(par["Classe_1"])
        j = classes.index(par["Classe_2"])
        matriz_ponderada[i, j] = matriz_ponderada[j, i] = par["Dist_Ponderada"]

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        matriz_ponderada,
        xticklabels=classes,
        yticklabels=classes,
        annot=True,
        fmt=".3f",
        cmap="YlOrRd",
    )
    plt.title("Distâncias ponderadas entre classes")
    plt.xlabel("Classe")
    plt.ylabel("Classe")
    plt.tight_layout()
    plt.savefig(ARQUIVO_HEATMAP_POND, dpi=200)
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=dispersoes, x="Classe", y="Dispersao_Intraclasse", color="steelblue")
    plt.title("Dispersão intraclasse")
    plt.xlabel("Classe")
    plt.ylabel("Distância média ao centroide")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(ARQUIVO_BARRAS_DISP, dpi=200)
    plt.close()

    print(f"Discriminante de Fisher (J_trace): {nota_fisher:.6f}")
    print(f"Critério das Distâncias (SDCM): {nota_distancias:.6f}")
    print(f"Resultados salvos em: {ARQUIVO_EXCEL}")

    return nota_fisher, nota_distancias


def executar_kmeans(
    X: np.ndarray, y: np.ndarray, classes: List[str]
) -> Dict[str, Any]:
    modelo = KMeans(n_clusters=len(classes), random_state=67, n_init=10)
    clusters = modelo.fit_predict(X)

    matriz_contingencia = pd.crosstab(
        pd.Series(y, name="Classe_Real"),
        pd.Series(clusters, name="Cluster")
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

    with pd.ExcelWriter(
        ARQUIVO_EXCEL, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as escritor:
        resumo_kmeans.to_excel(escritor, sheet_name="KMeans_Resumo", index=False)
        resultado["matriz_contingencia"].to_excel(
            escritor, sheet_name="KMeans_Contingencia"
        )
        resultado["matriz_confusao"].to_excel(escritor, sheet_name="KMeans_Confusao")
        tabela_mapeamento.to_excel(escritor, sheet_name="KMeans_Mapeamento", index=False)
        tabela_amostras.to_excel(escritor, sheet_name="KMeans_Amostras", index=False)


def executar() -> None:
    _, X, y, colunas_bins, classes = carregar_dados(ARQUIVO_ENTRADA_NORM)
    gerar_relatorio_separabilidade(X, y, colunas_bins, classes)

    resultado_kmeans = executar_kmeans(X, y, classes)
    registrar_resultado_kmeans(resultado_kmeans)
    print(f"K-means - acurácia: {resultado_kmeans['acuracia']:.6f}")
    print(
        "K-means - índice Rand ajustado: "
        f"{resultado_kmeans['indice_rand_ajustado']:.6f}"
    )
    print(f"K-means - resultados salvos em: {ARQUIVO_EXCEL}")


if __name__ == "__main__":
    executar()
