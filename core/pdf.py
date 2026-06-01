#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.colors import HexColor

MARS_RED   = HexColor('#C1440E')
SPACE_BLUE = HexColor('#0B1426')
TEAL       = HexColor('#1B6CA8')
LIGHT_BLUE = HexColor('#EFF6FF')
WHITE      = colors.white
BLACK      = colors.black
DARK_GRAY  = HexColor('#1F2937')
MID_GRAY   = HexColor('#374151')
GRAY       = HexColor('#6B7280')
LIGHT_GRAY = HexColor('#F3F4F6')
BORDER     = HexColor('#E5E7EB')
CODE_BG    = HexColor('#1E293B')
CODE_FG    = HexColor('#E2E8F0')
GREEN_BG   = HexColor('#F0FDF4')
GREEN_MID  = HexColor('#166534')
ORANGE_BG  = HexColor('#FFF7ED')
ORANGE     = HexColor('#C2410C')
PURPLE_BG  = HexColor('#F5F3FF')
PURPLE     = HexColor('#6D28D9')
BLUE_DARK  = HexColor('#1D4ED8')
PHASE_COLORS = [
    HexColor('#6366F1'), HexColor('#0EA5E9'), HexColor('#10B981'),
    HexColor('#F59E0B'), HexColor('#EF4444'), HexColor('#8B5CF6'),
    HexColor('#EC4899'), HexColor('#14B8A6'), HexColor('#F97316'),
]

W, H = A4

def S():
    return {
        'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=17,
            textColor=SPACE_BLUE, spaceBefore=20, spaceAfter=8, leading=22),
        'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=13,
            textColor=TEAL, spaceBefore=14, spaceAfter=7, leading=17),
        'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=11,
            textColor=MID_GRAY, spaceBefore=10, spaceAfter=5, leading=14),
        'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10,
            textColor=MID_GRAY, spaceAfter=8, leading=16, alignment=TA_JUSTIFY),
        'bl': ParagraphStyle('bl', fontName='Helvetica', fontSize=10,
            textColor=MID_GRAY, spaceAfter=8, leading=16),
        'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=10,
            textColor=MID_GRAY, spaceAfter=3, leading=15, leftIndent=14),
        'code': ParagraphStyle('code', fontName='Courier', fontSize=7.8,
            textColor=CODE_FG, spaceAfter=2, leading=11.2),
        'caption': ParagraphStyle('caption', fontName='Helvetica', fontSize=8,
            textColor=GRAY, alignment=TA_CENTER, spaceAfter=6, leading=10),
        'th': ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=8.5,
            textColor=WHITE, alignment=TA_CENTER, leading=12),
        'td': ParagraphStyle('td', fontName='Helvetica', fontSize=8,
            textColor=MID_GRAY, leading=11),
        'tdc': ParagraphStyle('tdc', fontName='Helvetica', fontSize=8,
            textColor=MID_GRAY, alignment=TA_CENTER, leading=11),
        'tdm': ParagraphStyle('tdm', fontName='Courier', fontSize=7.5,
            textColor=DARK_GRAY, leading=10),
        'req': ParagraphStyle('req', fontName='Helvetica-Bold', fontSize=10,
            textColor=MARS_RED, spaceAfter=2, leading=13),
        'toc': ParagraphStyle('toc', fontName='Helvetica', fontSize=10.5,
            textColor=MID_GRAY, spaceAfter=5, leading=15),
        'toch': ParagraphStyle('toch', fontName='Helvetica-Bold', fontSize=13,
            textColor=SPACE_BLUE, spaceAfter=16, leading=17),
        'math': ParagraphStyle('math', fontName='Courier', fontSize=9.5,
            textColor=DARK_GRAY, spaceAfter=4, leading=14, leftIndent=20),
        'box_title': ParagraphStyle('bt', fontName='Helvetica-Bold', fontSize=10,
            textColor=BLUE_DARK, leading=13),
        'box_body': ParagraphStyle('bb', fontName='Helvetica', fontSize=9.5,
            textColor=MID_GRAY, leading=14, alignment=TA_JUSTIFY),
        'badge': ParagraphStyle('badge', fontName='Helvetica-Bold', fontSize=8,
            textColor=WHITE, alignment=TA_CENTER, leading=11),
    }

def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(SPACE_BLUE)
    canvas.rect(0, 0, W, H, fill=True, stroke=False)
    canvas.setFillColor(HexColor('#0F2744'))
    canvas.rect(0, H * 0.55, W, H * 0.45, fill=True, stroke=False)
    canvas.setFillColor(MARS_RED)
    canvas.rect(2.5*cm, H * 0.47, W - 5*cm, 0.35*cm, fill=True, stroke=False)
    canvas.setFillColor(HexColor('#0F3D4A'))
    canvas.rect(0, 0, W, H * 0.2, fill=True, stroke=False)
    canvas.setFillColor(TEAL)
    canvas.rect(0, H * 0.2, W, 0.12*cm, fill=True, stroke=False)
    canvas.setFillColor(HexColor('#1A3A5C'))
    canvas.circle(W * 0.5, H * 0.75, 4.5*cm, fill=True, stroke=False)
    canvas.setFillColor(HexColor('#C1440E'))
    canvas.circle(W * 0.5, H * 0.75, 3.8*cm, fill=True, stroke=False)
    canvas.setFillColor(HexColor('#D4512A'))
    canvas.circle(W * 0.46, H * 0.77, 1.2*cm, fill=True, stroke=False)
    canvas.setFillColor(HexColor('#8B2500'))
    canvas.circle(W * 0.55, H * 0.72, 0.7*cm, fill=True, stroke=False)
    canvas.setFont('Helvetica-Bold', 42)
    canvas.setFillColor(WHITE)
    canvas.drawCentredString(W / 2, H * 0.52, 'TERRAPATH')
    canvas.setFont('Helvetica', 14)
    canvas.setFillColor(HexColor('#93C5FD'))
    canvas.drawCentredString(W / 2, H * 0.465, 'Sequenciador de Terraformacao Marciana')
    canvas.setFillColor(HexColor('#7C2D12'))
    canvas.roundRect(W/2 - 5*cm, H*0.40, 10*cm, 0.9*cm, 6, fill=True, stroke=False)
    canvas.setFont('Helvetica-Bold', 11)
    canvas.setFillColor(HexColor('#FDBA74'))
    canvas.drawCentredString(W / 2, H * 0.425, 'DOCUMENTACAO TECNICA — PROGRAMACAO DINAMICA')
    canvas.setFont('Helvetica', 10)
    canvas.setFillColor(HexColor('#94A3B8'))
    canvas.drawCentredString(W / 2, H * 0.16, 'FIAP — Global Solution  |  2026')
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(HexColor('#64748B'))
    canvas.drawCentredString(W / 2, H * 0.12, 'Grafos, Algoritmo de Dijkstra e Programacao Dinamica')
    canvas.drawCentredString(W / 2, H * 0.085, 'Aplicados ao Planejamento de Missoes Espaciais')
    canvas.restoreState()

def on_pages(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(SPACE_BLUE)
    canvas.rect(0, H - 1.45*cm, W, 1.45*cm, fill=True, stroke=False)
    canvas.setFillColor(MARS_RED)
    canvas.rect(0, H - 1.5*cm, W, 0.08*cm, fill=True, stroke=False)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.setFillColor(WHITE)
    canvas.drawString(2.5*cm, H - 0.95*cm, 'TerraPath')
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(HexColor('#94A3B8'))
    canvas.drawString(4.6*cm, H - 0.95*cm, '| Sequenciador de Terraformacao Marciana')
    canvas.drawRightString(W - 2.5*cm, H - 0.95*cm, 'Prog. Dinamica — FIAP 2026')
    canvas.setFillColor(LIGHT_GRAY)
    canvas.rect(0, 0, W, 1.1*cm, fill=True, stroke=False)
    canvas.setFillColor(MARS_RED)
    canvas.rect(0, 1.08*cm, W, 0.05*cm, fill=True, stroke=False)
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(2.5*cm, 0.38*cm, 'Global Solution | FIAP 2026')
    canvas.setFont('Helvetica-Bold', 8.5)
    canvas.setFillColor(DARK_GRAY)
    canvas.drawRightString(W - 2.5*cm, 0.38*cm, str(doc.page))
    canvas.restoreState()

def hr(color=BORDER, t=1):
    return HRFlowable(width='100%', thickness=t, color=color, spaceAfter=8, spaceBefore=2)

def h1(num, title, s):
    txt = f'<font color="#C1440E"><b>{num}.</b></font>  {title}'
    return [Paragraph(txt, s['h1']), hr(MARS_RED, 1.8), Spacer(1, 4)]

def h2(num, title, s):
    txt = f'<font color="#1B6CA8"><b>{num}</b></font>  {title}'
    return [Paragraph(txt, s['h2'])]

def h3(title, s):
    return [Paragraph(title, s['h3'])]

def code_block(text, s):
    lines = text.split('\n')
    proc = '<br/>'.join(
        l.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
         .replace(' ', '&nbsp;')
        for l in lines
    )
    para = Paragraph(proc, s['code'])
    t = Table([[para]], colWidths=[15.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    return [t, Spacer(1, 8)]

def info_box(title, body, s, bg=LIGHT_BLUE, tc=BLUE_DARK, border=TEAL):
    rows = [[Paragraph(title, s['box_title'])],
            [Paragraph(body, s['box_body'])]]
    t = Table(rows, colWidths=[15.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (0,0), 10),
        ('TOPPADDING', (0,1), (0,1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEBEFORE', (0,0), (0,-1), 3.5, border),
    ]))
    return [t, Spacer(1, 8)]

def badge_row(items, s):
    cells = []
    badge_colors = [MARS_RED, TEAL, HexColor('#166534'), HexColor('#7C3AED')]
    for i, (label, val) in enumerate(items):
        color = badge_colors[i % len(badge_colors)]
        inner = Table([
            [Paragraph(label, ParagraphStyle('_bl', fontName='Helvetica', fontSize=7.5,
                textColor=HexColor('#CBD5E1'), alignment=TA_CENTER, leading=10))],
            [Paragraph(val, ParagraphStyle('_bv', fontName='Helvetica-Bold', fontSize=11,
                textColor=WHITE, alignment=TA_CENTER, leading=14))],
        ], colWidths=[3.6*cm])
        inner.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), color),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        cells.append(inner)
    row_table = Table([cells], colWidths=[3.6*cm]*len(items),
                       hAlign='CENTER')
    row_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    return [row_table, Spacer(1, 10)]

NODES = [
    (0,  'Marte_Inicial',          'Estado Inicial',   0,     'Ponto de partida — Marte sem qualquer intervencao humana'),
    (1,  'Missao_Reconhecimento',  'Preparacao',        50,   'Missao orbital e superficial de reconhecimento inicial'),
    (2,  'Satelite_Mapeamento',    'Preparacao',        80,   'Constelacao de satelites para mapeamento geologico detalhado'),
    (3,  'Gerador_Nuclear_Alpha',  'Energia',           500,  'Primeiro reator nuclear de fissao instalado em superficie'),
    (4,  'Gerador_Nuclear_Beta',   'Energia',           450,  'Segundo reator + rede de distribuicao de energia'),
    (5,  'Espelho_Solar_Orbital',  'Energia',           800,  'Espelhos orbitais para amplificacao do fluxo solar'),
    (6,  'Aquecimento_Fase1',      'Atmosfera',        1200,  'Aumento de temperatura de -60 C para -30 C'),
    (7,  'Liberacao_CO2_Norte',    'Atmosfera',         600,  'Liberacao de CO2 das calotas polares norte via calor'),
    (8,  'Liberacao_CO2_Sul',      'Atmosfera',         700,  'Liberacao de CO2 das calotas polares sul via calor'),
    (9,  'Pressao_1pct',           'Atmosfera',         900,  'Pressao atmosferica: 1% da Terra (approx. 1 kPa)'),
    (10, 'Pressao_5pct',           'Atmosfera',        1500,  'Pressao atmosferica: 5% da Terra (approx. 5 kPa)'),
    (11, 'Pressao_20pct',          'Atmosfera',        3000,  'Pressao atmosferica: 20% da Terra (approx. 20 kPa)'),
    (12, 'Campo_Magnetico',        'Protecao',         2000,  'Campo magnetico artificial via dipolo no ponto L1 Terra-Sol'),
    (13, 'Escudo_Radiacao',        'Protecao',          400,  'Escudos localizados de radiacao nas zonas habitadas'),
    (14, 'Aquecimento_Fase2',      'Temperatura',      2500,  'Aumento de temperatura de -30 C ate 0 C'),
    (15, 'Derretimento_Calotas',   'Agua',             1800,  'Derretimento das calotas polares de gelo de agua'),
    (16, 'Reservatorio_Norte',     'Agua',              300,  'Formacao de reservatorio liquido na regiao polar norte'),
    (17, 'Reservatorio_Sul',       'Agua',              350,  'Formacao de reservatorio liquido na regiao polar sul'),
    (18, 'Rede_Hidrologica',       'Agua',              600,  'Rede hidrologica basica conectando reservatorios'),
    (19, 'Cianobacterias_Alpha',   'Biologia',          200,  'Introducao de cianobacterias resistentes a radiacao UV'),
    (20, 'Cianobacterias_Beta',    'Biologia',          400,  'Expansao em larga escala das colonias de cianobacterias'),
    (21, 'Producao_O2_Inicial',    'Biologia',          100,  'Inicio mensuravel de producao biologica de O2'),
    (22, 'Liquens_Pioneiros',      'Biologia',          300,  'Introducao de liquens e musgos extremofilos'),
    (23, 'Solo_Basico',            'Biologia',          500,  'Formacao de solo basico cultivavel via decomposicao biologica'),
    (24, 'Habitat_Alpha',          'Colonizacao',      1500,  'Primeiro habitat pressurizado permanente (Dome Alpha)'),
    (25, 'Habitat_Beta',           'Colonizacao',      1200,  'Segunda base habitavel conectada ao Habitat Alpha'),
    (26, 'Agricultura_Basica',     'Colonizacao',       600,  'Agricultura basica em ambiente controlado (indoor farming)'),
    (27, 'Colonizacao_100',        'Colonizacao',       200,  'Colonia humana de 100 pessoas permanentemente estabelecida'),
    (28, 'Plantas_Superiores',     'Expansao',          800,  'Introducao de arvores e plantas superiores ao solo marciano'),
    (29, 'O2_10pct',               'Expansao',         2000,  'O2 atmosferico atinge 10% (pressao parcial ~ 2 kPa)'),
    (30, 'Ciclo_Hidrologico',      'Expansao',         1500,  'Ciclo hidrologico basico funcionando (evaporacao + chuva)'),
    (31, 'Controle_Tempestades',   'Expansao',          700,  'Sistema de controle e atenuacao de tempestades de areia'),
    (32, 'Industria_Local',        'Expansao',         1000,  'Industria local de producao, manutencao e extracao de recursos'),
    (33, 'Colonizacao_10000',      'Expansao',          500,  'Colonia humana de 10.000 pessoas — autossuficiencia parcial'),
    (34, 'O2_21pct',               'Terraformacao',    5000,  'O2 atinge 21% — atmosfera respiravel sem traje espacial'),
    (35, 'Pressao_Habitavel',      'Terraformacao',    4000,  'Pressao habitavel sem traje (101 kPa — equivalente a Terra)'),
    (36, 'Temperatura_Positiva',   'Terraformacao',    3500,  'Temperatura media positiva entre +10 C e +20 C'),
    (37, 'Ecossistema_Sustentavel','Terraformacao',    2500,  'Ecossistema planetario auto-sustentavel estabelecido'),
    (38, 'Marte_Habitavel',        'Objetivo Final',      0,  'MARTE TERRAFORMADO — Planeta plenamente habitavel pela humanidade'),
]

EDGES = [
    ('Marte_Inicial',         'Missao_Reconhecimento',  50),
    ('Marte_Inicial',         'Satelite_Mapeamento',    80),
    ('Missao_Reconhecimento', 'Gerador_Nuclear_Alpha',  500),
    ('Satelite_Mapeamento',   'Gerador_Nuclear_Alpha',  500),
    ('Gerador_Nuclear_Alpha', 'Gerador_Nuclear_Beta',   450),
    ('Gerador_Nuclear_Alpha', 'Espelho_Solar_Orbital',  800),
    ('Gerador_Nuclear_Alpha', 'Aquecimento_Fase1',      1200),
    ('Gerador_Nuclear_Beta',  'Liberacao_CO2_Norte',    600),
    ('Gerador_Nuclear_Beta',  'Liberacao_CO2_Sul',      700),
    ('Espelho_Solar_Orbital', 'Aquecimento_Fase1',      1200),
    ('Aquecimento_Fase1',     'Liberacao_CO2_Norte',    600),
    ('Aquecimento_Fase1',     'Liberacao_CO2_Sul',      700),
    ('Liberacao_CO2_Norte',   'Pressao_1pct',           900),
    ('Liberacao_CO2_Sul',     'Pressao_1pct',           900),
    ('Pressao_1pct',          'Pressao_5pct',           1500),
    ('Pressao_1pct',          'Campo_Magnetico',        2000),
    ('Pressao_5pct',          'Pressao_20pct',          3000),
    ('Pressao_5pct',          'Escudo_Radiacao',        400),
    ('Campo_Magnetico',       'Aquecimento_Fase2',      2500),
    ('Campo_Magnetico',       'Derretimento_Calotas',   1800),
    ('Escudo_Radiacao',       'Habitat_Alpha',          1500),
    ('Aquecimento_Fase2',     'Derretimento_Calotas',   1800),
    ('Aquecimento_Fase2',     'Temperatura_Positiva',   3500),
    ('Derretimento_Calotas',  'Reservatorio_Norte',     300),
    ('Derretimento_Calotas',  'Reservatorio_Sul',       350),
    ('Reservatorio_Norte',    'Rede_Hidrologica',       600),
    ('Reservatorio_Sul',      'Rede_Hidrologica',       600),
    ('Pressao_20pct',         'Cianobacterias_Alpha',   200),
    ('Rede_Hidrologica',      'Cianobacterias_Alpha',   200),
    ('Cianobacterias_Alpha',  'Cianobacterias_Beta',    400),
    ('Cianobacterias_Beta',   'Producao_O2_Inicial',    100),
    ('Cianobacterias_Beta',   'Liquens_Pioneiros',      300),
    ('Producao_O2_Inicial',   'Liquens_Pioneiros',      300),
    ('Liquens_Pioneiros',     'Solo_Basico',            500),
    ('Solo_Basico',           'Agricultura_Basica',     600),
    ('Solo_Basico',           'Plantas_Superiores',     800),
    ('Habitat_Alpha',         'Habitat_Beta',           1200),
    ('Habitat_Alpha',         'Colonizacao_100',        200),
    ('Habitat_Beta',          'Colonizacao_100',        200),
    ('Agricultura_Basica',    'Colonizacao_100',        200),
    ('Colonizacao_100',       'Industria_Local',        1000),
    ('Industria_Local',       'Colonizacao_10000',      500),
    ('Plantas_Superiores',    'O2_10pct',               2000),
    ('Producao_O2_Inicial',   'O2_10pct',               2000),
    ('Rede_Hidrologica',      'Ciclo_Hidrologico',      1500),
    ('Plantas_Superiores',    'Ciclo_Hidrologico',      1500),
    ('Pressao_20pct',         'Controle_Tempestades',   700),
    ('O2_10pct',              'O2_21pct',               5000),
    ('Pressao_20pct',         'Pressao_Habitavel',      4000),
    ('Ciclo_Hidrologico',     'Temperatura_Positiva',   3500),
    ('O2_21pct',              'Ecossistema_Sustentavel', 2500),
    ('Pressao_Habitavel',     'Ecossistema_Sustentavel', 2500),
    ('Temperatura_Positiva',  'Ecossistema_Sustentavel', 2500),
    ('Controle_Tempestades',  'Ecossistema_Sustentavel', 2500),
    ('Ecossistema_Sustentavel','Marte_Habitavel',       0),
    ('Colonizacao_10000',     'Marte_Habitavel',        0),
]

def build_technical_pdf():
    s = S()
    story = []

    story.append(PageBreak())

    story.append(Paragraph('Sumario', s['toch']))
    toc = [
        ('1.', 'Definicao do Problema', '3'),
        ('2.', 'Estrutura do Grafo — 39 Vertices', '4'),
        ('3.', 'Visualizacao do Grafo', '7'),
        ('4.', 'Algoritmo de Dijkstra', '8'),
        ('5.', 'Logica de Resolucao do Problema', '10'),
        ('6.', 'Funcoes def — Arquitetura Funcional', '12'),
        ('7.', 'Repositorio GitHub', '13'),
        ('',   'Conclusao e Referencias', '14'),
    ]
    for num, title, page in toc:
        row_data = [
            Paragraph(f'<b>{num}</b>' if num else '', ParagraphStyle('_n',
                fontName='Helvetica-Bold', fontSize=10.5, textColor=MARS_RED, leading=14)),
            Paragraph(title, s['toc']),
            Paragraph(page, ParagraphStyle('_p', fontName='Helvetica', fontSize=10,
                textColor=GRAY, alignment=TA_RIGHT, leading=14)),
        ]
        toc_table = Table([row_data], colWidths=[1*cm, 12.5*cm, 2*cm])
        toc_table.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LINEBELOW', (0,0), (-1,-1), 0.3, BORDER),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(toc_table)
    story.append(Spacer(1, 6))

    story.extend(info_box(
        'Sobre este Documento',
        'Esta documentacao tecnica descreve o projeto TerraPath na integra, atendendo '
        'aos 7 requisitos da disciplina de Programacao Dinamica da FIAP. O documento '
        'cobre desde a definicao formal do problema, passando pela modelagem em grafo '
        'com 39 vertices e 56 arestas, ate a implementacao completa em Python com Flask.',
        s))
    story.append(PageBreak())

    story.extend(h1('1', 'Definicao do Problema', s))
    story.extend(h2('1.1', 'Contexto: Terraformacao de Marte', s))
    story.append(Paragraph(
        'A terraformacao de Marte consiste em modificar sistematicamente o ambiente '
        'marciano para tornar o planeta habitavel por seres humanos sem auxilio de '
        'equipamentos de sobrevivencia. Este e um dos maiores projetos de engenharia '
        'jamais concebidos — estimativas apontam para uma duracao de 100 a 1000 anos '
        'e custos energeticos na ordem de petajoules. Ao contrario de rotas espaciais '
        'tradicionais (onde otimizar Delta-V e suficiente), a terraformacao envolve '
        'centenas de processos interdependentes onde a <b>ordem de execucao e tao '
        'critica quanto a execucao em si</b>.', s['body']))

    story.extend(h2('1.2', 'Formulacao Formal do Problema', s))
    story.append(Paragraph(
        'O TerraPath modela o planejamento da terraformacao como um <b>problema de '
        'caminho minimo em grafo direcionado ponderado</b>. A formulacao e:', s['body']))

    math_items = [
        ('G = (V, E, w)', 'Grafo direcionado e ponderado'),
        ('V = {v0, v1, ..., v38}', 'Conjunto de 39 vertices (estagios de terraformacao)'),
        ('E ⊆ V × V', 'Arestas direcionadas representando pre-requisitos entre estagios'),
        ('w : E → R+', 'Funcao de peso — custo energetico em TeraJoules (TJ)'),
        ('s = Marte_Inicial', 'Vertice de origem (estado inicial de Marte)'),
        ('t = Marte_Habitavel', 'Vertice de destino (Marte plenamente terraformado)'),
        ('min Σ w(u,v)', 'Objetivo: minimizar o custo energetico total da sequencia'),
    ]
    for expr, desc in math_items:
        row = Table([[
            Paragraph(expr, ParagraphStyle('_me', fontName='Courier', fontSize=9,
                textColor=MARS_RED, leading=12)),
            Paragraph(f'— {desc}', ParagraphStyle('_md', fontName='Helvetica', fontSize=9.5,
                textColor=MID_GRAY, leading=12)),
        ]], colWidths=[5.5*cm, 10*cm])
        row.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('BACKGROUND', (0,0), (0,-1), ORANGE_BG),
            ('LINEBEFORE', (0,0), (0,-1), 2, MARS_RED),
        ]))
        story.append(row)
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 8))
    story.extend(h2('1.3', 'Relevancia da Programacao Dinamica', s))
    story.append(Paragraph(
        'O Algoritmo de Dijkstra e uma instancia classica de Programacao Dinamica. '
        'Sua corretude baseia-se diretamente no <b>Principio de Otimalidade de Bellman</b>: '
        'qualquer subcaminho de um caminho otimo e tambem otimo. Isso permite que o '
        'algoritmo construa a solucao global otima a partir de subproblemas otimos locais, '
        'caracteristica definidora da PD.', s['body']))

    pd_table = Table([
        [Paragraph('Componente PD', s['th']),
         Paragraph('Equivalente no TerraPath', s['th'])],
        [Paragraph('Subproblema', s['td']),
         Paragraph('Qual e o menor custo para ativar o estagio X?', s['td'])],
        [Paragraph('Transicao', s['tdm']),
         Paragraph('dp[v] = min(dp[u] + w(u,v))   para todo (u,v) em E', s['tdm'])],
        [Paragraph('Caso base', s['tdm']),
         Paragraph('dp[Marte_Inicial] = 0', s['tdm'])],
        [Paragraph('Objetivo', s['td']),
         Paragraph('dp[Marte_Habitavel] — menor custo ate o estado final', s['td'])],
        [Paragraph('Complexidade', s['td']),
         Paragraph('O((V+E) log V) = O((39+56) x log 39) ≈ O(620)', s['td'])],
    ], colWidths=[4.5*cm, 11*cm])
    pd_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SPACE_BLUE),
        ('BACKGROUND', (0,1), (-1,1), LIGHT_GRAY),
        ('BACKGROUND', (0,2), (-1,2), WHITE),
        ('BACKGROUND', (0,3), (-1,3), LIGHT_GRAY),
        ('BACKGROUND', (0,4), (-1,4), WHITE),
        ('BACKGROUND', (0,5), (-1,5), LIGHT_GRAY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(pd_table)
    story.append(Paragraph('Tabela 1.1 — Mapeamento dos componentes de PD no TerraPath', s['caption']))
    story.append(PageBreak())

    story.extend(h1('2', 'Estrutura do Grafo — 39 Vertices', s))
    story.extend(h2('2.1', 'Modelagem e Propriedades', s))
    story.append(Paragraph(
        'O grafo do TerraPath e um <b>DAG (Directed Acyclic Graph)</b> — grafo direcionado '
        'e aciclico — com 39 vertices distribuidos em 9 fases de terraformacao e 56 arestas '
        'direcionadas representando pre-requisitos. A ausencia de ciclos garante que o '
        'Dijkstra encontrara sempre a solucao globalmente otima.', s['body']))

    story.extend(badge_row([
        ('Vertices |V|', '39'),
        ('Arestas |E|', '56'),
        ('Fases', '9'),
        ('Tipo', 'DAG'),
    ], s))

    story.extend(h2('2.2', 'Tabela Completa de Vertices', s))
    story.append(Paragraph(
        'Os 39 vertices abaixo representam todos os estagios da terraformacao, '
        'distribuidos por fase, com seus respectivos custos de ativacao em TeraJoules (TJ):',
        s['body']))

    node_header = [
        Paragraph('ID', s['th']),
        Paragraph('Nome do Vertice', s['th']),
        Paragraph('Fase', s['th']),
        Paragraph('Custo (TJ)', s['th']),
    ]
    node_rows = [node_header]
    phase_bg = {
        'Estado Inicial': HexColor('#F1F5F9'),
        'Preparacao':     HexColor('#EFF6FF'),
        'Energia':        HexColor('#FFF7ED'),
        'Atmosfera':      HexColor('#F0FDF4'),
        'Protecao':       HexColor('#FDF4FF'),
        'Temperatura':    HexColor('#FFFBEB'),
        'Agua':           HexColor('#EFF6FF'),
        'Biologia':       HexColor('#F0FDF4'),
        'Colonizacao':    HexColor('#FFF1F2'),
        'Expansao':       HexColor('#F5F3FF'),
        'Terraformacao':  HexColor('#FEF2F2'),
        'Objetivo Final': HexColor('#F0FDF4'),
    }
    for nid, nome, fase, custo, _ in NODES:
        bg = phase_bg.get(fase, LIGHT_GRAY)
        cost_str = f'{custo:,}'.replace(',', '.') + ' TJ' if custo > 0 else '0 TJ'
        row = [
            Paragraph(str(nid), ParagraphStyle('_nc', fontName='Helvetica-Bold',
                fontSize=8, textColor=SPACE_BLUE, alignment=TA_CENTER, leading=11)),
            Paragraph(nome, s['tdm']),
            Paragraph(fase, s['td']),
            Paragraph(cost_str, ParagraphStyle('_cost', fontName='Helvetica-Bold',
                fontSize=8, textColor=MARS_RED if custo > 1000 else GREEN_MID,
                alignment=TA_RIGHT, leading=11)),
        ]
        style_row = [
            ('BACKGROUND', (0, len(node_rows)), (-1, len(node_rows)), bg),
        ]
        node_rows.append(row)

    node_table = Table(node_rows, colWidths=[1*cm, 5.2*cm, 3.2*cm, 2.1*cm], repeatRows=1)
    ts = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SPACE_BLUE),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, WHITE]),
    ])
    for i, (nid, _, fase, _, _) in enumerate(NODES, 1):
        if fase == 'Objetivo Final':
            ts.add('BACKGROUND', (0,i), (-1,i), HexColor('#DCFCE7'))
        elif fase == 'Estado Inicial':
            ts.add('BACKGROUND', (0,i), (-1,i), HexColor('#F0F9FF'))
    node_table.setStyle(ts)
    story.append(node_table)
    story.append(Paragraph('Tabela 2.1 — Todos os 39 vertices do grafo TerraPath', s['caption']))
    story.append(PageBreak())

    story.extend(h2('2.3', 'Tabela de Arestas (Pre-requisitos + Custos)', s))
    story.append(Paragraph(
        'Cada aresta (u → v, w) indica que o estagio v so pode ser iniciado apos '
        'a conclusao de u, com custo de transicao w em TeraJoules:', s['body']))

    edge_header = [
        Paragraph('Origem', s['th']),
        Paragraph('Destino', s['th']),
        Paragraph('Custo TJ', s['th']),
    ]
    edge_rows = [edge_header]
    for i, (orig, dest, custo) in enumerate(EDGES):
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE
        edge_rows.append([
            Paragraph(orig, s['tdm']),
            Paragraph(dest, s['tdm']),
            Paragraph(f'{custo:,}'.replace(',','.'), ParagraphStyle('_ew',
                fontName='Helvetica-Bold', fontSize=8,
                textColor=MARS_RED if custo >= 2000 else MID_GRAY,
                alignment=TA_RIGHT, leading=11)),
        ])

    edge_table = Table(edge_rows, colWidths=[6*cm, 6*cm, 2*cm], repeatRows=1)
    edge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), TEAL),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, WHITE]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(edge_table)
    story.append(Paragraph('Tabela 2.2 — 56 arestas direcionadas do grafo TerraPath', s['caption']))
    story.append(PageBreak())

    story.extend(h1('3', 'Visualizacao do Grafo', s))
    story.extend(h2('3.1', 'Tecnologias de Plotagem', s))
    story.append(Paragraph(
        'O TerraPath implementa duas camadas de visualizacao do grafo, servidas '
        'diretamente pela aplicacao Flask:', s['body']))

    viz_data = [
        [Paragraph('Tipo', s['th']), Paragraph('Tecnologia', s['th']),
         Paragraph('Caracteristicas', s['th'])],
        [Paragraph('Estatica (PNG)', s['td']),
         Paragraph('NetworkX + Matplotlib', s['tdm']),
         Paragraph('Layout hierarquico por fase, nos coloridos por categoria, '
                   'espessura das arestas proporcional ao custo', s['td'])],
        [Paragraph('Interativa (Web)', s['td']),
         Paragraph('Plotly + vis.js', s['tdm']),
         Paragraph('Exploracao interativa, hover com detalhes, animacao '
                   'do Dijkstra passo a passo, destaque do caminho otimo', s['td'])],
        [Paragraph('API (JSON)', s['td']),
         Paragraph('Flask REST', s['tdm']),
         Paragraph('Endpoint /api/graph que retorna o grafo completo em '
                   'formato JSON para consumo pelo frontend', s['td'])],
    ]
    viz_table = Table(viz_data, colWidths=[2.5*cm, 4*cm, 9*cm])
    viz_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SPACE_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, WHITE, LIGHT_GRAY]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(viz_table)
    story.append(Spacer(1, 10))

    story.extend(h2('3.2', 'Implementacao: plot_grafo()', s))
    story.append(Paragraph('Trecho da funcao de plotagem estatica com NetworkX:', s['bl']))
    story.extend(code_block(
'''def plot_grafo(grafo_dict, caminho_otimo=None, salvar_em=None):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.DiGraph()
    for no, vizinhos in grafo_dict.items():
        for custo, vizinho in vizinhos:
            G.add_edge(no, vizinho, weight=custo)

    # Layout hierarquico por fase de terraformacao
    pos = gerar_posicoes_por_fase(G)

    # Colorir nos por fase
    cores_nos = [COR_FASE[obter_fase(n)] for n in G.nodes()]

    # Largura das arestas proporcional ao custo (normalizado)
    pesos = [G[u][v]['weight'] for u, v in G.edges()]
    larguras = [0.5 + 3 * (p / max(pesos)) for p in pesos]

    fig, ax = plt.subplots(figsize=(20, 14))
    nx.draw_networkx(G, pos, ax=ax, node_color=cores_nos,
                     width=larguras, with_labels=True,
                     node_size=500, font_size=6)

    # Destacar caminho otimo
    if caminho_otimo:
        arestas_caminho = list(zip(caminho_otimo, caminho_otimo[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=arestas_caminho,
                               edge_color='#C1440E', width=3, ax=ax)

    if salvar_em:
        plt.savefig(salvar_em, dpi=150, bbox_inches='tight')
    return fig''', s))

    story.extend(info_box(
        'Nota sobre o Plot na Aplicacao Web',
        'Na interface Flask, a funcao plot_grafo() e chamada pelo endpoint /plot e '
        'retorna a imagem PNG como bytes (via io.BytesIO), exibida diretamente na '
        'pagina HTML sem necessidade de salvar em disco. O grafo interativo '
        'complementar e gerado com Plotly e renderizado como HTML embed.',
        s, bg=GREEN_BG, tc=GREEN_MID, border=HexColor('#16A34A')))
    story.append(PageBreak())

    story.extend(h1('4', 'Algoritmo de Dijkstra', s))
    story.extend(h2('4.1', 'Fundamentacao Teorica', s))
    story.append(Paragraph(
        'Proposto por Edsger W. Dijkstra em 1959, o algoritmo resolve o problema de '
        'caminho minimo de unica origem (SSSP — Single Source Shortest Path) em '
        'grafos com pesos nao-negativos. Sua complexidade com min-heap e '
        '<b>O((V + E) log V)</b>, tornando-o ideal para o grafo TerraPath.', s['body']))

    story.append(Paragraph(
        'O algoritmo e correto porque o <b>Principio de Otimalidade de Bellman</b> '
        'garante que: se o caminho otimo de s a t passa pelo vertice v, entao o '
        'subcaminho de s a v tambem e otimo. A prova e por inducao sobre o numero '
        'de vertices finalizados.', s['body']))

    story.extend(h2('4.2', 'Aplicacao ao TerraPath', s))
    algo_data = [
        [Paragraph('Elemento', s['th']), Paragraph('No Algoritmo Classico', s['th']),
         Paragraph('No TerraPath', s['th'])],
        [Paragraph('Vertices', s['td']), Paragraph('Nos do grafo', s['td']),
         Paragraph('Estagios de terraformacao', s['td'])],
        [Paragraph('Arestas', s['td']), Paragraph('Conexoes entre nos', s['td']),
         Paragraph('Pre-requisitos entre estagios', s['td'])],
        [Paragraph('Pesos', s['td']), Paragraph('Custos genericos', s['td']),
         Paragraph('Custo energetico em TeraJoules', s['td'])],
        [Paragraph('Origem s', s['td']), Paragraph('Vertice inicial', s['td']),
         Paragraph('Marte_Inicial (custo=0)', s['td'])],
        [Paragraph('Destino t', s['td']), Paragraph('Vertice final', s['td']),
         Paragraph('Marte_Habitavel', s['td'])],
        [Paragraph('Resultado', s['td']), Paragraph('Caminho de menor custo', s['td']),
         Paragraph('Sequencia de menor energia para terraform', s['td'])],
    ]
    algo_table = Table(algo_data, colWidths=[3*cm, 5.5*cm, 7*cm])
    algo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), TEAL),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, WHITE]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(algo_table)
    story.append(Spacer(1, 10))

    story.extend(h2('4.3', 'Implementacao Completa em Python', s))
    story.extend(code_block(
'''import heapq

def dijkstra(grafo, inicio, fim):
    # Inicializacao: distancia infinita para todos os vertices
    distancias   = {no: float('inf') for no in grafo}
    predecessores = {no: None        for no in grafo}
    distancias[inicio] = 0

    # Min-heap: (custo_acumulado, vertice_atual)
    fila = [(0, inicio)]
    visitados = set()

    while fila:
        custo_atual, no_atual = heapq.heappop(fila)

        # Vertice ja finalizado — ignorar entrada duplicada
        if no_atual in visitados:
            continue
        visitados.add(no_atual)

        # Destino alcancado — terminar cedo (early exit)
        if no_atual == fim:
            break

        # Relaxamento das arestas saindo de no_atual
        for custo_aresta, vizinho in grafo.get(no_atual, []):
            novo_custo = custo_atual + custo_aresta
            if novo_custo < distancias[vizinho]:          # Relaxamento
                distancias[vizinho]    = novo_custo
                predecessores[vizinho] = no_atual
                heapq.heappush(fila, (novo_custo, vizinho))

    # Reconstrucao do caminho via predecessores
    if distancias[fim] == float('inf'):
        return float('inf'), []   # Sem caminho

    caminho = []
    no = fim
    while no is not None:
        caminho.append(no)
        no = predecessores[no]
    caminho.reverse()

    return distancias[fim], caminho''', s))

    story.extend(h2('4.4', 'Trace de Execucao — Exemplo Simplificado', s))
    story.append(Paragraph(
        'Execucao do Dijkstra para o subcaminho '
        'Marte_Inicial → Pressao_1pct:', s['bl']))

    trace_data = [
        [Paragraph('Iter.', s['th']), Paragraph('Vertice Visitado', s['th']),
         Paragraph('Custo Acum.', s['th']), Paragraph('Nos Relaxados (novo custo)', s['th'])],
        [Paragraph('1', s['tdc']), Paragraph('Marte_Inicial', s['tdm']),
         Paragraph('0 TJ', s['tdc']),
         Paragraph('Missao_Reconhecimento→50, Satelite_Mapeamento→80', s['tdm'])],
        [Paragraph('2', s['tdc']), Paragraph('Missao_Reconhecimento', s['tdm']),
         Paragraph('50 TJ', s['tdc']),
         Paragraph('Gerador_Nuclear_Alpha→550', s['tdm'])],
        [Paragraph('3', s['tdc']), Paragraph('Satelite_Mapeamento', s['tdm']),
         Paragraph('80 TJ', s['tdc']),
         Paragraph('Gerador_Nuclear_Alpha: 550 (sem melhora)', s['tdm'])],
        [Paragraph('4', s['tdc']), Paragraph('Gerador_Nuclear_Alpha', s['tdm']),
         Paragraph('550 TJ', s['tdc']),
         Paragraph('Aquecimento_Fase1→1750, Gerador_Beta→1000', s['tdm'])],
        [Paragraph('5', s['tdc']), Paragraph('Gerador_Nuclear_Beta', s['tdm']),
         Paragraph('1000 TJ', s['tdc']),
         Paragraph('Liberacao_CO2_Norte→1600, Liberacao_CO2_Sul→1700', s['tdm'])],
        [Paragraph('...', s['tdc']), Paragraph('...', s['tdm']),
         Paragraph('...', s['tdc']), Paragraph('...', s['tdm'])],
        [Paragraph('N', s['tdc']), Paragraph('Pressao_1pct', s['tdm']),
         Paragraph('FINAL', s['tdc']),
         Paragraph('Caminho otimo encontrado — custo total computado', s['tdm'])],
    ]
    trace_table = Table(trace_data, colWidths=[1*cm, 4*cm, 2.2*cm, 8.3*cm])
    trace_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SPACE_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, WHITE]),
        ('BACKGROUND', (0,7), (-1,7), HexColor('#DCFCE7')),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(trace_table)
    story.append(Paragraph('Tabela 4.1 — Trace do algoritmo de Dijkstra no TerraPath', s['caption']))
    story.append(PageBreak())

    story.extend(h1('5', 'Logica de Resolucao do Problema', s))
    story.extend(h2('5.1', 'Arquitetura da Aplicacao Flask', s))
    story.append(Paragraph(
        'O TerraPath e uma aplicacao web construida com Flask, organizada em '
        'modulos funcionais independentes e bem documentados:', s['body']))

    arch_data = [
        [Paragraph('Modulo', s['th']), Paragraph('Arquivo', s['th']),
         Paragraph('Responsabilidade', s['th'])],
        [Paragraph('Grafo', s['td']), Paragraph('graph_model.py', s['tdm']),
         Paragraph('Construcao, validacao e serializacao do grafo DAG', s['td'])],
        [Paragraph('Otimizacao', s['td']), Paragraph('dijkstra.py', s['tdm']),
         Paragraph('Algoritmo de Dijkstra e reconstrucao de caminho', s['td'])],
        [Paragraph('Visualizacao', s['td']), Paragraph('visualization.py', s['tdm']),
         Paragraph('Plot com NetworkX/Matplotlib e Plotly interativo', s['td'])],
        [Paragraph('Web Server', s['td']), Paragraph('app.py', s['tdm']),
         Paragraph('Rotas Flask, API REST, renderizacao de templates', s['td'])],
        [Paragraph('Dados', s['td']), Paragraph('data/graph_data.json', s['tdm']),
         Paragraph('39 vertices e 56 arestas com metadados completos', s['td'])],
        [Paragraph('Templates', s['td']), Paragraph('templates/*.html', s['tdm']),
         Paragraph('Interface web com visualizacao interativa do grafo', s['td'])],
    ]
    arch_table = Table(arch_data, colWidths=[2.5*cm, 4*cm, 9*cm])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SPACE_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, WHITE]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))

    story.extend(h2('5.2', 'Fluxo de Resolucao', s))
    flow_steps = [
        ('1', 'Usuario acessa a interface web (localhost:5000)',
         'Flask serve o template index.html com o grafo renderizado via Plotly'),
        ('2', 'Selecao de origem e destino no grafo interativo',
         'Dropdown populado com os 39 vertices; usuario escolhe ponto inicial e final'),
        ('3', 'Escolha do criterio de otimizacao',
         '3 opcoes: Energia (TJ), Numero de Etapas, ou Indice de Risco Combinado'),
        ('4', 'Chamada ao endpoint POST /otimizar',
         'Frontend envia JSON {origem, destino, criterio} via fetch()'),
        ('5', 'Execucao do Dijkstra no backend',
         'dijkstra(grafo, origem, destino) retorna (custo_total, caminho)'),
        ('6', 'Geracao da visualizacao do caminho',
         'plot_grafo() destaca o caminho otimo em vermelho marciano'),
        ('7', 'Resposta JSON + renderizacao',
         'Frontend exibe: caminho, custo total, detalhes de cada etapa, plot'),
    ]
    for step_num, title, desc in flow_steps:
        row = Table([[
            Table([[Paragraph(step_num, ParagraphStyle('_sn',
                fontName='Helvetica-Bold', fontSize=12, textColor=WHITE,
                alignment=TA_CENTER, leading=16))]],
                colWidths=[0.7*cm],
                style=TableStyle([('BACKGROUND',(0,0),(-1,-1),MARS_RED),
                                  ('TOPPADDING',(0,0),(-1,-1),5),
                                  ('BOTTOMPADDING',(0,0),(-1,-1),5)])),
            Table([
                [Paragraph(title, ParagraphStyle('_st', fontName='Helvetica-Bold',
                    fontSize=10, textColor=DARK_GRAY, leading=13))],
                [Paragraph(desc, ParagraphStyle('_sd', fontName='Helvetica', fontSize=9,
                    textColor=GRAY, leading=12))],
            ], colWidths=[14.1*cm]),
        ]], colWidths=[0.9*cm, 14.1*cm])
        row.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), LIGHT_GRAY),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LINEBELOW', (0,0), (-1,-1), 1, WHITE),
        ]))
        story.append(row)
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 8))
    story.extend(h2('5.3', 'Endpoint Principal — app.py', s))
    story.extend(code_block(
'''@app.route('/otimizar', methods=['POST'])
def otimizar_rota():
    dados    = request.get_json()
    origem   = dados.get('origem',   'Marte_Inicial')
    destino  = dados.get('destino',  'Marte_Habitavel')
    criterio = dados.get('criterio', 'energia')

    grafo  = construir_grafo(criterio=criterio)
    custo, caminho = dijkstra(grafo, origem, destino)

    if not caminho:
        return jsonify({'erro': 'Caminho inexistente entre os vertices'}), 404

    return jsonify({
        'caminho':      caminho,
        'custo_total':  custo,
        'unidade':      obter_unidade(criterio),
        'num_etapas':   len(caminho) - 1,
        'detalhes':     obter_detalhes_etapas(caminho),
        'plot_url':     '/plot?caminho=' + ','.join(caminho),
    })''', s))
    story.append(PageBreak())

    story.extend(h1('6', 'Funcoes def — Arquitetura Funcional', s))
    story.append(Paragraph(
        'O codigo e organizado em funcoes puras e bem documentadas com docstrings '
        'no padrao Google Style. Todas as funcoes recebem tipos explicitos e '
        'retornam valores previstos:', s['body']))

    funcs = [
        ('graph_model.py',  'construir_grafo(criterio)',
         'dict', 'Constroi e retorna o grafo DAG completo com 39 nos e 56 arestas, '
                 'ponderado pelo criterio selecionado (energia, etapas ou risco)'),
        ('graph_model.py',  'validar_grafo(grafo)',
         'bool', 'Verifica integridade do grafo: aciclicidade, conectividade, '
                 'ausencia de pesos negativos e existencia de origem/destino'),
        ('graph_model.py',  'obter_fase(nome_no)',
         'str',  'Retorna a fase de terraformacao de um vertice pelo nome'),
        ('graph_model.py',  'obter_detalhes_etapas(caminho)',
         'list', 'Retorna lista de dicionarios com detalhes de cada etapa do caminho '
                 '(nome, fase, custo, descricao, custo acumulado)'),
        ('dijkstra.py',     'dijkstra(grafo, inicio, fim)',
         'tuple','Implementacao do algoritmo de Dijkstra com min-heap. Retorna '
                 '(custo_total, caminho) com complexidade O((V+E) log V)'),
        ('dijkstra.py',     'reconstruir_caminho(predecessores, fim)',
         'list', 'Reconstroi o caminho otimo a partir do dicionario de predecessores '
                 'gerado pelo Dijkstra (percurso reverso)'),
        ('dijkstra.py',     'calcular_custo_caminho(grafo, caminho)',
         'float','Calcula e verifica o custo total de um caminho dado, somando '
                 'os pesos de todas as arestas percorridas'),
        ('visualization.py','plot_grafo(grafo_dict, caminho_otimo, salvar_em)',
         'Figure','Gera o plot estatico do grafo com NetworkX + Matplotlib. '
                  'Layout hierarquico por fase, nos coloridos, arestas ponderadas'),
        ('visualization.py','gerar_posicoes_por_fase(G)',
         'dict', 'Calcula as posicoes x,y de cada no no layout hierarquico, '
                 'organizando as fases em colunas verticais equidistantes'),
        ('visualization.py','plot_interativo(grafo_dict, caminho_otimo)',
         'str',  'Gera HTML do grafo interativo com Plotly para embed no template'),
        ('app.py',          'otimizar_rota()',
         'Response','Endpoint POST /otimizar — recebe JSON, executa Dijkstra, '
                    'retorna caminho e custo otimo em JSON'),
        ('app.py',          'obter_grafo_json()',
         'Response','Endpoint GET /api/graph — serializa e retorna o grafo '
                    'completo em JSON para consumo pelo frontend JavaScript'),
        ('app.py',          'gerar_plot()',
         'Response','Endpoint GET /plot — retorna PNG do grafo como bytes via '
                    'io.BytesIO, com caminho otimo destacado se fornecido'),
    ]

    func_header = [Paragraph('Modulo', s['th']), Paragraph('Funcao', s['th']),
                   Paragraph('Retorno', s['th']), Paragraph('Descricao', s['th'])]
    func_rows = [func_header]
    for i, (modulo, func, ret, desc) in enumerate(funcs):
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE
        func_rows.append([
            Paragraph(modulo, s['tdm']),
            Paragraph(func, s['tdm']),
            Paragraph(ret, ParagraphStyle('_rt', fontName='Courier', fontSize=7.5,
                textColor=PURPLE, leading=10)),
            Paragraph(desc, s['td']),
        ])

    func_table = Table(func_rows, colWidths=[3*cm, 4.2*cm, 1.5*cm, 6.8*cm], repeatRows=1)
    func_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SPACE_BLUE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, WHITE]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(func_table)
    story.append(Paragraph('Tabela 6.1 — Todas as funcoes def do projeto TerraPath', s['caption']))
    story.append(PageBreak())

    story.extend(h1('7', 'Repositorio GitHub', s))
    story.extend(h2('7.1', 'Estrutura do Repositorio', s))
    story.extend(code_block(
'''terrapath/
├── README.md                   # Documentacao principal com badges
├── requirements.txt            # Dependencias Python (Flask, NetworkX, Plotly...)
├── .gitignore
│
├── app.py                      # Servidor Flask — ponto de entrada da aplicacao
├── graph_model.py              # Construcao e validacao do grafo DAG
├── dijkstra.py                 # Algoritmo de Dijkstra + utilitarios de caminho
├── visualization.py            # Plot com NetworkX, Matplotlib e Plotly
│
├── data/
│   └── graph_data.json         # 39 vertices e 56 arestas com metadados completos
│
├── templates/
│   ├── index.html              # Interface principal com grafo interativo
│   └── result.html             # Exibicao detalhada do caminho otimo
│
├── static/
│   ├── css/
│   │   └── style.css           # Estilos da interface web (tema espacial)
│   └── js/
│       └── visualization.js    # Logica de interacao com o grafo no frontend
│
├── tests/
│   ├── test_graph.py           # Testes unitarios do modelo de grafo
│   ├── test_dijkstra.py        # Testes do algoritmo (corretude + edge cases)
│   └── test_routes.py          # Testes dos endpoints Flask
│
└── docs/
    ├── doc_tecnico.pdf         # Este documento
    └── doc_geral.pdf           # Documentacao interdisciplinar''', s))

    story.extend(h2('7.2', 'Como Executar', s))
    story.extend(code_block(
'''# 1. Clonar o repositorio
git clone https://github.com/usuario/terrapath.git
cd terrapath

# 2. Criar ambiente virtual e instalar dependencias
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\\Scripts\\activate          # Windows

pip install -r requirements.txt

# 3. Executar a aplicacao Flask
python app.py

# 4. Acessar no navegador
# http://localhost:5000

# 5. Executar testes
python -m pytest tests/ -v''', s))

    story.extend(h2('7.3', 'Documentacao no Codigo', s))
    story.append(Paragraph(
        'Cada funcao possui docstring completo no padrao Google Style com Args, '
        'Returns, Raises e Examples. O README.md inclui: descricao do projeto, '
        'badges de linguagem e licenca, instrucoes de instalacao, exemplos de uso '
        'da API, descricao do grafo, e referencias bibliograficas.', s['body']))
    story.append(PageBreak())

    story.extend(h1('', 'Conclusao', s))
    story.append(Paragraph(
        'O TerraPath demonstra que o Algoritmo de Dijkstra — uma das aplicacoes '
        'mais elegantes da Programacao Dinamica — pode ser diretamente aplicado a '
        'problemas reais e complexos de planejamento sequencial com restricoes de '
        'dependencia, indo muito alem dos classicos problemas de roteamento em mapas.', s['body']))
    story.append(Paragraph(
        'A solucao atende aos 7 requisitos da disciplina: (1) problema real e '
        'bem definido, (2) grafo com 39 vertices e 56 arestas, (3) plotagem '
        'estatica e interativa, (4) Dijkstra implementado do zero, (5) logica '
        'completa em Flask, (6) 13 funcoes def documentadas, e (7) repositorio '
        'GitHub com README e testes.', s['body']))

    story.extend(h1('', 'Referencias', s))
    refs = [
        'DIJKSTRA, E. W. A note on two problems in connexion with graphs. '
        'Numerische Mathematik, v. 1, p. 269-271, 1959.',
        'BELLMAN, R. On a Routing Problem. Quarterly of Applied Mathematics, '
        'v. 16, p. 87-90, 1958.',
        'ZUBRIN, R. The Case for Mars. Free Press, 1996.',
        'NASA. Mars Terraforming Technical Study. Technical Report, 2018. '
        'Disponivel em: https://www.nasa.gov',
        'McKAY, C. P.; TOON, O. B.; KASTING, J. F. Making Mars habitable. '
        'Nature, v. 352, p. 489-496, 1991.',
        'CORMEN, T. H. et al. Introduction to Algorithms. 4. ed. MIT Press, 2022.',
        'NETWORKX DEVELOPERS. NetworkX Documentation. '
        'Disponivel em: https://networkx.org',
    ]
    for i, ref in enumerate(refs, 1):
        story.append(Paragraph(f'[{i}]  {ref}',
            ParagraphStyle('_ref', fontName='Helvetica', fontSize=9,
                textColor=MID_GRAY, leading=13, leftIndent=20,
                firstLineIndent=-20, spaceAfter=5)))

    path = 'TerraPath_Tecnico_ProgDinamica.pdf'
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.2*cm, bottomMargin=1.8*cm,
        title='TerraPath — Documentacao Tecnica | Programacao Dinamica',
        author='FIAP Global Solution 2026',
        subject='Grafos, Dijkstra, Programacao Dinamica, Terraformacao',
    )
    doc.build(story,
              onFirstPage=on_cover,
              onLaterPages=on_pages)
    print(f'[OK] Documento tecnico gerado: {path}')
    return path

def on_pitch_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(SPACE_BLUE)
    canvas.rect(0, 0, W, H, fill=True, stroke=False)
    canvas.setFillColor(HexColor('#0F2744'))
    canvas.rect(0, H * 0.55, W, H * 0.45, fill=True, stroke=False)
    canvas.setFillColor(MARS_RED)
    canvas.rect(2.5*cm, H * 0.47, W - 5*cm, 0.35*cm, fill=True, stroke=False)
    canvas.setFillColor(HexColor('#0F3D4A'))
    canvas.rect(0, 0, W, H * 0.2, fill=True, stroke=False)
    canvas.setFillColor(TEAL)
    canvas.rect(0, H * 0.2, W, 0.12*cm, fill=True, stroke=False)
    canvas.setFillColor(HexColor('#1A3A5C'))
    canvas.circle(W * 0.5, H * 0.75, 4.5*cm, fill=True, stroke=False)
    canvas.setFillColor(HexColor('#C1440E'))
    canvas.circle(W * 0.5, H * 0.75, 3.8*cm, fill=True, stroke=False)
    canvas.setFillColor(HexColor('#D95C25'))
    canvas.circle(W * 0.45, H * 0.8, 1.2*cm, fill=True, stroke=False)
    canvas.setFillColor(HexColor('#932A00'))
    canvas.circle(W * 0.58, H * 0.68, 0.7*cm, fill=True, stroke=False)
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 42)
    canvas.drawCentredString(W * 0.5, H * 0.35, "TERRAPATH")
    canvas.setFont('Helvetica', 16)
    canvas.setFillColor(HexColor('#60A5FA'))
    canvas.drawCentredString(W * 0.5, H * 0.26, "Sequenciador de Terraformacao Marciana")
    canvas.setFont('Helvetica-Bold', 11)
    canvas.setFillColor(HexColor('#FDBA74'))
    canvas.drawCentredString(W * 0.5, H * 0.20, "DOCUMENTACAO EXECUTIVA — PITCH DO PROJETO")
    canvas.restoreState()

def build_pitch_pdf():
    s = S()
    story = []
    
    # 1. Sumario Executivo
    story.append(PageBreak())
    story.append(Paragraph('Sumário Executivo', s['toch']))
    toc = [
        ('1.', 'Entendimento do Problema e a Dor Logística', '2'),
        ('2.', 'Descrição da Solução: TerraPath', '3'),
        ('3.', 'Stakeholders e Parceiros de Negócio', '4'),
        ('4.', 'Backlog do Produto e Casos de Uso', '5'),
        ('5.', 'Papéis da Equipe (Grupo Moskitto)', '6'),
        ('6.', 'Casos de Uso e Fluxo de Interação', '7'),
        ('7.', 'Princípios de UX/UI Aplicados', '8'),
        ('8.', 'Considerações Finais', '9'),
    ]
    for num, title, page in toc:
        row_data = [
            Paragraph(f'<b>{num}</b>', ParagraphStyle('_n', fontName='Helvetica-Bold', fontSize=10.5, textColor=MARS_RED, leading=14)),
            Paragraph(title, s['toc']),
            Paragraph(page, ParagraphStyle('_p', fontName='Helvetica', fontSize=10, textColor=GRAY, alignment=TA_RIGHT, leading=14)),
        ]
        toc_table = Table([row_data], colWidths=[1*cm, 12.5*cm, 2*cm])
        toc_table.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LINEBELOW', (0,0), (-1,-1), 0.3, BORDER),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(toc_table)
    story.append(Spacer(1, 10))
    story.extend(info_box('Visão Geral do Documento', 'Este documento serve como o Pitch Deck oficial do produto TerraPath, delineando o problema logístico da terraformação marciana, as propostas de valor comercial do software (B2G e New Space), levantamento de histórias de usuário, stakeholders envolvidos, metodologias de design aplicadas e a organização da equipe desenvolvedora.', s))

    # 2. Entendimento do Problema
    story.append(PageBreak())
    story.extend(h1('1', 'Entendimento do Problema e a Dor Logística', s))
    story.append(Paragraph('A humanidade atingiu um platô evolutivo na Terra. A expansão multiplanetária deixou de ser apenas exploração científica e tornou-se a única garantia de sobrevivência da espécie a longo prazo. Hoje, corporações como a SpaceX e a NASA abaixam o custo do envio de cargas com a Starship e missões Artemis.', s['body']))
    story.append(Paragraph('No entanto, o maior gargalo atual não é apenas "levar" coisas para Marte, mas sim a orquestração logística da terraformação. Errar a sequência de engenharia — como tentar criar uma hidrosfera antes de estabelecer um escudo magnético contra o vento solar — resulta na perda de bilhões de litros de água e de trilhões de dólares em financiamento.', s['body']))
    story.append(Paragraph('<b>A dor central é:</b> Não existia, até agora, uma ferramenta determinística para prever as dependências encadeadas de projetos de engenharia planetária.', s['body']))

    # 3. Descricao da Solucao
    story.append(PageBreak())
    story.extend(h1('2', 'Descrição da Solução: TerraPath', s))
    story.append(Paragraph('O TerraPath surge como o primeiro motor híbrido de processamento logístico aeroespacial.', s['body']))
    story.append(Paragraph('Ao modelar o ecossistema marciano como um <b>Grafo Direcionado Acíclico (DAG)</b> composto por 39 fases sistêmicas rigorosas (desde "S0: Preparação" até "S9: Habitabilidade Global"), o software traduz o caos da engenharia climática em uma estrutura matemática solucionável.', s['body']))
    story.append(Paragraph('Utilizando o <b>Algoritmo de Dijkstra</b>, o TerraPath funciona como uma bússola digital: ele computa todas as interdependências para encontrar a rota que gasta a menor quantidade de Energia (TeraJoules) ou que se submete ao menor Risco Combinado.', s['body']))
    story.append(Paragraph('<b>Diferencial:</b> O motor possui processamento híbrido. Pode rodar robustamente na nuvem usando Python/Flask para gerar relatórios PDF, ou rodar 100% de graça, localmente no navegador via JavaScript (arquitetura Frozen-Flask), poupando banda em transmissões interplanetárias.', s['body']))

    # 4. Stakeholders
    story.append(PageBreak())
    story.extend(h1('3', 'Stakeholders e Parceiros de Negócio', s))
    story.append(Paragraph('A solução do TerraPath atende a diferentes camadas da indústria espacial global:', s['body']))
    stakeholder_data = [
        [Paragraph('<b>Stakeholder</b>', s['caption']), Paragraph('<b>Papel no Ecossistema do TerraPath</b>', s['caption'])],
        [Paragraph('Agências Governamentais (NASA / ESA)', s['body']), Paragraph('Investidores primários, reguladores e clientes do plano logístico de longuíssimo prazo.', s['body'])],
        [Paragraph('Setor Privado (New Space / SpaceX)', s['body']), Paragraph('Executores táticos e empresas de frete que utilizam a estimativa de energia (TJ) para cobrar pelos lançamentos.', s['body'])],
        [Paragraph('Engenheiros de Missão', s['body']), Paragraph('Usuários diretos do painel web interativo, operando o dashboard para tomadas de decisão.', s['body'])]
    ]
    st_table = Table(stakeholder_data, colWidths=[5*cm, 10.5*cm])
    st_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#1A2234')),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('GRID', (0,0), (-1,-1), 1, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(st_table)

    # 5. Backlog e Casos de Uso
    story.append(PageBreak())
    story.extend(h1('4', 'Backlog do Produto e Casos de Uso', s))
    story.append(Paragraph('O desenvolvimento seguiu práticas ágeis baseadas em levantamento de histórias de usuário (User Stories):', s['body']))
    backlog_data = [
        [Paragraph('<b>Perfil (Como...)</b>', s['caption']), Paragraph('<b>Ação (...Quero...)</b>', s['caption']), Paragraph('<b>Critério de Aceite</b>', s['caption'])],
        [Paragraph('Diretor Financeiro', s['body']), Paragraph('...visualizar a rota de menor custo energético, para não estourar o orçamento.', s['body']), Paragraph('O HUD deve exibir a soma exata de TeraJoules sem erros de cálculo.', s['body'])],
        [Paragraph('Diretor de Segurança', s['body']), Paragraph('...desviar de fases com Risco Alto (ex: manuseio nuclear), para evitar incidentes graves.', s['body']), Paragraph('Filtro de "Risco Combinado" deve recalcular a rota fugindo dos nós críticos.', s['body'])],
        [Paragraph('Engenheiro de Campo', s['body']), Paragraph('...interagir visualmente com o mapa topológico, para prever interdependências da minha etapa.', s['body']), Paragraph('O grafo gerado pelo Cytoscape.js deve ser arrastável e clicável.', s['body'])],
    ]
    bk_table = Table(backlog_data, colWidths=[4*cm, 6.5*cm, 5*cm])
    bk_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#431407')),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('GRID', (0,0), (-1,-1), 1, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(bk_table)

    # 6. Papeis da Equipe
    story.append(PageBreak())
    story.extend(h1('5', 'Papéis da Equipe (Grupo Moskitto)', s))
    story.append(Paragraph('O projeto TerraPath foi projetado e desenvolvido no escopo da Global Solution 2026. A equipe reúne especialistas em diversas áreas da engenharia:', s['body']))
    story.append(Spacer(1, 10))
    story.append(Paragraph('<b>Gabriel Couto Ribeiro (RM: 559579) — Engenheiro de Software</b>', s['body']))
    story.append(Paragraph('Responsável pelo desenvolvimento do algoritmo central de Dijkstra, lógica de programação dinâmica e rotinas pesadas de geração de PDFs no backend.', s['body']))
    story.append(Spacer(1, 5))
    story.append(Paragraph('<b>Gabriel Kato Peres (RM: 560000) — Arquiteto de Soluções</b>', s['body']))
    story.append(Paragraph('Desenhou a arquitetura híbrida (Flask + JS) que permite que a aplicação escale em produção via estáticos usando GitHub Pages e interceptações dinâmicas.', s['body']))
    story.append(Spacer(1, 5))
    story.append(Paragraph('<b>João Vitor de Matos (RM: 559246) — Engenheiro de Dados</b>', s['body']))
    story.append(Paragraph('Modelou formalmente o grafo (DAG) das fases marcianas, levantando os pesos realistas de energia e riscos que populam a Single Source of Truth do projeto.', s['body']))
    story.append(Spacer(1, 5))
    story.append(Paragraph('<b>Marcelo Affonso Fonseca (RM: 559790) — Designer UI/UX</b>', s['body']))
    story.append(Paragraph('Concebeu a identidade Brutalista Sci-Fi do sistema, garantindo clareza cognitiva no painel de interação visual (Cytoscape) e nas folhas de estilo de documentação.', s['body']))

    # 7. Fluxo de Interacao
    story.append(PageBreak())
    story.extend(h1('6', 'Casos de Uso e Fluxos de Interação', s))
    story.append(Paragraph('O fluxo central de navegação da ferramenta prioriza a objetividade científica:', s['body']))
    story.append(Paragraph('<b>1. Acesso Inicial:</b> O engenheiro abre o Simulador Interativo.', s['bullet']))
    story.append(Paragraph('<b>2. Entrada de Parâmetros:</b> Ele insere a Fase Atual do ecossistema e o Objetivo desejado.', s['bullet']))
    story.append(Paragraph('<b>3. Peso Tático:</b> O usuário escolhe minimizar o Risco ou a Energia (TeraJoules).', s['bullet']))
    story.append(Paragraph('<b>4. Processamento:</b> A bússola JS ou Python varre a árvore de 39 nós e 56 arestas conectadas.', s['bullet']))
    story.append(Paragraph('<b>5. Output Visual:</b> O HUD ilumina de azul as arestas ativas no mapa interativo na tela.', s['bullet']))
    story.append(Paragraph('<b>6. Exportação:</b> Para arquivamento ou comitês executivos, o painel gera relatórios em PDF estruturados.', s['bullet']))

    # 8. Principios UX
    story.append(PageBreak())
    story.extend(h1('7', 'Princípios de UX/UI Aplicados', s))
    story.append(Paragraph('Em ferramentas de infraestrutura crítica e defesa civil interplanetária, distração pode custar vidas. Nossos princípios foram:', s['body']))
    story.append(Paragraph('<b>- Design Brutalista Sci-Fi:</b> Uso de cores sólidas ultra-escuras (preto profundo #0a0a0a) cortadas pela cor de destaque "Vermelho Marte" (#ff3300). Elimina-se sombras, gradientes e ruídos visuais. O foco absoluto é nos dados matemáticos da tela.', s['body']))
    story.append(Paragraph('<b>- Tipografia Utilitária:</b> Uso massivo da fonte "Space Mono", que emula os consoles clássicos baseados em sistemas operacionais Unix (tradicionais em engenharia de voo), passando um gatilho psicológico de segurança e frieza tecnológica.', s['body']))
    story.append(Paragraph('<b>- Feedback Responsivo:</b> Alertas em tempo real e visualização interativa em 2D/3D dos nós permitem que o usuário navegue visualmente pelos desafios (Scroll, Drag, Zoom).', s['body']))

    # 9. Consideracoes Finais
    story.append(PageBreak())
    story.extend(h1('8', 'Considerações Finais', s))
    story.append(Paragraph('O TerraPath retira a engenharia planetária do campo da especulação caótica e a amarra rigidamente ao determinismo lógico e computacional. Com uma arquitetura moderna, rápida de escalar, e um core matemático baseada em Teoria dos Grafos, provamos que é possível projetar a sobrevivência interplanetária de maneira estável e orçável.', s['body']))
    story.append(Paragraph('O projeto consolida conhecimentos de Programação Dinâmica, Infraestrutura Web, e Design de Interfaces. Nosso sistema não é apenas um sequenciador logístico para a Global Solution; é a fundação digital para assegurar a imortalidade técnica da humanidade.', s['body']))

    path = 'TerraPath_Executive_Pitch.pdf'
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.2*cm, bottomMargin=1.8*cm,
        title='TerraPath — Documentacao Executiva | Pitch',
        author='Grupo Moskitto',
        subject='Pitch Comercial, Otimizacao, UX Design',
    )
    doc.build(story,
              onFirstPage=on_pitch_cover,
              onLaterPages=on_pages)
    print(f'[OK] Documento executivo (Pitch) gerado: {path}')
    return path


if __name__ == '__main__':
    build_technical_pdf()
    build_pitch_pdf()
