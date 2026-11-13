# Reconhecimento de Padrões e Agrupamento Espectral (NIR)

> **Disciplina:** Tópicos Especiais em IA   
> **Instituição:** Universidade Federal Rural do Rio de Janeiro (UFRRJ) — Departamento de Computação / ICE  
> **Docente:** Profa. Gizelle Kupac Vianna  

---

## 1. Visão Geral do Projeto

Este repositório compreende um estudo experimental de **Reconhecimento de Padrões e Aprendizado Não-Supervisionado** aplicado a dados de espectroscopia no infravermelho próximo (*Near-Infrared Spectroscopy* — NIR). O objetivo central do sistema é discriminar e agrupar diferentes tipos de fibras têxteis puras a partir de suas assinaturas de absorção óptica, avaliando o impacto do pré-processamento, a qualidade da separabilidade do espaço de atributos e a eficiência da redução de dimensionalidade orientada por princípios probabilísticos.

O projeto investiga como métricas multivariadas clássicas e a modelagem bayesiana auxiliam na identificação de bandas espectrais informativas, mitigando ruídos e redundâncias inerentes a dados espectrais contínuos de alta dimensão.

---

## 2. Níveis de Abordagem Metodológica

O estudo é estruturado em três níveis analíticos complementares em ordem de complexidade conceitual:

### Nível 1: Pré-Processamento, Higienização e Estatística Multivariada
Focado na transformação dos dados espectrais brutos em uma representação tabular estruturada e regularizada.
- **Agrupamento Espectral (*Spectral Binning*):** Integração das curvas contínuas de absorbância óptica ($4000\text{ cm}^{-1}$ a $8000\text{ cm}^{-1}$) em 16 bandas espectrais discretizadas (`Bin_01` a `Bin_16`).
- **Normalização e Tratamento de Dispersão:** Aplicação de escalonamento min-max ($[0, 1]$), essencial para assegurar que distâncias geométricas em algoritmos baseados em espaço euclidiano reflitam a densidade das bandas de absorção de maneira equilibrada.
- **Análise Estatística de 1ª e 2ª Ordem:** Quantificação das tendências centrais e dispersões (médias globais e estratificadas por classe, desvios e variâncias) e análise das dependências lineares por meio das matrizes de covariância e correlação de Pearson.

### Nível 2: Quantificação de Separabilidade e Agrupamento Inicial
Dedica-se a medir a discriminabilidade geométrica intrínseca dos dados e a avaliar a capacidade de agrupamento não-supervisionado no espaço dimensional completo (16 atributos).
- **Métricas de Representação e Espalhamento:**
  - *Critério das Distâncias entre Centros de Massa (SDCM):* Avaliação da dispersão inter-classes ponderada pelas variâncias internas de cada grupo.
  - *Discriminante Multidimensional de Fisher:* Quantificação da razão entre a matriz de espalhamento inter-classes ($S_B$) e a matriz de espalhamento intra-classes ($S_W$), medindo o potencial discriminativo do hiperespaço.
- **Agrupamento com K-Means (Espaço Completo):** Execução do algoritmo de particionamento considerando $K$ igual ao número real de classes do gabarito têxtil, mapeamento de correspondência cluster-classe e diagnóstico de sobreposição geométrica entre materiais.

### Nível 3: Seleção de Características por Bayes e Agrupamento Reduzido
Aplica a teoria da decisão bayesiana para identificar as dimensões que maximizam a certeza na atribuição de classes, reavaliando o desempenho de agrupamento.
- **Modelagem de Densidade Condicional (*KDE* / Bayes):** Estimativa contínua das probabilidades condicionais $P(X_j \mid C_k)$ e avaliação da probabilidade *a posteriori* $P(C_k \mid X_j)$ por banda espectral. Atributos com sobreposição acentuada de densidades são filtrados, preservando aqueles com picos e vales discriminantes.
- **Reavaliação Comparativa:** Reexecução do K-Means no espaço reduzido de atributos selecionados, confrontando a qualidade da convergência e a acurácia dos agrupamentos frente aos resultados obtidos no Nível 2 e ao gabarito real das amostras.

---

## 3. Estrutura de Pastas e Arquivos

A organização do repositório reflete a segregação entre dados originais, transformações intermediárias, código-fonte modular e relatórios/evidências geradas:

```
topicos-ia-seg/
│
├── nir-sort/                        # Base bruta original de espectroscopia NIR
│   ├── DataDictionary.csv           # Dicionário original do repositório NIR-SORT
│   ├── DataFramework.txt            # Documentação e protocolo de amostragem
│   └── DataGrabs/                   # Leituras espectrais individuais por amostra (.CSV)
│
├── data/                            # Conjuntos de dados gerados e consolidados
│   ├── nir_benchtop_data.csv        # Base tabular pós-binning com 16 atributos espectrais
│   ├── nir_benchtop_data_norm.csv   # Base normalizada no intervalo [0, 1]
│   └── nir_benchtop_data_bayes.csv  # Base reduzida contendo apenas atributos selecionados
│
├── primeira-etapa/                  # Módulos do Nível 1: Estatística e Pré-processamento
│   └── primeira_etapa.py            # Rotinas de estatísticas de 1ª/2ª ordem, covariância e correlação
│
├── segunda-etapa/                   # Módulos do Nível 2: Separabilidade e Agrupamento Global
│   └── segunda_etapa.py             # Implementação de Fisher, SDCM e K-Means completo
│
├── terceira-etapa/                  # Módulos do Nível 3: Seleção Bayesiana e Agrupamento Reduzido
│   ├── teorema-bayes.py             # Estimativa de densidades (KDE), análise a posteriori e seleção
│   ├── kmeans-reduzido.py           # Agrupamento K-Means com o subconjunto selecionado
│   └── atributos_selecionados.json  # Relação serializada dos bins preservados
│
├── reports/                         # Relatórios consolidados, gráficos e tabelas exportadas
│   ├── etapa_1/                     # Gráficos de correlação, boxplots e estatísticas tabulares (.xlsx)
│   ├── etapa_2/                     # Matrizes de confusão, dispersões e métricas de Fisher/SDCM (.xlsx)
│   └── etapa_3/                     # Curvas de densidade KDE por bin, matrizes e comparação (.xlsx)
│
├── preprocessamento_nir.py          # Script de extração e estruturação da base a partir de nir-sort/
├── requirements.txt                 # Dependências Python dos scripts do projeto
├── Dicionario_de_Dados.md           # Detalhamento semântico dos bins espectrais e das classes têxteis
└── README.MD                        # Visão geral do projeto e documentação arquitetural
```

---

## 4. Tecnologias e Fundamentação

- **Linguagem & Bibliotecas:** Python 3, NumPy, Pandas, SciPy, Scikit-Learn, Matplotlib, Seaborn, OpenPyXL.
- **Domínio de Aplicação:** Espectroscopia de Refletância Difusa no Infravermelho Próximo (NIR) para triagem automatizada e reciclagem têxtil circular.

## 5. Execução pelo terminal

Instale as dependências do projeto:

```bash
python -m pip install -r requirements.txt
```

Inicie a interface interativa:

```bash
python executar_sistema.py
```

O menu permite executar o fluxo completo, na ordem pré-processamento,
primeira etapa, segunda etapa, seleção Bayes e K-Means reduzido, ou executar
uma etapa individual. As etapas usam os parâmetros e os arquivos de saída
padrão já definidos no projeto.

## 6. Geração do executável

Com o ambiente virtual e as dependências instalados, gere o executável com:

```bash
python -m PyInstaller --clean executar_sistema.spec
```

O arquivo será gerado em `dist/executar_sistema.exe`. Mantenha as pastas
`nir-sort/` e `data/` no mesmo diretório do executável, pois os dados de
entrada e os relatórios são lidos e gravados externamente ao bundle.
