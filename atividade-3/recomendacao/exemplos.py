"""Requisitos e perfis usados nos exemplos dos slides."""

req_slide9 = {
    "c1": {"attr": "mpix", "op": ">=", "val": 10.0},
    "c2": {"attr": "price", "op": "<", "val": 300},
}

req_slide15_rest = {
    "r1": {"attr": "price", "op": "<=", "val": 150, "label": "price(€)"},
    "r2": {"attr": "opt_zoom", "op": "==", "val": 5, "label": "opt-zoom"},
    "r3": {"attr": "sound", "op": "==", "val": "yes", "label": "sound"},
    "r4": {"attr": "waterproof", "op": "==", "val": "yes", "label": "waterproof"},
}

regras_maut_slide17 = {
    "price": [
        {"op": "<=", "val": 250, "pontos": {"Quality": 5, "Economy": 10}},
        {"op": ">", "val": 250, "pontos": {"Quality": 10, "Economy": 5}},
    ],
    "mpix": [
        {"op": "<=", "val": 8.0, "pontos": {"Quality": 4, "Economy": 10}},
        {"op": ">", "val": 8.0, "pontos": {"Quality": 10, "Economy": 6}},
    ],
    "opt_zoom": [
        {"op": "<=", "val": 9, "pontos": {"Quality": 6, "Economy": 9}},
        {"op": ">", "val": 9, "pontos": {"Quality": 10, "Economy": 6}},
    ],
    "lcd_size": [
        {"op": "<=", "val": 2.7, "pontos": {"Quality": 6, "Economy": 10}},
        {"op": ">", "val": 2.7, "pontos": {"Quality": 9, "Economy": 5}},
    ],
    "movies": [
        {"op": "==", "val": "yes", "pontos": {"Quality": 10, "Economy": 7}},
        {"op": "==", "val": "no", "pontos": {"Quality": 3, "Economy": 10}},
    ],
    "sound": [
        {"op": "==", "val": "yes", "pontos": {"Quality": 10, "Economy": 8}},
        {"op": "==", "val": "no", "pontos": {"Quality": 7, "Economy": 10}},
    ],
    "waterproof": [
        {"op": "==", "val": "yes", "pontos": {"Quality": 10, "Economy": 6}},
        {"op": "==", "val": "no", "pontos": {"Quality": 8, "Economy": 10}},
    ],
}

perfis_clientes_slide18 = {
    "Cu1": {"Quality": 0.80, "Economy": 0.20},
    "Cu2": {"Quality": 0.40, "Economy": 0.60},
}

req_slide15_sim = {
    "price": {"tipo": "LIB", "peso": 1.0},
    "opt_zoom": {"tipo": "TARGET", "alvo": 5, "peso": 1.0},
    "sound": {"tipo": "CAT", "alvo": "yes", "peso": 1.0},
    "waterproof": {"tipo": "CAT", "alvo": "yes", "peso": 1.0},
}

req_mib_lib = {
    "mpix": {"tipo": "MIB", "peso": 0.6},
    "price": {"tipo": "LIB", "peso": 0.4},
}
