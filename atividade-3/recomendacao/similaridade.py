import pandas as pd


def calcular_similaridade_casos(
    df: pd.DataFrame, requisitos_sim: dict
) -> pd.DataFrame:
    """Calcula a similaridade baseada em distância (Slide 19):

    similarity(p, REQ) = sum(w_r * sim(p, r)) / sum(w_r)
    LIB favorece valores menores; MIB, maiores. TARGET aproxima um alvo
    numérico e CAT verifica igualdade com um valor categórico.
    """
    resultados = []

    for item_id, item in df.iterrows():
        soma_ponderada = 0.0
        soma_pesos = 0.0
        detalhes = {}

        for atributo, configuracao in requisitos_sim.items():
            tipo = configuracao["tipo"]
            peso = configuracao["peso"]
            alvo = configuracao.get("alvo", None)
            valor_item = item[atributo]

            if tipo in ["LIB", "MIB", "TARGET"]:
                valor_minimo = df[atributo].min()
                valor_maximo = df[atributo].max()
                amplitude = valor_maximo - valor_minimo if valor_maximo != valor_minimo else 1.0

                if tipo == "LIB":
                    similaridade = (valor_maximo - valor_item) / amplitude
                elif tipo == "MIB":
                    similaridade = (valor_item - valor_minimo) / amplitude
                else:  # TARGET
                    similaridade = max(0.0, 1.0 - (abs(valor_item - alvo) / amplitude))
            else:  # CAT (Categórico/Booleano)
                similaridade = 1.0 if valor_item == alvo else 0.0

            soma_ponderada += peso * similaridade
            soma_pesos += peso
            detalhes[f"sim_{atributo}"] = round(similaridade, 3)

        pontuacao_final = soma_ponderada / soma_pesos if soma_pesos > 0 else 0.0
        detalhes["Item"] = item_id
        detalhes["Similarity_Score"] = round(pontuacao_final, 4)
        resultados.append(detalhes)

    ranking = pd.DataFrame(resultados).set_index("Item")
    return ranking.sort_values(by="Similarity_Score", ascending=False)
