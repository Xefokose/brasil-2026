import streamlit as st
import random
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="🇧🇷 Candidato 2026 - HARDCORE",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS
# ============================================================================
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 10px 0;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 12px;
        opacity: 0.7;
        text-transform: uppercase;
    }
    .metric-card h1 {
        margin: 10px 0 0 0;
        font-size: 28px;
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
    .event-card.crisis {
        border-left-color: #ff4757;
        background: #fff5f5;
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
    .advisor-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 5px 0;
        text-align: center;
    }
    .advisor-card.selected {
        border: 2px solid #00ff88;
        background: #f0fff4;
    }
    .scandal-warning {
        background: linear-gradient(135deg, #ff4757 0%, #ff6b81 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONQUISTAS
# ============================================================================
ACHIEVEMENTS = {
    "first_day": {"name": "Primeiro Dia", "desc": "Complete o dia 1", "icon": "🗳️"},
    "pop_30": {"name": "Emergindo", "desc": "Alcance 30% de popularidade", "icon": "📈"},
    "pop_50": {"name": "Favorito", "desc": "Alcance 50% de popularidade", "icon": "👑"},
    "pop_70": {"name": "Lenda", "desc": "Alcance 70% de popularidade", "icon": "🏆"},
    "rich": {"name": "Caixa Cheio", "desc": "Tenha R$ 500.000 em caixa", "icon": "💰"},
    "survivor": {"name": "Sobrevivente", "desc": "Sobreviva a 3 escândalos", "icon": "🛡️"},
    "coalition": {"name": "Negociador", "desc": "Mantenha coalizão acima de 70%", "icon": "🤝"},
    "victory_1st": {"name": "Vitória 1º Turno", "desc": "Vença no primeiro turno", "icon": "🎉"},
    "hardcore": {"name": "HARDCORE", "desc": "Complete no modo HARDCORE", "icon": "💀"},
    "marathon": {"name": "Maratonista", "desc": "Complete todos os dias", "icon": "🏃"},
}

# ============================================================================
# ASSESSORES
# ============================================================================
ASSESSORES = {
    "estrategista": {
        "nome": "Carlos Mendes",
        "cargo": "Estrategista Chefe",
        "icone": "🎯",
        "confiabilidade": 0.85,
        "especialidade": "popularidade",
        "descricao": "Focado em pesquisas e estratégia"
    },
    "financeiro": {
        "nome": "Ana Rodrigues",
        "cargo": "Diretora Financeira",
        "icone": "💰",
        "confiabilidade": 0.90,
        "especialidade": "caixa",
        "descricao": "Especialista em orçamento"
    },
    "comunicacao": {
        "nome": "Pedro Santos",
        "cargo": "Diretor de Comunicação",
        "icone": "📰",
        "confiabilidade": 0.75,
        "especialidade": "midia",
        "descricao": "Relação com imprensa"
    },
    "politico": {
        "nome": "Helena Costa",
        "cargo": "Articuladora Política",
        "icone": "🤝",
        "confiabilidade": 0.80,
        "especialidade": "coalizao",
        "descricao": "Negocia com partidos"
    },
    "juridico": {
        "nome": "Roberto Lima",
        "cargo": "Advogado Eleitoral",
        "icone": "⚖️",
        "confiabilidade": 0.95,
        "especialidade": "risco",
        "descricao": "Previne problemas jurídicos"
    }
}

# ============================================================================
# PARTIDOS DA COALIZÃO
# ============================================================================
PARTIDOS_COALIZAO = {
    "base": {"nome": "Partido da Base", "sigla": "PDB", "cor": "#DC143C", "apoio_inicial": 80},
    "centrao": {"nome": "Centrão Unido", "sigla": "CPU", "cor": "#FFD700", "apoio_inicial": 60},
    "progressista": {"nome": "Frente Progressista", "sigla": "FPP", "cor": "#228B22", "apoio_inicial": 70},
    "liberal": {"nome": "Aliança Liberal", "sigla": "ALB", "cor": "#0066CC", "apoio_inicial": 55}
}

# ============================================================================
# ESTADOS DECISIVOS
# ============================================================================
ESTADOS_DECISIVOS = {
    "SP": {"eleitores": 22.5, "cor": "#667eea"},
    "MG": {"eleitores": 10.8, "cor": "#228B22"},
    "RJ": {"eleitores": 8.9, "cor": "#FFD700"},
    "BA": {"eleitores": 8.2, "cor": "#FFA500"},
    "RS": {"eleitores": 5.8, "cor": "#DC143C"},
    "PR": {"eleitores": 5.7, "cor": "#228B22"},
    "PE": {"eleitores": 4.8, "cor": "#FFA500"},
    "CE": {"eleitores": 4.6, "cor": "#FFA500"},
}

# ============================================================================
# EVENTOS
# ============================================================================
EVENTOS = {
    "geral": [
        {
            "id": "debate_tv",
            "titulo": "📺 Debate Presidencial na TV",
            "desc": "O maior debate do ano está no ar. 60 milhões de brasileiros estão assistindo. Sua performance pode definir a eleição.",
            "icon": "📺",
            "tipo": "debate",
            "impacto": "critico",
            "duracao": 2,
            "opcoes": [
                {"texto": "Atacar adversários com dados", "descricao_oculta": "Alto risco, alta recompensa", "efeito_base": {"pop": 10, "caixa": 0, "energia": -20, "midia": 8, "risco": 15}},
                {"texto": "Focar em propostas emocionais", "descricao_oculta": "Bom para popularidade", "efeito_base": {"pop": 12, "caixa": -3000, "energia": -25, "midia": 5, "risco": 8}},
                {"texto": "Postura conciliadora", "descricao_oculta": "Seguro mas pouco impactante", "efeito_base": {"pop": 4, "caixa": 0, "energia": -15, "midia": 12, "risco": 3}},
            ]
        },
        {
            "id": "escandalo_corrupcao",
            "titulo": "🚨 ESCÂNDALO: Aliado em Esquema de Corrupção",
            "desc": "Um importante aliado da sua coalizão foi pego em esquema de desvio de verbas. A imprensa pede posicionamento imediato.",
            "icon": "🚨",
            "tipo": "crise",
            "impacto": "critico",
            "duracao": 3,
            "opcoes": [
                {"texto": "Romper aliança imediatamente", "descricao_oculta": "Ganha imagem de íntegro mas perde apoio", "efeito_base": {"pop": 8, "caixa": -8000, "energia": -25, "midia": -5, "risco": 20, "coalizao": -15}},
                {"texto": "Aguardar investigação", "descricao_oculta": "Seguro juridicamente, mas parece omissão", "efeito_base": {"pop": -12, "caixa": 0, "energia": -15, "midia": -15, "risco": 5, "coalizao": 5}},
                {"texto": "Defender aliado publicamente", "descricao_oculta": "Mantém coalizão mas associa ao escândalo", "efeito_base": {"pop": -20, "caixa": 0, "energia": -20, "midia": -25, "risco": 35, "coalizao": 10}},
            ]
        },
        {
            "id": "crise_economica",
            "titulo": "💸 CRISE ECONÔMICA INTERNACIONAL",
            "desc": "Dólar disparou 15%, bolsa caiu 8%. Eleitores estão preocupados com emprego e inflação.",
            "icon": "💸",
            "tipo": "economia",
            "impacto": "critico",
            "duracao": 2,
            "opcoes": [
                {"texto": "Prometer controle de preços", "descricao_oculta": "Popular mas economistas criticam", "efeito_base": {"pop": 12, "caixa": -15000, "energia": -20, "midia": 5, "risco": 18}},
                {"texto": "Defender autonomia do Banco Central", "descricao_oculta": "Mercado aprova, pouco popular", "efeito_base": {"pop": -5, "caixa": 8000, "energia": -15, "midia": 12, "risco": 8}},
                {"texto": "Anunciar pacote emergencial", "descricao_oculta": "Alto impacto, drena recursos", "efeito_base": {"pop": 15, "caixa": -35000, "energia": -25, "midia": 10, "risco": 12}},
            ]
        },
        {
            "id": "crise_saude",
            "titulo": "🏥 CRISE DE SAÚDE: HOSPITAIS LOTADOS",
            "desc": "Novo surto sobrecarregou o sistema de saúde. Imagens de pacientes em corredores viralizaram.",
            "icon": "🏥",
            "tipo": "saude",
            "impacto": "alto",
            "duracao": 2,
            "opcoes": [
                {"texto": "Visitar hospitais pessoalmente", "descricao_oculta": "Humaniza imagem, consome energia", "efeito_base": {"pop": 10, "caixa": -5000, "energia": -35, "midia": 8, "risco": 15}},
                {"texto": "Anunciar verba emergencial", "descricao_oculta": "Ação concreta, caro", "efeito_base": {"pop": 8, "caixa": -25000, "energia": -15, "midia": 10, "risco": 5}},
                {"texto": "Convocar coletiva com cientistas", "descricao_oculta": "Mostra competência, pode parecer frio", "efeito_base": {"pop": 5, "caixa": -3000, "energia": -20, "midia": 15, "risco": 3}},
            ]
        },
        {
            "id": "amazonia_queimadas",
            "titulo": "🌳 QUEIMADAS NA AMAZÔNIA",
            "desc": "Imagens de satélite mostram aumento de 45% nas queimadas. Líderes europeus ameaçam bloquear acordo.",
            "icon": "🌳",
            "tipo": "ambiente",
            "impacto": "alto",
            "duracao": 1,
            "opcoes": [
                {"texto": "Enviar tropas para fiscalização", "descricao_oculta": "Ação firme, irrita ruralistas", "efeito_base": {"pop": 8, "caixa": -20000, "energia": -25, "midia": 12, "risco": 15, "coalizao": -8}},
                {"texto": "Negociar com governadores", "descricao_oculta": "Solução política lenta", "efeito_base": {"pop": 3, "caixa": -8000, "energia": -20, "midia": 5, "risco": 8, "coalizao": 5}},
                {"texto": "Propor fundo internacional", "descricao_oculta": "Solução criativa, traz recursos", "efeito_base": {"pop": 6, "caixa": 15000, "energia": -20, "midia": 15, "risco": 10}},
            ]
        },
        {
            "id": "alianca_partidaria",
            "titulo": "🤝 PROPOSTA DE ALIANÇA",
            "desc": "Partido com 65 deputados oferece apoio. Exigem 5 ministérios e R$ 200 milhões em emendas.",
            "icon": "🤝",
            "tipo": "politica",
            "impacto": "alto",
            "duracao": 1,
            "opcoes": [
                {"texto": "Aceitar todas as exigências", "descricao_oculta": "Apoio imediato, esvazia caixa", "efeito_base": {"pop": -5, "caixa": 25000, "energia": -15, "midia": -8, "risco": 20, "coalizao": 15}},
                {"texto": "Negociar: 3 ministérios", "descricao_oculta": "Meio-termo arriscado", "efeito_base": {"pop": 2, "caixa": 12000, "energia": -20, "midia": 3, "risco": 15, "coalizao": 8}},
                {"texto": "Recusar mantendo coerência", "descricao_oculta": "Imagem limpa, perde apoio", "efeito_base": {"pop": 8, "caixa": 0, "energia": 5, "midia": 12, "risco": 5, "coalizao": -10}},
            ]
        },
        {
            "id": "horario_eleitoral",
            "titulo": "🎬 HORÁRIO ELEITORAL GRATUITO",
            "desc": "Você tem 5 minutos no rádio e TV para alcançar 80 milhões de eleitores.",
            "icon": "🎬",
            "tipo": "midia",
            "impacto": "alto",
            "duracao": 1,
            "opcoes": [
                {"texto": "Propostas detalhadas com dados", "descricao_oculta": "Atrai informados, técnico demais", "efeito_base": {"pop": 6, "caixa": -12000, "energia": -20, "midia": 10, "risco": 5}},
                {"texto": "Emoção e esperança", "descricao_oculta": "Conexão emocional forte", "efeito_base": {"pop": 10, "caixa": -12000, "energia": -18, "midia": 6, "risco": 8}},
                {"texto": "Ataques diretos aos adversários", "descricao_oculta": "Mobiliza base, afasta indecisos", "efeito_base": {"pop": 8, "caixa": -12000, "energia": -15, "midia": -5, "risco": 15}},
            ]
        },
        {
            "id": "seguranca_publica",
            "titulo": "🔫 ONDA DE VIOLÊNCIA",
            "desc": "Série de assaltos violentos chocou o país. Famílias de vítimas estão protestando.",
            "icon": "🔫",
            "tipo": "seguranca",
            "impacto": "alto",
            "duracao": 2,
            "opcoes": [
                {"texto": "Investimento em policiamento", "descricao_oculta": "Popular mas caro", "efeito_base": {"pop": 10, "caixa": -30000, "energia": -20, "midia": 8, "risco": 8}},
                {"texto": "Intervenção federal", "descricao_oculta": "Medida extrema, questionada", "efeito_base": {"pop": 8, "caixa": -35000, "energia": -30, "midia": 12, "risco": 22}},
                {"texto": "Prevenção social", "descricao_oculta": "Longo prazo, menos popular", "efeito_base": {"pop": 4, "caixa": -20000, "energia": -25, "midia": 10, "risco": 5}},
            ]
        },
        {
            "id": "fake_news",
            "titulo": "📱 FAKE NEWS VIRALIZA",
            "desc": "Vídeo manipulado com deepfake seu circula no WhatsApp. 5 milhões já viram.",
            "icon": "📱",
            "tipo": "midia",
            "impacto": "alto",
            "duracao": 2,
            "opcoes": [
                {"texto": "Processar criadores", "descricao_oculta": "Ação jurídica, processo lento", "efeito_base": {"pop": 3, "caixa": -15000, "energia": -20, "midia": 8, "risco": 10}},
                {"texto": "Desmentir em rede nacional", "descricao_oculta": "Resposta rápida, caro", "efeito_base": {"pop": 6, "caixa": -10000, "energia": -25, "midia": 12, "risco": 5}},
                {"texto": "Ignorar assunto", "descricao_oculta": "Pode funcionar ou falhar", "efeito_base": {"pop": -12, "caixa": 0, "energia": -8, "midia": -15, "risco": 25}},
            ]
        },
    ],
    "esquerda": [
        {
            "id": "nacionalizacao",
            "titulo": "🏛️ RESERVA ESTRATÉGICA DESCOBERTA",
            "desc": "Geólogos descobriram grande reserva de minerais raros. Empresas estrangeiras fazem ofertas.",
            "icon": "🏛️",
            "tipo": "economia",
            "impacto": "critico",
            "duracao": 2,
            "opcoes": [
                {"texto": "Monopólio estatal total", "descricao_oculta": "Base apoia, mercado reage mal", "efeito_base": {"pop": 15, "caixa": -15000, "energia": -25, "midia": 8, "risco": 18}},
                {"texto": "Parceria 51% estatal", "descricao_oculta": "Meio-termo", "efeito_base": {"pop": 6, "caixa": 20000, "energia": -20, "midia": 5, "risco": 12}},
                {"texto": "Leilão total privado", "descricao_oculta": "Mercado celebra, base trai", "efeito_base": {"pop": -20, "caixa": 40000, "energia": -15, "midia": -15, "risco": 30}},
            ]
        }
    ],
    "centro": [
        {
            "id": "reforma_politica",
            "titulo": "⚖️ REFORMA ELEITORAL EM PAUTA",
            "desc": "Congresso vota mudança no sistema eleitoral. Sua posição define o futuro.",
            "icon": "⚖️",
            "tipo": "politica",
            "impacto": "alto",
            "duracao": 2,
            "opcoes": [
                {"texto": "Reforma completa imediata", "descricao_oculta": "Imagem de reformador", "efeito_base": {"pop": 8, "caixa": -8000, "energia": -25, "midia": 12, "risco": 20}},
                {"texto": "Reforma gradual em 4 anos", "descricao_oculta": "Prudência", "efeito_base": {"pop": 4, "caixa": -3000, "energia": -18, "midia": 6, "risco": 10}},
                {"texto": "Manter sistema atual", "descricao_oculta": "Seguro, sem mudança", "efeito_base": {"pop": -5, "caixa": 5000, "energia": -10, "midia": -8, "risco": 8}},
            ]
        }
    ],
    "direita": [
        {
            "id": "privatizacoes",
            "titulo": "💼 CARTEIRA DE PRIVATIZAÇÕES",
            "desc": "Equipe preparou lista de 15 estatais. Estimativa: R$ 200 bilhões.",
            "icon": "💼",
            "tipo": "economia",
            "impacto": "critico",
            "duracao": 2,
            "opcoes": [
                {"texto": "Acelerar todas imediatamente", "descricao_oculta": "Mercado elege, sindicatos opõem", "efeito_base": {"pop": 10, "caixa": 50000, "energia": -30, "midia": 8, "risco": 25}},
                {"texto": "Privatizar apenas deficitárias", "descricao_oculta": "Seletivo", "efeito_base": {"pop": 5, "caixa": 20000, "energia": -20, "midia": 5, "risco": 15}},
                {"texto": "Congelar até após eleição", "descricao_oculta": "Adia polêmica", "efeito_base": {"pop": -8, "caixa": 0, "energia": -10, "midia": -10, "risco": 18}},
            ]
        }
    ]
}

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

def init_game(dificuldade="normal"):
    st.session_state.dia = 1
    st.session_state.total_dias = 45
    st.session_state.popularidade = 22.0
    st.session_state.caixa = 120000.00
    st.session_state.energia = 80
    st.session_state.midia = 45
    st.session_state.risco_escandalo = 10
    st.session_state.game_over = False
    st.session_state.vitoria = False
    st.session_state.historico = []
    st.session_state.evento_atual = None
    st.session_state.evolucao_popularidade = [22.0]
    st.session_state.evolucao_dias = [1]
    st.session_state.partido_escolhido = None
    st.session_state.eventos_usados = []
    st.session_state.pesquisas = []
    st.session_state.conquistas_unlocked = []
    st.session_state.combo = 0
    st.session_state.dificuldade = dificuldade
    st.session_state.estados_support = {estado: 20.0 + random.uniform(-5, 5) for estado in ESTADOS_DECISIVOS.keys()}
    st.session_state.coalizao_apoio = {partido: dados["apoio_inicial"] for partido, dados in PARTIDOS_COALIZAO.items()}
    st.session_state.assessor_selecionado = "estrategista"
    st.session_state.new_achievements = []
    st.session_state.show_stats = False
    st.session_state.mensagem_feedback = ""
    st.session_state.total_escandalos = 0
    st.session_state.msg_fim = ""
    
    if dificuldade == "facil":
        st.session_state.caixa = 180000.00
        st.session_state.popularidade = 28.0
        st.session_state.energia = 90
    elif dificuldade == "dificil":
        st.session_state.caixa = 80000.00
        st.session_state.popularidade = 18.0
        st.session_state.energia = 70
        st.session_state.risco_escandalo = 20
    elif dificuldade == "hardcore":
        st.session_state.caixa = 60000.00
        st.session_state.popularidade = 15.0
        st.session_state.energia = 60
        st.session_state.risco_escandalo = 30
        st.session_state.total_dias = 40

def load_high_score():
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

def get_assessor_advice(evento, opcao_index):
    assessor = ASSESSORES[st.session_state.assessor_selecionado]
    opcao = evento['opcoes'][opcao_index]
    
    if assessor['especialidade'] == 'popularidade':
        if opcao['efeito_base']['pop'] > 5:
            return f"✅ {assessor['nome']}: 'Esta opção pode aumentar sua popularidade.'"
        elif opcao['efeito_base']['pop'] < -5:
            return f"⚠️ {assessor['nome']}: 'Isso pode prejudicar suas pesquisas.'"
        else:
            return f"➡️ {assessor['nome']}: 'Impacto neutro na popularidade.'"
    elif assessor['especialidade'] == 'caixa':
        if opcao['efeito_base']['caixa'] > 5000:
            return f"✅ {assessor['nome']}: 'Melhora nossa situação financeira.'"
        elif opcao['efeito_base']['caixa'] < -10000:
            return f"⚠️ {assessor['nome']}: 'Vai drenar recursos rapidamente.'"
        else:
            return f"➡️ {assessor['nome']}: 'Impacto financeiro moderado.'"
    elif assessor['especialidade'] == 'risco':
        if opcao['efeito_base'].get('risco', 0) > 20:
            return f"🚨 {assessor['nome']}: 'ALTO RISCO detectado.'"
        elif opcao['efeito_base'].get('risco', 0) > 10:
            return f"⚠️ {assessor['nome']}: 'Risco moderado.'"
        else:
            return f"✅ {assessor['nome']}: 'Risco aceitável.'"
    else:
        if random.random() < assessor['confiabilidade']:
            if opcao['efeito_base']['pop'] > 0:
                return f"✅ {assessor['nome']}: 'Parece boa opção.'"
            else:
                return f"⚠️ {assessor['nome']}: 'Considere alternativas.'"
        else:
            if opcao['efeito_base']['pop'] > 0:
                return f"⚠️ {assessor['nome']}: 'Não recomendo.'"
            else:
                return f"✅ {assessor['nome']}: 'Pode funcionar.'"

def aplicar_consequencias(opcao):
    bonus = {"pop": 0, "caixa": 0, "energia": 0, "midia": 0}
    
    if st.session_state.partido_escolhido == "esquerda":
        bonus = {"pop": 1, "caixa": -500, "energia": 2, "midia": 1}
    elif st.session_state.partido_escolhido == "centro":
        bonus = {"pop": 0, "caixa": 1000, "energia": 1, "midia": 2}
    elif st.session_state.partido_escolhido == "direita":
        bonus = {"pop": -1, "caixa": 2000, "energia": 0, "midia": 0}
    
    mult = 1.0
    if st.session_state.dificuldade == "facil":
        mult = 1.1
    elif st.session_state.dificuldade == "dificil":
        mult = 0.85
    elif st.session_state.dificuldade == "hardcore":
        mult = 0.7
    
    variabilidade = random.uniform(0.8, 1.2)
    
    efeito_pop = (opcao['efeito_base']['pop'] + bonus['pop']) * mult * variabilidade
    efeito_caixa = (opcao['efeito_base']['caixa'] + bonus['caixa']) * mult * variabilidade
    efeito_energia = (opcao['efeito_base']['energia'] + bonus['energia']) * mult * variabilidade
    efeito_midia = (opcao['efeito_base'].get('midia', 0) + bonus['midia']) * mult * variabilidade
    efeito_risco = opcao['efeito_base'].get('risco', 0) * mult
    efeito_coalizao = opcao['efeito_base'].get('coalizao', 0) * mult
    
    st.session_state.popularidade += efeito_pop
    st.session_state.caixa += efeito_caixa
    st.session_state.energia += efeito_energia
    st.session_state.midia += efeito_midia
    st.session_state.risco_escandalo += efeito_risco
    
    if efeito_coalizao != 0:
        for partido in st.session_state.coalizao_apoio:
            st.session_state.coalizao_apoio[partido] += efeito_coalizao * random.uniform(0.8, 1.2)
            st.session_state.coalizao_apoio[partido] = max(0, min(100, st.session_state.coalizao_apoio[partido]))
    
    for estado in st.session_state.estados_support:
        variacao = random.uniform(-3, 4)
        if efeito_pop > 0:
            variacao += 1
        st.session_state.estados_support[estado] += variacao
        st.session_state.estados_support[estado] = max(0, min(100, st.session_state.estados_support[estado]))
    
    st.session_state.popularidade = max(0, min(100, st.session_state.popularidade))
    st.session_state.energia = max(0, min(100, st.session_state.energia))
    st.session_state.midia = max(0, min(100, st.session_state.midia))
    st.session_state.risco_escandalo = max(0, min(100, st.session_state.risco_escandalo))
    
    if efeito_pop > 3:
        st.session_state.combo += 1
    else:
        st.session_state.combo = 0
    
    st.session_state.evolucao_popularidade.append(st.session_state.popularidade)
    st.session_state.evolucao_dias.append(st.session_state.dia)
    
    st.session_state.pesquisas.append({
        'dia': st.session_state.dia,
        'pop': st.session_state.popularidade + random.uniform(-3, 3),
        'margem': 3
    })
    
    st.session_state.historico.append({
        'dia': st.session_state.dia,
        'evento': st.session_state.evento_atual['titulo'] if st.session_state.evento_atual else 'N/A',
        'pop': st.session_state.popularidade,
        'caixa': st.session_state.caixa,
        'energia': st.session_state.energia
    })
    
    if st.session_state.risco_escandalo >= 80:
        st.session_state.total_escandalos += 1
        st.session_state.risco_escandalo = 30
        st.session_state.popularidade -= 15
        st.session_state.midia -= 20
        st.error("🚨 ESCÂNDALO EXPLODIU! Popularidade caiu!")
    
    st.session_state.energia = min(100, st.session_state.energia + 3)
    st.session_state.caixa += bonus['caixa']
    
    st.session_state.mensagem_feedback = opcao['descricao_oculta']

def verificar_condicoes():
    if st.session_state.popularidade <= 3:
        st.session_state.game_over = True
        return "DERROTA: Popularidade abaixo de 3%."
    
    if st.session_state.caixa <= 0:
        st.session_state.game_over = True
        return "DERROTA: Campanha falida."
    
    if st.session_state.energia <= 0:
        st.session_state.game_over = True
        return "DERROTA: Colapso de saúde."
    
    if st.session_state.midia <= 5:
        st.session_state.game_over = True
        return "DERROTA: Imprensa hostil."
    
    media_coalizao = sum(st.session_state.coalizao_apoio.values()) / len(st.session_state.coalizao_apoio)
    if media_coalizao <= 20:
        st.session_state.game_over = True
        return "DERROTA: Coalizão desfeita."
    
    if st.session_state.dia > st.session_state.total_dias:
        st.session_state.game_over = True
        
        votos_totais = 0
        eleitores_totais = sum(ESTADOS_DECISIVOS[e]['eleitores'] for e in ESTADOS_DECISIVOS.keys())
        
        for estado, apoio in st.session_state.estados_support.items():
            if apoio >= 45:
                votos_totais += ESTADOS_DECISIVOS[estado]['eleitores']
        
        percentual_votos = (votos_totais / eleitores_totais) * 100
        
        if percentual_votos >= 50:
            st.session_state.vitoria = True
            return f"VITÓRIA NO 1º TURNO! {percentual_votos:.1f}% dos votos!"
        elif percentual_votos >= 40:
            st.session_state.vitoria = True
            return f"2º TURNO! {percentual_votos:.1f}% dos votos."
        else:
            st.session_state.vitoria = False
            return f"ELIMINADO! {percentual_votos:.1f}% dos votos."
    
    return None

def gerar_evento():
    if st.session_state.risco_escandalo >= 50 and random.random() < 0.3:
        crises = [e for e in EVENTOS['geral'] if e['tipo'] == 'crise']
        if crises:
            return random.choice(crises)
    
    eventos_gerais = EVENTOS["geral"]
    eventos_ideologia = EVENTOS.get(st.session_state.partido_escolhido, [])
    
    if eventos_ideologia and random.random() < 0.25:
        pool_eventos = eventos_ideologia
    else:
        pool_eventos = eventos_gerais
    
    eventos_disponiveis = [e for e in pool_eventos if e['id'] not in st.session_state.eventos_usados[-10:]]
    
    if not eventos_disponiveis:
        eventos_disponiveis = pool_eventos
        st.session_state.eventos_usados = []
    
    evento = random.choice(eventos_disponiveis)
    st.session_state.eventos_usados.append(evento['id'])
    
    return evento

# ============================================================================
# GRÁFICOS
# ============================================================================

def criar_grafico_evolucao():
    fig = go.Figure()
    
    cor = "#DC143C" if st.session_state.partido_escolhido == 'esquerda' else "#FFD700" if st.session_state.partido_escolhido == 'centro' else "#0066CC"
    
    fig.add_trace(go.Scatter(
        x=st.session_state.evolucao_dias,
        y=st.session_state.evolucao_popularidade,
        mode='lines+markers',
        line=dict(color=cor, width=3),
        marker=dict(size=8)
    ))
    
    fig.add_hline(y=50, line_dash="dash", line_color="green")
    fig.add_hline(y=40, line_dash="dash", line_color="orange")
    
    fig.update_layout(
        title='📈 Evolução da Popularidade',
        xaxis_title='Dia',
        yaxis_title='%',
        yaxis_range=[0, 100],
        height=300,
        template='plotly_white'
    )
    
    return fig

def criar_grafico_estados():
    estados = list(st.session_state.estados_support.keys())
    valores = list(st.session_state.estados_support.values())
    cores = [ESTADOS_DECISIVOS[e]['cor'] for e in estados]
    
    fig = go.Figure(data=[go.Bar(x=estados, y=valores, marker_color=cores)])
    fig.add_hline(y=45, line_dash="dash", line_color="green")
    
    fig.update_layout(
        title='🗺️ Apoio por Estado',
        yaxis_range=[0, 100],
        height=300,
        template='plotly_white',
        showlegend=False
    )
    
    return fig

def criar_grafico_coalizao():
    partidos = list(st.session_state.coalizao_apoio.keys())
    valores = list(st.session_state.coalizao_apoio.values())
    cores = [PARTIDOS_COALIZAO[p]['cor'] for p in partidos]
    
    fig = go.Figure(data=[go.Bar(x=[PARTIDOS_COALIZAO[p]['sigla'] for p in partidos], y=valores, marker_color=cores)])
    fig.add_hline(y=50, line_dash="dash", line_color="orange")
    
    fig.update_layout(
        title='🤝 Apoio da Coalizão',
        yaxis_range=[0, 100],
        height=250,
        template='plotly_white',
        showlegend=False
    )
    
    return fig

# ============================================================================
# TELAS
# ============================================================================

def mostrar_tela_inicial():
    st.markdown("<h1 style='text-align: center;'>🇧🇷 CANDIDATO 2026</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Simulador Presidencial HARDCORE</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎮 MECÂNICAS
        
        - 🎭 **Consequências Ocultas** - Não veja números exatos
        - 👥 **5 Assessores** - Cada um com confiabilidade diferente
        - 🤝 **Coalizão** - Mantenha 4 partidos aliados
        - 🗺️ **8 Estados** - Precisa ganhar estados específicos
        - 🚨 **Escândalos** - Risk meter que pode explodir
        - 📊 **Pesquisas com Margem** - Dados não são 100% precisos
        
        ### ⚠️ DIFICULDADE
        
        Este jogo é **INTENCIONALMENTE DIFÍCIL**. Requer estratégia!
        """)
        
        dificuldade = st.radio("Dificuldade:", ["Fácil", "Normal", "Difícil", "HARDCORE"])
        diff_map = {"Fácil": "facil", "Normal": "normal", "Difícil": "dificil", "HARDCORE": "hardcore"}
        st.session_state.dificuldade_temp = diff_map[dificuldade]
    
    with col2:
        st.markdown("### 🏆 Recorde")
        hs = load_high_score()
        st.metric("Maior Popularidade", f"{hs['score']:.1f}%")
        st.write(f"**Partido:** {hs['partido']}")
        st.write(f"**Dificuldade:** {hs['dificuldade']}")
    
    st.divider()
    
    st.markdown("### 🎭 Escolha Sua Ideologia")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);">
            <h2 style="margin: 0;">🔴</h2>
            <h3>ESQUERDA</h3>
            <p>+1% Pop por decisão</p>
            <p>+2 Energia/dia</p>
            <p>-R$ 500/dia</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔴 Esquerda", key="btn_esq", use_container_width=True):
            st.session_state.partido_escolhido = "esquerda"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);">
            <h2 style="margin: 0;">🟡</h2>
            <h3>CENTRO</h3>
            <p>±0% Pop</p>
            <p>+1 Energia/dia</p>
            <p>+R$ 1.000/dia</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🟡 Centro", key="btn_cen", use_container_width=True):
            st.session_state.partido_escolhido = "centro"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #0066CC 0%, #003366 100%);">
            <h2 style="margin: 0;">🔵</h2>
            <h3>DIREITA</h3>
            <p>-1% Pop por decisão</p>
            <p>±0 Energia/dia</p>
            <p>+R$ 2.000/dia</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔵 Direita", key="btn_dir", use_container_width=True):
            st.session_state.partido_escolhido = "direita"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()

def mostrar_jogo():
    col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
    with col_h1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 20px; border-radius: 15px; color: white;">
            <h2 style="margin: 0;">🇧🇷 CAMPANHA 2026</h2>
            <p style="margin: 10px 0 0 0;">Dia {st.session_state.dia}/{st.session_state.total_dias} | {st.session_state.dificuldade.upper()}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_h2:
        if st.button("📊 Gráficos", use_container_width=True):
            st.session_state.show_stats = not st.session_state.show_stats
    with col_h3:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.partido_escolhido = None
            st.rerun()
    
    if st.session_state.risco_escandalo >= 60:
        st.markdown(f"""
        <div class="scandal-warning">
            <h3 style="margin: 0;">🚨 ALERTA DE ESCÂNDALO</h3>
            <p style="margin: 5px 0 0 0;">Risco: {st.session_state.risco_escandalo:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.combo >= 3:
        st.markdown(f"""
        <div style="text-align: center; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 10px; border-radius: 20px; color: white; margin: 10px 0;">
            🔥 COMBO x{st.session_state.combo}
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Popularidade</h3>
            <h1>{st.session_state.popularidade:.1f}%</h1>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.popularidade / 100)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Caixa</h3>
            <h1>R$ {st.session_state.caixa:,.0f}</h1>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(st.session_state.caixa / 200000, 1.0))
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚡ Energia</h3>
            <h1>{st.session_state.energia}%</h1>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.energia / 100)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📰 Mídia</h3>
            <h1>{st.session_state.midia:.0f}</h1>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.midia / 100)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🚨 Risco</h3>
            <h1>{st.session_state.risco_escandalo:.0f}%</h1>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.risco_escandalo / 100)
    
    st.divider()
    
    st.markdown("### 👥 Assessores")
    cols_ass = st.columns(5)
    for i, (key, assessor) in enumerate(ASSESSORES.items()):
        with cols_ass[i]:
            selected = st.session_state.assessor_selecionado == key
            st.markdown(f"""
            <div class="advisor-card {'selected' if selected else ''}">
                <div style="font-size: 24px;">{assessor['icone']}</div>
                <strong>{assessor['nome']}</strong><br>
                <small>{assessor['confiabilidade']*100:.0f}% confiável</small>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Selecionar", key=f"ass_{key}", use_container_width=True):
                st.session_state.assessor_selecionado = key
                st.rerun()
    
    if st.session_state.show_stats:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.plotly_chart(criar_grafico_evolucao(), use_container_width=True)
        with col_g2:
            st.plotly_chart(criar_grafico_estados(), use_container_width=True)
        
        col_g3, col_g4 = st.columns(2)
        with col_g3:
            st.plotly_chart(criar_grafico_coalizao(), use_container_width=True)
        with col_g4:
            st.markdown("### 🗺️ Estados")
            for estado, dados in ESTADOS_DECISIVOS.items():
                apoio = st.session_state.estados_support[estado]
                status = "✅" if apoio >= 45 else "❌"
                st.write(f"{status} **{estado}**: {apoio:.1f}%")
        
        st.divider()
    
    if st.session_state.game_over:
        if st.session_state.vitoria:
            st.balloons()
            st.markdown(f"""
            <div class="victory-screen">
                <h1 style="margin: 0;">🎉 VITÓRIA!</h1>
                <p style="font-size: 20px;">Popularidade: <strong>{st.session_state.popularidade:.1f}%</strong></p>
                <p>Dias: <strong>{st.session_state.dia}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            if save_high_score(st.session_state.popularidade, st.session_state.dia, st.session_state.partido_escolhido, st.session_state.dificuldade):
                st.success("🏆 NOVO RECORDE!")
        else:
            st.markdown(f"""
            <div class="defeat-screen">
                <h1 style="margin: 0;">😞 DERROTA</h1>
                <p style="font-size: 20px;">{st.session_state.msg_fim}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🎮 Jogar Novamente", use_container_width=True):
            st.session_state.partido_escolhido = None
            st.rerun()
    else:
        if st.session_state.evento_atual is None:
            st.session_state.evento_atual = gerar_evento()
        
        evento = st.session_state.evento_atual
        
        classe = "crisis" if evento['tipo'] == 'crise' else ""
        st.markdown(f"""
        <div class="event-card {classe}">
            <div style="font-size: 48px;">{evento['icon']}</div>
            <h2 style="margin: 10px 0;">{evento['titulo']}</h2>
            <p style="font-size: 16px; line-height: 1.6;">{evento['desc']}</p>
            <div>
                <span style="background: #667eea; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">IMPACTO: {evento['impacto'].upper()}</span>
                <span style="background: #ff4757; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px; margin-left: 10px;">{evento['tipo'].upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        assessor = ASSESSORES[st.session_state.assessor_selecionado]
        st.info(f"💡 {assessor['icone']} {assessor['nome']}: {assessor['descricao']}")
        
        st.warning("⚠️ Consequências OCULTAS! Confie no seu assessor e analise o contexto.")
        
        for i, opcao in enumerate(evento['opcoes']):
            conselho = get_assessor_advice(evento, i)
            
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0;">
                <strong>Opção {i+1}:</strong> {opcao['texto']}<br>
                <em>{opcao['descricao_oculta']}</em><br>
                <strong>Conselho:</strong> {conselho}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Escolher Opção {i+1}", key=f"opt_{i}", use_container_width=True):
                aplicar_consequencias(opcao)
                st.session_state.evento_atual = None
                st.session_state.dia += 1
                
                msg = verificar_condicoes()
                if msg:
                    st.session_state.msg_fim = msg
                
                st.rerun()
        
        if st.session_state.mensagem_feedback:
            st.info(f"💬 {st.session_state.mensagem_feedback}")
        
        with st.expander("💡 Dicas"):
            st.write("""
            - Mantenha energia acima de 30%
            - Caixa acima de R$ 50.000 para emergências
            - Mídia acima de 30%
            - Coalizão média acima de 50%
            - Risco acima de 60% = perigo
            - Precisa de 45% em cada estado
            """)

def render_sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/ballot-box-with-ball.png", width=80)
        st.title("🎛️ Painel")
        
        if 'partido_escolhido' in st.session_state and st.session_state.partido_escolhido:
            st.write(f"**Partido:** {st.session_state.partido_escolhido.upper()}")
            st.write(f"**Dificuldade:** {st.session_state.dificuldade.upper()}")
            st.divider()
            
            st.write("### 📊 Status")
            st.write(f"📈 Pop: {st.session_state.popularidade:.1f}%")
            st.write(f"💰 Caixa: R$ {st.session_state.caixa:,.0f}")
            st.write(f"⚡ Energia: {st.session_state.energia}%")
            st.write(f"📰 Mídia: {st.session_state.midia:.0f}")
            st.write(f"🚨 Risco: {st.session_state.risco_escandalo:.0f}%")
            st.divider()
            
            if st.session_state.combo >= 2:
                st.write(f"🔥 **Combo:** x{st.session_state.combo}")
            
            st.write("### 🤝 Coalizão")
            for partido, apoio in st.session_state.coalizao_apoio.items():
                st.write(f"{PARTIDOS_COALIZAO[partido]['sigla']}: {apoio:.1f}%")
            
            st.divider()
            
            st.write("### 🏅 Conquistas")
            total = len(ACHIEVEMENTS)
            unlocked = len(st.session_state.conquistas_unlocked)
            st.write(f"{unlocked}/{total}")
            st.progress(unlocked / total)

def check_achievements():
    new_achievements = []
    
    if st.session_state.dia >= 2 and "first_day" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("first_day")
        new_achievements.append("first_day")
    
    if st.session_state.popularidade >= 30 and "pop_30" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("pop_30")
        new_achievements.append("pop_30")
    
    if st.session_state.popularidade >= 50 and "pop_50" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("pop_50")
        new_achievements.append("pop_50")
    
    if st.session_state.popularidade >= 70 and "pop_70" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("pop_70")
        new_achievements.append("pop_70")
    
    if st.session_state.caixa >= 500000 and "rich" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("rich")
        new_achievements.append("rich")
    
    if st.session_state.total_escandalos >= 3 and "survivor" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("survivor")
        new_achievements.append("survivor")
    
    return new_achievements

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
    if 'conquistas_unlocked' not in st.session_state:
        st.session_state.conquistas_unlocked = []
    if 'assessor_selecionado' not in st.session_state:
        st.session_state.assessor_selecionado = "estrategista"
    if 'partido_escolhido' not in st.session_state:
        st.session_state.partido_escolhido = None
    
    render_sidebar()
    
    if st.session_state.partido_escolhido is None:
        mostrar_tela_inicial()
    else:
        new_achs = check_achievements()
        if new_achs:
            for ach_id in new_achs:
                ach = ACHIEVEMENTS.get(ach_id, {})
                st.success(f"🏆 CONQUISTA: {ach.get('icon', '🏆')} {ach.get('name', 'Unknown')}!")
        
        mostrar_jogo()

if __name__ == "__main__":
    main()
