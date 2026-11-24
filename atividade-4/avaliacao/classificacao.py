"""Métricas de classificação e recuperação: Matriz de Confusão, Acurácia, Erro, Precision, Recall e F-Measure."""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class MatrizConfusao:
    """Tabela de contingência entre itens recuperados pelo sistema e itens relevantes."""

    vp: int  # Verdadeiro Positivo: recuperado e relevante
    fp: int  # Falso Positivo: recuperado e não relevante
    fn: int  # Falso Negativo: não recuperado, mas relevante
    vn: int = 0  # Verdadeiro Negativo: não recuperado e não relevante

    def __post_init__(self) -> None:
        if any(valor < 0 for valor in (self.vp, self.fp, self.fn, self.vn)):
            raise ValueError("As contagens da matriz de confusão não podem ser negativas.")

    @property
    def total_recuperados(self) -> int:
        return self.vp + self.fp

    @property
    def total_relevantes(self) -> int:
        return self.vp + self.fn

    @property
    def total_nao_relevantes(self) -> int:
        return self.fp + self.vn

    @property
    def total_documentos(self) -> int:
        return self.vp + self.vn + self.fp + self.fn

    @classmethod
    def de_resultados_binarios(
        cls,
        relevancias_recuperadas: Sequence[int | bool],
        total_relevantes: int,
        total_catalogo: int | None = None,
    ) -> "MatrizConfusao":
        """Cria a matriz a partir de uma lista recomendada (1=relevante, 0=não relevante).

        Ideal para o Exercício do Slide 10, onde cada posição recomendada é marcada como
        relevante (verde) ou não relevante (vermelho) e se conhece o total de relevantes.
        """
        for valor in relevancias_recuperadas:
            if valor not in (0, 1, False, True):
                raise ValueError("Os indicadores de relevância binária devem ser 0 ou 1.")

        vp = sum(1 for valor in relevancias_recuperadas if valor)
        fp = len(relevancias_recuperadas) - vp
        if total_relevantes < vp:
            raise ValueError(
                "total_relevantes não pode ser menor que os relevantes recuperados (VP)."
            )
        fn = total_relevantes - vp

        if total_catalogo is None:
            vn = 0
        else:
            vn = total_catalogo - (vp + fp + fn)
            if vn < 0:
                raise ValueError(
                    "total_catalogo é insuficiente para acomodar VP + FP + FN."
                )
        return cls(vp=vp, fp=fp, fn=fn, vn=vn)

    @classmethod
    def de_conjuntos(
        cls,
        itens_recuperados: Iterable[str],
        itens_relevantes: Iterable[str],
        catalogo_completo: Iterable[str] | None = None,
    ) -> "MatrizConfusao":
        """Cria a matriz comparando os identificadores recomendados com os relevantes."""
        rec = set(itens_recuperados)
        rel = set(itens_relevantes)
        vp = len(rec & rel)
        fp = len(rec - rel)
        fn = len(rel - rec)

        if catalogo_completo is None:
            vn = 0
        else:
            cat = set(catalogo_completo)
            if not (rec <= cat and rel <= cat):
                raise ValueError(
                    "Itens recuperados e relevantes devem pertencer ao catálogo completo."
                )
            vn = len(cat - (rec | rel))
        return cls(vp=vp, fp=fp, fn=fn, vn=vn)


def calcular_acuracia(vp: int, vn: int, fp: int, fn: int) -> float:
    """Porcentagem (fração entre 0 e 1) de documentos classificados corretamente (Slide 4)."""
    total = vp + vn + fp + fn
    if total <= 0:
        raise ValueError("O total de documentos deve ser maior que zero.")
    return (vp + vn) / total


def calcular_taxa_erro(vp: int, vn: int, fp: int, fn: int) -> float:
    """Fração de documentos classificados erroneamente pelo sistema (Slides 2 e 4)."""
    total = vp + vn + fp + fn
    if total <= 0:
        raise ValueError("O total de documentos deve ser maior que zero.")
    return (fp + fn) / total


def calcular_precisao(vp: int, fp: int) -> float:
    """Precision: fração de itens relevantes dentre os itens recuperados (Slides 3 e 4)."""
    recuperados = vp + fp
    if recuperados <= 0:
        raise ValueError("Não é possível calcular Precision sem itens recuperados (VP + FP = 0).")
    return vp / recuperados


def calcular_recall(vp: int, fn: int) -> float:
    """Recall: fração de itens relevantes recuperados dentre todos os relevantes (Slides 3 e 4)."""
    relevantes = vp + fn
    if relevantes <= 0:
        raise ValueError("Não é possível calcular Recall sem itens relevantes (VP + FN = 0).")
    return vp / relevantes


def calcular_f_measure(precisao: float, recall: float, beta: float = 1.0) -> float:
    """F-Measure (padrão F1 com beta=1.0): combina Precision e Recall (Slide 3)."""
    if beta <= 0:
        raise ValueError("O parâmetro beta deve ser positivo.")
    if not (0.0 <= precisao <= 1.0 and 0.0 <= recall <= 1.0):
        raise ValueError("Precision e Recall devem estar no intervalo [0, 1].")
    denominador = (beta**2 * precisao) + recall
    if denominador == 0.0:
        return 0.0
    return (1.0 + beta**2) * (precisao * recall) / denominador


@dataclass(frozen=True)
class ResumoClassificacao:
    """Reúne a matriz de confusão e as métricas derivadas."""

    matriz: MatrizConfusao
    precisao: float
    recall: float
    f1: float
    acuracia: float | None = None
    taxa_erro: float | None = None


def avaliar_classificacao(
    matriz: MatrizConfusao, incluir_acuracia: bool = True
) -> ResumoClassificacao:
    """Calcula Precision, Recall, F1 e (opcionalmente) Acurácia e Taxa de Erro."""
    precisao = calcular_precisao(matriz.vp, matriz.fp)
    recall = calcular_recall(matriz.vp, matriz.fn)
    f1 = calcular_f_measure(precisao, recall)
    acuracia = (
        calcular_acuracia(matriz.vp, matriz.vn, matriz.fp, matriz.fn)
        if incluir_acuracia
        else None
    )
    taxa_erro = (
        calcular_taxa_erro(matriz.vp, matriz.vn, matriz.fp, matriz.fn)
        if incluir_acuracia
        else None
    )
    return ResumoClassificacao(
        matriz=matriz,
        precisao=precisao,
        recall=recall,
        f1=f1,
        acuracia=acuracia,
        taxa_erro=taxa_erro,
    )
