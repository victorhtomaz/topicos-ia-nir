import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Callable, Dict, Optional

import questionary


DIRETORIO_RAIZ = Path(__file__).resolve().parent

ETAPAS: Dict[str, tuple[str, str, str]] = {
    "Pré-processamento": (
        "preprocessamento_nir.py",
        "executar_fluxo_completo",
        "Consolida os espectros NIR em data/nir_benchtop_data.csv.",
    ),
    "Primeira etapa": (
        "primeira-etapa/primeira_etapa.py",
        "executar",
        "Gera estatísticas, gráficos e a base normalizada.",
    ),
    "Segunda etapa": (
        "segunda-etapa/segunda_etapa.py",
        "executar",
        "Calcula separabilidade e executa o K-Means completo.",
    ),
    "Seleção Bayes": (
        "terceira-etapa/teorema-bayes.py",
        "executar",
        "Seleciona atributos e gera os relatórios Bayes/KDE.",
    ),
    "K-Means reduzido": (
        "terceira-etapa/kmeans-reduzido.py",
        "executar",
        "Executa o K-Means com os atributos selecionados.",
    ),
}


def carregar_etapa(caminho_relativo: str) -> ModuleType:
    caminho = DIRETORIO_RAIZ / caminho_relativo
    nome_modulo = f"projeto_nir_{caminho.stem.replace('-', '_')}"
    especificacao = importlib.util.spec_from_file_location(nome_modulo, caminho)
    if especificacao is None or especificacao.loader is None:
        raise ImportError(f"Não foi possível carregar a etapa: {caminho}")

    modulo = importlib.util.module_from_spec(especificacao)
    especificacao.loader.exec_module(modulo)
    return modulo


def obter_funcao_etapa(nome_etapa: str) -> Callable[[], object]:
    caminho, nome_funcao, _descricao = ETAPAS[nome_etapa]
    modulo = carregar_etapa(caminho)
    funcao = getattr(modulo, nome_funcao, None)
    if not callable(funcao):
        raise AttributeError(
            f"A etapa '{nome_etapa}' não possui a função '{nome_funcao}'."
        )
    return funcao


def executar_etapa(nome_etapa: str) -> bool:
    descricao = ETAPAS[nome_etapa][2]
    print(f"\n{nome_etapa}: {descricao}")
    try:
        obter_funcao_etapa(nome_etapa)()
    except (AttributeError, FileNotFoundError, ImportError, OSError, ValueError) as erro:
        print(f"Erro na etapa '{nome_etapa}': {erro}")
        return False

    print(f"Etapa concluída: {nome_etapa}")
    return True


def executar_fluxo_completo() -> bool:
    for nome_etapa in ETAPAS:
        if not executar_etapa(nome_etapa):
            print("O fluxo foi interrompido. Corrija o erro e execute novamente.")
            return False
    return True


def selecionar_etapa() -> Optional[str]:
    return questionary.select(
        "Qual etapa deseja executar?",
        choices=[
            questionary.Choice(
                title=f"{nome} - {descricao}",
                value=nome,
            )
            for nome, (_caminho, _funcao, descricao) in ETAPAS.items()
        ],
    ).ask()


def executar_interface() -> None:
    print("Projeto NIR - fluxo de análise")
    while True:
        escolha = questionary.select(
            "Escolha uma operação:",
            choices=[
                questionary.Choice(
                    "Executar fluxo completo",
                    value="completo",
                ),
                questionary.Choice(
                    "Executar uma etapa individual",
                    value="individual",
                ),
                questionary.Choice("Sair", value="sair"),
            ],
        ).ask()

        if escolha in (None, "sair"):
            print("Até logo!")
            return

        if escolha == "completo":
            executar_fluxo_completo()
        else:
            nome_etapa = selecionar_etapa()
            if nome_etapa is not None:
                executar_etapa(nome_etapa)

        print()


if __name__ == "__main__":
    executar_interface()
