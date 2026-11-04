import numpy as np
import pandas as pd

from .operadores import OPERADORES


def executar_consulta_conjuntiva(df: pd.DataFrame, requisitos: dict) -> pd.DataFrame:
    """Retorna os itens que satisfazem todos os requisitos (slide 9)."""
    mascaras = []
    for configuracao in requisitos.values():
        comparar = OPERADORES[configuracao["op"]]
        mascaras.append(comparar(df[configuracao["attr"]], configuracao["val"]))

    mascara_conjuntiva = np.logical_and.reduce(mascaras)
    return df[mascara_conjuntiva]


def diagnosticar_e_gerar_reparos(
    df: pd.DataFrame, requisitos: dict, formatadores: dict = None
) -> pd.DataFrame:
    """Mostra os conjuntos mínimos de requisitos violados por cada item.

    Um diagnóstico é mínimo quando nenhum outro item viola um subconjunto
    estrito dos seus requisitos. A tabela mostra os valores a reparar.
    """
    formatadores = formatadores or {}
    candidatos = []

    for item_id, item in df.iterrows():
        violacoes = []
        for requisito_id, configuracao in requisitos.items():
            comparar = OPERADORES[configuracao["op"]]
            if not comparar(item[configuracao["attr"]], configuracao["val"]):
                violacoes.append(requisito_id)
        candidatos.append(
            {"id": item_id, "violacoes": set(violacoes), "lista_violacoes": violacoes}
        )

    # Descarta diagnósticos que contêm outro conjunto de violações.
    conjuntos_violacoes = [candidato["violacoes"] for candidato in candidatos]
    diagnosticos_minimos = [
        candidato
        for candidato in candidatos
        if not any(outro < candidato["violacoes"] for outro in conjuntos_violacoes)
    ]

    # Primeiro os conjuntos menores; em caso de empate, a ordem dos requisitos.
    ordem_requisitos = list(requisitos.keys())
    diagnosticos_minimos.sort(
        key=lambda candidato: (
            len(candidato["lista_violacoes"]),
            [ordem_requisitos.index(r) for r in candidato["lista_violacoes"]],
        )
    )

    reparos = []
    for numero, candidato in enumerate(diagnosticos_minimos, start=1):
        item_id = candidato["id"]
        diagnostico = "{" + ", ".join(candidato["lista_violacoes"]) + "}"
        linha = {
            "Repair": f"Rep{numero} (repair d{numero}={diagnostico})",
            "Item": item_id,
        }

        for requisito_id, configuracao in requisitos.items():
            atributo = configuracao["attr"]
            nome_coluna = configuracao.get("label", atributo)
            if requisito_id in candidato["violacoes"]:
                valor = df.loc[item_id, atributo]
                formato = formatadores.get(atributo, "{}")
                linha[nome_coluna] = formato.format(valor)
            else:
                linha[nome_coluna] = "✓"

        reparos.append(linha)

    return pd.DataFrame(reparos)
