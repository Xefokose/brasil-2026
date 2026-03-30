
import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import plotly.graph_objects as go
import streamlit as st

# =========================================================
# CONFIGURAÇÃO
# =========================================================
st.set_page_config(
    page_title="🇧🇷 Candidato 2026: Viral Master V5",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
)

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%); }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
.hero{
    background: linear-gradient(135deg, #0f172a 0%, #172554 42%, #1d4ed8 100%);
    color:white; border-radius:24px; padding:28px; margin-bottom:16px;
    box-shadow:0 16px 48px rgba(15,23,42,.22);
}
.hero h1{margin:0 0 6px 0; font-size:2.2rem;}
.hero p{margin:0; opacity:.92;}
.panel{
    background:white; border-radius:18px; padding:18px;
    border:1px solid rgba(99,102,241,.08);
    box-shadow:0 10px 28px rgba(15,23,42,.08);
}
.metric-card{
    background:linear-gradient(135deg,#111827 0%,#1f2937 100%);
    color:white; border-radius:18px; padding:16px; min-height:110px;
    box-shadow:0 10px 26px rgba(0,0,0,.18);
}
.metric-card h4{margin:0; opacity:.78; font-size:12px; text-transform:uppercase; letter-spacing:.08em;}
.metric-card h2{margin:8px 0 6px 0; font-size:30px;}
.metric-card span{font-size:12px; opacity:.9;}
.event-box{
    background:linear-gradient(135deg,#fff 0%,#f8fafc 100%);
    border-left:8px solid #2563eb;
    border-radius:22px; padding:24px; margin-bottom:18px;
    box-shadow:0 12px 34px rgba(15,23,42,.10);
}
.event-crisis{border-left-color:#dc2626;}
.event-good{border-left-color:#16a34a;}
.event-followup{border-left-color:#7c3aed;}
.choice-box{
    background:#fff; border:1px solid #e5e7eb; border-radius:16px; padding:14px;
    box-shadow:0 6px 18px rgba(15,23,42,.05); margin-bottom:10px;
}
.choice-title{font-weight:700; color:#111827; margin-bottom:6px;}
.small-muted{color:#64748b; font-size:13px;}
.tag{
    display:inline-block; padding:6px 10px; border-radius:999px; font-size:11px;
    font-weight:700; margin-right:6px; margin-top:8px;
}
.tag-blue{background:#dbeafe;color:#1d4ed8;}
.tag-red{background:#fee2e2;color:#b91c1c;}
.tag-green{background:#dcfce7;color:#166534;}
.tag-purple{background:#ede9fe;color:#6d28d9;}
.effect-chip{
    display:inline-flex; align-items:center; gap:6px; padding:7px 10px; border-radius:999px;
    font-size:12px; font-weight:700; margin:4px 5px 0 0; background:#f3f4f6; color:#111827;
}
.consequence-card{
    background:linear-gradient(135deg,#fff7ed 0%,#fffbeb 100%);
    border:1px solid #fed7aa; border-radius:16px; padding:14px; margin-bottom:10px;
}
.achievement{
    display:inline-block; padding:8px 12px; border-radius:999px; margin:4px;
    background:linear-gradient(135deg,#a855f7 0%,#ec4899 100%); color:white;
    font-size:12px; font-weight:700;
}
.region-row{margin-bottom:10px;}
.success-strip{
    background:linear-gradient(135deg,#22c55e 0%,#16a34a 100%);
    color:white; padding:14px 16px; border-radius:14px; font-weight:600;
}
.warning-strip{
    background:linear-gradient(135deg,#ef4444 0%,#dc2626 100%);
    color:white; padding:14px 16px; border-radius:14px; font-weight:600;
}
.stButton>button{
    border-radius:12px !important; font-weight:700 !important; border:0 !important;
    background:linear-gradient(135deg,#2563eb 0%,#7c3aed 100%) !important; color:white !important;
    box-shadow:0 8px 18px rgba(59,130,246,.25) !important;
}
.stButton>button:hover{transform:translateY(-1px);}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

# =========================================================
# DADOS BASE
# =========================================================
REGIONS = {
    "Norte": {"peso": 8, "cor": "#0ea5e9"},
    "Nordeste": {"peso": 27, "cor": "#f59e0b"},
    "Centro-Oeste": {"peso": 8, "cor": "#22c55e"},
    "Sudeste": {"peso": 42, "cor": "#6366f1"},
    "Sul": {"peso": 15, "cor": "#ef4444"},
}

SEGMENTS = {
    "periferia": {"peso": 18, "nome": "Periferia"},
    "classe_media": {"peso": 18, "nome": "Classe média"},
    "agro": {"peso": 12, "nome": "Agro"},
    "evangelicos": {"peso": 14, "nome": "Evangélicos"},
    "jovens": {"peso": 12, "nome": "Jovens"},
    "servidores": {"peso": 11, "nome": "Servidores"},
    "empreendedores": {"peso": 15, "nome": "Empreendedores"},
}

PARTIES = {
    "centro": {"nome": "Movimento de Centro", "slogan": "Gestão sem histeria"},
    "popular": {"nome": "Frente Popular", "slogan": "Povo em primeiro lugar"},
    "liberal": {"nome": "Aliança Liberal", "slogan": "Produzir, crescer, simplificar"},
    "verde": {"nome": "Rede Verde Brasil", "slogan": "Desenvolver sem destruir"},
}

ADVISORS = {
    "estrategista": {
        "nome": "Carlos Mendes",
        "icone": "🎯",
        "descricao": "Timing, swing e leitura fina de campanha.",
        "start": {"intent": 1.5, "credibility": 2, "momentum": 2},
    },
    "financeiro": {
        "nome": "Ana Rodrigues",
        "icone": "💰",
        "descricao": "Caixa, captação legal e disciplina de gasto.",
        "start": {"cash": 30000, "credibility": -1, "allies": 2},
    },
    "comunicacao": {
        "nome": "Pedro Santos",
        "icone": "📰",
        "descricao": "Entra bem em TV, rádio, rede e corte viral.",
        "start": {"media": 8, "viral": 10, "intent": 1},
    },
    "politico": {
        "nome": "Helena Costa",
        "icone": "🤝",
        "descricao": "Consegue palanque, federação e telefonema útil.",
        "start": {"allies": 10, "time_tv": 5, "governabilidade": 8},
    },
    "juridico": {
        "nome": "Roberto Lima",
        "icone": "⚖️",
        "descricao": "Segura bomba do TSE e limpa zona cinzenta.",
        "start": {"risk": -10, "credibility": 4},
    },
}

RIVAL_ARCHETYPES = {
    "populista": {"nome": "Ronaldo Falcão", "perfil": "digital", "voto": 26.0, "rejeicao": 31.0},
    "tecnico": {"nome": "Marina Albuquerque", "perfil": "gestao", "voto": 23.0, "rejeicao": 22.0},
    "maquina": {"nome": "César Prado", "perfil": "estrutura", "voto": 25.0, "rejeicao": 28.0},
}

ACHIEVEMENTS = {
    "primeira_escolha": "🎯 Primeira decisão",
    "caixa_forte": "💰 Caixa forte",
    "campanha_viva": "⚡ Pulmão de campanha",
    "mestre_midia": "📰 Mestre da mídia",
    "blindado": "⚖️ Blindado",
    "furacao": "🔥 Furacão eleitoral",
    "sem_escandalo": "✨ Campanha limpa",
    "voto_util": "🗳️ Captou voto útil",
    "lider_nordeste": "🌵 Dominou o Nordeste",
    "lider_sudeste": "🏙️ Dominou o Sudeste",
    "crise_domada": "🛡️ Domou a crise",
    "primeiro_turno": "🏆 Vitória no 1º turno",
    "virada": "🔄 Virada histórica",
    "incansavel": "🏃 Incansável",
}

# =========================================================
# MODELOS
# =========================================================
@dataclass
class Consequence:
    key: str
    title: str
    desc: str
    duration: int
    daily: Dict[str, float] = field(default_factory=dict)
    end_effects: Dict[str, float] = field(default_factory=dict)
    severity: str = "warning"
    followup_event: Optional[str] = None
    followup_chance: float = 0.0


@dataclass
class Option:
    text: str
    summary: str
    effects: Dict[str, float]
    risky: bool = False
    requirement: Optional[Dict[str, float]] = None
    consequences: List[Consequence] = field(default_factory=list)


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
    followup_only: bool = False


# =========================================================
# HELPERS
# =========================================================
def clamp(x: float, low: float, high: float) -> float:
    return max(low, min(high, x))


def fmt_money(v: float) -> str:
    return f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def phase_for_day(day: int, total_days: int) -> str:
    pct = day / max(1, total_days)
    if pct <= 0.22:
        return "early"
    if pct <= 0.55:
        return "mid"
    if pct <= 0.82:
        return "late"
    return "final"


def phase_matches(card_phase: str, current: str) -> bool:
    if card_phase == "all":
        return True
    mapping = {
        "early": ["early"],
        "mid": ["mid"],
        "late": ["late"],
        "final": ["final"],
        "early_mid": ["early", "mid"],
        "mid_late": ["mid", "late"],
        "late_final": ["late", "final"],
    }
    return current in mapping.get(card_phase, [card_phase])


def chip(text: str) -> str:
    return f"<span class='effect-chip'>{text}</span>"


def apply_delta_to_map(map_obj: Dict[str, float], key: str, amount: float, high: float = 100.0):
    map_obj[key] = clamp(map_obj[key] + amount, 0, high)


def req_ok(req: Optional[Dict[str, float]]) -> bool:
    if not req:
        return True
    for key, min_value in req.items():
        if getattr_proxy(key) < min_value:
            return False
    return True


def getattr_proxy(name: str) -> float:
    s = st.session_state
    mapping = {
        "cash": s.cash,
        "energy": s.energy,
        "intent": s.intent,
        "rejection": s.rejection,
        "risk": s.risk,
        "allies": s.allies,
        "credibility": s.credibility,
        "media": s.media,
        "viral": s.viral,
        "time_tv": s.time_tv,
    }
    return mapping.get(name, 0.0)


# =========================================================
# CONSEQUÊNCIAS
# =========================================================
def cons_media_negative(days: int = 3):
    return Consequence(
        key=f"media_neg_{days}",
        title="Rodada de mídia negativa",
        desc="O assunto não morreu no mesmo dia. Painel, corte e coluna seguem cobrando.",
        duration=days,
        daily={"media": -2.0, "credibility": -1.1, "rejection": 0.5},
        severity="danger",
    )


def cons_organic_wave(days: int = 3):
    return Consequence(
        key=f"onda_org_{days}",
        title="Onda orgânica",
        desc="Seu movimento entrou na rua e no feed. A campanha respira melhor por alguns dias.",
        duration=days,
        daily={"intent": 0.6, "media": 1.4, "viral": 2.0, "momentum": 0.6},
        severity="good",
    )


def cons_tse_pressure():
    return Consequence(
        key="tse_pressure",
        title="Pressão do TSE",
        desc="A campanha entrou no radar jurídico. Daqui em diante, qualquer tropeço pesa em dobro.",
        duration=3,
        daily={"risk": 2.7, "credibility": -0.8},
        severity="danger",
        followup_event="f_tse_julgamento",
        followup_chance=0.42,
    )


def cons_allies_uneasy():
    return Consequence(
        key="allies_uneasy",
        title="Aliados desconfiados",
        desc="Sua base virou um grupo de mensagens com facas. O apoio existe, mas ficou caro.",
        duration=3,
        daily={"allies": -1.8, "governabilidade": -1.2, "cash": -3500},
        severity="warning",
        followup_event="f_rebeliao_base",
        followup_chance=0.34,
    )


def cons_cash_breath(days: int = 3):
    return Consequence(
        key=f"cash_breath_{days}",
        title="Fôlego de caixa",
        desc="A operação financeira entrou no eixo. Você ainda gasta, mas deixa de sangrar tanto.",
        duration=days,
        daily={"cash": 9000, "energy": -1.0},
        severity="good",
    )


def cons_burnout():
    return Consequence(
        key="burnout",
        title="Esgotamento",
        desc="Você quis abraçar o Brasil em 24 horas. O corpo está cobrando.",
        duration=3,
        daily={"energy": -4.0, "credibility": -0.3},
        severity="danger",
        followup_event="f_falha_no_palco",
        followup_chance=0.30,
    )


def cons_small_recovery():
    return Consequence(
        key="small_recovery",
        title="Recuperação tática",
        desc="Você tirou o pé sem desaparecer. A campanha continua viva e com menos tosse.",
        duration=2,
        daily={"energy": 3.0, "risk": -0.7},
        severity="good",
    )


def cons_regional_push(region: str):
    return Consequence(
        key=f"push_{region}",
        title=f"Onda regional em {region}",
        desc=f"A agenda bateu bem em {region}. Não decide a eleição sozinha, mas vira mapa.",
        duration=3,
        daily={region: 1.3, "intent": 0.2},
        severity="good",
    )


def cons_rejection_echo():
    return Consequence(
        key="rejection_echo",
        title="Rastro de rejeição",
        desc="A decisão desagradou um grupo e isso não some de um dia para o outro.",
        duration=3,
        daily={"rejection": 0.8, "intent": -0.3},
        severity="warning",
    )


# =========================================================
# EVENTOS — FÁBRICA
# =========================================================
def ev(eid, title, desc, category, tone, phase, tags, options, followup_only=False):
    return EventCard(
        id=eid, title=title, desc=desc, category=category, tone=tone,
        phase=phase, tags=tags, options=options, followup_only=followup_only
    )


def op(text, summary, effects, risky=False, requirement=None, consequences=None):
    return Option(
        text=text,
        summary=summary,
        effects=effects,
        risky=risky,
        requirement=requirement,
        consequences=consequences or [],
    )


def build_events() -> List[EventCard]:
    events: List[EventCard] = []

    # -------- Handcrafted macro events --------
    events.extend([
        ev(
            "debate_nacional",
            "📺 Debate presidencial em rede nacional",
            "Você entra ao vivo com audiência massiva. Um bom desempenho vira corte. Um tropeço vira meme, editorial e grupo da família.",
            "midia", "neutral", "mid_late", ["Debate", "TV", "Nacional"],
            [
                op("Entrar agressivo e confrontar com dados", "Você cresceu com a base e virou assunto, mas passou perto de soar irritado.",
                   {"intent": 2.5, "media": 6, "energy": -10, "credibility": 2, "viral": 6, "rejection": 0.7}),
                op("Ser didático, calmo e presidencial", "Você pareceu seguro. Não explodiu, mas deixou menos munição para adversários.",
                   {"intent": 1.8, "media": 4, "energy": -8, "credibility": 4, "rejection": -0.6, "momentum": 1},
                   consequences=[cons_organic_wave(2)]),
                op("Improvisar frases de efeito e atacar todo mundo", "Você pode viralizar ou parecer descontrolado. Foi um lance de alto risco.",
                   {"intent": 3.0, "media": 8, "energy": -12, "viral": 10, "risk": 5, "rejection": 2.2},
                   risky=True, consequences=[cons_media_negative(), cons_rejection_echo()]),
            ],
        ),
        ev(
            "entrevista_jn",
            "🎙️ Sabatina dura no telejornal",
            "A entrevista não foi marcada para te abraçar. A pauta vem com inflação, corrupção, fake news e promessas inexequíveis.",
            "midia", "crisis", "early_mid", ["Entrevista", "Telejornal"],
            [
                op("Responder com transparência e admitir limites", "Você ganhou credibilidade porque não vendeu milagre.",
                   {"credibility": 5, "media": 3, "intent": 1.0, "energy": -7, "rejection": -0.5}),
                op("Bater no entrevistador e falar em perseguição", "Sua base gostou, mas a rejeição em moderados subiu.",
                   {"intent": 1.2, "media": 2, "viral": 4, "energy": -7, "rejection": 1.8, "credibility": -2},
                   risky=True, consequences=[cons_media_negative(2)]),
                op("Levar números, plano e exemplos concretos", "Foi técnico, sóbrio e difícil de desmontar.",
                   {"intent": 1.7, "credibility": 4, "media": 4, "energy": -8, "classe_media": 3, "servidores": 2}),
            ],
        ),
        ev(
            "escandalo_aliado",
            "🚨 Aliado da coligação cai em operação",
            "A PF amanheceu na casa de um aliado. Seu telefone toca sem parar e o noticiário quer saber se você vai bancar ou cortar.",
            "politica", "crisis", "mid_late", ["Escândalo", "Aliados"],
            [
                op("Romper publicamente e exigir apuração total", "Você perdeu conforto político, mas preservou a própria pele.",
                   {"intent": 2, "credibility": 5, "allies": -8, "governabilidade": -3, "risk": -3, "rejection": -0.4},
                   consequences=[cons_allies_uneasy()]),
                op("Esperar fatos e falar em presunção de inocência", "Soou cauteloso, porém frio demais para quem queria posição rápida.",
                   {"intent": -1.0, "credibility": -2, "allies": 2, "risk": 2, "rejection": 1.2},
                   consequences=[cons_media_negative(2)]),
                op("Defender o aliado e atacar a operação", "Você comprou a crise inteira. Pode segurar base, mas o custo é pesado.",
                   {"allies": 6, "intent": -2, "credibility": -5, "risk": 9, "rejection": 3.0, "media": -4},
                   risky=True, consequences=[cons_media_negative(), cons_tse_pressure()]),
            ],
        ),
        ev(
            "whatsapp_vaza",
            "📱 Áudio vazado no WhatsApp",
            "Um trecho fora de contexto explode no zap e em canais de Telegram. O corte parece pior do que o áudio completo.",
            "digital", "crisis", "all", ["WhatsApp", "Vazamento", "Viral"],
            [
                op("Divulgar o áudio completo e contextualizar", "Você estancou parte do dano e recuperou controle do assunto.",
                   {"credibility": 3, "media": 2, "viral": 3, "risk": -1, "energy": -5},
                   consequences=[cons_organic_wave(2)]),
                op("Processar, notificar e remover conteúdo", "É o caminho mais institucional, mas o meme continua vivo por algumas horas.",
                   {"risk": -2, "credibility": 2, "cash": -12000, "energy": -4},
                   requirement={"cash": 15000}),
                op("Ignorar e tocar agenda", "Você economizou energia no curto prazo, mas a narrativa ficou com os outros.",
                   {"energy": 2, "intent": -1.3, "credibility": -2, "rejection": 1.4},
                   consequences=[cons_media_negative(2)]),
            ],
        ),
        ev(
            "pesquisa_ruim",
            "📉 Nova pesquisa te coloca abaixo do esperado",
            "Saiu tracking com você estacionado. Analistas falam em teto. Adversários já estão distribuindo gráfico em loop.",
            "pesquisa", "crisis", "mid_late", ["Pesquisa", "Tracking"],
            [
                op("Mudar mensagem e concentrar fogo em indecisos", "Você corrigiu a rota em vez de fingir que nada aconteceu.",
                   {"intent": 2.0, "media": 2, "cash": -8000, "energy": -5, "momentum": 1},
                   consequences=[cons_organic_wave(2)]),
                op("Desqualificar a pesquisa e falar com a base", "Seu eleitor fiel comprou. O resto achou chororô.",
                   {"viral": 4, "intent": 0.5, "credibility": -3, "rejection": 1.2}),
                op("Fazer caravana emergencial em estados-chave", "Você sobe com território, mas paga em caixa e energia.",
                   {"Nordeste": 3, "Sudeste": 2, "intent": 1.8, "cash": -18000, "energy": -9},
                   consequences=[cons_burnout()]),
            ],
        ),
        ev(
            "enchente_nacional",
            "🌧️ Tragédia climática domina o noticiário",
            "Enchentes severas atingem cidades importantes. A eleição pausa por algumas horas e a resposta humana vale mais que discurso.",
            "social", "crisis", "mid_late", ["Clima", "Emergência"],
            [
                op("Suspender agenda eleitoral e ir para a linha de frente", "A decisão foi humana e politicamente madura.",
                   {"credibility": 5, "intent": 2.2, "media": 3, "energy": -8, "cash": -10000, "rejection": -0.6},
                   consequences=[cons_regional_push("Sul")]),
                op("Anunciar fundo emergencial e plano de resposta", "Você ocupou espaço com proposta concreta e ganhou respeito técnico.",
                   {"credibility": 4, "intent": 1.4, "cash": -18000, "energy": -5, "servidores": 2, "classe_media": 2},
                   requirement={"cash": 25000}),
                op("Manter comício e citar a tragédia rapidamente", "Pegou muito mal. Ninguém quer candidato parecendo blindado ao sofrimento.",
                   {"intent": -3, "credibility": -5, "media": -3, "rejection": 2.8},
                   risky=True, consequences=[cons_media_negative(), cons_rejection_echo()]),
            ],
        ),
        ev(
            "greve_caminhoneiros",
            "🚚 Ameaça de paralisação logística",
            "Frete, combustível e abastecimento viram pauta nacional. Um posicionamento mal calibrado te corta em grupos diferentes.",
            "economia", "neutral", "mid_late", ["Economia", "Transporte"],
            [
                op("Negociar transição e compensação fiscal responsável", "Você soou adulto e evitou parecer improviso.",
                   {"credibility": 4, "classe_media": 2, "empreendedores": 2, "agro": 1, "intent": 1.2}),
                op("Prometer redução imediata e ampla de impostos", "A ideia é popular, mas o mercado e analistas apertaram.",
                   {"intent": 2.0, "media": 2, "credibility": -2, "rejection": 0.7, "risk": 2, "empreendedores": -2}),
                op("Comprar confronto e chamar a mobilização de chantagem", "Parte do eleitorado aprovou a firmeza; outra parte viu arrogância.",
                   {"intent": 0.6, "agro": -3, "empreendedores": -2, "rejection": 1.8, "viral": 3}),
            ],
        ),
        ev(
            "tse_propaganda",
            "⚖️ Representação no TSE por propaganda irregular",
            "Adversários apontam uso indevido de peça impulsionada. O caso ainda não te derruba, mas pode virar bola de neve.",
            "juridico", "crisis", "mid_late", ["TSE", "Jurídico", "Propaganda"],
            [
                op("Retirar a peça, pedir auditoria e responder tecnicamente", "Você cortou a hemorragia e ficou menos vulnerável.",
                   {"risk": -6, "credibility": 3, "cash": -6000, "energy": -3},
                   consequences=[cons_small_recovery()]),
                op("Dobrar a aposta e chamar de censura", "Pode animar militância, mas abriu flanco sério.",
                   {"viral": 6, "intent": 1.0, "risk": 9, "credibility": -3, "rejection": 1.4},
                   risky=True, consequences=[cons_tse_pressure()]),
                op("Empurrar para a equipe e fingir normalidade", "A ausência de comando transmite improviso.",
                   {"risk": 4, "credibility": -2, "media": -1},
                   consequences=[cons_tse_pressure()]),
            ],
        ),
        ev(
            "doadores",
            "💸 Grandes doadores querem entrar pesado",
            "Empresários sinalizam recursos dentro da lei, mas a narrativa da independência vai para o teste de estresse.",
            "financas", "neutral", "early_mid", ["Doação", "Caixa"],
            [
                op("Aceitar dentro da lei, com transparência total", "O caixa respirou e você não precisou entrar em gambiarra.",
                   {"cash": 45000, "credibility": 1, "media": 1, "empreendedores": 2},
                   consequences=[cons_cash_breath()]),
                op("Recusar e focar em microdoação", "Você reforçou a imagem de autonomia, mas o dinheiro entra mais devagar.",
                   {"credibility": 4, "viral": 3, "cash": 10000, "intent": 1.0}),
                op("Criar arranjo informal e torcer para não aparecer", "Nem pensar. Isso pode até aliviar o caixa, mas a bomba vem.",
                   {"cash": 70000, "risk": 14, "credibility": -5, "rejection": 2},
                   risky=True, consequences=[cons_tse_pressure(), cons_media_negative()]),
            ],
        ),
        ev(
            "pastores_apoio",
            "⛪ Lideranças religiosas pedem compromisso público",
            "Apoios relevantes querem declaração firme sobre costumes e liberdade religiosa. Cada palavra desloca grupos diferentes.",
            "segmento", "neutral", "all", ["Valores", "Religião"],
            [
                op("Assumir compromissos institucionais sem guerra cultural", "Você segurou pontes sem incendiar o centro.",
                   {"evangelicos": 4, "classe_media": 1, "credibility": 2, "rejection": -0.3}),
                op("Ir com tudo na pauta moral", "Mobiliza fortemente um lado e abre rejeição em outro.",
                   {"evangelicos": 6, "viral": 3, "jovens": -3, "rejection": 1.6}),
                op("Escapar da pauta e falar só de economia", "Pareceu cálculo frio. Não perde tudo, mas não cola.",
                   {"evangelicos": -2, "empreendedores": 2, "credibility": -1}),
            ],
        ),
        ev(
            "apoio_governador",
            "🏛️ Governador popular oferece palanque",
            "Um governador competitivo quer te abraçar em agenda conjunta. É força de máquina, mas também dívida política futura.",
            "politica", "good", "mid_late", ["Palanque", "Aliança"],
            [
                op("Aceitar e montar agenda intensa", "Você ganhou capilaridade e TV regional, ao custo de autonomia.",
                   {"allies": 7, "governabilidade": 5, "time_tv": 3, "intent": 1.4, "cash": -7000},
                   consequences=[cons_regional_push("Nordeste")]),
                op("Aceitar, mas limitar acenos programáticos", "Equilíbrio bom entre ganho eleitoral e independência.",
                   {"allies": 4, "governabilidade": 3, "intent": 1.2, "credibility": 1}),
                op("Recusar para não parecer dependente", "Você preservou marca própria, mas abriu chance para rival ocupar espaço.",
                   {"credibility": 1, "allies": -3, "Sudeste": -1, "Nordeste": -2}),
            ],
        ),
        ev(
            "voto_util_final",
            "🗳️ Pressão por voto útil cresce",
            "Analistas e eleitores começam a escolher entre viabilidade e afinidade. A reta final perdoa menos a teimosia.",
            "pesquisa", "neutral", "final", ["Reta final", "Voto útil"],
            [
                op("Falar em união e viabilidade com humildade", "Você captou parte do voto útil sem parecer desesperado.",
                   {"intent": 2.8, "credibility": 3, "media": 2, "rejection": -0.6},
                   consequences=[cons_organic_wave(2)]),
                op("Dobrar o tom e dizer que só você pode vencer", "Pode trazer impulso, mas a linha é fina entre força e desespero.",
                   {"intent": 2.0, "viral": 4, "rejection": 1.2, "credibility": -1}),
                op("Ignorar a conversa e repetir jingle", "Você deixou uma janela estratégica aberta.",
                   {"intent": -1.5, "media": -1, "momentum": -1}),
            ],
        ),
        ev(
            "fadiga_campanha",
            "😵 Seu corpo começou a cobrar",
            "Agenda, estrada, debate, live, bastidor. Você sente a campanha entrando na medula.",
            "energia", "crisis", "all", ["Energia", "Saúde"],
            [
                op("Tirar uma noite real de descanso e reduzir agenda", "Você recuperou motor e manteve a campanha respirando.",
                   {"energy": 9, "intent": -0.3, "media": -1},
                   consequences=[cons_small_recovery(), cons_small_recovery()]),
                op("Seguir no limite porque faltar agora é morrer", "No curto prazo você não some, mas o corpo pode sabotar.",
                   {"intent": 0.8, "media": 1, "energy": -7},
                   consequences=[cons_burnout()]),
                op("Delegar agendas e fazer aparições cirúrgicas", "Boa gestão de energia sem cara de abandono.",
                   {"energy": 6, "credibility": 1, "media": 1, "cash": -5000}),
            ],
        ),
        ev(
            "caixa_critico_event",
            "💳 O financeiro acendeu o alerta vermelho",
            "A campanha está gastando como se a eleição fosse amanhã, mas ainda há estrada pela frente.",
            "financas", "crisis", "all", ["Caixa", "Operação"],
            [
                op("Cortar eventos caros e priorizar digital", "Você estabilizou o caixa e ganhou eficiência.",
                   {"cash": 22000, "viral": 4, "media": 1, "intent": 0.8},
                   consequences=[cons_cash_breath(2)]),
                op("Fazer jantar de arrecadação e ligar para doadores", "Resolve bem o caixa, mas te prende com gente poderosa.",
                   {"cash": 38000, "allies": 2, "credibility": -1, "energy": -3}),
                op("Manter tudo igual e confiar que entra depois", "Isso raramente termina bonito.",
                   {"cash": -12000, "energy": -2, "risk": 2},
                   consequences=[cons_allies_uneasy()]),
            ],
        ),
    ])

    # -------- Generated media events --------
    media_topics = [
        ("podcast_gigante", "🎧 Podcast gigante quer entrevista de 2 horas", "Uma conversa longa pode humanizar ou escancarar contradições.", "all"),
        ("radio_popular", "📻 Rádio popular abre microfone no interior", "A audiência é massiva e espalhada, com potencial real de voto.", "early_mid"),
        ("editorial_jornal", "🗞️ Editorial cobra clareza sobre seu plano", "Você foi citado nominalmente e precisa reagir.", "mid_late"),
        ("debate_universitario", "🎓 Debate em universidade viraliza entre jovens", "Perguntas duras, recortes rápidos e ambiente hostil a respostas vazias.", "mid"),
        ("sabatina_empresarial", "🏢 Sabatina com empresários e investidores", "Mercado quer previsibilidade, não slogan.", "mid_late"),
        ("programa_popular", "📺 Programa popular quer te colocar na rua", "Contato com o povão, risco alto de parecer artificial.", "all"),
        ("live_influencer", "📱 Influenciador gigante convida para live", "Pode furar bolha ou virar constrangimento em segundos.", "all"),
        ("documentario_passado", "🎬 Documentário resgata fala antiga sua", "Arquivo velho ganhou vida nova no timing errado.", "late_final"),
    ]
    for eid, title, desc, phase in media_topics:
        events.append(
            ev(
                eid, title, desc, "midia", "neutral", phase, ["Mídia", "Narrativa"],
                [
                    op("Aceitar e preparar mensagem simples, humana e repetível",
                       "Você entrou com disciplina e saiu com ganhos mais sustentáveis.",
                       {"intent": 1.4, "media": 3, "credibility": 2, "energy": -5, "viral": 2}),
                    op("Ir para bater, viralizar e dominar o assunto",
                       "Você ganhou repercussão, mas também deixou mais arestas abertas.",
                       {"intent": 1.7, "media": 4, "viral": 5, "energy": -6, "rejection": 0.8},
                       risky=True, consequences=[cons_media_negative(2)] if "documentario" in eid else []),
                    op("Recusar e concentrar a agenda em território aliado",
                       "Você preservou tempo, mas perdeu vitrine e entregou a pauta de mão beijada.",
                       {"energy": 2, "media": -2, "intent": -0.5, "momentum": -1}),
                ]
            )
        )

    # -------- Economy and social --------
    econ_events = [
        ("preco_alimentos", "🥖 Alta de alimentos domina a conversa da semana", "Toda entrevista vira custo de vida e geladeira.", "all"),
        ("dolar_sobe", "💵 Dólar dispara e mercado entra em modo tensão", "Suas falas econômicas agora movem humor de investidor e de classe média.", "mid_late"),
        ("apagao_regional", "💡 Apagão regional gera caos e irritação", "O assunto entra em serviços, infraestrutura e governo.", "all"),
        ("seca_agro", "🌾 Seca afeta produção e humor do agro", "Centro-Oeste e Sul passam a ouvir soluções práticas, não poesia.", "mid_late"),
        ("fila_saude", "🏥 Imagens de filas na saúde viralizam", "A pauta social volta com força e pede resposta concreta.", "all"),
        ("seguranca_explode", "🚔 Crise de segurança domina telejornais", "O eleitor quer firmeza sem delírio punitivista.", "mid_late"),
        ("tarifa_transporte", "🚌 Reajuste no transporte vira revolta urbana", "Tema colado em periferia, trabalhador e jovens.", "early_mid"),
        ("greve_servidores", "🗂️ Greve de servidores pressiona seu discurso", "Qualquer fala apressada machuca um grupo relevante.", "all"),
    ]
    for eid, title, desc, phase in econ_events:
        seg_a = "periferia" if "transporte" in eid or "saude" in eid else "classe_media"
        seg_b = "agro" if "seca" in eid else "servidores" if "servidores" in eid else "empreendedores"
        reg = "Nordeste" if "seca" in eid else "Sudeste" if "transporte" in eid or "dolar" in eid else "Sul"
        events.append(
            ev(
                eid, title, desc, "economia", "neutral", phase, ["Realidade", "Brasil real"],
                [
                    op("Responder com proposta concreta, custo estimado e cronograma",
                       "Você não vendeu mágica e isso foi percebido como maturidade.",
                       {"intent": 1.3, "credibility": 4, seg_a: 3, seg_b: 2, reg: 2, "energy": -4}),
                    op("Bater no governo atual/anterior e simplificar a culpa",
                       "Funciona um pouco no curto prazo, mas parece vazio se usado demais.",
                       {"intent": 1.0, "viral": 3, "credibility": -1, "rejection": 0.6}),
                    op("Prometer solução ampla e imediata sem explicar conta",
                       "A frase cola, mas o custo na credibilidade vem em seguida.",
                       {"intent": 1.8, "media": 2, "credibility": -3, "rejection": 1.0, "risk": 2},
                       risky=True, consequences=[cons_media_negative(2)]),
                ]
            )
        )

    # -------- Coalitions and territory --------
    territory_events = [
        ("caravana_nordeste", "🌵 Caravana no Nordeste lota agenda", "Interior, rádio, lideranças locais e calor político de verdade.", "Nordeste", "periferia", "early_mid"),
        ("agro_show", "🚜 Feira do agro concentra atores pesados", "Você entra numa arena onde frase errada custa meses.", "Centro-Oeste", "agro", "mid_late"),
        ("favela_tour", "🏘️ Agenda em comunidade com alto simbolismo", "Pode gerar conexão real ou parecer turismo eleitoral.", "Sudeste", "periferia", "all"),
        ("sul_industrial", "🏭 Setor industrial do Sul cobra previsibilidade", "Menos ideologia, mais planilha e energia barata.", "Sul", "empreendedores", "mid_late"),
        ("norte_ambiental", "🌳 Pressão por agenda amazônica ganha corpo", "Tema mistura soberania, emprego e imagem internacional.", "Norte", "jovens", "mid_late"),
        ("interior_mg", "🛣️ Giro em cidades médias vira termômetro da campanha", "A política do Brasil profundo aparece sem filtro.", "Sudeste", "classe_media", "all"),
        ("sertao_agua", "💧 Pauta de água e infraestrutura domina o sertão", "A resposta precisa ser humana e executável.", "Nordeste", "servidores", "mid_late"),
        ("porto_sul", "🚢 Debate sobre logística e porto mobiliza empresários", "Tema técnico, mas com voto e manchete por trás.", "Sul", "empreendedores", "mid_late"),
    ]
    for eid, title, desc, region, segment, phase in territory_events:
        events.append(
            ev(
                eid, title, desc, "territorio", "good", phase, ["Território", region],
                [
                    op("Ir com agenda local, ouvir demandas e entregar solução factível",
                       "Você acertou o tom e ganhou lastro regional de verdade.",
                       {region: 4, segment: 4, "intent": 1.3, "credibility": 2, "cash": -9000, "energy": -5},
                       consequences=[cons_regional_push(region)]),
                    op("Chegar com discurso nacional pronto e empacotado",
                       "A agenda aconteceu, mas sem a potência que poderia ter tido.",
                       {region: 1.5, "intent": 0.5, "energy": -3}),
                    op("Transformar a agenda em guerra cultural ou briga de bolha",
                       "Vira corte, só que corta também pontes locais importantes.",
                       {region: -1.5, segment: 1.5, "viral": 4, "rejection": 1.0, "credibility": -2},
                       risky=True),
                ]
            )
        )

    # -------- Digital and misinformation --------
    digital_events = [
        ("meme_favoravel", "😂 Um meme favorável estoura nas redes", "A internet decidiu brincar a seu favor por 24 horas.", "all"),
        ("deepfake", "🧠 Vídeo manipulado começa a circular", "A peça é falsa, mas o algoritmo ama confusão.", "all"),
        ("tiktok_jovens", "📲 Trend no TikTok pode te colocar em outra faixa etária", "Oportunidade enorme de alcance com risco de vergonha alheia.", "all"),
        ("telegram_dossie", "📁 Dossiê apócrifo corre em canais políticos", "Meio da internet trata como prova, meio trata como fanfic.", "mid_late"),
        ("bots_hashtag", "🤖 Hashtag suspeita sobe associada ao seu nome", "Você precisa decidir entre negar, aproveitar ou auditar.", "all"),
        ("corte_podcast", "✂️ Corte de 20 segundos domina o algoritmo", "O corte te ajuda, mas simplifica demais o que foi dito.", "all"),
        ("ex_assessor_vaza", "🧾 Ex-assessor publica fio contra sua campanha", "Ninguém sabe se ele é ressentido ou informante. O dano vem da dúvida.", "mid_late"),
        ("live_flopou", "📉 Sua live principal flopou", "A equipe está em silêncio constrangido. O algoritmo foi cruel.", "early_mid"),
    ]
    for eid, title, desc, phase in digital_events:
        events.append(
            ev(
                eid, title, desc, "digital", "neutral", phase, ["Digital", "Rede"],
                [
                    op("Responder rápido, com equipe, contexto e formato certo",
                       "Velocidade e técnica seguraram boa parte do estrago ou ampliaram a chance.",
                       {"viral": 4, "media": 2, "credibility": 2, "energy": -3},
                       consequences=[cons_organic_wave(2)] if eid in {"meme_favoravel","corte_podcast","tiktok_jovens"} else []),
                    op("Entrar pessoalmente e improvisar na emoção",
                       "Você ganhou calor humano, mas improviso nem sempre casa com crise digital.",
                       {"viral": 5, "intent": 0.8, "energy": -5, "credibility": -1, "rejection": 0.7},
                       risky=True,
                       consequences=[cons_media_negative(2)] if eid in {"deepfake","telegram_dossie","ex_assessor_vaza","bots_hashtag"} else []),
                    op("Esperar a maré baixar e não alimentar o ciclo",
                       "Às vezes funciona. Às vezes o assunto cria raiz enquanto você observa.",
                       {"energy": 1, "viral": -1, "credibility": -0.8, "intent": -0.4}
                       if eid in {"deepfake","telegram_dossie","ex_assessor_vaza"} else
                       {"energy": 1, "viral": -0.2, "intent": -0.2}),
                ]
            )
        )

    # -------- Alliances and internal politics --------
    alliance_events = [
        ("centrao_cobra", "🧩 Partidos do centro querem espaço e compromisso", "Palanque vem com boleto político embutido.", "all"),
        ("prefeitos_reuniao", "🏘️ Reunião com prefeitos vira teste de capilaridade", "O interior não compra fumaça por muito tempo.", "early_mid"),
        ("senadores_duvida", "🏛️ Bancada importante hesita em te apoiar", "O sinal de elite política mexe no mercado e na percepção de viabilidade.", "mid_late"),
        ("federacao_prop", "🤝 Federação partidária oferece tempo de TV", "Mais TV e estrutura, mais amarração depois.", "mid_late"),
        ("base_insatisfeita", "😠 Sua base reclama de concessões ao centro", "Ganhar amplitude pode irritar quem te sustentou até aqui.", "mid_late"),
        ("vice_pressao", "🧷 Seu vice pede protagonismo e espaço no roteiro", "Recusar demais gera ruído; ceder demais te diminui.", "all"),
        ("governadores_neutros", "🧭 Governadores querem ficar neutros por enquanto", "Sem eles, sua campanha perde estrada em estados grandes.", "mid"),
        ("lider_sindical", "🛠️ Liderança sindical quer acordo público", "Ajuda em capilaridade, mas afasta alguns grupos.", "all"),
    ]
    for eid, title, desc, phase in alliance_events:
        events.append(
            ev(
                eid, title, desc, "politica", "neutral", phase, ["Política", "Coalizão"],
                [
                    op("Negociar sem entregar alma nem programa", "A articulação foi útil e não te deformou tanto.",
                       {"allies": 5, "governabilidade": 4, "time_tv": 2, "credibility": 1}),
                    op("Fechar acordo pesado para ganhar músculo imediato", "Você cresceu em estrutura, mas ficou mais dependente.",
                       {"allies": 8, "time_tv": 3, "intent": 1.0, "governabilidade": 5, "credibility": -1},
                       consequences=[cons_allies_uneasy()] if eid in {"base_insatisfeita","centrao_cobra","vice_pressao"} else []),
                    op("Bater o pé e manter pureza estratégica", "Preserva marca, mas perde estrada e telefone amigo.",
                       {"credibility": 2, "allies": -5, "time_tv": -2, "intent": -0.3}),
                ]
            )
        )

    # -------- Endgame events --------
    final_events = [
        ("fuga_de_votos", "🏃 Votos começam a migrar para candidatura viável", "Na reta final, gente que gosta de você pode decidir vencer sem você.", "final"),
        ("ataque_final", "🥊 Adversário guarda munição para ataque concentrado", "Uma ofensiva final quer te definir antes da urna.", "final"),
        ("carta_aberta", "📜 Intelectuais, artistas e economistas articulam carta aberta", "O simbolismo importa tanto quanto o conteúdo.", "final"),
        ("apoio_ultimo_segundo", "🚨 Apoio de última hora cai no seu colo", "Nem todo apoio tardio ajuda. Alguns parecem pânico.", "final"),
        ("erro_data", "🧭 Sua equipe erra dado em peça de reta final", "Erro bobo em hora cara custa mais do que devia.", "final"),
        ("telefone_sem_parar", "☎️ Todo mundo quer uma sinalização sua", "Mercado, base, partido, movimento social, empresariado. Todos no mesmo dia.", "final"),
        ("pesquisa_boca_urna", "📊 Tracking da véspera cria euforia e medo ao mesmo tempo", "O maior risco é agir como se a eleição já estivesse resolvida.", "final"),
        ("mobilizacao_urna", "🚌 Operação de mobilização para o dia do voto", "Última milha vale ouro e também dá problema se for mal organizada.", "final"),
    ]
    for eid, title, desc, phase in final_events:
        events.append(
            ev(
                eid, title, desc, "final", "neutral", phase, ["Reta final", "Decisão"],
                [
                    op("Ser disciplinado e fazer o básico muito bem feito", "Na reta final, o básico bem executado parece talento raro.",
                       {"intent": 1.6, "credibility": 2, "risk": -1, "energy": -4, "media": 1}),
                    op("Dobrar o volume e tentar uma arrancada emocional", "Pode encaixar e virar história, mas cobra caro se soar forçado.",
                       {"intent": 2.3, "viral": 4, "energy": -6, "rejection": 0.8},
                       risky=True),
                    op("Apostar tudo em guerra e confronto", "É o tipo de escolha que produz fãs e inimigos na mesma velocidade.",
                       {"intent": 1.0, "viral": 6, "credibility": -2, "rejection": 1.8, "risk": 3},
                       risky=True, consequences=[cons_media_negative(2)]),
                ]
            )
        )

    # -------- Follow-ups --------
    events.extend([
        ev(
            "f_tse_julgamento",
            "👨‍⚖️ Julgamento relâmpago no TSE",
            "O caso voltou em hora ruim. Agora o problema não é só jurídico: é simbólico.",
            "juridico", "crisis", "all", ["Follow-up", "TSE"],
            [
                op("Assumir erro operacional, corrigir e enquadrar a campanha", "Você não saiu ileso, mas evitou a imagem de reincidente.",
                   {"risk": -8, "credibility": 3, "cash": -8000, "media": 1}),
                op("Dobrar a briga pública contra a decisão", "Isso mobiliza nicho, mas estoura no centro da pista.",
                   {"viral": 4, "intent": 0.5, "risk": 10, "credibility": -4, "rejection": 1.3},
                   risky=True),
                op("Deixar o jurídico falar e sumir do tema", "Reduz ruído no curtíssimo prazo, mas soa pequeno.",
                   {"risk": -4, "credibility": -1, "media": -1}),
            ],
            followup_only=True,
        ),
        ev(
            "f_rebeliao_base",
            "🪓 Rebelião silenciosa na base aliada",
            "Sua coalizão segue contigo, mas sem sorriso e sem urgência. Cada agenda parece mais cara.",
            "politica", "crisis", "all", ["Follow-up", "Base"],
            [
                op("Abrir mesa política e redistribuir protagonismo", "Você comprou paz temporária, mas teve de ceder.",
                   {"allies": 6, "governabilidade": 4, "credibility": -0.5, "cash": -12000}),
                op("Mostrar força e enquadrar publicamente", "Pode funcionar uma vez. Na segunda já vira arrogância.",
                   {"allies": -4, "viral": 3, "rejection": 1.2, "governabilidade": -3},
                   risky=True),
                op("Trazer o vice e governadores para arbitrar", "A saída foi política e menos personalista.",
                   {"allies": 4, "governabilidade": 5, "media": 1}),
            ],
            followup_only=True,
        ),
        ev(
            "f_falha_no_palco",
            "😰 Você falha em evento por exaustão",
            "No palanque, o corpo entrega antes do discurso. A imagem corre mais rápido que a explicação.",
            "energia", "crisis", "all", ["Follow-up", "Energia"],
            [
                op("Assumir, repousar e retomar com disciplina", "Você humanizou o erro e cortou a espiral.",
                   {"energy": 8, "credibility": 2, "intent": 0.5, "media": 1},
                   consequences=[cons_small_recovery()]),
                op("Fingir normalidade e seguir no limite", "A campanha parece em piloto cego.",
                   {"energy": -6, "credibility": -2, "rejection": 0.8},
                   risky=True),
                op("Delegar agenda e soltar vídeo curto bem produzido", "Controlou o dano sem parecer sumiço.",
                   {"energy": 5, "media": 1, "credibility": 1}),
            ],
            followup_only=True,
        ),
    ])

    return events


EVENTS = build_events()

# =========================================================
# ESTADO
# =========================================================
def init_state(force: bool = False):
    defaults = {
        "started": False,
        "game_over": False,
        "victory": False,
        "first_turn": False,
        "result_text": "",
        "event": None,
        "last_feedback": "",
        "day": 1,
        "total_days": 45,
        "intent": 18.0,
        "rejection": 22.0,
        "credibility": 48.0,
        "cash": 135000.0,
        "energy": 76.0,
        "media": 42.0,
        "risk": 16.0,
        "allies": 44.0,
        "time_tv": 28.0,
        "momentum": 0.0,
        "narrative": 45.0,
        "viral": 18.0,
        "governabilidade": 35.0,
        "combo": 0,
        "max_combo": 0,
        "scandals": 0,
        "consequence_turns_survived": 0,
        "used_events": [],
        "followup_queue": [],
        "active_consequences": [],
        "achievements": [],
        "history": [],
        "regions": {k: 20.0 for k in REGIONS.keys()},
        "segments": {k: 20.0 for k in SEGMENTS.keys()},
        "rivals": {k: dict(v) for k, v in RIVAL_ARCHETYPES.items()},
        "poll_history": [18.0],
        "rej_history": [22.0],
        "cash_history": [135000.0],
        "energy_history": [76.0],
        "day_history": [1],
        "party": "centro",
        "advisor": "estrategista",
        "difficulty": "Normal",
        "seed": 2026,
        "post_presidency_mode": False,
    }
    for key, value in defaults.items():
        if force or key not in st.session_state:
            st.session_state[key] = value


def start_campaign(party: str, advisor: str, difficulty: str, seed: int):
    init_state(True)
    st.session_state.started = True
    st.session_state.party = party
    st.session_state.advisor = advisor
    st.session_state.difficulty = difficulty
    st.session_state.seed = seed
    random.seed(seed)

    # Partido
    if party == "popular":
        st.session_state.intent += 2.5
        st.session_state.regions["Nordeste"] += 5
        st.session_state.segments["periferia"] += 6
        st.session_state.segments["servidores"] += 2
    elif party == "liberal":
        st.session_state.cash += 25000
        st.session_state.segments["empreendedores"] += 7
        st.session_state.segments["agro"] += 4
        st.session_state.regions["Sudeste"] += 3
        st.session_state.rejection += 1.0
    elif party == "verde":
        st.session_state.credibility += 5
        st.session_state.segments["jovens"] += 5
        st.session_state.regions["Norte"] += 4
        st.session_state.intent += 1.0
    else:
        st.session_state.allies += 4
        st.session_state.time_tv += 3
        st.session_state.regions["Sudeste"] += 2
        st.session_state.segments["classe_media"] += 3

    # Assessor
    for k, v in ADVISORS[advisor]["start"].items():
        if k == "cash":
            st.session_state.cash += v
        elif k == "intent":
            st.session_state.intent += v
        elif k == "credibility":
            st.session_state.credibility += v
        elif k == "momentum":
            st.session_state.momentum += v
        elif k == "media":
            st.session_state.media += v
        elif k == "viral":
            st.session_state.viral += v
        elif k == "allies":
            st.session_state.allies += v
        elif k == "time_tv":
            st.session_state.time_tv += v
        elif k == "governabilidade":
            st.session_state.governabilidade += v
        elif k == "risk":
            st.session_state.risk += v

    # Dificuldade
    if difficulty == "Fácil":
        st.session_state.intent += 2
        st.session_state.cash += 25000
        st.session_state.energy += 8
        st.session_state.risk -= 3
    elif difficulty == "Difícil":
        st.session_state.intent -= 2
        st.session_state.cash -= 15000
        st.session_state.rejection += 2
        st.session_state.risk += 5
    elif difficulty == "Hardcore":
        st.session_state.intent -= 4
        st.session_state.cash -= 30000
        st.session_state.energy -= 8
        st.session_state.rejection += 4
        st.session_state.risk += 8

    # Clamp inicial
    st.session_state.intent = clamp(st.session_state.intent, 8, 35)
    st.session_state.rejection = clamp(st.session_state.rejection, 8, 45)
    st.session_state.credibility = clamp(st.session_state.credibility, 25, 80)
    st.session_state.energy = clamp(st.session_state.energy, 35, 95)
    st.session_state.media = clamp(st.session_state.media, 20, 80)
    st.session_state.risk = clamp(st.session_state.risk, 0, 60)
    st.session_state.allies = clamp(st.session_state.allies, 20, 80)
    st.session_state.time_tv = clamp(st.session_state.time_tv, 10, 80)
    st.session_state.governabilidade = clamp(st.session_state.governabilidade, 15, 80)

    generate_event()


# =========================================================
# MOTOR
# =========================================================
def add_history(title: str, option_text: str):
    st.session_state.history.append({"dia": st.session_state.day, "evento": title, "decisao": option_text})
    st.session_state.history = st.session_state.history[-12:]


def available_events() -> List[EventCard]:
    current_phase = phase_for_day(st.session_state.day, st.session_state.total_days)
    used = set(st.session_state.used_events)
    pool = [
        e for e in EVENTS
        if not e.followup_only
        and phase_matches(e.phase, current_phase)
        and e.id not in used
    ]
    if len(pool) < 6:
        pool.extend([
            e for e in EVENTS
            if not e.followup_only and e.id not in used
        ])
    return pool


def generate_event():
    if st.session_state.followup_queue:
        next_id = st.session_state.followup_queue.pop(0)
        for e in EVENTS:
            if e.id == next_id:
                st.session_state.event = e
                return
    pool = available_events()
    weights = []
    for e in pool:
        w = 1.0
        if e.category == "juridico" and st.session_state.risk > 35:
            w += 0.8
        if e.category == "digital" and st.session_state.viral > 26:
            w += 0.4
        if e.category == "financas" and st.session_state.cash < 60000:
            w += 0.7
        if e.category == "energia" and st.session_state.energy < 38:
            w += 0.8
        if e.category == "politica" and st.session_state.allies < 42:
            w += 0.6
        if e.category == "pesquisa" and st.session_state.day > 18:
            w += 0.4
        weights.append(w)
    st.session_state.event = random.choices(pool, weights=weights, k=1)[0]


def apply_effects(effects: Dict[str, float], risky: bool = False):
    if not effects:
        return
    s = st.session_state
    s.intent = clamp(s.intent + effects.get("intent", 0), 0, 70)
    s.rejection = clamp(s.rejection + effects.get("rejection", 0), 0, 85)
    s.credibility = clamp(s.credibility + effects.get("credibility", 0), 0, 100)
    s.cash = max(0.0, s.cash + effects.get("cash", 0))
    s.energy = clamp(s.energy + effects.get("energy", 0), 0, 100)
    s.media = clamp(s.media + effects.get("media", 0), 0, 100)
    s.risk = clamp(s.risk + effects.get("risk", 0), 0, 100)
    s.allies = clamp(s.allies + effects.get("allies", 0), 0, 100)
    s.time_tv = clamp(s.time_tv + effects.get("time_tv", 0), 0, 100)
    s.momentum = clamp(s.momentum + effects.get("momentum", 0), -20, 20)
    s.narrative = clamp(s.narrative + effects.get("narrative", 0), 0, 100)
    s.viral = clamp(s.viral + effects.get("viral", 0), 0, 100)
    s.governabilidade = clamp(s.governabilidade + effects.get("governabilidade", 0), 0, 100)

    for region in REGIONS.keys():
        if region in effects:
            apply_delta_to_map(s.regions, region, effects[region], 85)
    for seg in SEGMENTS.keys():
        if seg in effects:
            apply_delta_to_map(s.segments, seg, effects[seg], 85)

    # Spillovers
    if effects.get("periferia"):
        apply_delta_to_map(s.regions, "Nordeste", effects["periferia"] * 0.25, 85)
        apply_delta_to_map(s.regions, "Sudeste", effects["periferia"] * 0.15, 85)
    if effects.get("agro"):
        apply_delta_to_map(s.regions, "Centro-Oeste", effects["agro"] * 0.30, 85)
        apply_delta_to_map(s.regions, "Sul", effects["agro"] * 0.25, 85)
    if effects.get("empreendedores"):
        apply_delta_to_map(s.regions, "Sudeste", effects["empreendedores"] * 0.25, 85)
    if effects.get("evangelicos"):
        apply_delta_to_map(s.regions, "Nordeste", effects["evangelicos"] * 0.18, 85)
    if effects.get("jovens"):
        s.viral = clamp(s.viral + effects["jovens"] * 0.22, 0, 100)
    if risky and (effects.get("risk", 0) > 0 or effects.get("rejection", 0) > 0.6):
        s.scandals += 1

    positive_score = effects.get("intent", 0) + effects.get("credibility", 0) / 3 + effects.get("media", 0) / 5 - effects.get("rejection", 0)
    if positive_score > 1.2:
        s.combo += 1
    else:
        s.combo = max(0, s.combo - 1)
    s.max_combo = max(s.max_combo, s.combo)
    if s.combo >= 3:
        s.momentum = clamp(s.momentum + 1.0, -20, 20)


def add_consequence(cons: Consequence):
    st.session_state.active_consequences.append({
        "key": cons.key,
        "title": cons.title,
        "desc": cons.desc,
        "days_left": cons.duration,
        "daily": dict(cons.daily),
        "end_effects": dict(cons.end_effects),
        "severity": cons.severity,
        "followup_event": cons.followup_event,
        "followup_chance": cons.followup_chance,
        "triggered_followup": False,
    })


def process_consequences() -> List[str]:
    notes = []
    remaining = []
    for cons in st.session_state.active_consequences:
        apply_effects(cons["daily"])
        cons["days_left"] -= 1
        st.session_state.consequence_turns_survived += 1
        notes.append(f"{cons['title']} ainda está em campo.")
        if cons["followup_event"] and not cons["triggered_followup"]:
            if random.random() < cons["followup_chance"]:
                st.session_state.followup_queue.append(cons["followup_event"])
                cons["triggered_followup"] = True
                notes.append("O efeito escalou e gerou um novo problema.")
        if cons["days_left"] <= 0:
            apply_effects(cons["end_effects"])
        else:
            remaining.append(cons)
    st.session_state.active_consequences = remaining
    return notes


def rival_turn():
    s = st.session_state
    for _, rival in s.rivals.items():
        drift = random.uniform(-0.6, 0.8)
        if rival["perfil"] == "digital":
            drift += 0.15 if s.viral < 24 else -0.05
        if rival["perfil"] == "gestao":
            drift += 0.14 if s.credibility < 48 else -0.04
        if rival["perfil"] == "estrutura":
            drift += 0.12 if s.allies < 46 else -0.04
        if s.day > 34:
            drift += random.uniform(-0.4, 0.6)
        rival["voto"] = clamp(rival["voto"] + drift, 8, 42)
        rival["rejeicao"] = clamp(rival["rejeicao"] + random.uniform(-0.5, 0.7), 10, 60)


def daily_cost_model():
    s = st.session_state
    # custo base cresce com a proximidade da eleição, mídia e estrutura
    phase_factor = 1.0 + (s.day / s.total_days) * 0.55
    operation = 4200 + (s.time_tv * 38) + (s.allies * 22) + (s.media * 18)
    burn = operation * 0.20 * phase_factor
    if s.difficulty == "Difícil":
        burn *= 1.08
    elif s.difficulty == "Hardcore":
        burn *= 1.16
    s.cash = max(0.0, s.cash - burn)

    # energia: sobe e desce conforme qualidade da gestão
    energy_drop = 2.4 + (s.media / 80) + (s.day / s.total_days) * 1.8
    if s.energy < 30:
        energy_drop -= 0.6
    s.energy = clamp(s.energy - energy_drop, 0, 100)

    # mídia, risco e intenção oscilam com momentum e credibilidade
    s.media = clamp(s.media + random.uniform(-1.6, 1.8) + s.momentum * 0.08, 0, 100)
    s.risk = clamp(s.risk + random.uniform(-0.6, 1.4) - s.credibility * 0.008, 0, 100)

    region_avg = sum(s.regions.values()) / len(s.regions)
    seg_avg = sum(s.segments.values()) / len(s.segments)
    trend = (
        (region_avg - 24) * 0.025
        + (seg_avg - 24) * 0.020
        + (s.media - 45) * 0.018
        + (s.credibility - s.rejection) * 0.010
        + s.momentum * 0.09
        - max(0, s.risk - 35) * 0.045
    )
    if s.day >= 36:
        trend += (s.viral - 18) * 0.012  # voto útil / reta final
    s.intent = clamp(s.intent + trend + random.uniform(-0.5, 0.7), 3, 60)

    # rejeição tende a subir um pouco com exposição
    exposure = (s.media + s.viral) / 120
    s.rejection = clamp(s.rejection + random.uniform(-0.4, 0.5) + exposure * 0.18 - s.credibility * 0.004, 4, 80)

    # pequeno ganho de caixa se campanha estiver muito bem organizada
    if s.cash < 55000 and s.credibility > 54 and s.risk < 30:
        s.cash += 5000


def unlock_achievements():
    s = st.session_state
    if s.history and "primeira_escolha" not in s.achievements:
        s.achievements.append("primeira_escolha")
    if s.cash >= 180000 and "caixa_forte" not in s.achievements:
        s.achievements.append("caixa_forte")
    if s.energy >= 75 and s.day >= 18 and "campanha_viva" not in s.achievements:
        s.achievements.append("campanha_viva")
    if s.media >= 72 and "mestre_midia" not in s.achievements:
        s.achievements.append("mestre_midia")
    if s.risk <= 12 and s.day >= 20 and "blindado" not in s.achievements:
        s.achievements.append("blindado")
    if s.max_combo >= 4 and "furacao" not in s.achievements:
        s.achievements.append("furacao")
    if s.regions["Nordeste"] >= 40 and "lider_nordeste" not in s.achievements:
        s.achievements.append("lider_nordeste")
    if s.regions["Sudeste"] >= 36 and "lider_sudeste" not in s.achievements:
        s.achievements.append("lider_sudeste")
    if s.scandals == 0 and s.day >= 28 and "sem_escandalo" not in s.achievements:
        s.achievements.append("sem_escandalo")
    if s.day >= 38 and s.intent >= 28 and s.credibility >= 52 and "voto_util" not in s.achievements:
        s.achievements.append("voto_util")
    if s.scandals >= 2 and s.intent >= 24 and "crise_domada" not in s.achievements:
        s.achievements.append("crise_domada")
    if s.day >= s.total_days and "incansavel" not in s.achievements:
        s.achievements.append("incansavel")


def check_game_over():
    s = st.session_state
    if s.intent <= 4:
        s.game_over = True
        s.victory = False
        s.result_text = "Sua intenção de voto virou peça de museu. A campanha secou antes da urna."
    elif s.cash <= 0:
        s.game_over = True
        s.victory = False
        s.result_text = "O caixa acabou. Sem estrutura, a campanha morreu pela logística."
    elif s.energy <= 0:
        s.game_over = True
        s.victory = False
        s.result_text = "Seu corpo pediu arrego antes da democracia terminar o expediente."
    elif s.risk >= 95:
        s.game_over = True
        s.victory = False
        s.result_text = "O jurídico tomou o volante. A campanha implodiu numa espiral de risco, representação e desgaste."
    elif s.rejection >= 70 and s.day > 20:
        s.game_over = True
        s.victory = False
        s.result_text = "A rejeição virou muralha. Até quem te achava interessante começou a buscar outra saída."


def simulate_election():
    s = st.session_state
    region_score = sum(s.regions[r] * REGIONS[r]["peso"] for r in REGIONS) / sum(v["peso"] for v in REGIONS.values())
    seg_score = sum(s.segments[k] * SEGMENTS[k]["peso"] for k in SEGMENTS) / sum(v["peso"] for v in SEGMENTS.values())

    your_vote = (
        s.intent * 0.44
        + region_score * 0.20
        + seg_score * 0.16
        + s.credibility * 0.09
        + s.time_tv * 0.04
        + s.governabilidade * 0.03
        + s.momentum * 0.25
        + s.viral * 0.03
        - s.rejection * 0.20
    )
    if s.day >= 38 and s.intent > 24:
        your_vote += (s.credibility - s.rejection) * 0.05  # voto útil

    your_vote = clamp(your_vote, 8, 58)

    rivals = {k: clamp(v["voto"], 6, 45) for k, v in s.rivals.items()}
    total = your_vote + sum(rivals.values())
    scale = 100 / total
    your_vote *= scale
    rivals = {k: v * scale for k, v in rivals.items()}
    ordered = sorted(rivals.items(), key=lambda x: x[1], reverse=True)
    top_key, top_vote = ordered[0]

    if your_vote >= 50:
        s.victory = True
        s.game_over = True
        s.first_turn = True
        if "primeiro_turno" not in s.achievements:
            s.achievements.append("primeiro_turno")
        s.result_text = (
            f"Você venceu no 1º turno com {your_vote:.1f}% dos votos válidos. "
            "A campanha saiu do meme, passou pela trincheira e terminou no Planalto."
        )
        return

    transferable = max(0.0, 100 - your_vote - top_vote)
    transfer_factor = 0.50 + (s.credibility - s.rejection) / 240 + s.governabilidade / 340 + s.media / 500
    transfer_factor = clamp(transfer_factor, 0.36, 0.67)
    your_transfer = transferable * transfer_factor
    rival_transfer = transferable - your_transfer

    second_you = your_vote + your_transfer
    second_rival = top_vote + rival_transfer
    total2 = second_you + second_rival
    second_you = second_you * 100 / total2
    second_rival = second_rival * 100 / total2

    s.game_over = True
    if second_you > second_rival:
        s.victory = True
        if s.poll_history and min(s.poll_history) < 16 and "virada" not in s.achievements:
            s.achievements.append("virada")
        s.result_text = (
            f"Você foi ao 2º turno contra {s.rivals[top_key]['nome']} e venceu por "
            f"{second_you:.1f}% a {second_rival:.1f}%. Foi marra, disciplina e sobrevivência."
        )
    else:
        s.victory = False
        s.result_text = (
            f"Você chegou ao 2º turno, mas perdeu para {s.rivals[top_key]['nome']} por "
            f"{second_rival:.1f}% a {second_you:.1f}%. Faltou um pouco de lastro para o sprint final."
        )


def next_day(option: Option):
    notes = []
    apply_effects(option.effects, risky=option.risky)
    for cons in option.consequences:
        add_consequence(cons)
        notes.append(f"Consequência ativada: {cons.title}")

    notes.extend(process_consequences())
    rival_turn()
    daily_cost_model()
    unlock_achievements()

    st.session_state.used_events.append(st.session_state.event.id)
    add_history(st.session_state.event.title, option.text)
    st.session_state.poll_history.append(st.session_state.intent)
    st.session_state.rej_history.append(st.session_state.rejection)
    st.session_state.cash_history.append(st.session_state.cash)
    st.session_state.energy_history.append(st.session_state.energy)
    st.session_state.day_history.append(st.session_state.day)

    st.session_state.last_feedback = option.summary + ("\n\n" + " | ".join(notes) if notes else "")
    check_game_over()
    if st.session_state.game_over:
        return

    st.session_state.day += 1
    if st.session_state.day > st.session_state.total_days:
        simulate_election()
    else:
        generate_event()


# =========================================================
# UI
# =========================================================
def render_metric_cards():
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    cards = [
        (c1, "INTENÇÃO", f"{st.session_state.intent:.1f}%", "Pesquisa do dia"),
        (c2, "REJEIÇÃO", f"{st.session_state.rejection:.1f}%", "Quanto menor, melhor"),
        (c3, "CAIXA", fmt_money(st.session_state.cash), "Operação viva"),
        (c4, "MÍDIA", f"{st.session_state.media:.0f}", "TV, rádio e corte"),
        (c5, "RISCO", f"{st.session_state.risk:.0f}%", "Jurídico e crise"),
        (c6, "ENERGIA", f"{st.session_state.energy:.0f}%", "Fôlego real"),
    ]
    for col, title, value, desc in cards:
        with col:
            st.markdown(
                f"<div class='metric-card'><h4>{title}</h4><h2>{value}</h2><span>{desc}</span></div>",
                unsafe_allow_html=True
            )


def sidebar_panel():
    with st.sidebar:
        st.markdown("## 🎛️ Painel da campanha")
        st.caption(f"Seed: {st.session_state.get('seed', '-')}")
        if st.session_state.started:
            st.write(f"**Dia:** {st.session_state.day}/{st.session_state.total_days}")
            st.write(f"**Partido:** {PARTIES[st.session_state.party]['nome']}")
            st.write(f"**Assessor:** {ADVISORS[st.session_state.advisor]['nome']}")
            st.write(f"**Dificuldade:** {st.session_state.difficulty}")
            st.progress(clamp(st.session_state.intent / 50, 0, 1), text="viabilidade")
            st.progress(clamp((100 - st.session_state.rejection) / 100, 0, 1), text="aceitação")
            st.progress(clamp(st.session_state.energy / 100, 0, 1), text="energia")
            st.progress(clamp(st.session_state.governabilidade / 100, 0, 1), text="governabilidade")
            if st.session_state.combo >= 2:
                st.success(f"🔥 Combo ativo x{st.session_state.combo}")
            if st.session_state.active_consequences:
                st.warning(f"⚠️ {len(st.session_state.active_consequences)} consequência(s) ativa(s)")
            if st.session_state.cash < 45000:
                st.warning("💸 Caixa crítico")
            if st.session_state.energy < 28:
                st.warning("😵 Energia muito baixa")
            if st.session_state.risk > 55:
                st.error("🚨 Juridicamente perigoso")

            st.markdown("---")
            st.markdown("### Oposição")
            for _, rival in sorted(st.session_state.rivals.items(), key=lambda x: x[1]["voto"], reverse=True):
                st.write(f"**{rival['nome']}** — {rival['voto']:.1f}%")

            st.markdown("---")
            st.markdown("### Conquistas")
            if st.session_state.achievements:
                for ach in st.session_state.achievements[-6:]:
                    st.markdown(f"<div class='achievement'>{ACHIEVEMENTS[ach]}</div>", unsafe_allow_html=True)
            else:
                st.caption("Nenhuma ainda.")

            st.markdown("---")
            if st.button("🔄 Reiniciar campanha", use_container_width=True):
                init_state(True)
                st.rerun()


def render_charts():
    left, right = st.columns([1.25, 1])

    with left:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=st.session_state.day_history, y=st.session_state.poll_history, mode="lines+markers", name="Intenção"))
        fig.add_trace(go.Scatter(x=st.session_state.day_history, y=st.session_state.rej_history, mode="lines+markers", name="Rejeição"))
        fig.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=35, b=10),
            title="Termômetro eleitoral",
            legend=dict(orientation="h"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("<div class='panel'><h4 style='margin-top:0'>Mapa por regiões</h4>", unsafe_allow_html=True)
        for region, value in st.session_state.regions.items():
            color = REGIONS[region]["cor"]
            st.markdown(
                f"<div class='region-row'><div style='display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px'><span><strong>{region}</strong></span><span>{value:.1f}%</span></div><div style='background:#e5e7eb;border-radius:999px;height:10px;overflow:hidden'><div style='background:{color};width:{max(1, value)}%;height:10px;border-radius:999px'></div></div></div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    l2, r2 = st.columns([1.25, 1])
    with l2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=st.session_state.day_history, y=st.session_state.cash_history, mode="lines+markers", name="Caixa"))
        fig2.update_layout(height=280, margin=dict(l=10, r=10, t=35, b=10), title="Pulso do caixa")
        st.plotly_chart(fig2, use_container_width=True)
    with r2:
        st.markdown("<div class='panel'><h4 style='margin-top:0'>Segmentos eleitorais</h4>", unsafe_allow_html=True)
        for seg, value in st.session_state.segments.items():
            st.markdown(
                f"<div class='region-row'><div style='display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px'><span><strong>{SEGMENTS[seg]['nome']}</strong></span><span>{value:.1f}%</span></div><div style='background:#e5e7eb;border-radius:999px;height:10px;overflow:hidden'><div style='background:#7c3aed;width:{max(1, value)}%;height:10px;border-radius:999px'></div></div></div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)


def render_event():
    event = st.session_state.event
    tone_class = "event-crisis" if event.tone == "crisis" else "event-good" if event.tone == "good" else "event-followup" if event.followup_only else ""
    st.markdown(f"<div class='event-box {tone_class}'>", unsafe_allow_html=True)
    st.markdown(f"### {event.title}")
    st.write(event.desc)
    for tag in event.tags[:4]:
        cls = "tag-red" if event.tone == "crisis" else "tag-green" if event.tone == "good" else "tag-purple" if event.followup_only else "tag-blue"
        st.markdown(f"<span class='tag {cls}'>{tag}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### Escolha sua resposta")
    for idx, option in enumerate(event.options, start=1):
        enabled = req_ok(option.requirement)
        with st.container():
            st.markdown("<div class='choice-box'>", unsafe_allow_html=True)
            st.markdown(f"<div class='choice-title'>{idx}. {option.text}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='small-muted'>{option.summary}</div>", unsafe_allow_html=True)

            chips = []
            eff = option.effects
            if "intent" in eff: chips.append(chip(f"Intenção {'+' if eff['intent']>=0 else ''}{eff['intent']:.1f}"))
            if "rejection" in eff: chips.append(chip(f"Rejeição {'+' if eff['rejection']>=0 else ''}{eff['rejection']:.1f}"))
            if "credibility" in eff: chips.append(chip(f"Credibilidade {'+' if eff['credibility']>=0 else ''}{eff['credibility']:.1f}"))
            if "cash" in eff: chips.append(chip(f"Caixa {'+' if eff['cash']>=0 else ''}{fmt_money(eff['cash'])}"))
            if "energy" in eff: chips.append(chip(f"Energia {'+' if eff['energy']>=0 else ''}{eff['energy']:.1f}"))
            if "risk" in eff: chips.append(chip(f"Risco {'+' if eff['risk']>=0 else ''}{eff['risk']:.1f}"))
            if "media" in eff: chips.append(chip(f"Mídia {'+' if eff['media']>=0 else ''}{eff['media']:.1f}"))
            if "viral" in eff: chips.append(chip(f"Viral {'+' if eff['viral']>=0 else ''}{eff['viral']:.1f}"))
            if chips:
                st.markdown("".join(chips), unsafe_allow_html=True)
            if option.consequences:
                st.caption("Essa escolha pode abrir consequências persistentes.")
            btn_label = "Escolher"
            if not enabled and option.requirement:
                reqs = ", ".join([f"{k} ≥ {v}" for k, v in option.requirement.items()])
                st.caption(f"Requer: {reqs}")
            if st.button(btn_label, key=f"opt_{st.session_state.day}_{event.id}_{idx}", disabled=not enabled, use_container_width=True):
                next_day(option)
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


def render_feedback_and_consequences():
    if st.session_state.last_feedback:
        st.info(st.session_state.last_feedback)
    if st.session_state.active_consequences:
        st.markdown("#### Consequências ativas")
        for cons in st.session_state.active_consequences:
            st.markdown(
                f"<div class='consequence-card'><strong>{cons['title']}</strong><br><span class='small-muted'>{cons['desc']}</span><br><span class='small-muted'>Dias restantes: {cons['days_left']}</span></div>",
                unsafe_allow_html=True,
            )


def render_history():
    if not st.session_state.history:
        return
    st.markdown("#### Últimas decisões")
    for row in reversed(st.session_state.history[-5:]):
        st.markdown(
            f"- **Dia {row['dia']}** — {row['evento']} → *{row['decisao']}*"
        )


def render_start_screen():
    st.markdown(
        f"""
        <div class="hero">
            <h1>🇧🇷 Candidato 2026: Viral Master V5</h1>
            <p>45 turnos, caixa e energia equilibrados, consequências persistentes, mais de 50 eventos únicos e sem repetição durante a campanha.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='panel'>Este modo foi pensado para ficar mais real e mais viciante: resposta com consequência, custo de operação, voto útil, pressão do TSE, alianças, território, segmentos e reta final com risco de colapso.</div>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        party = st.selectbox("Partido", options=list(PARTIES.keys()), format_func=lambda x: PARTIES[x]["nome"])
        advisor = st.selectbox("Assessor principal", options=list(ADVISORS.keys()), format_func=lambda x: f"{ADVISORS[x]['icone']} {ADVISORS[x]['nome']}")
    with c2:
        difficulty = st.selectbox("Dificuldade", options=["Fácil", "Normal", "Difícil", "Hardcore"], index=1)
        seed = st.number_input("Seed da campanha", min_value=1, max_value=999999, value=2026, step=1)

    st.markdown("### O que muda nesta versão")
    st.markdown(
        "- Mais de **50 eventos únicos** na rotação normal.\n"
        "- **45 turnos sem repetição** do mesmo evento.\n"
        "- **Energia e caixa** com consumo realista.\n"
        "- **Consequências persistentes** e follow-ups.\n"
        "- **Regiões, segmentos, mídia, aliados e risco jurídico** integrados.\n"
        "- **1º e 2º turno** com voto útil na reta final."
    )
    if st.button("🚀 Iniciar campanha", use_container_width=True):
        start_campaign(party, advisor, difficulty, int(seed))
        st.rerun()


def render_result():
    if st.session_state.victory:
        st.markdown(f"<div class='success-strip'>✅ {st.session_state.result_text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='warning-strip'>❌ {st.session_state.result_text}</div>", unsafe_allow_html=True)

    render_charts()

    st.markdown("### Fechamento da campanha")
    st.write(
        f"**Intenção final:** {st.session_state.intent:.1f}% | "
        f"**Rejeição final:** {st.session_state.rejection:.1f}% | "
        f"**Caixa restante:** {fmt_money(st.session_state.cash)} | "
        f"**Escândalos:** {st.session_state.scandals}"
    )

    if st.session_state.victory:
        st.markdown(
            "<div class='panel'><strong>Gancho para a próxima evolução:</strong> esta base já deixa preparado o terreno para um modo pós-eleição com governabilidade, ministérios, crise no Congresso, orçamento e popularidade de governo.</div>",
            unsafe_allow_html=True,
        )

    if st.button("🔁 Jogar novamente", use_container_width=True):
        init_state(True)
        st.rerun()


def main():
    init_state()
    sidebar_panel()

    if not st.session_state.started:
        render_start_screen()
        return

    st.markdown(
        f"""
        <div class="hero">
            <h1>🇧🇷 Corrida ao Planalto</h1>
            <p>Dia {st.session_state.day} de {st.session_state.total_days} • {PARTIES[st.session_state.party]['nome']} • {ADVISORS[st.session_state.advisor]['nome']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_metric_cards()

    if st.session_state.game_over:
        render_result()
        return

    render_feedback_and_consequences()
    render_event()
    render_charts()
    render_history()


if __name__ == "__main__":
    main()
