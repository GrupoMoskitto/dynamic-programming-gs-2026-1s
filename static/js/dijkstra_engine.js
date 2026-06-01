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

function runJsDijkstra(origem, destino, criterio) {
    if (!window.GRAPH_DATA) {
        console.error("GRAPH_DATA não encontrado!");
        alert("Erro fatal: Banco de dados do grafo não carregado na versão estática.");
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
    
    const costValue = dist[destino];
    const steps = path.length - 1;
    let unit = "TJ";
    if (criterio === 'etapas') unit = "Transições";
    if (criterio === 'risco') unit = "Risco Relativo";
    
    document.getElementById('js-result-cost').innerText = costValue.toLocaleString('pt-BR');
    document.getElementById('js-result-unit').innerText = unit;
    document.getElementById('js-result-steps').innerText = steps;
    
    const resultSection = document.getElementById('js-result-section');
    resultSection.style.display = 'block';
    
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function interceptForm(event) {
    event.preventDefault();
    
    const origem = document.getElementById('origem').value;
    const destino = document.getElementById('destino').value;
    const criterio = document.getElementById('criterio').value;
    
    runJsDijkstra(origem, destino, criterio);
}
