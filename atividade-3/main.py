from recomendacao.consulta import executar_consulta_conjuntiva, diagnosticar_e_gerar_reparos
from recomendacao.dados import carregar_catalogo
from recomendacao.exemplos import (
    req_slide9, req_slide15_rest, regras_maut_slide17,
    perfis_clientes_slide18, req_slide15_sim, req_mib_lib,
)
from recomendacao.maut import calcular_maut_generico
from recomendacao.similaridade import calcular_similaridade_casos


def main():
    df_catalogo = carregar_catalogo()
    print("=== 1. CATÁLOGO DE PRODUTOS")
    print(df_catalogo)
    print("-" * 75)
    print("\n=== 2. CONSULTA CONJUNTIVA E REPAROS")
    consulta_slide9 = executar_consulta_conjuntiva(df_catalogo, req_slide9)
    print(
        f"Consulta Conjuntiva (mpix >= 10 e price < 300): {list(consulta_slide9.index)}"
    )
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
    print("\n=== 3. RANKING POR UTILIDADE MULTI-ATRIBUTO - MAUT")
    df_maut = calcular_maut_generico(
        df_catalogo, regras_maut_slide17, perfis_clientes_slide18
    )
    print(df_maut)
    print("-" * 75)
    print("\n=== 4. SIMILARIDADE BASEADA EM CASOS / DISTÂNCIA")
    print("A) Ranking de Similaridade para os Requisitos (Pesos Iguais):")
    df_sim_caso_a = calcular_similaridade_casos(df_catalogo, req_slide15_sim)
    print(df_sim_caso_a)
    print(
        "\nB) Ranking de Similaridade MIB/LIB (Maximizar mpix [0.6] e Minimizar price [0.4]):"
    )
    df_sim_caso_b = calcular_similaridade_casos(df_catalogo, req_mib_lib)
    print(df_sim_caso_b)


if __name__ == "__main__":
    main()
