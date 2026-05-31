#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any, Optional
import networkx as nx
import plotly.graph_objects as go

from core.graph_model import (
    NODES, COR_FASE, FASES_ORDEM,
    obter_fase, obter_detalhes_etapas
)

def gerar_posicoes_por_fase(G: nx.DiGraph) -> dict[str, tuple[float, float]]:
    nos_por_fase: dict[str, list[str]] = {}
    for node in G.nodes():
        try:
            fase = obter_fase(node)
        except KeyError:
            fase = 'Desconhecida'
        if fase not in nos_por_fase:
            nos_por_fase[fase] = []
        nos_por_fase[fase].append(node)

    pos: dict[str, tuple[float, float]] = {}

    for fase_idx, fase in enumerate(FASES_ORDEM):
        nos = nos_por_fase.get(fase, [])
        if not nos:
            continue

        x = fase_idx * 20.0
        num_nos = len(nos)
        
        y_start = (num_nos - 1) * 12.0 / 2.0
        
        for i, no in enumerate(nos):
            y = y_start - (i * 12.0)
            pos[no] = (x, y)

    return pos


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"rgba({r}, {g}, {b}, {alpha})"
    return hex_color

def plot_grafo_plotly(
    grafo_dict: dict[str, list[tuple[float, str]]],
    caminho_otimo: Optional[list[str]] = None,
) -> str:
    G = nx.DiGraph()

    for _, nome, _, _, _ in NODES:
        G.add_node(nome)

    for no, vizinhos in grafo_dict.items():
        for custo, vizinho in vizinhos:
            G.add_edge(no, vizinho, weight=custo)

    pos = gerar_posicoes_por_fase(G)
    
    edges_caminho = []
    if caminho_otimo and len(caminho_otimo) > 1:
        edges_caminho = list(zip(caminho_otimo, caminho_otimo[1:]))

    annotations = []
    path_color = '#ef4444' 
    edge_color = '#333333'

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        is_path = caminho_otimo and (edge in edges_caminho)
        
        width = 2.5 if is_path else 1.0
        color = path_color if is_path else edge_color
        alpha = 1.0 if is_path else 0.4
        
        annotations.append(dict(
            ax=x0, ay=y0,
            x=x1, y=y1,
            xref='x', yref='y',
            axref='x', ayref='y',
            showarrow=True,
            arrowhead=2 if not is_path else 4,
            arrowsize=1.2,
            arrowwidth=width,
            arrowcolor=color,
            opacity=alpha,
            standoff=18, 
            startstandoff=18
        ))

    node_x = []
    node_y = []
    node_hover = []
    node_customdata = []
    node_text = []
    node_colors = []
    node_borders = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        is_path = (caminho_otimo and (node in caminho_otimo)) or not caminho_otimo
        is_in_path_strictly = caminho_otimo and (node in caminho_otimo)
        
        try:
            fase_no = obter_fase(node)
        except ValueError:
            fase_no = 'ESTADO INICIAL'
            
        cor_no = COR_FASE.get(fase_no, '#ffffff')
        
        detalhes = obter_detalhes_etapas([node])
        desc = detalhes[0]['descricao'] if detalhes else ''
        custo = detalhes[0]['custo_ativacao'] if detalhes else 0
        
        hover_text = f"<b>{node.replace('_', ' ')}</b><br>Fase: {fase_no}<br>Custo: {custo} TJ<br><br><i>{desc}</i>"
        node_hover.append(hover_text)
        node_customdata.append([node, fase_no, custo, desc, cor_no])
        node_text.append(node.replace('_', ' '))
        
        bg_color = hex_to_rgba(cor_no, 0.4) if not is_in_path_strictly else cor_no
        borda = cor_no if is_in_path_strictly else '#444444'
        
        if not is_path:
            bg_color = 'rgba(20,20,20,0.5)'
            borda = '#222222'

        node_colors.append(bg_color)
        node_borders.append(borda)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition='bottom center',
        textfont=dict(color='#cccccc', size=11, family='monospace'),
        hoverinfo='text',
        hovertext=node_hover,
        customdata=node_customdata,
        marker=dict(
            size=28,
            color=node_colors,
            line=dict(width=2.5, color=node_borders)
        ),
        showlegend=False
    )

    fig = go.Figure(
        data=[node_trace],
        layout=go.Layout(
            width=2000,
            height=600,
            dragmode='pan',
            showlegend=False,
            hovermode='closest',
            hoverlabel=dict(
                bgcolor="#050505",
                font_size=13,
                font_family="monospace",
                bordercolor="#333"
            ),
            margin=dict(b=20, l=10, r=10, t=20),
            plot_bgcolor='#050505',
            paper_bgcolor='#050505',
            xaxis=dict(showgrid=True, gridcolor='#111111', gridwidth=1, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=True, gridcolor='#111111', gridwidth=1, zeroline=False, showticklabels=False),
            annotations=annotations
        )
    )

    return fig.to_html(full_html=False, include_plotlyjs='cdn', div_id='plotly-graph-div', config={'displayModeBar': False, 'responsive': False, 'scrollZoom': True})
