import streamlit as st
import random
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="🇧🇷 Candidato 2026 - Simulador Presidencial",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS PERSONALIZADO
# ============================================================================
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 10px 0;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 14px;
        opacity: 0.9;
        text-transform: uppercase;
    }
    .metric-card h1 {
        margin: 10px 0 0 0;
        font-size: 32px;
        font-weight: 700;
    }
    .event-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #667eea;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .victory-screen {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 20px 0;
    }
    .defeat-screen {
        background: linear-gradient(135deg, #cb2d3e 0%, #ef473a 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 20px 0;
    }
    .achievement-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 5px 0;
    }
    .achievement-card.locked {
        background: #e0e0e0;
        color: #999;
    }
    .combo-counter {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 10px 20px;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0;
    }
    .news-item {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SISTEMA DE CONQUISTAS
# ============================================================================
ACHIEVEMENTS = {
    "first_vote": {"name": "Primeiro Voto", "desc": "Complete seu primeiro dia", "icon": "🗳️"},
    "popularity_10": {"name": "Começo Promissor", "desc": "Alcance 10% de popularidade", "icon": "📈"},
    "popularity_30": {"name": "Em Ascensão", "desc": "Alcance 30% de popularidade", "icon": "🚀"},
    "popularity_50": {"name": "Favorito", "desc": "Alcance 50% de popularidade", "icon": "👑"},
    "popularity_70": {"name": "Lenda Viva", "desc": "Alcance 70% de popularidade", "icon": "🏆"},
    "rich_campaign": {"name": "Caixa Cheio", "desc": "Tenha R$ 500.000 em caixa", "icon": "💰"},
    "scandal_survivor": {"name": "Sobrevivente", "desc": "Sobreviva a 3 escândalos", "icon": "🛡️"},
    "first_turn_victory": {"name": "Vitória Esmagadora", "desc": "Vença no primeiro turno", "icon": "🎉"},
    "comeback_king": {"name": "Rei do Comeback", "desc": "Volte de menos de 10% para vitória", "icon": "🔄"},
    "marathon": {"name": "Maratonista", "desc": "Complete todos os 30 dias", "icon": "🏃"},
}

# ============================================================================
# PARTIDOS/IDEOLOGIAS
# ============================================================================
PARTIDOS = {
    "esquerda": {
        "nome": "Frente Progressista",
        "sigla": "FPT",
        "cor": "#DC143C",
        "icone": "🔴",
        "bonus": {"pop": 1, "caixa": -500, "energia": 2, "midia": 1},
        "descricao": "Foco em direitos sociais e trabalhistas",
        "dificuldade": "Médio"
    },
    "centro": {
        "nome": "Aliança Democrática",
        "sigla": "ALD",
        "cor": "#FFD700",
        "icone": "🟡",
        "bonus": {"pop": 0, "caixa": 1000, "energia": 1, "midia": 2},
        "descricao": "Equilíbrio e diálogo entre extremos",
        "dificuldade": "Fácil"
    },
    "direita": {
        "nome": "Movimento Liberal",
        "sigla": "MBL",
        "cor": "#0066CC",
        "icone": "🔵",
        "bonus": {"pop": -1, "caixa": 2000, "energia": 0, "midia": 0},
        "descricao": "Liberdade econômica e segurança",
        "dificuldade": "Difícil"
    }
}

# ============================================================================
# REGIÕES BRASILEIRAS
# ============================================================================
REGIOES = {
    "Norte": {"eleitores": 8.5, "cor": "#228B22"},
    "Nordeste": {"eleitores": 28.5, "cor": "#FFA500"},
    "Centro-Oeste": {"eleitores": 7.8, "cor": "#FFD700"},
    "Sudeste": {"eleitores": 62.5, "cor": "#667eea"},
    "Sul": {"eleitores": 15.2, "cor": "#DC143C"}
}

# ============================================================================
# BANCO DE DADOS DE EVENTOS (CENÁRIO BRASILEIRO)
# ============================================================================
EVENTOS = {
    "geral": [
        {
            "titulo": "📺 Debate Presidencial na TV",
            "desc": "O maior debate do ano está no ar. 50 milhões de brasileiros estão assistindo.",
            "icon": "📺",
            "tipo": "debate",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Atacar adversários com dados", "efeito": {"pop": 8, "caixa": 0, "energia": -15, "midia": 5}, "feedback": "Argumentos sólidos impressionaram os eleitores."},
                {"texto": "Focar em propostas emocionais", "efeito": {"pop": 10, "caixa": -2000, "energia": -20, "midia": 3}, "feedback": "Discurso emocionante viralizou nas redes."},
                {"texto": "Postura conciliadora", "efeito": {"pop": 5, "caixa": 0, "energia": -10, "midia": 8}, "feedback": "Imprensa elogiou sua maturidade."},
            ]
        },
        {
            "titulo": "🚨 Escândalo de Corrupção Vaza",
            "desc": "Um membro da sua coalizão foi pego em esquema de corrupção.",
            "icon": "🚨",
            "tipo": "crise",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Romper aliança imediatamente", "efeito": {"pop": 5, "caixa": -5000, "energia": -20, "midia": -5}, "feedback": "Ganhou imagem de íntegro, mas perdeu apoio."},
                {"texto": "Aguardar investigação", "efeito": {"pop": -8, "caixa": 0, "energia": -10, "midia": -10}, "feedback": "Eleitores interpretaram como omissão."},
                {"texto": "Defender aliado publicamente", "efeito": {"pop": -15, "caixa": 0, "energia": -15, "midia": -15}, "feedback": "Base manteve apoio, mas indecisos fugiram."},
            ]
        },
        {
            "titulo": "💸 Crise Econômica Internacional",
            "desc": "Dólar dispara, bolsa cai. Eleitores estão preocupados.",
            "icon": "💸",
            "tipo": "economia",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Prometer controle de preços", "efeito": {"pop": 8, "caixa": -10000, "energia": -15, "midia": 3}, "feedback": "Popular nas classes baixas."},
                {"texto": "Defender autonomia do Banco Central", "efeito": {"pop": 2, "caixa": 0, "energia": -10, "midia": 8}, "feedback": "Mercado reagiu bem."},
                {"texto": "Anunciar pacote de emergência", "efeito": {"pop": 10, "caixa": -25000, "energia": -20, "midia": 5}, "feedback": "Medidas urgentes acalmaram mercados."},
            ]
        },
        {
            "titulo": "🏥 Crise de Saúde Pública",
            "desc": "Hospitais lotados e fila de vacinação cresce.",
            "icon": "🏥",
            "tipo": "saude",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Visitar hospitais pessoalmente", "efeito": {"pop": 7, "caixa": -3000, "energia": -30, "midia": 5}, "feedback": "Imagem humanizada fortalecida."},
                {"texto": "Anunciar verba emergencial", "efeito": {"pop": 5, "caixa": -20000, "energia": -10, "midia": 6}, "feedback": "Ação concreta elogiada."},
                {"texto": "Convocar cientistas para coletiva", "efeito": {"pop": 4, "caixa": -2000, "energia": -15, "midia": 10}, "feedback": "Transparência técnica bem recebida."},
            ]
        },
        {
            "titulo": "🌳 Queimadas na Amazônia",
            "desc": "Imagens de satélite mostram aumento de desmatamento.",
            "icon": "🌳",
            "tipo": "ambiente",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Enviar tropas para fiscalização", "efeito": {"pop": 6, "caixa": -15000, "energia": -20, "midia": 8}, "feedback": "Ação firme agradou ambientalistas."},
                {"texto": "Negociar com governadores", "efeito": {"pop": 3, "caixa": -5000, "energia": -15, "midia": 5}, "feedback": "Solução política, mas lenta."},
                {"texto": "Propor fundo internacional", "efeito": {"pop": 4, "caixa": 10000, "energia": -15, "midia": 7}, "feedback": "Solução criativa atraiu investimentos."},
            ]
        },
        {
            "titulo": "👷 Reforma Trabalhista",
            "desc": "Centrais sindicais e empresários cobram posicionamento.",
            "icon": "👷",
            "tipo": "trabalho",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Ampliar direitos trabalhistas", "efeito": {"pop": 8, "caixa": -10000, "energia": -15, "midia": 5}, "feedback": "Sindicatos mobilizaram apoio."},
                {"texto": "Flexibilizar para gerar empregos", "efeito": {"pop": -5, "caixa": 8000, "energia": -10, "midia": 3}, "feedback": "Empresários apoiaram."},
                {"texto": "Criar mesa de diálogo tripartite", "efeito": {"pop": 4, "caixa": -3000, "energia": -20, "midia": 8}, "feedback": "Abordagem negociada elogiada."},
            ]
        },
        {
            "titulo": "🔫 Segurança Pública",
            "desc": "Índices de violência batem recorde.",
            "icon": "🔫",
            "tipo": "seguranca",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Mais investimento em policiamento", "efeito": {"pop": 7, "caixa": -20000, "energia": -15, "midia": 5}, "feedback": "Medida popular e concreta."},
                {"texto": "Focar em prevenção social", "efeito": {"pop": 4, "caixa": -15000, "energia": -20, "midia": 6}, "feedback": "Visão de longo prazo."},
                {"texto": "Intervenção federal em estados", "efeito": {"pop": 5, "caixa": -25000, "energia": -25, "midia": 8}, "feedback": "Medida extrema gerou debate."},
            ]
        },
        {
            "titulo": "🎓 Educação Básica",
            "desc": "Brasil ocupa posição ruim no PISA.",
            "icon": "🎓",
            "tipo": "educacao",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Aumentar salário de professores", "efeito": {"pop": 6, "caixa": -25000, "energia": -15, "midia": 7}, "feedback": "Categoria valorizada apoiou."},
                {"texto": "Investir em tecnologia nas escolas", "efeito": {"pop": 5, "caixa": -20000, "energia": -12, "midia": 8}, "feedback": "Modernização bem recebida."},
                {"texto": "Focar em ensino técnico", "efeito": {"pop": 4, "caixa": -15000, "energia": -10, "midia": 5}, "feedback": "Alinhado com mercado."},
            ]
        },
        {
            "titulo": "🏠 Habitação Popular",
            "desc": "Déficit habitacional cresce nas grandes cidades.",
            "icon": "🏠",
            "tipo": "habitacao",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Construir 1 milhão de casas", "efeito": {"pop": 10, "caixa": -50000, "energia": -25, "midia": 8}, "feedback": "Proposta ambiciosa empolgou."},
                {"texto": "Subsidiar aluguel social", "efeito": {"pop": 5, "caixa": -20000, "energia": -15, "midia": 6}, "feedback": "Solução rápida mas paliativa."},
                {"texto": "Regularizar favelas existentes", "efeito": {"pop": 6, "caixa": -15000, "energia": -20, "midia": 7}, "feedback": "Abordagem pragmática."},
            ]
        },
        {
            "titulo": "⚡ Crise Energética",
            "desc": "Reservatórios de hidrelétricas em nível crítico.",
            "icon": "⚡",
            "tipo": "energia",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Racionamento preventivo", "efeito": {"pop": -5, "caixa": 5000, "energia": -10, "midia": -5}, "feedback": "Impopular mas responsável."},
                {"texto": "Ativar termelétricas", "efeito": {"pop": 2, "caixa": -30000, "energia": -15, "midia": 3}, "feedback": "Solução cara evitou apagões."},
                {"texto": "Importar energia de vizinhos", "efeito": {"pop": 3, "caixa": -20000, "energia": -12, "midia": 5}, "feedback": "Solução rápida e eficaz."},
            ]
        },
        {
            "titulo": "📱 Fake News nas Redes",
            "desc": "Vídeo manipulado seu viraliza no WhatsApp.",
            "icon": "📱",
            "tipo": "midia",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Processar criadores do vídeo", "efeito": {"pop": 2, "caixa": -10000, "energia": -15, "midia": 5}, "feedback": "Ação jurídica mostrou seriedade."},
                {"texto": "Desmentir em rede nacional", "efeito": {"pop": 5, "caixa": -5000, "energia": -20, "midia": 8}, "feedback": "Resposta rápida limitou danos."},
                {"texto": "Pedir ajuda às plataformas", "efeito": {"pop": 3, "caixa": -3000, "energia": -10, "midia": 6}, "feedback": "Redes removeram conteúdo."},
            ]
        },
        {
            "titulo": "🤝 Aliança Partidária",
            "desc": "Partido com 50 deputados oferece apoio.",
            "icon": "🤝",
            "tipo": "politica",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Aceitar e negociar cargos", "efeito": {"pop": -3, "caixa": 15000, "energia": -10, "midia": -5}, "feedback": "Base parlamentar fortalecida."},
                {"texto": "Recusar mantendo coerência", "efeito": {"pop": 5, "caixa": 0, "energia": 5, "midia": 8}, "feedback": "Imagem de integridade reforçada."},
                {"texto": "Negociar apenas políticas públicas", "efeito": {"pop": 3, "caixa": 5000, "energia": -15, "midia": 6}, "feedback": "Meio-termo bem recebido."},
            ]
        },
        {
            "titulo": "📊 Pesquisa Eleitoral Divulgada",
            "desc": "Instituto renomado libera nova pesquisa.",
            "icon": "📊",
            "tipo": "pesquisa",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Comemorar e usar na propaganda", "efeito": {"pop": 3, "caixa": -5000, "energia": -5, "midia": 5}, "feedback": "Momentum positivo mantido."},
                {"texto": "Ficar cauteloso e trabalhar mais", "efeito": {"pop": 2, "caixa": -3000, "energia": -15, "midia": 3}, "feedback": "Humildade elogiada."},
                {"texto": "Focar em estados onde vai mal", "efeito": {"pop": 4, "caixa": -10000, "energia": -20, "midia": 4}, "feedback": "Estratégia inteligente."},
            ]
        },
        {
            "titulo": "🎬 Horário Eleitoral Gratuito",
            "desc": "Seu tempo no rádio e TV pode definir votos.",
            "icon": "🎬",
            "tipo": "midia",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Propostas detalhadas de governo", "efeito": {"pop": 4, "caixa": -8000, "energia": -15, "midia": 6}, "feedback": "Eleitores informados aprovaram."},
                {"texto": "Emoção e esperança no futuro", "efeito": {"pop": 7, "caixa": -8000, "energia": -12, "midia": 5}, "feedback": "Conexão emocional funcionou."},
                {"texto": "Depoimentos de apoiadores", "efeito": {"pop": 5, "caixa": -8000, "energia": -8, "midia": 4}, "feedback": "Testemunhos reais convenceram."},
            ]
        },
        {
            "titulo": "🌾 Crise no Agronegócio",
            "desc": "Produtores rurais protestam por preços baixos.",
            "icon": "🌾",
            "tipo": "agro",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Subsidiar insumos agrícolas", "efeito": {"pop": 6, "caixa": -30000, "energia": -15, "midia": 5}, "feedback": "Setor produtivo apoiou."},
                {"texto": "Negociar com China exportações", "efeito": {"pop": 4, "caixa": -10000, "energia": -20, "midia": 7}, "feedback": "Solução de mercado."},
                {"texto": "Focar em agricultura familiar", "efeito": {"pop": 3, "caixa": -15000, "energia": -12, "midia": 4}, "feedback": "Equilíbrio entre setores."},
            ]
        },
    ],
    "esquerda": [
        {
            "titulo": "👊 Mobilização Sindical",
            "desc": "Centrais sindicais convocam greve geral.",
            "icon": "👊",
            "tipo": "trabalho",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Apoiar greve publicamente", "efeito": {"pop": 10, "caixa": -5000, "energia": -20, "midia": -5}, "feedback": "Base trabalhista mobilizada."},
                {"texto": "Chamar para negociação", "efeito": {"pop": 3, "caixa": 0, "energia": -15, "midia": 5}, "feedback": "Posição moderada."},
                {"texto": "Manter neutralidade", "efeito": {"pop": -8, "caixa": 0, "energia": -5, "midia": 0}, "feedback": "Base sentiu-se traída."},
            ]
        },
        {
            "titulo": "🏛️ Nacionalização de Recursos",
            "desc": "Descoberta de grande reserva mineral.",
            "icon": "🏛️",
            "tipo": "economia",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Defender estatal exclusiva", "efeito": {"pop": 12, "caixa": -10000, "energia": -20, "midia": 5}, "feedback": "Soberania nacional elogiada."},
                {"texto": "Parceria público-privada", "efeito": {"pop": 5, "caixa": 15000, "energia": -15, "midia": 3}, "feedback": "Solução pragmática."},
                {"texto": "Concessão total à privada", "efeito": {"pop": -15, "caixa": 25000, "energia": -10, "midia": -10}, "feedback": "Base progressista revoltada."},
            ]
        },
    ],
    "centro": [
        {
            "titulo": "⚖️ Reforma do Sistema Político",
            "desc": "Proposta de mudança no sistema eleitoral.",
            "icon": "⚖️",
            "tipo": "politica",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Apoiar reforma completa", "efeito": {"pop": 6, "caixa": -5000, "energia": -20, "midia": 8}, "feedback": "Imagem de reformador."},
                {"texto": "Propor mudanças graduais", "efeito": {"pop": 4, "caixa": -2000, "energia": -15, "midia": 5}, "feedback": "Prudência elogiada."},
                {"texto": "Manter sistema atual", "efeito": {"pop": -3, "caixa": 0, "energia": -5, "midia": -3}, "feedback": "Visto como conservador."},
            ]
        },
    ],
    "direita": [
        {
            "titulo": "💼 Desestatização",
            "desc": "Carteira de investimentos cobra agilidade.",
            "icon": "💼",
            "tipo": "economia",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Acelerar privatizações", "efeito": {"pop": 8, "caixa": 30000, "energia": -20, "midia": 5}, "feedback": "Mercado reagiu bem."},
                {"texto": "Manter ritmo atual", "efeito": {"pop": 0, "caixa": 0, "energia": -10, "midia": 0}, "feedback": "Neutro."},
                {"texto": "Revisar contratos anteriores", "efeito": {"pop": -10, "caixa": -5000, "energia": -15, "midia": -8}, "feedback": "Base econômica frustrada."},
            ]
        },
        {
            "titulo": "🔒 Lei e Ordem",
            "desc": "Onda de crimes violentos gera comoção.",
            "icon": "🔒",
            "tipo": "seguranca",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Endurecer penas criminal", "efeito": {"pop": 10, "caixa": -5000, "energia": -15, "midia": 5}, "feedback": "Proposta popular."},
                {"texto": "Investir em inteligência policial", "efeito": {"pop": 5, "caixa": -15000, "energia": -20, "midia": 7}, "feedback": "Abordagem técnica."},
                {"texto": "Focar em reinserção social", "efeito": {"pop": -8, "caixa": -10000, "energia": -15, "midia": -5}, "feedback": "Base conservadora criticou."},
            ]
        },
    ]
}

# ============================================================================
# FUNÇÕES DE INICIALIZAÇÃO
# ============================================================================

def init_game(dificuldade="normal"):
    """Inicializa todas as variáveis do jogo"""
    st.session_state.dia = 1
    st.session_state.total_dias = 30
    st.session_state.popularidade = 25.0
    st.session_state.caixa = 150000.00
    st.session_state.energia = 100
    st.session_state.midia = 50
    st.session_state.game_over = False
    st.session_state.vitoria = False
    st.session_state.historico = []
    st.session_state.evento_atual = None
    st.session_state.evolucao_popularidade = [25.0]
    st.session_state.evolucao_dias = [1]
    st.session_state.eventos_usados = []
    st.session_state.pesquisas = []
    st.session_state.conquistas_unlocked = []
    st.session_state.combo = 0
    st.session_state.max_combo = 0
    st.session_state.dificuldade = dificuldade
    st.session_state.regioes_support = {reg: 25.0 for reg in REGIOES.keys()}
    st.session_state.escandalos_sofridos = 0
    st.session_state.new_achievements = []
    st.session_state.show_stats = False
    st.session_state.mensagem_feedback = ""
    
    # Ajustes por dificuldade
    if dificuldade == "facil":
        st.session_state.caixa = 200000.00
        st.session_state.popularidade = 30.0
    elif dificuldade == "dificil":
        st.session_state.caixa = 100000.00
        st.session_state.popularidade = 20.0

def load_high_score():
    """Carrega o high score"""
    if 'high_score_data' not in st.session_state:
        st.session_state.high_score_data = {
            'score': 0,
            'dia': 0,
            'partido': 'Nenhum',
            'data': 'N/A',
            'dificuldade': 'normal'
        }
    return st.session_state.high_score_data

def save_high_score(popularidade, dia, partido, dificuldade):
    """Salva novo high score"""
    current = st.session_state.high_score_data
    if popularidade > current['score']:
        st.session_state.high_score_data = {
            'score': popularidade,
            'dia': dia,
            'partido': partido,
            'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'dificuldade': dificuldade
        }
        return True
    return False

# ============================================================================
# LÓGICA DO JOGO
# ============================================================================

def check_achievements():
    """Verifica e desbloqueia conquistas"""
    new_achievements = []
    
    if st.session_state.dia >= 2 and "first_vote" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("first_vote")
        new_achievements.append("first_vote")
    
    pop = st.session_state.popularidade
    if pop >= 10 and "popularity_10" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("popularity_10")
        new_achievements.append("popularity_10")
    if pop >= 30 and "popularity_30" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("popularity_30")
        new_achievements.append("popularity_30")
    if pop >= 50 and "popularity_50" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("popularity_50")
        new_achievements.append("popularity_50")
    if pop >= 70 and "popularity_70" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("popularity_70")
        new_achievements.append("popularity_70")
    
    if st.session_state.caixa >= 500000 and "rich_campaign" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("rich_campaign")
        new_achievements.append("rich_campaign")
    
    if st.session_state.escandalos_sofridos >= 3 and "scandal_survivor" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("scandal_survivor")
        new_achievements.append("scandal_survivor")
    
    if st.session_state.combo >= 5 and st.session_state.combo > st.session_state.max_combo:
        st.session_state.max_combo = st.session_state.combo
    
    return new_achievements

def gerar_evento():
    """Seleciona um evento aleatório"""
    eventos_gerais = EVENTOS["geral"]
    eventos_ideologia = EVENTOS.get(st.session_state.partido_escolhido, [])
    
    if eventos_ideologia and random.random() < 0.3:
        pool_eventos = eventos_ideologia
    else:
        pool_eventos = eventos_gerais
    
    eventos_disponiveis = [e for e in pool_eventos if e['titulo'] not in st.session_state.eventos_usados[-8:]]
    
    if not eventos_disponiveis:
        eventos_disponiveis = pool_eventos
        st.session_state.eventos_usados = []
    
    evento = random.choice(eventos_disponiveis)
    st.session_state.eventos_usados.append(evento['titulo'])
    
    if random.random() < 0.15 and evento['tipo'] != 'crise':
        crises = [e for e in eventos_gerais if e['tipo'] == 'crise']
        if crises:
            evento = random.choice(crises)
            st.session_state.escandalos_sofridos += 1
    
    return evento

def aplicar_consequencias(opcao):
    """Aplica os efeitos da escolha"""
    bonus = PARTIDOS[st.session_state.partido_escolhido]['bonus']
    
    mult = 1.0
    if st.session_state.dificuldade == "facil":
        mult = 1.2
    elif st.session_state.dificuldade == "dificil":
        mult = 0.8
    
    st.session_state.popularidade += (opcao['efeito']['pop'] + bonus['pop']) * mult
    st.session_state.caixa += (opcao['efeito']['caixa'] + bonus['caixa']) * mult
    st.session_state.energia += (opcao['efeito']['energia'] + bonus['energia']) * mult
    st.session_state.midia += (opcao['efeito'].get('midia', 0) + bonus['midia']) * mult
    
    st.session_state.popularidade = max(0, min(100, st.session_state.popularidade))
    st.session_state.energia = max(0, min(100, st.session_state.energia))
    st.session_state.midia = max(0, min(100, st.session_state.midia))
    
    atualizar_regioes(opcao)
    
    if opcao['efeito']['pop'] > 0:
        st.session_state.combo += 1
    else:
        st.session_state.combo = 0
    
    st.session_state.evolucao_popularidade.append(st.session_state.popularidade)
    st.session_state.evolucao_dias.append(st.session_state.dia)
    
    st.session_state.pesquisas.append({
        'dia': st.session_state.dia,
        'pop': st.session_state.popularidade,
        'midia': st.session_state.midia
    })
    
    st.session_state.historico.append({
        'dia': st.session_state.dia,
        'feedback': opcao['feedback'],
        'pop': st.session_state.popularidade,
        'caixa': st.session_state.caixa,
        'energia': st.session_state.energia
    })
    
    st.session_state.mensagem_feedback = opcao['feedback']
    
    new_achievements = check_achievements()
    st.session_state.new_achievements = new_achievements

def atualizar_regioes(opcao):
    """Atualiza apoio por região"""
    for reg in REGIOES.keys():
        variacao = random.uniform(-2, 3)
        if opcao['efeito']['pop'] > 0:
            variacao += 1
        else:
            variacao -= 1
        
        st.session_state.regioes_support[reg] += variacao
        st.session_state.regioes_support[reg] = max(0, min(100, st.session_state.regioes_support[reg]))

def verificar_condicoes():
    """Verifica condições de vitória/derrota"""
    if st.session_state.popularidade >= 60:
        st.session_state.vitoria = True
        st.session_state.game_over = True
        return "VITÓRIA ESMAGADORA! Você atingiu 60% e venceu em 1º turno!"
    
    if st.session_state.popularidade <= 5:
        st.session_state.game_over = True
        return "DERROTA: Popularidade abaixo de 5%. Partido pediu sua renúncia."
    
    if st.session_state.caixa <= 0:
        st.session_state.game_over = True
        return "DERROTA: Campanha falida. TSE cassou sua candidatura."
    
    if st.session_state.energia <= 0:
        st.session_state.game_over = True
        return "DERROTA: Colapso de saúde. Candidato hospitalizado."
    
    if st.session_state.midia <= 10:
        st.session_state.game_over = True
        return "DERROTA: Imprensa hostil destruiu sua imagem."
    
    if st.session_state.dia > st.session_state.total_dias:
        st.session_state.game_over = True
        if st.session_state.popularidade >= 50:
            st.session_state.vitoria = True
            return "PARABÉNS! Você venceu no 1º turno!"
        elif st.session_state.popularidade >= 40:
            st.session_state.vitoria = True
            return "CLASSIFICADO! Você vai para o 2º turno!"
        else:
            st.session_state.vitoria = False
            return "ELIMINADO: Não atingiu votos suficientes."
    
    if st.session_state.dia == 15:
        return "📊 PESQUISA DE MEIO DE CAMPANHA DIVULGADA!"
            
    return None

# ============================================================================
# GRÁFICOS
# ============================================================================

def criar_grafico_evolucao():
    """Cria gráfico da evolução da popularidade"""
    fig = go.Figure()
    
    partido_cor = PARTIDOS[st.session_state.partido_escolhido]['cor']
    
    fig.add_trace(go.Scatter(
        x=st.session_state.evolucao_dias,
        y=st.session_state.evolucao_popularidade,
        mode='lines+markers',
        name='Popularidade',
        line=dict(color=partido_cor, width=4),
        marker=dict(size=10)
    ))
    
    fig.add_hline(y=50, line_dash="dash", line_color="green", annotation_text="Vitória 1º Turno")
    fig.add_hline(y=40, line_dash="dash", line_color="orange", annotation_text="2º Turno")
    fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Zona de Perigo")
    
    fig.update_layout(
        title='📈 Evolução da Popularidade',
        xaxis_title='Dia de Campanha',
        yaxis_title='Popularidade (%)',
        yaxis_range=[0, 100],
        height=350,
        template='plotly_white'
    )
    
    return fig

def criar_grafico_regioes():
    """Cria gráfico de apoio por região"""
    regioes = list(st.session_state.regioes_support.keys())
    valores = list(st.session_state.regioes_support.values())
    cores = [REGIOES[r]['cor'] for r in regioes]
    
    fig = go.Figure(data=[
        go.Bar(
            x=regioes,
            y=valores,
            marker_color=cores,
            text=[f'{v:.1f}%' for v in valores],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='🗺️ Apoio por Região',
        yaxis_range=[0, 100],
        height=350,
        template='plotly_white',
        showlegend=False
    )
    
    return fig

# ============================================================================
# TELAS DO JOGO
# ============================================================================

def mostrar_tela_inicial():
    """Tela de seleção de partido"""
    st.markdown("""
    <div style="text-align: center; padding: 40px;">
        <h1 style="font-size: 48px; margin: 0;">🇧🇷 CANDIDATO 2026</h1>
        <p style="font-size: 18px; color: #666;">Simulador Presidencial Brasileiro</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎮 Como Jogar
        
        1. **Escolha sua ideologia** - Cada uma tem bônus únicos
        2. **Tome decisões** - 30 dias de campanha
        3. **Gerencie recursos** - Popularidade, Caixa, Energia e Mídia
        4. **Conquiste regiões** - Diferentes áreas do Brasil
        5. **Desbloqueie conquistas** - 10 achievements para coletar
        
        ### ⚠️ Aviso
        Este é um jogo **fictício** para fins educacionais.
        Nenhum político ou partido real foi usado.
        """)
        
        st.markdown("### 🎯 Nível de Dificuldade")
        dificuldade = st.radio(
            "Escolha a dificuldade:",
            ["Fácil", "Normal", "Difícil"],
            label_visibility="collapsed"
        )
        
        diff_map = {"Fácil": "facil", "Normal": "normal", "Difícil": "dificil"}
        st.session_state.dificuldade_temp = diff_map[dificuldade]
    
    with col2:
        st.markdown("### 🏆 Recorde Atual")
        hs = load_high_score()
        st.metric("Maior Popularidade", f"{hs['score']:.1f}%")
        st.write(f"**Partido:** {hs['partido']}")
        st.write(f"**Dificuldade:** {hs['dificuldade']}")
        st.write(f"**Data:** {hs['data']}")
        
        total_ach = len(ACHIEVEMENTS)
        unlocked = len(st.session_state.get('conquistas_unlocked', []))
        st.write(f"### 🏅 Conquistas: {unlocked}/{total_ach}")
    
    st.divider()
    
    st.markdown("### 🎭 Escolha Sua Ideologia")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        partido = PARTIDOS['esquerda']
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {partido['cor']} 0%, #8B0000 100%); padding: 25px; border-radius: 15px; color: white;">
            <h2 style="margin: 0; font-size: 48px;">{partido['icone']}</h2>
            <h3 style="margin: 10px 0;">{partido['nome']}</h3>
            <p style="font-size: 12px;">{partido['sigla']}</p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p style="font-size: 14px;">{partido['descricao']}</p>
            <p>💰 Caixa: +R$ 500/dia</p>
            <p>📊 Popularidade: +1% por decisão</p>
            <p>⚡ Energia: +2/dia</p>
            <p>🎯 Dificuldade: {partido['dificuldade']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔴 Jogar como Esquerda", key="btn_esq", use_container_width=True, type="primary"):
            st.session_state.partido_escolhido = "esquerda"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()
    
    with col2:
        partido = PARTIDOS['centro']
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {partido['cor']} 0%, #FFA500 100%); padding: 25px; border-radius: 15px; color: white;">
            <h2 style="margin: 0; font-size: 48px;">{partido['icone']}</h2>
            <h3 style="margin: 10px 0;">{partido['nome']}</h3>
            <p style="font-size: 12px;">{partido['sigla']}</p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p style="font-size: 14px;">{partido['descricao']}</p>
            <p>💰 Caixa: +R$ 1.000/dia</p>
            <p>📊 Popularidade: Neutro</p>
            <p>⚡ Energia: +1/dia</p>
            <p>🎯 Dificuldade: {partido['dificuldade']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🟡 Jogar como Centro", key="btn_cen", use_container_width=True, type="primary"):
            st.session_state.partido_escolhido = "centro"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()
    
    with col3:
        partido = PARTIDOS['direita']
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {partido['cor']} 0%, #003366 100%); padding: 25px; border-radius: 15px; color: white;">
            <h2 style="margin: 0; font-size: 48px;">{partido['icone']}</h2>
            <h3 style="margin: 10px 0;">{partido['nome']}</h3>
            <p style="font-size: 12px;">{partido['sigla']}</p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p style="font-size: 14px;">{partido['descricao']}</p>
            <p>💰 Caixa: +R$ 2.000/dia</p>
            <p>📊 Popularidade: -1% por decisão</p>
            <p>⚡ Energia: Neutro</p>
            <p>🎯 Dificuldade: {partido['dificuldade']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔵 Jogar como Direita", key="btn_dir", use_container_width=True, type="primary"):
            st.session_state.partido_escolhido = "direita"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()

def mostrar_jogo():
    """Tela principal do jogo"""
    partido_info = PARTIDOS[st.session_state.partido_escolhido]
    
    # Header
    col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
    with col_h1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {partido_info['cor']} 0%, #333 100%); padding: 20px; border-radius: 15px; color: white;">
            <h2 style="margin: 0;">{partido_info['icone']} {partido_info['nome']} ({partido_info['sigla']})</h2>
            <p style="margin: 5px 0 0 0;">Dia {st.session_state.dia}/{st.session_state.total_dias} | {st.session_state.dificuldade.upper()}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_h2:
        if st.button("📊 Gráficos", use_container_width=True):
            st.session_state.show_stats = not st.session_state.show_stats
    with col_h3:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.partido_escolhido = None
            st.rerun()
    
    # Combo counter
    if st.session_state.combo >= 3:
        st.markdown(f"""
        <div style="text-align: center;">
            <div class="combo-counter">
                🔥 COMBO x{st.session_state.combo} - Bônus de Popularidade!
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats em cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Popularidade</h3>
            <h1>{st.session_state.popularidade:.1f}%</h1>
            <p>Meta: 40%+</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.popularidade / 100)
    
    with col2:
        cor_caixa = "#11998e" if st.session_state.caixa > 50000 else "#f093fb" if st.session_state.caixa > 10000 else "#cb2d3e"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {cor_caixa} 0%, #333 100%);">
            <h3>💰 Caixa</h3>
            <h1>R$ {st.session_state.caixa:,.0f}</h1>
            <p>{'Saudável' if st.session_state.caixa > 50000 else 'Atenção' if st.session_state.caixa > 10000 else 'Crítico'}</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(st.session_state.caixa / 200000, 1.0))
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3>⚡ Energia</h3>
            <h1>{st.session_state.energia}%</h1>
            <p>Descanse se < 30%</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.energia / 100)
    
    with col4:
        cor_midia = "#667eea" if st.session_state.midia > 50 else "#cb2d3e"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {cor_midia} 0%, #333 100%);">
            <h3>📰 Mídia</h3>
            <h1>{st.session_state.midia:.0f}</h1>
            <p>Relação com imprensa</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.midia / 100)
    
    st.divider()
    
    # Gráficos
    if st.session_state.show_stats:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.plotly_chart(criar_grafico_evolucao(), use_container_width=True)
        with col_g2:
            st.plotly_chart(criar_grafico_regioes(), use_container_width=True)
        st.divider()
    
    # Área do evento
    if st.session_state.game_over:
        if st.session_state.vitoria:
            st.balloons()
            st.markdown(f"""
            <div class="victory-screen">
                <h1 style="font-size: 48px; margin: 0;">🎉 VITÓRIA!</h1>
                <p style="font-size: 24px; margin: 20px 0;">Sua campanha foi um sucesso!</p>
                <p style="font-size: 18px;">Popularidade final: <strong>{st.session_state.popularidade:.1f}%</strong></p>
                <p style="font-size: 16px;">Dias completados: <strong>{st.session_state.dia}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            if save_high_score(st.session_state.popularidade, st.session_state.dia, partido_info['nome'], st.session_state.dificuldade):
                st.success("🏆 NOVO RECORDE PESSOAL!")
        else:
            st.markdown(f"""
            <div class="defeat-screen">
                <h1 style="font-size: 48px; margin: 0;">😞 DERROTA</h1>
                <p style="font-size: 24px; margin: 20px 0;">Não foi dessa vez...</p>
                <p style="font-size: 18px;">Popularidade final: <strong>{st.session_state.popularidade:.1f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Conquistas
        if st.session_state.conquistas_unlocked:
            st.markdown("### 🏅 Conquistas Desbloqueadas")
            cols = st.columns(3)
            for i, ach_id in enumerate(st.session_state.conquistas_unlocked):
                with cols[i % 3]:
                    ach = ACHIEVEMENTS[ach_id]
                    st.markdown(f"""
                    <div class="achievement-card">
                        <strong>{ach['icon']} {ach['name']}</strong><br>
                        <small>{ach['desc']}</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Histórico
        with st.expander("📜 Resumo da Campanha", expanded=False):
            for i, item in enumerate(st.session_state.historico, 1):
                st.text(f"{i}. Dia {item['dia']}: {item['feedback']}")
        
        if st.button("🎮 Jogar Novamente", use_container_width=True, type="primary"):
            st.session_state.partido_escolhido = None
            st.rerun()
            
    else:
        # Gerar evento
        if st.session_state.evento_atual is None:
            st.session_state.evento_atual = gerar_evento()
        
        evento = st.session_state.evento_atual
        
        # Card do evento
        st.markdown(f"""
        <div class="event-card">
            <div style="font-size: 48px; margin-bottom: 10px;">{evento['icon']}</div>
            <h2 style="margin: 0 0 10px 0; color: #333;">{evento['titulo']}</h2>
            <p style="font-size: 16px; color: #555; line-height: 1.6;">{evento['desc']}</p>
            <div style="margin-top: 15px;">
                <span style="background: #667eea; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">
                    Impacto: {evento['impacto'].upper()}
                </span>
                <span style="background: #764ba2; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px; margin-left: 10px;">
                    Tipo: {evento['tipo'].upper()}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### 🤔 Qual sua decisão?")
        
        # Botões de opção
        cols = st.columns(3)
        for i, opcao in enumerate(evento['opcoes']):
            with cols[i]:
                bonus = PARTIDOS[st.session_state.partido_escolhido]['bonus']
                pop_prev = opcao['efeito']['pop'] + bonus['pop']
                caixa_prev = opcao['efeito']['caixa'] + bonus['caixa']
                energia_prev = opcao['efeito']['energia'] + bonus['energia']
                
                pop_icon = "📈" if pop_prev > 0 else "📉" if pop_prev < 0 else "➡️"
                caixa_icon = "💰" if caixa_prev > 0 else "💸" if caixa_prev < 0 else "➡️"
                energia_icon = "⚡" if energia_prev > 0 else "🔋" if energia_prev < 0 else "➡️"
                
                button_text = f"{opcao['texto']}\n\n{pop_icon} {pop_prev:+.0f}% | {caixa_icon} R$ {caixa_prev:+,.0f} | {energia_icon} {energia_prev:+.0f}"
                
                if st.button(button_text, key=f"opt_{i}", use_container_width=True):
                    aplicar_consequencias(opcao)
                    st.session_state.evento_atual = None
                    st.session_state.dia += 1
                    
                    # Recuperação diária
                    st.session_state.energia = min(100, st.session_state.energia + 5)
                    st.session_state.caixa += PARTIDOS[st.session_state.partido_escolhido]['bonus']['caixa']
                    
                    msg = verificar_condicoes()
                    if msg:
                        st.session_state.msg_fim = msg
                    
                    st.rerun()
        
        # Feedback
        if st.session_state.mensagem_feedback:
            st.info(f"💬 {st.session_state.mensagem_feedback}")
        
        # Conquistas novas
        if st.session_state.new_achievements:
            for ach_id in st.session_state.new_achievements:
                ach = ACHIEVEMENTS[ach_id]
                st.success(f"🏆 CONQUISTA: {ach['icon']} {ach['name']}!")
            st.session_state.new_achievements = []
        
        # Dicas
        with st.expander("💡 Dicas de Estratégia"):
            st.write("""
            - **Popularidade** acima de 50% = vitória no 1º turno
            - **Popularidade** acima de 40% = 2º turno
            - **Caixa** negativo = cassação pelo TSE
            - **Energia** zero = hospitalização
            - **Mídia** abaixo de 10 = imprensa hostil
            - Combos de decisões positivas aumentam popularidade
            - Cada partido tem bônus diferentes
            """)

# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar():
    """Renderiza a sidebar"""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/ballot-box-with-ball.png", width=80)
        st.title("🎛️ Painel")
        
        if 'partido_escolhido' in st.session_state and st.session_state.partido_escolhido:
            st.write(f"**Partido:** {PARTIDOS[st.session_state.partido_escolhido]['nome']}")
            st.write(f"**Dificuldade:** {st.session_state.dificuldade.upper()}")
            st.divider()
            
            st.write("### 📊 Status")
            st.write(f"📈 Popularidade: {st.session_state.popularidade:.1f}%")
            st.write(f"💰 Caixa: R$ {st.session_state.caixa:,.0f}")
            st.write(f"⚡ Energia: {st.session_state.energia}%")
            st.write(f"📰 Mídia: {st.session_state.midia:.0f}")
            st.divider()
            
            if st.session_state.combo >= 2:
                st.write(f"🔥 **Combo:** x{st.session_state.combo}")
            
            if st.session_state.pesquisas:
                st.write("### 📰 Últimas Pesquisas")
                for p in st.session_state.pesquisas[-3:]:
                    st.write(f"Dia {p['dia']}: {p['pop']:.1f}%")
            
            st.divider()
            
            st.write("### 🏅 Conquistas")
            total = len(ACHIEVEMENTS)
            unlocked = len(st.session_state.conquistas_unlocked)
            st.write(f"{unlocked}/{total} desbloqueadas")
            st.progress(unlocked / total)
        
        st.divider()
        st.info("""
        **📖 Como Jogar:**
        1. Escolha ideologia
        2. Decida a cada dia
        3. Mantenha stats altos
        4. Chegue ao dia 30
        5. Vença com 40%+
        """)

# ============================================================================
# MAIN
# ============================================================================

def main():
    if 'show_stats' not in st.session_state:
        st.session_state.show_stats = False
    if 'mensagem_feedback' not in st.session_state:
        st.session_state.mensagem_feedback = ""
    if 'new_achievements' not in st.session_state:
        st.session_state.new_achievements = []
    
    render_sidebar()
    
    if 'partido_escolhido' not in st.session_state or st.session_state.partido_escolhido is None:
        mostrar_tela_inicial()
    else:
        mostrar_jogo()

if __name__ == "__main__":
    main()
