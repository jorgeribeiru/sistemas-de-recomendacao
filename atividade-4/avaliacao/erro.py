"""Métricas de erro de predição de notas: MAE, MSE e RMSE (Slides 5, 6 e 7)."""

from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite, sqrt


def _validar_pares(reais: Sequence[float], previstos: Sequence[float]) -> None:
    if len(reais) != len(previstos):
        raise ValueError("As listas de valores reais e previstos devem ter o mesmo tamanho.")
    if not reais:
        raise ValueError("É necessário informar ao menos um par de observações.")
    if any(not isfinite(v) for v in reais) or any(not isfinite(v) for v in previstos):
        raise ValueError("Todos os valores reais e previstos devem ser números finitos.")


def calcular_mae(reais: Sequence[float], previstos: Sequence[float]) -> float:
    """Mean Absolute Error (Slide 5): média de |y_i - y_hat_i|."""
    _validar_pares(reais, previstos)
    soma_erros_absolutos = sum(abs(y - y_hat) for y, y_hat in zip(reais, previstos))
    return soma_erros_absolutos / len(reais)


def calcular_mse(reais: Sequence[float], previstos: Sequence[float]) -> float:
    """Mean Square Error (Slide 6): média de (y_i - y_hat_i)^2."""
    _validar_pares(reais, previstos)
    soma_erros_quadrados = sum((y - y_hat) ** 2 for y, y_hat in zip(reais, previstos))
    return soma_erros_quadrados / len(reais)


def calcular_rmse(reais: Sequence[float], previstos: Sequence[float]) -> float:
    """Root Mean Square Error (Slide 7): raiz quadrada do MSE."""
    return sqrt(calcular_mse(reais, previstos))


@dataclass(frozen=True)
class ResumoErro:
    """Agrupa MAE, MSE, RMSE e os erros individuais e_i = y_i - y_hat_i."""

    n: int
    mae: float
    mse: float
    rmse: float
    erros: tuple[float, ...]
    maior_erro_absoluto: float


def resumir_erros(reais: Sequence[float], previstos: Sequence[float]) -> ResumoErro:
    """Calcula MAE, MSE e RMSE juntamente com o diagnóstico dos desvios."""
    _validar_pares(reais, previstos)
    erros = tuple(y - y_hat for y, y_hat in zip(reais, previstos))
    mae = calcular_mae(reais, previstos)
    mse = calcular_mse(reais, previstos)
    rmse = sqrt(mse)
    maior_abs = max(abs(erro) for erro in erros)
    return ResumoErro(
        n=len(reais),
        mae=mae,
        mse=mse,
        rmse=rmse,
        erros=erros,
        maior_erro_absoluto=maior_abs,
    )
