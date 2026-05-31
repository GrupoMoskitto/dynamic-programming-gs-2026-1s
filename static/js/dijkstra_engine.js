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
    
    const edges = window.GRAPH_DATA.edges;
    const adj = {};
    window.GRAPH_DATA.nodes.forEach(n => { adj[n.id] = []; });
    
    edges.forEach(e => {
        let peso = 1;
        if (criterio === 'energia') peso = e.energia;
        else if (criterio === 'risco') peso = e.risco;
        
        adj[e.source].push({ target: e.target, weight: peso });
    });
    
    const dist = {};
    const prev = {};
    window.GRAPH_DATA.nodes.forEach(n => {
        dist[n.id] = Infinity;
        prev[n.id] = null;
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
    
    document.getElementById('graph-section').scrollIntoView({ behavior: 'smooth' });
}

function interceptForm(event) {
    event.preventDefault();
    
    const origem = document.getElementById('origem').value;
    const destino = document.getElementById('destino').value;
    const criterio = document.getElementById('criterio').value;
    
    runJsDijkstra(origem, destino, criterio);
}
