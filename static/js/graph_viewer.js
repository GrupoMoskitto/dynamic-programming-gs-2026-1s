/**
 * graph_viewer.js — Lógica do Cytoscape.js para renderização do Grafo.
 */

document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('cy');
    if (!container) return;

    try {
        // Fetch do grafo dinâmico para evitar problemas de CORS e Paths no GH Pages
        const response = await fetch(window.API_GRAPH_URL || '/api/graph.json');
        const data = await response.json();

        // Preparar elementos pro Cytoscape
        const elements = [];
        const caminhoSet = new Set(typeof CAMINHO_OTIMO !== 'undefined' && CAMINHO_OTIMO ? CAMINHO_OTIMO : []);

        // Nós
        data.vertices.forEach(v => {
            const isPath = caminhoSet.has(v.nome);
            elements.push({
                data: {
                    id: v.nome,
                    label: v.nome.replace(/_/g, ' '),
                    fase: v.fase,
                    custo: v.custo_ativacao,
                    descricao: v.descricao,
                    cor: v.cor,
                    isPath: isPath
                }
            });
        });

        // Arestas
        data.arestas.forEach(e => {
            // Verifica se faz parte do caminho ótimo
            let isPath = false;
            if (typeof CAMINHO_OTIMO !== 'undefined' && CAMINHO_OTIMO) {
                const idx = CAMINHO_OTIMO.indexOf(e.origem);
                if (idx !== -1 && CAMINHO_OTIMO[idx + 1] === e.destino) {
                    isPath = true;
                }
            }

            elements.push({
                data: {
                    id: `${e.origem}-${e.destino}`,
                    source: e.origem,
                    target: e.destino,
                    weight: e.custo,
                    isPath: isPath
                }
            });
        });

        // Estilos Brutalistas
        const style = [
            {
                selector: 'node',
                style: {
                    'shape': 'rectangle',
                    'background-color': '#161616',
                    'border-color': 'data(cor)',
                    'border-width': 2,
                    'label': 'data(label)',
                    'color': '#fff',
                    'font-family': '"Space Mono", monospace',
                    'font-size': '12px',
                    'font-weight': 'bold',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'width': 'label',
                    'height': 'label',
                    'padding': '14px',
                    'text-wrap': 'wrap',
                    'text-max-width': '140px'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 1.5,
                    'line-color': '#262626',
                    'target-arrow-color': '#262626',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'taxi', // Linhas ortogonais brutais
                    'taxi-direction': 'downward',
                    'taxi-turn': '20px',
                    'arrow-scale': 1.2
                }
            },
            {
                selector: 'node[?isPath]',
                style: {
                    'background-color': '#d4412a',
                    'border-color': '#ff5e45',
                    'color': '#fff',
                    'font-weight': 'bold',
                    'border-width': 2,
                    'z-index': 10
                }
            },
            {
                selector: 'edge[?isPath]',
                style: {
                    'width': 3,
                    'line-color': '#d4412a',
                    'target-arrow-color': '#d4412a',
                    'z-index': 10
                }
            },
            // Hover states
            {
                selector: 'node:active',
                style: {
                    'overlay-opacity': 0
                }
            },
            {
                selector: 'node.hover',
                style: {
                    'border-color': '#3fb950',
                    'border-width': 2,
                    'color': '#fff'
                }
            },
            {
                selector: 'edge.hover',
                style: {
                    'line-color': '#3fb950',
                    'target-arrow-color': '#3fb950',
                    'width': 2,
                    'z-index': 9
                }
            },
            {
                selector: '.faded',
                style: {
                    'opacity': 0.15
                }
            }
        ];

        // Inicializar Cytoscape
        window.cy = cytoscape({
            container: container,
            elements: elements,
            style: style,
            layout: {
                name: 'dagre',
                rankDir: 'TB',
                nodeSep: 60,
                edgeSep: 20,
                rankSep: 80,
                animate: true
            },
            wheelSensitivity: 0.2
        });

        // HUD elements
        const hudEmpty = document.getElementById('inspector-empty');
        const hudContent = document.getElementById('inspector-content');
        const hudFase = document.getElementById('hud-fase');
        const hudDot = document.getElementById('hud-dot');
        const hudTitle = document.getElementById('hud-title');
        const hudCost = document.getElementById('hud-cost');
        const hudCostBar = document.getElementById('hud-cost-bar');
        const hudDesc = document.getElementById('hud-desc');
        const hudReqs = document.getElementById('hud-reqs');
        const hudUnlocks = document.getElementById('hud-unlocks');

        function showHUD(nodeData, nodeObj) {
            if (!hudContent) return;
            hudEmpty.style.display = 'none';
            hudContent.style.display = 'block';

            // Animação de scan
            hudContent.classList.remove('scan-effect');
            void hudContent.offsetWidth; // trigger reflow
            hudContent.classList.add('scan-effect');

            hudFase.textContent = nodeData.fase;
            hudDot.style.backgroundColor = nodeData.cor;
            hudTitle.textContent = nodeData.label;
            hudCost.textContent = nodeData.custo.toLocaleString('pt-BR');
            hudDesc.textContent = nodeData.descricao;

            // Barra de energia (limite heurístico de 15.000 TJ para preencher barra)
            const MAX_COST = 15000;
            const pct = Math.min(100, Math.max(0, (nodeData.custo / MAX_COST) * 100));
            hudCostBar.style.width = pct + '%';

            // Incomers e Outgoers
            const incomers = nodeObj.incomers('node');
            const outgoers = nodeObj.outgoers('node');

            hudReqs.innerHTML = '';
            if (incomers.length === 0) {
                hudReqs.innerHTML = '<span style="color:#555; font-size:0.65rem;">Nenhum</span>';
            } else {
                incomers.forEach(n => {
                    hudReqs.innerHTML += `<div class="conn-item">${n.data('label')}</div>`;
                });
            }

            hudUnlocks.innerHTML = '';
            if (outgoers.length === 0) {
                hudUnlocks.innerHTML = '<span style="color:#555; font-size:0.65rem;">Fim da Rota</span>';
            } else {
                outgoers.forEach(n => {
                    hudUnlocks.innerHTML += `<div class="conn-item">${n.data('label')}</div>`;
                });
            }
        }

        // Interatividade: Hover e Tap atualizam o HUD e iluminam vizinhos
        function highlightNode(node) {
            const neighborhood = node.neighborhood().add(node);
            window.cy.elements().addClass('faded');
            neighborhood.removeClass('faded');
            neighborhood.addClass('hover');
            showHUD(node.data(), node);
        }

        window.cy.on('mouseover tap', 'node', function(e) {
            highlightNode(e.target);
        });

        window.cy.on('mouseout', 'node', function(e) {
            // Em caso de touch, tap pode ser melhor mantido até tap fora
            if (e.type === 'mouseout') {
                window.cy.elements().removeClass('faded hover');
            }
        });

        // Fit após o primeiro layout
        window.cy.on('layoutstop', function() {
            window.cy.fit(window.cy.elements(), 30); // 30px padding
        });

    } catch (err) {
        console.error("Erro ao carregar grafo Cytoscape:", err);
        container.innerHTML = `<div style="padding:20px; color:#d4412a;">Falha ao carregar grafo interativo: ${err.message}<br>Stack: ${err.stack}</div>`;
    }
});
