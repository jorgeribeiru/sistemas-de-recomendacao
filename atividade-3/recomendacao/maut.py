import pandas as pd

from .operadores import OPERADORES


def calcular_maut_generico(
    df: pd.DataFrame, regras_dimensoes: dict, perfis_clientes: dict
) -> pd.DataFrame:
    """Soma pontos por dimensão e calcula o ranking de cada perfil.

    Para cada atributo, somente a primeira regra satisfeita atribui pontos.
    A pontuação do cliente é a soma ponderada das dimensões.
    """
    nomes_dimensoes = list(
        next(iter(regras_dimensoes.values()))[0]["pontos"].keys()
    )
    resultados = []

    for item_id, item in df.iterrows():
        pontos_por_dimensao = {dimensao: 0.0 for dimensao in nomes_dimensoes}

        for atributo, lista_regras in regras_dimensoes.items():
            valor_item = item[atributo]
            for regra in lista_regras:
                comparar = OPERADORES[regra["op"]]
                if comparar(valor_item, regra["val"]):
                    for dimensao, pontos in regra["pontos"].items():
                        pontos_por_dimensao[dimensao] += pontos
                    break  # Aplica a primeira regra satisfeita para o atributo

        resultado_item = {"id": item_id, **pontos_por_dimensao}
        for cliente, pesos in perfis_clientes.items():
            pontuacao = sum(
                pontos_por_dimensao[dimensao] * peso for dimensao, peso in pesos.items()
            )
            resultado_item[f"{cliente}_Score"] = round(pontuacao, 2)

        resultados.append(resultado_item)

    ranking = pd.DataFrame(resultados).set_index("id")
    for cliente in perfis_clientes:
        ranking[f"Rank_{cliente}"] = (
            ranking[f"{cliente}_Score"]
            .rank(ascending=False, method="first")
            .astype(int)
        )

    return ranking
