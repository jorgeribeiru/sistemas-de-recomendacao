"""Exemplos literais extraídos dos slides de MetricasDeAvaliacao.pdf."""

# Slide 8 — Exemplo passo a passo de DCG (1º lugar: 3, 2º lugar: 2, 3º lugar: 3)
RANKING_SLIDE8: list[float] = [3.0, 2.0, 3.0]

# Slide 10 — Exercícios de Precision e Recall
# Legenda do slide: "Total Relevantes = [quadrado verde] x 20"
TOTAL_RELEVANTES_SLIDE10: int = 20

# Catálogo total adotado para ilustrar também VN, Acurácia e Taxa de Erro (Slide 4).
# Nota: Precision, Recall e F1 independem deste valor (usam apenas VP, FP e FN).
TOTAL_CATALOGO_SLIDE10: int = 50

# Recomendador 1 (posições 1 a 10):
# Vermelho=0 (não relevante), Verde=1 (relevante)
# Posições verdes no slide: 2, 3, 7, 8 e 10 -> 5 relevantes em 10 recuperados
RECOMENDADOR_1_SLIDE10: list[int] = [0, 1, 1, 0, 0, 0, 1, 1, 0, 1]

# Recomendador 2 (posições 1 a 5):
# Posições verdes no slide: 2, 4 e 5 -> 3 relevantes em 5 recuperados
RECOMENDADOR_2_SLIDE10: list[int] = [0, 1, 0, 1, 1]
