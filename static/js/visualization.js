/**
 * visualization.js — Interatividade mínima, sem firula.
 */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // Highlight de linha da tabela
    var rows = document.querySelectorAll('.details-table tbody tr');
    rows.forEach(function (row) {
        row.addEventListener('mouseenter', function () {
            this.style.backgroundColor = '#1a1a1a';
        });
        row.addEventListener('mouseleave', function () {
            this.style.backgroundColor = '';
        });
    });

    // --- Plotly HUD Logic ---
    const plotlyDiv = document.getElementById('plotly-graph-div');
    if (plotlyDiv) {
        // Plotly é injetado dinamicamente, então esperamos o objeto estar pronto
        const checkPlotly = setInterval(() => {
            if (plotlyDiv.on) {
                clearInterval(checkPlotly);
                plotlyDiv.on('plotly_click', function(data){
                    if(data.points.length === 0) return;
                    const pt = data.points[0];
                    if(!pt.customdata) return; // Se clicou na linha, ignoramos
                    
                    const [id, fase, custo, desc, color] = pt.customdata;
                    
                    // Esconder tela vazia e mostrar conteúdo
                    document.getElementById('plotly-inspector-empty').style.display = 'none';
                    document.getElementById('plotly-inspector-content').style.display = 'block';
                    
                    // Preencher textos básicos
                    document.getElementById('plotly-hud-title').innerText = id.replace(/_/g, ' ');
                    document.getElementById('plotly-hud-fase').innerText = fase;
                    document.getElementById('plotly-hud-dot').style.backgroundColor = color;
                    document.getElementById('plotly-hud-cost').innerText = custo;
                    document.getElementById('plotly-hud-desc').innerHTML = desc;
                    
                    // Animar barra de energia (Máx 2000 como referência)
                    const MAX_COST = 2000;
                    const pct = Math.min(100, Math.max(0, (custo / MAX_COST) * 100));
                    document.getElementById('plotly-hud-cost-bar').style.width = pct + '%';
                    document.getElementById('plotly-hud-cost-bar').style.backgroundColor = color;
                    
                    // Calcular Entradas (Reqs) e Saídas (Unlocks) usando window.graphData
                    const hudReqs = document.getElementById('plotly-hud-reqs');
                    const hudUnlocks = document.getElementById('plotly-hud-unlocks');
                    hudReqs.innerHTML = '';
                    hudUnlocks.innerHTML = '';
                    
                    if (window.graphData) {
                        const inEdges = window.graphData.edges.filter(e => e.target === id);
                        const outEdges = window.graphData.edges.filter(e => e.source === id);
                        
                        if(inEdges.length === 0) {
                            hudReqs.innerHTML = '<span class="conn-badge" style="background:#222;border:1px solid #333;color:#666">Nenhum</span>';
                        }
                        inEdges.forEach(e => {
                            hudReqs.innerHTML += `<span class="conn-badge" style="border-left:2px solid #ef4444">${e.source.replace(/_/g, ' ')}</span>`;
                        });
                        
                        if(outEdges.length === 0) {
                            hudUnlocks.innerHTML = '<span class="conn-badge" style="background:#222;border:1px solid #333;color:#666">Fim da Linha</span>';
                        }
                        outEdges.forEach(e => {
                            hudUnlocks.innerHTML += `<span class="conn-badge" style="border-left:2px solid #10b981">${e.target.replace(/_/g, ' ')}</span>`;
                        });
                    }
                });
            }
        }, 200);
    }
});
