"""Leitura dos arquivos CSV didáticos da Atividade 4."""

import csv
from dataclasses import dataclass
from pathlib import Path

PASTA_DADOS = Path(__file__).resolve().parent.parent / "data"


@dataclass(frozen=True)
class RegistroPredicao:
    """Linha de data/predicoes_notas.csv comparando nota real e dois modelos."""

    user_id: str
    item_id: str
    title: str
    nota_real: float
    modelo_a: float
    modelo_b: float


@dataclass(frozen=True)
class ItemRanqueado:
    """Linha de data/rankings_usuarios.csv com posição, score e relevâncias."""

    user_id: str
    posicao: int
    item_id: str
    score_previsto: float
    relevancia_grau: float
    relevante_binario: int


def carregar_predicoes_notas(caminho: Path | None = None) -> list[RegistroPredicao]:
    """Carrega os pares de notas reais e previstas pelos Modelos A e B."""
    arquivo = caminho or (PASTA_DADOS / "predicoes_notas.csv")
    with arquivo.open(encoding="utf-8", newline="") as handle:
        leitor = csv.DictReader(handle)
        registros = [
            RegistroPredicao(
                user_id=linha["user_id"].strip(),
                item_id=linha["item_id"].strip(),
                title=linha["title"].strip(),
                nota_real=float(linha["nota_real"]),
                modelo_a=float(linha["modelo_a"]),
                modelo_b=float(linha["modelo_b"]),
            )
            for linha in leitor
        ]
    if not registros:
        raise ValueError(f"Nenhum registro encontrado em {arquivo}.")
    return registros


def carregar_rankings_usuarios(
    caminho: Path | None = None,
) -> dict[str, list[ItemRanqueado]]:
    """Carrega e ordena por posição os rankings recomendados de cada usuário."""
    arquivo = caminho or (PASTA_DADOS / "rankings_usuarios.csv")
    agrupado: dict[str, list[ItemRanqueado]] = {}
    with arquivo.open(encoding="utf-8", newline="") as handle:
        leitor = csv.DictReader(handle)
        for linha in leitor:
            item = ItemRanqueado(
                user_id=linha["user_id"].strip(),
                posicao=int(linha["posicao"]),
                item_id=linha["item_id"].strip(),
                score_previsto=float(linha["score_previsto"]),
                relevancia_grau=float(linha["relevancia_grau"]),
                relevante_binario=int(linha["relevante_binario"]),
            )
            agrupado.setdefault(item.user_id, []).append(item)

    if not agrupado:
        raise ValueError(f"Nenhum ranking encontrado em {arquivo}.")
    for usuario in agrupado:
        agrupado[usuario].sort(key=lambda r: r.posicao)
    return agrupado
