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
# CSS PREMIUM COM FORMATAÇÃO PROFISSIONAL
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; box-sizing: border-box; }
    
    /* Cards de Métricas */
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 22px 18px;
        border-radius: 18px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
        border: 1px solid rgba(255,255,255,0.08);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        margin: 6px 0;
    }
    .metric-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(102, 126, 234, 0.45); }
    .metric-card h3 { margin: 0; font-size: 11px; opacity: 0.75; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 600; }
    .metric-card h1 { margin: 10px 0 0 0; font-size: 28px; font-weight: 700; }
    .metric-card .trend { font-size: 12px; margin-top: 6px; opacity: 0.9; }
    .trend.up { color: #00ff88; font-weight: 600; }
    .trend.down { color: #ff4757; font-weight: 600; }
    .trend.warn { color: #ffa500; font-weight: 600; }
    
    /* Card de Evento Premium */
    .event-card {
        background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
        padding: 32px;
        border-radius: 22px;
        border-left: 7px solid #667eea;
        box-shadow: 0 10px 35px rgba(0,0,0,0.12);
        margin: 22px 0;
        animation: slideIn 0.35s ease;
    }
    @keyframes slideIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    .event-card.crisis { border-left-color: #ff4757; background: linear-gradient(135deg, #fff5f5 0%, #ffeaea 100%); }
    .event-card.opportunity { border-left-color: #00ff88; background: linear-gradient(135deg, #f0fff4 0%, #e8fff0 100%); }
    
    /* Tags de Evento */
    .event-tags { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 18px; }
    .tag { padding: 5px 12px; border-radius: 18px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .tag.impact { background: #667eea; color: white; }
    .tag.duration { background: #764ba2; color: white; }
    .tag.type { background: #ff4757; color: white; }
    .tag.trap { background: linear-gradient(135deg, #f093fb, #f5576c); color: white; animation: pulse 2s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.85; } }
    
    /* Opções de Decisão - Formatação Profissional */
    .option-container {
        display: grid;
        grid-template-columns: 1fr;
        gap: 14px;
        margin: 20px 0;
    }
    .option-card {
        background: white;
        padding: 18px 22px;
        border-radius: 14px;
        border: 2px solid #e8e8e8;
        transition: all 0.2s ease;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .option-card:hover {
        border-color: #667eea;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.18);
        transform: translateX(4px);
    }
    .option-card.trap {
        border-left: 4px solid #ff4757;
        background: linear-gradient(90deg, #fff5f5 0%, white 100%);
    }
    .option-card.smart {
        border-left: 4px solid #00ff88;
        background: linear-gradient(90deg, #f0fff4 0%, white 100%);
    }
    
    .option-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding-bottom: 8px;
        border-bottom: 1px dashed #e0e0e0;
    }
    .option-number {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 14px;
        flex-shrink: 0;
    }
    .option-title {
        font-weight: 600;
        font-size: 15px;
        color: #222;
        line-height: 1.3;
    }
    
    .option-desc {
        font-size: 13px;
        color: #666;
        font-style: italic;
        padding-left: 38px;
        line-height: 1.4;
    }
    
    .option-advice {
        background: #f8f9fa;
        padding: 10px 14px;
        border-radius: 10px;
        border-left: 3px solid #667eea;
        font-size: 13px;
        color: #444;
        margin-left: 38px;
        line-height: 1.4;
    }
    
    .option-stats {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        padding-left: 38px;
        font-size: 12px;
    }
    .stat-item {
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 3px 8px;
        background: #f0f0f0;
        border-radius: 6px;
    }
    .stat-positive { color: #00aa55; font-weight: 600; }
    .stat-negative { color: #dd3344; font-weight: 600; }
    .stat-neutral { color: #666; }
    
    /* Botões Premium */
    .stButton>button {
        border-radius: 11px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        transition: all 0.25s ease !important;
        border: 2px solid transparent !important;
        font-size: 13px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(102, 126, 234, 0.35) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 7px 22px rgba(102, 126, 234, 0.55) !important;
    }
    .stButton>button:disabled {
        background: #ccc !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
    }
    
    /* Telas de Vitória/Derrota */
    .victory-screen {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 50%, #00ff88 100%);
        padding: 45px;
        border-radius: 26px;
        color: white;
        text-align: center;
        margin: 28px 0;
        box-shadow: 0 18px 55px rgba(0,255,136,0.4);
        animation: celebrate 0.5s ease;
    }
    @keyframes celebrate { 0% { transform: scale(0.97); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
    .defeat-screen {
        background: linear-gradient(135deg, #cb2d3e 0%, #ef473a 50%, #ff4757 100%);
        padding: 45px;
        border-radius: 26px;
        color: white;
        text-align: center;
        margin: 28px 0;
        box-shadow: 0 18px 55px rgba(255,71,87,0.4);
    }
    
    /* Alertas */
    .alert-box {
        background: linear-gradient(135deg, #ff6b81 0%, #ff4757 100%);
        color: white;
        padding: 16px 22px;
        border-radius: 14px;
        margin: 18px 0;
        font-weight: 500;
        font-size: 14px;
        box-shadow: 0 7px 25px rgba(255,71,87,0.35);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .success-box {
        background: linear-gradient(135deg, #00ff88 0%, #00d9a0 100%);
        color: #1a1a2e;
        padding: 16px 22px;
        border-radius: 14px;
        margin: 18px 0;
        font-weight: 500;
        font-size: 14px;
        box-shadow: 0 7px 25px rgba(0,255,136,0.35);
    }
    
    /* Assessores */
    .advisor-card {
        background: white;
        padding: 16px 14px;
        border-radius: 14px;
        box-shadow: 0 3px 16px rgba(0,0,0,0.08);
        margin: 6px 0;
        border: 2px solid transparent;
        transition: all 0.25s ease;
        text-align: center;
    }
    .advisor-card:hover { border-color: #667eea; transform: translateY(-2px); }
    .advisor-card.selected {
        border-color: #00ff88;
        background: linear-gradient(135deg, #f0fff4, #e8fff0);
        box-shadow: 0 6px 24px rgba(0,255,136,0.25);
    }
    
    /* Conquistas */
    .achievement-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 7px 14px;
        border-radius: 18px;
        font-size: 12px;
        font-weight: 600;
        margin: 3px;
        animation: popIn 0.35s ease;
    }
    @keyframes popIn { 0% { transform: scale(0); opacity: 0; } 70% { transform: scale(1.08); } 100% { transform: scale(1); opacity: 1; } }
    
    /* Header Premium */
    .game-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 28px 32px;
        border-radius: 22px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 12px 45px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.08);
    }
    
    /* Combo Badge */
    .combo-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 9px 22px;
        border-radius: 24px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 7px;
        margin: 12px 0;
        animation: pulse 2s infinite;
        box-shadow: 0 7px 22px rgba(240, 147, 251, 0.45);
        font-size: 13px;
    }
    
    /* Hint Box */
    .hint-box {
        background: #f8fafc;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 14px 0;
        font-size: 13px;
        color: #445;
        line-height: 1.5;
    }
    .hint-box strong { color: #222; }
    
    /* Regional Bar */
    .region-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        background: white;
        border-radius: 11px;
        margin: 5px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .region-bar {
        flex: 1;
        height: 7px;
        background: #e8e8e8;
        border-radius: 4px;
        overflow: hidden;
    }
    .region-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.35s ease;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 7px; }
    ::-webkit-scrollbar-track { background: #1a1a2e; border-radius: 3px; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SISTEMA DE CONQUISTAS
# ============================================================================
ACHIEVEMENTS = {
    "first_decision": {"name": "Primeira Decisão", "desc": "Faça sua primeira escolha estratégica", "icon": "🎯", "rarity": "common"},
    "pop_rising": {"name": "Em Ascensão", "desc": "Alcance 30% de popularidade", "icon": "📈", "rarity": "common"},
    "pop_leader": {"name": "Líder nas Pesquisas", "desc": "Alcance 50% de popularidade", "icon": "👑", "rarity": "rare"},
    "pop_legend": {"name": "Lenda Política", "desc": "Alcance 70% de popularidade", "icon": "🏆", "rarity": "legendary"},
    "treasury_master": {"name": "Mestre do Tesouro", "desc": "Acumule R$ 500.000 em caixa", "icon": "💰", "rarity": "rare"},
    "scandal_survivor": {"name": "Sobrevivente", "desc": "Sobreviva a 3 escândalos", "icon": "🛡️", "rarity": "epic"},
    "combo_king": {"name": "Rei do Combo", "desc": "Alcance combo x5", "icon": "🔥", "rarity": "rare"},
    "regional_champion": {"name": "Campeão Regional", "desc": "Lidere em 5+ estados decisivos", "icon": "🗺️", "rarity": "epic"},
    "first_turn_win": {"name": "Vitória Esmagadora", "desc": "Vença no primeiro turno", "icon": "🎉", "rarity": "legendary"},
    "comeback_king": {"name": "Rei do Comeback", "desc": "Volte de <15% para vitória", "icon": "🔄", "rarity": "legendary"},
    "clean_campaign": {"name": "Campanha Limpa", "desc": "Termine sem escândalos", "icon": "✨", "rarity": "legendary"},
    "marathon": {"name": "Maratonista", "desc": "Complete todos os 45 dias", "icon": "🏃", "rarity": "epic"},
    "donation_expert": {"name": "Especialista em Doações", "desc": "Receba R$ 100k em doações legais", "icon": "🤝", "rarity": "rare"},
    "media_master": {"name": "Mestre da Mídia", "desc": "Mantenha relação com mídia acima de 70", "icon": "📰", "rarity": "epic"},
}

# ============================================================================
# ASSESSORES COM CONFIABILIDADE
# ============================================================================
ASSESSORES = {
    "estrategista": {"nome": "Carlos Mendes", "cargo": "Estrategista Chefe", "icone": "🎯", "confiabilidade": 0.85, "especialidade": "popularidade", "descricao": "Analisa pesquisas e tendências eleitorais", "cor": "#667eea"},
    "financeiro": {"nome": "Ana Rodrigues", "cargo": "Diretora Financeira", "icone": "💰", "confiabilidade": 0.92, "especialidade": "caixa", "descricao": "Especialista em orçamento e captação legal", "cor": "#00ff88"},
    "comunicacao": {"nome": "Pedro Santos", "cargo": "Diretor de Comunicação", "icone": "📰", "confiabilidade": 0.72, "especialidade": "midia", "descricao": "Gerencia relação com imprensa e redes sociais", "cor": "#ffa500"},
    "politico": {"nome": "Dra. Helena Costa", "cargo": "Articuladora Política", "icone": "🤝", "confiabilidade": 0.78, "especialidade": "coalizao", "descricao": "Negocia com partidos e aliados no Congresso", "cor": "#ff4757"},
    "juridico": {"nome": "Dr. Roberto Lima", "cargo": "Advogado Eleitoral", "icone": "⚖️", "confiabilidade": 0.96, "especialidade": "risco", "descricao": "Previne problemas jurídicos e garante conformidade TSE", "cor": "#9b59b6"},
}

# ============================================================================
# PARTIDOS DA COALIZÃO
# ============================================================================
PARTIDOS_COALIZAO = {
    "base": {"nome": "Partido da Base", "sigla": "PDB", "cor": "#DC143C", "apoio_inicial": 82},
    "centrao": {"nome": "Centrão Unido", "sigla": "CPU", "cor": "#FFD700", "apoio_inicial": 65},
    "progressista": {"nome": "Frente Progressista", "sigla": "FPP", "cor": "#228B22", "apoio_inicial": 71},
    "liberal": {"nome": "Aliança Liberal", "sigla": "ALB", "cor": "#0066CC", "apoio_inicial": 58},
}

# ============================================================================
# ESTADOS DECISIVOS DO BRASIL
# ============================================================================
ESTADOS_DECISIVOS = {
    "SP": {"eleitores": 22.5, "cor": "#667eea", "perfil": "urbano-industrial"},
    "MG": {"eleitores": 10.8, "cor": "#228B22", "perfil": "misto"},
    "RJ": {"eleitores": 8.9, "cor": "#FFD700", "perfil": "urbano-turístico"},
    "BA": {"eleitores": 8.2, "cor": "#FFA500", "perfil": "nordeste"},
    "RS": {"eleitores": 5.8, "cor": "#DC143C", "perfil": "sul-agro"},
    "PR": {"eleitores": 5.7, "cor": "#228B22", "perfil": "sul-agro"},
    "PE": {"eleitores": 4.8, "cor": "#FFA500", "perfil": "nordeste"},
    "CE": {"eleitores": 4.6, "cor": "#FFA500", "perfil": "nordeste"},
}

# ============================================================================
# BANCO MASSIVO DE EVENTOS REAIS DO BRASIL (40+ EVENTOS - ZERO REPETIÇÃO)
# ============================================================================
EVENTOS = {
    "geral": [
        # === DEBATES E MÍDIA ===
        {
            "id": "debate_tv_1", "categoria": "midia",
            "titulo": "📺 Debate Presidencial - Transmissão Nacional",
            "desc": "O momento mais importante da campanha. 65 milhões de brasileiros assistindo ao vivo. Moderadores farão perguntas difíceis sobre economia, corrupção e propostas.",
            "icon": "📺", "tipo": "debate", "impacto": "crítico", "duracao": 2, "armadilha": True,
            "opcoes": [
                {"texto": "Atacar adversários com dados e fatos contundentes", "desc": "Parece forte, mas pode alienar eleitores moderados que buscam união.", "efeito": {"pop": 8, "caixa": 0, "energia": -22, "midia": 6, "risco": 18}, "cond": {"pop_min": 28}, "armadilha": False, "dica": "Bom para mobilizar base, cuidado com o tom."},
                {"texto": "Focar em histórias emocionais e conexão com o povo", "desc": "ARMADILHA: Parece óbvio, mas eleitores técnicos podem achar superficial.", "efeito": {"pop": 14, "caixa": -4000, "energia": -28, "midia": 4, "risco": 12}, "cond": {}, "armadilha": True, "dica": "⚠️ Pode parecer populista para eleitores de alta renda."},
                {"texto": "Postura conciliadora: 'Acima das brigas, focado no Brasil'", "desc": "Seguro para manter, mas pouco impactante para crescer nas pesquisas.", "efeito": {"pop": 3, "caixa": 0, "energia": -18, "midia": 14, "risco": 4}, "cond": {}, "armadilha": False, "dica": "Ideal se já está liderando. Ruim se precisa crescer."},
                {"texto": "Ignorar ataques e apresentar plano de governo detalhado", "desc": "Impressiona eleitores informados, mas pode parecer evasivo para massas.", "efeito": {"pop": 5, "caixa": -2000, "energia": -25, "midia": 10, "risco": 8}, "cond": {"energia_min": 40}, "armadilha": False, "dica": "Excelente para eleitores com ensino superior (25% do eleitorado)."},
            ]
        },
        {
            "id": "entrevista_exclusiva", "categoria": "midia",
            "titulo": "🎙️ Entrevista Exclusiva com Jornalista Influente",
            "desc": "Um dos maiores jornalistas do país pede entrevista exclusiva. A pauta é livre, mas perguntas difíceis virão sobre seu passado e propostas.",
            "icon": "🎙️", "tipo": "midia", "impacto": "alto", "duracao": 1, "armadilha": False,
            "opcoes": [
                {"texto": "Conceder entrevista com transparência total", "desc": "Ganha credibilidade, mas abre espaço para perguntas difíceis.", "efeito": {"pop": 6, "caixa": -3000, "energia": -18, "midia": 15, "risco": 10}, "cond": {}, "armadilha": False, "dica": "✅ Mídia: Transparência gera confiança. ⚠️ Risco: Perguntas imprevisíveis."},
                {"texto": "Limitar pauta a temas pré-aprovados", "desc": "Controla narrativa, mas pode parecer evasivo para imprensa.", "efeito": {"pop": 2, "caixa": -1000, "energia": -12, "midia": -5, "risco": 5}, "cond": {}, "armadilha": False, "dica": "Seguro, mas pode perder oportunidade de engajamento."},
                {"texto": "Recusar entrevista e focar em redes sociais", "desc": "ARMADILHA: Evita riscos, mas imprensa pode criar narrativa negativa.", "efeito": {"pop": -8, "caixa": 0, "energia": 5, "midia": -15, "risco": 12}, "cond": {}, "armadilha": True, "dica": "🚨 Comunicação: Pode parecer que está fugindo de perguntas difíceis."},
            ]
        },
        
        # === CRISES E ESCÂNDALOS ===
        {
            "id": "escandalo_aliado_1", "categoria": "crise",
            "titulo": "🚨 ESCÂNDALO: Aliado Envolvido em Desvio de Verbas",
            "desc": "PF divulga operação que aponta desvio de R$ 47 milhões por aliado da coalizão. Nome ligado a contratos superfaturados de obras públicas.",
            "icon": "🚨", "tipo": "crise", "impacto": "crítico", "duracao": 3, "armadilha": True,
            "opcoes": [
                {"texto": "Romper aliança imediatamente e condenar publicamente", "desc": "Ganha imagem de íntegro, mas pode perder apoio crucial no Congresso.", "efeito": {"pop": 10, "caixa": -10000, "energia": -28, "midia": -3, "risco": 22, "coalizao": -18}, "cond": {}, "armadilha": False, "dica": "✅ Jurídico: Ação correta. ⚠️ Político: Pode enfraquecer base."},
                {"texto": "Aguardar conclusão da investigação antes de se posicionar", "desc": "ARMADILHA: Parece prudente, mas eleitores interpretam como omissão.", "efeito": {"pop": -15, "caixa": 0, "energia": -18, "midia": -18, "risco": 8, "coalizao": 8}, "cond": {}, "armadilha": True, "dica": "⚠️ Comunicação: Silêncio é interpretado como culpa nas redes."},
                {"texto": "Defender aliado: 'Presunção de inocência até prova final'", "desc": "ARMADILHA PERIGOSA: Mantém coalizão, mas associa SUA imagem ao escândalo.", "efeito": {"pop": -25, "caixa": 0, "energia": -25, "midia": -30, "risco": 40, "coalizao": 15}, "cond": {"coalizao_min": 65}, "armadilha": True, "dica": "🚨 Jurídico: Risco altíssimo. Se aliado for condenado, você cai junto."},
                {"texto": "Anunciar CPI própria para investigar com transparência", "desc": "Mostra ação proativa, mas gasta capital político e pode backfire.", "efeito": {"pop": 6, "caixa": -18000, "energia": -32, "midia": 10, "risco": 28, "coalizao": -12}, "cond": {"caixa_min": 60000}, "armadilha": False, "dica": "✅ Estratégia: Mostra liderança. ⚠️ Financeiro: Custo alto."},
            ]
        },
        {
            "id": "vazamento_whatsapp", "categoria": "crise",
            "titulo": "📱 Áudio Vaza no WhatsApp: Contexto Distorcido",
            "desc": "Áudio seu em reunião privada vaza no WhatsApp. Trecho fora de contexto viraliza. 4.8 milhões já viram antes do desmentido.",
            "icon": "📱", "tipo": "crise", "impacto": "alto", "duracao": 2, "armadilha": True,
            "opcoes": [
                {"texto": "Divulgar áudio completo com contexto real", "desc": "Transparência pode reverter dano, mas dá mais visibilidade ao vazamento.", "efeito": {"pop": 5, "caixa": -2000, "energia": -15, "midia": 12, "risco": 8}, "cond": {}, "armadilha": False, "dica": "✅ Comunicação: Contexto completo ajuda. ⚠️ Mídia: Pode amplificar o assunto."},
                {"texto": "Processar quem vazou e exigir remoção", "desc": "Ação jurídica mostra seriedade, mas processo é lento.", "efeito": {"pop": 3, "caixa": -12000, "energia": -20, "midia": 8, "risco": 12}, "cond": {"caixa_min": 40000}, "armadilha": False, "dica": "✅ Jurídico: Caminho correto. ⚠️ Tempo: Fake news continua enquanto processo anda."},
                {"texto": "Ignorar e focar em pauta positiva", "desc": "ARMADILHA: Pode funcionar, mas áudio pode definir narrativa por dias.", "efeito": {"pop": -10, "caixa": 0, "energia": -8, "midia": -12, "risco": 22}, "cond": {}, "armadilha": True, "dica": "🚨 Estratégico: Risco de perder controle da narrativa."},
            ]
        },
        
        # === ECONOMIA E FINANÇAS ===
        {
            "id": "crise_economica_1", "categoria": "economia",
            "titulo": "💸 CRISE ECONÔMICA GLOBAL AFETA BRASIL",
            "desc": "Mercados em turbulência: dólar +18% em uma semana, bolsa -12%, FMI revisa previsão de crescimento do Brasil para 0.3%.",
            "icon": "💸", "tipo": "economia", "impacto": "crítico", "duracao": 2, "armadilha": True,
            "opcoes": [
                {"texto": "Prometer controle rigoroso de preços e combate à especulação", "desc": "ARMADILHA: Popular a curto prazo, mas economistas alertam para inflação futura.", "efeito": {"pop": 15, "caixa": -18000, "energia": -24, "midia": 4, "risco": 22}, "cond": {}, "armadilha": True, "dica": "⚠️ Financeiro: Pode gerar inflação. ✅ Estratégico: Popular imediato."},
                {"texto": "Defender autonomia total do Banco Central e metas fiscais", "desc": "Mercado aprova, mas pode ser impopular com eleitores de baixa renda.", "efeito": {"pop": -8, "caixa": 12000, "energia": -18, "midia": 15, "risco": 10}, "cond": {}, "armadilha": False, "dica": "✅ Financeiro: Estabilidade. ⚠️ Político: Impopular com base."},
                {"texto": "Anunciar pacote emergencial de R$ 40 bilhões para proteger empregos", "desc": "Alto impacto imediato, mas drena recursos da campanha de forma crítica.", "efeito": {"pop": 18, "caixa": -45000, "energia": -30, "midia": 12, "risco": 15}, "cond": {"caixa_min": 100000}, "armadilha": False, "dica": "✅ Estratégico: Popular e concreto. ⚠️ Financeiro: Custo muito alto."},
                {"texto": "Culpar governo anterior e prometer 'mudança estrutural'", "desc": "ARMADILHA: Fácil politicamente, mas parece evasivo sem propostas concretas.", "efeito": {"pop": 4, "caixa": 0, "energia": -14, "midia": -6, "risco": 14}, "cond": {}, "armadilha": True, "dica": "⚠️ Comunicação: Pode parecer discurso vazio sem ações."},
            ]
        },
        {
            "id": "doacoes_campanha", "categoria": "financas",
            "titulo": "💰 DOAÇÕES DE CAMPANHA: OPORTUNIDADE E RISCOS",
            "desc": "Empresários e sindicatos oferecem doações. TSE exige transparência total. Doações acima de R$ 10k precisam de declaração pública.",
            "icon": "💰", "tipo": "financas", "impacto": "alto", "duracao": 1, "armadilha": True,
            "opcoes": [
                {"texto": "Aceitar doações dentro dos limites legais com transparência", "desc": "Reforça caixa, mas exige prestação de contas pública.", "efeito": {"pop": 3, "caixa": 35000, "energia": -12, "midia": 8, "risco": 8}, "cond": {}, "armadilha": False, "dica": "✅ Financeiro: Recursos para campanha. ✅ Jurídico: Dentro da lei."},
                {"texto": "Recusar doações de grandes empresas para evitar vínculos", "desc": "Mantém imagem limpa, mas limita recursos para propaganda.", "efeito": {"pop": 7, "caixa": -5000, "energia": -8, "midia": 12, "risco": 4}, "cond": {}, "armadilha": False, "dica": "✅ Comunicação: Imagem de independência. ⚠️ Financeiro: Menos recursos."},
                {"texto": "Aceitar doações 'por baixo dos panos' para evitar exposição", "desc": "ARMADILHA PERIGOSA: Pode resolver caixa, mas risco jurídico altíssimo se descoberto.", "efeito": {"pop": -5, "caixa": 50000, "energia": -15, "midia": -10, "risco": 45}, "cond": {}, "armadilha": True, "dica": "🚨 Jurídico: Crime eleitoral. Se descoberto, cassação certa."},
                {"texto": "Focar em vaquinha online com pequenos doadores", "desc": "Democrático e transparente, mas arrecadação mais lenta.", "efeito": {"pop": 8, "caixa": 15000, "energia": -20, "midia": 15, "risco": 3}, "cond": {"midia_min": 40}, "armadilha": False, "dica": "✅ Comunicação: Engajamento digital. ⚠️ Tempo: Arrecadação gradual."},
            ]
        },
        
        # === SAÚDE E EDUCAÇÃO ===
        {
            "id": "crise_saude_1", "categoria": "saude",
            "titulo": "🏥 CRISE DE SAÚDE: HOSPITAIS EM COLAPSO",
            "desc": "Novo surto de doença respiratória sobrecarrega sistema. UTIs com 98% de ocupação, fila de vacinação com 2 meses de espera.",
            "icon": "🏥", "tipo": "saude", "impacto": "alto", "duracao": 2, "armadilha": False,
            "opcoes": [
                {"texto": "Visitar hospitais pessoalmente e conversar com famílias", "desc": "Humaniza imagem, mas há risco de contágio e consome energia crítica.", "efeito": {"pop": 12, "caixa": -6000, "energia": -40, "midia": 10, "risco": 18}, "cond": {"energia_min": 55}, "armadilha": False, "dica": "✅ Comunicação: Imagem humanizada. ⚠️ Energia: Custo muito alto."},
                {"texto": "Anunciar verba emergencial de R$ 8 bilhões para saúde", "desc": "Ação concreta e mensurável. Caro, mas eficaz e transparente.", "efeito": {"pop": 10, "caixa": -32000, "energia": -18, "midia": 14, "risco": 6}, "cond": {"caixa_min": 70000}, "armadilha": False, "dica": "✅ Financeiro: Investimento visível. ✅ Estratégico: Ação concreta."},
                {"texto": "Convocar coletiva com cientistas e apresentar plano técnico", "desc": "Mostra competência técnica, mas pode parecer frio em momento emocional.", "efeito": {"pop": 6, "caixa": -4000, "energia": -24, "midia": 18, "risco": 4}, "cond": {}, "armadilha": False, "dica": "✅ Mídia: Transparência técnica. ⚠️ Emoção: Pode parecer distante."},
                {"texto": "Culpar gestão anterior e prometer investigação de responsabilidades", "desc": "ARMADILHA: Político mas insensível com vítimas. Alto risco de backfire.", "efeito": {"pop": -10, "caixa": 0, "energia": -12, "midia": -14, "risco": 24}, "cond": {}, "armadilha": True, "dica": "🚨 Comunicação: Pode parecer que está se aproveitando da tragédia."},
            ]
        },
        {
            "id": "educacao_pisa", "categoria": "educacao",
            "titulo": "🎓 RESULTADO DO PISA: BRASIL ENTRE OS PIORES",
            "desc": "Brasil ocupa 63º lugar em leitura, 66º em matemática. Professores e pais cobram posicionamento sobre educação básica.",
            "icon": "🎓", "tipo": "educacao", "impacto": "alto", "duracao": 2, "armadilha": False,
            "opcoes": [
                {"texto": "Anunciar aumento de 30% no salário de professores", "desc": "Popular com categoria, mas impacto fiscal significativo.", "efeito": {"pop": 11, "caixa": -28000, "energia": -18, "midia": 12, "risco": 10}, "cond": {"caixa_min": 60000}, "armadilha": False, "dica": "✅ Base: Professores mobilizados. ⚠️ Financeiro: Custo recorrente alto."},
                {"texto": "Propor reforma do ensino médio com foco em técnico", "desc": "Alinhado com demanda do mercado, mas mudança leva tempo.", "efeito": {"pop": 6, "caixa": -15000, "energia": -22, "midia": 10, "risco": 8}, "cond": {}, "armadilha": False, "dica": "✅ Estratégico: Solução de longo prazo. ⚠️ Popular: Resultados demoram."},
                {"texto": "Focar em tecnologia: tablets e internet em todas as escolas", "desc": "Moderno e visível, mas não resolve problemas estruturais.", "efeito": {"pop": 8, "caixa": -22000, "energia": -20, "midia": 14, "risco": 12}, "cond": {}, "armadilha": False, "dica": "✅ Comunicação: Proposta visível. ⚠️ Estratégico: Pode ser visto como paliativo."},
                {"texto": "Privatizar gestão de escolas públicas via concessão", "desc": "ARMADILHA: Polêmico. Pode agradar empresários, mas irrita sindicatos.", "efeito": {"pop": -12, "caixa": 18000, "energia": -25, "midia": -8, "risco": 28}, "cond": {}, "armadilha": True, "dica": "🚨 Político: Pode dividir base e gerar oposição forte."},
            ]
        },
        
        # === SEGURANÇA E JUSTIÇA ===
        {
            "id": "seguranca_publica_1", "categoria": "seguranca",
            "titulo": "🔫 ONDA DE VIOLÊNCIA: POPULAÇÃO EXIGE AÇÕES",
            "desc": "Série de assaltos violentos e homicídios choca o país. Famílias de vítimas protestam. 76% citam segurança como prioridade #1.",
            "icon": "🔫", "tipo": "seguranca", "impacto": "alto", "duracao": 2, "armadilha": False,
            "opcoes": [
                {"texto": "Anunciar investimento massivo em policiamento ostensivo", "desc": "Muito popular, mas caro. Resultados levam tempo para aparecer.", "efeito": {"pop": 12, "caixa": -35000, "energia": -24, "midia": 10, "risco": 10}, "cond": {"caixa_min": 80000}, "armadilha": False, "dica": "✅ Estratégico: Popular e concreto. ⚠️ Financeiro: Custo muito alto."},
                {"texto": "Propor intervenção federal em estados com crise de segurança", "desc": "Medida extrema. Popular, mas questionada constitucionalmente por especialistas.", "efeito": {"pop": 10, "caixa": -40000, "energia": -35, "midia": 14, "risco": 26}, "cond": {}, "armadilha": False, "dica": "✅ Popular: Medida forte. ⚠️ Jurídico: Pode ser contestada no STF."},
                {"texto": "Focar em prevenção social e inteligência policial", "desc": "Abordagem técnica e de longo prazo. Menos popular, mas sustentável.", "efeito": {"pop": 5, "caixa": -24000, "energia": -28, "midia": 12, "risco": 6}, "cond": {}, "armadilha": False, "dica": "✅ Estratégico: Solução sustentável. ⚠️ Popular: Resultados demoram."},
                {"texto": "Culpar governo anterior e prometer 'mão firme'", "desc": "ARMADILHA: Fácil politicamente, mas pode parecer evasivo sem ações concretas.", "efeito": {"pop": 6, "caixa": 0, "energia": -14, "midia": -6, "risco": 18}, "cond": {}, "armadilha": True, "dica": "⚠️ Comunicação: Pode parecer discurso vazio sem ações."},
            ]
        },
        {
            "id": "reforma_penal", "categoria": "justica",
            "titulo": "⚖️ REFORMA PENAL EM DEBATE NO CONGRESSO",
            "desc": "Proposta de endurecimento de penas divide opinião. Defensores de direitos humanos e familiares de vítimas cobram posição.",
            "icon": "⚖️", "tipo": "justica", "impacto": "alto", "duracao": 2, "armadilha": True,
            "opcoes": [
                {"texto": "Apoiar endurecimento de penas para crimes violentos", "desc": "Popular com maioria, mas pode aumentar superlotação carcerária.", "efeito": {"pop": 10, "caixa": -5000, "energia": -18, "midia": 6, "risco": 14}, "cond": {}, "armadilha": False, "dica": "✅ Popular: Atende demanda pública. ⚠️ Estratégico: Pode não resolver causa raiz."},
                {"texto": "Propor foco em reinserção social e redução de reincidência", "desc": "Abordagem técnica, mas pode parecer 'brando com criminosos'.", "efeito": {"pop": -6, "caixa": -12000, "energia": -22, "midia": 12, "risco": 8}, "cond": {}, "armadilha": False, "dica": "✅ Estratégico: Solução de longo prazo. ⚠️ Popular: Pode ser mal interpretado."},
                {"texto": "Manter posição neutra e aguardar relatório técnico", "desc": "ARMADILHA: Seguro, mas pode parecer omisso em tema sensível.", "efeito": {"pop": -4, "caixa": 0, "energia": -10, "midia": -5, "risco": 10}, "cond": {}, "armadilha": True, "dica": "⚠️ Comunicação: Pode perder oportunidade de liderança no debate."},
            ]
        },
        
        # === MEIO AMBIENTE E AGRO ===
        {
            "id": "amazonia_internacional", "categoria": "ambiente",
            "titulo": "🌳 AMAZÔNIA: PRESSÃO INTERNACIONAL CRÍTICA",
            "desc": "Imagens de satélite da NASA mostram +52% nas queimadas. UE ameaça bloquear acordo comercial. Investidores reavaliam Brasil.",
            "icon": "🌳", "tipo": "ambiente", "impacto": "alto", "duracao": 1, "armadilha": True,
            "opcoes": [
                {"texto": "Enviar tropas e IBAMA para fiscalização imediata", "desc": "Ação firme agrada ambientalistas, mas irrita ruralistas da coalizão.", "efeito": {"pop": 9, "caixa": -24000, "energia": -28, "midia": 15, "risco": 18, "coalizao": -10}, "cond": {}, "armadilha": False, "dica": "✅ Mídia: Imagem internacional. ⚠️ Coalizão: Ruralistas podem abandonar."},
                {"texto": "Negociar com governadores plano de desenvolvimento sustentável", "desc": "Solução política equilibrada, mas ação parece lenta para urgência.", "efeito": {"pop": 4, "caixa": -10000, "energia": -24, "midia": 7, "risco": 10, "coalizao": 8}, "cond": {}, "armadilha": False, "dica": "✅ Político: Mantém aliados. ⚠️ Mídia: Pode parecer inação."},
                {"texto": "Propor fundo internacional de US$ 3 bilhões para preservação", "desc": "ARMADILHA: Solução criativa, mas depende de aprovação externa incerta.", "efeito": {"pop": 7, "caixa": 18000, "energia": -24, "midia": 18, "risco": 14}, "cond": {"midia_min": 55}, "armadilha": True, "dica": "⚠️ Estratégico: Se aprovado, ótimo. Se não, parece promessa vazia."},
                {"texto": "Priorizar desenvolvimento econômico da região com salvaguardas", "desc": "ARMADILHA: Discurso equilibrado, mas vago. Pode não satisfazer nenhum lado.", "efeito": {"pop": 1, "caixa": -6000, "energia": -18, "midia": 2, "risco": 16}, "cond": {}, "armadilha": True, "dica": "⚠️ Comunicação: Pode ser interpretado como 'ficar em cima do muro'."},
            ]
        },
        {
            "id": "agro_exportacao", "categoria": "agro",
            "titulo": "🌾 AGRONEGÓCIO: OPORTUNIDADES DE EXPORTAÇÃO",
            "desc": "China e UE buscam aumentar importações de soja e carne. Produtores rurais cobram apoio para infraestrutura logística.",
            "icon": "🌾", "tipo": "agro", "impacto": "alto", "duracao": 1, "armadilha": False,
            "opcoes": [
                {"texto": "Anunciar investimento em ferrovias e portos para escoamento", "desc": "Atende demanda do agro, mas custo elevado e prazo longo.", "efeito": {"pop": 7, "caixa": -30000, "energia": -22, "midia": 10, "risco": 8}, "cond": {"caixa_min": 70000}, "armadilha": False, "dica": "✅ Base rural: Atende demanda. ⚠️ Financeiro: Investimento de longo prazo."},
                {"texto": "Simplificar licenciamento ambiental para obras de infraestrutura", "desc": "Acelera obras, mas pode gerar críticas de ambientalistas.", "efeito": {"pop": 5, "caixa": -8000, "energia": -15, "midia": -6, "risco": 18}, "cond": {}, "armadilha": False, "dica": "✅ Agro: Agilidade. ⚠️ Ambiente: Pode gerar oposição."},
                {"texto": "Focar em agricultura familiar e sustentabilidade", "desc": "Equilibra interesses, mas pode não atender demanda por escala.", "efeito": {"pop": 6, "caixa": -15000, "energia": -18, "midia": 8, "risco": 10}, "cond": {}, "armadilha": False, "dica": "✅ Comunicação: Mensagem equilibrada. ⚠️ Agro: Pode achar insuficiente."},
            ]
        },
        
        # === POLÍTICA E ALIANÇAS ===
        {
            "id": "alianca_premium", "categoria": "politica",
            "titulo": "🤝 PROPOSTA DE ALIANÇA DECISIVA",
            "desc": "Partido com 72 deputados e 9 governadores oferece apoio formal. Em troca: 6 ministérios, R$ 250M em emendas, veto a 3 projetos.",
            "icon": "🤝", "tipo": "politica", "impacto": "alto", "duracao": 1, "armadilha": True,
            "opcoes": [
                {"texto": "Aceitar todas as exigências e fechar aliança imediatamente", "desc": "Apoio político imediato, mas esvazia caixa e irrita base ideológica.", "efeito": {"pop": -6, "caixa": 30000, "energia": -18, "midia": -10, "risco": 24, "coalizao": 18}, "cond": {}, "armadilha": False, "dica": "✅ Político: Base parlamentar fortalecida. ⚠️ Base: Pode sentir traição."},
                {"texto": "Negociar: 4 ministérios e R$ 120 milhões", "desc": "Meio-termo arriscado. Podem aceitar ou recusar e ficar inimigos.", "efeito": {"pop": 3, "caixa": 15000, "energia": -24, "midia": 4, "risco": 18, "coalizao": 10}, "cond": {}, "armadilha": False, "dica": "✅ Estratégico: Equilíbrio. ⚠️ Risco: Podem recusar e fechar com adversário."},
                {"texto": "Recusar mantendo coerência programática", "desc": "ARMADILHA: Mantém imagem limpa, mas pode perder apoio crucial para vencer.", "efeito": {"pop": 10, "caixa": 0, "energia": 6, "midia": 15, "risco": 6, "coalizao": -14}, "cond": {}, "armadilha": True, "dica": "✅ Comunicação: Imagem de integridade. ⚠️ Estratégico: Pode custar eleição."},
                {"texto": "Pedir tempo para consultar base do partido e militância", "desc": "Adia decisão mas pode parecer indeciso. Eles podem fechar com adversário.", "efeito": {"pop": -1, "caixa": 0, "energia": -10, "midia": -4, "risco": 22, "coalizao": -6}, "cond": {}, "armadilha": False, "dica": "⚠️ Estratégico: Perde timing. Pode perder a oportunidade."},
            ]
        },
        {
            "id": "reforma_politica", "categoria": "politica",
            "titulo": "⚖️ REFORMA DO SISTEMA ELEITORAL EM VOTAÇÃO",
            "desc": "Congresso vota mudança no sistema eleitoral. Sua posição pode definir o futuro da política brasileira por décadas.",
            "icon": "⚖️", "tipo": "politica", "impacto": "alto", "duracao": 2, "armadilha": False,
            "opcoes": [
                {"texto": "Apoiar reforma completa e imediata do sistema", "desc": "Imagem de reformador, mas cria inimigos no establishment político.", "efeito": {"pop": 10, "caixa": -10000, "energia": -28, "midia": 15, "risco": 24}, "cond": {}, "armadilha": False, "dica": "✅ Mídia: Imagem de mudança. ⚠️ Político: Cria oposição no Congresso."},
                {"texto": "Propor reforma gradual em 4 anos com amplo debate", "desc": "Prudência elogiada por analistas, mas pode parecer falta de coragem.", "efeito": {"pop": 5, "caixa": -4000, "energia": -22, "midia": 8, "risco": 12}, "cond": {}, "armadilha": False, "dica": "✅ Estratégico: Equilíbrio. ⚠️ Reformistas: Pode achar lento demais."},
                {"texto": "Manter sistema atual com ajustes menores", "desc": "ARMADILHA: Seguro para aliados, mas perde imagem de agente de mudança.", "efeito": {"pop": -6, "caixa": 6000, "energia": -12, "midia": -10, "risco": 10}, "cond": {}, "armadilha": True, "dica": "⚠️ Comunicação: Pode parecer conservador demais para eleitor de mudança."},
            ]
        },
        
        # === INFRAESTRUTURA E DESENVOLVIMENTO ===
        {
            "id": "infraestrutura_obras", "categoria": "infra",
            "titulo": "🏗️ PAC DE INFRAESTRUTURA: OBRAS PARADAS",
            "desc": "Milhares de obras paralisadas por falta de recursos. Prefeitos e governadores cobram liberação de verbas.",
            "icon": "🏗️", "tipo": "infra", "impacto": "alto", "duracao": 2, "armadilha": False,
            "opcoes": [
                {"texto": "Liberar verbas emergenciais para obras prioritárias", "desc": "Atende demanda local, mas drena caixa da campanha.", "efeito": {"pop": 9, "caixa": -28000, "energia": -20, "midia": 10, "risco": 8}, "cond": {"caixa_min": 60000}, "armadilha": False, "dica": "✅ Regional: Atende demanda local. ⚠️ Financeiro: Custo significativo."},
                {"texto": "Priorizar obras via Parcerias Público-Privadas (PPPs)", "desc": "Atrai investimento privado, mas processo é burocrático e lento.", "efeito": {"pop": 5, "caixa": 8000, "energia": -25, "midia": 8, "risco": 12}, "cond": {}, "armadilha": False, "dica": "✅ Financeiro: Menos custo direto. ⚠️ Tempo: Resultados demoram."},
                {"texto": "Focar em manutenção de obras existentes antes de novas", "desc": "Pragmático, mas pode parecer falta de ambição para eleitores.", "efeito": {"pop": 3, "caixa": -12000, "energia": -15, "midia": 5, "risco": 6}, "cond": {}, "armadilha": False, "dica": "✅ Estratégico: Uso eficiente de recursos. ⚠️ Comunicação: Pode parecer pouco visionário."},
            ]
        },
        
        # === TECNOLOGIA E INOVAÇÃO ===
        {
            "id": "tech_inovacao", "categoria": "tech",
            "titulo": "💻 TECNOLOGIA: BRASIL PRECISA SE MODERNIZAR",
            "desc": "Startups brasileiras buscam apoio. Setor de TI cobra incentivos fiscais. Jovens eleitores cobram agenda digital.",
            "icon": "💻", "tipo": "tech", "impacto": "medio", "duracao": 1, "armadilha": False,
            "opcoes": [
                {"texto": "Anunciar incentivos fiscais para startups e inovação", "desc": "Atrai jovens e setor de tecnologia, mas reduz arrecadação.", "efeito": {"pop": 8, "caixa": -10000, "energia": -18, "midia": 12, "risco": 8}, "cond": {}, "armadilha": False, "dica": "✅ Jovens: Agenda moderna. ⚠️ Financeiro: Menos arrecadação."},
                {"texto": "Focar em inclusão digital: internet gratuita em áreas carentes", "desc": "Popular e social, mas custo de implementação elevado.", "efeito": {"pop": 10, "caixa": -22000, "energia": -22, "midia": 14, "risco": 6}, "cond": {"caixa_min": 50000}, "armadilha": False, "dica": "✅ Social: Inclusão digital. ⚠️ Financeiro: Custo recorrente."},
                {"texto": "Manter políticas atuais e focar em outras prioridades", "desc": "Seguro, mas pode perder engajamento com eleitores jovens.", "efeito": {"pop": -4, "caixa": 0, "energia": -8, "midia": -6, "risco": 8}, "cond": {}, "armadilha": False, "dica": "⚠️ Estratégico: Pode perder conexão com eleitores de 18-35 anos."},
            ]
        },
        
        # === EVENTOS ESPECÍFICOS POR IDEOLOGIA ===
        # Esquerda
        {
            "id": "nacionalizacao_esq", "categoria": "economia", "ideologia": "esquerda",
            "titulo": "🏛️ RESERVA ESTRATÉGICA: MINERAIS RAROS",
            "desc": "Geólogos descobriram grande reserva de minerais raros. Empresas estrangeiras fazem ofertas bilionárias.",
            "icon": "🏛️", "tipo": "economia", "impacto": "crítico", "duracao": 2, "armadilha": True,
            "opcoes": [
                {"texto": "Defender monopólio estatal total da exploração", "desc": "Base progressista apoia, mas mercado reage com fuga de investimentos.", "efeito": {"pop": 18, "caixa": -18000, "energia": -30, "midia": 10, "risco": 22}, "cond": {}, "armadilha": False, "dica": "✅ Base: Soberania nacional. ⚠️ Mercado: Pode afastar investimentos."},
                {"texto": "Parceria com maioria estatal (51%) e privada (49%)", "desc": "ARMADILHA: Meio-termo que pode não satisfazer base purista nem mercado.", "efeito": {"pop": 7, "caixa": 24000, "energia": -24, "midia": 6, "risco": 14}, "cond": {}, "armadilha": True, "dica": "⚠️ Base: Pode achar traição. ⚠️ Mercado: Pode achar insuficiente."},
                {"texto": "Leilão total para iniciativa privada com royalties", "desc": "ARMADILHA PERIGOSA: Mercado celebra, mas base progressista considera traição.", "efeito": {"pop": -24, "caixa": 48000, "energia": -18, "midia": -18, "risco": 35}, "cond": {}, "armadilha": True, "dica": "🚨 Base: Pode abandonar campanha. ⚠️ Caixa: Ganho financeiro imediato."},
            ]
        },
        # Centro
        {
            "id": "reforma_centro", "categoria": "politica", "ideologia": "centro",
            "titulo": "⚖️ REFORMA ADMINISTRATIVA: ESTADO EFICIENTE",
            "desc": "Proposta de modernização do estado divide opinião. Servidores públicos e contribuintes cobram posicionamento.",
            "icon": "⚙️", "tipo": "politica", "impacto": "alto", "duracao": 2, "armadilha": False,
            "opcoes": [
                {"texto": "Propor digitalização e redução de burocracia", "desc": "Popular com contribuintes, mas servidores podem se opor.", "efeito": {"pop": 7, "caixa": -8000, "energia": -22, "midia": 10, "risco": 12}, "cond": {}, "armadilha": False, "dica": "✅ Contribuintes: Menos burocracia. ⚠️ Servidores: Pode gerar resistência."},
                {"texto": "Manter estrutura atual com ajustes pontuais", "desc": "Seguro, mas pode parecer falta de coragem reformista.", "efeito": {"pop": 2, "caixa": 0, "energia": -12, "midia": -5, "risco": 8}, "cond": {}, "armadilha": False, "dica": "⚠️ Comunicação: Pode parecer conservador para eleitor de mudança."},
                {"texto": "Propor avaliação de desempenho e meritocracia", "desc": "ARMADILHA: Pode ser visto como ataque a servidores públicos.", "efeito": {"pop": -8, "caixa": 5000, "energia": -20, "midia": 4, "risco": 20}, "cond": {}, "armadilha": True, "dica": "🚨 Base: Servidores podem mobilizar oposição."},
            ]
        },
        # Direita
        {
            "id": "privatizacao_dir", "categoria": "economia", "ideologia": "direita",
            "titulo": "💼 CARTEIRA DE PRIVATIZAÇÕES PRONTA",
            "desc": "Equipe preparou lista de 18 estatais. Estimativa: R$ 220 bilhões. Sindicatos já anunciaram oposição.",
            "icon": "💼", "tipo": "economia", "impacto": "crítico", "duracao": 2, "armadilha": True,
            "opcoes": [
                {"texto": "Acelerar todas as privatizações imediatamente", "desc": "Mercado celebra, mas sindicatos fazem oposição ferrenha.", "efeito": {"pop": 12, "caixa": 58000, "energia": -35, "midia": 10, "risco": 28}, "cond": {}, "armadilha": False, "dica": "✅ Mercado: Reação muito positiva. ⚠️ Sindicatos: Oposição ativa."},
                {"texto": "Privatizar apenas estatais deficitárias", "desc": "ARMADILHA: Seletivo. Menos impacto, mas também menos oposição.", "efeito": {"pop": 6, "caixa": 24000, "energia": -24, "midia": 6, "risco": 18}, "cond": {}, "armadilha": True, "dica": "⚠️ Mercado: Pode achar insuficiente. ⚠️ Estratégico: Meio-termo arriscado."},
                {"texto": "Congelar privatizações até após eleição", "desc": "ARMADILHA PERIGOSA: Adia polêmica, mas base econômica fica frustrada.", "efeito": {"pop": -10, "caixa": 0, "energia": -12, "midia": -12, "risco": 22}, "cond": {}, "armadilha": True, "dica": "🚨 Base econômica: Pode sentir traição. ⚠️ Estratégico: Perde momentum reformista."},
            ]
        },
    ],
}

# ============================================================================
# INICIALIZAÇÃO COMPLETA DO JOGO
# ============================================================================
def init_game(dificuldade="Normal"):
    """Inicializa TODAS as variáveis do jogo"""
    st.session_state.dia = 1
    st.session_state.total_dias = 45
    st.session_state.popularidade = 22.0
    st.session_state.caixa = 120000.00
    st.session_state.energia = 80
    st.session_state.midia = 45
    st.session_state.risco_escandalo = 12
    st.session_state.game_over = False
    st.session_state.vitoria = False
    st.session_state.msg_fim = ""
    st.session_state.evento_atual = None
    st.session_state.historico = []
    st.session_state.evolucao_pop = [22.0]
    st.session_state.evolucao_dias = [1]
    st.session_state.eventos_usados = []
    st.session_state.estados_support = {e: 20.0 + random.uniform(-5, 5) for e in ESTADOS_DECISIVOS}
    st.session_state.coalizao_apoio = {p: d["apoio_inicial"] for p, d in PARTIDOS_COALIZAO.items()}
    st.session_state.conquistas_unlocked = []
    st.session_state.new_achievements = []
    st.session_state.combo = 0
    st.session_state.max_combo = 0
    st.session_state.total_escandalos = 0
    st.session_state.total_doacoes = 0
    st.session_state.partido = st.session_state.get('partido', 'centro')
    st.session_state.dificuldade = dificuldade
    st.session_state.assessor_selecionado = "estrategista"
    st.session_state.mostrar_grafico = False
    
    # Ajustes por dificuldade
    if dificuldade == "Fácil":
        st.session_state.caixa = 180000; st.session_state.popularidade = 28; st.session_state.energia = 90; st.session_state.risco_escandalo = 8
    elif dificuldade == "Difícil":
        st.session_state.caixa = 80000; st.session_state.popularidade = 18; st.session_state.energia = 70; st.session_state.risco_escandalo = 20
    elif dificuldade == "HARDCORE":
        st.session_state.caixa = 60000; st.session_state.popularidade = 15; st.session_state.energia = 60; st.session_state.risco_escandalo = 30; st.session_state.total_dias = 40

def load_high_score():
    if 'high_score_data' not in st.session_state:
        st.session_state.high_score_data = {'score': 0, 'dia': 0, 'partido': 'Nenhum', 'data': 'N/A', 'dificuldade': 'Normal'}
    return st.session_state.high_score_data

def save_high_score(pop, dia, partido, dif):
    current = st.session_state.high_score_data
    if pop > current['score']:
        st.session_state.high_score_data = {'score': pop, 'dia': dia, 'partido': partido, 'data': datetime.now().strftime('%d/%m/%Y'), 'dificuldade': dif}
        return True
    return False

# ============================================================================
# LÓGICA DO JOGO
# ============================================================================
def get_assessor_advice(evento, idx):
    ass = ASSESSORES[st.session_state.assessor_selecionado]
    op = evento['opcoes'][idx]
    if random.random() < ass['confiabilidade']:
        if ass['especialidade'] == 'popularidade':
            if op['efeito']['pop'] > 6: return f"✅ {ass['nome']}: 'Pode aumentar significativamente sua popularidade.'"
            elif op['efeito']['pop'] < -6: return f"⚠️ {ass['nome']}: 'Pode prejudicar suas pesquisas.'"
            else: return f"➡️ {ass['nome']}: 'Impacto neutro na popularidade.'"
        elif ass['especialidade'] == 'caixa':
            if op['efeito']['caixa'] > 8000: return f"✅ {ass['nome']}: 'Melhora nossa situação financeira.'"
            elif op['efeito']['caixa'] < -15000: return f"⚠️ {ass['nome']}: 'Vai drenar recursos rapidamente.'"
            else: return f"➡️ {ass['nome']}: 'Impacto financeiro moderado.'"
        elif ass['especialidade'] == 'risco':
            r = op['efeito'].get('risco', 0)
            if r > 22: return f"🚨 {ass['nome']}: 'ALTO RISCO JURÍDICO detectado.'"
            elif r > 12: return f"⚠️ {ass['nome']}: 'Risco moderado. Proceda com cautela.'"
            else: return f"✅ {ass['nome']}: 'Risco jurídico aceitável.'"
        else:
            if op['efeito']['pop'] > 5: return f"✅ {ass['nome']}: 'Boa opção estrategicamente.'"
            elif op['efeito']['pop'] < -5: return f"⚠️ {ass['nome']}: 'Considere alternativas.'"
            else: return f"➡️ {ass['nome']}: 'Opção equilibrada.'"
    else:
        if op['efeito']['pop'] > 5: return f"⚠️ {ass['nome']}: 'Não recomendo esta opção.'"
        elif op['efeito']['pop'] < -5: return f"✅ {ass['nome']}: 'Esta opção pode funcionar.'"
        else: return f"➡️ {ass['nome']}: 'Qualquer escolha serve.'"

def check_condicoes(opcao):
    cond = opcao.get('cond', {})
    if 'pop_min' in cond and st.session_state.popularidade < cond['pop_min']: return False, f"Requer {cond['pop_min']}% pop"
    if 'caixa_min' in cond and st.session_state.caixa < cond['caixa_min']: return False, f"Requer R$ {cond['caixa_min']:,} caixa"
    if 'energia_min' in cond and st.session_state.energia < cond['energia_min']: return False, f"Requer {cond['energia_min']}% energia"
    if 'midia_min' in cond and st.session_state.midia < cond['midia_min']: return False, f"Requer {cond['midia_min']} mídia"
    if 'coalizao_min' in cond:
        media = sum(st.session_state.coalizao_apoio.values()) / len(st.session_state.coalizao_apoio)
        if media < cond['coalizao_min']: return False, "Requer apoio da coalizão"
    return True, ""

def aplicar_consequencias(opcao):
    bonus = {"pop": 0, "caixa": 0, "energia": 0, "midia": 0}
    if st.session_state.partido == "esquerda": bonus = {"pop": 1.2, "caixa": -600, "energia": 2.5, "midia": 1.0}
    elif st.session_state.partido == "centro": bonus = {"pop": 0, "caixa": 1200, "energia": 1.5, "midia": 2.0}
    elif st.session_state.partido == "direita": bonus = {"pop": -0.8, "caixa": 2200, "energia": 0, "midia": 0}
    
    mult = {"Fácil": 1.15, "Normal": 1.0, "Difícil": 0.82, "HARDCORE": 0.68}.get(st.session_state.dificuldade, 1.0)
    var = random.uniform(0.75, 1.25)
    
    ep = (opcao['efeito']['pop'] + bonus['pop']) * mult * var
    ec = (opcao['efeito']['caixa'] + bonus['caixa']) * mult * var
    ene = (opcao['efeito']['energia'] + bonus['energia']) * mult * var
    em = (opcao['efeito'].get('midia', 0) + bonus['midia']) * mult * var
    er = opcao['efeito'].get('risco', 0) * mult
    ecol = opcao['efeito'].get('coalizao', 0) * mult
    
    st.session_state.popularidade = max(0, min(100, st.session_state.popularidade + ep))
    st.session_state.caixa += ec
    st.session_state.energia = max(0, min(100, st.session_state.energia + ene))
    st.session_state.midia = max(0, min(100, st.session_state.midia + em))
    st.session_state.risco_escandalo = max(0, min(100, st.session_state.risco_escandalo + er))
    
    if ecol != 0:
        for p in st.session_state.coalizao_apoio:
            st.session_state.coalizao_apoio[p] = max(0, min(100, st.session_state.coalizao_apoio[p] + ecol * random.uniform(0.7, 1.3)))
    
    for est in st.session_state.estados_support:
        v = random.uniform(-4, 5) + (1.5 if ep > 0 else 0)
        st.session_state.estados_support[est] = max(0, min(100, st.session_state.estados_support[est] + v))
    
    if ep > 4: st.session_state.combo += 1; st.session_state.max_combo = max(st.session_state.max_combo, st.session_state.combo)
    else: st.session_state.combo = 0
    
    st.session_state.evolucao_pop.append(st.session_state.popularidade)
    st.session_state.evolucao_dias.append(st.session_state.dia)
    st.session_state.historico.append({'dia': st.session_state.dia, 'evento': st.session_state.evento_atual['titulo'][:60], 'pop': st.session_state.popularidade})
    
    if st.session_state.risco_escandalo >= 82:
        st.session_state.total_escandalos += 1
        st.session_state.risco_escandalo = 35
        st.session_state.popularidade -= 18
        st.session_state.midia -= 22
        st.error("🚨 ESCÂNDALO EXPLODIU! Popularidade -18%!")
    
    st.session_state.energia = min(100, st.session_state.energia + 4)
    st.session_state.caixa += bonus['caixa']
    if ec > 10000: st.session_state.total_doacoes += ec

def verificar_fim():
    if st.session_state.popularidade <= 4: st.session_state.game_over = True; st.session_state.vitoria = False; return "Popularidade ≤4%. Candidatura encerrada."
    if st.session_state.caixa <= 0: st.session_state.game_over = True; st.session_state.vitoria = False; return "Caixa zerado. TSE cassou candidatura."
    if st.session_state.energia <= 0: st.session_state.game_over = True; st.session_state.vitoria = False; return "Energia zerada. Hospitalizado."
    if st.session_state.midia <= 6: st.session_state.game_over = True; st.session_state.vitoria = False; return "Imprensa hostil destruiu imagem."
    if sum(st.session_state.coalizao_apoio.values())/len(st.session_state.coalizao_apoio) <= 22:
        st.session_state.game_over = True; st.session_state.vitoria = False; return "Coalizão desfeita. Sem apoio no Congresso."
    
    if st.session_state.dia > st.session_state.total_dias:
        st.session_state.game_over = True
        votos = sum(ESTADOS_DECISIVOS[e]['eleitores'] for e, a in st.session_state.estados_support.items() if a >= 45)
        total = sum(ESTADOS_DECISIVOS[e]['eleitores'] for e in ESTADOS_DECISIVOS)
        pct = (votos/total)*100
        if pct >= 52: st.session_state.vitoria = True; return f"🎉 VITÓRIA 1º TURNO! {pct:.1f}% dos votos!"
        elif pct >= 42: st.session_state.vitoria = True; return f"✅ 2º TURNO! {pct:.1f}% dos votos."
        else: st.session_state.vitoria = False; return f"❌ ELIMINADO! {pct:.1f}% dos votos."
    return None

def gerar_evento():
    if st.session_state.risco_escandalo >= 52 and random.random() < 0.35:
        crises = [e for e in EVENTOS['geral'] if e['tipo'] == 'crise' and e.get('ideologia') in [None, st.session_state.partido]]
        if crises:
            ev = random.choice(crises)
            if ev['id'] not in st.session_state.eventos_usados[-15:]:
                st.session_state.eventos_usados.append(ev['id']); return ev
    
    pool = [e for e in EVENTOS['geral'] if e.get('ideologia') in [None, st.session_state.partido]]
    disp = [e for e in pool if e['id'] not in st.session_state.eventos_usados[-15:]]
    if not disp: disp = pool; st.session_state.eventos_usados = []
    ev = random.choice(disp); st.session_state.eventos_usados.append(ev['id']); return ev

# ============================================================================
# GRÁFICOS
# ============================================================================
def grafico_evolucao():
    cor = {"esquerda": "#DC143C", "centro": "#FFD700", "direita": "#0066CC"}.get(st.session_state.partido, "#667eea")
    fig = go.Figure(go.Scatter(x=st.session_state.evolucao_dias, y=st.session_state.evolucao_pop, mode='lines+markers', line=dict(color=cor, width=4)))
    fig.add_hline(y=52, line_dash="dash", line_color="#00ff88"); fig.add_hline(y=42, line_dash="dash", line_color="#ffa500")
    fig.update_layout(title='📈 Popularidade', xaxis_title='Dia', yaxis_title='%', yaxis_range=[0,100], height=320, template='plotly_white')
    return fig

def grafico_estados():
    fig = go.Figure(go.Bar(x=list(st.session_state.estados_support.keys()), y=list(st.session_state.estados_support.values()),
        marker_color=[ESTADOS_DECISIVOS[e]['cor'] for e in st.session_state.estados_support]))
    fig.add_hline(y=45, line_dash="dash", line_color="#00ff88")
    fig.update_layout(title='🗺️ Estados', yaxis_range=[0,100], height=300, template='plotly_white', showlegend=False)
    return fig

# ============================================================================
# TELAS
# ============================================================================
def tela_inicial():
    st.markdown("<h1 style='text-align:center;font-size:48px;margin:0;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>🇧🇷 CANDIDATO 2026</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;font-size:18px;color:#666;margin:10px 0 30px'>Simulador Presidencial Premium</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("### 🎮 MECÂNICAS PREMIUM\n- 🎭 Consequências ocultas\n- 👥 5 assessores com confiabilidade variável\n- 🤝 Coalizão de 4 partidos\n- 🗺️ 8 estados decisivos\n- 💰 Sistema de doações TSE\n- 💣 Perguntas com armadilhas\n- 🚨 Escândalos ocultos")
        dif = st.radio("🎯 Dificuldade:", ["Fácil", "Normal", "Difícil", "HARDCORE"], label_visibility="collapsed")
        st.session_state.dif_temp = dif
    with c2:
        hs = load_high_score()
        st.markdown(f"### 🏆 Recorde\n<div class='metric-card'><h3>Maior Popularidade</h3><h1>{hs['score']:.1f}%</h1><p>{hs['partido']} | {hs['dificuldade']}</p></div>", unsafe_allow_html=True)
        st.write(f"🏅 Conquistas: {len(st.session_state.get('conquistas_unlocked',[]))}/{len(ACHIEVEMENTS)}")
    
    st.divider()
    st.markdown("### 🎭 Escolha Sua Ideologia")
    c1, c2, c3 = st.columns(3)
    
    def btn_partido(cor, icone, nome, sigla, bonus_pop, bonus_caixa, key):
        st.markdown(f"<div class='metric-card' style='background:linear-gradient(135deg,{cor},#333)'><h2 style='margin:0;font-size:40px'>{icone}</h2><h3>{nome}</h3><p style='font-size:13px'>{sigla}</p><hr style='border-color:rgba(255,255,255,0.3)'><p style='font-size:12px'>📈 Pop: {bonus_pop:+.1f}/decisão</p><p style='font-size:12px'>💰 Caixa: {bonus_caixa:+.0f}/dia</p></div>", unsafe_allow_html=True)
        if st.button(f"{icone} {nome}", key=key, use_container_width=True, type="primary"): return True
        return False
    
    with c1:
        if btn_partido("#DC143C", "🔴", "ESQUERDA", "Frente Progressista", 1.2, -600, "esq"):
            st.session_state.partido = "esquerda"; init_game(st.session_state.dif_temp); st.rerun()
    with c2:
        if btn_partido("#FFD700", "🟡", "CENTRO", "Aliança Democrática", 0, 1200, "cen"):
            st.session_state.partido = "centro"; init_game(st.session_state.dif_temp); st.rerun()
    with c3:
        if btn_partido("#0066CC", "🔵", "DIREITA", "Movimento Liberal", -0.8, 2200, "dir"):
            st.session_state.partido = "direita"; init_game(st.session_state.dif_temp); st.rerun()

def render_opcao(idx, opcao, evento):
    pode, motivo = check_condicoes(opcao)
    conselho = get_assessor_advice(evento, idx)
    classe = "trap" if opcao.get('armadilha') else "smart" if opcao['efeito']['pop'] > 8 else ""
    
    pop_s = "📈" if opcao['efeito']['pop'] > 0 else "📉" if opcao['efeito']['pop'] < 0 else "➡️"
    caixa_s = "💰" if opcao['efeito']['caixa'] > 0 else "💸" if opcao['efeito']['caixa'] < 0 else "➡️"
    ene_s = "⚡" if opcao['efeito']['energia'] > 0 else "🔋" if opcao['efeito']['energia'] < 0 else "➡️"
    
    st.markdown(f"""
    <div class="option-card {classe}">
        <div class="option-header">
            <div class="option-number">{idx+1}</div>
            <div class="option-title">{opcao['texto']}</div>
        </div>
        <div class="option-desc">{opcao['desc']}</div>
        <div class="option-advice"><strong>💡 Conselho:</strong> {conselho}</div>
        <div class="option-stats">
            <span class="stat-item {('stat-positive' if opcao['efeito']['pop']>0 else 'stat-negative' if opcao['efeito']['pop']<0 else 'stat-neutral')}">{pop_s} Pop: {opcao['efeito']['pop']:+}</span>
            <span class="stat-item {('stat-positive' if opcao['efeito']['caixa']>0 else 'stat-negative' if opcao['efeito']['caixa']<0 else 'stat-neutral')}">{caixa_s} Caixa: {opcao['efeito']['caixa']:+,}</span>
            <span class="stat-item {('stat-positive' if opcao['efeito']['energia']>0 else 'stat-negative' if opcao['efeito']['energia']<0 else 'stat-neutral')}">{ene_s} Energia: {opcao['efeito']['energia']:+}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if pode:
        if st.button(f"✅ Escolher Opção {idx+1}", key=f"opt_{idx}", use_container_width=True):
            aplicar_consequencias(opcao)
            st.session_state.evento_atual = None
            st.session_state.dia += 1
            msg = verificar_fim()
            if msg: st.session_state.msg_fim = msg
            st.rerun()
    else:
        st.button(f"🔒 Opção {idx+1} ({motivo})", key=f"opt_{idx}", use_container_width=True, disabled=True)

def tela_jogo():
    nome = {"esquerda": "🔴 Esquerda", "centro": "🟡 Centro", "direita": "🔵 Direita"}.get(st.session_state.partido, "")
    st.markdown(f"""<div class="game-header"><h2 style="margin:0;font-size:26px">🇧🇷 CAMPANHA PRESIDENCIAL 2026</h2><p style="margin:10px 0 0;font-size:15px;opacity:0.9">{nome} | Dia {st.session_state.dia}/{st.session_state.total_dias} | {st.session_state.dificuldade}</p></div>""", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("📊 Gráficos", use_container_width=True): st.session_state.mostrar_grafico = not st.session_state.mostrar_grafico
    with c2:
        if st.button("🔄 Reiniciar", use_container_width=True): st.session_state.partido = None; st.rerun()
    
    if st.session_state.risco_escandalo >= 62:
        st.markdown(f"""<div class="alert-box">🚨 ALERTA: Risco de escândalo {st.session_state.risco_escandalo:.0f}%</div>""", unsafe_allow_html=True)
    if st.session_state.combo >= 3:
        st.markdown(f"""<div style="text-align:center"><div class="combo-badge">🔥 COMBO x{st.session_state.combo}</div></div>""", unsafe_allow_html=True)
    
    # Stats
    c1, c2, c3, c4, c5 = st.columns(5)
    def stat_card(titulo, valor, sub, cor, prog):
        st.markdown(f"""<div class="metric-card" style="background:linear-gradient(135deg,{cor},#333)"><h3>{titulo}</h3><h1>{valor}</h1><p class="trend">{sub}</p></div>""", unsafe_allow_html=True)
        st.progress(prog)
    
    with c1: stat_card("📊 Popularidade", f"{st.session_state.popularidade:.1f}%", "Meta: 42%+", "#00ff88" if st.session_state.popularidade>=42 else "#ffa500" if st.session_state.popularidade>=25 else "#ff4757", st.session_state.popularidade/100)
    with c2: stat_card("💰 Caixa", f"R$ {st.session_state.caixa:,.0f}", "Saudável" if st.session_state.caixa>=80000 else "Atenção" if st.session_state.caixa>=35000 else "CRÍTICO", "#00ff88" if st.session_state.caixa>=80000 else "#ffa500" if st.session_state.caixa>=35000 else "#ff4757", min(st.session_state.caixa/250000,1))
    with c3: stat_card("⚡ Energia", f"{st.session_state.energia}%", "Bom" if st.session_state.energia>=55 else "Cansado" if st.session_state.energia>=30 else "EXAUSTO", "#00ff88" if st.session_state.energia>=55 else "#ffa500" if st.session_state.energia>=30 else "#ff4757", st.session_state.energia/100)
    with c4: stat_card("📰 Mídia", f"{st.session_state.midia:.0f}", "Favorável" if st.session_state.midia>=55 else "Neutra" if st.session_state.midia>=30 else "HOSTIL", "#00ff88" if st.session_state.midia>=55 else "#ffa500" if st.session_state.midia>=30 else "#ff4757", st.session_state.midia/100)
    with c5: stat_card("🚨 Risco", f"{st.session_state.risco_escandalo:.0f}%", "Seguro" if st.session_state.risco_escandalo<=30 else "Atenção" if st.session_state.risco_escandalo<=60 else "PERIGO", "#00ff88" if st.session_state.risco_escandalo<=30 else "#ffa500" if st.session_state.risco_escandalo<=60 else "#ff4757", st.session_state.risco_escandalo/100)
    
    st.divider()
    
    # Assessores
    st.markdown("### 👥 Assessores")
    cols = st.columns(5)
    for i, (k, a) in enumerate(ASSESSORES.items()):
        with cols[i]:
            sel = st.session_state.assessor_selecionado == k
            st.markdown(f"""<div class="advisor-card {'selected' if sel else ''}"><div style="font-size:24px">{a['icone']}</div><strong style="font-size:12px">{a['nome']}</strong><br><small>{a['cargo']}</small><br><small style="color:{a['cor']}">{a['confiabilidade']*100:.0f}%</small></div>""", unsafe_allow_html=True)
            if st.button("Selecionar", key=f"ass_{k}", use_container_width=True): st.session_state.assessor_selecionado = k; st.rerun()
    
    if st.session_state.mostrar_grafico:
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(grafico_evolucao(), use_container_width=True)
        with c2: st.plotly_chart(grafico_estados(), use_container_width=True)
        st.divider()
    
    if st.session_state.game_over:
        if st.session_state.vitoria:
            st.balloons()
            st.markdown(f"""<div class="victory-screen"><h1 style="margin:0;font-size:48px">🎉 VITÓRIA!</h1><p style="font-size:22px;margin:20px 0">{st.session_state.msg_fim}</p><p>Popularidade: <strong>{st.session_state.popularidade:.1f}%</strong></p></div>""", unsafe_allow_html=True)
            if save_high_score(st.session_state.popularidade, st.session_state.dia, st.session_state.partido, st.session_state.dificuldade): st.success("🏆 NOVO RECORDE!")
        else:
            st.markdown(f"""<div class="defeat-screen"><h1 style="margin:0;font-size:48px">😞 DERROTA</h1><p style="font-size:22px;margin:20px 0">{st.session_state.msg_fim}</p></div>""", unsafe_allow_html=True)
        
        if st.session_state.conquistas_unlocked:
            st.markdown("### 🏅 Conquistas")
            cols = st.columns(3)
            for i, aid in enumerate(st.session_state.conquistas_unlocked):
                a = ACHIEVEMENTS.get(aid, {})
                with cols[i%3]: st.markdown(f"""<div class="achievement-badge">{a.get('icon','🏆')} {a.get('name','?')}</div>""", unsafe_allow_html=True)
        
        if st.button("🎮 Jogar Novamente", use_container_width=True, type="primary"): st.session_state.partido = None; st.rerun()
    else:
        if st.session_state.evento_atual is None: st.session_state.evento_atual = gerar_evento()
        ev = st.session_state.evento_atual
        
        tags = f"""<div class="event-tags">
            <span class="tag impact">IMPACTO: {ev['impacto'].upper()}</span>
            <span class="tag duration">{ev['duracao']} DIAS</span>
            <span class="tag type">{ev['tipo'].upper()}</span>
            {'<span class="tag trap">💣 ARMADILHA</span>' if ev.get('armadilha') else ''}
        </div>"""
        
        st.markdown(f"""<div class="event-card {'crisis' if ev['tipo']=='crise' else 'opportunity' if ev['impacto']=='crítico' else ''}">
            <div style="font-size:48px;margin-bottom:12px">{ev['icon']}</div>
            <h2 style="margin:0 0 12px;color:#333;font-size:24px">{ev['titulo']}</h2>
            <div style="font-size:15px;color:#555;line-height:1.6">{ev['desc']}</div>
            {tags}
        </div>""", unsafe_allow_html=True)
        
        ass = ASSESSORES[st.session_state.assessor_selecionado]
        st.markdown(f"""<div class="hint-box"><strong>{ass['icone']} {ass['nome']}</strong> — {ass['descricao']}<br><small>Confiabilidade: {ass['confiabilidade']*100:.0f}% | Especialidade: {ass['especialidade']}</small></div>""", unsafe_allow_html=True)
        
        st.warning("⚠️ **Consequências OCULTAS!** Confie no assessor, analise o contexto e decida estrategicamente.")
        
        st.markdown('<div class="option-container">', unsafe_allow_html=True)
        for i, op in enumerate(ev['opcoes']): render_opcao(i, op, ev)
        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("💡 Dicas Estratégicas"):
            st.write("- Mantenha energia >30%, caixa >R$50k, mídia >30%\n- Coalizão média >55%, risco <60%\n- Precisa de 45% em cada estado para vencer\n- Assessores podem errar: nenhum é 100% confiável\n- Armadilhas: a escolha 'óbvia' nem sempre é a melhor")

def sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/ballot-box-with-ball.png", width=70)
        st.title("🎛️ Painel")
        if st.session_state.get('partido'):
            st.markdown(f"""<div style="background:linear-gradient(135deg,#1a1a2e,#16213e);padding:16px;border-radius:12px;color:white;margin-bottom:16px"><strong>🎭 Partido:</strong> {st.session_state.partido.upper()}<br><strong>🎯 Dificuldade:</strong> {st.session_state.dificuldade}</div>""", unsafe_allow_html=True)
            st.write("### 📊 Status"); st.write(f"📅 Dia: {st.session_state.dia}/{st.session_state.total_dias}"); st.write(f"📈 Pop: {st.session_state.popularidade:.1f}%"); st.write(f"💰 Caixa: R$ {st.session_state.caixa:,.0f}"); st.write(f"⚡ Energia: {st.session_state.energia}%"); st.write(f"📰 Mídia: {st.session_state.midia:.0f}"); st.write(f"🚨 Risco: {st.session_state.risco_escandalo:.0f}%")
            if st.session_state.popularidade<25: st.warning("⚠️ Pop crítica!"); 
            if st.session_state.caixa<40000: st.warning("⚠️ Caixa baixo!"); 
            if st.session_state.energia<35: st.warning("⚠️ Energia baixa!"); 
            if st.session_state.risco_escandalo>55: st.error("🚨 Risco alto!")
            if st.session_state.combo>=2: st.markdown(f"""<div style="background:linear-gradient(135deg,#f093fb,#f5576c);padding:10px;border-radius:10px;color:white;text-align:center;font-weight:600;margin:10px 0">🔥 Combo x{st.session_state.combo}</div>""", unsafe_allow_html=True)
            st.divider(); st.write("### 🤝 Coalizão")
            for p, a in st.session_state.coalizao_apoio.items(): st.write(f"{PARTIDOS_COALIZAO[p]['sigla']}: {a:.1f}%"); st.progress(a/100)
            st.divider(); st.write(f"### 🏅 Conquistas: {len(st.session_state.conquistas_unlocked)}/{len(ACHIEVEMENTS)}"); st.progress(len(st.session_state.conquistas_unlocked)/len(ACHIEVEMENTS))
        st.divider(); st.info("**📖 Como Jogar:**\n1. Escolha ideologia\n2. Selecione assessor\n3. Decida a cada dia\n4. Mantenha stats altos\n5. Vença com 42%+")

def check_achievements():
    new = []
    if st.session_state.dia>=2 and "first_decision" not in st.session_state.conquistas_unlocked: st.session_state.conquistas_unlocked.append("first_decision"); new.append("first_decision")
    if st.session_state.popularidade>=30 and "pop_rising" not in st.session_state.conquistas_unlocked: st.session_state.conquistas_unlocked.append("pop_rising"); new.append("pop_rising")
    if st.session_state.popularidade>=50 and "pop_leader" not in st.session_state.conquistas_unlocked: st.session_state.conquistas_unlocked.append("pop_leader"); new.append("pop_leader")
    if st.session_state.popularidade>=70 and "pop_legend" not in st.session_state.conquistas_unlocked: st.session_state.conquistas_unlocked.append("pop_legend"); new.append("pop_legend")
    if st.session_state.caixa>=500000 and "treasury_master" not in st.session_state.conquistas_unlocked: st.session_state.conquistas_unlocked.append("treasury_master"); new.append("treasury_master")
    if st.session_state.total_escandalos>=3 and "scandal_survivor" not in st.session_state.conquistas_unlocked: st.session_state.conquistas_unlocked.append("scandal_survivor"); new.append("scandal_survivor")
    if st.session_state.combo>=5 and "combo_king" not in st.session_state.conquistas_unlocked: st.session_state.conquistas_unlocked.append("combo_king"); new.append("combo_king")
    if sum(1 for v in st.session_state.estados_support.values() if v>=45)>=5 and "regional_champion" not in st.session_state.conquistas_unlocked: st.session_state.conquistas_unlocked.append("regional_champion"); new.append("regional_champion")
    if st.session_state.total_doacoes>=100000 and "donation_expert" not in st.session_state.conquistas_unlocked: st.session_state.conquistas_unlocked.append("donation_expert"); new.append("donation_expert")
    if st.session_state.midia>=70 and "media_master" not in st.session_state.conquistas_unlocked: st.session_state.conquistas_unlocked.append("media_master"); new.append("media_master")
    return new

def main():
    for v in ['partido','recorde_pop','mostrar_grafico','assessor_selecionado','conquistas_unlocked','new_achievements','combo','max_combo','total_escandalos','total_doacoes','high_score_data']:
        if v not in st.session_state:
            st.session_state[v] = None if v=='partido' else (0.0 if v=='recorde_pop' else (False if v in ['mostrar_grafico'] else ("estrategista" if v=='assessor_selecionado' else ([] if v in ['conquistas_unlocked','new_achievements'] else (0 if v in ['combo','max_combo','total_escandalos','total_doacoes'] else {'score':0,'dia':0,'partido':'Nenhum','data':'N/A','dificuldade':'Normal'})))))
    
    if st.session_state.partido and not all(v in st.session_state for v in ['dia','popularidade','caixa','energia','midia','risco_escandalo','game_over','vitoria','evento_atual','historico','evolucao_pop','evolucao_dias','dificuldade','eventos_usados','estados_support','coalizao_apoio']): init_game(st.session_state.get('dificuldade','Normal'))
    
    sidebar()
    if st.session_state.partido is None: tela_inicial()
    else:
        new_achs = check_achievements()
        for aid in new_achs:
            a = ACHIEVEMENTS.get(aid, {}); st.success(f"🏆 CONQUISTA: {a.get('icon','🏆')} {a.get('name','?')}!")
        tela_jogo()

if __name__ == "__main__": main()
