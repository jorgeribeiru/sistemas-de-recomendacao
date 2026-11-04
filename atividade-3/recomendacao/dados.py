from pathlib import Path

import pandas as pd


def carregar_catalogo() -> pd.DataFrame:
    """Carrega o catálogo de câmeras da atividade."""
    caminho = Path(__file__).resolve().parent.parent / "data" / "cameras.csv"
    return pd.read_csv(caminho).rename(columns={"price_eur": "price"}).set_index("id")
