import streamlit as st
import random
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="🇧🇷 Candidato 2026 - Premium",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS PREMIUM COM ANIMAÇÕES
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Cards de Métricas Premium */
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 25px 20px;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin: 8px 0;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.4);
    }
    .metric-card h3 {
        margin: 0;
        font-size: 12px;
        opacity: 0.75;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    .metric-card h1 {
        margin: 12px 0 0 0;
        font-size: 32px;
        font-weight: 700;
    }
    .metric-card .trend {
        font-size: 13px;
        margin-top: 8px;
        opacity: 0.9;
    }
    .trend.up { color: #00ff88; font-weight: 600; }
    .trend.down { color: #ff4757; font-weight: 600; }
    .trend.warn { color: #ffa500; font-weight: 600; }
    
    /* Cards de Eventos Premium */
    .event-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 35px;
        border-radius: 24px;
        border-left: 8px solid #667eea;
        box-shadow: 0 12px 40px rgba(0,0,0,0.12);
        margin: 25px 0;
        animation: slideIn 0.4s ease;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .event-card.crisis {
        border-left-color: #ff4757;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
        animation: pulse 3s infinite;
    }
    .event-card.opportunity {
        border-left-color: #00ff88;
        background: linear-gradient(135deg, #f0fff4 0%, #e0ffe8 100%);
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 12px 40px rgba(255,71,87,0.12); }
        50% { box-shadow: 0 12px 60px rgba(255,71,87,0.25); }
    }
    
    /* Botões Premium */
    .stButton>button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 14px 28px !important;
        transition: all 0.3s ease !important;
        border: 2px solid transparent !important;
        font-size: 14px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
        border-color: rgba(255,255,255,0.3) !important;
    }
    
    /* Opções de Decisão */
    .option-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 2px solid #e0e0e0;
        margin: 12px 0;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .option-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        transform: translateX(5px);
    }
    .option-card.trap {
        border-left: 4px solid #ff4757;
        background: linear-gradient(90deg, #fff5f5, white);
    }
    .option-card.smart {
        border-left: 4px solid #00ff88;
        background: linear-gradient(90deg, #f0fff4, white);
    }
    
    /* Tela de Vitória/Derrota */
    .victory-screen {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 50%, #00ff88 100%);
        padding: 50px;
        border-radius: 28px;
        color: white;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 20px 60px rgba(0,255,136,0.4);
        animation: celebrate 0.6s ease;
    }
    @keyframes celebrate {
        0% { transform: scale(0.95); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    .defeat-screen {
        background: linear-gradient(135deg, #cb2d3e 0%, #ef473a 50%, #ff4757 100%);
        padding: 50px;
        border-radius: 28px;
        color: white;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 20px 60px rgba(255,71,87,0.4);
    }
    
    /* Alertas e Notificações */
    .alert-box {
        background: linear-gradient(135deg, #ff6b81 0%, #ff4757 100%);
        color: white;
        padding: 18px 25px;
        border-radius: 16px;
        margin: 20px 0;
        font-weight: 500;
        animation: shake 0.5s ease;
        box-shadow: 0 8px 30px rgba(255,71,87,0.4);
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .success-box {
        background: linear-gradient(135deg, #00ff88 0%, #00d9a0 100%);
        color: #1a1a2e;
        padding: 18px 25px;
        border-radius: 16px;
        margin: 20px 0;
        font-weight: 500;
        box-shadow: 0 8px 30px rgba(0,255,136,0.4);
    }
    
    /* Barras de Progresso Premium */
    .progress-wrapper {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 3px;
        margin: 8px 0;
    }
    .progress-fill {
        height: 12px;
        border-radius: 8px;
        transition: width 0.5s ease;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Advisor Cards */
    .advisor-card {
        background: white;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 8px 0;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        text-align: center;
    }
    .advisor-card:hover {
        border-color: #667eea;
        transform: translateY(-3px);
    }
    .advisor-card.selected {
        border-color: #00ff88;
        background: linear-gradient(135deg, #f0fff4, #e0ffe8);
        box-shadow: 0 8px 30px rgba(0,255,136,0.3);
    }
    
    /* Achievements */
    .achievement-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin: 4px;
        animation: popIn 0.4s ease;
    }
    @keyframes popIn {
        0% { transform: scale(0); opacity: 0; }
        70% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Regional Support */
    .region-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 16px;
        background: white;
        border-radius: 12px;
        margin: 6px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .region-bar {
        flex: 1;
        height: 8px;
        background: #e0e0e0;
        border-radius: 4px;
        margin: 0 12px;
        overflow: hidden;
    }
    .region-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.4s ease;
    }
    
    /* Header Premium */
    .game-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 30px;
        border-radius: 24px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Combo Counter */
    .combo-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 10px 24px;
        border-radius: 25px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin: 15px 0;
        animation: pulse 2s infinite;
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.5);
    }
    
    /* Tooltip Style */
    .hint-text {
        background: #f8f9fa;
        padding: 12px 16px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        font-size: 14px;
        color: #555;
    }
    
    /* Scrollbar Premium */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #1a1a2e; border-radius: 4px; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #764ba2; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SISTEMA DE CONQUISTAS
# ============================================================================
ACHIEVEMENTS = {
    "first_decision": {"name": "Primeira Decisão", "desc": "Faça sua primeira escolha", "icon": "🎯", "rarity": "common"},
    "pop_rising": {"name": "Em Ascensão", "desc": "Alcance 30% de popularidade", "icon": "📈", "rarity": "common"},
    "pop_leader": {"name": "Líder nas Pesquisas", "desc": "Alcance 50% de popularidade", "icon": "👑", "rarity": "rare"},
    "pop_legend": {"name": "Lenda Política", "desc": "Alcance 70% de popularidade", "icon": "🏆", "rarity": "legendary"},
    "treasury_master": {"name": "Mestre do Tesouro", "desc": "Acumule R$ 500.000 em caixa", "icon": "💰", "rarity": "rare"},
    "scandal_survivor": {"name": "Sobrevivente", "desc": "Sobreviva a 3 escândalos", "icon": "🛡️", "rarity": "epic"},
    "combo_king": {"name": "Rei do Combo", "desc": "Alcance combo x5", "icon": "🔥", "rarity": "rare"},
    "regional_champion": {"name": "Campeão Regional", "desc": "Lidere em 5+ estados", "icon": "🗺️", "rarity": "epic"},
    "first_turn_win": {"name": "Vitória Esmagadora", "desc": "Vença no primeiro turno", "icon": "🎉", "rarity": "legendary"},
    "comeback_king": {"name": "Rei do Comeback", "desc": "Volte de <15% para vitória", "icon": "🔄", "rarity": "legendary"},
    "perfect_campaign": {"name": "Campanha Perfeita", "desc": "Termine sem escândalos", "icon": "✨", "rarity": "legendary"},
    "marathon": {"name": "Maratonista", "desc": "Complete todos os 45 dias", "icon": "🏃", "rarity": "epic"},
}

# ============================================================================
# ASSESSORES (COM CONFIABILIDADE VARIÁVEL)
# ============================================================================
ASSESSORES = {
    "estrategista": {
        "nome": "Carlos Mendes",
        "cargo": "Estrategista Chefe",
        "icone": "🎯",
        "confiabilidade": 0.85,
        "especialidade": "popularidade",
        "descricao": "Analisa pesquisas e tendências eleitorais",
        "cor": "#667eea"
    },
    "financeiro": {
        "nome": "Ana Rodrigues",
        "cargo": "Diretora Financeira",
        "icone": "💰",
        "confiabilidade": 0.92,
        "especialidade": "caixa",
        "descricao": "Especialista em orçamento e captação",
        "cor": "#00ff88"
    },
    "comunicacao": {
        "nome": "Pedro Santos",
        "cargo": "Diretor de Comunicação",
        "icone": "📰",
        "confiabilidade": 0.70,
        "especialidade": "midia",
        "descricao": "Gerencia relação com imprensa e redes",
        "cor": "#ffa500"
    },
    "politico": {
        "nome": "Dra. Helena Costa",
        "cargo": "Articuladora Política",
        "icone": "🤝",
        "confiabilidade": 0.78,
        "especialidade": "coalizao",
        "descricao": "Negocia com partidos e aliados",
        "cor": "#ff4757"
    },
    "juridico": {
        "nome": "Dr. Roberto Lima",
        "cargo": "Advogado Eleitoral",
        "icone": "⚖️",
        "confiabilidade": 0.96,
        "especialidade": "risco",
        "descricao": "Previne problemas jurídicos e escândalos",
        "cor": "#9b59b6"
    }
}

# ============================================================================
# PARTIDOS DA COALIZÃO
# ============================================================================
PARTIDOS_COALIZAO = {
    "base": {"nome": "Partido da Base", "sigla": "PDB", "cor": "#DC143C", "apoio_inicial": 82},
    "centrao": {"nome": "Centrão Unido", "sigla": "CPU", "cor": "#FFD700", "apoio_inicial": 65},
    "progressista": {"nome": "Frente Progressista", "sigla": "FPP", "cor": "#228B22", "apoio_inicial": 71},
    "liberal": {"nome": "Aliança Liberal", "sigla": "ALB", "cor": "#0066CC", "apoio_inicial": 58}
}

# ============================================================================
# ESTADOS DECISIVOS
# ============================================================================
ESTADOS_DECISIVOS = {
    "SP": {"eleitores": 22.5, "cor": "#667eea", "perfil": "urbano"},
    "MG": {"eleitores": 10.8, "cor": "#228B22", "perfil": "misto"},
    "RJ": {"eleitores": 8.9, "cor": "#FFD700", "perfil": "urbano"},
    "BA": {"eleitores": 8.2, "cor": "#FFA500", "perfil": "nordeste"},
    "RS": {"eleitores": 5.8, "cor": "#DC143C", "perfil": "sul"},
    "PR": {"eleitores": 5.7, "cor": "#228B22", "perfil": "sul"},
    "PE": {"eleitores": 4.8, "cor": "#FFA500", "perfil": "nordeste"},
    "CE": {"eleitores": 4.6, "cor": "#FFA500", "perfil": "nordeste"},
}

# ============================================================================
# BANCO DE DADOS DE EVENTOS PREMIUM (COM ARMADILHAS!)
# ============================================================================
EVENTOS = {
    "geral": [
        {
            "id": "debate_tv_premium",
            "titulo": "📺 Debate Presidencial - Transmissão Nacional",
            "desc": """
            O momento mais importante da campanha chegou. 65 milhões de brasileiros 
            estão assistindo ao vivo. Os moderadores já alertaram: perguntas difíceis 
            virão sobre economia, corrupção e propostas.
            
            <div class='hint-text'>
            💡 <strong>Dica do Estrategista:</strong> Eleitores indecisos (38% do eleitorado) 
            decidem o voto baseado em debates. Um erro pode custar 5-10 pontos.
            </div>
            """,
            "icon": "📺",
            "tipo": "debate",
            "impacto": "crítico",
            "duracao": 2,
            "armadilha": True,
            "opcoes": [
                {
                    "texto": "Atacar adversários com dados e fatos contundentes",
                    "descricao_oculta": "Parece forte, mas pode alienar eleitores moderados que buscam união.",
                    "efeito_base": {"pop": 8, "caixa": 0, "energia": -22, "midia": 6, "risco": 18},
                    "condicoes": {"pop_minima": 28},
                    "armadilha": False,
                    "dica_assessor": "Bom para mobilizar sua base, mas cuidado com o tom."
                },
                {
                    "texto": "Focar em histórias emocionais e conexão com o povo",
                    "descricao_oculta": "ARMADILHA: Parece a escolha óbvia, mas eleitores técnicos podem achar superficial.",
                    "efeito_base": {"pop": 14, "caixa": -4000, "energia": -28, "midia": 4, "risco": 12},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "⚠️ Cuidado: pode parecer populista para eleitores de alta renda."
                },
                {
                    "texto": "Postura conciliadora: 'Acima das brigas, focado no Brasil'",
                    "descricao_oculta": "Seguro para manter, mas pouco impactante para crescer nas pesquisas.",
                    "efeito_base": {"pop": 3, "caixa": 0, "energia": -18, "midia": 14, "risco": 4},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "Ideal se você já está liderando. Ruim se precisa crescer."
                },
                {
                    "texto": "Ignorar ataques e apresentar plano de governo detalhado",
                    "descricao_oculta": "Impressiona eleitores informados, mas pode parecer evasivo para massas.",
                    "efeito_base": {"pop": 5, "caixa": -2000, "energia": -25, "midia": 10, "risco": 8},
                    "condicoes": {"energia_minima": 40},
                    "armadilha": False,
                    "dica_assessor": "Excelente para eleitores com ensino superior (25% do eleitorado)."
                }
            ]
        },
        {
            "id": "escandalo_aliado",
            "titulo": "🚨 ESCÂNDALO: Aliado Envolvido em Desvio de Verbas",
            "desc": """
            A Polícia Federal divulgou operação que aponta desvio de R$ 47 milhões 
            por um importante aliado da sua coalizão. O nome dele está ligado a 
            contratos superfaturados de obras públicas.
            
            <div class='hint-text'>
            🚨 <strong>ALERTA:</strong> Sua resposta nas próximas 24h definirá 
            se você será visto como íntegro ou conivente. A imprensa está em cima.
            </div>
            """,
            "icon": "🚨",
            "tipo": "crise",
            "impacto": "crítico",
            "duracao": 3,
            "armadilha": True,
            "opcoes": [
                {
                    "texto": "Romper aliança imediatamente e condenar publicamente",
                    "descricao_oculta": "Ganha imagem de íntegro, mas pode perder apoio crucial no Congresso.",
                    "efeito_base": {"pop": 10, "caixa": -10000, "energia": -28, "midia": -3, "risco": 22, "coalizao": -18},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Jurídico: Ação correta. ⚠️ Político: Pode enfraquecer sua base."
                },
                {
                    "texto": "Aguardar conclusão da investigação antes de se posicionar",
                    "descricao_oculta": "ARMADILHA: Parece prudente, mas eleitores interpretam como omissão ou conivência.",
                    "efeito_base": {"pop": -15, "caixa": 0, "energia": -18, "midia": -18, "risco": 8, "coalizao": 8},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "⚠️ Comunicação: Silêncio é interpretado como culpa nas redes sociais."
                },
                {
                    "texto": "Defender aliado: 'Presunção de inocência até prova final'",
                    "descricao_oculta": "ARMADILHA PERIGOSA: Mantém coalizão, mas associa SUA imagem ao escândalo.",
                    "efeito_base": {"pop": -25, "caixa": 0, "energia": -25, "midia": -30, "risco": 40, "coalizao": 15},
                    "condicoes": {"coalizao_minima": 65},
                    "armadilha": True,
                    "dica_assessor": "🚨 Jurídico: Risco altíssimo. Se aliado for condenado, você cai junto."
                },
                {
                    "texto": "Anunciar CPI própria para investigar com transparência",
                    "descricao_oculta": "Mostra ação proativa, mas gasta capital político e pode backfire.",
                    "efeito_base": {"pop": 6, "caixa": -18000, "energia": -32, "midia": 10, "risco": 28, "coalizao": -12},
                    "condicoes": {"caixa_minima": 60000},
                    "armadilha": False,
                    "dica_assessor": "✅ Estratégia: Mostra liderança. ⚠️ Financeiro: Custo alto."
                }
            ]
        },
        {
            "id": "crise_economica_premium",
            "titulo": "💸 CRISE ECONÔMICA GLOBAL AFETA BRASIL",
            "desc": """
            Mercados internacionais em turbulência: dólar +18% em uma semana, 
            bolsa -12%, FMI revisa previsão de crescimento do Brasil para 0.3%.
            
            <div class='hint-text'>
            📊 <strong>Dado Crítico:</strong> 71% dos eleitores citam economia 
            como principal preocupação. Classes C/D são as mais sensíveis.
            </div>
            """,
            "icon": "💸",
            "tipo": "economia",
            "impacto": "crítico",
            "duracao": 2,
            "armadilha": True,
            "opcoes": [
                {
                    "texto": "Prometer controle rigoroso de preços e combate à especulação",
                    "descricao_oculta": "ARMADILHA: Muito popular a curto prazo, mas economistas alertam para inflação futura.",
                    "efeito_base": {"pop": 15, "caixa": -18000, "energia": -24, "midia": 4, "risco": 22},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "⚠️ Financeiro: Pode gerar inflação. ✅ Estratégico: Popular imediato."
                },
                {
                    "texto": "Defender autonomia total do Banco Central e metas fiscais",
                    "descricao_oculta": "Mercado aprova, mas pode ser impopular com eleitores de baixa renda.",
                    "efeito_base": {"pop": -8, "caixa": 12000, "energia": -18, "midia": 15, "risco": 10},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Financeiro: Estabilidade. ⚠️ Político: Impopular com base."
                },
                {
                    "texto": "Anunciar pacote emergencial de R$ 40 bilhões para proteger empregos",
                    "descricao_oculta": "Alto impacto imediato, mas drena recursos da campanha de forma crítica.",
                    "efeito_base": {"pop": 18, "caixa": -45000, "energia": -30, "midia": 12, "risco": 15},
                    "condicoes": {"caixa_minima": 100000},
                    "armadilha": False,
                    "dica_assessor": "✅ Estratégico: Popular e concreto. ⚠️ Financeiro: Custo muito alto."
                },
                {
                    "texto": "Culpar governo anterior e prometer 'mudança estrutural'",
                    "descricao_oculta": "ARMADILHA: Fácil politicamente, mas parece evasivo sem propostas concretas.",
                    "efeito_base": {"pop": 4, "caixa": 0, "energia": -14, "midia": -6, "risco": 14},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "⚠️ Comunicação: Pode parecer discurso vazio sem ações."
                }
            ]
        },
        {
            "id": "crise_saude_premium",
            "titulo": "🏥 CRISE DE SAÚDE: HOSPITAIS EM COLAPSO",
            "desc": """
            Novo surto de doença respiratória sobrecarrega sistema de saúde. 
            UTIs com 98% de ocupação, fila de vacinação com 2 meses de espera.
            
            <div class='hint-text'>
            🚑 <strong>Urgente:</strong> Imagens de pacientes em corredores 
            viralizaram. Famílias organizam protestos para amanhã.
            </div>
            """,
            "icon": "🏥",
            "tipo": "saude",
            "impacto": "alto",
            "duracao": 2,
            "armadilha": False,
            "opcoes": [
                {
                    "texto": "Visitar hospitais pessoalmente e conversar com famílias",
                    "descricao_oculta": "Humaniza imagem, mas há risco de contágio e consome energia crítica.",
                    "efeito_base": {"pop": 12, "caixa": -6000, "energia": -40, "midia": 10, "risco": 18},
                    "condicoes": {"energia_minima": 55},
                    "armadilha": False,
                    "dica_assessor": "✅ Comunicação: Imagem humanizada. ⚠️ Energia: Custo muito alto."
                },
                {
                    "texto": "Anunciar verba emergencial de R$ 8 bilhões para saúde",
                    "descricao_oculta": "Ação concreta e mensurável. Caro, mas eficaz e transparente.",
                    "efeito_base": {"pop": 10, "caixa": -32000, "energia": -18, "midia": 14, "risco": 6},
                    "condicoes": {"caixa_minima": 70000},
                    "armadilha": False,
                    "dica_assessor": "✅ Financeiro: Investimento visível. ✅ Estratégico: Ação concreta."
                },
                {
                    "texto": "Convocar coletiva com cientistas e apresentar plano técnico",
                    "descricao_oculta": "Mostra competência técnica, mas pode parecer frio em momento emocional.",
                    "efeito_base": {"pop": 6, "caixa": -4000, "energia": -24, "midia": 18, "risco": 4},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Mídia: Transparência técnica. ⚠️ Emoção: Pode parecer distante."
                },
                {
                    "texto": "Culpar gestão anterior e prometer investigação de responsabilidades",
                    "descricao_oculta": "ARMADILHA: Político mas insensível com vítimas. Alto risco de backfire.",
                    "efeito_base": {"pop": -10, "caixa": 0, "energia": -12, "midia": -14, "risco": 24},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "🚨 Comunicação: Pode parecer que está se aproveitando da tragédia."
                }
            ]
        },
        {
            "id": "amazonia_internacional",
            "titulo": "🌳 AMAZÔNIA: PRESSÃO INTERNACIONAL CRÍTICA",
            "desc": """
            Imagens de satélite da NASA mostram +52% nas queimadas. 
            UE ameaça bloquear acordo comercial. Investidores reavaliam Brasil.
            
            <div class='hint-text'>
            🌍 <strong>Impacto Global:</strong> Decisão afeta imagem internacional, 
            investimentos e relação com ruralistas da base.
            </div>
            """,
            "icon": "🌳",
            "tipo": "ambiente",
            "impacto": "alto",
            "duracao": 1,
            "armadilha": True,
            "opcoes": [
                {
                    "texto": "Enviar tropas e IBAMA para fiscalização imediata",
                    "descricao_oculta": "Ação firme agrada ambientalistas, mas irrita ruralistas da coalizão.",
                    "efeito_base": {"pop": 9, "caixa": -24000, "energia": -28, "midia": 15, "risco": 18, "coalizao": -10},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Mídia: Imagem internacional. ⚠️ Coalizão: Ruralistas podem abandonar."
                },
                {
                    "texto": "Negociar com governadores plano de desenvolvimento sustentável",
                    "descricao_oculta": "Solução política equilibrada, mas ação parece lenta para urgência.",
                    "efeito_base": {"pop": 4, "caixa": -10000, "energia": -24, "midia": 7, "risco": 10, "coalizao": 8},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Político: Mantém aliados. ⚠️ Mídia: Pode parecer inação."
                },
                {
                    "texto": "Propor fundo internacional de US$ 3 bilhões para preservação",
                    "descricao_oculta": "ARMADILHA: Solução criativa, mas depende de aprovação externa incerta.",
                    "efeito_base": {"pop": 7, "caixa": 18000, "energia": -24, "midia": 18, "risco": 14},
                    "condicoes": {"midia_minima": 55},
                    "armadilha": True,
                    "dica_assessor": "⚠️ Estratégico: Se aprovado, ótimo. Se não, parece promessa vazia."
                },
                {
                    "texto": "Priorizar desenvolvimento econômico da região com salvaguardas",
                    "descricao_oculta": "ARMADILHA: Discurso equilibrado, mas vago. Pode não satisfazer nenhum lado.",
                    "efeito_base": {"pop": 1, "caixa": -6000, "energia": -18, "midia": 2, "risco": 16},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "⚠️ Comunicação: Pode ser interpretado como 'ficar em cima do muro'."
                }
            ]
        },
        {
            "id": "pesquisa_vazada_premium",
            "titulo": "📊 PESQUISA INTERNA VAZA: NÚMEROS PREOCUPANTES",
            "desc": """
            Pesquisa encomendada pela campanha vazou para a imprensa. 
            Você está 9 pontos atrás do principal adversário em estados decisivos.
            
            <div class='hint-text'>
            ⚠️ <strong>Risco:</strong> Moral da equipe em queda, doadores hesitando, 
            imprensa especulando sobre troca de candidato.
            </div>
            """,
            "icon": "📊",
            "tipo": "crise",
            "impacto": "alto",
            "duracao": 2,
            "armadilha": True,
            "opcoes": [
                {
                    "texto": "Confirmar autenticidade e anunciar reestruturação da campanha",
                    "descricao_oculta": "Honestidade pode recuperar confiança, mas admite fraqueza publicamente.",
                    "efeito_base": {"pop": 4, "caixa": -12000, "energia": -24, "midia": 10, "risco": 14},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Comunicação: Transparência. ⚠️ Estratégico: Admite vulnerabilidade."
                },
                {
                    "texto": "Negar autenticidade e processar responsável pelo vazamento",
                    "descricao_oculta": "ARMADILHA PERIGOSA: Contém dano imediato, mas se descobrirem a verdade, crise explode.",
                    "efeito_base": {"pop": -2, "caixa": -10000, "energia": -18, "midia": -8, "risco": 32},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "🚨 Jurídico: Se mentira for descoberta, dano irreparável."
                },
                {
                    "texto": "Ignorar vazamento e focar em eventos positivos para mudar narrativa",
                    "descricao_oculta": "Espera poeira baixar. Funciona se houver bons resultados em seguida.",
                    "efeito_base": {"pop": -4, "caixa": 0, "energia": -12, "midia": -10, "risco": 18},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "⚠️ Estratégico: Passivo. Pode funcionar ou piorar a situação."
                },
                {
                    "texto": "Divulgar contra-pesquisa mostrando cenários favoráveis",
                    "descricao_oculta": "Contra-ataque informativo. Pode parecer manipulação se exagerado.",
                    "efeito_base": {"pop": 6, "caixa": -15000, "energia": -22, "midia": 6, "risco": 20},
                    "condicoes": {"caixa_minima": 50000},
                    "armadilha": False,
                    "dica_assessor": "✅ Estratégico: Muda narrativa. ⚠️ Mídia: Pode parecer manipulação."
                }
            ]
        },
        {
            "id": "alianca_premium",
            "titulo": "🤝 PROPOSTA DE ALIANÇA DECISIVA",
            "desc": """
            Partido com 72 deputados e 9 governadores oferece apoio formal. 
            Em troca: 6 ministérios, R$ 250 milhões em emendas, e veto a 3 projetos.
            
            <div class='hint-text'>
            📈 <strong>Análise:</strong> Esta aliança pode adicionar 10-14% de votos, 
            mas custa recursos e pode irritar base ideológica.
            </div>
            """,
            "icon": "🤝",
            "tipo": "politica",
            "impacto": "alto",
            "duracao": 1,
            "armadilha": True,
            "opcoes": [
                {
                    "texto": "Aceitar todas as exigências e fechar aliança imediatamente",
                    "descricao_oculta": "Apoio político imediato, mas esvazia caixa e irrita base ideológica.",
                    "efeito_base": {"pop": -6, "caixa": 30000, "energia": -18, "midia": -10, "risco": 24, "coalizao": 18},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Político: Base parlamentar fortalecida. ⚠️ Base: Pode sentir traição."
                },
                {
                    "texto": "Negociar: 4 ministérios e R$ 120 milhões",
                    "descricao_oculta": "Meio-termo arriscado. Podem aceitar ou recusar e ficar inimigos.",
                    "efeito_base": {"pop": 3, "caixa": 15000, "energia": -24, "midia": 4, "risco": 18, "coalizao": 10},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Estratégico: Equilíbrio. ⚠️ Risco: Podem recusar e fechar com adversário."
                },
                {
                    "texto": "Recusar mantendo coerência programática",
                    "descricao_oculta": "ARMADILHA: Mantém imagem limpa, mas pode perder apoio crucial para vencer.",
                    "efeito_base": {"pop": 10, "caixa": 0, "energia": 6, "midia": 15, "risco": 6, "coalizao": -14},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "✅ Comunicação: Imagem de integridade. ⚠️ Estratégico: Pode custar eleição."
                },
                {
                    "texto": "Pedir tempo para consultar base do partido e militância",
                    "descricao_oculta": "Adia decisão mas pode parecer indeciso. Eles podem fechar com adversário.",
                    "efeito_base": {"pop": -1, "caixa": 0, "energia": -10, "midia": -4, "risco": 22, "coalizao": -6},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "⚠️ Estratégico: Perde timing. Pode perder a oportunidade."
                }
            ]
        },
        {
            "id": "horario_eleitoral_premium",
            "titulo": "🎬 HORÁRIO ELEITORAL: SUA ÚLTIMA CHANCE",
            "desc": """
            Último bloco do horário eleitoral gratuito. 5 minutos no rádio e TV 
            para alcançar 85 milhões de eleitores. Produção de qualidade: R$ 12.000.
            
            <div class='hint-text'>
            📺 <strong>Audiência:</strong> 85M espectadores | 35% decidem voto baseado nisso
            </div>
            """,
            "icon": "🎬",
            "tipo": "midia",
            "impacto": "alto",
            "duracao": 1,
            "armadilha": False,
            "opcoes": [
                {
                    "texto": "Propostas detalhadas com dados, especialistas e metas",
                    "descricao_oculta": "Atrai eleitores informados (25%), mas pode ser técnico demais para massas.",
                    "efeito_base": {"pop": 7, "caixa": -14000, "energia": -24, "midia": 12, "risco": 6},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Mídia: Credibilidade técnica. ⚠️ Alcance: Pode não engajar massas."
                },
                {
                    "texto": "Emoção e esperança com depoimentos reais de brasileiros",
                    "descricao_oculta": "Conexão emocional forte. Pode parecer populista para críticos.",
                    "efeito_base": {"pop": 12, "caixa": -14000, "energia": -20, "midia": 7, "risco": 10},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Estratégico: Engaja emocionalmente. ⚠️ Mídia: Críticos podem atacar."
                },
                {
                    "texto": "Ataques diretos aos adversários com comparações de gestão",
                    "descricao_oculta": "Mobiliza base fiel, mas pode afastar eleitores indecisos que buscam união.",
                    "efeito_base": {"pop": 9, "caixa": -14000, "energia": -18, "midia": -6, "risco": 18},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Base: Mobiliza fiéis. ⚠️ Indecisos: Pode afastar moderados."
                },
                {
                    "texto": "Foco em realizações passadas e experiência de gestão",
                    "descricao_oculta": "Bom se tiver histórico positivo. Ruim se estiver sendo avaliado por promessas.",
                    "efeito_base": {"pop": 6, "caixa": -14000, "energia": -15, "midia": 6, "risco": 12},
                    "condicoes": {"pop_minima": 32},
                    "armadilha": False,
                    "dica_assessor": "✅ Estratégico: Bom se já tem imagem positiva. ⚠️ Risco: Pode parecer arrogante."
                }
            ]
        },
        {
            "id": "greve_geral_premium",
            "titulo": "👊 GREVE GERAL: CENTRAIS SINDICAIS COBRAM POSIÇÃO",
            "desc": """
            Centrais sindicais convocam greve geral para próxima semana. 
            28 milhões de trabalhadores devem parar. Eles pedem seu apoio público.
            
            <div class='hint-text'>
            ⚖️ <strong>Dilema:</strong> Apoiar ganha trabalhadores, afasta empresários. 
            Neutralidade irrita sindicatos. Criticar pode gerar campanha contra você.
            </div>
            """,
            "icon": "👊",
            "tipo": "trabalho",
            "impacto": "alto",
            "duracao": 2,
            "armadilha": True,
            "opcoes": [
                {
                    "texto": "Apoiar publicamente a greve e participar de ato sindical",
                    "descricao_oculta": "Fortalece base trabalhista, mas afasta empresários e classe média.",
                    "efeito_base": {"pop": 14, "caixa": -10000, "energia": -35, "midia": -10, "risco": 20},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Base: Trabalhadores mobilizados. ⚠️ Caixa: Empresários podem cortar doações."
                },
                {
                    "texto": "Chamar governo e sindicatos para negociação imediata",
                    "descricao_oculta": "Posição de mediador. Pode agradar moderados mas irrita extremos.",
                    "efeito_base": {"pop": 5, "caixa": -4000, "energia": -28, "midia": 10, "risco": 12},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Comunicação: Imagem de pacificador. ⚠️ Ambos lados: Podem achar fraco."
                },
                {
                    "texto": "Manter neutralidade e focar em propostas de longo prazo",
                    "descricao_oculta": "ARMADILHA: Seguro, mas pode parecer omisso em momento crucial para trabalhadores.",
                    "efeito_base": {"pop": -8, "caixa": 0, "energia": -12, "midia": 0, "risco": 14},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "⚠️ Estratégico: Pode perder apoio de base trabalhista crucial."
                },
                {
                    "texto": "Criticar greve e defender diálogo sem paralisação",
                    "descricao_oculta": "ARMADILHA PERIGOSA: Agrada empresários, mas sindicatos podem fazer campanha ativa contra você.",
                    "efeito_base": {"pop": -12, "caixa": 12000, "energia": -18, "midia": 6, "risco": 24},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "🚨 Político: Sindicatos podem mobilizar 28M de votos CONTRA você."
                }
            ]
        },
        {
            "id": "seguranca_premium",
            "titulo": "🔫 ONDA DE VIOLÊNCIA: POPULAÇÃO EXIGE AÇÕES URGENTES",
            "desc": """
            Série de assaltos violentos e homicídios choca o país. 
            Famílias de vítimas protestam. Oposição cobra posicionamento.
            
            <div class='hint-text'>
            📈 <strong>Pesquisa:</strong> 76% citam segurança como prioridade #1. 
            Medidas duras são populares, mas podem violar direitos humanos.
            </div>
            """,
            "icon": "🔫",
            "tipo": "seguranca",
            "impacto": "alto",
            "duracao": 2,
            "armadilha": False,
            "opcoes": [
                {
                    "texto": "Anunciar investimento massivo em policiamento ostensivo",
                    "descricao_oculta": "Muito popular, mas caro. Resultados levam tempo para aparecer.",
                    "efeito_base": {"pop": 12, "caixa": -35000, "energia": -24, "midia": 10, "risco": 10},
                    "condicoes": {"caixa_minima": 80000},
                    "armadilha": False,
                    "dica_assessor": "✅ Estratégico: Popular e concreto. ⚠️ Financeiro: Custo muito alto."
                },
                {
                    "texto": "Propor intervenção federal em estados com crise de segurança",
                    "descricao_oculta": "Medida extrema. Popular, mas questionada constitucionalmente por especialistas.",
                    "efeito_base": {"pop": 10, "caixa": -40000, "energia": -35, "midia": 14, "risco": 26},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Popular: Medida forte. ⚠️ Jurídico: Pode ser contestada no STF."
                },
                {
                    "texto": "Focar em prevenção social e inteligência policial",
                    "descricao_oculta": "Abordagem técnica e de longo prazo. Menos popular, mas sustentável.",
                    "efeito_base": {"pop": 5, "caixa": -24000, "energia": -28, "midia": 12, "risco": 6},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Estratégico: Solução sustentável. ⚠️ Popular: Resultados demoram."
                },
                {
                    "texto": "Culpar governo anterior e prometer 'mão firme'",
                    "descricao_oculta": "ARMADILHA: Fácil politicamente, mas pode parecer evasivo sem ações concretas.",
                    "efeito_base": {"pop": 6, "caixa": 0, "energia": -14, "midia": -6, "risco": 18},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "⚠️ Comunicação: Pode parecer discurso vazio sem ações."
                }
            ]
        },
        {
            "id": "fake_news_premium",
            "titulo": "📱 FAKE NEWS VIRALIZA: DEEPFAKE SEU CIRCULA NO WHATSAPP",
            "desc": """
            Vídeo manipulado com deepfake seu está viralizando. 
            6.2 milhões de pessoas já viram antes do desmentido. 
            O vídeo mostra você dizendo coisas que nunca disse.
            
            <div class='hint-text'>
            ⚡ <strong>Urgente:</strong> Cada hora aumenta o dano exponencialmente. 
            Desmentir dá mais visibilidade. Ignorar permite que se espalhe.
            </div>
            """,
            "icon": "📱",
            "tipo": "midia",
            "impacto": "alto",
            "duracao": 2,
            "armadilha": True,
            "opcoes": [
                {
                    "texto": "Processar criadores e exigir remoção imediata via justiça",
                    "descricao_oculta": "Ação jurídica mostra seriedade, mas processo é lento e fake news continua circulando.",
                    "efeito_base": {"pop": 4, "caixa": -18000, "energia": -24, "midia": 10, "risco": 12},
                    "condicoes": {"caixa_minima": 50000},
                    "armadilha": False,
                    "dica_assessor": "✅ Jurídico: Ação correta. ⚠️ Tempo: Fake news continua enquanto processo anda."
                },
                {
                    "texto": "Desmentir em rede nacional com provas técnicas do deepfake",
                    "descricao_oculta": "Resposta rápida e transparente. Caro, mas eficaz para conter dano.",
                    "efeito_base": {"pop": 8, "caixa": -12000, "energia": -28, "midia": 15, "risco": 6},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Comunicação: Resposta rápida. ✅ Mídia: Transparência técnica."
                },
                {
                    "texto": "Pedir ajuda oficial às plataformas digitais para remover conteúdo",
                    "descricao_oculta": "Solução técnica, mas plataformas podem demorar e burocracia atrasa ação.",
                    "efeito_base": {"pop": 3, "caixa": -6000, "energia": -18, "midia": 8, "risco": 14},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Técnico: Caminho correto. ⚠️ Tempo: Pode ser lento demais."
                },
                {
                    "texto": "Ignorar e não dar mais visibilidade ao assunto (stratégie du silence)",
                    "descricao_oculta": "ARMADILHA PERIGOSA: Pode funcionar às vezes, mas fake news pode definir narrativa.",
                    "efeito_base": {"pop": -15, "caixa": 0, "energia": -10, "midia": -18, "risco": 30},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "🚨 Comunicação: Risco altíssimo. Fake news pode definir percepção pública."
                }
            ]
        },
    ],
    "esquerda": [
        {
            "id": "nacionalizacao_premium",
            "titulo": "🏛️ RESERVA ESTRATÉGICA: MINERAIS RAROS",
            "desc": """
            Geólogos descobriram uma das maiores reservas de minerais raros do mundo 
            em território nacional. Empresas estrangeiras já fazem ofertas bilionárias.
            
            <div class='hint-text'>
            ⚖️ <strong>Dilema Ideológico:</strong> Esta decisão define sua identidade. 
            Base progressista espera soberania. Mercado espera abertura.
            </div>
            """,
            "icon": "🏛️",
            "tipo": "economia",
            "impacto": "crítico",
            "duracao": 2,
            "armadilha": True,
            "opcoes": [
                {
                    "texto": "Defender monopólio estatal total da exploração",
                    "descricao_oculta": "Base progressista apoia fortemente, mas mercado reage negativamente com fuga de investimentos.",
                    "efeito_base": {"pop": 18, "caixa": -18000, "energia": -30, "midia": 10, "risco": 22},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Base: Soberania nacional. ⚠️ Mercado: Pode afastar investimentos."
                },
                {
                    "texto": "Parceria com maioria estatal (51%) e privada (49%)",
                    "descricao_oculta": "ARMADILHA: Meio-termo que pode não satisfazer base purista nem mercado plenamente.",
                    "efeito_base": {"pop": 7, "caixa": 24000, "energia": -24, "midia": 6, "risco": 14},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "⚠️ Base: Pode achar traição. ⚠️ Mercado: Pode achar insuficiente."
                },
                {
                    "texto": "Leilão total para iniciativa privada com royalties",
                    "descricao_oculta": "ARMADILHA PERIGOSA: Mercado celebra, mas base progressista considera traição ideológica.",
                    "efeito_base": {"pop": -24, "caixa": 48000, "energia": -18, "midia": -18, "risco": 35},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "🚨 Base: Pode abandonar campanha. ⚠️ Caixa: Ganho financeiro imediato."
                }
            ]
        }
    ],
    "centro": [
        {
            "id": "reforma_politica_premium",
            "titulo": "⚖️ REFORMA DO SISTEMA ELEITORAL EM VOTAÇÃO",
            "desc": """
            Congresso está votando mudança no sistema eleitoral. 
            Sua posição pode definir o futuro da política brasileira por décadas.
            
            <div class='hint-text'>
            🗳️ <strong>Impacto:</strong> Todos os lados cobram posicionamento. 
            Decisão define se você é reformador ou conservador.
            </div>
            """,
            "icon": "⚖️",
            "tipo": "politica",
            "impacto": "alto",
            "duracao": 2,
            "armadilha": False,
            "opcoes": [
                {
                    "texto": "Apoiar reforma completa e imediata do sistema",
                    "descricao_oculta": "Imagem de reformador, mas cria inimigos no establishment político.",
                    "efeito_base": {"pop": 10, "caixa": -10000, "energia": -28, "midia": 15, "risco": 24},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Mídia: Imagem de mudança. ⚠️ Político: Cria oposição no Congresso."
                },
                {
                    "texto": "Propor reforma gradual em 4 anos com amplo debate",
                    "descricao_oculta": "Prudência elogiada por analistas, mas pode parecer falta de coragem para reformistas.",
                    "efeito_base": {"pop": 5, "caixa": -4000, "energia": -22, "midia": 8, "risco": 12},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Estratégico: Equilíbrio. ⚠️ Reformistas: Pode achar lento demais."
                },
                {
                    "texto": "Manter sistema atual com ajustes menores",
                    "descricao_oculta": "ARMADILHA: Seguro para aliados, mas perde imagem de agente de mudança.",
                    "efeito_base": {"pop": -6, "caixa": 6000, "energia": -12, "midia": -10, "risco": 10},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "⚠️ Comunicação: Pode parecer conservador demais para eleitor de mudança."
                }
            ]
        }
    ],
    "direita": [
        {
            "id": "privatizacoes_premium",
            "titulo": "💼 CARTEIRA DE PRIVATIZAÇÕES PRONTA",
            "desc": """
            Equipe econômica preparou lista de 18 estatais para privatização. 
            Estimativa: R$ 220 bilhões em arrecadação. Sindicatos já anunciaram oposição.
            
            <div class='hint-text'>
            💰 <strong>Impacto:</strong> Mercado celebra, sindicatos opõem. 
            Decisão define se você é liberal ou pragmático.
            </div>
            """,
            "icon": "💼",
            "tipo": "economia",
            "impacto": "crítico",
            "duracao": 2,
            "armadilha": True,
            "opcoes": [
                {
                    "texto": "Acelerar todas as privatizações imediatamente",
                    "descricao_oculta": "Mercado e investidores celebram, mas sindicatos fazem oposição ferrenha e podem mobilizar votos contra.",
                    "efeito_base": {"pop": 12, "caixa": 58000, "energia": -35, "midia": 10, "risco": 28},
                    "condicoes": {},
                    "armadilha": False,
                    "dica_assessor": "✅ Mercado: Reação muito positiva. ⚠️ Sindicatos: Oposição ativa."
                },
                {
                    "texto": "Privatizar apenas estatais deficitárias",
                    "descricao_oculta": "ARMADILHA: Seletivo. Menos impacto financeiro, mas também menos oposição. Pode parecer tímido.",
                    "efeito_base": {"pop": 6, "caixa": 24000, "energia": -24, "midia": 6, "risco": 18},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "⚠️ Mercado: Pode achar insuficiente. ⚠️ Estratégico: Meio-termo arriscado."
                },
                {
                    "texto": "Congelar privatizações até após eleição",
                    "descricao_oculta": "ARMADILHA PERIGOSA: Adia polêmica, mas base econômica fica frustrada e pode cortar apoio.",
                    "efeito_base": {"pop": -10, "caixa": 0, "energia": -12, "midia": -12, "risco": 22},
                    "condicoes": {},
                    "armadilha": True,
                    "dica_assessor": "🚨 Base econômica: Pode sentir traição. ⚠️ Estratégico: Perde momentum reformista."
                }
            ]
        }
    ]
}

# ============================================================================
# INICIALIZAÇÃO COMPLETA DO JOGO
# ============================================================================
def init_game(dificuldade="normal"):
    """Inicializa TODAS as variáveis do jogo em um único lugar"""
    
    # Stats principais
    st.session_state.dia = 1
    st.session_state.total_dias = 45
    st.session_state.popularidade = 22.0
    st.session_state.caixa = 120000.00
    st.session_state.energia = 80
    st.session_state.midia = 45
    st.session_state.risco_escandalo = 12
    
    # Estado do jogo
    st.session_state.game_over = False
    st.session_state.vitoria = False
    st.session_state.msg_fim = ""
    
    # Dados do jogo
    st.session_state.evento_atual = None
    st.session_state.historico = []
    st.session_state.evolucao_pop = [22.0]
    st.session_state.evolucao_dias = [1]
    st.session_state.eventos_usados = []
    
    # Sistema regional
    st.session_state.estados_support = {estado: 20.0 + random.uniform(-5, 5) for estado in ESTADOS_DECISIVOS.keys()}
    
    # Coalizão
    st.session_state.coalizao_apoio = {partido: dados["apoio_inicial"] for partido, dados in PARTIDOS_COALIZAO.items()}
    
    # Conquistas e progressão
    st.session_state.conquistas_unlocked = []
    st.session_state.new_achievements = []
    st.session_state.combo = 0
    st.session_state.max_combo = 0
    st.session_state.total_escandalos = 0
    
    # Configurações
    st.session_state.partido = st.session_state.get('partido', 'centro')
    st.session_state.dificuldade = dificuldade
    st.session_state.assessor_selecionado = "estrategista"
    
    # UI
    st.session_state.mostrar_grafico = False
    st.session_state.mostrar_estados = False
    st.session_state.mostrar_coalizao = False
    
    # Ajustes por dificuldade
    if dificuldade == "Fácil":
        st.session_state.caixa = 180000.00
        st.session_state.popularidade = 28.0
        st.session_state.energia = 90
        st.session_state.risco_escandalo = 8
    elif dificuldade == "Difícil":
        st.session_state.caixa = 80000.00
        st.session_state.popularidade = 18.0
        st.session_state.energia = 70
        st.session_state.risco_escandalo = 20
    elif dificuldade == "HARDCORE":
        st.session_state.caixa = 60000.00
        st.session_state.popularidade = 15.0
        st.session_state.energia = 60
        st.session_state.risco_escandalo = 30
        st.session_state.total_dias = 40

def load_high_score():
    """Carrega o high score do jogador"""
    if 'high_score_data' not in st.session_state:
        st.session_state.high_score_data = {
            'score': 0,
            'dia': 0,
            'partido': 'Nenhum',
            'data': 'N/A',
            'dificuldade': 'Normal'
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

# ============================================================================
# LÓGICA AVANÇADA DO JOGO
# ============================================================================

def get_assessor_advice(evento, opcao_index):
    """Gera conselho do assessor com margem de erro baseada na confiabilidade"""
    assessor = ASSESSORES[st.session_state.assessor_selecionado]
    opcao = evento['opcoes'][opcao_index]
    
    # Chance do assessor dar conselho correto baseado na confiabilidade
    if random.random() < assessor['confiabilidade']:
        # Conselho correto
        if assessor['especialidade'] == 'popularidade':
            if opcao['efeito_base']['pop'] > 6:
                return f"✅ {assessor['nome']}: 'Esta opção pode aumentar significativamente sua popularidade.'"
            elif opcao['efeito_base']['pop'] < -6:
                return f"⚠️ {assessor['nome']}: 'Cuidado, isso pode prejudicar suas pesquisas.'"
            else:
                return f"➡️ {assessor['nome']}: 'Impacto neutro na popularidade.'"
        
        elif assessor['especialidade'] == 'caixa':
            if opcao['efeito_base']['caixa'] > 8000:
                return f"✅ {assessor['nome']}: 'Esta opção melhora nossa situação financeira.'"
            elif opcao['efeito_base']['caixa'] < -15000:
                return f"⚠️ {assessor['nome']}: 'Isso vai drenar nossos recursos rapidamente.'"
            else:
                return f"➡️ {assessor['nome']}: 'Impacto financeiro moderado.'"
        
        elif assessor['especialidade'] == 'risco':
            risco = opcao['efeito_base'].get('risco', 0)
            if risco > 22:
                return f"🚨 {assessor['nome']}: 'ALTO RISCO JURÍDICO detectado nesta opção.'"
            elif risco > 12:
                return f"⚠️ {assessor['nome']}: 'Risco moderado. Proceda com cautela.'"
            else:
                return f"✅ {assessor['nome']}: 'Risco jurídico aceitável.'"
        
        else:
            # Conselhos genéricos baseados no efeito
            if opcao['efeito_base']['pop'] > 5:
                return f"✅ {assessor['nome']}: 'Esta parece ser uma boa opção estrategicamente.'"
            elif opcao['efeito_base']['pop'] < -5:
                return f"⚠️ {assessor['nome']}: 'Considere alternativas menos arriscadas.'"
            else:
                return f"➡️ {assessor['nome']}: 'Opção equilibrada.'"
    else:
        # Conselho ERRADO (assessor não é 100% confiável!)
        if opcao['efeito_base']['pop'] > 5:
            return f"⚠️ {assessor['nome']}: 'Não recomendo esta opção neste momento.'"
        elif opcao['efeito_base']['pop'] < -5:
            return f"✅ {assessor['nome']}: 'Esta opção pode funcionar bem.'"
        else:
            return f"➡️ {assessor['nome']}: 'Qualquer escolha serve.'"

def check_condicoes_opcao(opcao):
    """Verifica se as condições para a opção são atendidas"""
    condicoes = opcao.get('condicoes', {})
    
    if 'pop_minima' in condicoes and st.session_state.popularidade < condicoes['pop_minima']:
        return False, f"Requer {condicoes['pop_minima']}% de popularidade"
    
    if 'caixa_minima' in condicoes and st.session_state.caixa < condicoes['caixa_minima']:
        return False, f"Requer R$ {condicoes['caixa_minima']:,} em caixa"
    
    if 'energia_minima' in condicoes and st.session_state.energia < condicoes['energia_minima']:
        return False, f"Requer {condicoes['energia_minima']}% de energia"
    
    if 'midia_minima' in condicoes and st.session_state.midia < condicoes['midia_minima']:
        return False, f"Requer {condicoes['midia_minima']} de relação com mídia"
    
    if 'coalizao_minima' in condicoes:
        media = sum(st.session_state.coalizao_apoio.values()) / len(st.session_state.coalizao_apoio)
        if media < condicoes['coalizao_minima']:
            return False, f"Requer apoio médio da coalizão"
    
    return True, ""

def aplicar_consequencias(opcao):
    """Aplica consequências com variabilidade e imprevisibilidade"""
    
    # Bônus do partido escolhido
    bonus = {"pop": 0, "caixa": 0, "energia": 0, "midia": 0}
    if st.session_state.partido == "esquerda":
        bonus = {"pop": 1.2, "caixa": -600, "energia": 2.5, "midia": 1.0}
    elif st.session_state.partido == "centro":
        bonus = {"pop": 0, "caixa": 1200, "energia": 1.5, "midia": 2.0}
    elif st.session_state.partido == "direita":
        bonus = {"pop": -0.8, "caixa": 2200, "energia": 0, "midia": 0}
    
    # Multiplicador de dificuldade
    mult = 1.0
    if st.session_state.dificuldade == "Fácil":
        mult = 1.15
    elif st.session_state.dificuldade == "Difícil":
        mult = 0.82
    elif st.session_state.dificuldade == "HARDCORE":
        mult = 0.68
    
    # Variabilidade aleatória (±25%) para imprevisibilidade
    variabilidade = random.uniform(0.75, 1.25)
    
    # Aplicar efeitos com todos os modificadores
    efeito_pop = (opcao['efeito_base']['pop'] + bonus['pop']) * mult * variabilidade
    efeito_caixa = (opcao['efeito_base']['caixa'] + bonus['caixa']) * mult * variabilidade
    efeito_energia = (opcao['efeito_base']['energia'] + bonus['energia']) * mult * variabilidade
    efeito_midia = (opcao['efeito_base'].get('midia', 0) + bonus['midia']) * mult * variabilidade
    efeito_risco = opcao['efeito_base'].get('risco', 0) * mult
    efeito_coalizao = opcao['efeito_base'].get('coalizao', 0) * mult
    
    # Atualizar stats
    st.session_state.popularidade += efeito_pop
    st.session_state.caixa += efeito_caixa
    st.session_state.energia += efeito_energia
    st.session_state.midia += efeito_midia
    st.session_state.risco_escandalo += efeito_risco
    
    # Atualizar coalizão
    if efeito_coalizao != 0:
        for partido in st.session_state.coalizao_apoio:
            st.session_state.coalizao_apoio[partido] += efeito_coalizao * random.uniform(0.7, 1.3)
            st.session_state.coalizao_apoio[partido] = max(0, min(100, st.session_state.coalizao_apoio[partido]))
    
    # Atualizar estados
    for estado in st.session_state.estados_support:
        variacao = random.uniform(-4, 5)
        if efeito_pop > 0:
            variacao += 1.5
        st.session_state.estados_support[estado] += variacao
        st.session_state.estados_support[estado] = max(0, min(100, st.session_state.estados_support[estado]))
    
    # Limites
    st.session_state.popularidade = max(0, min(100, st.session_state.popularidade))
    st.session_state.energia = max(0, min(100, st.session_state.energia))
    st.session_state.midia = max(0, min(100, st.session_state.midia))
    st.session_state.risco_escandalo = max(0, min(100, st.session_state.risco_escandalo))
    
    # Combo system
    if efeito_pop > 4:
        st.session_state.combo += 1
        if st.session_state.combo > st.session_state.max_combo:
            st.session_state.max_combo = st.session_state.combo
    else:
        st.session_state.combo = 0
    
    # Registrar evolução
    st.session_state.evolucao_pop.append(st.session_state.popularidade)
    st.session_state.evolucao_dias.append(st.session_state.dia)
    
    # Registrar pesquisa com margem de erro
    st.session_state.pesquisas.append({
        'dia': st.session_state.dia,
        'pop': st.session_state.popularidade + random.uniform(-3.5, 3.5),
        'margem': 3.5
    })
    
    # Histórico
    st.session_state.historico.append({
        'dia': st.session_state.dia,
        'evento': st.session_state.evento_atual['titulo'] if st.session_state.evento_atual else 'N/A',
        'pop': st.session_state.popularidade,
        'caixa': st.session_state.caixa,
        'energia': st.session_state.energia
    })
    
    # Verificar escândalo
    if st.session_state.risco_escandalo >= 82:
        st.session_state.total_escandalos += 1
        st.session_state.risco_escandalo = 35
        st.session_state.popularidade -= 18
        st.session_state.midia -= 22
        st.error("🚨 ESCÂNDALO EXPLODIU! Popularidade caiu drasticamente!")
    
    # Recuperação diária
    st.session_state.energia = min(100, st.session_state.energia + 4)
    st.session_state.caixa += bonus['caixa']

def verificar_condicoes():
    """Verifica condições de vitória/derrota (MAIS RIGOROSO)"""
    
    # Derrotas imediatas
    if st.session_state.popularidade <= 4:
        st.session_state.game_over = True
        st.session_state.vitoria = False
        return "DERROTA: Popularidade abaixo de 4%. Partido retirou sua candidatura."
    
    if st.session_state.caixa <= 0:
        st.session_state.game_over = True
        st.session_state.vitoria = False
        return "DERROTA: Campanha falida. TSE cassou sua candidatura."
    
    if st.session_state.energia <= 0:
        st.session_state.game_over = True
        st.session_state.vitoria = False
        return "DERROTA: Colapso de saúde. Candidato hospitalizado."
    
    if st.session_state.midia <= 6:
        st.session_state.game_over = True
        st.session_state.vitoria = False
        return "DERROTA: Imprensa hostil destruiu sua imagem pública."
    
    # Verificar coalizão
    media_coalizao = sum(st.session_state.coalizao_apoio.values()) / len(st.session_state.coalizao_apoio)
    if media_coalizao <= 22:
        st.session_state.game_over = True
        st.session_state.vitoria = False
        return "DERROTA: Coalizão desfeita. Sem apoio no Congresso."
    
    # Fim dos dias
    if st.session_state.dia > st.session_state.total_dias:
        st.session_state.game_over = True
        
        # Calcular votos por estado (precisa de 45% em cada)
        votos_totais = 0
        eleitores_totais = sum(ESTADOS_DECISIVOS[e]['eleitores'] for e in ESTADOS_DECISIVOS.keys())
        
        for estado, apoio in st.session_state.estados_support.items():
            if apoio >= 45:
                votos_totais += ESTADOS_DECISIVOS[estado]['eleitores']
        
        percentual_votos = (votos_totais / eleitores_totais) * 100
        
        if percentual_votos >= 52:
            st.session_state.vitoria = True
            return f"🎉 VITÓRIA NO 1º TURNO! Você conquistou {percentual_votos:.1f}% dos votos válidos!"
        elif percentual_votos >= 42:
            st.session_state.vitoria = True
            return f"✅ CLASSIFICADO PARA 2º TURNO! Você teve {percentual_votos:.1f}% dos votos."
        else:
            st.session_state.vitoria = False
            return f"❌ ELIMINADO! Você teve apenas {percentual_votos:.1f}% dos votos."
    
    return None

def gerar_evento():
    """Gera evento com lógica avançada"""
    
    # Chance de crise baseada no risco
    if st.session_state.risco_escandalo >= 52 and random.random() < 0.35:
        crises = [e for e in EVENTOS['geral'] if e['tipo'] == 'crise']
        if crises:
            evento = random.choice(crises)
            st.session_state.eventos_usados.append(evento['id'])
            return evento
    
    # Eventos baseados no partido
    eventos_gerais = EVENTOS["geral"]
    eventos_ideologia = EVENTOS.get(st.session_state.partido, [])
    
    if eventos_ideologia and random.random() < 0.28:
        pool_eventos = eventos_ideologia
    else:
        pool_eventos = eventos_gerais
    
    # Filtrar eventos já usados recentemente
    eventos_disponiveis = [e for e in pool_eventos if e['id'] not in st.session_state.eventos_usados[-12:]]
    
    if not eventos_disponiveis:
        eventos_disponiveis = pool_eventos
        st.session_state.eventos_usados = []
    
    evento = random.choice(eventos_disponiveis)
    st.session_state.eventos_usados.append(evento['id'])
    
    return evento

# ============================================================================
# GRÁFICOS PREMIUM
# ============================================================================

def criar_grafico_evolucao():
    """Cria gráfico premium da evolução da popularidade"""
    cor = "#DC143C" if st.session_state.partido == 'esquerda' else "#FFD700" if st.session_state.partido == 'centro' else "#0066CC"
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=st.session_state.evolucao_dias,
        y=st.session_state.evolucao_pop,
        mode='lines+markers',
        name='Popularidade',
        line=dict(color=cor, width=4),
        marker=dict(size=10, symbol='circle')
    ))
    
    fig.add_hline(y=52, line_dash="dash", line_color="#00ff88", annotation_text="Vitória 1º Turno")
    fig.add_hline(y=42, line_dash="dash", line_color="#ffa500", annotation_text="2º Turno")
    fig.add_hline(y=12, line_dash="dash", line_color="#ff4757", annotation_text="Zona de Perigo")
    
    fig.update_layout(
        title='📈 Evolução da Popularidade',
        xaxis_title='Dia de Campanha',
        yaxis_title='Popularidade (%)',
        yaxis_range=[0, 100],
        height=350,
        template='plotly_white',
        font=dict(family='Inter', size=12),
        hovermode='x unified'
    )
    
    return fig

def criar_grafico_estados():
    """Cria gráfico de apoio por estado"""
    estados = list(st.session_state.estados_support.keys())
    valores = list(st.session_state.estados_support.values())
    cores = [ESTADOS_DECISIVOS[e]['cor'] for e in estados]
    
    fig = go.Figure(data=[
        go.Bar(
            x=estados,
            y=valores,
            marker_color=cores,
            text=[f'{v:.1f}%' for v in valores],
            textposition='auto'
        )
    ])
    
    fig.add_hline(y=45, line_dash="dash", line_color="#00ff88", annotation_text="Meta por Estado")
    
    fig.update_layout(
        title='🗺️ Apoio por Estado Decisivo',
        yaxis_range=[0, 100],
        height=350,
        template='plotly_white',
        showlegend=False,
        font=dict(family='Inter', size=11)
    )
    
    return fig

def criar_grafico_coalizao():
    """Cria gráfico de apoio da coalizão"""
    partidos = list(st.session_state.coalizao_apoio.keys())
    valores = list(st.session_state.coalizao_apoio.values())
    cores = [PARTIDOS_COALIZAO[p]['cor'] for p in partidos]
    
    fig = go.Figure(data=[
        go.Bar(
            x=[PARTIDOS_COALIZAO[p]['sigla'] for p in partidos],
            y=valores,
            marker_color=cores,
            text=[f'{v:.1f}%' for v in valores],
            textposition='auto'
        )
    ])
    
    fig.add_hline(y=50, line_dash="dash", line_color="#ffa500", annotation_text="Apoio Mínimo")
    
    fig.update_layout(
        title='🤝 Apoio da Coalizão Partidária',
        yaxis_range=[0, 100],
        height=300,
        template='plotly_white',
        showlegend=False,
        font=dict(family='Inter', size=11)
    )
    
    return fig

# ============================================================================
# TELAS DO JOGO
# ============================================================================

def mostrar_tela_inicial():
    """Tela inicial premium"""
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px;">
        <h1 style="font-size: 52px; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">🇧🇷 CANDIDATO 2026</h1>
        <p style="font-size: 20px; color: #666; margin: 15px 0;">Simulador Presidencial Premium</p>
        <p style="font-size: 14px; color: #999;">A campanha eleitoral mais realista e desafiadora</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_info, col_rec = st.columns([2, 1])
    
    with col_info:
        st.markdown("""
        ### 🎮 MECÂNICAS PREMIUM
        
        | Recurso | Descrição |
        |---------|-----------|
        | 🎭 **Consequências Ocultas** | Não veja números exatos antes de decidir |
        | 👥 **5 Assessores** | Cada um com confiabilidade diferente (70-96%) |
        | 🤝 **Coalizão de 4 Partidos** | Mantenha todos felizes simultaneamente |
        | 🗺️ **8 Estados Decisivos** | Precisa de 45% em cada para vencer |
        | 🚨 **Escândalos Ocultos** | Risk meter que pode explodir a qualquer momento |
        | 📊 **Pesquisas com Margem** | Dados têm ±3.5% de erro |
        | ⚡ **Variabilidade Aleatória** | Efeitos variam ±25% a cada decisão |
        | 🔒 **Condições Bloqueadas** | Algumas opções requerem stats mínimos |
        | 💣 **Perguntas com Armadilhas** | A escolha óbvia nem sempre é a melhor |
        
        ### ⚠️ AVISO DE DIFICULDADE
        
        Este jogo é **INTENCIONALMENTE DESAFIADOR**. A maioria dos jogadores 
        não completa a campanha na primeira tentativa. Requer estratégia, 
        gestão de recursos e tomada de decisão sob pressão.
        """)
        
        st.markdown("### 🎯 Nível de Dificuldade")
        dificuldade = st.radio(
            "Escolha sabiamente:",
            ["Fácil - Aprendizado", "Normal - Experiência Real", "Difícil - Desafio", "HARDCORE - Somente Expert"],
            label_visibility="collapsed"
        )
        
        diff_map = {
            "Fácil - Aprendizado": "Fácil",
            "Normal - Experiência Real": "Normal", 
            "Difícil - Desafio": "Difícil",
            "HARDCORE - Somente Expert": "HARDCORE"
        }
        st.session_state.dificuldade_temp = diff_map[dificuldade]
    
    with col_rec:
        st.markdown("### 🏆 Seu Recorde")
        hs = load_high_score()
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Maior Popularidade</h3>
            <h1>{hs['score']:.1f}%</h1>
            <p style="font-size: 14px;">{hs['partido']}</p>
            <p style="font-size: 12px; opacity: 0.7;">{hs['dificuldade']} | {hs['data']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        total_ach = len(ACHIEVEMENTS)
        unlocked = len(st.session_state.get('conquistas_unlocked', []))
        st.write(f"### 🏅 Conquistas: {unlocked}/{total_ach}")
        st.progress(unlocked / total_ach)
    
    st.divider()
    
    st.markdown("### 🎭 Escolha Sua Ideologia")
    
    col_esq, col_cen, col_dir = st.columns(3)
    
    with col_esq:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);">
            <h2 style="font-size: 48px; margin: 0;">🔴</h2>
            <h3>ESQUERDA</h3>
            <p style="font-size: 14px;">Frente Progressista</p>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">
            <p style="font-size: 13px;">📈 +1.2% Popularidade/decisão</p>
            <p style="font-size: 13px;">⚡ +2.5 Energia/dia</p>
            <p style="font-size: 13px; color: #ff6b6b;">💰 -R$ 600 Caixa/dia</p>
            <p style="font-size: 12px; margin-top: 15px;">✅ Eventos sociais exclusivos</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔴 Jogar como Esquerda", key="btn_esq", use_container_width=True, type="primary"):
            st.session_state.partido = "esquerda"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()
    
    with col_cen:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);">
            <h2 style="font-size: 48px; margin: 0;">🟡</h2>
            <h3>CENTRO</h3>
            <p style="font-size: 14px;">Aliança Democrática</p>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">
            <p style="font-size: 13px;">📈 ±0% Popularidade (Neutro)</p>
            <p style="font-size: 13px;">⚡ +1.5 Energia/dia</p>
            <p style="font-size: 13px; color: #90ee90;">💰 +R$ 1.200 Caixa/dia</p>
            <p style="font-size: 12px; margin-top: 15px;">✅ Eventos de reforma exclusivos</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🟡 Jogar como Centro", key="btn_cen", use_container_width=True, type="primary"):
            st.session_state.partido = "centro"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()
    
    with col_dir:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #0066CC 0%, #003366 100%);">
            <h2 style="font-size: 48px; margin: 0;">🔵</h2>
            <h3>DIREITA</h3>
            <p style="font-size: 14px;">Movimento Liberal</p>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 15px 0;">
            <p style="font-size: 13px;">📈 -0.8% Popularidade/decisão</p>
            <p style="font-size: 13px;">⚡ ±0 Energia/dia</p>
            <p style="font-size: 13px; color: #90ee90;">💰 +R$ 2.200 Caixa/dia</p>
            <p style="font-size: 12px; margin-top: 15px;">✅ Eventos econômicos exclusivos</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔵 Jogar como Direita", key="btn_dir", use_container_width=True, type="primary"):
            st.session_state.partido = "direita"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()

def mostrar_jogo():
    """Tela principal do jogo premium"""
    
    # Header premium
    nome_partido = "🔴 Esquerda" if st.session_state.partido == "esquerda" else "🟡 Centro" if st.session_state.partido == "centro" else "🔵 Direita"
    st.markdown(f"""
    <div class="game-header">
        <h2 style="margin: 0; font-size: 28px;">🇧🇷 CAMPANHA PRESIDENCIAL 2026</h2>
        <p style="margin: 12px 0 0 0; font-size: 16px; opacity: 0.9;">{nome_partido} | Dia {st.session_state.dia}/{st.session_state.total_dias} | {st.session_state.dificuldade}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Controles
    col_graf, col_reiniciar = st.columns([1, 1])
    with col_graf:
        if st.button("📊 Gráficos", use_container_width=True):
            st.session_state.mostrar_grafico = not st.session_state.mostrar_grafico
    with col_reiniciar:
        if st.button("🔄 Reiniciar Campanha", use_container_width=True):
            st.session_state.partido = None
            st.rerun()
    
    # Alerta de escândalo
    if st.session_state.risco_escandalo >= 62:
        st.markdown(f"""
        <div class="alert-box">
            🚨 ALERTA DE ESCÂNDALO IMINENTE | Risco: {st.session_state.risco_escandalo:.0f}%
        </div>
        """, unsafe_allow_html=True)
    
    # Combo counter
    if st.session_state.combo >= 3:
        st.markdown(f"""
        <div style="text-align: center;">
            <div class="combo-badge">
                🔥 COMBO x{st.session_state.combo} - Bônus de Popularidade Ativo!
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats em cards premium
    col_pop, col_caixa, col_energia, col_midia, col_risco = st.columns(5)
    
    with col_pop:
        cor = "#00ff88" if st.session_state.popularidade >= 42 else "#ffa500" if st.session_state.popularidade >= 25 else "#ff4757"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {cor}, #333);">
            <h3>📊 Popularidade</h3>
            <h1>{st.session_state.popularidade:.1f}%</h1>
            <p class="trend">Meta: 42%+</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.popularidade / 100)
    
    with col_caixa:
        cor = "#00ff88" if st.session_state.caixa >= 80000 else "#ffa500" if st.session_state.caixa >= 35000 else "#ff4757"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {cor}, #333);">
            <h3>💰 Caixa</h3>
            <h1>R$ {st.session_state.caixa:,.0f}</h1>
            <p class="trend">{'Saudável' if st.session_state.caixa >= 80000 else 'Atenção' if st.session_state.caixa >= 35000 else 'CRÍTICO'}</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(st.session_state.caixa / 250000, 1.0))
    
    with col_energia:
        cor = "#00ff88" if st.session_state.energia >= 55 else "#ffa500" if st.session_state.energia >= 30 else "#ff4757"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {cor}, #333);">
            <h3>⚡ Energia</h3>
            <h1>{st.session_state.energia}%</h1>
            <p class="trend">{'Bom' if st.session_state.energia >= 55 else 'Cansado' if st.session_state.energia >= 30 else 'EXAUSTO'}</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.energia / 100)
    
    with col_midia:
        cor = "#00ff88" if st.session_state.midia >= 55 else "#ffa500" if st.session_state.midia >= 30 else "#ff4757"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {cor}, #333);">
            <h3>📰 Mídia</h3>
            <h1>{st.session_state.midia:.0f}</h1>
            <p class="trend">{'Favorável' if st.session_state.midia >= 55 else 'Neutra' if st.session_state.midia >= 30 else 'HOSTIL'}</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.midia / 100)
    
    with col_risco:
        cor = "#00ff88" if st.session_state.risco_escandalo <= 30 else "#ffa500" if st.session_state.risco_escandalo <= 60 else "#ff4757"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {cor}, #333);">
            <h3>🚨 Risco</h3>
            <h1>{st.session_state.risco_escandalo:.0f}%</h1>
            <p class="trend">{'Seguro' if st.session_state.risco_escandalo <= 30 else 'Atenção' if st.session_state.risco_escandalo <= 60 else 'PERIGO'}</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.risco_escandalo / 100)
    
    st.divider()
    
    # Assessores
    st.markdown("### 👥 Selecione Seu Assessor para Conselho")
    cols_ass = st.columns(5)
    for i, (key, assessor) in enumerate(ASSESSORES.items()):
        with cols_ass[i]:
            selected = st.session_state.assessor_selecionado == key
            st.markdown(f"""
            <div class="advisor-card {'selected' if selected else ''}">
                <div style="font-size: 28px; margin-bottom: 8px;">{assessor['icone']}</div>
                <strong style="font-size: 13px;">{assessor['nome']}</strong><br>
                <small style="color: #666;">{assessor['cargo']}</small><br>
                <small style="color: {assessor['cor']}; font-weight: 600;">{assessor['confiabilidade']*100:.0f}% confiável</small>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Selecionar", key=f"ass_{key}", use_container_width=True):
                st.session_state.assessor_selecionado = key
                st.rerun()
    
    # Gráficos (toggle)
    if st.session_state.mostrar_grafico:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.plotly_chart(criar_grafico_evolucao(), use_container_width=True)
        with col_g2:
            st.plotly_chart(criar_grafico_estados(), use_container_width=True)
        
        col_g3, col_g4 = st.columns(2)
        with col_g3:
            st.plotly_chart(criar_grafico_coalizao(), use_container_width=True)
        with col_g4:
            st.markdown("### 🗺️ Estados Decisivos")
            for estado, dados in ESTADOS_DECISIVOS.items():
                apoio = st.session_state.estados_support[estado]
                status = "✅" if apoio >= 45 else "❌"
                st.markdown(f"""
                <div class="region-item">
                    <strong>{estado}</strong> ({dados['eleitores']}M)
                    <div class="region-bar">
                        <div class="region-fill" style="width: {apoio}%; background: {dados['cor']};"></div>
                    </div>
                    <span style="font-weight: 600;">{apoio:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
    
    # Área do evento
    if st.session_state.game_over:
        # Tela de fim de jogo
        if st.session_state.vitoria:
            st.balloons()
            st.markdown(f"""
            <div class="victory-screen">
                <h1 style="margin: 0; font-size: 52px;">🎉 VITÓRIA!</h1>
                <p style="font-size: 24px; margin: 25px 0;">Sua campanha entrou para a história!</p>
                <p style="font-size: 20px;">Popularidade final: <strong>{st.session_state.popularidade:.1f}%</strong></p>
                <p style="font-size: 18px;">Dias completados: <strong>{st.session_state.dia}</strong></p>
                <p style="font-size: 16px;">Escândalos sobrevividos: <strong>{st.session_state.total_escandalos}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            if save_high_score(st.session_state.popularidade, st.session_state.dia, st.session_state.partido, st.session_state.dificuldade):
                st.success("🏆 NOVO RECORDE PESSOAL!")
        else:
            st.markdown(f"""
            <div class="defeat-screen">
                <h1 style="margin: 0; font-size: 52px;">😞 DERROTA</h1>
                <p style="font-size: 24px; margin: 25px 0;">A política é implacável...</p>
                <p style="font-size: 20px;">{st.session_state.msg_fim}</p>
                <p style="font-size: 18px;">Popularidade final: <strong>{st.session_state.popularidade:.1f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Conquistas desbloqueadas
        if st.session_state.conquistas_unlocked:
            st.markdown("### 🏅 Conquistas Desbloqueadas")
            cols = st.columns(3)
            for i, ach_id in enumerate(st.session_state.conquistas_unlocked):
                ach = ACHIEVEMENTS.get(ach_id, {})
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="achievement-badge">
                        {ach.get('icon', '🏆')} {ach.get('name', 'Unknown')}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Histórico
        with st.expander("📜 Resumo Completo da Campanha", expanded=False):
            for i, item in enumerate(st.session_state.historico, 1):
                st.write(f"{i}. Dia {item['dia']}: {item['evento'][:50]}... (Pop: {item['pop']:.1f}%)")
        
        if st.button("🎮 Jogar Novamente", use_container_width=True, type="primary"):
            st.session_state.partido = None
            st.rerun()
            
    else:
        # Gerar evento se necessário
        if st.session_state.evento_atual is None:
            st.session_state.evento_atual = gerar_evento()
        
        evento = st.session_state.evento_atual
        
        # Card do evento premium
        classe = "crisis" if evento['tipo'] == 'crise' else "opportunity" if evento['impacto'] == 'crítico' else ""
        st.markdown(f"""
        <div class="event-card {classe}">
            <div style="font-size: 56px; margin-bottom: 15px;">{evento['icon']}</div>
            <h2 style="margin: 0 0 15px 0; color: #333; font-size: 26px;">{evento['titulo']}</h2>
            <div style="font-size: 16px; color: #555; line-height: 1.7;">{evento['desc']}</div>
            <div style="margin-top: 20px; display: flex; gap: 10px; flex-wrap: wrap;">
                <span style="background: #667eea; color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                    IMPACTO: {evento['impacto'].upper()}
                </span>
                <span style="background: #764ba2; color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                    DURAÇÃO: {evento['duracao']} DIAS
                </span>
                <span style="background: {'#ff4757' if evento['tipo'] == 'crise' else '#667eea'}; color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                    {evento['tipo'].upper()}
                </span>
                {'<span style="background: #f093fb; color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;">💣 CONTÉM ARMADILHA</span>' if evento.get('armadilha') else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Info do assessor selecionado
        assessor = ASSESSORES[st.session_state.assessor_selecionado]
        st.markdown(f"""
        <div class="hint-text">
            <strong>{assessor['icone']} {assessor['nome']}</strong> — {assessor['descricao']}<br>
            <small>Confiabilidade: {assessor['confiabilidade']*100:.0f}% | Especialidade: {assessor['especialidade']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.warning("""
        ⚠️ **ATENÇÃO:** Consequências exatas estão OCULTAS. 
        Confie no conselho do seu assessor, analise o contexto 
        e tome decisões baseadas em estratégia. 
        Esta é a realidade da política!
        """)
        
        # Botões de opção
        for i, opcao in enumerate(evento['opcoes']):
            # Verificar condições
            pode_escolher, motivo = check_condicoes_opcao(opcao)
            
            # Conselho do assessor
            conselho = get_assessor_advice(evento, i)
            
            # Classe visual para armadilhas
            classe_opcao = "trap" if opcao.get('armadilha') else "smart" if opcao['efeito_base']['pop'] > 8 else ""
            
            st.markdown(f"""
            <div class="option-card {classe_opcao}">
                <strong>Opção {i+1}:</strong> {opcao['texto']}<br>
                <em style="color: #666; font-size: 14px;">{opcao['descricao_oculta']}</em><br>
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px dashed #ddd;">
                    <strong>💡 Conselho:</strong> {conselho}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if pode_escolher:
                if st.button(f"✅ Escolher Opção {i+1}", key=f"opt_{i}", use_container_width=True):
                    aplicar_consequencias(opcao)
                    st.session_state.evento_atual = None
                    st.session_state.dia += 1
                    
                    msg = verificar_condicoes()
                    if msg:
                        st.session_state.msg_fim = msg
                    
                    st.rerun()
            else:
                st.button(f"🔒 Opção {i+1} (Requisitos: {motivo})", key=f"opt_{i}", use_container_width=True, disabled=True)
        
        # Feedback da última ação
        if st.session_state.historico:
            ultimo = st.session_state.historico[-1]
            st.info(f"💬 {ultimo['evento'][:80]}...")
        
        # Dicas estratégicas
        with st.expander("💡 Dicas de Estratégia Premium"):
            st.write("""
            ### 📖 Guia de Sobrevivência HARDCORE
            
            **GERENCIAMENTO DE RECURSOS:**
            - Nunca deixe energia abaixo de 30% (recuperação lenta)
            - Mantenha caixa acima de R$ 50.000 para emergências
            - Mídia abaixo de 30% = zona de perigo extremo
            
            **COALIZÃO:**
            - Média de apoio deve ficar acima de 55%
            - Partidos com menos de 35% podem abandonar
            - Negocie antes que seja tarde
            
            **ESTADOS:**
            - Foque em estados com mais eleitores (SP: 22.5M, MG: 10.8M)
            - Precisa de 45% em cada estado para contar como vitória
            - Não negligencie estados pequenos
            
            **RISCO DE ESCÂNDALO:**
            - Acima de 60% = perigo iminente
            - Escolha opções com baixo risco quando estiver alto
            - Escândalos causam -18% popularidade instantânea
            
            **ASSESSORES:**
            - Estrategista: Melhor para popularidade (85% confiável)
            - Financeiro: Mais confiável para caixa (92%)
            - Jurídico: Essencial quando risco está alto (96%)
            - Nenhum assessor é 100% confiável!
            
            **ARMADILHAS:**
            - A escolha "óbvia" nem sempre é a melhor
            - Leia as descrições ocultas com atenção
            - Às vezes, a opção menos popular é a mais estratégica
            """)

# ============================================================================
# SIDEBAR PREMIUM
# ============================================================================

def render_sidebar():
    """Sidebar premium com informações"""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/ballot-box-with-ball.png", width=80)
        st.title("🎛️ Painel de Controle")
        
        if 'partido' in st.session_state and st.session_state.partido:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px;">
                <strong>🎭 Partido:</strong> {st.session_state.partido.upper()}<br>
                <strong>🎯 Dificuldade:</strong> {st.session_state.dificuldade}
            </div>
            """, unsafe_allow_html=True)
            
            st.write("### 📊 Status Atual")
            st.write(f"📅 **Dia:** {st.session_state.dia}/{st.session_state.total_dias}")
            st.write(f"📈 **Popularidade:** {st.session_state.popularidade:.1f}%")
            st.write(f"💰 **Caixa:** R$ {st.session_state.caixa:,.0f}")
            st.write(f"⚡ **Energia:** {st.session_state.energia}%")
            st.write(f"📰 **Mídia:** {st.session_state.midia:.0f}")
            st.write(f"🚨 **Risco:** {st.session_state.risco_escandalo:.0f}%")
            
            # Alertas contextuais
            if st.session_state.popularidade < 25:
                st.warning("⚠️ Popularidade crítica!")
            if st.session_state.caixa < 40000:
                st.warning("⚠️ Caixa baixo para emergências!")
            if st.session_state.energia < 35:
                st.warning("⚠️ Energia baixa - descanse!")
            if st.session_state.risco_escandalo > 55:
                st.error("🚨 Risco de escândalo alto!")
            
            st.divider()
            
            # Combo
            if st.session_state.combo >= 2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f093fb, #f5576c); padding: 12px; border-radius: 12px; color: white; text-align: center; font-weight: 600;">
                    🔥 Combo x{st.session_state.combo} Ativo!
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Coalizão
            st.write("### 🤝 Coalizão Partidária")
            for partido, apoio in st.session_state.coalizao_apoio.items():
                cor = PARTIDOS_COALIZAO[partido]['cor']
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 10px; margin: 8px 0;">
                    <span style="width: 8px; height: 8px; background: {cor}; border-radius: 50%;"></span>
                    <span style="flex: 1;">{PARTIDOS_COALIZAO[partido]['sigla']}</span>
                    <span style="font-weight: 600;">{apoio:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
                st.progress(apoio / 100)
            
            st.divider()
            
            # Conquistas
            st.write("### 🏅 Conquistas")
            total = len(ACHIEVEMENTS)
            unlocked = len(st.session_state.conquistas_unlocked)
            st.write(f"**{unlocked}/{total}** desbloqueadas")
            st.progress(unlocked / total)
            
            # Mostrar conquistas recentes
            if st.session_state.conquistas_unlocked:
                st.write("**Últimas:**")
                for ach_id in st.session_state.conquistas_unlocked[-3:]:
                    ach = ACHIEVEMENTS.get(ach_id, {})
                    st.write(f"• {ach.get('icon', '🏆')} {ach.get('name', 'Unknown')}")
        
        st.divider()
        st.info("""
        **📖 Como Jogar:**
        1. Escolha ideologia
        2. Selecione assessor
        3. Decida a cada dia
        4. Mantenha stats altos
        5. Vença com 42%+
        
        **💡 Dica:** Clique em "Gráficos" para ver evolução!
        """)

# ============================================================================
# SISTEMA DE CONQUISTAS
# ============================================================================

def check_achievements():
    """Verifica e desbloqueia conquistas"""
    new_achievements = []
    
    # Primeira decisão
    if st.session_state.dia >= 2 and "first_decision" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("first_decision")
        new_achievements.append("first_decision")
    
    # Popularidade
    pop = st.session_state.popularidade
    if pop >= 30 and "pop_rising" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("pop_rising")
        new_achievements.append("pop_rising")
    if pop >= 50 and "pop_leader" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("pop_leader")
        new_achievements.append("pop_leader")
    if pop >= 70 and "pop_legend" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("pop_legend")
        new_achievements.append("pop_legend")
    
    # Caixa
    if st.session_state.caixa >= 500000 and "treasury_master" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("treasury_master")
        new_achievements.append("treasury_master")
    
    # Escândalos
    if st.session_state.total_escandalos >= 3 and "scandal_survivor" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("scandal_survivor")
        new_achievements.append("scandal_survivor")
    
    # Combo
    if st.session_state.combo >= 5 and "combo_king" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("combo_king")
        new_achievements.append("combo_king")
    
    # Estados
    estados_liderando = sum(1 for v in st.session_state.estados_support.values() if v >= 45)
    if estados_liderando >= 5 and "regional_champion" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("regional_champion")
        new_achievements.append("regional_champion")
    
    return new_achievements

# ============================================================================
# MAIN - PONTO DE ENTRADA
# ============================================================================

def main():
    """Função principal - inicializa tudo corretamente"""
    
    # Inicializar variáveis essenciais
    essential_vars = [
        'partido', 'recorde_pop', 'mostrar_grafico', 'mostrar_estados', 
        'mostrar_coalizao', 'assessor_selecionado', 'conquistas_unlocked',
        'new_achievements', 'combo', 'max_combo', 'total_escandalos',
        'high_score_data', 'pesquisas'
    ]
    
    for var in essential_vars:
        if var not in st.session_state:
            if var == 'partido':
                st.session_state.partido = None
            elif var == 'recorde_pop':
                st.session_state.recorde_pop = 0.0
            elif var in ['mostrar_grafico', 'mostrar_estados', 'mostrar_coalizao']:
                st.session_state[var] = False
            elif var == 'assessor_selecionado':
                st.session_state.assessor_selecionado = "estrategista"
            elif var == 'conquistas_unlocked':
                st.session_state.conquistas_unlocked = []
            elif var == 'new_achievements':
                st.session_state.new_achievements = []
            elif var in ['combo', 'max_combo', 'total_escandalos']:
                st.session_state[var] = 0
            elif var == 'high_score_data':
                st.session_state.high_score_data = {'score': 0, 'dia': 0, 'partido': 'Nenhum', 'data': 'N/A', 'dificuldade': 'Normal'}
            elif var == 'pesquisas':
                st.session_state.pesquisas = []
    
    # Se o jogo já começou, garantir que todas as variáveis existem
    if st.session_state.partido is not None:
        required_vars = [
            'dia', 'total_dias', 'popularidade', 'caixa', 'energia',
            'midia', 'risco_escandalo', 'game_over', 'vitoria', 'msg_fim',
            'evento_atual', 'historico', 'evolucao_pop', 'evolucao_dias',
            'dificuldade', 'eventos_usados', 'estados_support', 'coalizao_apoio'
        ]
        if not all(var in st.session_state for var in required_vars):
            init_game(st.session_state.get('dificuldade', 'Normal'))
    
    # Renderizar sidebar
    render_sidebar()
    
    # Renderizar tela apropriada
    if st.session_state.partido is None:
        mostrar_tela_inicial()
    else:
        # Check achievements
        new_achs = check_achievements()
        if new_achs:
            for ach_id in new_achs:
                ach = ACHIEVEMENTS.get(ach_id, {})
                st.success(f"🏆 CONQUISTA: {ach.get('icon', '🏆')} {ach.get('name', 'Unknown')}!")
        
        mostrar_jogo()

# ============================================================================
# EXECUÇÃO
# ============================================================================
if __name__ == "__main__":
    main()
