import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional

import plotly.graph_objects as go
import streamlit as st

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="🇧🇷 Candidato 2026: Viral Edition",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
)

random.seed()

# =========================================================
# STYLE
# =========================================================
STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%); }
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #1d4ed8 100%);
        border-radius: 24px;
        padding: 28px;
        color: white;
        box-shadow: 0 18px 50px rgba(15,23,42,.22);
        margin-bottom: 18px;
    }
    .hero h1 { margin: 0 0 6px 0; font-size: 2.1rem; }
    .hero p { margin: 0; opacity: .92; }
    .card {
        background: white;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 8px 26px rgba(15,23,42,.08);
        border: 1px solid rgba(99,102,241,.08);
    }
    .metric-card {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        color: white; padding: 16px; border-radius: 18px;
        min-height: 108px; box-shadow: 0 10px 28px rgba(0,0,0,.18);
    }
    .metric-card h4 { margin:0; opacity:.78; font-size:12px; text-transform: uppercase; letter-spacing: .08em; }
    .metric-card h2 { margin:10px 0 6px 0; font-size: 30px; }
    .metric-card span { font-size: 12px; opacity: .9; }
    .event-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-left: 8px solid #2563eb;
        border-radius: 22px; padding: 24px; box-shadow: 0 12px 34px rgba(15,23,42,.10);
        margin-bottom: 18px;
    }
    .event-crisis { border-left-color: #dc2626; }
    .event-good { border-left-color: #16a34a; }
    .tag {
        display:inline-block; padding:6px 10px; border-radius:999px; font-size:11px;
        font-weight:700; margin-right:6px; margin-top:8px;
    }
    .tag-blue { background:#dbeafe; color:#1d4ed8; }
    .tag-red { background:#fee2e2; color:#b91c1c; }
    .tag-green { background:#dcfce7; color:#166534; }
    .choice-box {
        background: #fff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 14px;
        box-shadow: 0 6px 18px rgba(15,23,42,.05); margin-bottom: 10px;
    }
    .choice-title { font-weight: 700; color:#111827; margin-bottom:6px; }
    .small-muted { color:#64748b; font-size: 13px; }
    .warning-strip {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white; padding: 14px 16px; border-radius: 14px; font-weight: 600;
    }
    .success-strip {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white; padding: 14px 16px; border-radius: 14px; font-weight: 600;
    }
    .advisor {
        background: white; border-radius: 16px; padding: 14px;
        border: 1px solid #e5e7eb; box-shadow: 0 6px 18px rgba(15,23,42,.05);
    }
    .achievement {
        display:inline-block; padding:8px 12px; border-radius:999px; margin:4px;
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%); color:white;
        font-size:12px; font-weight:700;
    }
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================
REGIOES = {
    "Norte": {"peso": 8, "perfil": "ambiental"},
    "Nordeste": {"peso": 27, "perfil": "social"},
    "Centro-Oeste": {"peso": 8, "perfil": "agro"},
    "Sudeste": {"peso": 42, "perfil": "mercado"},
    "Sul": {"peso": 15, "perfil": "agro"},
}

SEGMENTOS = {
    "periferia": {"peso": 18, "chave": "social"},
    "classe_media": {"peso": 18, "chave": "gestao"},
    "agro": {"peso": 12, "chave": "agro"},
    "evangelicos": {"peso": 14, "chave": "valores"},
    "jovens": {"peso": 12, "chave": "digital"},
    "servidores": {"peso": 11, "chave": "gestao"},
    "empreendedores": {"peso": 15, "chave": "mercado"},
}

ADVERSARIOS = {
    "populista": {"nome": "Ronaldo Falcão", "base": 26, "perfil": "digital", "rejeicao": 31},
    "tecnico": {"nome": "Marina Albuquerque", "base": 23, "perfil": "gestao", "rejeicao": 22},
    "maquina": {"nome": "César Prado", "base": 25, "perfil": "estrutura", "rejeicao": 28},
}

ASSESSORES = {
    "estrategista": {
        "nome": "Carlos Mendes",
        "icone": "🎯",
        "especialidade": "pesquisa",
        "bonus": {"narrativa": 2, "momentum": 1},
        "descricao": "Lê pesquisas, detecta swing e melhora decisões de timing.",
    },
    "financeiro": {
        "nome": "Ana Rodrigues",
        "icone": "💰",
        "especialidade": "arrecadacao",
        "bonus": {"caixa": 10000, "credibilidade": -1},
        "descricao": "Turbina caixa e negocia captação legal, mas pode soar fria.",
    },
    "comunicacao": {
        "nome": "Pedro Santos",
        "icone": "📰",
        "especialidade": "midia",
        "bonus": {"midia": 5, "viral": 8},
        "descricao": "Transforma bom momento em viral. Em crise, pode amplificar erro.",
    },
    "politico": {
        "nome": "Helena Costa",
        "icone": "🤝",
        "especialidade": "coalizao",
        "bonus": {"aliados": 8, "tempo_tv": 3},
        "descricao": "Abre portas em Brasília e protege sua governabilidade.",
    },
    "juridico": {
        "nome": "Roberto Lima",
        "icone": "⚖️",
        "especialidade": "compliance",
        "bonus": {"risco": -8, "credibilidade": 2},
        "descricao": "Evita cassação, enquadra propaganda e reduz dano em crise.",
    },
}

PARTIDOS = {
    "centro": {"nome": "Movimento de Centro", "slogan": "Gestão com equilíbrio"},
    "popular": {"nome": "Frente Popular", "slogan": "Povo em primeiro lugar"},
    "liberal": {"nome": "Aliança Liberal", "slogan": "Produzir, crescer e simplificar"},
    "verde": {"nome": "Rede Verde Brasil", "slogan": "Desenvolver sem destruir"},
}

ACHIEVEMENTS = {
    "primeiro_viral": "📲 Primeiro viral",
    "virou_o_jogo": "🔄 Virou o jogo",
    "caixa_forte": "💰 Caixa forte",
    "mestre_midia": "📰 Mestre da mídia",
    "blindado": "⚖️ Blindado",
    "furacao": "🔥 Furacão de campanha",
    "lider_nordeste": "🌵 Dominou o Nordeste",
    "lider_sudeste": "🏙️ Dominou o Sudeste",
    "sem_escandalo": "✨ Campanha limpa",
    "primeiro_turno": "🏆 Vitória no 1º turno",
}


@dataclass
class Option:
    text: str
    summary: str
    effects: Dict[str, float]
    requires: Optional[Dict[str, float]] = None
    risky: bool = False


@dataclass
class EventCard:
    id: str
    title: str
    desc: str
    category: str
    tone: str
    phase: str
    tags: List[str]
    options: List[Option]


EVENTS: List[EventCard] = [
    EventCard(
        id="debate_nacional",
        title="📺 Debate nacional em horário nobre",
        desc="Você enfrenta os três principais adversários ao vivo. Um corte certo pode te empurrar para o topo. Um tropeço vira meme por uma semana.",
        category="mídia",
        tone="neutral",
        phase="all",
        tags=["alto impacto", "tv", "viral"],
        options=[
            Option("Bater duro em corrupção e desperdício", "Mobiliza indignação e cresce entre classe média, mas aumenta rejeição.", {"intencao": 2.5, "rejeicao": 2.0, "midia": 6, "energia": -12, "credibilidade": 1, "narrativa": 2}),
            Option("Apresentar plano concreto e linguagem simples", "Menos espetáculo, mais consistência.", {"intencao": 1.8, "rejeicao": -0.8, "midia": 4, "energia": -10, "credibilidade": 4, "gestao": 5}),
            Option("Entrar no tom provocador da internet", "Pode explodir nas redes, mas também gerar fadiga e rejeição.", {"intencao": 2.0, "rejeicao": 3.0, "midia": 8, "energia": -9, "viral": 15, "digital": 4}, risky=True),
        ],
    ),
    EventCard(
        id="pesquisa_queda",
        title="📉 Nova pesquisa te coloca fora do 2º turno",
        desc="Institutos apontam estagnação e sua militância entra em modo pânico. O mercado e os influenciadores políticos começam a te abandonar.",
        category="pesquisa",
        tone="crisis",
        phase="early_mid",
        tags=["crise", "pesquisa", "pressão"],
        options=[
            Option("Trocar a narrativa e focar no custo de vida", "Reposiciona a campanha com pauta de bolso.", {"intencao": 2.8, "social": 7, "midia": 2, "caixa": -8000, "energia": -6}),
            Option("Dobrar a aposta no discurso técnico", "Ganha respeito, mas nem sempre gera voto.", {"credibilidade": 4, "gestao": 6, "midia": 1, "intencao": 0.6, "energia": -5}),
            Option("Atacar o instituto e gritar manipulação", "Engaja sua base, mas aumenta rejeição em moderados.", {"viral": 10, "intencao": 1.0, "rejeicao": 2.5, "credibilidade": -3, "midia": 5}, risky=True),
        ],
    ),
    EventCard(
        id="audio_vazado",
        title="📱 Áudio vazado no WhatsApp",
        desc="Um trecho de reunião interna sai do contexto e vira munição em grupos bolsonados, lulistas, isentões e páginas de fofoca política ao mesmo tempo.",
        category="crise",
        tone="crisis",
        phase="all",
        tags=["whatsapp", "vazamento", "narrativa"],
        options=[
            Option("Liberar o áudio completo e assumir o desgaste", "Transparência segura a credibilidade.", {"credibilidade": 5, "rejeicao": -1.0, "midia": 4, "energia": -6, "intencao": 0.8}),
            Option("Partir para o ataque jurídico e pedir derrubada", "Reduz risco futuro, mas não encerra a repercussão no mesmo dia.", {"risco": -8, "caixa": -12000, "midia": 2, "intencao": 0.4, "energia": -4}),
            Option("Fingir que nada aconteceu e subir hashtag positiva", "Pode funcionar por sorte, mas o risco é feio.", {"viral": 6, "midia": -3, "rejeicao": 2.0, "credibilidade": -4, "intencao": -0.8}, risky=True),
        ],
    ),
    EventCard(
        id="alianca_centrao",
        title="🤝 O centrão quer entrar na campanha",
        desc="Eles oferecem tempo de TV, prefeitos, prefeitas e capilaridade no interior. Em troca, cobram espaço e compromissos que podem irritar sua base.",
        category="política",
        tone="neutral",
        phase="mid",
        tags=["coalizão", "tempo de TV", "interior"],
        options=[
            Option("Fechar acordo e ampliar a estrutura", "Muito forte para capilaridade, com custo de coerência.", {"aliados": 12, "tempo_tv": 6, "intencao": 1.8, "credibilidade": -2, "rejeicao": 1.0, "caixa": 12000}),
            Option("Aceitar apoio sem loteamento pesado", "Negócio difícil, mas equilibrado.", {"aliados": 7, "tempo_tv": 4, "intencao": 1.2, "credibilidade": 1, "caixa": 5000}),
            Option("Recusar para preservar a narrativa", "Mantém pureza, mas perde máquina eleitoral.", {"credibilidade": 3, "narrativa": 3, "aliados": -8, "tempo_tv": -4, "intencao": -1.0}, risky=True),
        ],
    ),
    EventCard(
        id="greve_combustivel",
        title="⛽ Alta dos combustíveis domina o noticiário",
        desc="Motoristas, autônomos e famílias pressionam. Todo candidato está sendo cobrado por uma saída simples para um problema complicado.",
        category="economia",
        tone="crisis",
        phase="all",
        tags=["economia", "bolso", "urgência"],
        options=[
            Option("Anunciar pacote emergencial com foco em transporte e gás", "Popular, mas consome caixa político e financeiro.", {"intencao": 2.4, "social": 6, "caixa": -18000, "credibilidade": 1, "midia": 4}),
            Option("Defender reforma estrutural e previsibilidade fiscal", "Boa para mercado, menos sedutora para o povão.", {"mercado": 7, "credibilidade": 4, "intencao": 0.7, "midia": 2}),
            Option("Culpar adversários e fazer live indignada", "Funciona na base, mas pesa na rejeição.", {"viral": 12, "intencao": 1.0, "rejeicao": 1.8, "credibilidade": -2}, risky=True),
        ],
    ),
    EventCard(
        id="enchente_sudeste",
        title="🌧️ Enchentes em capitais do Sudeste",
        desc="A tragédia humanitária exige presença, empatia e proposta concreta. Não dá para parecer turista de crise.",
        category="social",
        tone="crisis",
        phase="all",
        tags=["tragédia", "Sudeste", "empatia"],
        options=[
            Option("Ir ao local com equipe técnica e anunciar reconstrução", "Ação forte se a comunicação não exagerar.", {"sudeste": 5, "intencao": 1.6, "credibilidade": 4, "caixa": -15000, "energia": -9}),
            Option("Priorizar fala institucional e coordenação federativa", "Menos emocional, mais responsável.", {"gestao": 6, "credibilidade": 3, "intencao": 1.0, "midia": 2}),
            Option("Transformar a tragédia em palanque contra rival", "Pode viralizar, mas pega muito mal.", {"viral": 8, "midia": 3, "rejeicao": 3.0, "credibilidade": -5, "intencao": -1.2}, risky=True),
        ],
    ),
    EventCard(
        id="apoio_governador_ne",
        title="🌵 Governador popular do Nordeste quer te apoiar",
        desc="O apoio pode te dar palanque e estrutura em cidades-chave, mas cobra prioridade para programas sociais e obras.",
        category="aliança",
        tone="good",
        phase="mid",
        tags=["Nordeste", "aliança", "estrutura"],
        options=[
            Option("Fechar apoio e assumir pauta social com força", "Excelente para Nordeste e periferia.", {"nordeste": 8, "social": 6, "aliados": 5, "intencao": 2.0, "caixa": -6000}),
            Option("Aceitar apoio, mas manter discurso mais amplo", "Equilíbrio nacional.", {"nordeste": 5, "intencao": 1.2, "credibilidade": 2, "aliados": 4}),
            Option("Evitar foto para não parecer regionalizado", "Estratégia fria demais para uma chance boa.", {"nordeste": -4, "credibilidade": 0, "intencao": -0.8}, risky=True),
        ],
    ),
    EventCard(
        id="pauta_agro",
        title="🌾 Lideranças do agro exigem posição clara",
        desc="Produtores cobram segurança jurídica, infraestrutura e resposta sobre embargo ambiental. Um aceno certo move o Centro-Oeste e parte do Sul.",
        category="agro",
        tone="neutral",
        phase="all",
        tags=["agro", "Centro-Oeste", "Sul"],
        options=[
            Option("Falar em produção com previsibilidade e licença rápida", "Agrada mercado e agro, mas gera ruído ambiental.", {"agro": 7, "mercado": 4, "centro-oeste": 5, "sul": 3, "rejeicao": 0.7}),
            Option("Defender produção com rastreabilidade e crédito verde", "Equilibrado e moderno.", {"agro": 4, "ambiental": 5, "credibilidade": 3, "intencao": 1.0}),
            Option("Atacar o setor para agradar nicho urbano", "Pode render aplauso online, mas custa caro no interior.", {"digital": 3, "agro": -8, "centro-oeste": -6, "sul": -4, "rejeicao": 1.5}, risky=True),
        ],
    ),
    EventCard(
        id="tiktok_jovem",
        title="🎵 Vídeo curto explode no TikTok",
        desc="Sua equipe descobriu um formato que humaniza sua imagem. Agora é decidir se vira onda ou vergonha alheia nacional.",
        category="digital",
        tone="good",
        phase="early_mid",
        tags=["TikTok", "jovens", "viral"],
        options=[
            Option("Entrar na trend com humor medido", "Boa chance de crescer com jovens sem parecer caricato.", {"digital": 8, "jovens": 6, "viral": 18, "intencao": 1.5, "credibilidade": 1}),
            Option("Usar o formato para explicar proposta em 30 segundos", "Menos meme, mais valor.", {"digital": 5, "gestao": 3, "credibilidade": 3, "intencao": 1.2}),
            Option("Forçar meme sem timing", "Clássico erro de político tentando ser cool.", {"viral": 10, "credibilidade": -5, "rejeicao": 2.2, "intencao": -0.6}, risky=True),
        ],
    ),
    EventCard(
        id="operacao_pf_aliado",
        title="🚨 Operação atinge aliado importante",
        desc="A Polícia Federal faz buscas em nomes ligados ao seu arco de apoio. A imprensa quer uma resposta em minutos, não em horas.",
        category="crise",
        tone="crisis",
        phase="all",
        tags=["PF", "escândalo", "risco jurídico"],
        options=[
            Option("Romper imediatamente e defender apuração total", "Dói na coalizão, mas blinda sua imagem.", {"credibilidade": 6, "risco": -10, "aliados": -8, "intencao": 1.3, "rejeicao": -1.0}),
            Option("Pedir cautela e aguardar investigação", "Mais político, menos contundente.", {"aliados": 2, "credibilidade": -1, "risco": 4, "intencao": -0.2}),
            Option("Defender o aliado e atacar a operação", "Muito perigoso.", {"aliados": 5, "credibilidade": -6, "risco": 14, "rejeicao": 3.5, "intencao": -1.8}, risky=True),
        ],
    ),
    EventCard(
        id="sabatina_jn",
        title="🎙️ Sabatina dura em TV nacional",
        desc="Perguntas secas, interrupções e pressão sobre números. Não basta carisma; precisa parecer presidenciável por inteiro.",
        category="mídia",
        tone="neutral",
        phase="late",
        tags=["entrevista", "credibilidade", "reta final"],
        options=[
            Option("Responder com precisão e reconhecer limites", "Passa seriedade e maturidade.", {"credibilidade": 5, "midia": 5, "intencao": 1.3, "rejeicao": -0.6}),
            Option("Buscar confronto com os jornalistas", "Pode incendiar a base, mas afastar indecisos.", {"viral": 12, "midia": 6, "rejeicao": 2.5, "intencao": 0.4}, risky=True),
            Option("Ser simpático e evitar tensão", "Seguro, porém pode parecer leve demais.", {"midia": 3, "intencao": 0.7, "credibilidade": 1}),
        ],
    ),
    EventCard(
        id="direito_resposta",
        title="⚖️ TSE concede direito de resposta",
        desc="Você venceu uma disputa sobre propaganda enganosa. O momento é bom, mas exagerar no tom pode virar arrogância.",
        category="jurídico",
        tone="good",
        phase="late",
        tags=["TSE", "justiça eleitoral", "oportunidade"],
        options=[
            Option("Usar o espaço para desmontar fake news com calma", "Excelente para confiança.", {"credibilidade": 5, "risco": -6, "midia": 3, "intencao": 1.1}),
            Option("Transformar a vitória em peça agressiva", "Pode render corte, mas eleva fadiga.", {"viral": 7, "intencao": 0.8, "rejeicao": 1.2}),
            Option("Fazer fala institucional curta e elegante", "Menos impacto, mais classe.", {"credibilidade": 3, "rejeicao": -0.4, "intencao": 0.6}),
        ],
    ),
    EventCard(
        id="apagao_regional",
        title="💡 Apagão atinge cidades estratégicas",
        desc="A crise mexe com comércio, segurança e humor do eleitor. Sua resposta precisa parecer de presidente, não de comentarista de rede social.",
        category="infraestrutura",
        tone="crisis",
        phase="all",
        tags=["crise", "segurança", "serviços"],
        options=[
            Option("Cobrar plano emergencial e reconstrução da rede", "Postura firme e prática.", {"gestao": 6, "intencao": 1.3, "credibilidade": 2, "energia": -5}),
            Option("Visitar o local e ouvir comerciantes", "Bom para empatia local.", {"sudeste": 3, "sul": 2, "intencao": 1.0, "midia": 2, "energia": -8}),
            Option("Usar o tema só para lacrar contra rivais", "Barato que pode sair caro.", {"viral": 6, "rejeicao": 2.0, "credibilidade": -3, "intencao": -0.4}, risky=True),
        ],
    ),
    EventCard(
        id="apoio_evangelico",
        title="⛪ Liderança evangélica sinaliza apoio condicional",
        desc="A aproximação pode mexer fortemente em intenção de voto, mas qualquer ruído de incoerência será cobrado em dobro.",
        category="valores",
        tone="good",
        phase="mid_late",
        tags=["evangélicos", "valores", "mobilização"],
        options=[
            Option("Aceitar apoio com foco em família e combate às drogas", "Ganhos claros no segmento.", {"valores": 7, "evangelicos": 6, "intencao": 1.5, "rejeicao": 0.5}),
            Option("Receber apoio com discurso de união e liberdade religiosa", "Mais amplo e menos sectário.", {"evangelicos": 4, "credibilidade": 3, "intencao": 1.0}),
            Option("Fazer aceno exagerado só por voto", "Cheiro de oportunismo.", {"evangelicos": 2, "credibilidade": -4, "rejeicao": 1.8, "intencao": -0.3}, risky=True),
        ],
    ),
    EventCard(
        id="vaquinha_recorde",
        title="💸 Sua vaquinha online começa a decolar",
        desc="Pequenos doadores estão engajados. Dá para transformar isso em narrativa de independência — ou parecer só mais uma máquina de arrecadação.",
        category="finanças",
        tone="good",
        phase="all",
        tags=["doações", "digital", "independência"],
        options=[
            Option("Transformar cada doação em prova de campanha popular", "Ótimo para base e caixa.", {"caixa": 24000, "intencao": 1.2, "credibilidade": 2, "viral": 8}),
            Option("Arrecadar com discrição e prestar contas bem", "Menos brilho, mais solidez.", {"caixa": 18000, "credibilidade": 4, "risco": -3}),
            Option("Forçar urgência emocional o tempo todo", "Arrecada, mas pode cansar.", {"caixa": 28000, "rejeicao": 1.0, "credibilidade": -2, "intencao": 0.4}, risky=True),
        ],
    ),
    EventCard(
        id="ultimo_debate",
        title="🎯 Último debate antes da votação",
        desc="Aqui não é mais só crescer: é evitar derreter na reta final e seduzir indecisos e voto útil.",
        category="mídia",
        tone="neutral",
        phase="late",
        tags=["debate final", "indecisos", "voto útil"],
        options=[
            Option("Falar com serenidade e mirar o centro", "Puxa indecisos e reduz medo.", {"intencao": 2.1, "rejeicao": -1.2, "credibilidade": 3, "midia": 4}),
            Option("Ir para o tudo ou nada no confronto", "Potencial alto e risco alto.", {"intencao": 2.6, "rejeicao": 2.2, "viral": 10, "midia": 6}, risky=True),
            Option("Buscar voto útil com argumento de viabilidade", "Muito eficiente se você já estiver competitivo.", {"intencao": 1.8, "narrativa": 2, "credibilidade": 2, "tempo_tv": 1}),
        ],
    ),
]


# =========================================================
# HELPERS
# =========================================================
def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def phase_for_day(day: int, total: int) -> str:
    progress = day / total
    if progress < 0.25:
        return "early"
    if progress < 0.60:
        return "mid"
    return "late"


def event_matches_phase(event_phase: str, day_phase: str) -> bool:
    mapping = {
        "all": {"early", "mid", "late"},
        "early_mid": {"early", "mid"},
        "mid": {"mid"},
        "mid_late": {"mid", "late"},
        "late": {"late"},
    }
    return day_phase in mapping.get(event_phase, {day_phase})


def init_state(reset_seed: bool = True):
    if reset_seed:
        st.session_state.seed = random.randint(10_000, 999_999)
    rnd = random.Random(st.session_state.get("seed", 12345))

    st.session_state.day = 1
    st.session_state.total_days = 30
    st.session_state.party = "centro"
    st.session_state.difficulty = "Normal"
    st.session_state.advisor = "estrategista"
    st.session_state.started = False
    st.session_state.game_over = False
    st.session_state.victory = False
    st.session_state.result_text = ""
    st.session_state.last_feedback = ""
    st.session_state.event = None
    st.session_state.used_events = []
    st.session_state.history = []
    st.session_state.achievements = []
    st.session_state.scandals = 0
    st.session_state.combo = 0
    st.session_state.max_combo = 0
    st.session_state.recovery_flag = False
    st.session_state.first_turn = False

    st.session_state.intent = 21.5
    st.session_state.rejection = 24.0
    st.session_state.credibility = 48.0
    st.session_state.cash = 120_000.0
    st.session_state.energy = 78.0
    st.session_state.media = 44.0
    st.session_state.risk = 14.0
    st.session_state.allies = 52.0
    st.session_state.time_tv = 18.0
    st.session_state.momentum = 0.0
    st.session_state.narrative = 45.0
    st.session_state.viral = 10.0

    st.session_state.regions = {
        "Norte": 21 + rnd.uniform(-3, 4),
        "Nordeste": 23 + rnd.uniform(-4, 5),
        "Centro-Oeste": 20 + rnd.uniform(-3, 3),
        "Sudeste": 21 + rnd.uniform(-3, 3),
        "Sul": 20 + rnd.uniform(-3, 3),
    }
    st.session_state.segments = {k: 22 + rnd.uniform(-4, 4) for k in SEGMENTOS.keys()}

    st.session_state.rivals = {
        key: {
            "nome": value["nome"],
            "voto": float(value["base"]),
            "rejeicao": float(value["rejeicao"]),
            "perfil": value["perfil"],
        }
        for key, value in ADVERSARIOS.items()
    }

    st.session_state.poll_history = [st.session_state.intent]
    st.session_state.rej_history = [st.session_state.rejection]
    st.session_state.day_history = [1]


def apply_setup_choices():
    party = st.session_state.party
    advisor = st.session_state.advisor
    diff = st.session_state.difficulty

    if party == "popular":
        st.session_state.intent += 2.0
        st.session_state.regions["Nordeste"] += 4
        st.session_state.segments["periferia"] += 4
        st.session_state.segments["servidores"] += 2
        st.session_state.time_tv += 1
    elif party == "liberal":
        st.session_state.cash += 20_000
        st.session_state.regions["Sudeste"] += 3
        st.session_state.segments["empreendedores"] += 5
        st.session_state.segments["agro"] += 2
        st.session_state.rejection += 1.5
    elif party == "verde":
        st.session_state.credibility += 5
        st.session_state.regions["Norte"] += 4
        st.session_state.segments["jovens"] += 4
        st.session_state.intent += 1.0

    bonus = ASSESSORES[advisor]["bonus"]
    st.session_state.cash += bonus.get("caixa", 0)
    st.session_state.credibility += bonus.get("credibilidade", 0)
    st.session_state.media += bonus.get("midia", 0)
    st.session_state.viral += bonus.get("viral", 0)
    st.session_state.allies += bonus.get("aliados", 0)
    st.session_state.time_tv += bonus.get("tempo_tv", 0)
    st.session_state.risk = clamp(st.session_state.risk + bonus.get("risco", 0), 0, 100)
    st.session_state.narrative += bonus.get("narrativa", 0)
    st.session_state.momentum += bonus.get("momentum", 0)

    if diff == "Fácil":
        st.session_state.intent += 3
        st.session_state.cash += 25_000
        st.session_state.energy += 10
        st.session_state.rejection -= 2
        st.session_state.risk -= 4
    elif diff == "Difícil":
        st.session_state.intent -= 2
        st.session_state.cash -= 25_000
        st.session_state.rejection += 2
        st.session_state.risk += 5
    elif diff == "Hardcore":
        st.session_state.intent -= 4
        st.session_state.cash -= 45_000
        st.session_state.energy -= 10
        st.session_state.rejection += 4
        st.session_state.risk += 10

    st.session_state.intent = clamp(st.session_state.intent, 5, 60)
    st.session_state.rejection = clamp(st.session_state.rejection, 5, 80)
    st.session_state.energy = clamp(st.session_state.energy, 10, 100)
    st.session_state.media = clamp(st.session_state.media, 5, 100)
    st.session_state.started = True


def get_available_events() -> List[EventCard]:
    day_phase = phase_for_day(st.session_state.day, st.session_state.total_days)
    recent = set(st.session_state.used_events[-8:])
    pool = [e for e in EVENTS if e.id not in recent and event_matches_phase(e.phase, day_phase)]
    if not pool:
        pool = [e for e in EVENTS if event_matches_phase(e.phase, day_phase)]
    return pool


def weighted_event_pick(pool: List[EventCard]) -> EventCard:
    weights = []
    for e in pool:
        weight = 1.0
        if e.tone == "crisis" and (st.session_state.risk > 40 or st.session_state.rejection > 35):
            weight += 1.8
        if e.tone == "good" and st.session_state.momentum > 4:
            weight += 1.2
        if e.category == "jurídico" and st.session_state.risk > 35:
            weight += 0.8
        if e.category == "finanças" and st.session_state.cash < 50_000:
            weight += 1.3
        if e.category == "aliança" and st.session_state.allies < 45:
            weight += 1.2
        weights.append(weight)
    return random.choices(pool, weights=weights, k=1)[0]


def generate_event():
    pool = get_available_events()
    st.session_state.event = weighted_event_pick(pool)


def option_enabled(option: Option) -> bool:
    req = option.requires or {}
    for key, value in req.items():
        current = getattr_proxy(key)
        if current < value:
            return False
    return True


def getattr_proxy(name: str) -> float:
    mapping = {
        "cash": st.session_state.cash,
        "energy": st.session_state.energy,
        "media": st.session_state.media,
        "risk": st.session_state.risk,
        "credibility": st.session_state.credibility,
        "intent": st.session_state.intent,
    }
    return mapping.get(name, 0)


def apply_effects(effects: Dict[str, float], risky: bool = False):
    advisor = st.session_state.advisor
    mult = 1.0
    if st.session_state.difficulty == "Fácil":
        mult = 1.08
    elif st.session_state.difficulty == "Difícil":
        mult = 0.94
    elif st.session_state.difficulty == "Hardcore":
        mult = 0.88

    if advisor == "juridico" and risky:
        effects = effects.copy()
        effects["risk"] = effects.get("risk", 0) * 0.55
        effects["credibility"] = effects.get("credibility", 0) + 0.8
    elif advisor == "comunicacao" and ("midia" in effects or "viral" in effects):
        effects = effects.copy()
        effects["midia"] = effects.get("midia", 0) * 1.2
        effects["viral"] = effects.get("viral", 0) * 1.25
    elif advisor == "financeiro" and ("caixa" in effects or "cash" in effects):
        effects = effects.copy()
        effects["caixa"] = effects.get("caixa", 0) * 1.15
    elif advisor == "politico" and ("aliados" in effects or "tempo_tv" in effects):
        effects = effects.copy()
        effects["aliados"] = effects.get("aliados", 0) * 1.15
        effects["tempo_tv"] = effects.get("tempo_tv", 0) * 1.20
    elif advisor == "estrategista" and "intencao" in effects:
        effects = effects.copy()
        effects["intencao"] = effects.get("intencao", 0) * 1.15

    st.session_state.intent = clamp(st.session_state.intent + effects.get("intencao", 0) * mult, 0, 80)
    st.session_state.rejection = clamp(st.session_state.rejection + effects.get("rejeicao", 0), 0, 95)
    st.session_state.credibility = clamp(st.session_state.credibility + effects.get("credibilidade", 0), 0, 100)
    st.session_state.cash = max(0.0, st.session_state.cash + effects.get("caixa", 0) + effects.get("cash", 0))
    st.session_state.energy = clamp(st.session_state.energy + effects.get("energia", -2), 0, 100)
    st.session_state.media = clamp(st.session_state.media + effects.get("midia", 0), 0, 100)
    st.session_state.risk = clamp(st.session_state.risk + effects.get("risco", 0) + effects.get("risk", 0), 0, 100)
    st.session_state.allies = clamp(st.session_state.allies + effects.get("aliados", 0), 0, 100)
    st.session_state.time_tv = clamp(st.session_state.time_tv + effects.get("tempo_tv", 0), 0, 100)
    st.session_state.momentum = clamp(st.session_state.momentum + effects.get("momentum", 0), -20, 20)
    st.session_state.narrative = clamp(st.session_state.narrative + effects.get("narrativa", 0), 0, 100)
    st.session_state.viral = clamp(st.session_state.viral + effects.get("viral", 0), 0, 100)

    # microtargeting -> segmentos/regiões
    region_map = {
        "nordeste": "Nordeste",
        "sudeste": "Sudeste",
        "sul": "Sul",
        "centro-oeste": "Centro-Oeste",
        "norte": "Norte",
    }
    for key, region_name in region_map.items():
        if key in effects:
            st.session_state.regions[region_name] = clamp(st.session_state.regions[region_name] + effects[key] * 0.8, 0, 80)

    segment_keys = ["social", "gestao", "agro", "valores", "digital", "mercado", "jovens", "evangelicos"]
    for seg in list(st.session_state.segments.keys()):
        if seg in effects:
            st.session_state.segments[seg] = clamp(st.session_state.segments[seg] + effects[seg] * 0.8, 0, 80)

    # distribui efeitos temáticos em segmentos relacionados
    if effects.get("social"):
        st.session_state.segments["periferia"] = clamp(st.session_state.segments["periferia"] + effects["social"] * 0.8, 0, 80)
        st.session_state.regions["Nordeste"] = clamp(st.session_state.regions["Nordeste"] + effects["social"] * 0.35, 0, 80)
    if effects.get("gestao"):
        st.session_state.segments["classe_media"] = clamp(st.session_state.segments["classe_media"] + effects["gestao"] * 0.65, 0, 80)
        st.session_state.segments["servidores"] = clamp(st.session_state.segments["servidores"] + effects["gestao"] * 0.5, 0, 80)
    if effects.get("mercado"):
        st.session_state.segments["empreendedores"] = clamp(st.session_state.segments["empreendedores"] + effects["mercado"] * 0.75, 0, 80)
        st.session_state.regions["Sudeste"] = clamp(st.session_state.regions["Sudeste"] + effects["mercado"] * 0.35, 0, 80)
    if effects.get("agro"):
        st.session_state.segments["agro"] = clamp(st.session_state.segments["agro"] + effects["agro"] * 0.9, 0, 80)
        st.session_state.regions["Centro-Oeste"] = clamp(st.session_state.regions["Centro-Oeste"] + effects["agro"] * 0.5, 0, 80)
        st.session_state.regions["Sul"] = clamp(st.session_state.regions["Sul"] + effects["agro"] * 0.3, 0, 80)
    if effects.get("digital"):
        st.session_state.segments["jovens"] = clamp(st.session_state.segments["jovens"] + effects["digital"] * 0.7, 0, 80)

    if risky:
        st.session_state.scandals += 1 if (effects.get("risco", 0) + effects.get("risk", 0)) > 8 else 0

    positive = effects.get("intencao", 0) + effects.get("credibilidade", 0) / 4 - effects.get("rejeicao", 0)
    if positive > 0.8:
        st.session_state.combo += 1
    else:
        st.session_state.combo = 0
    st.session_state.max_combo = max(st.session_state.max_combo, st.session_state.combo)
    if st.session_state.combo >= 3:
        st.session_state.momentum = clamp(st.session_state.momentum + 1.5, -20, 20)


def rival_turn():
    for key, rival in st.session_state.rivals.items():
        drift = random.uniform(-0.8, 1.0)
        if rival["perfil"] == "digital":
            drift += (0.12 if st.session_state.viral < 25 else -0.08) * random.uniform(0.5, 1.2)
        if rival["perfil"] == "gestao":
            drift += 0.15 if st.session_state.credibility < 45 else -0.05
        if rival["perfil"] == "estrutura":
            drift += 0.14 if st.session_state.allies < 48 else -0.04
        rival["voto"] = clamp(rival["voto"] + drift, 8, 45)
        rival["rejeicao"] = clamp(rival["rejeicao"] + random.uniform(-0.5, 0.9), 10, 60)


def daily_decay_and_growth():
    # desgaste natural
    st.session_state.energy = clamp(st.session_state.energy - random.uniform(3, 6), 0, 100)
    st.session_state.cash = max(0.0, st.session_state.cash - random.uniform(3500, 9500))
    st.session_state.media = clamp(st.session_state.media + random.uniform(-3, 3) + st.session_state.momentum * 0.06, 0, 100)
    st.session_state.risk = clamp(st.session_state.risk + random.uniform(-1.5, 2.5), 0, 100)

    # conversão sistêmica para intenção de voto
    regional_score = sum(st.session_state.regions[r] * REGIOES[r]["peso"] for r in REGIOES) / 100
    segment_score = sum(st.session_state.segments[s] * SEGMENTOS[s]["peso"] for s in SEGMENTOS) / 100
    structure_bonus = (st.session_state.media * 0.04 + st.session_state.time_tv * 0.05 + st.session_state.allies * 0.03)
    narrative_bonus = (st.session_state.credibility * 0.035 + st.session_state.narrative * 0.025 + st.session_state.momentum * 0.3)
    penalty = st.session_state.rejection * 0.07 + st.session_state.risk * 0.05
    target_intent = 8 + regional_score * 0.18 + segment_score * 0.17 + structure_bonus + narrative_bonus - penalty
    target_intent = clamp(target_intent, 4, 65)

    # converge aos poucos para parecer campanha real
    st.session_state.intent = clamp(st.session_state.intent * 0.60 + target_intent * 0.40, 0, 80)

    # votação útil em reta final
    if st.session_state.day > st.session_state.total_days - 5 and st.session_state.intent > 24:
        third_best = sorted([rv["voto"] for rv in st.session_state.rivals.values()], reverse=True)[-1]
        if st.session_state.intent > third_best:
            st.session_state.intent = clamp(st.session_state.intent + 0.6, 0, 80)

    # pequenas flutuações regionais
    for region in st.session_state.regions:
        st.session_state.regions[region] = clamp(st.session_state.regions[region] + random.uniform(-1.1, 1.4) + st.session_state.momentum * 0.02, 0, 80)
    for seg in st.session_state.segments:
        st.session_state.segments[seg] = clamp(st.session_state.segments[seg] + random.uniform(-1.2, 1.2), 0, 80)


def add_history(label: str, option_text: str):
    st.session_state.history.insert(0, f"Dia {st.session_state.day}: {label} → {option_text}")
    st.session_state.history = st.session_state.history[:12]


def unlock_achievements():
    achievements = st.session_state.achievements
    if st.session_state.viral >= 25 and "primeiro_viral" not in achievements:
        achievements.append("primeiro_viral")
    if st.session_state.cash >= 180_000 and "caixa_forte" not in achievements:
        achievements.append("caixa_forte")
    if st.session_state.media >= 72 and "mestre_midia" not in achievements:
        achievements.append("mestre_midia")
    if st.session_state.risk <= 10 and st.session_state.day >= 12 and "blindado" not in achievements:
        achievements.append("blindado")
    if st.session_state.max_combo >= 4 and "furacao" not in achievements:
        achievements.append("furacao")
    if st.session_state.regions["Nordeste"] >= 40 and "lider_nordeste" not in achievements:
        achievements.append("lider_nordeste")
    if st.session_state.regions["Sudeste"] >= 38 and "lider_sudeste" not in achievements:
        achievements.append("lider_sudeste")
    if st.session_state.scandals == 0 and st.session_state.day >= st.session_state.total_days and "sem_escandalo" not in achievements:
        achievements.append("sem_escandalo")
    if st.session_state.recovery_flag and st.session_state.intent >= 28 and "virou_o_jogo" not in achievements:
        achievements.append("virou_o_jogo")


def check_game_over():
    if st.session_state.intent <= 5:
        st.session_state.game_over = True
        st.session_state.result_text = "Sua candidatura evaporou nas pesquisas. Virou figurante do próprio jogo."
    elif st.session_state.cash <= 0:
        st.session_state.game_over = True
        st.session_state.result_text = "O caixa secou. Sem gasolina política, a campanha morreu na estrada."
    elif st.session_state.energy <= 0:
        st.session_state.game_over = True
        st.session_state.result_text = "Você colapsou na maratona. O ritmo da campanha engoliu seu candidato."
    elif st.session_state.risk >= 92:
        st.session_state.game_over = True
        st.session_state.result_text = "A campanha afundou num mar de risco jurídico e crise de imagem."
    elif st.session_state.rejection >= 72:
        st.session_state.game_over = True
        st.session_state.result_text = "A rejeição ficou tóxica demais. Nem viral salva quando metade do país fecha a cara."


def simulate_final_result():
    your_vote = clamp(
        st.session_state.intent
        + st.session_state.media * 0.03
        + st.session_state.time_tv * 0.02
        + st.session_state.allies * 0.015
        - st.session_state.rejection * 0.05,
        5,
        65,
    )

    rivals = {k: clamp(v["voto"], 6, 45) for k, v in st.session_state.rivals.items()}
    total = your_vote + sum(rivals.values())
    scale = 100 / total
    your_vote *= scale
    rivals = {k: v * scale for k, v in rivals.items()}
    ordered = sorted(rivals.items(), key=lambda x: x[1], reverse=True)
    top_rival_key, top_rival_vote = ordered[0]

    if your_vote >= 50:
        st.session_state.victory = True
        st.session_state.game_over = True
        st.session_state.first_turn = True
        st.session_state.result_text = f"Você venceu no 1º turno com {your_vote:.1f}% dos votos válidos. Brasil em choque e sua campanha entra para o folclore político."
        if "primeiro_turno" not in st.session_state.achievements:
            st.session_state.achievements.append("primeiro_turno")
        return

    # segundo turno
    your_transfer = (100 - your_vote - top_rival_vote) * (
        0.50 + (st.session_state.credibility - st.session_state.rejection) / 220 + st.session_state.narrative / 300
    )
    rival_transfer = (100 - your_vote - top_rival_vote) - your_transfer
    second_you = clamp(your_vote + your_transfer, 20, 80)
    second_rival = clamp(top_rival_vote + rival_transfer, 20, 80)
    total2 = second_you + second_rival
    second_you = second_you * 100 / total2
    second_rival = second_rival * 100 / total2

    st.session_state.game_over = True
    if second_you > second_rival:
        st.session_state.victory = True
        st.session_state.result_text = f"Você foi ao 2º turno contra {st.session_state.rivals[top_rival_key]['nome']} e venceu por {second_you:.1f}% a {second_rival:.1f}%. Foi no limite, mas foi."
    else:
        st.session_state.victory = False
        st.session_state.result_text = f"Você chegou ao 2º turno, mas perdeu para {st.session_state.rivals[top_rival_key]['nome']} por {second_rival:.1f}% a {second_you:.1f}%. Doeu — e rende revanche."


def next_day(option: Option):
    apply_effects(option.effects, risky=option.risky)
    rival_turn()
    daily_decay_and_growth()
    unlock_achievements()

    if st.session_state.intent < 15:
        st.session_state.recovery_flag = True

    st.session_state.used_events.append(st.session_state.event.id)
    add_history(st.session_state.event.title, option.text)
    st.session_state.poll_history.append(st.session_state.intent)
    st.session_state.rej_history.append(st.session_state.rejection)
    st.session_state.day_history.append(st.session_state.day)

    st.session_state.last_feedback = option.summary
    check_game_over()
    if st.session_state.game_over:
        return

    st.session_state.day += 1
    if st.session_state.day > st.session_state.total_days:
        simulate_final_result()
    else:
        generate_event()


def fmt_money(v: float) -> str:
    return f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def bar_html(label: str, value: float, color: str) -> str:
    return f"""
    <div style='margin-bottom:10px'>
      <div style='display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px'>
        <span><strong>{label}</strong></span><span>{value:.1f}%</span>
      </div>
      <div style='background:#e5e7eb;border-radius:999px;height:10px;overflow:hidden'>
        <div style='background:{color};width:{max(1,value)}%;height:10px;border-radius:999px'></div>
      </div>
    </div>
    """


def render_metric_cards():
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    cards = [
        (c1, "INTENÇÃO", f"{st.session_state.intent:.1f}%", "Pesquisa do dia"),
        (c2, "REJEIÇÃO", f"{st.session_state.rejection:.1f}%", "Quanto mais baixo, melhor"),
        (c3, "CAIXA", fmt_money(st.session_state.cash), "Campanha viva"),
        (c4, "MÍDIA", f"{st.session_state.media:.0f}", "Noticiário e corte"),
        (c5, "RISCO", f"{st.session_state.risk:.0f}%", "Jurídico + escândalo"),
        (c6, "ENERGIA", f"{st.session_state.energy:.0f}%", "Fôlego de campanha"),
    ]
    for col, title, value, desc in cards:
        with col:
            st.markdown(f"<div class='metric-card'><h4>{title}</h4><h2>{value}</h2><span>{desc}</span></div>", unsafe_allow_html=True)


def sidebar_panel():
    with st.sidebar:
        st.markdown("## 🎛️ Painel de Campanha")
        st.caption(f"Seed da campanha: {st.session_state.get('seed','-')}")
        if st.session_state.started:
            st.write(f"**Dia:** {st.session_state.day}/{st.session_state.total_days}")
            st.write(f"**Partido:** {PARTIDOS[st.session_state.party]['nome']}")
            st.write(f"**Assessor:** {ASSESSORES[st.session_state.advisor]['nome']}")
            st.write(f"**Dificuldade:** {st.session_state.difficulty}")
            st.progress(clamp(st.session_state.intent / 50, 0, 1), text="competitividade")
            st.progress(clamp((100 - st.session_state.rejection) / 100, 0, 1), text="aceitação")
            st.progress(clamp(st.session_state.energy / 100, 0, 1), text="energia")

            if st.session_state.combo >= 2:
                st.success(f"🔥 Combo ativo x{st.session_state.combo}")
            if st.session_state.risk > 55:
                st.error("🚨 Campanha flertando com crise grande")
            elif st.session_state.risk > 35:
                st.warning("⚠️ Risco subindo")
            if st.session_state.cash < 35_000:
                st.warning("💸 Caixa crítico")
            if st.session_state.intent < 18:
                st.warning("📉 Você precisa virar o jogo")

            st.markdown("### 🧭 Regiões")
            region_colors = {
                "Norte": "#16a34a",
                "Nordeste": "#f97316",
                "Centro-Oeste": "#84cc16",
                "Sudeste": "#2563eb",
                "Sul": "#7c3aed",
            }
            for reg, val in st.session_state.regions.items():
                st.markdown(bar_html(reg, val, region_colors[reg]), unsafe_allow_html=True)

            st.markdown("### 🏅 Conquistas")
            if st.session_state.achievements:
                for ach in st.session_state.achievements[-6:]:
                    st.markdown(f"- {ACHIEVEMENTS[ach]}")
            else:
                st.caption("Nenhuma conquista ainda.")

        st.markdown("---")
        if st.button("🔄 Nova campanha", use_container_width=True):
            init_state(reset_seed=True)
            st.rerun()


def render_charts():
    col1, col2 = st.columns([1.4, 1])
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=st.session_state.day_history, y=st.session_state.poll_history, mode="lines+markers", name="Você"))
        fig.add_trace(go.Scatter(x=st.session_state.day_history, y=st.session_state.rej_history, mode="lines", name="Rejeição"))
        fig.update_layout(height=320, margin=dict(l=20, r=20, t=30, b=20), title="Termômetro da campanha")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        rival_names = ["Você"] + [v["nome"] for v in st.session_state.rivals.values()]
        rival_votes = [st.session_state.intent] + [v["voto"] for v in st.session_state.rivals.values()]
        fig2 = go.Figure(go.Bar(x=rival_names, y=rival_votes))
        fig2.update_layout(height=320, margin=dict(l=20, r=20, t=30, b=20), title="Corrida eleitoral")
        st.plotly_chart(fig2, use_container_width=True)


def render_setup():
    st.markdown("<div class='hero'><h1>🇧🇷 Candidato 2026: Viral Edition</h1><p>Um simulador de campanha presidencial com rejeição, voto útil, 2º turno, crise, coalizão, viral e eventos inspirados na política brasileira.</p></div>", unsafe_allow_html=True)

    st.markdown("### Monte sua campanha")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.party = st.selectbox(
            "Partido",
            list(PARTIDOS.keys()),
            format_func=lambda x: f"{PARTIDOS[x]['nome']} — {PARTIDOS[x]['slogan']}",
        )
    with c2:
        st.session_state.advisor = st.selectbox(
            "Assessor principal",
            list(ASSESSORES.keys()),
            format_func=lambda x: f"{ASSESSORES[x]['icone']} {ASSESSORES[x]['nome']} — {ASSESSORES[x]['especialidade']}",
        )
    with c3:
        st.session_state.difficulty = st.selectbox("Dificuldade", ["Fácil", "Normal", "Difícil", "Hardcore"], index=1)

    st.markdown("### O que muda nesta versão")
    cols = st.columns(5)
    highlights = [
        ("🧠", "Rejeição separada da intenção de voto"),
        ("🗺️", "Mapa regional e segmentos sociais"),
        ("⚖️", "Crises jurídicas e TSE"),
        ("🔥", "Viral, combo e momentum"),
        ("🗳️", "1º e 2º turno com transferência de votos"),
    ]
    for col, item in zip(cols, highlights):
        with col:
            st.markdown(f"<div class='card' style='min-height:120px;text-align:center'><div style='font-size:30px'>{item[0]}</div><div style='font-weight:700;margin-top:8px'>{item[1]}</div></div>", unsafe_allow_html=True)

    st.markdown("### Seu estrategista de confiança")
    advisor = ASSESSORES[st.session_state.advisor]
    st.markdown(f"<div class='advisor'><h4 style='margin:0'>{advisor['icone']} {advisor['nome']}</h4><div class='small-muted'>{advisor['descricao']}</div></div>", unsafe_allow_html=True)

    if st.button("🚀 Iniciar campanha", use_container_width=True, type="primary"):
        init_state(reset_seed=False)
        apply_setup_choices()
        generate_event()
        st.rerun()


def render_event():
    event = st.session_state.event
    tone_class = "event-crisis" if event.tone == "crisis" else "event-good" if event.tone == "good" else ""
    st.markdown(
        f"""
        <div class='event-box {tone_class}'>
            <h2 style='margin-top:0'>{event.title}</h2>
            <p style='font-size:15px;line-height:1.55'>{event.desc}</p>
            {''.join([f"<span class='tag {'tag-red' if event.tone=='crisis' else 'tag-green' if event.tone=='good' else 'tag-blue'}'>{tag}</span>" for tag in event.tags])}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.last_feedback:
        klass = "success-strip" if "boa" in st.session_state.last_feedback.lower() or "ótimo" in st.session_state.last_feedback.lower() else "warning-strip"
        st.markdown(f"<div class='{klass}'>{st.session_state.last_feedback}</div>", unsafe_allow_html=True)
        st.write("")

    st.markdown("### Escolha sua resposta")
    for idx, option in enumerate(event.options):
        st.markdown(
            f"<div class='choice-box'><div class='choice-title'>{idx+1}. {option.text}</div><div class='small-muted'>{option.summary}</div></div>",
            unsafe_allow_html=True,
        )
        if st.button(f"Escolher opção {idx+1}", key=f"opt_{event.id}_{idx}", use_container_width=True, disabled=not option_enabled(option)):
            next_day(option)
            st.rerun()


def render_results():
    if st.session_state.victory:
        st.markdown(f"<div class='success-strip' style='font-size:18px'>{st.session_state.result_text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='warning-strip' style='font-size:18px'>{st.session_state.result_text}</div>", unsafe_allow_html=True)

    st.write("")
    render_charts()
    st.markdown("### Últimos movimentos")
    for line in st.session_state.history[:8]:
        st.write(f"- {line}")


def render_bottom_panels():
    col1, col2, col3 = st.columns([1, 1, 1.1])
    with col1:
        st.markdown("### 👥 Segmentos")
        for seg, val in sorted(st.session_state.segments.items(), key=lambda x: x[1], reverse=True):
            st.markdown(bar_html(seg.replace("_", " ").title(), val, "#2563eb"), unsafe_allow_html=True)
    with col2:
        st.markdown("### 🏛️ Estrutura")
        st.metric("Aliados", f"{st.session_state.allies:.0f}")
        st.metric("Tempo de TV", f"{st.session_state.time_tv:.0f}")
        st.metric("Credibilidade", f"{st.session_state.credibility:.0f}")
        st.metric("Viral", f"{st.session_state.viral:.0f}")
        st.metric("Narrativa", f"{st.session_state.narrative:.0f}")
    with col3:
        st.markdown("### 📰 Diário da campanha")
        if st.session_state.history:
            for h in st.session_state.history[:10]:
                st.write(f"• {h}")
        else:
            st.caption("Sem histórico ainda.")
        if st.session_state.achievements:
            st.markdown("### 🏅 Badges")
            badges = "".join([f"<span class='achievement'>{ACHIEVEMENTS[a]}</span>" for a in st.session_state.achievements])
            st.markdown(badges, unsafe_allow_html=True)


def main():
    if "seed" not in st.session_state:
        init_state(reset_seed=True)

    sidebar_panel()

    if not st.session_state.started:
        render_setup()
        return

    st.markdown(
        f"<div class='hero'><h1>🇧🇷 {PARTIDOS[st.session_state.party]['nome']}</h1><p>Dia {st.session_state.day}/{st.session_state.total_days} • {PARTIDOS[st.session_state.party]['slogan']} • Assessor: {ASSESSORES[st.session_state.advisor]['nome']}</p></div>",
        unsafe_allow_html=True,
    )

    render_metric_cards()
    st.write("")
    render_charts()
    st.write("")

    if st.session_state.game_over:
        render_results()
    else:
        render_event()
        st.write("")
        render_bottom_panels()


if __name__ == "__main__":
    main()
