import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.integrate import trapezoid
from scipy.stats import norm

if getattr(sys, 'frozen', False):
    DIRETORIO_RAIZ = Path(sys.executable).resolve().parent
else:
    DIRETORIO_RAIZ = Path(__file__).resolve().parent.parent

PASTA_TERCEIRA_ETAPA = DIRETORIO_RAIZ / "terceira-etapa"
PASTA_DATA = DIRETORIO_RAIZ / "data"
PASTA_ETAPA3 = DIRETORIO_RAIZ / "reports" / "etapa_3"
PASTA_KDE = PASTA_ETAPA3 / "densidades_kde"

PASTA_DATA.mkdir(parents=True, exist_ok=True)
PASTA_ETAPA3.mkdir(parents=True, exist_ok=True)
PASTA_KDE.mkdir(parents=True, exist_ok=True)

ARQUIVO_ENTRADA_NORM = PASTA_DATA / "nir_benchtop_data_norm.csv"
ARQUIVO_SAIDA_REDUZIDO = PASTA_DATA / "nir_benchtop_data_bayes.csv"
ARQUIVO_JSON_ATRIBUTOS = PASTA_TERCEIRA_ETAPA / "atributos_selecionados.json"
ARQUIVO_EXCEL_BAYES = PASTA_ETAPA3 / "selecao_bayes_etapa3.xlsx"
ARQUIVO_GRID_KDE = PASTA_ETAPA3 / "densidades_kde_todos_bins.png"


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


def modelar_bayes_atributos(
    df: pd.DataFrame,
    colunas_bins: List[str],
    classes: List[str],
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Dict[str, Any]]]:
    
    n_amostras = len(df)
    n_classes = len(classes)
    priors = {classe: float(np.mean(df["Fibra"] == classe)) for classe in classes}

    parametros_lista: List[Dict[str, Any]] = []
    metricas_lista: List[Dict[str, Any]] = []
    bayes_modelos: Dict[str, Dict[str, Any]] = {}

    for col in colunas_bins:
        dados_col = df[col].values
        medias: Dict[str, float] = {}
        desvios: Dict[str, float] = {}

        for classe in classes:
            subset = df.loc[df["Fibra"] == classe, col].values
            media = float(np.mean(subset))
            desvio = float(np.std(subset, ddof=1)) if len(subset) > 1 else 1e-4
            desvio = max(desvio, 1e-4)

            medias[classe] = media
            desvios[classe] = desvio

            parametros_lista.append(
                {
                    "Atributo": col,
                    "Classe": classe,
                    "Media": media,
                    "Desvio_Padrao": desvio,
                    "Prior_P(C)": priors[classe],
                }
            )

        verossimilhanca = np.zeros((n_amostras, n_classes))
        for k, classe in enumerate(classes):
            verossimilhanca[:, k] = (
                norm.pdf(dados_col, loc=medias[classe], scale=desvios[classe])
                * priors[classe]
            )

        soma_posteriori = np.sum(verossimilhanca, axis=1, keepdims=True)
        posteriors = np.where(
            soma_posteriori > 0,
            verossimilhanca / soma_posteriori,
            1.0 / n_classes,
        )

        pred_indices = np.argmax(posteriors, axis=1)
        classes_preditas = [classes[idx] for idx in pred_indices]
        acuracia_bayes = float(np.mean(classes_preditas == df["Fibra"].values))

        certeza_media = float(np.mean(np.max(posteriors, axis=1)))

        entropia = -float(
            np.mean(np.sum(posteriors * np.log(posteriors + 1e-12), axis=1))
        )

        sobreposicoes = []
        for i in range(n_classes):
            for j in range(i + 1, n_classes):
                c1, c2 = classes[i], classes[j]
                m1, s1 = medias[c1], desvios[c1]
                m2, s2 = medias[c2], desvios[c2]

                g_min = min(m1 - 4 * s1, m2 - 4 * s2)
                g_max = max(m1 + 4 * s1, m2 + 4 * s2)
                grid = np.linspace(g_min, g_max, 1000)

                pdf1 = norm.pdf(grid, m1, s1)
                pdf2 = norm.pdf(grid, m2, s2)
                ovl = trapezoid(np.minimum(pdf1, pdf2), grid)
                sobreposicoes.append(float(np.clip(ovl, 0.0, 1.0)))

        sobreposicao_media = float(np.mean(sobreposicoes)) if sobreposicoes else 0.0

        bayes_modelos[col] = {
            "medias": medias,
            "desvios": desvios,
            "priors": priors,
            "acuracia_bayes": acuracia_bayes,
            "certeza_media": certeza_media,
            "entropia": entropia,
            "sobreposicao_media": sobreposicao_media,
        }

        metricas_lista.append(
            {
                "Atributo": col,
                "Acuracia_Bayes": acuracia_bayes,
                "Certeza_Media": certeza_media,
                "Entropia_Posterior": entropia,
                "Sobreposicao_Media": sobreposicao_media,
            }
        )

    df_metricas = pd.DataFrame(metricas_lista)
    df_parametros = pd.DataFrame(parametros_lista)

    return df_metricas, df_parametros, bayes_modelos


def selecionar_atributos(
    df_metricas: pd.DataFrame,
    limiar_sobreposicao: float = 0.15,
    limiar_acuracia: float = 0.75,
) -> Tuple[List[str], List[str], pd.DataFrame]:

    df_selecao = df_metricas.copy()
    status_lista: List[str] = []

    for _, row in df_selecao.iterrows():
        acc = row["Acuracia_Bayes"]
        ovl = row["Sobreposicao_Media"]

        retido = (ovl <= limiar_sobreposicao) and (acc >= limiar_acuracia)
        status_lista.append("Retido" if retido else "Descartado")

    df_selecao["Status"] = status_lista

    df_selecao = df_selecao.sort_values("Acuracia_Bayes", ascending=False).reset_index(
        drop=True
    )

    atributos_selecionados = df_selecao.loc[
        df_selecao["Status"] == "Retido", "Atributo"
    ].tolist()
    colunas_originais = [c for c in df_metricas["Atributo"] if c in atributos_selecionados]
    atributos_descartados = [
        c for c in df_metricas["Atributo"] if c not in colunas_originais
    ]

    return colunas_originais, atributos_descartados, df_selecao


def gerar_graficos_kde(
    df: pd.DataFrame,
    colunas_bins: List[str],
    classes: List[str],
    df_selecao: pd.DataFrame,
) -> None:
    
    dict_status = dict(zip(df_selecao["Atributo"], df_selecao["Status"]))
    dict_acc = dict(zip(df_selecao["Atributo"], df_selecao["Acuracia_Bayes"]))
    dict_ovl = dict(zip(df_selecao["Atributo"], df_selecao["Sobreposicao_Media"]))

    cores_classes = sns.color_palette("tab10", len(classes))
    mapa_cores = dict(zip(classes, cores_classes))

    print(f"{len(colunas_bins)} gráficos individuais de densidade KDE em: {PASTA_KDE}")
    for col in colunas_bins:
        status = dict_status[col]
        acc = dict_acc[col]
        ovl = dict_ovl[col]

        plt.figure(figsize=(9, 5.5))
        for classe in classes:
            dados_classe = df.loc[df["Fibra"] == classe, col]
            sns.kdeplot(
                dados_classe,
                label=classe,
                color=mapa_cores[classe],
                common_norm=False,
                fill=True,
                alpha=0.25,
                linewidth=2,
            )

        cor_titulo = "forestgreen" if status == "Retido" else "firebrick"
        plt.title(
            f"Densidade Espectral: {col} [{status.upper()}]\n"
            f"Acurácia Bayesiana: {acc:.1%} | Sobreposição Média: {ovl:.1%}",
            fontsize=13,
            fontweight="bold",
            color=cor_titulo,
        )
        plt.xlabel(f"Intensidade Normalizada ({col})", fontsize=11)
        plt.ylabel("Densidade de Probabilidade P(X | C)", fontsize=11)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend(title="Fibra", loc="upper right", framealpha=0.9)
        plt.tight_layout()

        caminho_individual = PASTA_KDE / f"kde_{col}.png"
        plt.savefig(caminho_individual, dpi=200)
        plt.close()

    print(f"Gerando painel consolidado em grade (4x4) em: {ARQUIVO_GRID_KDE}")
    fig, axes = plt.subplots(4, 4, figsize=(20, 16))
    axes = axes.flatten()

    for idx, col in enumerate(colunas_bins):
        ax = axes[idx]
        status = dict_status[col]
        acc = dict_acc[col]
        ovl = dict_ovl[col]

        for classe in classes:
            dados_classe = df.loc[df["Fibra"] == classe, col]
            sns.kdeplot(
                dados_classe,
                ax=ax,
                color=mapa_cores[classe],
                common_norm=False,
                fill=True,
                alpha=0.2,
                linewidth=1.5,
            )

        cor_box = "forestgreen" if status == "Retido" else "gray"
        ax.set_title(
            f"{col} ({status}) | Acc: {acc:.0%} | OVL: {ovl:.0%}",
            fontsize=10,
            fontweight="bold",
            color=cor_box,
        )
        ax.set_xlabel("Valor Normalizado", fontsize=8)
        ax.set_ylabel("Densidade", fontsize=8)
        ax.tick_params(labelsize=8)
        ax.grid(True, linestyle=":", alpha=0.4)

    handles = [
        plt.Line2D(
            [0],
            [0],
            color=mapa_cores[c],
            lw=3,
            label=c,
        )
        for c in classes
    ]
    fig.legend(
        handles=handles,
        loc="upper center",
        ncol=len(classes),
        fontsize=11,
        bbox_to_anchor=(0.5, 0.995),
    )
    fig.suptitle(
        "Distribuições de Densidade de Probabilidade por Classe",
        fontsize=16,
        fontweight="bold",
        y=1.015,
    )
    plt.tight_layout()
    plt.savefig(ARQUIVO_GRID_KDE, dpi=250, bbox_inches="tight")
    plt.close()


def salvar_relatorio_bayes(
    df: pd.DataFrame,
    df_selecao: pd.DataFrame,
    df_parametros: pd.DataFrame,
    atributos_sel: List[str],
    atributos_desc: List[str],
) -> None:
    
    print(f"\nSalvando relatório de seleção por Bayes em: {ARQUIVO_EXCEL_BAYES}")
    with pd.ExcelWriter(ARQUIVO_EXCEL_BAYES, engine="openpyxl") as escritor:
        df_selecao.to_excel(escritor, sheet_name="Selecao_Atributos_Bayes", index=False)
        df_parametros.to_excel(escritor, sheet_name="Parametros_Gaussianos", index=False)

    dados_json = {
        "atributos_selecionados": atributos_sel,
        "atributos_descartados": atributos_desc,
        "total_atributos_originais": len(atributos_sel) + len(atributos_desc),
        "total_atributos_selecionados": len(atributos_sel),
    }

    with open(ARQUIVO_JSON_ATRIBUTOS, "w", encoding="utf-8") as f:
        json.dump(dados_json, f, indent=4, ensure_ascii=False)
    print(f"Atributos selecionados salvos em JSON: {ARQUIVO_JSON_ATRIBUTOS}")

    df_reduzido = df[atributos_sel + ["Fibra"]]
    df_reduzido.to_csv(ARQUIVO_SAIDA_REDUZIDO, index=False)
    print(f"Base reduzida com atributos selecionados salva em: {ARQUIVO_SAIDA_REDUZIDO}")


def executar() -> None:

    df, _, _, colunas_bins, classes = carregar_dados(ARQUIVO_ENTRADA_NORM)

    df_metricas, df_parametros, bayes_modelos = modelar_bayes_atributos(
        df, colunas_bins, classes
    )

    atributos_sel, atributos_desc, df_selecao = selecionar_atributos(
        df_metricas, limiar_sobreposicao=0.15, limiar_acuracia=0.75
    )

    gerar_graficos_kde(df, colunas_bins, classes, df_selecao)

    salvar_relatorio_bayes(df, df_selecao, df_parametros, atributos_sel, atributos_desc)


if __name__ == "__main__":
    executar()
