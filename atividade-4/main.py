"""Execução didática de todas as métricas e exercícios da Atividade 4."""

from avaliacao.classificacao import MatrizConfusao, avaliar_classificacao
from avaliacao.dados import carregar_predicoes_notas, carregar_rankings_usuarios
from avaliacao.erro import resumir_erros
from avaliacao.exemplos import (
    RANKING_SLIDE8,
    RECOMENDADOR_1_SLIDE10,
    RECOMENDADOR_2_SLIDE10,
    TOTAL_CATALOGO_SLIDE10,
    TOTAL_RELEVANTES_SLIDE10,
)
from avaliacao.ranking import (
    calcular_dcg,
    calcular_dcg_medio_usuarios,
    calcular_idcg,
    calcular_ndcg,
    calcular_ndcg_medio_usuarios,
    detalhar_dcg_posicoes,
)
from avaliacao.roc import calcular_auc_roc, calcular_curva_roc_ranking

SEPARADOR = "-" * 78


def _formatar_sequencia_slide10(sequencia: list[int]) -> str:
    return " ".join(f"{i}:{'V' if v else 'X'}" for i, v in enumerate(sequencia, start=1))


def exibir_secao_classificacao() -> None:
    print("=== 1. CLASSIFICAÇÃO E EXERCÍCIO DO SLIDE 10 (PRECISION, RECALL, F1 E ACURÁCIA)")
    print(
        f"Total de relevantes na base = {TOTAL_RELEVANTES_SLIDE10} | "
        f"Catálogo total ilustrativo (para VN/Acurácia) = {TOTAL_CATALOGO_SLIDE10}\n"
    )

    cenarios = [
        ("Recomendador 1 (Top-10)", RECOMENDADOR_1_SLIDE10),
        ("Recomendador 2 (Top-5)", RECOMENDADOR_2_SLIDE10),
    ]

    for nome, lista_binaria in cenarios:
        print(f"• {nome}: [{_formatar_sequencia_slide10(lista_binaria)}]")

    print(
        "\n"
        f"{'Sistema':<24} {'VP':>4} {'FP':>4} {'FN':>4} {'VN':>4} "
        f"{'Precision':>10} {'Recall':>9} {'F1':>9} {'Acurácia':>10} {'Taxa Erro':>10}"
    )
    print(SEPARADOR)

    for nome, lista_binaria in cenarios:
        matriz = MatrizConfusao.de_resultados_binarios(
            relevancias_recuperadas=lista_binaria,
            total_relevantes=TOTAL_RELEVANTES_SLIDE10,
            total_catalogo=TOTAL_CATALOGO_SLIDE10,
        )
        resumo = avaliar_classificacao(matriz, incluir_acuracia=True)
        print(
            f"{nome:<24} {matriz.vp:>4} {matriz.fp:>4} {matriz.fn:>4} {matriz.vn:>4} "
            f"{resumo.precisao * 100:>9.2f}% {resumo.recall * 100:>8.2f}% "
            f"{resumo.f1 * 100:>8.2f}% {(resumo.acuracia or 0.0) * 100:>9.2f}% "
            f"{(resumo.taxa_erro or 0.0) * 100:>9.2f}%"
        )
    print(SEPARADOR)


def exibir_secao_erros() -> None:
    print("\n=== 2. MÉTRICAS DE ERRO DE PREDIÇÃO DE NOTAS (SLIDES 5, 6 E 7: MAE, MSE E RMSE)")
    registros = carregar_predicoes_notas()
    reais = [r.nota_real for r in registros]
    prev_a = [r.modelo_a for r in registros]
    prev_b = [r.modelo_b for r in registros]

    print(
        f"{'Usuário':<8} {'Item':<5} {'Título':<20} {'Real':>6} "
        f"{'Mod. A':>8} {'|e_A|':>7} {'Mod. B':>8} {'|e_B|':>7}"
    )
    print(SEPARADOR)
    for r in registros:
        print(
            f"{r.user_id:<8} {r.item_id:<5} {r.title:<20} {r.nota_real:>6.2f} "
            f"{r.modelo_a:>8.2f} {abs(r.nota_real - r.modelo_a):>7.2f} "
            f"{r.modelo_b:>8.2f} {abs(r.nota_real - r.modelo_b):>7.2f}"
        )

    resumo_a = resumir_erros(reais, prev_a)
    resumo_b = resumir_erros(reais, prev_b)

    print("\nComparativo consolidado (n = 8 avaliações):")
    print(f"{'Modelo':<28} {'MAE':>10} {'MSE':>10} {'RMSE':>10} {'Maior |e_i|':>13}")
    print(SEPARADOR)
    print(
        f"{'Modelo A (erros leves)':<28} {resumo_a.mae:>10.4f} {resumo_a.mse:>10.4f} "
        f"{resumo_a.rmse:>10.4f} {resumo_a.maior_erro_absoluto:>13.2f}"
    )
    print(
        f"{'Modelo B (erros grandes)':<28} {resumo_b.mae:>10.4f} {resumo_b.mse:>10.4f} "
        f"{resumo_b.rmse:>10.4f} {resumo_b.maior_erro_absoluto:>13.2f}"
    )
    print(SEPARADOR)


def exibir_secao_ranking() -> None:
    print("\n=== 3. MÉTRICAS DE RANKING PONDERADO (SLIDES 8 E 9: DCG, IDCG E NDCG)")
    print("A) Memória de cálculo do Slide 8 — Relevâncias [3, 2, 3]:")
    passos = detalhar_dcg_posicoes(RANKING_SLIDE8)
    for passo in passos:
        print(
            f"   {passo.posicao}º lugar (p = {passo.posicao}): Relevância {passo.relevancia:.0f} "
            f"-> {passo.relevancia:.0f} / max(1, log2({passo.posicao})) "
            f"= {passo.relevancia:.0f} / {passo.desconto:.2f} = {passo.ganho_descontado:.2f}"
        )
    dcg_slide8 = calcular_dcg(RANKING_SLIDE8)
    idcg_slide8 = calcular_idcg(RANKING_SLIDE8)
    ndcg_slide8 = calcular_ndcg(RANKING_SLIDE8)
    print(
        f"   DCG = {dcg_slide8:.4f} (no slide: ~6,89) | "
        f"IDCG [3, 3, 2] = {idcg_slide8:.4f} | NDCG = {ndcg_slide8:.4f}"
    )

    print("\nB) Avaliação multiusuário (data/rankings_usuarios.csv — Corte Top-5):")
    rankings_csv = carregar_rankings_usuarios()
    relevancias_por_usuario = {
        u: [item.relevancia_grau for item in itens] for u, itens in rankings_csv.items()
    }

    corte_k = 5
    print(f"{'Usuário':<10} {'Relevâncias Top-5':<24} {'DCG@5':>10} {'IDCG@5':>10} {'NDCG@5':>10}")
    print(SEPARADOR)
    for usuario, rel_completa in relevancias_por_usuario.items():
        top_k = [int(r) for r in rel_completa[:corte_k]]
        dcg_u = calcular_dcg(rel_completa, k=corte_k)
        idcg_u = calcular_idcg(rel_completa, k=corte_k)
        ndcg_u = calcular_ndcg(rel_completa, relevancias_ideais=rel_completa, k=corte_k)
        print(f"{usuario:<10} {str(top_k):<24} {dcg_u:>10.4f} {idcg_u:>10.4f} {ndcg_u:>10.4f}")

    dcg_medio = calcular_dcg_medio_usuarios(relevancias_por_usuario, k=corte_k)
    ndcg_medio = calcular_ndcg_medio_usuarios(
        relevancias_por_usuario, ideais_por_usuario=relevancias_por_usuario, k=corte_k
    )
    print(SEPARADOR)
    print(f"{'Média (U = 3 usuários)':<35} {dcg_medio:>10.4f} {'-':>10} {ndcg_medio:>10.4f}")
    print(SEPARADOR)


def exibir_secao_roc() -> None:
    print("\n=== 4. CURVA ROC E ÁREA SOB A CURVA - AUC (SLIDE 9)")
    rankings_csv = carregar_rankings_usuarios()

    itens_u1 = rankings_csv["u1"]
    pontos_u1 = calcular_curva_roc_ranking(
        relevantes_ordenados=[item.relevante_binario for item in itens_u1],
        scores_ordenados=[item.score_previsto for item in itens_u1],
    )
    auc_u1 = calcular_auc_roc(pontos_u1)

    print("A) Evolução da Curva ROC por corte/limiar para o perfil u1:")
    print(
        f"{'Corte k':>7} {'Limiar':>8} {'VP':>4} {'FP':>4} {'FN':>4} {'VN':>4} "
        f"{'FPR (1-Esp.)':>14} {'TPR (Recall)':>14}"
    )
    print(SEPARADOR)
    for p in pontos_u1:
        limiar_txt = "-" if p.limiar_score is None else f"{p.limiar_score:.2f}"
        print(
            f"{p.corte:>7} {limiar_txt:>8} {p.vp:>4} {p.fp:>4} {p.fn:>4} {p.vn:>4} "
            f"{p.fpr:>14.4f} {p.tpr:>14.4f}"
        )
    print(f"AUC-ROC (u1) = {auc_u1:.4f}")

    print("\nB) Comparação de AUC-ROC entre perfis de ranking:")
    descricoes = {
        "u1": "Bom recomendador (relevantes concentrados no topo)",
        "u2": "Recomendador perfeito (todos os relevantes antes dos não relevantes)",
        "u3": "Recomendador fraco (relevantes empurrados para o fim da lista)",
    }
    for usuario, itens in rankings_csv.items():
        pontos = calcular_curva_roc_ranking(
            relevantes_ordenados=[i.relevante_binario for i in itens],
            scores_ordenados=[i.score_previsto for i in itens],
        )
        auc = calcular_auc_roc(pontos)
        print(f"   • {usuario} — {descricoes[usuario]}: AUC = {auc:.4f}")
    print(SEPARADOR)


def main() -> int:
    exibir_secao_classificacao()
    exibir_secao_erros()
    exibir_secao_ranking()
    exibir_secao_roc()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
