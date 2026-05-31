#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from core.graph_model import construir_grafo
from core.dijkstra import dijkstra, reconstruir_caminho, calcular_custo_caminho


class TestDijkstraBasico:

    def test_caminho_completo(self) -> None:
        grafo = construir_grafo('energia')
        custo, caminho = dijkstra(grafo, 'Marte_Inicial', 'Marte_Habitavel')
        assert custo < float('inf')
        assert len(caminho) > 0
        assert caminho[0] == 'Marte_Inicial'
        assert caminho[-1] == 'Marte_Habitavel'

    def test_caminho_para_si_mesmo(self) -> None:
        grafo = construir_grafo('energia')
        custo, caminho = dijkstra(grafo, 'Marte_Inicial', 'Marte_Inicial')
        assert custo == 0
        assert caminho == ['Marte_Inicial']

    def test_caminho_adjacente(self) -> None:
        grafo = construir_grafo('energia')
        custo, caminho = dijkstra(grafo, 'Marte_Inicial', 'Missao_Reconhecimento')
        assert custo == 50
        assert caminho == ['Marte_Inicial', 'Missao_Reconhecimento']

    def test_caminho_inexistente(self) -> None:
        grafo = construir_grafo('energia')
        # Marte_Habitavel não tem arestas de saída para Marte_Inicial
        custo, caminho = dijkstra(grafo, 'Marte_Habitavel', 'Marte_Inicial')
        assert custo == float('inf')
        assert caminho == []

    def test_custo_nao_negativo(self) -> None:
        grafo = construir_grafo('energia')
        custo, _ = dijkstra(grafo, 'Marte_Inicial', 'Marte_Habitavel')
        assert custo >= 0


class TestDijkstraCriterios:

    def test_criterio_etapas_menos_nos(self) -> None:
        grafo_energia = construir_grafo('energia')
        grafo_etapas = construir_grafo('etapas')

        _, caminho_energia = dijkstra(grafo_energia, 'Marte_Inicial', 'Marte_Habitavel')
        _, caminho_etapas = dijkstra(grafo_etapas, 'Marte_Inicial', 'Marte_Habitavel')

        assert len(caminho_etapas) <= len(caminho_energia)

    def test_criterio_risco(self) -> None:
        grafo = construir_grafo('risco')
        custo, caminho = dijkstra(grafo, 'Marte_Inicial', 'Marte_Habitavel')
        assert custo < float('inf')
        assert len(caminho) > 0


class TestDijkstraEdgeCases:

    def test_vertice_inicio_invalido(self) -> None:
        grafo = construir_grafo('energia')
        with pytest.raises(ValueError, match="início"):
            dijkstra(grafo, 'Vertice_Fake', 'Marte_Habitavel')

    def test_vertice_fim_invalido(self) -> None:
        grafo = construir_grafo('energia')
        with pytest.raises(ValueError, match="fim"):
            dijkstra(grafo, 'Marte_Inicial', 'Vertice_Fake')

    def test_grafo_simples(self) -> None:
        grafo = {
            'A': [(10, 'B'), (3, 'C')],
            'B': [(1, 'D')],
            'C': [(8, 'D')],
            'D': [],
        }
        custo, caminho = dijkstra(grafo, 'A', 'D')
        assert custo == 11  # A→B→D = 10+1 = 11 (mais barato que A→C→D = 3+8 = 11)
        assert caminho[0] == 'A'
        assert caminho[-1] == 'D'

    def test_grafo_com_multiplos_caminhos(self) -> None:
        grafo = {
            'A': [(1, 'B'), (10, 'C')],
            'B': [(1, 'C')],
            'C': [(1, 'D')],
            'D': [],
        }
        custo, caminho = dijkstra(grafo, 'A', 'D')
        assert custo == 3  # A→B→C→D = 1+1+1
        assert caminho == ['A', 'B', 'C', 'D']


class TestReconstruirCaminho:

    def test_caminho_simples(self) -> None:
        preds = {'A': None, 'B': 'A', 'C': 'B'}
        caminho = reconstruir_caminho(preds, 'C')
        assert caminho == ['A', 'B', 'C']

    def test_caminho_unico_vertice(self) -> None:
        preds = {'A': None}
        caminho = reconstruir_caminho(preds, 'A')
        assert caminho == ['A']

    def test_caminho_longo(self) -> None:
        preds = {'A': None, 'B': 'A', 'C': 'B', 'D': 'C', 'E': 'D'}
        caminho = reconstruir_caminho(preds, 'E')
        assert caminho == ['A', 'B', 'C', 'D', 'E']


class TestCalcularCustoCaminho:

    def test_custo_caminho_valido(self) -> None:
        grafo = construir_grafo('energia')
        custo = calcular_custo_caminho(
            grafo, ['Marte_Inicial', 'Missao_Reconhecimento']
        )
        assert custo == 50.0

    def test_custo_caminho_unico_no(self) -> None:
        grafo = construir_grafo('energia')
        custo = calcular_custo_caminho(grafo, ['Marte_Inicial'])
        assert custo == 0.0

    def test_custo_aresta_inexistente(self) -> None:
        grafo = construir_grafo('energia')
        with pytest.raises(ValueError, match="não existe"):
            calcular_custo_caminho(
                grafo, ['Marte_Inicial', 'Marte_Habitavel']
            )

    def test_consistencia_custo_dijkstra(self) -> None:
        grafo = construir_grafo('energia')
        custo_dijkstra, caminho = dijkstra(grafo, 'Marte_Inicial', 'Marte_Habitavel')
        custo_calculado = calcular_custo_caminho(grafo, caminho)
        assert abs(custo_dijkstra - custo_calculado) < 1e-6


class TestOtimalidade:

    def test_caminho_otimo_e_subotimo(self) -> None:
        grafo = construir_grafo('energia')
        custo_otimo, caminho_otimo = dijkstra(grafo, 'Marte_Inicial', 'Marte_Habitavel')

        # Verificar que o custo calculado bate
        custo_verificado = calcular_custo_caminho(grafo, caminho_otimo)
        assert abs(custo_otimo - custo_verificado) < 1e-6

    def test_todos_nos_no_caminho_existem(self) -> None:
        grafo = construir_grafo('energia')
        _, caminho = dijkstra(grafo, 'Marte_Inicial', 'Marte_Habitavel')
        for no in caminho:
            assert no in grafo

    def test_arestas_do_caminho_existem(self) -> None:
        grafo = construir_grafo('energia')
        _, caminho = dijkstra(grafo, 'Marte_Inicial', 'Marte_Habitavel')
        for i in range(len(caminho) - 1):
            vizinhos = [v for _, v in grafo[caminho[i]]]
            assert caminho[i + 1] in vizinhos
