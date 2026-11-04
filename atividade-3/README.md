# Atividade 3 — recomendação baseada em conhecimento

## Base de dados

`data/cameras.csv` transcreve o catálogo de câmeras da página 7 do
[PDF fornecido](Recommender_Systems_An_Introduction_Chapter04_Knowledge-based_recommendation.pdf).
São oito câmeras, identificadas de P1 a P8.

O preço (`price_eur`) está em euros; `mpix` indica megapixels, `opt_zoom` é o
fator de zoom óptico e `lcd_size` é o tamanho da tela LCD conforme o slide.
Os campos `movies`, `sound` e `waterproof` preservam os valores `yes` e `no`
do material. O símbolo × foi omitido dos fatores de zoom para mantê-los
numéricos.

## Executar

O programa usa Python 3, NumPy e pandas. Com as dependências instaladas,
execute na raiz do repositório:

```bash
python atividade-3/main.py
```

O programa carrega o CSV e apresenta a consulta conjuntiva, os reparos de
requisitos e os rankings por utilidade multiatributo e similaridade.

## Organização

- `main.py`: executa e apresenta os exemplos.
- `recomendacao/dados.py`: carrega o catálogo de câmeras.
- `recomendacao/exemplos.py`: reúne os requisitos, regras e perfis dos slides.
- `recomendacao/consulta.py`: consulta conjuntiva e diagnóstico de reparos.
- `recomendacao/maut.py`: cálculo e ranking de utilidade multiatributo.
- `recomendacao/similaridade.py`: cálculo de similaridade baseada em casos.
- `recomendacao/operadores.py`: operadores relacionais compartilhados.

## Apresentação do código

Consulte o [roteiro de apresentação](APRESENTACAO.md) para explicar a ordem de
execução, cada função e suas variáveis, com exemplos da saída do programa.
