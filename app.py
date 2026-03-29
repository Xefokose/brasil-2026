
import streamlit as st
import random
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import hashlib

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA E CSS PERSONALIZADO
# ============================================================================
st.set_page_config(
    page_title="🇧🇷 Candidato 2026 - Simulador Presidencial",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Jogo desenvolvido para fins educacionais. Nenhum político real foi usado."
    }
)

# CSS PROFISSIONAL E MODERNO
st.markdown("""
<style>
    /* Importar fonte */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Estilos Gerais */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Cards de Métricas */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
        margin: 10px 0;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-card h3 {
        margin: 0;
        font-size: 14px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-card h1 {
        margin: 10px 0 0 0;
        font-size: 32px;
        font-weight: 700;
    }
    .metric-card .subtitle {
        font-size: 12px;
        opacity: 0.8;
        margin-top: 5px;
    }
    
    /* Cards de Eventos */
    .event-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        border-left: 6px solid #667eea;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .event-card h2 {
        color: #333;
        margin-top: 0;
    }
    .event-card .icon {
        font-size: 48px;
        margin-bottom: 10px;
    }
    
    /* Botões Personalizados */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* Cards de Conquistas */
    .achievement-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 5px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .achievement-card.locked {
        background: #e0e0e0;
        color: #999;
    }
    .achievement-icon {
        font-size: 24px;
    }
    
    /* Barras de Progresso */
    .progress-container {
        background: #e0e0e0;
        border-radius: 10px;
        padding: 3px;
        margin: 5px 0;
    }
    .progress-bar {
        height: 20px;
        border-radius: 8px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 12px;
    }
    
    /* News Feed */
    .news-item {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .news-item.urgent {
        border-left-color: #dc3545;
        background: #fff5f5;
    }
    .news-item.positive {
        border-left-color: #28a745;
        background: #f0fff4;
    }
    
    /* Tela de Vitória/Derrota */
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
    
    /* Tooltip */
    .tooltip {
        position: relative;
        cursor: help;
    }
    
    /* Animações */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Container principal */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Header */
    .game-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        text-align: center;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    /* Regional Support */
    .region-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 5px 0;
    }
    
    /* Combo Counter */
    .combo-counter {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 10px 20px;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SISTEMA DE CONQUISTAS (ACHIEVEMENTS)
# ============================================================================
ACHIEVEMENTS = {
    "first_vote": {
        "name": "Primeiro Voto",
        "desc": "Complete seu primeiro dia de campanha",
        "icon": "🗳️",
        "rarity": "common"
    },
    "popularity_10": {
        "name": "Começo Promissor",
        "desc": "Alcance 10% de popularidade",
        "icon": "📈",
        "rarity": "common"
    },
    "popularity_30": {
        "name": "Em Ascensão",
        "desc": "Alcance 30% de popularidade",
        "icon": "🚀",
        "rarity": "uncommon"
    },
    "popularity_50": {
        "name": "Favorito",
        "desc": "Alcance 50% de popularidade",
        "icon": "👑",
        "rarity": "rare"
    },
    "popularity_70": {
        "name": "Lenda Viva",
        "desc": "Alcance 70% de popularidade",
        "icon": "🏆",
        "rarity": "legendary"
    },
    "rich_campaign": {
        "name": "Caixa Cheio",
        "desc": "Tenha R$ 500.000 em caixa",
        "icon": "💰",
        "rarity": "uncommon"
    },
    "full_energy": {
        "name": "Maratonista",
        "desc": "Mantenha 100% de energia por 5 dias",
        "icon": "⚡",
        "rarity": "rare"
    },
    "coalition_master": {
        "name": "Negociador",
        "desc": "Feche 5 alianças partidárias",
        "icon": "🤝",
        "rarity": "rare"
    },
    "scandal_survivor": {
        "name": "Sobrevivente",
        "desc": "Sobreviva a 3 escândalos",
        "icon": "🛡️",
        "rarity": "epic"
    },
    "first_turn_victory": {
        "name": "Vitória Esmagadora",
        "desc": "Vença no primeiro turno",
        "icon": "🎉",
        "rarity": "legendary"
    },
    "comeback_king": {
        "name": "Rei do Comeback",
        "desc": "Volte de menos de 10% para vitória",
        "icon": "🔄",
        "rarity": "legendary"
    },
    "perfect_campaign": {
        "name": "Campanha Perfeita",
        "desc": "Termine sem nenhum escândalo",
        "icon": "✨",
        "rarity": "legendary"
    }
}

# ============================================================================
# BANCO DE DADOS DE EVENTOS (CENÁRIO BRASILEIRO REALISTA)
# ============================================================================
EVENTOS = {
    "geral": [
        {
            "titulo": "📺 Debate Presidencial na TV",
            "desc": "O maior debate do ano está no ar. 50 milhões de brasileiros estão assistindo. Sua performance pode definir a eleição.",
            "icon": "📺",
            "tipo": "debate",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Atacar adversários com dados", "efeito": {"pop": 8, "caixa": 0, "energia": -15, "midia": 5}, "feedback": "Argumentos sólidos impressionaram os eleitores indecisos."},
                {"texto": "Focar em propostas emocionais", "efeito": {"pop": 10, "caixa": -2000, "energia": -20, "midia": 3}, "feedback": "Discurso emocionante viralizou nas redes sociais."},
                {"texto": "Postura conciliadora", "efeito": {"pop": 5, "caixa": 0, "energia": -10, "midia": 8}, "feedback": "Imprensa elogiou sua maturidade política."},
                {"texto": "Ignorar ataques e focar no futuro", "efeito": {"pop": 3, "caixa": 0, "energia": -12, "midia": 6}, "feedback": "Alguns acharam evasivo, outros prudente."}
            ]
        },
        {
            "titulo": "🚨 Escândalo de Corrupção Vaza",
            "desc": "Um membro da sua coalizão foi pego em esquema de corrupção. A imprensa cobra posicionamento imediato.",
            "icon": "🚨",
            "tipo": "crise",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Romper aliança imediatamente", "efeito": {"pop": 5, "caixa": -5000, "energia": -20, "midia": -5}, "feedback": "Ganhou imagem de íntegro, mas perdeu apoio político."},
                {"texto": "Aguardar investigação", "efeito": {"pop": -8, "caixa": 0, "energia": -10, "midia": -10}, "feedback": "Eleitores interpretaram como omissão."},
                {"texto": "Defender aliado publicamente", "efeito": {"pop": -15, "caixa": 0, "energia": -15, "midia": -15}, "feedback": "Base manteve apoio, mas indecisos fugiram."},
                {"texto": "Criar CPI para investigar", "efeito": {"pop": 3, "caixa": -10000, "energia": -25, "midia": 5}, "feedback": "Mostrou ação, mas gastou capital político."}
            ]
        },
        {
            "titulo": "💸 Crise Econômica Internacional",
            "desc": "Dólar dispara, bolsa cai e FMI emite alerta. Eleitores estão preocupados com emprego e inflação.",
            "icon": "💸",
            "tipo": "economia",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Prometer controle de preços", "efeito": {"pop": 8, "caixa": -10000, "energia": -15, "midia": 3}, "feedback": "Popular nas classes baixas, economistas criticam."},
                {"texto": "Defender autonomia do Banco Central", "efeito": {"pop": 2, "caixa": 0, "energia": -10, "midia": 8}, "feedback": "Mercado reagiu bem, mas pouco popular."},
                {"texto": "Culpar governo anterior", "efeito": {"pop": 5, "caixa": 0, "energia": -8, "midia": -5}, "feedback": "Base aprovou, mas pareceu evasivo."},
                {"texto": "Anunciar pacote de emergência", "efeito": {"pop": 10, "caixa": -25000, "energia": -20, "midia": 5}, "feedback": "Medidas urgentes acalmaram mercados."}
            ]
        },
        {
            "titulo": "🏥 Pandemia/ Crise de Saúde",
            "desc": "Novo surto de doença preocupa população. Hospitais lotados e fila de vacinação cresce.",
            "icon": "🏥",
            "tipo": "saude",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Visitar hospitais pessoalmente", "efeito": {"pop": 7, "caixa": -3000, "energia": -30, "midia": 5}, "feedback": "Imagem humanizada, mas risco de contágio."},
                {"texto": "Anunciar verba emergencial", "efeito": {"pop": 5, "caixa": -20000, "energia": -10, "midia": 6}, "feedback": "Ação concreta elogiada por gestores."},
                {"texto": "Culpar gestão anterior", "efeito": {"pop": 3, "caixa": 0, "energia": -5, "midia": -8}, "feedback": "Pareceu insensível em momento de crise."},
                {"texto": "Convocar cientistas para coletiva", "efeito": {"pop": 4, "caixa": -2000, "energia": -15, "midia": 10}, "feedback": "Transparência técnica bem recebida."}
            ]
        },
        {
            "titulo": "🌳 Queimadas na Amazônia",
            "desc": "Imagens de satélite mostram aumento de desmatamento. Comunidade internacional pressiona por ações.",
            "icon": "🌳",
            "tipo": "ambiente",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Enviar tropas para fiscalização", "efeito": {"pop": 6, "caixa": -15000, "energia": -20, "midia": 8}, "feedback": "Ação firme agradou ambientalistas."},
                {"texto": "Negociar com governadores", "efeito": {"pop": 3, "caixa": -5000, "energia": -15, "midia": 5}, "feedback": "Solução política, mas lenta."},
                {"texto": "Priorizar desenvolvimento regional", "efeito": {"pop": -5, "caixa": 5000, "energia": -10, "midia": -10}, "feedback": "Base rural apoiou, internacional criticou."},
                {"texto": "Propor fundo internacional", "efeito": {"pop": 4, "caixa": 10000, "energia": -15, "midia": 7}, "feedback": "Solução criativa atraiu investimentos."}
            ]
        },
        {
            "titulo": "👷 Reforma Trabalhista",
            "desc": "Centrais sindicais e empresários cobram posicionamento sobre leis trabalhistas.",
            "icon": "👷",
            "tipo": "trabalho",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Ampliar direitos trabalhistas", "efeito": {"pop": 8, "caixa": -10000, "energia": -15, "midia": 5}, "feedback": "Sindicatos mobilizaram apoio."},
                {"texto": "Flexibilizar para gerar empregos", "efeito": {"pop": -5, "caixa": 8000, "energia": -10, "midia": 3}, "feedback": "Empresários apoiaram, trabalhadores criticaram."},
                {"texto": "Manter legislação atual", "efeito": {"pop": 0, "caixa": 0, "energia": -5, "midia": 0}, "feedback": "Posição segura, mas sem entusiasmo."},
                {"texto": "Criar mesa de diálogo tripartite", "efeito": {"pop": 4, "caixa": -3000, "energia": -20, "midia": 8}, "feedback": "Abordagem negociada elogiada."}
            ]
        },
        {
            "titulo": "🔫 Segurança Pública",
            "desc": "Índices de violência batem recorde. População exige medidas urgentes.",
            "icon": "🔫",
            "tipo": "seguranca",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Mais investimento em policiamento", "efeito": {"pop": 7, "caixa": -20000, "energia": -15, "midia": 5}, "feedback": "Medida popular e concreta."},
                {"texto": "Focar em prevenção social", "efeito": {"pop": 4, "caixa": -15000, "energia": -20, "midia": 6}, "feedback": "Visão de longo prazo apreciada."},
                {"texto": "Liberalizar porte de armas", "efeito": {"pop": -8, "caixa": 0, "energia": -10, "midia": -10}, "feedback": "Polêmica dividiu opiniões drasticamente."},
                {"texto": "Intervenção federal em estados", "efeito": {"pop": 5, "caixa": -25000, "energia": -25, "midia": 8}, "feedback": "Medida extrema gerou debate constitucional."}
            ]
        },
        {
            "titulo": "🎓 Educação Básica",
            "desc": "Brasil ocupa posição ruim no PISA. Professores e pais cobram melhorias.",
            "icon": "🎓",
            "tipo": "educacao",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Aumentar salário de professores", "efeito": {"pop": 6, "caixa": -25000, "energia": -15, "midia": 7}, "feedback": "Categoria valorizada apoiou."},
                {"texto": "Investir em tecnologia nas escolas", "efeito": {"pop": 5, "caixa": -20000, "energia": -12, "midia": 8}, "feedback": "Modernização bem recebida."},
                {"texto": "Focar em ensino técnico", "efeito": {"pop": 4, "caixa": -15000, "energia": -10, "midia": 5}, "feedback": "Alinhado com demanda do mercado."},
                {"texto": "Privatizar gestão escolar", "efeito": {"pop": -10, "caixa": 10000, "energia": -20, "midia": -8}, "feedback": "Controvérsia enorme entre educadores."}
            ]
        },
        {
            "titulo": "🏠 Habitação Popular",
            "desc": "Déficit habitacional cresce. Movimentos sociais ocupam prédios em grandes cidades.",
            "icon": "🏠",
            "tipo": "habitacao",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Construir 1 milhão de casas", "efeito": {"pop": 10, "caixa": -50000, "energia": -25, "midia": 8}, "feedback": "Proposta ambiciosa empolgou eleitores."},
                {"texto": "Subsidiar aluguel social", "efeito": {"pop": 5, "caixa": -20000, "energia": -15, "midia": 6}, "feedback": "Solução rápida mas paliativa."},
                {"texto": "Regularizar favelas existentes", "efeito": {"pop": 6, "caixa": -15000, "energia": -20, "midia": 7}, "feedback": "Abordagem pragmática elogiada."},
                {"texto": "Parceria com construtoras", "efeito": {"pop": 3, "caixa": -10000, "energia": -10, "midia": 4}, "feedback": "Solução viável mas pouco popular."}
            ]
        },
        {
            "titulo": "⚡ Crise Energética",
            "desc": "Reservatórios de hidrelétricas em nível crítico. Risco de apagão preocupa indústria.",
            "icon": "⚡",
            "tipo": "energia",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Racionamento preventivo", "efeito": {"pop": -5, "caixa": 5000, "energia": -10, "midia": -5}, "feedback": "Impopular mas responsável."},
                {"texto": "Ativar termelétricas", "efeito": {"pop": 2, "caixa": -30000, "energia": -15, "midia": 3}, "feedback": "Solução cara evitou apagões."},
                {"texto": "Importar energia de vizinhos", "efeito": {"pop": 3, "caixa": -20000, "energia": -12, "midia": 5}, "feedback": "Solução rápida e eficaz."},
                {"texto": "Campanha de economia", "efeito": {"pop": 0, "caixa": -2000, "energia": -20, "midia": 6}, "feedback": "Conscientização teve adesão mista."}
            ]
        },
        {
            "titulo": "📱 Fake News nas Redes",
            "desc": "Vídeo manipulado seu viraliza no WhatsApp. Milhões já viram antes da desmentido.",
            "icon": "📱",
            "tipo": "midia",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Processar criadores do vídeo", "efeito": {"pop": 2, "caixa": -10000, "energia": -15, "midia": 5}, "feedback": "Ação jurídica mostrou seriedade."},
                {"texto": "Desmentir em rede nacional", "efeito": {"pop": 5, "caixa": -5000, "energia": -20, "midia": 8}, "feedback": "Resposta rápida limitou danos."},
                {"texto": "Ignorar e não dar atenção", "efeito": {"pop": -8, "caixa": 0, "energia": -5, "midia": -10}, "feedback": "Fake news continuou circulando."},
                {"texto": "Pedir ajuda às plataformas", "efeito": {"pop": 3, "caixa": -3000, "energia": -10, "midia": 6}, "feedback": "Redes sociais removeram conteúdo."}
            ]
        },
        {
            "titulo": "🤝 Aliança Partidária",
            "desc": "Partido com 50 deputados oferece apoio em troca de cargos no futuro governo.",
            "icon": "🤝",
            "tipo": "politica",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Aceitar e negociar cargos", "efeito": {"pop": -3, "caixa": 15000, "energia": -10, "midia": -5}, "feedback": "Base parlamentar fortalecida, mas criticaram."},
                {"texto": "Recusar mantendo coerência", "efeito": {"pop": 5, "caixa": 0, "energia": 5, "midia": 8}, "feedback": "Imagem de integridade reforçada."},
                {"texto": "Negociar apenas políticas públicas", "efeito": {"pop": 3, "caixa": 5000, "energia": -15, "midia": 6}, "feedback": "Meio-termo bem recebido."},
                {"texto": "Pedir tempo para decidir", "efeito": {"pop": 0, "caixa": 0, "energia": -5, "midia": 0}, "feedback": "Adiou decisão sem ganhar nada."}
            ]
        },
        {
            "titulo": "📊 Pesquisa Eleitoral Divulgada",
            "desc": "Instituto renomado libera nova pesquisa. Seu desempenho define estratégia dos próximos dias.",
            "icon": "📊",
            "tipo": "pesquisa",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Comemorar e usar na propaganda", "efeito": {"pop": 3, "caixa": -5000, "energia": -5, "midia": 5}, "feedback": "Momentum positivo mantido."},
                {"texto": "Ficar cauteloso e trabalhar mais", "efeito": {"pop": 2, "caixa": -3000, "energia": -15, "midia": 3}, "feedback": "Humildade elogiada pela imprensa."},
                {"texto": "Criticar metodologia da pesquisa", "efeito": {"pop": -2, "caixa": 0, "energia": -10, "midia": -5}, "feedback": "Pareceu desesperado para alguns."},
                {"texto": "Focar em estados onde vai mal", "efeito": {"pop": 4, "caixa": -10000, "energia": -20, "midia": 4}, "feedback": "Estratégia inteligente de recuperação."}
            ]
        },
        {
            "titulo": "🎬 Horário Eleitoral Gratuito",
            "desc": "Seu tempo no rádio e TV pode definir votos. Qual mensagem passar?",
            "icon": "🎬",
            "tipo": "midia",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Propostas detalhadas de governo", "efeito": {"pop": 4, "caixa": -8000, "energia": -15, "midia": 6}, "feedback": "Eleitores informados aprovaram."},
                {"texto": "Emoção e esperança no futuro", "efeito": {"pop": 7, "caixa": -8000, "energia": -12, "midia": 5}, "feedback": "Conexão emocional funcionou."},
                {"texto": "Ataques aos adversários", "efeito": {"pop": 5, "caixa": -8000, "energia": -10, "midia": -3}, "feedback": "Base animou, indecisos recearam."},
                {"texto": "Depoimentos de apoiadores", "efeito": {"pop": 5, "caixa": -8000, "energia": -8, "midia": 4}, "feedback": "Testemunhos reais convenceram."}
            ]
        },
        {
            "titulo": "🌾 Crise no Agronegócio",
            "desc": "Produtores rurais protestam por preços baixos e custos altos. Bancada ruralista cobra posição.",
            "icon": "🌾",
            "tipo": "agro",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Subsidiar insumos agrícolas", "efeito": {"pop": 6, "caixa": -30000, "energia": -15, "midia": 5}, "feedback": "Setor produtivo apoiou."},
                {"texto": "Negociar com China exportações", "efeito": {"pop": 4, "caixa": -10000, "energia": -20, "midia": 7}, "feedback": "Solução de mercado elogiada."},
                {"texto": "Focar em agricultura familiar", "efeito": {"pop": 3, "caixa": -15000, "energia": -12, "midia": 4}, "feedback": "Equilíbrio entre setores."},
                {"texto": "Manter política atual", "efeito": {"pop": -2, "caixa": 0, "energia": -5, "midia": -3}, "feedback": "Visto como omisso na crise."}
            ]
        }
    ],
    "esquerda": [
        {
            "titulo": "👊 Mobilização Sindical",
            "desc": "Centrais sindicais convocam greve geral e pedem seu apoio público.",
            "icon": "👊",
            "tipo": "trabalho",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Apoiar greve publicamente", "efeito": {"pop": 10, "caixa": -5000, "energia": -20, "midia": -5}, "feedback": "Base trabalhista mobilizada a seu favor."},
                {"texto": "Chamar para negociação", "efeito": {"pop": 3, "caixa": 0, "energia": -15, "midia": 5}, "feedback": "Posição moderada agradou ambos lados."},
                {"texto": "Manter neutralidade", "efeito": {"pop": -8, "caixa": 0, "energia": -5, "midia": 0}, "feedback": "Base sentiu-se traída."}
            ]
        },
        {
            "titulo": "🏛️ Nacionalização de Recursos",
            "desc": "Descoberta de grande reserva mineral gera debate sobre exploração estatal vs privada.",
            "icon": "🏛️",
            "tipo": "economia",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Defender estatal exclusiva", "efeito": {"pop": 12, "caixa": -10000, "energia": -20, "midia": 5}, "feedback": "Soberania nacional elogiada pela base."},
                {"texto": "Parceria público-privada", "efeito": {"pop": 5, "caixa": 15000, "energia": -15, "midia": 3}, "feedback": "Solução pragmática mas criticada."},
                {"texto": "Concessão total à iniciativa privada", "efeito": {"pop": -15, "caixa": 25000, "energia": -10, "midia": -10}, "feedback": "Base progressista revoltada."}
            ]
        },
        {
            "titulo": "📚 Universidade Pública",
            "desc": "Cortes no orçamento das federais geram protestos de estudantes e professores.",
            "icon": "📚",
            "tipo": "educacao",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Prometer restaurar orçamento", "efeito": {"pop": 8, "caixa": -20000, "energia": -15, "midia": 6}, "feedback": "Comunidade acadêmica apoiou."},
                {"texto": "Propor eficiência sem cortes", "efeito": {"pop": 3, "caixa": -5000, "energia": -12, "midia": 4}, "feedback": "Bem intencionado mas vago."},
                {"texto": "Sugerir parcerias com empresas", "efeito": {"pop": -5, "caixa": 10000, "energia": -10, "midia": -5}, "feedback": "Visto como privatização disfarçada."}
            ]
        }
    ],
    "centro": [
        {
            "titulo": "⚖️ Reforma do Sistema Político",
            "desc": "Proposta de mudança no sistema eleitoral divide Congresso e opinião pública.",
            "icon": "⚖️",
            "tipo": "politica",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Apoiar reforma completa", "efeito": {"pop": 6, "caixa": -5000, "energia": -20, "midia": 8}, "feedback": "Imagem de reformador consolidada."},
                {"texto": "Propor mudanças graduais", "efeito": {"pop": 4, "caixa": -2000, "energia": -15, "midia": 5}, "feedback": "Prudência elogiada por analistas."},
                {"texto": "Manter sistema atual", "efeito": {"pop": -3, "caixa": 0, "energia": -5, "midia": -3}, "feedback": "Visto como conservador demais."}
            ]
        },
        {
            "titulo": "🤝 Pacto Federativo",
            "desc": "Governadores de todos os estados cobram mais autonomia e recursos.",
            "icon": "🤝",
            "tipo": "politica",
            "impacto": "medio",
            "opcoes": [
                {"texto": "Ampliar repasses aos estados", "efeito": {"pop": 7, "caixa": -30000, "energia": -15, "midia": 6}, "feedback": "Governadores apoiaram fortemente."},
                {"texto": "Manter distribuição atual", "efeito": {"pop": 0, "caixa": 0, "energia": -10, "midia": 0}, "feedback": "Seguro mas sem ganhos políticos."},
                {"texto": "Exigir contrapartidas", "efeito": {"pop": 3, "caixa": 10000, "energia": -20, "midia": 5}, "feedback": "Negociação dura mas eficaz."}
            ]
        }
    ],
    "direita": [
        {
            "titulo": "💼 Desestatização",
            "desc": "Carteira de investimentos cobra agilidade em leilões de estatais.",
            "icon": "💼",
            "tipo": "economia",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Acelerar privatizações", "efeito": {"pop": 8, "caixa": 30000, "energia": -20, "midia": 5}, "feedback": "Mercado reagiu muito positivamente."},
                {"texto": "Manter ritmo atual", "efeito": {"pop": 0, "caixa": 0, "energia": -10, "midia": 0}, "feedback": "Nem agradou nem desagradou."},
                {"texto": "Revisar contratos anteriores", "efeito": {"pop": -10, "caixa": -5000, "energia": -15, "midia": -8}, "feedback": "Base econômica sentiu-se traída."}
            ]
        },
        {
            "titulo": "🔒 Lei e Ordem",
            "desc": "Onda de crimes violentos gera comoção. População exige mão dura.",
            "icon": "🔒",
            "tipo": "seguranca",
            "impacto": "alto",
            "opcoes": [
                {"texto": "Endurecer penas criminal", "efeito": {"pop": 10, "caixa": -5000, "energia": -15, "midia": 5}, "feedback": "Proposta popular entre eleitores."},
                {"texto": "Investir em inteligência policial", "efeito": {"pop": 5, "caixa": -15000, "energia": -20, "midia": 7}, "feedback": "Abordagem técnica elogiada."},
                {"texto": "Focar em reinserção social", "efeito": {"pop": -8, "caixa": -10000, "energia": -15, "midia": -5}, "feedback": "Base conservadora criticou."}
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
        "sigla": "FPT",
        "cor": "#DC143C",
        "cor_gradiente": "linear-gradient(135deg, #DC143C 0%, #8B0000 100%)",
        "icone": "🔴",
        "bonus": {"pop": 1, "caixa": -500, "energia": 2, "midia": 1},
        "descricao": "Foco em direitos sociais, trabalhistas e distribuição de renda",
        "base_eleitoral": ["Sindicatos", "Movimentos Sociais", "Universitários"],
        "dificuldade": "medio"
    },
    "centro": {
        "nome": "Aliança Democrática",
        "sigla": "ALD",
        "cor": "#FFD700",
        "cor_gradiente": "linear-gradient(135deg, #FFD700 0%, #FFA500 100%)",
        "icone": "🟡",
        "bonus": {"pop": 0, "caixa": 1000, "energia": 1, "midia": 2},
        "descricao": "Equilíbrio, diálogo e reformas institucionais",
        "base_eleitoral": ["Classe Média", "Empresários Moderados", "Servidores"],
        "dificuldade": "facil"
    },
    "direita": {
        "nome": "Movimento Liberal",
        "sigla": "MBL",
        "cor": "#0066CC",
        "cor_gradiente": "linear-gradient(135deg, #0066CC 0%, #003366 100%)",
        "icone": "🔵",
        "bonus": {"pop": -1, "caixa": 2000, "energia": 0, "midia": 0},
        "descricao": "Liberdade econômica, segurança e valores tradicionais",
        "base_eleitoral": ["Empresários", "Classe Média Alta", "Religiosos"],
        "dificuldade": "dificil"
    }
}

# ============================================================================
# SISTEMA DE REGIÕES BRASILEIRAS
# ============================================================================
REGIOES = {
    "Norte": {"pop": 15, "eleitores": 8.5, "cor": "#228B22"},
    "Nordeste": {"pop": 20, "eleitores": 28.5, "cor": "#FFA500"},
    "Centro-Oeste": {"pop": 12, "eleitores": 7.8, "cor": "#FFD700"},
    "Sudeste": {"pop": 35, "eleitores": 62.5, "cor": "#667eea"},
    "Sul": {"pop": 18, "eleitores": 15.2, "cor": "#DC143C"}
}

# ============================================================================
# FUNÇÕES DE LÓGICA DO JOGO
# ============================================================================

def init_game(dificuldade="normal"):
    """Inicializa todas as variáveis de estado do jogo"""
    st.session_state.dia = 1
    st.session_state.total_dias = 30
    st.session_state.popularidade = 25.0
    st.session_state.caixa = 150000.00
    st.session_state.energia = 100
    st.session_state.midia = 50  # Relação com a imprensa
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
    st.session_state.conquistas_unlocked = []
    st.session_state.combo = 0
    st.session_state.max_combo = 0
    st.session_state.dificuldade = dificuldade
    st.session_state.regioes_support = {reg: 25.0 for reg in REGIOES.keys()}
    st.session_state.evolucao_regioes = {reg: [25.0] for reg in REGIOES.keys()}
    st.session_state.escandalos_sofridos = 0
    # Ajustes por dificuldade
    if dificuldade == "facil":
        st.session_state.caixa = 200000.00
        st.session_state.popularidade = 30.0
    elif dificuldade == "dificil":
        st.session_state.caixa = 100000.00
        st.session_state.popularidade = 20.0
    # Resetar eventos usados
    st.session_state.eventos_usados = []
    # Inicializar high score se não existir
    if 'high_score_data' not in st.session_state:
        st.session_state.high_score_data = {
            'score': 0,
            'dia': 0,
            'partido': 'Nenhum',
            'data': 'N/A',
            'dificuldade': 'normal'
        }

def load_high_score():
    """Carrega o high score do session state"""
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
    """Salva novo high score se for melhor"""
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

def check_achievements():
    """Verifica e desbloqueia conquistas"""
    new_achievements = []
    
    # Primeira votação
    if st.session_state.dia >= 2 and "first_vote" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("first_vote")
        new_achievements.append("first_vote")
    
    # Popularidade
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
    
    # Caixa
    if st.session_state.caixa >= 500000 and "rich_campaign" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("rich_campaign")
        new_achievements.append("rich_campaign")
    
    # Escândalos
    if st.session_state.escandalos_sofridos >= 3 and "scandal_survivor" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("scandal_survivor")
        new_achievements.append("scandal_survivor")
    
    # Combo
    if st.session_state.combo >= 5 and st.session_state.combo > st.session_state.max_combo:
        st.session_state.max_combo = st.session_state.combo
    
    return new_achievements

def gerar_evento():
    """Seleciona um evento aleatório baseado na ideologia e contexto"""
    eventos_gerais = EVENTOS["geral"]
    eventos_ideologia = EVENTOS.get(st.session_state.partido_escolhido, [])
    
    # 70% chance de evento geral, 30% de evento específico
    if eventos_ideologia and random.random() < 0.3:
        pool_eventos = eventos_ideologia
    else:
        pool_eventos = eventos_gerais
    
    # Filtrar eventos já usados recentemente
    eventos_disponiveis = [e for e in pool_eventos if e['titulo'] not in st.session_state.eventos_usados[-8:]]
    
    if not eventos_disponiveis:
        eventos_disponiveis = pool_eventos
        st.session_state.eventos_usados = []  # Resetar se todos usados
    
    evento = random.choice(eventos_disponiveis)
    st.session_state.eventos_usados.append(evento['titulo'])
    
    # Chance de evento de crise/escândalo (15%)
    if random.random() < 0.15 and evento['tipo'] != 'crise':
        # Forçar evento de crise
        crises = [e for e in eventos_gerais if e['tipo'] == 'crise']
        if crises:
            evento = random.choice(crises)
            st.session_state.escandalos_sofridos += 1
    
    return evento

def aplicar_consequencias(opcao):
    """Aplica os efeitos da escolha com bônus do partido e dificuldade"""
    bonus = PARTIDOS[st.session_state.partido_escolhido]['bonus']
    
    # Multiplicador de dificuldade
    mult = 1.0
    if st.session_state.dificuldade == "facil":
        mult = 1.2
    elif st.session_state.dificuldade == "dificil":
        mult = 0.8
    
    # Aplicar efeitos com bônus
    st.session_state.popularidade += (opcao['efeito']['pop'] + bonus['pop']) * mult
    st.session_state.caixa += (opcao['efeito']['caixa'] + bonus['caixa']) * mult
    st.session_state.energia += (opcao['efeito']['energia'] + bonus['energia']) * mult
    st.session_state.midia += (opcao['efeito'].get('midia', 0) + bonus['midia']) * mult
    
    # Limites
    st.session_state.popularidade = max(0, min(100, st.session_state.popularidade))
    st.session_state.energia = max(0, min(100, st.session_state.energia))
    st.session_state.midia = max(0, min(100, st.session_state.midia))
    
    # Atualizar regiões baseado na decisão
    atualizar_regioes(opcao)
    
    # Combo system
    if opcao['efeito']['pop'] > 0:
        st.session_state.combo += 1
    else:
        st.session_state.combo = 0
    
    # Salvar evolução
    st.session_state.evolucao_popularidade.append(st.session_state.popularidade)
    st.session_state.evolucao_dias.append(st.session_state.dia)
    
    # Salvar pesquisa
    st.session_state.pesquisas.append({
        'dia': st.session_state.dia,
        'pop': st.session_state.popularidade,
        'midia': st.session_state.midia
    })
    
    # Histórico
    st.session_state.historico.append({
        'dia': st.session_state.dia,
        'feedback': opcao['feedback'],
        'pop': st.session_state.popularidade,
        'caixa': st.session_state.caixa,
        'energia': st.session_state.energia
    })
    
    # Verificar conquistas
    new_achievements = check_achievements()
    if new_achievements:
        st.session_state.new_achievements = new_achievements

def atualizar_regioes(opcao):
    """Atualiza apoio por região baseado na decisão"""
    # Variação aleatória + impacto da decisão
    for reg in REGIOES.keys():
        variacao = random.uniform(-2, 3)
        if opcao['efeito']['pop'] > 0:
            variacao += 1
        else:
            variacao -= 1
        
        st.session_state.regioes_support[reg] += variacao
        st.session_state.regioes_support[reg] = max(0, min(100, st.session_state.regioes_support[reg]))
        st.session_state.evolucao_regioes[reg].append(st.session_state.regioes_support[reg])

def verificar_condicoes():
    """Verifica condições de vitória/derrota"""
    # Vitória antecipada
    if st.session_state.popularidade >= 60:
        st.session_state.vitoria = True
        st.session_state.game_over = True
        return "VITÓRIA ESMAGADORA! Você atingiu 60% e venceu em 1º turno!"
    
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
    
    if st.session_state.midia <= 10:
        st.session_state.game_over = True
        return "DERROTA: Imprensa hostil destruiu sua imagem."
    
    # Fim dos 30 dias
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
    
    # Pesquisa especial no dia 15
    if st.session_state.dia == 15:
        return "📊 PESQUISA DE MEIO DE CAMPANHA DIVULGADA!"
            
    return None

def criar_grafico_evolucao():
    """Cria gráfico Plotly da evolução da popularidade"""
    fig = go.Figure()
    
    partido_cor = PARTIDOS[st.session_state.partido_escolhido]['cor']
    
    fig.add_trace(go.Scatter(
        x=st.session_state.evolucao_dias,
        y=st.session_state.evolucao_popularidade,
        mode='lines+markers',
        name='Popularidade',
        line=dict(color=partido_cor, width=4),
        marker=dict(size=10, symbol='circle')
    ))
    
    # Linhas de referência
    fig.add_hline(y=50, line_dash="dash", line_color="green", annotation_text="Vitória 1º Turno", annotation_position="right")
    fig.add_hline(y=40, line_dash="dash", line_color="orange", annotation_text="2º Turno", annotation_position="right")
    fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Zona de Perigo", annotation_position="right")
    
    fig.update_layout(
        title='📈 Evolução da Popularidade Nacional',
        xaxis_title='Dia de Campanha',
        yaxis_title='Popularidade (%)',
        yaxis_range=[0, 100],
        xaxis_range=[1, 30],
        height=400,
        template='plotly_white',
        hovermode='x unified',
        font=dict(family='Inter', size=12)
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

def criar_grafico_radar():
    """Cria gráfico radar de stats"""
    fig = go.Figure()
    
    stats = {
        'Popularidade': st.session_state.popularidade,
        'Caixa': min(st.session_state.caixa / 5000, 100),
        'Energia': st.session_state.energia,
        'Mídia': st.session_state.midia
    }
    
    fig.add_trace(go.Scatterpolar(
        r=list(stats.values()),
        theta=list(stats.keys()),
        fill='toself',
        name='Status Atual',
        line_color=PARTIDOS[st.session_state.partido_escolhido]['cor']
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        height=350,
        template='plotly_white'
    )
    
    return fig

# ============================================================================
# COMPONENTES DE UI
# ============================================================================

def render_metric_card(title, value, subtitle="", color="#667eea", icon=""):
    """Renderiza um card de métrica estilizado"""
    return f"""
    <div class="metric-card" style="background: {color};">
        <h3>{icon} {title}</h3>
        <h1>{value}</h1>
        <div class="subtitle">{subtitle}</div>
    </div>
    """

def render_event_card(evento):
    """Renderiza o card do evento atual"""
    return f"""
    <div class="event-card">
        <div class="icon">{evento['icon']}</div>
        <h2>{evento['titulo']}</h2>
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
    """

def render_achievement(ach_id, unlocked=False):
    """Renderiza card de conquista"""
    ach = ACHIEVEMENTS[ach_id]
    if unlocked:
        return f"""
        <div class="achievement-card">
            <span class="achievement-icon">{ach['icon']}</span>
            <div>
                <strong>{ach['name']}</strong><br>
                <small>{ach['desc']}</small>
            </div>
        </div>
        """
    else:
        return f"""
        <div class="achievement-card locked">
            <span class="achievement-icon">🔒</span>
            <div>
                <strong>{ach['name']}</strong><br>
                <small>{ach['desc']}</small>
            </div>
        </div>
        """

def render_news_feed():
    """Renderiza feed de notícias baseado nas ações"""
    if not st.session_state.historico:
        return ""
    
    news = []
    for item in st.session_state.historico[-5:]:
        if item['pop'] > st.session_state.popularidade - 3:
            tipo = "positive"
            emoji = "✅"
        elif item['pop'] < st.session_state.popularidade - 5:
            tipo = "urgent"
            emoji = "⚠️"
        else:
            tipo = ""
            emoji = "📰"
        
        news.append(f"""
        <div class="news-item {tipo}">
            <strong>{emoji} Dia {item['dia']}</strong>: {item['feedback']}
        </div>
        """)
    
    return "".join(news[::-1])

# ============================================================================
# TELAS DO JOGO
# ============================================================================

def mostrar_tela_inicial():
    """Tela de seleção de partido e dificuldade"""
    # Header
    st.markdown("""
    <div class="game-header">
        <h1 style="font-size: 48px; margin: 0;">🇧🇷 CANDIDATO 2026</h1>
        <p style="font-size: 18px; opacity: 0.9; margin: 10px 0 0 0;">Simulador Presidencial Brasileiro</p>
        <p style="font-size: 14px; opacity: 0.7;">Tome decisões, gerencie crises e conquiste o Planalto</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instruções
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎮 Como Jogar
        
        1. **Escolha sua ideologia** - Cada uma tem bônus e desafios únicos
        2. **Tome decisões** - 30 dias de campanha com eventos realistas
        3. **Gerencie recursos** - Popularidade, Caixa, Energia e Relação com Mídia
        4. **Conquiste regiões** - Diferentes áreas do Brasil têm perfis eleitorais
        5. **Desbloqueie conquistas** - 12 achievements para coletar
        
        ### ⚠️ Aviso Importante
        Este é um jogo **fictício** para fins educacionais e de entretenimento.
        Nenhum político, partido ou evento real foi usado. Todas as situações
        são simuladas para representar desafios genéricos de campanhas eleitorais.
        """)
        
        # Dificuldade
        st.markdown("### 🎯 Nível de Dificuldade")
        dificuldade = st.radio(
            "Escolha a dificuldade:",
            ["Fácil - Para iniciantes", "Normal - Experiência balanceada", "Difícil - Desafio máximo"],
            label_visibility="collapsed"
        )
        
        diff_map = {
            "Fácil - Para iniciantes": "facil",
            "Normal - Experiência balanceada": "normal",
            "Difícil - Desafio máximo": "dificil"
        }
        st.session_state.dificuldade_temp = diff_map[dificuldade]
    
    with col2:
        # High Score
        st.markdown("### 🏆 Recorde Atual")
        hs = load_high_score()
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h3>📊 Maior Popularidade</h3>
            <h1>{hs['score']:.1f}%</h1>
            <div class="subtitle">{hs['partido']} | {hs['dificuldade']}</div>
            <div class="subtitle">{hs['data']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Conquistas totais
        total_ach = len(ACHIEVEMENTS)
        if 'conquistas_unlocked' in st.session_state:
            unlocked = len(st.session_state.conquistas_unlocked)
        else:
            unlocked = 0
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: 20px;">
            <p>🏅 Conquistas: <strong>{unlocked}/{total_ach}</strong></p>
        </div>
        """)
    
    st.divider()
    
    # Seleção de Partido
    st.markdown("### 🎭 Escolha Sua Ideologia")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        partido = PARTIDOS['esquerda']
        st.markdown(f"""
        <div style="background: {partido['cor_gradiente']}; padding: 25px; border-radius: 15px; color: white; height: 100%;">
            <h2 style="margin: 0; font-size: 48px;">{partido['icone']}</h2>
            <h3 style="margin: 10px 0;">{partido['nome']}</h3>
            <p style="font-size: 12px; opacity: 0.9;">{partido['sigla']}</p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p style="font-size: 14px;">{partido['descricao']}</p>
            <div style="margin-top: 15px;">
                <p>💰 Caixa: <strong>+R$ 500/dia</strong></p>
                <p>📊 Popularidade: <strong>+1% por decisão</strong></p>
                <p>⚡ Energia: <strong>+2/dia</strong></p>
                <p>📰 Mídia: <strong>+1/dia</strong></p>
            </div>
            <p style="margin-top: 15px; font-size: 12px;">🎯 Dificuldade: <strong>{partido['dificuldade'].upper()}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔴 Jogar como Esquerda", key="btn_esq", use_container_width=True, type="primary"):
            st.session_state.partido_escolhido = "esquerda"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()
    
    with col2:
        partido = PARTIDOS['centro']
        st.markdown(f"""
        <div style="background: {partido['cor_gradiente']}; padding: 25px; border-radius: 15px; color: white; height: 100%;">
            <h2 style="margin: 0; font-size: 48px;">{partido['icone']}</h2>
            <h3 style="margin: 10px 0;">{partido['nome']}</h3>
            <p style="font-size: 12px; opacity: 0.9;">{partido['sigla']}</p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p style="font-size: 14px;">{partido['descricao']}</p>
            <div style="margin-top: 15px;">
                <p>💰 Caixa: <strong>+R$ 1.000/dia</strong></p>
                <p>📊 Popularidade: <strong>Neutro</strong></p>
                <p>⚡ Energia: <strong>+1/dia</strong></p>
                <p>📰 Mídia: <strong>+2/dia</strong></p>
            </div>
            <p style="margin-top: 15px; font-size: 12px;">🎯 Dificuldade: <strong>{partido['dificuldade'].upper()}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🟡 Jogar como Centro", key="btn_cen", use_container_width=True, type="primary"):
            st.session_state.partido_escolhido = "centro"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()
    
    with col3:
        partido = PARTIDOS['direita']
        st.markdown(f"""
        <div style="background: {partido['cor_gradiente']}; padding: 25px; border-radius: 15px; color: white; height: 100%;">
            <h2 style="margin: 0; font-size: 48px;">{partido['icone']}</h2>
            <h3 style="margin: 10px 0;">{partido['nome']}</h3>
            <p style="font-size: 12px; opacity: 0.9;">{partido['sigla']}</p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p style="font-size: 14px;">{partido['descricao']}</p>
            <div style="margin-top: 15px;">
                <p>💰 Caixa: <strong>+R$ 2.000/dia</strong></p>
                <p>📊 Popularidade: <strong>-1% por decisão</strong></p>
                <p>⚡ Energia: <strong>Neutro</strong></p>
                <p>📰 Mídia: <strong>Neutro</strong></p>
            </div>
            <p style="margin-top: 15px; font-size: 12px;">🎯 Dificuldade: <strong>{partido['dificuldade'].upper()}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔵 Jogar como Direita", key="btn_dir", use_container_width=True, type="primary"):
            st.session_state.partido_escolhido = "direita"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()

def mostrar_jogo():
    """Tela principal do jogo"""
    partido_info = PARTIDOS[st.session_state.partido_escolhido]
    
    # Header com informações do partido
    col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
    with col_h1:
        st.markdown(f"""
        <div style="background: {partido_info['cor_gradiente']}; padding: 20px; border-radius: 15px; color: white;">
            <h2 style="margin: 0;">{partido_info['icone']} {partido_info['nome']} ({partido_info['sigla']})</h2>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">Dificuldade: {st.session_state.dificuldade.upper()} | Dia {st.session_state.dia}/{st.session_state.total_dias}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_h2:
        if st.button("📊 Stats", use_container_width=True):
            st.session_state.show_stats = not st.session_state.get('show_stats', False)
    with col_h3:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.partido_escolhido = None
            st.rerun()
    
    # Combo counter
    if st.session_state.combo >= 3:
        st.markdown(f"""
        <div style="text-align: center;">
            <div class="combo-counter pulse">
                🔥 COMBO x{st.session_state.combo} - Bônus de Popularidade!
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats em cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(render_metric_card(
            "Popularidade",
            f"{st.session_state.popularidade:.1f}%",
            "Meta: 40%+",
            partido_info['cor_gradiente'],
            "📊"
        ), unsafe_allow_html=True)
        st.progress(st.session_state.popularidade / 100)
    
    with col2:
        cor_caixa = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)" if st.session_state.caixa > 50000 else "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)" if st.session_state.caixa > 10000 else "linear-gradient(135deg, #cb2d3e 0%, #ef473a 100%)"
        st.markdown(render_metric_card(
            "Caixa",
            f"R$ {st.session_state.caixa:,.0f}",
            "Saudável" if st.session_state.caixa > 50000 else "Atenção" if st.session_state.caixa > 10000 else "Crítico",
            cor_caixa,
            "💰"
        ), unsafe_allow_html=True)
        st.progress(min(st.session_state.caixa / 200000, 1.0))
    
    with col3:
        cor_energia = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        st.markdown(render_metric_card(
            "Energia",
            f"{st.session_state.energia}%",
            "Descanse se < 30%",
            cor_energia,
            "⚡"
        ), unsafe_allow_html=True)
        st.progress(st.session_state.energia / 100)
    
    with col4:
        cor_midia = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" if st.session_state.midia > 50 else "linear-gradient(135deg, #cb2d3e 0%, #ef473a 100%)"
        st.markdown(render_metric_card(
            "Mídia",
            f"{st.session_state.midia:.0f}",
            "Relação com imprensa",
            cor_midia,
            "📰"
        ), unsafe_allow_html=True)
        st.progress(st.session_state.midia / 100)
    
    st.divider()
    
    # Gráficos e Stats Avançados
    if st.session_state.get('show_stats', False):
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.plotly_chart(criar_grafico_evolucao(), use_container_width=True)
        with col_g2:
            st.plotly_chart(criar_grafico_regioes(), use_container_width=True)
        
        col_g3, col_g4 = st.columns(2)
        with col_g3:
            st.plotly_chart(criar_grafico_radar(), use_container_width=True)
        with col_g4:
            st.markdown("### 📰 Últimas Notícias")
            st.markdown(render_news_feed(), unsafe_allow_html=True)
        
        st.divider()
    
    # Área do evento
    if st.session_state.game_over:
        # Tela de fim de jogo
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
            
            # Salvar high score
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
        
        # Mostrar conquistas desbloqueadas
        if st.session_state.conquistas_unlocked:
            st.markdown("### 🏅 Conquistas Desbloqueadas")
            cols = st.columns(3)
            for i, ach_id in enumerate(st.session_state.conquistas_unlocked):
                with cols[i % 3]:
                    st.markdown(render_achievement(ach_id, True), unsafe_allow_html=True)
        
        # Histórico completo
        with st.expander("📜 Resumo Completo da Campanha", expanded=False):
            for i, item in enumerate(st.session_state.historico, 1):
                st.text(f"{i}. Dia {item['dia']}: {item['feedback']} (Pop: {item['pop']:.1f}%)")
        
        if st.button("🎮 Jogar Novamente", use_container_width=True, type="primary"):
            st.session_state.partido_escolhido = None
            st.rerun()
            
    else:
        # Gerar evento se necessário
        if st.session_state.evento_atual is None:
            st.session_state.evento_atual = gerar_evento()
        
        evento = st.session_state.evento_atual
        
        # Caixa do evento
        st.markdown(render_event_card(evento), unsafe_allow_html=True)
        
        st.write("### 🤔 Qual sua decisão?")
        
        # Botões de opção
        cols = st.columns(3)
        for i, opcao in enumerate(evento['opcoes']):
            with cols[i]:
                # Calcular preview de consequências
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
                    
                    # Recuperação de energia diária
                    st.session_state.energia = min(100, st.session_state.energia + 5)
                    # Bonus de caixa diário
                    st.session_state.caixa += PARTIDOS[st.session_state.partido_escolhido]['bonus']['caixa']
                    
                    msg = verificar_condicoes()
                    if msg:
                        st.session_state.msg_fim = msg
                    
                    # Mostrar conquistas novas
                    if hasattr(st.session_state, 'new_achievements') and st.session_state.new_achievements:
                        for ach_id in st.session_state.new_achievements:
                            ach = ACHIEVEMENTS[ach_id]
                            st.success(f"🏆 CONQUISTA DESBLOQUEADA: {ach['icon']} {ach['name']}!")
                        st.session_state.new_achievements = []
                    
                    st.rerun()
        
        # Feedback da última ação
        if len(st.session_state.historico) > 0:
            ultimo = st.session_state.historico[-1]
            st.info(f"💬 {ultimo['feedback']}")
        
        # Dicas contextuais
        with st.expander("💡 Dicas de Estratégia"):
            st.write("""
            - **Popularidade** acima de 50% garante vitória no 1º turno
            - **Caixa** negativo = cassação da candidatura pelo TSE
            - **Energia** zero = hospitalização e fim de campanha
            - **Mídia** abaixo de 10 = imprensa hostil destrói imagem
            - Cada partido tem bônus e penalidades diferentes
            - Equilibre gastos com ganhos de popularidade
            - Monitore apoio regional para estratégia nacional
            - Combos de decisões positivas aumentam popularidade
            """)

# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar():
    """Renderiza a sidebar com informações"""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/ballot-box-with-ball.png", width=80)
        st.title("🎛️ Painel")
        
        if 'partido_escolhido' in st.session_state and st.session_state.partido_escolhido:
            st.write(f"**Partido:** {PARTIDOS[st.session_state.partido_escolhido]['nome']}")
            st.write(f"**Dificuldade:** {st.session_state.dificuldade.upper()}")
            st.divider()
            
            # Stats rápidos
            st.write("### 📊 Status")
            st.write(f"📈 Popularidade: {st.session_state.popularidade:.1f}%")
            st.write(f"💰 Caixa: R$ {st.session_state.caixa:,.0f}")
            st.write(f"⚡ Energia: {st.session_state.energia}%")
            st.write(f"📰 Mídia: {st.session_state.midia:.0f}")
            st.divider()
            
            # Combo
            if st.session_state.combo >= 2:
                st.write(f"🔥 **Combo:** x{st.session_state.combo}")
            
            # Pesquisas recentes
            if st.session_state.pesquisas:
                st.write("### 📰 Últimas Pesquisas")
                for p in st.session_state.pesquisas[-3:]:
                    st.write(f"Dia {p['dia']}: {p['pop']:.1f}%")
            
            st.divider()
            
            # Conquistas
            st.write("### 🏅 Conquistas")
            total = len(ACHIEVEMENTS)
            unlocked = len(st.session_state.conquistas_unlocked) if 'conquistas_unlocked' in st.session_state else 0
            st.write(f"{unlocked}/{total} desbloqueadas")
            st.progress(unlocked / total)
            
            # Mostrar algumas conquistas
            if 'conquistas_unlocked' in st.session_state:
                for ach_id in st.session_state.conquistas_unlocked[:3]:
                    ach = ACHIEVEMENTS[ach_id]
                    st.write(f"{ach['icon']} {ach['name']}")
        
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
    # Inicializar session state
    if 'show_stats' not in st.session_state:
        st.session_state.show_stats = False
    
    # Render sidebar
    render_sidebar()
    
    # Tela principal
    if 'partido_escolhido' not in st.session_state or st.session_state.partido_escolhido is None:
        mostrar_tela_inicial()
    else:
        mostrar_jogo()

if __name__ == "__main__":
    main()
