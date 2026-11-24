"""Testes unitários das métricas de avaliação e gabaritos dos slides (Atividade 4)."""

from contextlib import redirect_stdout
from io import StringIO
from math import log2
import unittest

from avaliacao.classificacao import (
    MatrizConfusao,
    avaliar_classificacao,
    calcular_acuracia,
    calcular_f_measure,
    calcular_precisao,
    calcular_recall,
    calcular_taxa_erro,
)
from avaliacao.dados import carregar_predicoes_notas, carregar_rankings_usuarios
from avaliacao.erro import calcular_mae, calcular_mse, calcular_rmse, resumir_erros
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
import main as script_principal


class ClassificacaoSlideTests(unittest.TestCase):
    def test_exercicio_slide10_recomendador_1(self) -> None:
        matriz = MatrizConfusao.de_resultados_binarios(
            RECOMENDADOR_1_SLIDE10,
            total_relevantes=TOTAL_RELEVANTES_SLIDE10,
            total_catalogo=TOTAL_CATALOGO_SLIDE10,
        )
        self.assertEqual((matriz.vp, matriz.fp, matriz.fn, matriz.vn), (5, 5, 15, 25))
        resumo = avaliar_classificacao(matriz)
        self.assertAlmostEqual(resumo.precisao, 0.50)
        self.assertAlmostEqual(resumo.recall, 0.25)
        self.assertAlmostEqual(resumo.f1, 1.0 / 3.0)
        self.assertAlmostEqual(resumo.acuracia or 0.0, 0.60)
        self.assertAlmostEqual(resumo.taxa_erro or 0.0, 0.40)

    def test_exercicio_slide10_recomendador_2(self) -> None:
        matriz = MatrizConfusao.de_resultados_binarios(
            RECOMENDADOR_2_SLIDE10,
            total_relevantes=TOTAL_RELEVANTES_SLIDE10,
            total_catalogo=TOTAL_CATALOGO_SLIDE10,
        )
        self.assertEqual((matriz.vp, matriz.fp, matriz.fn, matriz.vn), (3, 2, 17, 28))
        resumo = avaliar_classificacao(matriz)
        self.assertAlmostEqual(resumo.precisao, 0.60)
        self.assertAlmostEqual(resumo.recall, 0.15)
        self.assertAlmostEqual(resumo.f1, 0.24)
        self.assertAlmostEqual(
            (resumo.acuracia or 0.0) + (resumo.taxa_erro or 0.0), 1.0
        )

    def test_construcao_por_conjuntos_e_validacoes(self) -> None:
        matriz = MatrizConfusao.de_conjuntos(
            itens_recuperados=["m1", "m2", "m3"],
            itens_relevantes=["m2", "m3", "m4"],
            catalogo_completo=["m1", "m2", "m3", "m4", "m5"],
        )
        self.assertEqual((matriz.vp, matriz.fp, matriz.fn, matriz.vn), (2, 1, 1, 1))
        self.assertEqual(calcular_f_measure(0.0, 0.0), 0.0)

        with self.assertRaises(ValueError):
            calcular_precisao(0, 0)
        with self.assertRaises(ValueError):
            calcular_recall(0, 0)
        with self.assertRaises(ValueError):
            calcular_acuracia(0, 0, 0, 0)
        with self.assertRaises(ValueError):
            calcular_taxa_erro(0, 0, 0, 0)
        with self.assertRaises(ValueError):
            MatrizConfusao(-1, 0, 0, 0)


class ErroPredicaoTests(unittest.TestCase):
    def test_comparacao_mae_mse_rmse_base_csv(self) -> None:
        registros = carregar_predicoes_notas()
        reais = [r.nota_real for r in registros]
        prev_a = [r.modelo_a for r in registros]
        prev_b = [r.modelo_b for r in registros]

        self.assertAlmostEqual(calcular_mae(reais, prev_a), 0.50)
        self.assertAlmostEqual(calcular_mae(reais, prev_b), 0.50)

        self.assertAlmostEqual(calcular_mse(reais, prev_a), 0.25)
        self.assertAlmostEqual(calcular_rmse(reais, prev_a), 0.50)

        self.assertAlmostEqual(calcular_mse(reais, prev_b), 1.00)
        self.assertAlmostEqual(calcular_rmse(reais, prev_b), 1.00)

        resumo_b = resumir_erros(reais, prev_b)
        self.assertEqual(resumo_b.n, 8)
        self.assertAlmostEqual(resumo_b.maior_erro_absoluto, 2.0)

    def test_validacao_entradas_invalidas(self) -> None:
        with self.assertRaises(ValueError):
            calcular_mae([], [])
        with self.assertRaises(ValueError):
            calcular_mse([1.0, 2.0], [1.0])
        with self.assertRaises(ValueError):
            calcular_rmse([float("nan")], [3.0])


class RankingDCGTests(unittest.TestCase):
    def test_exemplo_exato_slide8(self) -> None:
        passos = detalhar_dcg_posicoes(RANKING_SLIDE8)
        self.assertAlmostEqual(passos[0].ganho_descontado, 3.00)
        self.assertAlmostEqual(passos[1].ganho_descontado, 2.00)
        self.assertAlmostEqual(passos[2].ganho_descontado, 3.0 / log2(3))

        dcg = calcular_dcg(RANKING_SLIDE8)
        self.assertAlmostEqual(round(dcg, 2), 6.89)

        idcg = calcular_idcg(RANKING_SLIDE8)
        self.assertAlmostEqual(idcg, 3.0 + 3.0 + 2.0 / log2(3))
        self.assertAlmostEqual(calcular_ndcg(RANKING_SLIDE8), dcg / idcg)

    def test_ndcg_perfeito_nulo_e_multiusuario(self) -> None:
        self.assertAlmostEqual(calcular_ndcg([3, 3, 2, 1, 0]), 1.0)
        self.assertEqual(calcular_ndcg([0, 0, 0]), 0.0)

        rankings = {"u1": [3, 2, 3], "u2": [3, 3, 2]}
        dcg_medio = calcular_dcg_medio_usuarios(rankings)
        self.assertAlmostEqual(
            dcg_medio, (calcular_dcg([3, 2, 3]) + calcular_dcg([3, 3, 2])) / 2.0
        )
        ndcg_medio = calcular_ndcg_medio_usuarios(rankings)
        self.assertAlmostEqual(ndcg_medio, (calcular_ndcg([3, 2, 3]) + 1.0) / 2.0)


class CurvaROCTests(unittest.TestCase):
    def test_auc_perfeito_aleatorio_e_usuarios_csv(self) -> None:
        pontos_perfeitos = calcular_curva_roc_ranking([1, 1, 1, 0, 0, 0])
        self.assertAlmostEqual(calcular_auc_roc(pontos_perfeitos), 1.0)

        pontos_invertidos = calcular_curva_roc_ranking([0, 0, 0, 1, 1, 1])
        self.assertAlmostEqual(calcular_auc_roc(pontos_invertidos), 0.0)

        # Empate total de scores gera diagonal (0,0) -> (1,1) com AUC = 0.5
        pontos_empate = calcular_curva_roc_ranking(
            [1, 0, 1, 0], scores_ordenados=[0.5, 0.5, 0.5, 0.5]
        )
        self.assertAlmostEqual(calcular_auc_roc(pontos_empate), 0.5)

        rankings = carregar_rankings_usuarios()
        auc_u1 = calcular_auc_roc(
            calcular_curva_roc_ranking(
                [i.relevante_binario for i in rankings["u1"]],
                [i.score_previsto for i in rankings["u1"]],
            )
        )
        auc_u2 = calcular_auc_roc(
            calcular_curva_roc_ranking(
                [i.relevante_binario for i in rankings["u2"]],
                [i.score_previsto for i in rankings["u2"]],
            )
        )
        auc_u3 = calcular_auc_roc(
            calcular_curva_roc_ranking(
                [i.relevante_binario for i in rankings["u3"]],
                [i.score_previsto for i in rankings["u3"]],
            )
        )
        self.assertAlmostEqual(auc_u1, 0.8125)
        self.assertAlmostEqual(auc_u2, 1.0000)
        self.assertAlmostEqual(auc_u3, 0.3750)


class MainExecucaoTests(unittest.TestCase):
    def test_main_executa_todas_as_secoes_sem_erros(self) -> None:
        saida = StringIO()
        with redirect_stdout(saida):
            codigo = script_principal.main()
        texto = saida.getvalue()
        self.assertEqual(codigo, 0)
        self.assertIn("Recomendador 1 (Top-10)", texto)
        self.assertIn("Modelo A (erros leves)", texto)
        self.assertIn("DCG = 6.8928", texto)
        self.assertIn("AUC-ROC (u1) = 0.8125", texto)


if __name__ == "__main__":
    unittest.main()
