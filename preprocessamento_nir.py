import argparse
import re
from pathlib import Path
import sys
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# Dicionário de Mapeamento de Fibras
MAPEAMENTO_FIBRAS: Dict[str, str] = {
    "a": "Cotton",
    "b": "Polyester",
    "c": "Nylon",
    "d": "Polyacrylic",
    "e": "Spandex",
    "f": "Recycled Polyester",
    "g": "Rayon",
    "h": "Natural Cellulosics",
    "i": "Wool",
}

# Expressão regular para selecionar arquivos Nicolet com medida de Absorbância
# Formato: {origem}_{conteudo}_{lote}_{fator_forma}_{instrumento}_{replica_formato}.csv
PADRAO_ARQUIVO_NICOLET_ABSORBANCIA = re.compile(
    r"^[^_]+_[^_]+_[^_]+_[^_]+_N_[^_]*A\.csv$", re.IGNORECASE
)

# Expressão regular para identificar tecidos 100% monomateriais
PADRAO_FIBRA_MONOMATERIAL = re.compile(r"^([a-zA-Z])100(?:[a-zA-Z]000)*$")

if getattr(sys, 'frozen', False):
    DIRETORIO_RAIZ = Path(sys.executable).resolve().parent
else:
    DIRETORIO_RAIZ = Path(__file__).resolve().parent
PASTA_DATAGRBS = DIRETORIO_RAIZ / "nir-sort" / "DataGrabs"
ARQUIVO_SAIDA_PADRAO = DIRETORIO_RAIZ / "data" / "nir_benchtop_data.csv"

def varrer_e_filtrar_arquivos(diretorio_dados: Path) -> List[Path]:
    arquivos_encontrados: List[Path] = []

    for item in diretorio_dados.iterdir():
        if item.is_file() and PADRAO_ARQUIVO_NICOLET_ABSORBANCIA.match(item.name):
            arquivos_encontrados.append(item)

    arquivos_encontrados.sort(key=lambda p: p.name)
    return arquivos_encontrados

def extrair_classe_fibra(nome_arquivo: str) -> Optional[Tuple[str, str]]:
    partes = nome_arquivo.split("_")
    if len(partes) < 6:
        return None

    campo_fibra = partes[1]
    correspondencia_mono = PADRAO_FIBRA_MONOMATERIAL.match(campo_fibra)

    if correspondencia_mono:
        codigo_fibra = correspondencia_mono.group(1).lower()
        nome_classe = MAPEAMENTO_FIBRAS.get(codigo_fibra, f"Fibra_{codigo_fibra.upper()}")
        return codigo_fibra, nome_classe

    return None

def carregar_espectro(caminho_arquivo: Path) -> Tuple[np.ndarray, np.ndarray]:
    matriz_espectral = np.loadtxt(caminho_arquivo, delimiter=",")
    numeros_onda = matriz_espectral[:, 0]
    absorbancias = matriz_espectral[:, 1]
    return numeros_onda, absorbancias

def aplicar_spectral_binning(
    numeros_onda: np.ndarray,
    absorbancias: np.ndarray,
    limite_min: float = 4000.0,
    limite_max: float = 8000.0,
    largura_bin: float = 250.0
) -> List[float]:
    bordas = np.arange(limite_min, limite_max + largura_bin, largura_bin)
    qtd_bins = len(bordas) - 1
    medias_bins: List[float] = []

    for i in range(qtd_bins):
        inicio = bordas[i]
        fim = bordas[i + 1]

        if i == qtd_bins - 1:
            mascara = (numeros_onda >= inicio) & (numeros_onda <= fim)
        else:
            mascara = (numeros_onda >= inicio) & (numeros_onda < fim)

        pontos_bin = absorbancias[mascara]
        
        if len(pontos_bin) == 0:
            medias_bins.append(0.0)
        else:
            medias_bins.append(float(np.mean(pontos_bin)))

    vetor_bins = np.array(medias_bins)

    soma_total = np.sum(vetor_bins)
    if soma_total > 0:
        vetor_bins = vetor_bins / soma_total

    return vetor_bins.tolist()

def calcular_intervalos_fisicos_bins(
    numeros_onda: Optional[np.ndarray] = None,
    limite_min: float = 4000.0,
    limite_max: float = 8000.0,
    largura_bin: float = 250.0,
) -> List[Dict[str, float]]:
    
    bordas = np.arange(limite_min, limite_max + largura_bin, largura_bin)
    qtd_bins = len(bordas) - 1
    detalhes: List[Dict[str, float]] = []

    for i in range(qtd_bins):
        inicio = float(bordas[i])
        fim = float(bordas[i + 1])
        comp_onda_min = 1e7 / fim
        comp_onda_max = 1e7 / inicio

        qtd_pontos = 0
        if numeros_onda is not None:
            if i == 0:
                mascara = (numeros_onda >= inicio - 1.0) & (numeros_onda < fim)
            elif i == qtd_bins - 1:
                mascara = (numeros_onda >= inicio) & (numeros_onda <= fim)
            else:
                mascara = (numeros_onda >= inicio) & (numeros_onda < fim)
            qtd_pontos = int(np.sum(mascara))

        detalhes.append(
            {
                "bin": f"Bin_{i+1:02d}",
                "num_onda_inicio_cm-1": inicio,
                "num_onda_fim_cm-1": fim,
                "comp_onda_min_nm": comp_onda_min,
                "comp_onda_max_nm": comp_onda_max,
                "qtd_pontos": qtd_pontos,
            }
        )

    return detalhes

def processar_dataset_nir(
    diretorio_dados: Path,
    limite_min: float = 4000.0,
    limite_max: float = 8000.0,
    largura_bin: float = 250.0,
    nome_coluna_rotulo: str = "Fibra",
) -> Tuple[pd.DataFrame, List[Dict[str, float]]]:
    arquivos_candidatos = varrer_e_filtrar_arquivos(diretorio_dados)
    print(
        f"Varredura: {len(arquivos_candidatos)} arquivos encontrados."
    )

    linhas_tabela: List[List] = []
    amostras_validas = 0
    intervalos_referencia: Optional[List[Dict[str, float]]] = None

    num_bins = int(round((limite_max - limite_min) / largura_bin))
    nomes_colunas_bins = [f"Bin_{i:02d}" for i in range(1, num_bins + 1)]

    for arquivo in arquivos_candidatos:
        resultado_rotulo = extrair_classe_fibra(arquivo.name)
        if not resultado_rotulo:
            continue

        _codigo, nome_classe = resultado_rotulo

        numeros_onda, absorbancias = carregar_espectro(arquivo)

        if intervalos_referencia is None:
            intervalos_referencia = calcular_intervalos_fisicos_bins(
                numeros_onda=numeros_onda,
                limite_min=limite_min,
                limite_max=limite_max,
                largura_bin=largura_bin,
            )

        valores_bins = aplicar_spectral_binning(
            numeros_onda=numeros_onda,
            absorbancias=absorbancias,
            limite_min=limite_min,
            limite_max=limite_max,
            largura_bin=largura_bin,
        )

        linhas_tabela.append([nome_classe] + valores_bins)
        amostras_validas += 1

    print(
        f"{amostras_validas} amostras 100% puras selecionadas."
    )

    colunas_finais = [nome_coluna_rotulo] + nomes_colunas_bins
    dataframe_final = pd.DataFrame(linhas_tabela, columns=colunas_finais)

    return dataframe_final, intervalos_referencia or []


def salvar_dataset_consolidado(dataframe: pd.DataFrame, caminho_saida: Path) -> None:
    
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(caminho_saida, index=False, encoding="utf-8")
    print(f"Salvando dados em: '{caminho_saida}'.")
    print(
        f"Dimensões: {dataframe.shape[0]} amostras x {dataframe.shape[1]} colunas "
        f"(1 rótulo + {dataframe.shape[1] - 1} variáveis contínuas)."
    )


def exibir_resumo_estatistico(
    dataframe: pd.DataFrame,
    intervalos_bins: List[Dict[str, float]],
    nome_coluna_rotulo: str = "Fibra",
) -> None:
    print("RESUMO DO PROCESSAMENTO ESPECTRAL (NIR-SORT)")

    print("\nDistribuição das Amostras por Classe:")
    contagem_classes = dataframe[nome_coluna_rotulo].value_counts()
    for classe, contagem in contagem_classes.items():
        porcentagem = (contagem / len(dataframe)) * 100
        print(f"  - {classe:<15}: {contagem:>3} amostras ({porcentagem:>5.1f}%)")
    print(f"  Total de amostras: {len(dataframe)}")

    print("\nIntervalos Espectrais dos 16 Bins (Spectral Binning):")
    print(f"  {'Bin':<8} | {'Número de Onda (cm^-1)':<25} | {'Comprimento de Onda (nm)':<26} | {'Pontos':<6}")
    print("  " + "-" * 72)
    for info in intervalos_bins:
        faixa_wn = f"{info['num_onda_inicio_cm-1']:>7.1f} a {info['num_onda_fim_cm-1']:>7.1f}"
        faixa_wl = f"{info['comp_onda_min_nm']:>7.1f} a {info['comp_onda_max_nm']:>7.1f}"
        print(f"  {info['bin']:<8} | {faixa_wn:<25} | {faixa_wl:<26} | {info['qtd_pontos']:<6}")

def executar_fluxo_completo(
    diretorio_origem: Path = PASTA_DATAGRBS,
    arquivo_destino: Path = ARQUIVO_SAIDA_PADRAO,
    coluna_rotulo: str = "Fibra",
) -> pd.DataFrame:
    
    diretorio_dados = Path(diretorio_origem)
    caminho_csv = Path(arquivo_destino)
    print(f"Diretório de entrada: '{diretorio_dados}'")

    dataframe_consolidado, intervalos = processar_dataset_nir(
        diretorio_dados=diretorio_dados,
        limite_min=4000.0,
        limite_max=8000.0,
        largura_bin=250.0,
        nome_coluna_rotulo=coluna_rotulo,
    )

    salvar_dataset_consolidado(dataframe_consolidado, caminho_csv)

    exibir_resumo_estatistico(
        dataframe=dataframe_consolidado,
        intervalos_bins=intervalos,
        nome_coluna_rotulo=coluna_rotulo,
    )

    return dataframe_consolidado


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pré-processamento do dataset NIR-SORT."
    )
    parser.add_argument(
        "--diretorio",
        "-d",
        type=str,
        default=str(PASTA_DATAGRBS),
        help=f"Caminho para a pasta de dados (padrão: {PASTA_DATAGRBS.name}).",
    )
    parser.add_argument(
        "--saida",
        "-s",
        type=str,
        default=str(ARQUIVO_SAIDA_PADRAO),
        help=f"Caminho do arquivo CSV de saída (padrão: {ARQUIVO_SAIDA_PADRAO.name}).",
    )
    parser.add_argument(
        "--coluna-rotulo",
        "-c",
        type=str,
        default="Fibra",
        help="Nome da coluna de rótulo (padrão: Fibra).",
    )

    args = parser.parse_args()

    executar_fluxo_completo(
        diretorio_origem=Path(args.diretorio),
        arquivo_destino=Path(args.saida),
        coluna_rotulo=args.coluna_rotulo,
    )
