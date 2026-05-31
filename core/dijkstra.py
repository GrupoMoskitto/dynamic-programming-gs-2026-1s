#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import heapq
from typing import Optional


def dijkstra(
    grafo: dict[str, list[tuple[float, str]]],
    inicio: str,
    fim: str,
) -> tuple[float, list[str]]:
    if inicio not in grafo:
        raise ValueError(f"Vértice de início '{inicio}' não existe no grafo.")
    if fim not in grafo:
        raise ValueError(f"Vértice de fim '{fim}' não existe no grafo.")

    distancias: dict[str, float] = {no: float('inf') for no in grafo}
    predecessores: dict[str, Optional[str]] = {no: None for no in grafo}
    distancias[inicio] = 0

    fila: list[tuple[float, str]] = [(0, inicio)]
    visitados: set[str] = set()

    while fila:
        custo_atual, no_atual = heapq.heappop(fila)

        if no_atual in visitados:
            continue
        visitados.add(no_atual)

        if no_atual == fim:
            break

        for custo_aresta, vizinho in grafo.get(no_atual, []):
            novo_custo = custo_atual + custo_aresta
            if novo_custo < distancias[vizinho]:  
                distancias[vizinho] = novo_custo
                predecessores[vizinho] = no_atual
                heapq.heappush(fila, (novo_custo, vizinho))

    if distancias[fim] == float('inf'):
        return float('inf'), []  

    caminho = reconstruir_caminho(predecessores, fim)
    return distancias[fim], caminho


def reconstruir_caminho(
    predecessores: dict[str, Optional[str]],
    fim: str,
) -> list[str]:
    caminho: list[str] = []
    no: Optional[str] = fim
    while no is not None:
        caminho.append(no)
        no = predecessores.get(no)
    caminho.reverse()
    return caminho


def calcular_custo_caminho(
    grafo: dict[str, list[tuple[float, str]]],
    caminho: list[str],
) -> float:
    if len(caminho) < 2:
        return 0.0

    custo_total = 0.0
    for i in range(len(caminho) - 1):
        origem = caminho[i]
        destino = caminho[i + 1]

        aresta_encontrada = False
        for custo, vizinho in grafo.get(origem, []):
            if vizinho == destino:
                custo_total += custo
                aresta_encontrada = True
                break

        if not aresta_encontrada:
            raise ValueError(
                f"Aresta ({origem} → {destino}) não existe no grafo."
            )

    return custo_total
