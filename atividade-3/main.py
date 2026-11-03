import operator
import numpy as np
import pandas as pd

# Mapeamento global de operadores relacionais para tornar as funções genéricas
OPERADORES = {
    "<=": operator.le,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    ">": operator.gt,
}


# ==============================================================================
# FUNÇÕES GENÉRICAS (Funcionam para qualquer DataFrame e conjunto de regras)
# ==============================================================================
def executar_consulta_conjuntiva(df: pd.DataFrame, requisitos: dict) -> pd.DataFrame:
    """Executa uma consulta conjuntiva genérica sigma[criteria](P) (Slide 9)

    sobre qualquer DataFrame a partir de um dicionário de requisitos.
    """
    mascaras = []
    for req_id, cfg in requisitos.items():
        op_func = OPERADORES[cfg["op"]]
        mascaras.append(op_func(df[cfg["attr"]], cfg["val"]))

    mascara_conjuntiva = np.logical_and.reduce(mascaras)
    return df[mascara_conjuntiva]


def diagnosticar_e_gerar_reparos(
    df: pd.DataFrame, requisitos: dict, formatadores: dict = None
) -> pd.DataFrame:
    """Identifica automaticamente se REQ tem solução.

    Caso não tenha (Slide 12-16):
      1. Descobre os diagnósticos mínimos 'd' (menores subconjuntos de restrições
         que precisam ser reparadas para encontrar pelo menos um item).
      2. Executa pi[attributes(d)] sigma[REQ - d](P) para montar a Tabela de Reparos.
    """
    formatadores = formatadores or {}
    candidatos = []

    for item_id, row in df.iterrows():
        violadas = []
        for req_id, cfg in requisitos.items():
            op_func = OPERADORES[cfg["op"]]
            if not op_func(row[cfg["attr"]], cfg["val"]):
                violadas.append(req_id)
        candidatos.append(
            {"id": item_id, "violadas": set(violadas), "lista_v": violadas}
        )

    # Filtra apenas os diagnósticos mínimos (onde nenhum outro item viola um subconjunto estrito)
    todos_conjuntos = [c["violadas"] for c in candidatos]
    minimos = [
        c
        for c in candidatos
        if not any(outro < c["violadas"] for outro in todos_conjuntos)
    ]

    # Ordena os diagnósticos na ordem canônica dos requisitos (ex: {r1, r2}, {r1, r4}, {r2, r3})
    chaves_req = list(requisitos.keys())
    minimos.sort(
        key=lambda c: (len(c["lista_v"]), [chaves_req.index(r) for r in c["lista_v"]])
    )

    reparos_lista = []
    for idx, c in enumerate(minimos, start=1):
        item_id = c["id"]
        diag_str = "{" + ", ".join(c["lista_v"]) + "}"
        linha = {
            "Repair": f"Rep{idx} (repair d{idx}={diag_str})",
            "Item": item_id,
        }

        for req_id, cfg in requisitos.items():
            attr = cfg["attr"]
            nome_col = cfg.get("label", attr)
            if req_id in c["violadas"]:
                val_bruto = df.loc[item_id, attr]
                fmt = formatadores.get(attr, "{}")
                linha[nome_col] = fmt.format(val_bruto)
            else:
                linha[nome_col] = "✓"

        reparos_lista.append(linha)

    return pd.DataFrame(reparos_lista)


def calcular_maut_generico(
    df: pd.DataFrame, regras_dimensoes: dict, perfis_clientes: dict
) -> pd.DataFrame:
    """Calcula a utilidade multi-atributo (MAUT) de forma genérica

    para quaisquer dimensões (ex: Quality, Economy) e perfis de clientes (ex: Cu1, Cu2).
    """
    nomes_dimensoes = list(
        next(iter(regras_dimensoes.values()))[0]["pontos"].keys()
    )
    resultados = []

    for item_id, row in df.iterrows():
        totais_dim = {dim: 0.0 for dim in nomes_dimensoes}

        for attr, lista_regras in regras_dimensoes.items():
            val_item = row[attr]
            for regra in lista_regras:
                op_func = OPERADORES[regra["op"]]
                if op_func(val_item, regra["val"]):
                    for dim, pts in regra["pontos"].items():
                        totais_dim[dim] += pts
                    break  # Aplica a primeira regra satisfeita para o atributo

        linha_res = {"id": item_id, **totais_dim}
        for nome_cli, pesos_cli in perfis_clientes.items():
            score_cli = sum(
                totais_dim[dim] * peso for dim, peso in pesos_cli.items()
            )
            linha_res[f"{nome_cli}_Score"] = round(score_cli, 2)

        resultados.append(linha_res)

    df_maut = pd.DataFrame(resultados).set_index("id")
    for nome_cli in perfis_clientes:
        df_maut[f"Rank_{nome_cli}"] = (
            df_maut[f"{nome_cli}_Score"]
            .rank(ascending=False, method="first")
            .astype(int)
        )

    return df_maut


def calcular_similaridade_casos(
    df: pd.DataFrame, requisitos_sim: dict
) -> pd.DataFrame:
    """Calcula a similaridade baseada em distância (Slide 19):

    similarity(p, REQ) = sum(w_r * sim(p, r)) / sum(w_r)
    Suporta 'LIB' (Less Is Better), 'MIB' (More Is Better), 'TARGET' e 'CAT'.
    """
    resultados = []

    for item_id, row in df.iterrows():
        soma_ponderada = 0.0
        soma_pesos = 0.0
        detalhes_sim = {}

        for attr, config in requisitos_sim.items():
            tipo = config["tipo"]
            peso = config["peso"]
            alvo = config.get("alvo", None)
            valor_item = row[attr]

            if tipo in ["LIB", "MIB", "TARGET"]:
                val_min = df[attr].min()
                val_max = df[attr].max()
                amplitude = val_max - val_min if val_max != val_min else 1.0

                if tipo == "LIB":
                    sim_r = (val_max - valor_item) / amplitude
                elif tipo == "MIB":
                    sim_r = (valor_item - val_min) / amplitude
                else:  # TARGET
                    sim_r = max(0.0, 1.0 - (abs(valor_item - alvo) / amplitude))
            else:  # CAT (Categórico/Booleano)
                sim_r = 1.0 if valor_item == alvo else 0.0

            soma_ponderada += peso * sim_r
            soma_pesos += peso
            detalhes_sim[f"sim_{attr}"] = round(sim_r, 3)

        score_final = soma_ponderada / soma_pesos if soma_pesos > 0 else 0.0
        detalhes_sim["Item"] = item_id
        detalhes_sim["Similarity_Score"] = round(score_final, 4)
        resultados.append(detalhes_sim)

    df_res = pd.DataFrame(resultados).set_index("Item")
    return df_res.sort_values(by="Similarity_Score", ascending=False)


# ==============================================================================
# 1. BASE DE DADOS: Catálogo de Câmeras Digitais
# ==============================================================================
dados_cameras = {
    "id": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"],
    "price": [148, 182, 189, 196, 151, 199, 259, 278],
    "mpix": [8.0, 8.0, 8.0, 10.0, 7.1, 9.0, 10.0, 9.1],
    "opt_zoom": [4, 5, 10, 12, 3, 3, 3, 10],
    "lcd_size": [2.5, 2.7, 2.5, 2.7, 3.0, 3.0, 3.0, 3.0],
    "movies": ["no", "yes", "yes", "yes", "yes", "yes", "yes", "yes"],
    "sound": ["no", "yes", "yes", "no", "yes", "yes", "yes", "yes"],
    "waterproof": ["yes", "no", "no", "yes", "no", "no", "no", "yes"],
}
df_catalogo = pd.DataFrame(dados_cameras).set_index("id")

print("=== 1. CATÁLOGO DE PRODUTOS")
print(df_catalogo)
print("-" * 75)


# ==============================================================================
# 2. CONSULTA CONJUNTIVA E REPAROS DE REQUISITOS
# ==============================================================================
print("\n=== 2. CONSULTA CONJUNTIVA E REPAROS")

# Consulta do Slide 9 parametrizada genericamente
req_slide9 = {
    "c1": {"attr": "mpix", "op": ">=", "val": 10.0},
    "c2": {"attr": "price", "op": "<", "val": 300},
}
consulta_slide9 = executar_consulta_conjuntiva(df_catalogo, req_slide9)
print(
    f"Consulta Conjuntiva Slide 9 (mpix >= 10 e price < 300): {list(consulta_slide9.index)}"
)

# Requisitos do Slide 15 parametrizados genericamente
req_slide15_rest = {
    "r1": {"attr": "price", "op": "<=", "val": 150, "label": "price(€)"},
    "r2": {"attr": "opt_zoom", "op": "==", "val": 5, "label": "opt-zoom"},
    "r3": {"attr": "sound", "op": "==", "val": "yes", "label": "sound"},
    "r4": {"attr": "waterproof", "op": "==", "val": "yes", "label": "waterproof"},
}
resultado_req_completo = executar_consulta_conjuntiva(df_catalogo, req_slide15_rest)
print(
    f"Resultado para REQ completo {{r1, r2, r3, r4}}: {list(resultado_req_completo.index)} (Sem solução!)"
)

print("\nTabela de Reparos:")
df_reparos = diagnosticar_e_gerar_reparos(
    df_catalogo, req_slide15_rest, formatadores={"opt_zoom": "{}x"}
)
print(df_reparos.to_string(index=False))
print("-" * 75)


# ==============================================================================
# 3. TEORIA DA UTILIDADE MULTI-ATRIBUTO - MAUT
# ==============================================================================
print("\n=== 3. RANKING POR UTILIDADE MULTI-ATRIBUTO - MAUT")

regras_maut_slide17 = {
    "price": [
        {"op": "<=", "val": 250, "pontos": {"Quality": 5, "Economy": 10}},
        {"op": ">", "val": 250, "pontos": {"Quality": 10, "Economy": 5}},
    ],
    "mpix": [
        {"op": "<=", "val": 8.0, "pontos": {"Quality": 4, "Economy": 10}},
        {"op": ">", "val": 8.0, "pontos": {"Quality": 10, "Economy": 6}},
    ],
    "opt_zoom": [
        {"op": "<=", "val": 9, "pontos": {"Quality": 6, "Economy": 9}},
        {"op": ">", "val": 9, "pontos": {"Quality": 10, "Economy": 6}},
    ],
    "lcd_size": [
        {"op": "<=", "val": 2.7, "pontos": {"Quality": 6, "Economy": 10}},
        {"op": ">", "val": 2.7, "pontos": {"Quality": 9, "Economy": 5}},
    ],
    "movies": [
        {"op": "==", "val": "yes", "pontos": {"Quality": 10, "Economy": 7}},
        {"op": "==", "val": "no", "pontos": {"Quality": 3, "Economy": 10}},
    ],
    "sound": [
        {"op": "==", "val": "yes", "pontos": {"Quality": 10, "Economy": 8}},
        {"op": "==", "val": "no", "pontos": {"Quality": 7, "Economy": 10}},
    ],
    "waterproof": [
        {"op": "==", "val": "yes", "pontos": {"Quality": 10, "Economy": 6}},
        {"op": "==", "val": "no", "pontos": {"Quality": 8, "Economy": 10}},
    ],
}

perfis_clientes_slide18 = {
    "Cu1": {"Quality": 0.80, "Economy": 0.20},
    "Cu2": {"Quality": 0.40, "Economy": 0.60},
}

df_maut = calcular_maut_generico(
    df_catalogo, regras_maut_slide17, perfis_clientes_slide18
)
print(df_maut)
print("-" * 75)


# ==============================================================================
# 4. RECOMENDAÇÃO BASEADA EM CASOS - SIMILARIDADE POR DISTÂNCIA (Slide 19)
# ==============================================================================
print("\n=== 4. SIMILARIDADE BASEADA EM CASOS / DISTÂNCIA")

# Caso A: Requisitos do Slide 15 avaliados por similaridade (Slide 19)
req_slide15_sim = {
    "price": {"tipo": "LIB", "peso": 1.0},
    "opt_zoom": {"tipo": "TARGET", "alvo": 5, "peso": 1.0},
    "sound": {"tipo": "CAT", "alvo": "yes", "peso": 1.0},
    "waterproof": {"tipo": "CAT", "alvo": "yes", "peso": 1.0},
}

print("A) Ranking de Similaridade para os Requisitos do Slide 15 (Pesos Iguais):")
df_sim_caso_a = calcular_similaridade_casos(df_catalogo, req_slide15_sim)
print(df_sim_caso_a)

# Caso B: Exemplo MIB vs LIB do Slide 19 (Maximizar Resolução MIB e Minimizar Preço LIB)
req_mib_lib = {
    "mpix": {"tipo": "MIB", "peso": 0.6},
    "price": {"tipo": "LIB", "peso": 0.4},
}

print(
    "\nB) Ranking de Similaridade MIB/LIB do Slide 19 (Maximizar mpix [0.6] e Minimizar price [0.4]):"
)
df_sim_caso_b = calcular_similaridade_casos(df_catalogo, req_mib_lib)
print(df_sim_caso_b)