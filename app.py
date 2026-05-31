#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
from flask import Flask, render_template, request, jsonify, Response

from core.graph_model import (
    construir_grafo, validar_grafo, obter_detalhes_etapas,
    obter_unidade, obter_todos_vertices, grafo_para_json,
)
from core.dijkstra import dijkstra, calcular_custo_caminho
from core.visualization import plot_grafo_plotly

app = Flask(__name__)

_VERTICES_VALIDOS = set(obter_todos_vertices())
_CRITERIOS_VALIDOS = {'energia', 'etapas', 'risco'}
_NOME_VERTICE_RE = re.compile(r'^[A-Za-z0-9_]+$')


def _validar_nome_vertice(nome: str) -> bool:
    return (
        isinstance(nome, str)
        and bool(_NOME_VERTICE_RE.match(nome))
        and nome in _VERTICES_VALIDOS
    )



@app.route('/')
def home() -> str:
    return render_template('home.html')


@app.route('/simulador')
def simulador() -> str:
    vertices = obter_todos_vertices()
    grafo = construir_grafo('energia')
    plotly_html = plot_grafo_plotly(grafo, None)

    use_js_dijkstra = os.environ.get('USE_JS_DIJKSTRA', 'False').lower() == 'true'

    return render_template(
        'index.html',
        vertices=vertices,
        plotly_html=plotly_html,
        use_js_dijkstra=use_js_dijkstra,
        graph_json=json.dumps(grafo_para_json())
    )


@app.route('/resultado', methods=['POST'])
def resultado() -> str:
    origem = request.form.get('origem', 'Marte_Inicial')
    destino = request.form.get('destino', 'Marte_Habitavel')
    criterio = request.form.get('criterio', 'energia')

    if not _validar_nome_vertice(origem):
        return render_template('result.html', erro='Vértice de origem inválido.'), 400
    if not _validar_nome_vertice(destino):
        return render_template('result.html', erro='Vértice de destino inválido.'), 400
    if criterio not in _CRITERIOS_VALIDOS:
        return render_template('result.html', erro='Critério de otimização inválido.'), 400

    grafo = construir_grafo(criterio=criterio)
    custo, caminho = dijkstra(grafo, origem, destino)

    if not caminho:
        return render_template(
            'result.html',
            erro=f'Caminho inexistente entre {origem} e {destino}.',
        ), 404

    detalhes = obter_detalhes_etapas(caminho)
    unidade = obter_unidade(criterio)
    plotly_html = plot_grafo_plotly(grafo, caminho)

    return render_template(
        'result.html',
        caminho=caminho,
        caminho_json=json.dumps(caminho),
        custo_total=custo,
        unidade=unidade,
        num_etapas=len(caminho) - 1,
        detalhes=detalhes,
        criterio=criterio,
        origem=origem,
        destino=destino,
        plotly_html=plotly_html
    )


@app.route('/documentacao')
def documentacao() -> str:
    return render_template('docs.html')



@app.route('/otimizar', methods=['POST'])
def otimizar_rota() -> tuple[Response, int] | Response:
    dados = request.get_json()
    if not dados or not isinstance(dados, dict):
        return jsonify({'erro': 'Corpo JSON inválido.'}), 400

    origem = dados.get('origem', 'Marte_Inicial')
    destino = dados.get('destino', 'Marte_Habitavel')
    criterio = dados.get('criterio', 'energia')

    if not _validar_nome_vertice(str(origem)):
        return jsonify({'erro': 'Vértice de origem inválido.'}), 400
    if not _validar_nome_vertice(str(destino)):
        return jsonify({'erro': 'Vértice de destino inválido.'}), 400
    if criterio not in _CRITERIOS_VALIDOS:
        return jsonify({'erro': 'Critério inválido. Use: energia, etapas, risco.'}), 400

    grafo = construir_grafo(criterio=criterio)
    custo, caminho = dijkstra(grafo, str(origem), str(destino))

    if not caminho:
        return jsonify({'erro': 'Caminho inexistente entre os vértices.'}), 404

    plot_caminho = ','.join(caminho)
    return jsonify({
        'caminho': caminho,
        'custo_total': custo,
        'unidade': obter_unidade(criterio),
        'num_etapas': len(caminho) - 1,
        'detalhes': obter_detalhes_etapas(caminho),
        'plot_url': f'/plot?caminho={plot_caminho}',
    })


@app.route('/api/graph', methods=['GET'])
def obter_grafo_json() -> Response:
    return jsonify(grafo_para_json())



@app.after_request
def adicionar_cabecalhos_seguranca(response: Response) -> Response:
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net https://cdn.plot.ly; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    response.headers['Permissions-Policy'] = (
        'camera=(), microphone=(), geolocation=()'
    )
    return response



if __name__ == '__main__':
    grafo_inicial = construir_grafo('energia')
    if validar_grafo(grafo_inicial):
        print('[OK] Grafo validado: 39 vértices, 56 arestas, DAG verificado.')
    else:
        print('[ERRO] Falha na validação do grafo!')

    app.run(host='127.0.0.1', port=5000, debug=True)
