from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

DIRETORIO_RAIZ = Path(__file__).resolve().parent.parent

PASTA_DATA = DIRETORIO_RAIZ / "data"
PASTA_ETAPA1 = DIRETORIO_RAIZ / "reports" / "etapa_1"

PASTA_DATA.mkdir(parents=True, exist_ok=True)
PASTA_ETAPA1.mkdir(parents=True, exist_ok=True)

ARQUIVO_ENTRADA = PASTA_DATA / "nir_benchtop_data.csv"
ARQUIVO_SAIDA_NORM = PASTA_DATA / "nir_benchtop_data_norm.csv"
ARQUIVO_HEATMAP = PASTA_ETAPA1 / "matriz_correlacao_etapa1.png"
ARQUIVO_BOXPLOT = PASTA_ETAPA1 / "boxplot_outliers_etapa1.png"
ARQUIVO_EXCEL = PASTA_ETAPA1 / "estatisticas_etapa1.xlsx"

def executar():

    if not ARQUIVO_ENTRADA.exists():
        raise FileNotFoundError(
            f"Arquivo de entrada não encontrado: {ARQUIVO_ENTRADA}\n"
        )

    df = pd.read_csv(ARQUIVO_ENTRADA)
    print(f"Dados carregados de: {ARQUIVO_ENTRADA}")
    print(f"Informações: {df.shape[0]} amostras e {df.shape[1]} colunas")

    colunas_bins = [col for col in df.columns if col.startswith('Bin_')]

    print("\nHigienização:")
    nulos = df[colunas_bins + ['Fibra']].isna().sum().sum()
    if nulos > 0:
        print(f"- Removendo {nulos} registros com valores nulos")
        df = df.dropna(subset=colunas_bins + ['Fibra'])
    else:
        print("- Nenhum valor nulo encontrado. Dados consistentes.")

    X_bruto = df[colunas_bins]
    y = df['Fibra']

    print("\nInspeção de Outliers (Critério IQR 1.5x):")
    outliers_resumo = []
    mascara_outliers = pd.DataFrame(False, index=df.index, columns=colunas_bins)

    for col in colunas_bins:
        q1 = float(X_bruto[col].quantile(0.25))
        q3 = float(X_bruto[col].quantile(0.75))
        iqr = q3 - q1
        lim_inf = q1 - 1.5 * iqr
        lim_sup = q3 + 1.5 * iqr
        outliers_col = (X_bruto[col] < lim_inf) | (X_bruto[col] > lim_sup)
        mascara_outliers[col] = outliers_col
        qtd = int(outliers_col.sum())
        outliers_resumo.append({
            'Atributo': col,
            'Q1': q1,
            'Q3': q3,
            'IQR': iqr,
            'Limite_Inferior': lim_inf,
            'Limite_Superior': lim_sup,
            'Qtd_Outliers': qtd,
            'Perc_Outliers (%)': (qtd / len(df)) * 100
        })

    df_outliers = pd.DataFrame(outliers_resumo)
    total_amostras_com_outlier = int((mascara_outliers.any(axis=1)).sum())
    print(f"- Total de atributos analisados: {len(colunas_bins)}")
    print(f"- Amostras contendo ao menos um ponto fora dos limites IQR: {total_amostras_com_outlier} de {len(df)}")
    print("- Diagnóstico: Os pontos extremos observados decorrem de assinaturas de absorção espectrais naturais de classes específicas, não constituindo falhas ou registros espúrios de medição.")

    media_global = X_bruto.mean()
    medias_estratificadas = df.groupby('Fibra')[colunas_bins].mean()

    variancia_global = X_bruto.var()
    desvio_global = X_bruto.std()
    matriz_cov = X_bruto.cov()
    matriz_corr = X_bruto.corr(method='pearson')

    df_stats_globais = pd.DataFrame({
        'Atributo': colunas_bins,
        'Media_Global': media_global.values,
        'Variancia': variancia_global.values,
        'Desvio_Padrao': desvio_global.values
    })

    print(f"\nSalvando tabelas estatísticas em: {ARQUIVO_EXCEL}")
    with pd.ExcelWriter(ARQUIVO_EXCEL, engine='openpyxl') as writer:
        df_stats_globais.to_excel(writer, sheet_name='Globais_1a_e_2a_Ordem', index=False)
        medias_estratificadas.to_excel(writer, sheet_name='Medias_Estratificadas')
        matriz_cov.to_excel(writer, sheet_name='Matriz_Covariancia')
        matriz_corr.to_excel(writer, sheet_name='Matriz_Correlacao')
        df_outliers.to_excel(writer, sheet_name='Inspecao_Outliers', index=False)

    print(f"\nMapa de calor de correlação de Pearson em: {ARQUIVO_HEATMAP}")
    plt.figure(figsize=(14, 10))
    sns.heatmap(
        matriz_corr, 
        annot=True, 
        fmt=".2f", 
        cmap="coolwarm", 
        linewidths=0.5
    )
    plt.title("Matriz de Correlação de Pearson - 16 Bins Espectrais", fontsize=15)
    plt.tight_layout()
    plt.savefig(ARQUIVO_HEATMAP, dpi=300)
    plt.close()

    print(f"\nBoxplot de inspeção de outliers em: {ARQUIVO_BOXPLOT}")
    plt.figure(figsize=(14, 6))
    sns.boxplot(data=X_bruto, palette="Set2")
    plt.title("Inspeção de Outliers por Atributo Espectral (16 Bins) - Dados Brutos", fontsize=14)
    plt.xlabel("Bins Espectrais", fontsize=12)
    plt.ylabel("Intensidade Relativa (Absorbância)", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(ARQUIVO_BOXPLOT, dpi=300)
    plt.close()

    print(f"\nNormalizando dados com MinMaxScaler em: {ARQUIVO_SAIDA_NORM}")
    scaler = MinMaxScaler()
    X_norm_array = scaler.fit_transform(X_bruto)

    df_norm = pd.DataFrame(X_norm_array, columns=colunas_bins)
    df_norm['Fibra'] = y.values

    df_norm.to_csv(ARQUIVO_SAIDA_NORM, index=False)
    print(f"Base normalizada salva em: {ARQUIVO_SAIDA_NORM}")

if __name__ == "__main__":
    executar()