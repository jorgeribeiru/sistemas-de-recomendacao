# Roteiro de apresentação do código

Siga a ordem de execução: `main.py`, carregamento dos dados, consulta e reparos,
MAUT e similaridade. Ao apresentar cada função, mostre suas entradas, as variáveis
principais e o retorno. Execute `python atividade-3/main.py` para relacionar cada
etapa com a saída no terminal.

## 1. Entrada do programa: `main.py`

A função `main()` organiza os exemplos. Primeiro, `df_catalogo` recebe o catálogo
lido do CSV. Depois, a função chama as operações e imprime seus resultados:

- `consulta_slide9`: câmeras que atendem aos requisitos do slide 9.
- `resultado_req_completo`: resultado da consulta com os quatro requisitos do
  slide 15; neste exemplo, está vazio.
- `df_reparos`: tabela que mostra quais requisitos precisam ser revistos.
- `df_maut`: pontos, pontuações e posições de cada câmera por perfil.
- `df_sim_caso_a` e `df_sim_caso_b`: rankings para duas configurações de
  similaridade.

A condição `if __name__ == "__main__"` chama `main()` quando o arquivo é
executado diretamente. Os requisitos e pesos importados de `exemplos.py`
configuram os cálculos; as funções que os processam ficam nos outros módulos.

## 2. Leitura dos dados: `dados.py`

`carregar_catalogo()` monta em `caminho` o endereço de `data/cameras.csv`,
relativo ao próprio arquivo Python. `pd.read_csv(caminho)` lê os dados em um
DataFrame; `rename` muda `price_eur` para `price`, nome usado pelas regras; e
`set_index("id")` usa o identificador da câmera como índice. A função retorna
esse DataFrame. Assim, `item_id` nas funções seguintes será, por exemplo, `P1`.

## 3. Operadores e exemplos

Em `operadores.py`, o dicionário `OPERADORES` associa textos como `">="` e
`"<"` a funções de comparação do módulo `operator`. Assim, uma regra pode
informar o operador como texto, e o código busca a função correspondente.

Em `exemplos.py`, cada requisito de consulta tem `attr` (coluna), `op`
(operador) e `val` (valor de comparação). Por exemplo, `c1` compara `mpix`
com `10.0` usando `>=`. Os requisitos de reparo também podem ter `label`,
que define o nome da coluna na tabela exibida.

`regras_maut_slide17` reúne as regras de pontuação por atributo;
`perfis_clientes_slide18` define os pesos de qualidade e economia para cada
cliente. `req_slide15_sim` e `req_mib_lib` definem os atributos, tipos e pesos
usados na similaridade.

## 4. Consulta conjuntiva: `executar_consulta_conjuntiva`

Entradas: `df`, o catálogo, e `requisitos`, um dicionário de condições. Retorno:
um DataFrame contendo somente as linhas que satisfazem todas as condições.

1. `mascaras` começa como uma lista vazia. Cada máscara indica, com `True` ou
   `False`, quais linhas atendem a uma condição.
2. O laço percorre `requisitos.values()`. A variável `configuracao` recebe o
   dicionário de uma condição, sem precisar do identificador `c1`, `c2` etc.
3. `comparar` recebe a função de `OPERADORES` correspondente a `op`. Ela é
   aplicada à coluna `df[configuracao["attr"]]` e ao valor `configuracao["val"]`.
   O resultado é adicionado a `mascaras`.
4. `np.logical_and.reduce(mascaras)` combina as máscaras com E lógico e guarda
   o resultado em `mascara_conjuntiva`.
5. `df[mascara_conjuntiva]` retorna as linhas selecionadas. No exemplo de
   10 MP ou mais e preço abaixo de €300, são P4 e P7.

## 5. Diagnóstico: `diagnosticar_e_gerar_reparos`

Entradas: `df`, `requisitos` e o dicionário opcional `formatadores`, usado para
exibir valores como `5x`. O retorno é uma tabela de itens e requisitos a rever.
A função pode ser chamada independentemente, mas o exemplo a apresenta depois
de uma consulta sem resultados.

1. `candidatos` reúne os dados de cada câmera. `df.iterrows()` fornece
   `item_id` (índice) e `item` (linha). Para cada requisito, `requisito_id` é
   seu nome e `configuracao` contém atributo, operador e valor.
2. `comparar` testa a condição. Se ela falhar, o nome do requisito entra na
   lista `violacoes`. Cada candidato guarda seu ID, as violações como conjunto
   e a mesma lista na ordem original.
3. `conjuntos_violacoes` reúne os conjuntos de todos os candidatos. A variável
   `diagnosticos_minimos` mantém aqueles para os quais nenhum outro conjunto é
   um subconjunto estrito. Isso significa mínimo por inclusão, não apenas menor
   quantidade de violações. Conjuntos iguais podem aparecer em mais de um item.
4. `ordem_requisitos` ajuda a ordenar a apresentação: primeiro pela quantidade
   de violações e depois pela ordem em que os requisitos foram declarados.
5. Para cada `candidato` mínimo, `numero` numera a linha, `diagnostico` monta
   o texto com os requisitos violados e `linha` guarda o resultado. Para cada
   `atributo`, `nome_coluna` define o cabeçalho; se houve violação, `valor` é
   formatado com `formato`; caso contrário, a célula recebe `✓`.
6. As linhas são acumuladas em `reparos` e convertidas em DataFrame. Por
   exemplo, P2 viola `r1` e `r4`: preço e resistência à água.

## 6. Utilidade multiatributo: `calcular_maut_generico`

Entradas: `df`, `regras_dimensoes` e `perfis_clientes`. Retorno: DataFrame com
pontos por dimensão, pontuação e posição de cada câmera para cada cliente.

1. `nomes_dimensoes` obtém as dimensões da primeira regra, como `Quality` e
   `Economy`. `resultados` acumula uma linha por câmera.
2. Para cada `item_id` e `item`, `pontos_por_dimensao` começa com zero em cada
   dimensão. O laço percorre cada `atributo` e sua `lista_regras`.
3. `valor_item` é o valor da câmera naquele atributo. Para cada `regra`,
   `comparar` verifica a condição; quando ela é satisfeita, os `pontos` são
   somados à respectiva `dimensao`. O `break` impede que outras regras do mesmo
   atributo sejam aplicadas.
4. `resultado_item` começa com o ID e os totais. Para cada `cliente`, a
   `pontuacao` é a soma de cada total multiplicado pelo peso correspondente em
   `pesos`. O resultado arredondado entra em `resultados`.
5. `ranking` é o DataFrame criado a partir dos resultados. `rank` atribui as
   posições em ordem decrescente; `method="first"` desempata pela ordem das
   linhas. Por exemplo, Cu1 dá à P8 a pontuação `69 × 0,8 + 43 × 0,2 = 63,8`.

## 7. Similaridade: `calcular_similaridade_casos`

Entradas: `df` e `requisitos_sim`, que informa tipo, peso e, quando necessário,
alvo para cada atributo. Retorno: DataFrame ordenado pela similaridade final.

1. `resultados` acumula as linhas. Para cada `item_id` e `item`, começam em
   zero `soma_ponderada` e `soma_pesos`; `detalhes` armazenará as notas.
2. Para cada `atributo`, `configuracao` fornece `tipo`, `peso` e `alvo`;
   `valor_item` é o valor da câmera. Nos tipos numéricos, `valor_minimo` e
   `valor_maximo` vêm do catálogo e `amplitude` é a diferença entre eles. Se
   forem iguais, a amplitude usada é 1 para evitar divisão por zero.
3. A variável `similaridade` recebe a nota conforme o tipo:
   - `LIB`: favorece valores menores, como preço.
   - `MIB`: favorece valores maiores, como resolução.
   - `TARGET`: favorece proximidade com o alvo numérico.
   - `CAT`: vale 1 quando o valor é igual ao alvo e 0 caso contrário.
4. A nota vezes o `peso` entra em `soma_ponderada`; o peso entra em
   `soma_pesos`. A nota arredondada vai para `detalhes`.
5. `pontuacao_final` divide a soma ponderada pela soma dos pesos, quando esta
   é positiva; caso contrário, recebe zero. O código monta `ranking` e o ordena
   pela coluna `Similarity_Score`. No exemplo de resolução e preço, P4 fica em
   primeiro com 0,8523.
