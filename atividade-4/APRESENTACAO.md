# Roteiro de apresentação do código

Siga a ordem de execução de `main.py`: classificação (Slide 10), métricas de erro de predição (Slides 5–7), métricas de ranking ponderado (Slides 8–9) e curva ROC/AUC (Slide 9). Execute `python atividade-4/main.py` para acompanhar cada bloco no terminal.

## 1. Entrada do programa: `main.py`

A função `main()` divide a demonstração em quatro funções independentes, cada uma associada a um módulo do pacote `avaliacao/`:

- `exibir_secao_classificacao()`: resolve o exercício visual do Slide 10 comparando o Recomendador 1 (10 itens) e o Recomendador 2 (5 itens).
- `exibir_secao_erros()`: lê `data/predicoes_notas.csv` e compara o Modelo A (pequenos desvios constantes) com o Modelo B (poucos erros, porém grandes) em MAE, MSE e RMSE.
- `exibir_secao_ranking()`: reproduz a memória de cálculo do Slide 8 (`[3, 2, 3]`) e calcula DCG@5, IDCG@5 e NDCG@5 individual e médio para os usuários de `data/rankings_usuarios.csv`.
- `exibir_secao_roc()`: mostra corte a corte os valores de `VP`, `FP`, `FN`, `VN`, `FPR` e `TPR` e compara a área sob a curva (`AUC-ROC`) entre perfis de recomendação.

## 2. Exemplos e leitura dos dados: `exemplos.py` e `dados.py`

- Em `exemplos.py`:
  - `TOTAL_RELEVANTES_SLIDE10 = 20` representa os 20 itens relevantes indicados na figura do Slide 10.
  - `RECOMENDADOR_1_SLIDE10` e `RECOMENDADOR_2_SLIDE10` transcrevem as cores dos quadrados em sequências de `0` (vermelho, não relevante) e `1` (verde, relevante).
  - `TOTAL_CATALOGO_SLIDE10 = 50` define um tamanho de acervo ilustrativo para demonstrar também `VN`, `Acurácia` e `Taxa de Erro` (lembrando que `Precision`, `Recall` e `F1` dependem apenas de `VP`, `FP` e `FN`).
  - `RANKING_SLIDE8 = [3.0, 2.0, 3.0]` guarda os graus de relevância do Slide 8.
- Em `dados.py`:
  - `carregar_predicoes_notas()` lê `data/predicoes_notas.csv` e devolve objetos `RegistroPredicao`.
  - `carregar_rankings_usuarios()` lê `data/rankings_usuarios.csv`, agrupa os itens por `user_id` e os ordena pela coluna `posicao`.

## 3. Classificação e recuperação: `classificacao.py`

1. A classe `MatrizConfusao` guarda `vp`, `fp`, `fn` e `vn`:
   - `de_resultados_binarios(relevancias_recuperadas, total_relevantes, total_catalogo)` soma os `1` para obter `vp`, usa os demais recuperados como `fp`, calcula `fn = total_relevantes - vp` e, quando há `total_catalogo`, obtém `vn`.
   - `de_conjuntos(itens_recuperados, itens_relevantes, catalogo_completo)` monta a mesma matriz a partir de conjuntos de IDs de itens.
2. Funções das métricas (Slides 2, 3 e 4):
   - `calcular_acuracia`: `(vp + vn) / total`.
   - `calcular_taxa_erro`: `(fp + fn) / total` (complementar da acurácia).
   - `calcular_precisao`: `vp / (vp + fp)` — no Slide 10, Recomendador 1 obtém `5/10 = 50%` e Recomendador 2 obtém `3/5 = 60%`.
   - `calcular_recall`: `vp / (vp + fn)` — no Slide 10, Recomendador 1 obtém `5/20 = 25%` e Recomendador 2 obtém `3/20 = 15%`.
   - `calcular_f_measure`: combina Precision e Recall pela média harmônica ponderada por `beta` (padrão `beta = 1.0`, gerando `F1 = 33,33%` para o Recomendador 1 e `24,00%` para o Recomendador 2).

## 4. Erro de predição de notas: `erro.py`

Entradas: sequências `reais` ($y_i$) e `previstos` ($\hat{y}_i$) de mesmo tamanho, validadas por `_validar_pares`.

1. `calcular_mae`: soma `abs(y - y_hat)` e divide por `n` (Slide 5).
2. `calcular_mse`: soma `(y - y_hat) ** 2` e divide por `n` (Slide 6).
3. `calcular_rmse`: extrai `sqrt(calcular_mse(...))`, voltando para a mesma unidade da nota (Slide 7).
4. `resumir_erros`: reúne `mae`, `mse`, `rmse`, a tupla `erros` e `maior_erro_absoluto`. Na base `predicoes_notas.csv`, tanto o Modelo A (8 desvios de `0,5`) quanto o Modelo B (6 acertos exatos e 2 erros de `2,0`) têm `MAE = 0,5000`, mas o Modelo B salta para `MSE = 1,0000` e `RMSE = 1,0000` contra `0,2500` e `0,5000` do Modelo A.

## 5. Ranking ponderado por posição: `ranking.py`

1. `calcular_desconto_posicao(posicao)` aplica `max(1.0, log2(posicao))`, fiel à equação do Slide 8: posições `p = 1` e `p = 2` têm divisor `1,0`, e a partir de `p = 3` o ganho sofre desconto logarítmico.
2. `detalhar_dcg_posicoes(relevancias, k)` devolve objetos `PassoDCG` com `posicao`, `relevancia`, `desconto` e `ganho_descontado`. Para `[3, 2, 3]`, produz `3,00`, `2,00` e `1,89`, somando `DCG = 6,8928` (`~6,89` no slide).
3. `calcular_idcg(relevancias_ideais, k)` ordena as relevâncias em ordem decrescente (`[3, 3, 2]`, `IDCG = 7,2619`) e `calcular_ndcg` divide `DCG / IDCG` (`0,9492`).
4. `calcular_dcg_medio_usuarios` e `calcular_ndcg_medio_usuarios` calculam a média aritmética entre os $U$ usuários conforme o somatório externo do Slide 8.

## 6. Curva ROC e AUC: `roc.py`

1. `calcular_curva_roc_ranking` parte da origem `(FPR = 0, TPR = 0)` com `corte = 0` e percorre a lista ordenada por `scores_ordenados` acumulando `vp_acumulado` e `fp_acumulado` a cada limiar.
2. Em cada ponto, `tpr` usa `calcular_recall(vp, fn)` e `fpr` usa `calcular_fpr(fp, vn) = fp / (fp + vn)`.
3. `calcular_auc_roc(pontos_roc)` soma a área dos trapézios entre pontos consecutivos: `(atual.fpr - anterior.fpr) * (anterior.tpr + atual.tpr) / 2`. No exemplo, `u2` atinge `AUC = 1,0000` (separação perfeita), `u1` atinge `0,8125` e `u3` fica em `0,3750`.
