"""Curva ROC (Receiver Operating Characteristics) e Área sob a Curva - AUC (Slide 9)."""

from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite

from .classificacao import calcular_recall


@dataclass(frozen=True)
class PontoROC:
    """Estado da avaliação em um corte k (ou limiar de score) da lista ordenada."""

    corte: int
    limiar_score: float | None
    vp: int
    fp: int
    fn: int
    vn: int
    fpr: float  # False Positive Rate = FP / (FP + VN)
    tpr: float  # True Positive Rate (Recall) = VP / (VP + FN)


def calcular_fpr(fp: int, vn: int) -> float:
    """Taxa de Falsos Positivos: fração de não relevantes incorretamente recuperados."""
    nao_relevantes = fp + vn
    if nao_relevantes <= 0:
        raise ValueError(
            "Não é possível calcular FPR sem itens não relevantes (FP + VN = 0)."
        )
    return fp / nao_relevantes


def calcular_curva_roc_ranking(
    relevantes_ordenados: Sequence[int | bool],
    scores_ordenados: Sequence[float] | None = None,
    total_relevantes: int | None = None,
    total_nao_relevantes: int | None = None,
) -> list[PontoROC]:
    """Gera os pontos (FPR, TPR) variando o tamanho k da lista recomendada (k = 0..N).

    Quando scores_ordenados é informado com empates, agrupa itens de mesmo score no
    mesmo limiar para refletir fielmente a curva ROC por threshold.
    """
    if not relevantes_ordenados:
        raise ValueError("A sequência de itens avaliados não pode ser vazia.")
    for valor in relevantes_ordenados:
        if valor not in (0, 1, False, True):
            raise ValueError("Cada item deve ter relevância binária 0 ou 1.")

    if scores_ordenados is not None:
        if len(scores_ordenados) != len(relevantes_ordenados):
            raise ValueError("scores_ordenados deve ter o mesmo tamanho de relevantes_ordenados.")
        if any(not isfinite(s) for s in scores_ordenados):
            raise ValueError("Todos os scores devem ser números finitos.")
        if any(
            scores_ordenados[i] < scores_ordenados[i + 1]
            for i in range(len(scores_ordenados) - 1)
        ):
            raise ValueError("scores_ordenados deve estar em ordem não crescente.")

    pos_observados = sum(1 for v in relevantes_ordenados if v)
    neg_observados = len(relevantes_ordenados) - pos_observados

    tot_pos = pos_observados if total_relevantes is None else total_relevantes
    tot_neg = neg_observados if total_nao_relevantes is None else total_nao_relevantes

    if tot_pos < pos_observados or tot_pos <= 0:
        raise ValueError("total_relevantes deve ser positivo e >= positivos na lista.")
    if tot_neg < neg_observados or tot_neg <= 0:
        raise ValueError("total_nao_relevantes deve ser positivo e >= negativos na lista.")

    pontos = [
        PontoROC(
            corte=0,
            limiar_score=None,
            vp=0,
            fp=0,
            fn=tot_pos,
            vn=tot_neg,
            fpr=0.0,
            tpr=0.0,
        )
    ]

    vp_acumulado = 0
    fp_acumulado = 0
    n = len(relevantes_ordenados)
    indice = 0

    while indice < n:
        if scores_ordenados is not None:
            limiar = scores_ordenados[indice]
            while indice < n and scores_ordenados[indice] == limiar:
                if relevantes_ordenados[indice]:
                    vp_acumulado += 1
                else:
                    fp_acumulado += 1
                indice += 1
        else:
            limiar = None
            if relevantes_ordenados[indice]:
                vp_acumulado += 1
            else:
                fp_acumulado += 1
            indice += 1

        fn = tot_pos - vp_acumulado
        vn = tot_neg - fp_acumulado
        pontos.append(
            PontoROC(
                corte=indice,
                limiar_score=limiar,
                vp=vp_acumulado,
                fp=fp_acumulado,
                fn=fn,
                vn=vn,
                fpr=calcular_fpr(fp_acumulado, vn),
                tpr=calcular_recall(vp_acumulado, fn),
            )
        )

    if pontos[-1].fpr < 1.0 or pontos[-1].tpr < 1.0:
        pontos.append(
            PontoROC(
                corte=tot_pos + tot_neg,
                limiar_score=None,
                vp=tot_pos,
                fp=tot_neg,
                fn=0,
                vn=0,
                fpr=1.0,
                tpr=1.0,
            )
        )

    return pontos


def calcular_auc_roc(pontos_roc: Sequence[PontoROC]) -> float:
    """Calcula a Área sob a Curva ROC (AUC) via integração pela regra do trapézio."""
    if len(pontos_roc) < 2:
        raise ValueError("São necessários ao menos dois pontos para calcular a AUC.")
    area = 0.0
    for anterior, atual in zip(pontos_roc, pontos_roc[1:]):
        largura = atual.fpr - anterior.fpr
        if largura < 0:
            raise ValueError("Os pontos da curva ROC devem ter FPR não decrescente.")
        altura_media = (anterior.tpr + atual.tpr) / 2.0
        area += largura * altura_media
    return area
