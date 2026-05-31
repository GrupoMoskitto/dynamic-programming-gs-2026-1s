#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestRotaIndex:

    def test_index_status_200(self, client) -> None:
        resp = client.get('/')
        assert resp.status_code == 200

    def test_index_contem_terrapath(self, client) -> None:
        resp = client.get('/')
        assert b'TerraPath' in resp.data

    def test_index_contem_formulario(self, client) -> None:
        resp = client.get('/')
        assert b'optimization-form' in resp.data


class TestRotaOtimizar:

    def test_otimizar_sucesso(self, client) -> None:
        resp = client.post('/otimizar',
            data=json.dumps({
                'origem': 'Marte_Inicial',
                'destino': 'Marte_Habitavel',
                'criterio': 'energia',
            }),
            content_type='application/json',
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'caminho' in data
        assert 'custo_total' in data
        assert data['caminho'][0] == 'Marte_Inicial'
        assert data['caminho'][-1] == 'Marte_Habitavel'

    def test_otimizar_criterio_etapas(self, client) -> None:
        resp = client.post('/otimizar',
            data=json.dumps({
                'origem': 'Marte_Inicial',
                'destino': 'Marte_Habitavel',
                'criterio': 'etapas',
            }),
            content_type='application/json',
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['unidade'] == 'Etapas'

    def test_otimizar_criterio_risco(self, client) -> None:
        resp = client.post('/otimizar',
            data=json.dumps({
                'origem': 'Marte_Inicial',
                'destino': 'Marte_Habitavel',
                'criterio': 'risco',
            }),
            content_type='application/json',
        )
        assert resp.status_code == 200

    def test_otimizar_caminho_inexistente(self, client) -> None:
        resp = client.post('/otimizar',
            data=json.dumps({
                'origem': 'Marte_Habitavel',
                'destino': 'Marte_Inicial',
                'criterio': 'energia',
            }),
            content_type='application/json',
        )
        assert resp.status_code == 404
        data = resp.get_json()
        assert 'erro' in data

    def test_otimizar_vertice_invalido(self, client) -> None:
        resp = client.post('/otimizar',
            data=json.dumps({
                'origem': 'Vertice_Falso',
                'destino': 'Marte_Habitavel',
                'criterio': 'energia',
            }),
            content_type='application/json',
        )
        assert resp.status_code == 400

    def test_otimizar_criterio_invalido(self, client) -> None:
        resp = client.post('/otimizar',
            data=json.dumps({
                'origem': 'Marte_Inicial',
                'destino': 'Marte_Habitavel',
                'criterio': 'invalido',
            }),
            content_type='application/json',
        )
        assert resp.status_code == 400

    def test_otimizar_sem_json(self, client) -> None:
        resp = client.post('/otimizar', content_type='application/json')
        assert resp.status_code == 400

    def test_otimizar_retorna_detalhes(self, client) -> None:
        resp = client.post('/otimizar',
            data=json.dumps({
                'origem': 'Marte_Inicial',
                'destino': 'Marte_Habitavel',
                'criterio': 'energia',
            }),
            content_type='application/json',
        )
        data = resp.get_json()
        assert 'detalhes' in data
        assert 'num_etapas' in data
        assert data['num_etapas'] > 0


class TestRotaApiGraph:

    def test_api_graph_status_200(self, client) -> None:
        resp = client.get('/api/graph')
        assert resp.status_code == 200

    def test_api_graph_json_valido(self, client) -> None:
        resp = client.get('/api/graph')
        data = resp.get_json()
        assert data is not None

    def test_api_graph_tem_vertices(self, client) -> None:
        resp = client.get('/api/graph')
        data = resp.get_json()
        assert data['total_vertices'] == 39

    def test_api_graph_tem_arestas(self, client) -> None:
        resp = client.get('/api/graph')
        data = resp.get_json()
        assert data['total_arestas'] == 56


class TestRotaPlot:

    def test_plot_status_200(self, client) -> None:
        resp = client.get('/plot')
        assert resp.status_code == 200

    def test_plot_content_type_png(self, client) -> None:
        resp = client.get('/plot')
        assert resp.content_type == 'image/png'

    def test_plot_com_caminho(self, client) -> None:
        resp = client.get('/plot?caminho=Marte_Inicial,Missao_Reconhecimento')
        assert resp.status_code == 200
        assert resp.content_type == 'image/png'


class TestRotaResultado:

    def test_resultado_sucesso(self, client) -> None:
        resp = client.post('/resultado', data={
            'origem': 'Marte_Inicial',
            'destino': 'Marte_Habitavel',
            'criterio': 'energia',
        })
        assert resp.status_code == 200
        assert b'Rota' in resp.data or b'resultado' in resp.data.lower()

    def test_resultado_caminho_inexistente(self, client) -> None:
        resp = client.post('/resultado', data={
            'origem': 'Marte_Habitavel',
            'destino': 'Marte_Inicial',
            'criterio': 'energia',
        })
        assert resp.status_code == 404


class TestCabecalhosSeguranca:

    def test_x_content_type_options(self, client) -> None:
        resp = client.get('/')
        assert resp.headers.get('X-Content-Type-Options') == 'nosniff'

    def test_x_frame_options(self, client) -> None:
        resp = client.get('/')
        assert resp.headers.get('X-Frame-Options') == 'DENY'

    def test_content_security_policy(self, client) -> None:
        resp = client.get('/')
        csp = resp.headers.get('Content-Security-Policy')
        assert csp is not None
        assert "default-src 'self'" in csp

    def test_permissions_policy(self, client) -> None:
        resp = client.get('/')
        pp = resp.headers.get('Permissions-Policy')
        assert pp is not None
        assert 'camera=()' in pp
