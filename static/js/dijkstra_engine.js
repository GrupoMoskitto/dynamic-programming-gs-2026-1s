class PriorityQueue {
    constructor() {
        this.elements = [];
    }
    enqueue(element, priority) {
        this.elements.push({element, priority});
        this.elements.sort((a, b) => a.priority - b.priority);
    }
    dequeue() {
        return this.elements.shift().element;
    }
    isEmpty() {
        return this.elements.length === 0;
    }
}

function updateHUDWithPath(path, arestas, phaseMap) {
    if (window.cy) {
        window.cy.elements().removeClass('path-node path-edge');
        for (let i = 0; i < path.length; i++) {
            const nodeId = path[i];
            window.cy.$(`#${nodeId}`).addClass('path-node');
            if (i < path.length - 1) {
                const nextId = path[i+1];
                window.cy.$(`edge[source="${nodeId}"][target="${nextId}"]`).addClass('path-edge');
            }
        }
    }
    
    let realEnergy = 0;
    let realRisk = 0;
    
    const RISCO_FASE = {
        'Estado Inicial': 0.0, 'Preparacao': 1.0, 'Energia': 3.0,
        'Atmosfera': 2.5, 'Protecao': 4.0, 'Temperatura': 3.5,
        'Agua': 2.0, 'Biologia': 3.0, 'Colonizacao': 2.5,
        'Expansao': 3.5, 'Terraformacao': 5.0, 'Objetivo Final': 0.0
    };
    
    const trajList = document.getElementById('js-trajectory-list');
    trajList.innerHTML = '';
    trajList.className = 'timeline-list';
    
    for (let i = 0; i < path.length - 1; i++) {
        const u = path[i];
        const v = path[i+1];
        const edge = arestas.find(e => e.origem === u && e.destino === v);
        
        let edgeCost = '?';
        
        if (edge) {
            edgeCost = edge.custo;
            realEnergy += edge.custo;
            const faseDest = phaseMap[v] || '';
            const fator = RISCO_FASE[faseDest] !== undefined ? RISCO_FASE[faseDest] : 1.0;
            realRisk += fator;
        }
        
        const baseRisk = 1.2;
        const li = document.createElement('li');
        li.className = 'trajectory-item';
        
        li.innerHTML = `
            <div class="traj-nodes">
                <span class="traj-step">#${(i+1).toString().padStart(2, '0')}</span>
                <span class="traj-node">${u.replace(/_/g, ' ')}</span>
                <span class="traj-arrow">➔</span>
                <span class="traj-node" style="color: var(--info);">${v.replace(/_/g, ' ')}</span>
            </div>
            <div class="traj-cost">${edgeCost} TJ</div>
        `;
        trajList.appendChild(li);
    }
    
    const steps = path.length - 1;
    

    const plotlyDivs = document.querySelectorAll('.js-plotly-plot');
    if (plotlyDivs.length > 0 && window.Plotly) {
        const pdiv = plotlyDivs[0];
        const nodeTrace = pdiv.data.find(t => t.mode && t.mode.includes('markers'));
        if (nodeTrace) {
            const numNodes = nodeTrace.x.length;
            const nodeColors = new Array(numNodes).fill('rgba(20,20,20,0.5)');
            const nodeBorders = new Array(numNodes).fill('#222222');
            
            const nodesData = [];
            for(let i=0; i < numNodes; i++) {
                const nName = nodeTrace.customdata[i][0];
                const baseColor = nodeTrace.customdata[i][4];
                nodesData.push({x: nodeTrace.x[i], y: nodeTrace.y[i], name: nName});
                
                if (path.includes(nName)) {
                    nodeColors[i] = baseColor;
                    nodeBorders[i] = baseColor;
                }
            }
            Plotly.restyle(pdiv, {'marker.color': [nodeColors], 'marker.line.color': [nodeBorders]}, [0]);
            
            if (pdiv.layout && pdiv.layout.annotations) {
                const newAnnotations = JSON.parse(JSON.stringify(pdiv.layout.annotations));
                
                const getClosestNode = (px, py) => {
                    let minDist = Infinity;
                    let closest = null;
                    for(const nd of nodesData) {
                        const dist = Math.sqrt(Math.pow(nd.x - px, 2) + Math.pow(nd.y - py, 2));
                        if(dist < minDist) {
                            minDist = dist;
                            closest = nd.name;
                        }
                    }
                    return closest;
                };

                for(let j=0; j < newAnnotations.length; j++) {
                    const ann = newAnnotations[j];
                    
                    if (ann.name && ann.name.endsWith('|nodelabel')) continue;
                    
                    let uName = null;
                    let vName = null;
                    
                    if (ann.name && ann.name.includes('|')) {
                        const parts = ann.name.split('|');
                        uName = parts[0];
                        vName = parts[1];
                    } else {
                        uName = getClosestNode(ann.ax, ann.ay);
                        vName = getClosestNode(ann.x, ann.y);
                    }
                    
                    if (!uName || !vName) continue;
                    
                    let isPathEdge = false;
                    for (let p=0; p < path.length - 1; p++) {
                        if (path[p] === uName && path[p+1] === vName) {
                            isPathEdge = true;
                            break;
                        }
                    }
                    
                    if (isPathEdge) {
                        if (ann.name && ann.name.endsWith('|text')) {
                            if (ann.font) ann.font.color = '#38bdf8';
                            ann.bordercolor = '#38bdf8';
                            ann.opacity = 1.0;
                        } else {
                            ann.arrowcolor = '#38bdf8';
                            ann.opacity = 1.0;
                            ann.arrowwidth = 2.5;
                            ann.arrowhead = 4;
                        }
                    } else {
                        if (ann.name && ann.name.endsWith('|text')) {
                            if (ann.font) ann.font.color = '#444444';
                            ann.bordercolor = '#222222';
                            ann.opacity = 0.4;
                        } else {
                            ann.arrowcolor = '#333333';
                            ann.opacity = 0.3;
                            ann.arrowwidth = 1.0;
                            ann.arrowhead = 2;
                        }
                    }
                }
                Plotly.relayout(pdiv, {'annotations': newAnnotations});
            }
        }
    }
    const budget = (realEnergy * 0.015).toFixed(1); 
    
    let probability = 100 - (realRisk * 3.5);
    if (probability > 99) probability = 99.9;
    if (probability < 5) probability = 5.0;
    
    const probColor = probability < 50 ? 'var(--warning)' : 'var(--info)';
    const riskColor = realRisk > 15 ? 'var(--warning)' : 'var(--accent)';
    
    document.getElementById('js-result-cost').innerText = realEnergy.toLocaleString('pt-BR');
    document.getElementById('js-result-steps').innerText = steps;
    
    const elRisk = document.getElementById('js-result-risk');
    elRisk.innerText = realRisk.toFixed(1);
    elRisk.style.color = riskColor;
    
    document.getElementById('js-result-budget').innerText = "$" + budget;
    
    const elProb = document.getElementById('js-result-prob');
    elProb.innerText = probability.toFixed(1) + "%";
    elProb.style.color = probColor;
    
    const resultSection = document.getElementById('results-section');
    if (resultSection) {
        resultSection.style.display = 'block';
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function runJsDijkstra(origem, destino, criterio) {
    if (!window.GRAPH_DATA) {
        alert("Erro fatal: Banco de dados do grafo não carregado.");
        return;
    }
    
    const arestas = window.GRAPH_DATA.arestas;
    const adj = {};
    const phaseMap = {};
    window.GRAPH_DATA.vertices.forEach(v => { 
        adj[v.nome] = []; 
        phaseMap[v.nome] = v.fase;
    });
    
    const RISCO_FASE = {
        'Estado Inicial': 0.0, 'Preparacao': 1.0, 'Energia': 3.0,
        'Atmosfera': 2.5, 'Protecao': 4.0, 'Temperatura': 3.5,
        'Agua': 2.0, 'Biologia': 3.0, 'Colonizacao': 2.5,
        'Expansao': 3.5, 'Terraformacao': 5.0, 'Objetivo Final': 0.0
    };
    
    arestas.forEach(e => {
        let peso = 1;
        if (criterio === 'energia') peso = e.custo;
        else if (criterio === 'risco') {
            const faseDest = phaseMap[e.destino] || '';
            const fator = RISCO_FASE[faseDest] !== undefined ? RISCO_FASE[faseDest] : 1.0;
            peso = e.custo * fator;
        }
        adj[e.origem].push({ target: e.destino, weight: peso });
    });
    
    const dist = {};
    const prev = {};
    window.GRAPH_DATA.vertices.forEach(v => {
        dist[v.nome] = Infinity;
        prev[v.nome] = null;
    });
    
    dist[origem] = 0;
    const pq = new PriorityQueue();
    pq.enqueue(origem, 0);
    
    while (!pq.isEmpty()) {
        const u = pq.dequeue();
        if (u === destino) break;
        adj[u].forEach(neighbor => {
            const v = neighbor.target;
            const alt = dist[u] + neighbor.weight;
            if (alt < dist[v]) {
                dist[v] = alt;
                prev[v] = u;
                pq.enqueue(v, alt);
            }
        });
    }
    
    if (dist[destino] === Infinity) {
        alert("Caminho impossível entre os estágios selecionados!");
        return;
    }
    
    const path = [];
    let curr = destino;
    while (curr !== null) {
        path.unshift(curr);
        curr = prev[curr];
    }
    
    updateHUDWithPath(path, arestas, phaseMap);
}

function interceptForm(event) {
    event.preventDefault();
    
    const origem = document.getElementById('origem').value;
    const destino = document.getElementById('destino').value;
    const criterio = document.getElementById('criterio').value;
    
    if (window.USE_JS_DIJKSTRA) {
        runJsDijkstra(origem, destino, criterio);
    } else {
        const btn = document.getElementById('btn-optimize');
        const oldText = btn.innerHTML;
        btn.innerHTML = 'Conectando ao Backend...';
        
        fetch('/otimizar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({origem, destino, criterio})
        })
        .then(response => response.json())
        .then(data => {
            btn.innerHTML = oldText;
            if (data.erro) { 
                alert("Erro: " + data.erro); 
                return; 
            }
            
            const arestas = window.GRAPH_DATA.arestas;
            const phaseMap = {};
            window.GRAPH_DATA.vertices.forEach(v => { 
                phaseMap[v.nome] = v.fase;
            });
            
            updateHUDWithPath(data.caminho, arestas, phaseMap);
        })
        .catch(err => {
            btn.innerHTML = oldText;
            alert("Erro ao conectar com a API Python.");
            console.error(err);
        });
    }
}
