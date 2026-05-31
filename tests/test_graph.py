#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from core.graph_model import (
    NODES, EDGES, construir_grafo, validar_grafo,
    obter_fase, obter_custo_ativacao, obter_descricao,
    obter_detalhes_etapas, obter_unidade, obter_todos_vertices,
    grafo_para_json,
)


class TestEstruturaDados:

    def test_total_vertices(self) -> None:
        assert len(NODES) == 39

    def test_total_arestas(self) -> None:
        assert len(EDGES) == 56

    def test_ids_unicos(self) -> None:
        ids = [node[0] for node in NODES]
        assert len(ids) == len(set(ids))

    def test_nomes_unicos(self) -> None:
        nomes = [node[1] for node in NODES]
        assert len(nomes) == len(set(nomes))

    def test_ids_sequenciais(self) -> None:
        ids = sorted([node[0] for node in NODES])
        assert ids == list(range(39))

    def test_marte_inicial_existe(self) -> None:
        assert NODES[0][1] == 'Marte_Inicial'
        assert NODES[0][3] == 0  # custo zero

    def test_marte_habitavel_existe(self) -> None:
        assert NODES[-1][1] == 'Marte_Habitavel'
        assert NODES[-1][3] == 0  # custo zero

    def test_arestas_referenciam_vertices_validos(self) -> None:
        nomes_validos = {node[1] for node in NODES}
        for origem, destino, _ in EDGES:
            assert origem in nomes_validos, f"Origem inválida: {origem}"
            assert destino in nomes_validos, f"Destino inválido: {destino}"

    def test_custos_nao_negativos(self) -> None:
        for _, _, custo in EDGES:
            assert custo >= 0, f"Custo negativo encontrado: {custo}"


class TestConstruirGrafo:

    def test_construir_grafo_energia(self) -> None:
        grafo = construir_grafo('energia')
        assert len(grafo) == 39
        # Verificar que Marte_Inicial tem vizinhos
        assert len(grafo['Marte_Inicial']) > 0

    def test_construir_grafo_etapas(self) -> None:
        grafo = construir_grafo('etapas')
        for no, vizinhos in grafo.items():
            for custo, _ in vizinhos:
                assert custo == 1.0

    def test_construir_grafo_risco(self) -> None:
        grafo = construir_grafo('risco')
        assert len(grafo) == 39

    def test_criterio_invalido_levanta_erro(self) -> None:
        with pytest.raises(ValueError, match="inválido"):
            construir_grafo('invalido')

    def test_todos_nos_presentes(self) -> None:
        grafo = construir_grafo()
        nomes = {node[1] for node in NODES}
        assert set(grafo.keys()) == nomes

    def test_total_arestas_no_grafo(self) -> None:
        grafo = construir_grafo()
        total = sum(len(vizinhos) for vizinhos in grafo.values())
        assert total == 56


class TestValidarGrafo:

    def test_grafo_valido(self) -> None:
        grafo = construir_grafo()
        assert validar_grafo(grafo) is True

    def test_grafo_sem_marte_inicial(self) -> None:
        grafo = construir_grafo()
        del grafo['Marte_Inicial']
        assert validar_grafo(grafo) is False

    def test_grafo_sem_marte_habitavel(self) -> None:
        grafo = construir_grafo()
        del grafo['Marte_Habitavel']
        assert validar_grafo(grafo) is False

    def test_grafo_com_peso_negativo(self) -> None:
        grafo = {'A': [(-1, 'B')], 'B': [], 'Marte_Inicial': [], 'Marte_Habitavel': []}
        assert validar_grafo(grafo) is False

    def test_grafo_com_ciclo(self) -> None:
        grafo = {
            'Marte_Inicial': [(1, 'A')],
            'A': [(1, 'B')],
            'B': [(1, 'A')],  # Ciclo!
            'Marte_Habitavel': [],
        }
        assert validar_grafo(grafo) is False

    def test_grafo_desconectado(self) -> None:
        grafo = {
            'Marte_Inicial': [(1, 'A')],
            'A': [],
            'Marte_Habitavel': [],  # Inalcançável
        }
        assert validar_grafo(grafo) is False


class TestConsultas:

    def test_obter_fase_valida(self) -> None:
        assert obter_fase('Marte_Inicial') == 'Estado Inicial'
        assert obter_fase('Gerador_Nuclear_Alpha') == 'Energia'

    def test_obter_fase_invalida(self) -> None:
        with pytest.raises(KeyError):
            obter_fase('Vertice_Inexistente')

    def test_obter_custo_ativacao(self) -> None:
        assert obter_custo_ativacao('Marte_Inicial') == 0
        assert obter_custo_ativacao('Gerador_Nuclear_Alpha') == 500

    def test_obter_descricao(self) -> None:
        desc = obter_descricao('Marte_Inicial')
        assert 'Marte' in desc

    def test_obter_unidade_energia(self) -> None:
        assert 'TeraJoules' in obter_unidade('energia')

    def test_obter_unidade_etapas(self) -> None:
        assert 'Etapas' in obter_unidade('etapas')

    def test_obter_todos_vertices(self) -> None:
        vertices = obter_todos_vertices()
        assert len(vertices) == 39
        assert vertices[0] == 'Marte_Inicial'
        assert vertices[-1] == 'Marte_Habitavel'


class TestDetalhesEtapas:

    def test_detalhes_caminho_simples(self) -> None:
        detalhes = obter_detalhes_etapas(['Marte_Inicial', 'Missao_Reconhecimento'])
        assert len(detalhes) == 2
        assert detalhes[0]['nome'] == 'Marte_Inicial'
        assert detalhes[0]['custo_acumulado'] == 0
        assert detalhes[1]['custo_transicao'] == 50
        assert detalhes[1]['custo_acumulado'] == 50

    def test_detalhes_caminho_unico(self) -> None:
        detalhes = obter_detalhes_etapas(['Marte_Inicial'])
        assert len(detalhes) == 1
        assert detalhes[0]['custo_acumulado'] == 0

    def test_detalhes_contem_campos_obrigatorios(self) -> None:
        detalhes = obter_detalhes_etapas(['Marte_Inicial', 'Missao_Reconhecimento'])
        campos = {'etapa', 'nome', 'fase', 'custo_ativacao',
                  'custo_transicao', 'custo_acumulado', 'descricao'}
        for d in detalhes:
            assert campos.issubset(d.keys())


class TestGrafoJson:

    def test_json_tem_vertices(self) -> None:
        data = grafo_para_json()
        assert data['total_vertices'] == 39

    def test_json_tem_arestas(self) -> None:
        data = grafo_para_json()
        assert data['total_arestas'] == 56

    def test_json_tem_fases(self) -> None:
        data = grafo_para_json()
        assert len(data['fases']) > 0

    def test_vertice_json_tem_campos(self) -> None:
        data = grafo_para_json()
        v = data['vertices'][0]
        assert 'id' in v
        assert 'nome' in v
        assert 'fase' in v
        assert 'custo_ativacao' in v
        assert 'cor' in v
