import streamlit as st
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Candidato 2026 - Simulador Eleitoral",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Personalizado para melhor visual
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    .event-box {
        background-color: #e8f4fd;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .victory {
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #28a745;
    }
    .defeat {
        background-color: #f8d7da;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# BANCO DE DADOS DE EVENTOS (EXPANDIDO)
# ============================================================================
EVENTOS = {
    "geral": [
        {
            "titulo": "📺 Debate na Televisão",
            "desc": "Você foi convidado para um debate nacional transmitido ao vivo. Milhões estão assistindo.",
            "icon": "📺",
            "opcoes": [
                {"texto": "Atacar o oponente", "efeito": {"pop": 5, "caixa": 0, "energia": -10}, "feedback": "A base adorou, mas indecisos ficaram receosos."},
                {"texto": "Focar em propostas", "efeito": {"pop": 2, "caixa": 0, "energia": -15}, "feedback": "Respeitado pela imprensa, mas acharam técnico demais."},
                {"texto": "Promessa polêmica", "efeito": {"pop": 10, "caixa": -5000, "energia": -20}, "feedback": "Viralizou! Mas o caixa sofreu."}
            ]
        },
        {
            "titulo": "🤝 Comício no Interior",
            "desc": "Um município do interior pede sua visita. O custo de logística é significativo.",
            "icon": "🤝",
            "opcoes": [
                {"texto": "Ir de helicóptero", "efeito": {"pop": 3, "caixa": -10000, "energia": -5}, "feedback": "Rápido, mas criticaram o gasto."},
                {"texto": "Ir de carreta", "efeito": {"pop": 5, "caixa": -2000, "energia": -20}, "feedback": "O povo viu seu esforço na estrada."},
                {"texto": "Enviar vídeo", "efeito": {"pop": -5, "caixa": 0, "energia": 10}, "feedback": "Economizou, mas pareceram distante."}
            ]
        },
        {
            "titulo": "📱 Vazamento no WhatsApp",
            "desc": "Um áudio seu vazou fora de contexto nos grupos de família.",
            "icon": "📱",
            "opcoes": [
                {"texto": "Esclarecer publicamente", "efeito": {"pop": 0, "caixa": -1000, "energia": -10}, "feedback": "Conteve o dano, mas gerou ruído."},
                {"texto": "Ignorar", "efeito": {"pop": -5, "caixa": 0, "energia": 0}, "feedback": "O boato se espalhou sem resposta."},
                {"texto": "Processar", "efeito": {"pop": 2, "caixa": -5000, "energia": -15}, "feedback": "Mostrou firmeza, mas gastou recursos."}
            ]
        },
        {
            "titulo": "💰 Doação de Campanha",
            "desc": "Uma empresa quer fazer doação dentro da lei eleitoral.",
            "icon": "💰",
            "opcoes": [
                {"texto": "Aceitar", "efeito": {"pop": -2, "caixa": 20000, "energia": 0}, "feedback": "Caixa cheio, mas criticaram o vínculo."},
                {"texto": "Recusar", "efeito": {"pop": 3, "caixa": 0, "energia": 0}, "feedback": "Ganhou imagem de independência."},
                {"texto": "Pedir contrapartida", "efeito": {"pop": -10, "caixa": 30000, "energia": -10}, "feedback": "Caixa enorme, mas surgiram acusações."}
            ]
        },
        {
            "titulo": "🏥 Visita Hospitalar",
            "desc": "Humanização da campanha. Requer tempo e empatia.",
            "icon": "🏥",
            "opcoes": [
                {"texto": "Visita longa", "efeito": {"pop": 5, "caixa": -500, "energia": -25}, "feedback": "Imagem humanizada fortalecida."},
                {"texto": "Visita rápida", "efeito": {"pop": -3, "caixa": -500, "energia": -5}, "feedback": "Acusado de usar pacientes."},
                {"texto": "Enviar representante", "efeito": {"pop": 0, "caixa": -1000, "energia": 5}, "feedback": "Seguro, mas sem impacto."}
            ]
        },
        {
            "titulo": "📉 Crise Econômica",
            "desc": "O dólar subiu e a bolsa caiu. O eleitor está nervoso.",
            "icon": "📉",
            "opcoes": [
                {"texto": "Culpar governo atual", "efeito": {"pop": 5, "caixa": 0, "energia": -5}, "feedback": "A base concordou."},
                {"texto": "Propor austeridade", "efeito": {"pop": -5, "caixa": 0, "energia": -10}, "feedback": "Impopular, mas responsável."},
                {"texto": "Prometer subsídios", "efeito": {"pop": 8, "caixa": -15000, "energia": -10}, "feedback": "Popularidade subiu, caixa sangrou."}
            ]
        },
        {
            "titulo": "🎓 Proposta para Educação",
            "desc": "Sindicato de professores pede posicionamento sobre educação.",
            "icon": "🎓",
            "opcoes": [
                {"texto": "Aumentar investimento", "efeito": {"pop": 6, "caixa": -10000, "energia": -10}, "feedback": "Professores apoiaram."},
                {"texto": "Focar em gestão", "efeito": {"pop": 2, "caixa": -2000, "energia": -5}, "feedback": "Proposta técnica, reception morna."},
                {"texto": "Privatizar parte", "efeito": {"pop": -8, "caixa": 5000, "energia": -15}, "feedback": "Controvérsia enorme nas redes."}
            ]
        },
        {
            "titulo": "👮 Segurança Pública",
            "desc": "Índice de violência aumentou. Eleitores cobram posição.",
            "icon": "👮",
            "opcoes": [
                {"texto": "Mais policiamento", "efeito": {"pop": 7, "caixa": -8000, "energia": -10}, "feedback": "Proposta popular."},
                {"texto": "Focar em prevenção", "efeito": {"pop": 3, "caixa": -5000, "energia": -15}, "feedback": "Visão de longo prazo."},
                {"texto": "Armar cidadãos", "efeito": {"pop": -5, "caixa": 0, "energia": -20}, "feedback": "Polêmica dividindo opiniões."}
            ]
        },
        {
            "titulo": "🌱 Meio Ambiente",
            "desc": "Organizações internacionais cobram posição sobre Amazônia.",
            "icon": "🌱",
            "opcoes": [
                {"texto": "Proteção total", "efeito": {"pop": 4, "caixa": -3000, "energia": -10}, "feedback": "Apoio internacional."},
                {"texto": "Desenvolvimento sustentável", "efeito": {"pop": 2, "caixa": -2000, "energia": -15}, "feedback": "Equilíbrio difícil."},
                {"texto": "Priorizar economia", "efeito": {"pop": -6, "caixa": 5000, "energia": -5}, "feedback": "Críticas de ambientalistas."}
            ]
        },
        {
            "titulo": "🏛️ Aliança Política",
            "desc": "Partido influente propõe aliança para o segundo turno.",
            "icon": "🏛️",
            "opcoes": [
                {"texto": "Aceitar aliança", "efeito": {"pop": 5, "caixa": 10000, "energia": -10}, "feedback": "Base de apoio ampliou."},
                {"texto": "Manter independência", "efeito": {"pop": 0, "caixa": 0, "energia": 5}, "feedback": "Coerência mantida."},
                {"texto": "Negociar cargos", "efeito": {"pop": -3, "caixa": 15000, "energia": -15}, "feedback": "Acusado de troca de favores."}
            ]
        }
    ],
    "esquerda": [
        {
            "titulo": "👷 Reforma Trabalhista",
            "desc": "Centrais sindicais cobram posicionamento sobre direitos trabalhistas.",
            "icon": "👷",
            "opcoes": [
                {"texto": "Reverter reformas", "efeito": {"pop": 8, "caixa": -5000, "energia": -15}, "feedback": "Sindicatos mobilizados a seu favor."},
                {"texto": "Manter com ajustes", "efeito": {"pop": 0, "caixa": 0, "energia": -10}, "feedback": "Posição moderada."},
                {"texto": "Aprofundar reformas", "efeito": {"pop": -15, "caixa": 10000, "energia": -20}, "feedback": "Base traiu você."}
            ]
        },
        {
            "titulo": "🏠 Programa Habitacional",
            "desc": "Déficit habitacional é tema quente nas periferias.",
            "icon": "🏠",
            "opcoes": [
                {"texto": "1 milhão de casas", "efeito": {"pop": 10, "caixa": -20000, "energia": -20}, "feedback": "Proposta ambiciosa popular."},
                {"texto": "Parceria com iniciativa privada", "efeito": {"pop": 3, "caixa": -5000, "energia": -10}, "feedback": "Solução viável mas menos popular."},
                {"texto": "Focar em urbanização", "efeito": {"pop": 5, "caixa": -8000, "energia": -15}, "feedback": "Abordagem técnica apreciada."}
            ]
        }
    ],
    "centro": [
        {
            "titulo": "⚖️ Reforma Tributária",
            "desc": "Setor produtivo e sociedade cobram simplificação dos impostos.",
            "icon": "⚖️",
            "opcoes": [
                {"texto": "Unificar impostos", "efeito": {"pop": 6, "caixa": -5000, "energia": -15}, "feedback": "Ampla aprovação."},
                {"texto": "Reduzir gradualmente", "efeito": {"pop": 3, "caixa": -2000, "energia": -10}, "feedback": "Cautela elogiada."},
                {"texto": "Manter sistema atual", "efeito": {"pop": -5, "caixa": 0, "energia": -5}, "feedback": "Visto como omisso."}
            ]
        },
        {
            "titulo": "🤝 Diálogo Nacional",
            "desc": "País polarizado pede candidato conciliador.",
            "icon": "🤝",
            "opcoes": [
                {"texto": "Convocar todos os lados", "efeito": {"pop": 7, "caixa": -3000, "energia": -20}, "feedback": "Imagem de pacificador."},
                {"texto": "Focar no meio-termo", "efeito": {"pop": 4, "caixa": -1000, "energia": -10}, "feedback": "Equilíbrio mantido."},
                {"texto": "Tomar lado definido", "efeito": {"pop": -3, "caixa": 5000, "energia": -5}, "feedback": "Perdeu imagem de neutro."}
            ]
        }
    ],
    "direita": [
        {
            "titulo": "💼 Liberdade Econômica",
            "desc": "Empresários cobram menos burocracia e impostos.",
            "icon": "💼",
            "opcoes": [
                {"texto": "Reduzir ministérios", "efeito": {"pop": 8, "caixa": -3000, "energia": -15}, "feedback": "Mercado reagiu bem."},
                {"texto": "Privatizações", "efeito": {"pop": 5, "caixa": 10000, "energia": -20}, "feedback": "Controvérsia mas caixa cheio."},
                {"texto": "Manter estatais", "efeito": {"pop": -8, "caixa": 0, "energia": -10}, "feedback": "Base econômica frustrada."}
            ]
        },
        {
            "titulo": "🔫 Armamento Civil",
            "desc": "Debate sobre posse de armas divide o país.",
            "icon": "🔫",
            "opcoes": [
                {"texto": "Facilitar posse", "efeito": {"pop": 7, "caixa": 0, "energia": -15}, "feedback": "Base fiel apoiou."},
                {"texto": "Manter restrições", "efeito": {"pop": -10, "caixa": 5000, "energia": -10}, "feedback": "Base traiu você."},
                {"texto": "Focar em controle", "efeito": {"pop": 2, "caixa": 0, "energia": -20}, "feedback": "Posição técnica moderada."}
            ]
        }
    ]
}

# ============================================================================
# SISTEMA DE PARTIDOS/IDEOLOGIAS
# ============================================================================
PARTIDOS = {
    "esquerda": {
        "nome": "Frente Progressista",
        "cor": "#DC143C",
        "icone": "🔴",
        "bonus": {"pop": 1, "caixa": -500},
        "descricao": "Foco em direitos sociais e trabalhistas"
    },
    "centro": {
        "nome": "Aliança Democrática",
        "cor": "#FFD700",
        "icone": "🟡",
        "bonus": {"pop": 0, "caixa": 1000},
        "descricao": "Equilíbrio e diálogo entre extremos"
    },
    "direita": {
        "nome": "Movimento Liberal",
        "cor": "#0066CC",
        "icone": "🔵",
        "bonus": {"pop": -1, "caixa": 2000},
        "descricao": "Liberdade econômica e segurança"
    }
}

# ============================================================================
# FUNÇÕES DE LÓGICA DO JOGO
# ============================================================================

def init_game():
    """Inicializa todas as variáveis de estado do jogo"""
    st.session_state.dia = 1
    st.session_state.total_dias = 30
    st.session_state.popularidade = 25.0
    st.session_state.caixa = 150000.00
    st.session_state.energia = 100
    st.session_state.game_over = False
    st.session_state.vitoria = False
    st.session_state.historico = []
    st.session_state.evento_atual = None
    st.session_state.evolucao_popularidade = [25.0]
    st.session_state.evolucao_dias = [1]
    st.session_state.partido_escolhido = None
    st.session_state.eventos_usados = []
    st.session_state.pesquisas = []
    st.session_state.turno = 1
    st.session_state.high_score = load_high_score()

def load_high_score():
    """Carrega o high score do session state ou inicializa"""
    if 'high_score_data' not in st.session_state:
        st.session_state.high_score_data = {
            'score': 0,
            'dia': 0,
            'partido': 'Nenhum',
            'data': 'N/A'
        }
    return st.session_state.high_score_data

def save_high_score(popularidade, dia, partido):
    """Salva novo high score se for melhor"""
    if popularidade > st.session_state.high_score_data['score']:
        st.session_state.high_score_data = {
            'score': popularidade,
            'dia': dia,
            'partido': partido,
            'data': datetime.now().strftime('%d/%m/%Y %H:%M')
        }
        return True
    return False

def gerar_evento():
    """Seleciona um evento aleatório baseado na ideologia"""
    eventos_gerais = EVENTOS["geral"]
    eventos_ideologia = EVENTOS.get(st.session_state.partido_escolhido, [])
    
    # 70% chance de evento geral, 30% de evento específico da ideologia
    if eventos_ideologia and random.random() < 0.3:
        pool_eventos = eventos_ideologia
    else:
        pool_eventos = eventos_gerais
    
    # Filtrar eventos já usados recentemente
    eventos_disponiveis = [e for e in pool_eventos if e['titulo'] not in st.session_state.eventos_usados[-5:]]
    
    if not eventos_disponiveis:
        eventos_disponiveis = pool_eventos
    
    evento = random.choice(eventos_disponiveis)
    st.session_state.eventos_usados.append(evento['titulo'])
    
    return evento

def aplicar_consequencias(opcao):
    """Aplica os efeitos da escolha com bônus do partido"""
    bonus = PARTIDOS[st.session_state.partido_escolhido]['bonus']
    
    st.session_state.popularidade += opcao['efeito']['pop'] + bonus['pop']
    st.session_state.caixa += opcao['efeito']['caixa'] + bonus['caixa']
    st.session_state.energia += opcao['efeito']['energia']
    
    # Limites
    st.session_state.popularidade = max(0, min(100, st.session_state.popularidade))
    st.session_state.energia = max(0, min(100, st.session_state.energia))
    
    # Salvar evolução para gráfico
    st.session_state.evolucao_popularidade.append(st.session_state.popularidade)
    st.session_state.evolucao_dias.append(st.session_state.dia)
    
    # Salvar pesquisa
    st.session_state.pesquisas.append({
        'dia': st.session_state.dia,
        'pop': st.session_state.popularidade
    })
    
    # Histórico
    st.session_state.historico.append({
        'dia': st.session_state.dia,
        'feedback': opcao['feedback'],
        'pop': st.session_state.popularidade
    })

def verificar_condicoes():
    """Verifica condições de vitória/derrota"""
    # Vitória antecipada
    if st.session_state.popularidade >= 55:
        st.session_state.vitoria = True
        st.session_state.game_over = True
        return "VITÓRIA ESMAGADORA! Você atingiu 55% e venceu em 1º turno!"
    
    # Derrotas
    if st.session_state.popularidade <= 5:
        st.session_state.game_over = True
        return "DERROTA: Popularidade abaixo de 5%. Partido pediu sua renúncia."
    
    if st.session_state.caixa <= 0:
        st.session_state.game_over = True
        return "DERROTA: Campanha falida. TSE cassou sua candidatura."
    
    if st.session_state.energia <= 0:
        st.session_state.game_over = True
        return "DERROTA: Colapso de saúde. Candidato hospitalizado."
    
    # Fim dos 30 dias
    if st.session_state.dia > st.session_state.total_dias:
        st.session_state.game_over = True
        if st.session_state.popularidade >= 45:
            st.session_state.vitoria = True
            return "PARABÉNS! Você foi para o 2º turno com boa vantagem!"
        elif st.session_state.popularidade >= 35:
            st.session_state.vitoria = True
            return "CLASSIFICADO! Você vai para o 2º turno disputado."
        else:
            st.session_state.vitoria = False
            return "ELIMINADO: Não atingiu votos suficientes para o 2º turno."
    
    # Pesquisa especial no dia 15
    if st.session_state.dia == 15:
        st.session_state.turno = 2
        return "📊 PESQUISA DE MEIO DE CAMPANHA DIVULGADA!"
            
    return None

def criar_grafico_evolucao():
    """Cria gráfico Plotly da evolução da popularidade"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=st.session_state.evolucao_dias,
        y=st.session_state.evolucao_popularidade,
        mode='lines+markers',
        name='Popularidade',
        line=dict(color=PARTIDOS[st.session_state.partido_escolhido]['cor'], width=3),
        marker=dict(size=8)
    ))
    
    # Linhas de referência
    fig.add_hline(y=45, line_dash="dash", line_color="green", annotation_text="2º Turno")
    fig.add_hline(y=55, line_dash="dash", line_color="gold", annotation_text="Vitória 1º Turno")
    fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Zona de Perigo")
    
    fig.update_layout(
        title='📈 Evolução da Popularidade',
        xaxis_title='Dia de Campanha',
        yaxis_title='Popularidade (%)',
        yaxis_range=[0, 100],
        xaxis_range=[1, 30],
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig

# ============================================================================
# INTERFACE DO USUÁRIO
# ============================================================================

def mostrar_tela_inicial():
    """Tela de seleção de partido/ideologia"""
    st.title("🗳️ Candidato 2026")
    st.subheader("Simulador de Campanha Eleitoral")
    
    st.markdown("""
    ### 📋 Sobre o Jogo
    Você é um candidato presidencial em ano de eleição. Tome decisões estratégicas 
    por **30 dias de campanha** e tente chegar ao dia da eleição com máxima popularidade.
    
    **⚠️ Aviso:** Este é um jogo fictício para fins educacionais. 
    Nenhum político ou partido real foi usado.
    """)
    
    st.divider()
    
    st.header("🎯 Escolha Sua Ideologia")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: {PARTIDOS['esquerda']['cor']}20; padding: 20px; border-radius: 10px; border: 2px solid {PARTIDOS['esquerda']['cor']};">
        <h2 style="color: {PARTIDOS['esquerda']['cor']}">{PARTIDOS['esquerda']['icone']} Esquerda</h2>
        <p><strong>{PARTIDOS['esquerda']['nome']}</strong></p>
        <p>{PARTIDOS['esquerda']['descricao']}</p>
        <p>💰 Bônus: +R$ 500/dia</p>
        <p>📊 Popularidade: +1% por decisão</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔴 Jogar como Esquerda", key="btn_esq", use_container_width=True):
            st.session_state.partido_escolhido = "esquerda"
            init_game()
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div style="background-color: {PARTIDOS['centro']['cor']}20; padding: 20px; border-radius: 10px; border: 2px solid {PARTIDOS['centro']['cor']};">
        <h2 style="color: {PARTIDOS['centro']['cor']}">{PARTIDOS['centro']['icone']} Centro</h2>
        <p><strong>{PARTIDOS['centro']['nome']}</strong></p>
        <p>{PARTIDOS['centro']['descricao']}</p>
        <p>💰 Bônus: +R$ 1.000/dia</p>
        <p>📊 Popularidade: Neutro</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🟡 Jogar como Centro", key="btn_cen", use_container_width=True):
            st.session_state.partido_escolhido = "centro"
            init_game()
            st.rerun()
    
    with col3:
        st.markdown(f"""
        <div style="background-color: {PARTIDOS['direita']['cor']}20; padding: 20px; border-radius: 10px; border: 2px solid {PARTIDOS['direita']['cor']};">
        <h2 style="color: {PARTIDOS['direita']['cor']}">{PARTIDOS['direita']['icone']} Direita</h2>
        <p><strong>{PARTIDOS['direita']['nome']}</strong></p>
        <p>{PARTIDOS['direita']['descricao']}</p>
        <p>💰 Bônus: +R$ 2.000/dia</p>
        <p>📊 Popularidade: -1% por decisão</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔵 Jogar como Direita", key="btn_dir", use_container_width=True):
            st.session_state.partido_escolhido = "direita"
            init_game()
            st.rerun()
    
    st.divider()
    
    # High Score
    st.header("🏆 Recorde Atual")
    hs = st.session_state.high_score_data
    st.metric("Maior Popularidade", f"{hs['score']:.1f}%", 
              help=f"Partido: {hs['partido']} | Dia: {hs['dia']} | Data: {hs['data']}")

def mostrar_jogo():
    """Tela principal do jogo"""
    partido_info = PARTIDOS[st.session_state.partido_escolhido]
    
    # Header com informações do partido
    col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
    with col_h1:
        st.title(f"{partido_info['icone']} {partido_info['nome']}")
    with col_h2:
        st.metric("Dia", f"{st.session_state.dia}/{st.session_state.total_dias}")
    with col_h3:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.partido_escolhido = None
            st.rerun()
    
    # Stats em cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <h3>📊 Popularidade</h3>
        <h1 style="color: {partido_info['cor']}">{st.session_state.popularidade:.1f}%</h1>
        <progress value="{st.session_state.popularidade}" max="100" style="width:100%"></progress>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h3>💰 Caixa</h3>
        <h1 style="color: green">R$ {st.session_state.caixa:,.2f}</h1>
        <small>{'✅ Saudável' if st.session_state.caixa > 50000 else '⚠️ Atenção' if st.session_state.caixa > 10000 else '🚨 Crítico'}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <h3>⚡ Energia</h3>
        <h1 style="color: orange">{st.session_state.energia}%</h1>
        <progress value="{st.session_state.energia}" max="100" style="width:100%"></progress>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
        <h3>🎯 Meta</h3>
        <h1>45%</h1>
        <small>Para 2º Turno</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Gráfico de evolução
    if len(st.session_state.evolucao_popularidade) > 1:
        st.plotly_chart(criar_grafico_evolucao(), use_container_width=True)
    
    st.divider()
    
    # Área do evento
    if st.session_state.game_over:
        # Tela de fim de jogo
        if st.session_state.vitoria:
            st.balloons()
            st.markdown(f"""
            <div class="victory">
            <h1>🎉 VITÓRIA!</h1>
            <p>Sua campanha foi um sucesso! Popularidade final: <strong>{st.session_state.popularidade:.1f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Salvar high score
            if save_high_score(st.session_state.popularidade, st.session_state.dia, partido_info['nome']):
                st.success("🏆 Novo Recorde Pessoal!")
        else:
            st.markdown(f"""
            <div class="defeat">
            <h1>😞 DERROTA</h1>
            <p>Não foi dessa vez. Popularidade final: <strong>{st.session_state.popularidade:.1f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Histórico completo
        st.subheader("📜 Resumo da Campanha")
        for i, item in enumerate(st.session_state.historico[-10:], 1):
            st.text(f"{i}. Dia {item['dia']}: {item['feedback']} (Pop: {item['pop']:.1f}%)")
        
        if st.button("🎮 Jogar Novamente", use_container_width=True):
            st.session_state.partido_escolhido = None
            st.rerun()
            
    else:
        # Gerar evento se necessário
        if st.session_state.evento_atual is None:
            st.session_state.evento_atual = gerar_evento()
        
        evento = st.session_state.evento_atual
        
        # Caixa do evento
        st.markdown(f"""
        <div class="event-box">
        <h2>{evento['icon']} {evento['titulo']}</h2>
        <p>{evento['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### 🤔 Qual sua decisão?")
        
        # Botões de opção
        cols = st.columns(3)
        for i, opcao in enumerate(evento['opcoes']):
            with cols[i]:
                if st.button(f"Option {i+1}: {opcao['texto']}", key=f"opt_{i}", use_container_width=True):
                    aplicar_consequencias(opcao)
                    st.session_state.evento_atual = None
                    st.session_state.dia += 1
                    
                    msg = verificar_condicoes()
                    if msg:
                        st.session_state.msg_fim = msg
                    
                    st.rerun()
        
        # Feedback da última ação
        if len(st.session_state.historico) > 0:
            ultimo = st.session_state.historico[-1]
            st.info(f"💬 {ultimo['feedback']}")
        
        # Dicas
        with st.expander("💡 Dicas de Estratégia"):
            st.write("""
            - **Popularidade** acima de 45% garante 2º turno
            - **Caixa** negativo = cassação da candidatura
            - **Energia** zero = hospitalização
            - Cada partido tem bônus diferentes
            - Equilibre gastos com ganhos de popularidade
            """)

# ============================================================================
# MAIN
# ============================================================================

def main():
    # Sidebar com informações
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/ballot-box-with-ball.png", width=80)
        st.title("Painel de Controle")
        
        if 'partido_escolhido' in st.session_state and st.session_state.partido_escolhido:
            st.write(f"**Partido:** {PARTIDOS[st.session_state.partido_escolhido]['nome']}")
            st.write(f"**Turno:** {st.session_state.turno}º")
            st.divider()
            st.write("### 📊 Estatísticas Rápidas")
            st.write(f"📈 Popularidade: {st.session_state.popularidade:.1f}%")
            st.write(f"💰 Caixa: R$ {st.session_state.caixa:,.2f}")
            st.write(f"⚡ Energia: {st.session_state.energia}%")
            st.divider()
            
            # Pesquisas recentes
            if st.session_state.pesquisas:
                st.write("### 📰 Últimas Pesquisas")
                for p in st.session_state.pesquisas[-3:]:
                    st.write(f"Dia {p['dia']}: {p['pop']:.1f}%")
        
        st.divider()
        st.info("""
        **Como Jogar:**
        1. Escolha sua ideologia
        2. Tome decisões a cada dia
        3. Mantenha popularidade alta
        4. Não deixe caixa ou energia zerarem
        5. Chegue ao dia 30 com 45%+
        """)
    
    # Tela principal
    if 'partido_escolhido' not in st.session_state or st.session_state.partido_escolhido is None:
        mostrar_tela_inicial()
    else:
        mostrar_jogo()

if __name__ == "__main__":
    main()
