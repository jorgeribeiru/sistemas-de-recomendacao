# Atividade 4 — Métricas de avaliação

Implementação didática e modular das métricas de avaliação de Sistemas de Recomendação apresentadas em [MetricasDeAvaliacao.pdf](MetricasDeAvaliacao.pdf), utilizando apenas a biblioteca padrão do Python 3.10+.

## Executar

Na raiz do repositório:

```bash
python atividade-4/main.py
```

Para executar a suíte de testes unitários:

```bash
cd atividade-4
python -m unittest discover -v
```

## Métricas cobertas

1. **Classificação e recuperação Top-N (`avaliacao/classificacao.py`):**
   - Matriz de confusão: Verdadeiro Positivo (`VP`), Falso Positivo (`FP`), Falso Negativo (`FN`) e Verdadeiro Negativo (`VN`).
   - **Acurácia:** $(VP + VN) / (VP + VN + FP + FN)$
   - **Taxa de erro:** $(FP + FN) / (VP + VN + FP + FN)$
   - **Precision:** $VP / (VP + FP)$
   - **Recall:** $VP / (VP + FN)$
   - **F-Measure ($F_1$):** $2 \cdot (\text{Precision} \cdot \text{Recall}) / (\text{Precision} + \text{Recall})$
   - Resolução completa do **Exercício do Slide 10** (Recomendador 1 vs. Recomendador 2, com 20 itens relevantes na base).

2. **Erro de predição de notas (`avaliacao/erro.py`):**
   - **MAE (*Mean Absolute Error*):** média de $|y_i - \hat{y}_i|$.
   - **MSE (*Mean Square Error*):** média de $(y_i - \hat{y}_i)^2$.
   - **RMSE (*Root Mean Square Error*):** $\sqrt{\text{MSE}}$.
   - Comparação sobre `data/predicoes_notas.csv` mostrando por que dois modelos com o mesmo MAE (`0,50`) apresentam MSE e RMSE bem distintos quando um deles comete erros grandes.

3. **Ranking ponderado por posição (`avaliacao/ranking.py`):**
   - **DCG (*Discounted Cumulative Gain*):** usa o desconto posicional $\max(1, \log_2 p)$ definido no **Slide 8**, reproduzindo passo a passo o exemplo `[3, 2, 3]` ($\text{DCG} \approx 6{,}89$).
   - **IDCG e NDCG (*Normalized DCG*):** normalização pelo ranking ideal ($\text{DCG} / \text{IDCG} \in [0, 1]$), individual e médio entre múltiplos usuários (`data/rankings_usuarios.csv`).

4. **Curva ROC e AUC (`avaliacao/roc.py`):**
   - Evolução da Taxa de Verdadeiros Positivos ($\text{TPR} = \text{Recall}$) contra a Taxa de Falsos Positivos ($\text{FPR} = FP / (FP + VN)$) variando o corte/limiar de recomendação.
   - Cálculo da área sob a curva (**AUC-ROC**) pela regra do trapézio.

## Organização

- `main.py`: executa e apresenta todas as seções no terminal.
- `avaliacao/classificacao.py`: matriz de confusão, Acurácia, Taxa de Erro, Precision, Recall e F-Measure.
- `avaliacao/erro.py`: cálculos de MAE, MSE e RMSE.
- `avaliacao/ranking.py`: cálculos de DCG, IDCG e NDCG (por lista e multiusuário).
- `avaliacao/roc.py`: construção da curva ROC por corte/limiar e cálculo de AUC.
- `avaliacao/exemplos.py`: dados literais dos exemplos dos Slides 8 e 10.
- `avaliacao/dados.py`: leitura dos arquivos CSV em `data/`.
- `tests/test_avaliacao.py`: testes unitários validando gabaritos dos slides e casos de borda.

## Apresentação do código

Consulte o [roteiro de apresentação](APRESENTACAO.md) para explicar a ordem de execução, cada módulo, suas funções, variáveis e resultados exibidos no terminal.
