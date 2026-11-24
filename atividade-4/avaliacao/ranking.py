"""Métricas de ranking ponderado por posição: DCG, IDCG e NDCG (Slides 8 e 9)."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import isfinite, log2


@dataclass(frozen=True)
class PassoDCG:
    """Memória de cálculo de uma posição p no ranking conforme o Slide 8."""

    posicao: int
    relevancia: float
    desconto: float
    ganho_descontado: float


def _validar_relevancias(relevancias: Sequence[float], k: int | None = None) -> list[float]:
    if k is not None and k < 1:
        raise ValueError("O corte k deve ser um inteiro positivo.")
    recorte = list(relevancias[:k] if k is not None else relevancias)
    if not recorte:
        raise ValueError("A lista de relevâncias não pode ser vazia.")
    if any(not isfinite(r) or r < 0 for r in recorte):
        raise ValueError("As relevâncias devem ser números finitos e não negativos.")
    return recorte


def calcular_desconto_posicao(posicao: int) -> float:
    """Denominador max(1, log2(p)) definido no Slide 8 (p >= 1)."""
    if posicao < 1:
        raise ValueError("A posição p no ranking deve começar em 1.")
    return max(1.0, log2(posicao))


def detalhar_dcg_posicoes(
    relevancias: Sequence[float], k: int | None = None
) -> list[PassoDCG]:
    """Devolve o cálculo posição a posição (p = 1..P) usado no exemplo do Slide 8."""
    recorte = _validar_relevancias(relevancias, k)
    passos: list[PassoDCG] = []
    for indice, relevancia in enumerate(recorte, start=1):
        desconto = calcular_desconto_posicao(indice)
        passos.append(
            PassoDCG(
                posicao=indice,
                relevancia=relevancia,
                desconto=desconto,
                ganho_descontado=relevancia / desconto,
            )
        )
    return passos


def calcular_dcg(relevancias: Sequence[float], k: int | None = None) -> float:
    """Discounted Cumulative Gain para um único ranking: soma w_p / max(1, log2(p))."""
    return sum(passo.ganho_descontado for passo in detalhar_dcg_posicoes(relevancias, k))


def calcular_idcg(relevancias_ideais: Sequence[float], k: int | None = None) -> float:
    """Ideal DCG: ganho acumulado máximo ao ordenar as relevâncias de forma decrescente."""
    if any(not isfinite(r) or r < 0 for r in relevancias_ideais):
        raise ValueError("As relevâncias ideais devem ser números finitos e não negativos.")
    ordenadas = sorted(relevancias_ideais, reverse=True)
    return calcular_dcg(ordenadas, k=k)


def calcular_ndcg(
    relevancias: Sequence[float],
    relevancias_ideais: Sequence[float] | None = None,
    k: int | None = None,
) -> float:
    """Normalized DCG (Slide 9): razão DCG / IDCG no intervalo [0, 1]."""
    dcg = calcular_dcg(relevancias, k=k)
    base_ideal = relevancias_ideais if relevancias_ideais is not None else relevancias
    idcg = calcular_idcg(base_ideal, k=k)
    if idcg == 0.0:
        return 0.0
    return dcg / idcg


def calcular_dcg_medio_usuarios(
    rankings_por_usuario: Mapping[str, Sequence[float]], k: int | None = None
) -> float:
    """Equação geral do Slide 8: média (1/U) do DCG entre U usuários."""
    if not rankings_por_usuario:
        raise ValueError("É necessário informar ao menos um usuário.")
    soma_dcg = sum(calcular_dcg(rel, k=k) for rel in rankings_por_usuario.values())
    return soma_dcg / len(rankings_por_usuario)


def calcular_ndcg_medio_usuarios(
    rankings_por_usuario: Mapping[str, Sequence[float]],
    ideais_por_usuario: Mapping[str, Sequence[float]] | None = None,
    k: int | None = None,
) -> float:
    """Média do NDCG entre U usuários."""
    if not rankings_por_usuario:
        raise ValueError("É necessário informar ao menos um usuário.")
    soma_ndcg = 0.0
    for usuario, rel in rankings_por_usuario.items():
        ideal = ideais_por_usuario[usuario] if ideais_por_usuario is not None else rel
        soma_ndcg += calcular_ndcg(rel, relevancias_ideais=ideal, k=k)
    return soma_ndcg / len(rankings_por_usuario)
