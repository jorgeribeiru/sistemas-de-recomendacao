# Sistemas de Recomendação

Repositório da disciplina de **Sistemas de Recomendação**, reunindo implementações didáticas, bases de dados e materiais de referência organizados progressivamente por atividade (`atividade-1/`, `atividade-2/`, …).

Cada pasta mantém seu próprio `README.md` com instruções detalhadas, parâmetros de execução e descrição dos dados. Este documento unifica a visão geral do repositório e acompanha a evolução da disciplina à medida que novas atividades são adicionadas.

## Atividades

| Atividade | Abordagem | Principais tópicos | Bases de dados | Dependências | Material |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [Atividade 1](atividade-1/README.md) | Recomendação colaborativa (baseada em usuários) | Similaridade de Pearson, vizinhos mais próximos (*k*-NN), previsão de notas e recomendação Top-N | `book`, `movies`, MovieLens 100K e CSV próprio | Biblioteca padrão | [Slides](atividade-1/Slide.pdf) · Cap. 2 |
| [Atividade 2](atividade-2/README.md) | Recomendação baseada em conteúdo | Matriz termo-documento, pesos TF-IDF e similaridade de cosseno (Shakespeare); carga de corpus textual (BBC) | Shakespeare (matriz do slide) e notícias BBC | Biblioteca padrão | [Slides Cap. 3](atividade-2/Recommender_Systems_An_Introduction_Chapter03_Content-based_recommendation.pdf) · Cap. 3 |
| [Atividade 3](atividade-3/README.md) | Recomendação baseada em conhecimento | Consultas conjuntivas, diagnóstico mínimo e reparo de requisitos, MAUT por perfil de cliente e similaridade baseada em casos (`LIB`, `MIB`, `TARGET`, `CAT`) | Catálogo de câmeras (`cameras.csv`) | `numpy`, `pandas` | [Slides Cap. 4](atividade-3/Recommender_Systems_An_Introduction_Chapter04_Knowledge-based_recommendation.pdf) · [Roteiro](atividade-3/APRESENTACAO.md) · Cap. 4 |
| [Atividade 4](atividade-4/README.md) | Avaliação de sistemas de recomendação | Matriz de confusão, Acurácia, Taxa de Erro, Precision, Recall, F-Measure, MAE, MSE, RMSE, DCG, NDCG e Curva ROC / AUC | Exercícios dos slides, `predicoes_notas.csv` e `rankings_usuarios.csv` | Biblioteca padrão | [Slides](atividade-4/MetricasDeAvaliacao.pdf) · [Roteiro](atividade-4/APRESENTACAO.md) · Cap. 7 |

> **Nota sobre a Atividade 2:** `atividade-2/main.py` faz a inspeção das bases (`shakespeare` e `bbc`), enquanto o cálculo de TF-IDF e a similaridade de cosseno para as peças de Shakespeare estão implementados em `atividade-2/content_based/`. A vetorização e o ranking sobre os textos completos da BBC permanecem como próximos passos.

## Requisitos e ambiente

- **Python 3.10 ou superior** em todas as atividades.
- **Atividades 1, 2 e 4:** utilizam apenas a biblioteca padrão do Python.
- **Atividade 3:** utiliza `numpy` e `pandas`:

```bash
pip install numpy pandas
```

## Execução rápida

Os comandos abaixo podem ser executados a partir da raiz do repositório. Para subcomandos, flags, formatos de CSV e detalhes das saídas, consulte o `README.md` de cada atividade.

### Atividade 1 — Recomendação colaborativa

```bash
python atividade-1/main.py
```

Para rodar os testes unitários:

```bash
cd atividade-1
python -m unittest discover -v
```

### Atividade 2 — Recomendação baseada em conteúdo

```bash
# Inspeção das bases disponíveis
python atividade-2/main.py

# Cálculo de TF-IDF e similaridade de cosseno (Shakespeare)
python atividade-2/content_based/tf-idf.py
python atividade-2/content_based/similarity.py
```

### Atividade 3 — Recomendação baseada em conhecimento

```bash
python atividade-3/main.py
```

### Atividade 4 — Métricas de avaliação

```bash
python atividade-4/main.py
```

Para rodar os testes unitários da Atividade 4:

```bash
cd atividade-4
python -m unittest discover -v
```

## Bases externas opcionais

Conjuntos de dados maiores ficam fora do versionamento (conforme [`.gitignore`](.gitignore)) e podem ser baixados sob demanda pelos scripts de cada atividade:

- **MovieLens 100K** (Atividade 1): `python atividade-1/scripts/download_movielens.py`
- **BBC News fulltext** (Atividade 2): `python atividade-2/scripts/download_bbc.py`

## Estrutura do repositório

O repositório segue um padrão modular por pasta para facilitar o acréscimo de novos exercícios ao longo da disciplina:

```text
sistemas-de-recomendacao/
├── README.md                      # Visão geral unificada da disciplina
├── Livro-RecommenderSystems.pdf   # Livro-texto de referência (Jannach et al.)
├── APRESENTACAO.md                # Roteiro de apresentação do código (Atividade 3)
├── atividade-1/                   # Recomendação colaborativa (CLI, pacotes, dados, scripts, testes)
├── atividade-2/                   # Recomendação baseada em conteúdo (dados, scripts, TF-IDF e cosseno)
├── atividade-3/                   # Recomendação baseada em conhecimento (catálogo, consulta, MAUT, similaridade)
└── atividade-4/                   # Métricas de avaliação (classificação, erro, DCG/NDCG, curva ROC e testes)
```

Ao adicionar uma nova atividade (`atividade-N/`), mantenha um `README.md` próprio dentro da pasta e atualize este arquivo incluindo uma linha na tabela de [Atividades](#atividades), eventuais novas dependências e o comando correspondente em **Execução rápida**.

## Referências

- **Livro-texto:** [Recommender Systems: An Introduction](Livro-RecommenderSystems.pdf) — os capítulos acompanham a progressão das atividades.
- **Materiais complementares:** slides de cada capítulo dentro da respectiva pasta `atividade-N/` e [roteiro de apresentação](atividade-3/APRESENTACAO.md) da Atividade 3.
