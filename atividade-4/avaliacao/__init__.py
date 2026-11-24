"""Pacote modular de Métricas de Avaliação em Sistemas de Recomendação (Atividade 4)."""

from .classificacao import (
    MatrizConfusao,
    ResumoClassificacao,
    avaliar_classificacao,
    calcular_acuracia,
    calcular_f_measure,
    calcular_precisao,
    calcular_recall,
    calcular_taxa_erro,
)
from .dados import (
    ItemRanqueado,
    RegistroPredicao,
    carregar_predicoes_notas,
    carregar_rankings_usuarios,
)
from .erro import (
    ResumoErro,
    calcular_mae,
    calcular_mse,
    calcular_rmse,
    resumir_erros,
)
from .ranking import (
    PassoDCG,
    calcular_dcg,
    calcular_dcg_medio_usuarios,
    calcular_desconto_posicao,
    calcular_idcg,
    calcular_ndcg,
    calcular_ndcg_medio_usuarios,
    detalhar_dcg_posicoes,
)
from .roc import (
    PontoROC,
    calcular_auc_roc,
    calcular_curva_roc_ranking,
    calcular_fpr,
)

__all__ = [
    "ItemRanqueado",
    "MatrizConfusao",
    "PassoDCG",
    "PontoROC",
    "RegistroPredicao",
    "ResumoClassificacao",
    "ResumoErro",
    "avaliar_classificacao",
    "calcular_acuracia",
    "calcular_auc_roc",
    "calcular_curva_roc_ranking",
    "calcular_dcg",
    "calcular_dcg_medio_usuarios",
    "calcular_desconto_posicao",
    "calcular_f_measure",
    "calcular_fpr",
    "calcular_idcg",
    "calcular_mae",
    "calcular_mse",
    "calcular_ndcg",
    "calcular_ndcg_medio_usuarios",
    "calcular_precisao",
    "calcular_recall",
    "calcular_rmse",
    "calcular_taxa_erro",
    "carregar_predicoes_notas",
    "carregar_rankings_usuarios",
    "detalhar_dcg_posicoes",
    "resumir_erros",
]
