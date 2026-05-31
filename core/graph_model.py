#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any


NODES: list[tuple[int, str, str, int, str]] = [
    (0,  'Marte_Inicial',          'Estado Inicial',   0,     'Ponto de partida — Marte sem qualquer intervenção humana'),
    (1,  'Missao_Reconhecimento',  'Preparacao',        50,   'Missão orbital e superficial de reconhecimento inicial'),
    (2,  'Satelite_Mapeamento',    'Preparacao',        80,   'Constelação de satélites para mapeamento geológico detalhado'),
    (3,  'Gerador_Nuclear_Alpha',  'Energia',           500,  'Primeiro reator nuclear de fissão instalado em superfície'),
    (4,  'Gerador_Nuclear_Beta',   'Energia',           450,  'Segundo reator + rede de distribuição de energia'),
    (5,  'Espelho_Solar_Orbital',  'Energia',           800,  'Espelhos orbitais para amplificação do fluxo solar'),
    (6,  'Aquecimento_Fase1',      'Atmosfera',        1200,  'Aumento de temperatura de -60°C para -30°C'),
    (7,  'Liberacao_CO2_Norte',    'Atmosfera',         600,  'Liberação de CO2 das calotas polares norte via calor'),
    (8,  'Liberacao_CO2_Sul',      'Atmosfera',         700,  'Liberação de CO2 das calotas polares sul via calor'),
    (9,  'Pressao_1pct',           'Atmosfera',         900,  'Pressão atmosférica: 1% da Terra (≈ 1 kPa)'),
    (10, 'Pressao_5pct',           'Atmosfera',        1500,  'Pressão atmosférica: 5% da Terra (≈ 5 kPa)'),
    (11, 'Pressao_20pct',          'Atmosfera',        3000,  'Pressão atmosférica: 20% da Terra (≈ 20 kPa)'),
    (12, 'Campo_Magnetico',        'Protecao',         2000,  'Campo magnético artificial via dipolo no ponto L1 Terra-Sol'),
    (13, 'Escudo_Radiacao',        'Protecao',          400,  'Escudos localizados de radiação nas zonas habitadas'),
    (14, 'Aquecimento_Fase2',      'Temperatura',      2500,  'Aumento de temperatura de -30°C até 0°C'),
    (15, 'Derretimento_Calotas',   'Agua',             1800,  'Derretimento das calotas polares de gelo de água'),
    (16, 'Reservatorio_Norte',     'Agua',              300,  'Formação de reservatório líquido na região polar norte'),
    (17, 'Reservatorio_Sul',       'Agua',              350,  'Formação de reservatório líquido na região polar sul'),
    (18, 'Rede_Hidrologica',       'Agua',              600,  'Rede hidrológica básica conectando reservatórios'),
    (19, 'Cianobacterias_Alpha',   'Biologia',          200,  'Introdução de cianobactérias resistentes a radiação UV'),
    (20, 'Cianobacterias_Beta',    'Biologia',          400,  'Expansão em larga escala das colônias de cianobactérias'),
    (21, 'Producao_O2_Inicial',    'Biologia',          100,  'Início mensurável de produção biológica de O2'),
    (22, 'Liquens_Pioneiros',      'Biologia',          300,  'Introdução de líquens e musgos extremófilos'),
    (23, 'Solo_Basico',            'Biologia',          500,  'Formação de solo básico cultivável via decomposição biológica'),
    (24, 'Habitat_Alpha',          'Colonizacao',      1500,  'Primeiro habitat pressurizado permanente (Dome Alpha)'),
    (25, 'Habitat_Beta',           'Colonizacao',      1200,  'Segunda base habitável conectada ao Habitat Alpha'),
    (26, 'Agricultura_Basica',     'Colonizacao',       600,  'Agricultura básica em ambiente controlado (indoor farming)'),
    (27, 'Colonizacao_100',        'Colonizacao',       200,  'Colônia humana de 100 pessoas permanentemente estabelecida'),
    (28, 'Plantas_Superiores',     'Expansao',          800,  'Introdução de árvores e plantas superiores ao solo marciano'),
    (29, 'O2_10pct',               'Expansao',         2000,  'O2 atmosférico atinge 10% (pressão parcial ≈ 2 kPa)'),
    (30, 'Ciclo_Hidrologico',      'Expansao',         1500,  'Ciclo hidrológico básico funcionando (evaporação + chuva)'),
    (31, 'Controle_Tempestades',   'Expansao',          700,  'Sistema de controle e atenuação de tempestades de areia'),
    (32, 'Industria_Local',        'Expansao',         1000,  'Indústria local de produção, manutenção e extração de recursos'),
    (33, 'Colonizacao_10000',      'Expansao',          500,  'Colônia humana de 10.000 pessoas — autossuficiência parcial'),
    (34, 'O2_21pct',               'Terraformacao',    5000,  'O2 atinge 21% — atmosfera respirável sem traje espacial'),
    (35, 'Pressao_Habitavel',      'Terraformacao',    4000,  'Pressão habitável sem traje (101 kPa — equivalente à Terra)'),
    (36, 'Temperatura_Positiva',   'Terraformacao',    3500,  'Temperatura média positiva entre +10°C e +20°C'),
    (37, 'Ecossistema_Sustentavel','Terraformacao',    2500,  'Ecossistema planetário auto-sustentável estabelecido'),
    (38, 'Marte_Habitavel',        'Objetivo Final',      0,  'MARTE TERRAFORMADO — Planeta plenamente habitável pela humanidade'),
]

EDGES: list[tuple[str, str, int]] = [
    ('Marte_Inicial',         'Missao_Reconhecimento',  50),
    ('Marte_Inicial',         'Satelite_Mapeamento',    80),
    ('Missao_Reconhecimento', 'Gerador_Nuclear_Alpha',  500),
    ('Satelite_Mapeamento',   'Gerador_Nuclear_Alpha',  500),
    ('Gerador_Nuclear_Alpha', 'Gerador_Nuclear_Beta',   450),
    ('Gerador_Nuclear_Alpha', 'Espelho_Solar_Orbital',  800),
    ('Gerador_Nuclear_Alpha', 'Aquecimento_Fase1',      1200),
    ('Gerador_Nuclear_Beta',  'Liberacao_CO2_Norte',    600),
    ('Gerador_Nuclear_Beta',  'Liberacao_CO2_Sul',      700),
    ('Espelho_Solar_Orbital', 'Aquecimento_Fase1',      1200),
    ('Aquecimento_Fase1',     'Liberacao_CO2_Norte',    600),
    ('Aquecimento_Fase1',     'Liberacao_CO2_Sul',      700),
    ('Liberacao_CO2_Norte',   'Pressao_1pct',           900),
    ('Liberacao_CO2_Sul',     'Pressao_1pct',           900),
    ('Pressao_1pct',          'Pressao_5pct',           1500),
    ('Pressao_1pct',          'Campo_Magnetico',        2000),
    ('Pressao_5pct',          'Pressao_20pct',          3000),
    ('Pressao_5pct',          'Escudo_Radiacao',        400),
    ('Campo_Magnetico',       'Aquecimento_Fase2',      2500),
    ('Campo_Magnetico',       'Derretimento_Calotas',   1800),
    ('Escudo_Radiacao',       'Habitat_Alpha',          1500),
    ('Aquecimento_Fase2',     'Derretimento_Calotas',   1800),
    ('Aquecimento_Fase2',     'Temperatura_Positiva',   3500),
    ('Derretimento_Calotas',  'Reservatorio_Norte',     300),
    ('Derretimento_Calotas',  'Reservatorio_Sul',       350),
    ('Reservatorio_Norte',    'Rede_Hidrologica',       600),
    ('Reservatorio_Sul',      'Rede_Hidrologica',       600),
    ('Pressao_20pct',         'Cianobacterias_Alpha',   200),
    ('Rede_Hidrologica',      'Cianobacterias_Alpha',   200),
    ('Cianobacterias_Alpha',  'Cianobacterias_Beta',    400),
    ('Cianobacterias_Beta',   'Producao_O2_Inicial',    100),
    ('Cianobacterias_Beta',   'Liquens_Pioneiros',      300),
    ('Producao_O2_Inicial',   'Liquens_Pioneiros',      300),
    ('Liquens_Pioneiros',     'Solo_Basico',            500),
    ('Solo_Basico',           'Agricultura_Basica',     600),
    ('Solo_Basico',           'Plantas_Superiores',     800),
    ('Habitat_Alpha',         'Habitat_Beta',           1200),
    ('Habitat_Alpha',         'Colonizacao_100',        200),
    ('Habitat_Beta',          'Colonizacao_100',        200),
    ('Agricultura_Basica',    'Colonizacao_100',        200),
    ('Colonizacao_100',       'Industria_Local',        1000),
    ('Industria_Local',       'Colonizacao_10000',      500),
    ('Plantas_Superiores',    'O2_10pct',               2000),
    ('Producao_O2_Inicial',   'O2_10pct',               2000),
    ('Rede_Hidrologica',      'Ciclo_Hidrologico',      1500),
    ('Plantas_Superiores',    'Ciclo_Hidrologico',      1500),
    ('Pressao_20pct',         'Controle_Tempestades',   700),
    ('O2_10pct',              'O2_21pct',               5000),
    ('Pressao_20pct',         'Pressao_Habitavel',      4000),
    ('Ciclo_Hidrologico',     'Temperatura_Positiva',   3500),
    ('O2_21pct',              'Ecossistema_Sustentavel', 2500),
    ('Pressao_Habitavel',     'Ecossistema_Sustentavel', 2500),
    ('Temperatura_Positiva',  'Ecossistema_Sustentavel', 2500),
    ('Controle_Tempestades',  'Ecossistema_Sustentavel', 2500),
    ('Ecossistema_Sustentavel','Marte_Habitavel',       0),
    ('Colonizacao_10000',     'Marte_Habitavel',        0),
]

_NODE_MAP: dict[str, tuple[int, str, str, int, str]] = {
    node[1]: node for node in NODES
}

FASES_ORDEM: list[str] = [
    'Estado Inicial', 'Preparacao', 'Energia', 'Atmosfera',
    'Protecao', 'Temperatura', 'Agua', 'Biologia',
    'Colonizacao', 'Expansao', 'Terraformacao', 'Objetivo Final',
]

COR_FASE: dict[str, str] = {
    'Estado Inicial': '#6366F1',
    'Preparacao':     '#0EA5E9',
    'Energia':        '#F59E0B',
    'Atmosfera':      '#10B981',
    'Protecao':       '#8B5CF6',
    'Temperatura':    '#EF4444',
    'Agua':           '#0EA5E9',
    'Biologia':       '#10B981',
    'Colonizacao':    '#EC4899',
    'Expansao':       '#14B8A6',
    'Terraformacao':  '#F97316',
    'Objetivo Final': '#6366F1',
}

RISCO_FASE: dict[str, float] = {
    'Estado Inicial': 0.0,
    'Preparacao':     1.0,
    'Energia':        3.0,
    'Atmosfera':      2.5,
    'Protecao':       4.0,
    'Temperatura':    3.5,
    'Agua':           2.0,
    'Biologia':       3.0,
    'Colonizacao':    2.5,
    'Expansao':       3.5,
    'Terraformacao':  5.0,
    'Objetivo Final': 0.0,
}


def obter_fase(nome_no: str) -> str:
    if nome_no not in _NODE_MAP:
        raise KeyError(f"Vértice '{nome_no}' não encontrado no grafo.")
    return _NODE_MAP[nome_no][2]


def obter_custo_ativacao(nome_no: str) -> int:
    if nome_no not in _NODE_MAP:
        raise KeyError(f"Vértice '{nome_no}' não encontrado no grafo.")
    return _NODE_MAP[nome_no][3]


def obter_descricao(nome_no: str) -> str:
    if nome_no not in _NODE_MAP:
        raise KeyError(f"Vértice '{nome_no}' não encontrado no grafo.")
    return _NODE_MAP[nome_no][4]


def construir_grafo(criterio: str = 'energia') -> dict[str, list[tuple[float, str]]]:
    criterios_validos = ('energia', 'etapas', 'risco')
    if criterio not in criterios_validos:
        raise ValueError(
            f"Critério '{criterio}' inválido. Use: {criterios_validos}"
        )

    grafo: dict[str, list[tuple[float, str]]] = {}

    for _, nome, _, _, _ in NODES:
        grafo[nome] = []

    for origem, destino, custo_tj in EDGES:
        if criterio == 'energia':
            peso = float(custo_tj)
        elif criterio == 'etapas':
            peso = 1.0
        elif criterio == 'risco':
            fase_destino = obter_fase(destino)
            peso = float(custo_tj) * RISCO_FASE.get(fase_destino, 1.0)
        else:
            peso = float(custo_tj)

        grafo[origem].append((peso, destino))

    return grafo


def validar_grafo(grafo: dict[str, list[tuple[float, str]]]) -> bool:
    if 'Marte_Inicial' not in grafo or 'Marte_Habitavel' not in grafo:
        return False

    for no, vizinhos in grafo.items():
        for custo, _ in vizinhos:
            if custo < 0:
                return False

    BRANCO, CINZA, PRETO = 0, 1, 2
    cores: dict[str, int] = {no: BRANCO for no in grafo}

    def dfs_ciclo(no: str) -> bool:
        cores[no] = CINZA
        for _, vizinho in grafo.get(no, []):
            if cores.get(vizinho) == CINZA:
                return True
            if cores.get(vizinho) == BRANCO and dfs_ciclo(vizinho):
                return True
        cores[no] = PRETO
        return False

    for no in grafo:
        if cores[no] == BRANCO:
            if dfs_ciclo(no):
                return False

    visitados: set[str] = set()
    fila = ['Marte_Inicial']
    while fila:
        atual = fila.pop(0)
        if atual in visitados:
            continue
        visitados.add(atual)
        for _, vizinho in grafo.get(atual, []):
            if vizinho not in visitados:
                fila.append(vizinho)

    if 'Marte_Habitavel' not in visitados:
        return False

    return True


def obter_detalhes_etapas(caminho: list[str]) -> list[dict[str, Any]]:
    detalhes: list[dict[str, Any]] = []
    custo_acumulado = 0

    aresta_custo: dict[tuple[str, str], int] = {}
    for origem, destino, custo in EDGES:
        aresta_custo[(origem, destino)] = custo

    for i, nome in enumerate(caminho):
        custo_transicao = 0
        if i > 0:
            custo_transicao = aresta_custo.get((caminho[i - 1], nome), 0)
        custo_acumulado += custo_transicao

        detalhes.append({
            'etapa': i,
            'nome': nome,
            'fase': obter_fase(nome),
            'custo_ativacao': obter_custo_ativacao(nome),
            'custo_transicao': custo_transicao,
            'custo_acumulado': custo_acumulado,
            'descricao': obter_descricao(nome),
        })

    return detalhes


def obter_unidade(criterio: str) -> str:
    unidades = {
        'energia': 'TeraJoules (TJ)',
        'etapas': 'Etapas',
        'risco': 'Índice de Risco (TJ × fator)',
    }
    return unidades.get(criterio, 'TeraJoules (TJ)')


def obter_todos_vertices() -> list[str]:
    return [node[1] for node in NODES]


def grafo_para_json() -> dict[str, Any]:
    vertices = []
    for nid, nome, fase, custo, descricao in NODES:
        vertices.append({
            'id': nid,
            'nome': nome,
            'fase': fase,
            'custo_ativacao': custo,
            'descricao': descricao,
            'cor': COR_FASE.get(fase, '#6366F1'),
        })

    arestas = []
    for origem, destino, custo in EDGES:
        arestas.append({
            'origem': origem,
            'destino': destino,
            'custo': custo,
        })

    return {
        'vertices': vertices,
        'arestas': arestas,
        'total_vertices': len(vertices),
        'total_arestas': len(arestas),
        'fases': FASES_ORDEM,
    }
