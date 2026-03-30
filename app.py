import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import plotly.graph_objects as go
import streamlit as st

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="🇧🇷 Candidato 2026: Viral Edition V4",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# STYLE
# =========================================================
STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%); }
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #172554 45%, #1d4ed8 100%);
        border-radius: 26px;
        padding: 28px;
        color: white;
        box-shadow: 0 18px 50px rgba(15,23,42,.22);
        margin-bottom: 16px;
    }
    .hero h1 { margin:0 0 6px 0; font-size: 2.1rem; }
    .hero p { margin:0; opacity:.9; }
    .panel {
        background: white;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 8px 24px rgba(15,23,42,.08);
        border: 1px solid rgba(99,102,241,.08);
    }
    .metric-card {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        color: white;
        border-radius: 18px;
        padding: 16px;
        min-height: 108px;
        box-shadow: 0 10px 28px rgba(0,0,0,.18);
    }
    .metric-card h4 { margin:0; opacity:.78; font-size:12px; text-transform: uppercase; letter-spacing: .08em; }
    .metric-card h2 { margin:10px 0 6px 0; font-size: 30px; }
    .metric-card span { font-size: 12px; opacity: .9; }
    .event-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-left: 8px solid #2563eb;
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 12px 34px rgba(15,23,42,.10);
        margin-bottom: 18px;
    }
    .event-crisis { border-left-color: #dc2626; }
    .event-good { border-left-color: #16a34a; }
    .event-followup { border-left-color: #7c3aed; }
    .tag {
        display:inline-block; padding:6px 10px; border-radius:999px; font-size:11px;
        font-weight:700; margin-right:6px; margin-top:8px;
    }
    .tag-blue { background:#dbeafe; color:#1d4ed8; }
    .tag-red { background:#fee2e2; color:#b91c1c; }
    .tag-green { background:#dcfce7; color:#166534; }
    .tag-purple { background:#ede9fe; color:#6d28d9; }
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
    .effect-chip {
        display:inline-flex; align-items:center; gap:6px; padding:7px 10px; border-radius:999px;
        font-size:12px; font-weight:700; margin:4px 5px 0 0; background:#f3f4f6; color:#111827;
    }
    .consequence-card {
        background: linear-gradient(135deg, #fff7ed 0%, #fffbeb 100%);
        border: 1px solid #fed7aa; border-radius: 16px; padding: 14px; margin-bottom: 10px;
    }
    .achievement {
        display:inline-block; padding:8px 12px; border-radius:999px; margin:4px;
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%); color:white;
        font-size:12px; font-weight:700;
    }
    .region-row { margin-bottom: 10px; }
    .gov-box {
        background: linear-gradient(135deg, #ecfeff 0%, #eff6ff 100%);
        border-radius: 18px; padding: 16px; border: 1px solid #bfdbfe;
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
    "periferia": {"peso": 18, "chave": "social", "nome": "Periferia"},
    "classe_media": {"peso": 18, "chave": "gestao", "nome": "Classe média"},
    "agro": {"peso": 12, "chave": "agro", "nome": "Agro"},
    "evangelicos": {"peso": 14, "chave": "valores", "nome": "Evangélicos"},
    "jovens": {"peso": 12, "chave": "digital", "nome": "Jovens"},
    "servidores": {"peso": 11, "chave": "gestao", "nome": "Servidores"},
    "empreendedores": {"peso": 15, "chave": "mercado", "nome": "Empreendedores"},
}

ADVERSARIOS = {
    "populista": {"nome": "Ronaldo Falcão", "base": 26, "perfil": "digital", "rejeicao": 31},
    "tecnico": {"nome": "Marina Albuquerque", "base": 23, "perfil": "gestao", "rejeicao": 22},
    "maquina": {"nome": "César Prado", "base": 25, "perfil": "estrutura", "rejeicao": 28},
}

ASSESSORES = {
    "estrategista": {
        "nome": "Carlos Mendes", "icone": "🎯", "descricao": "Lê swing, timing e tendência.",
        "bonus": {"narrativa": 2, "momentum": 1, "credibilidade": 1},
    },
    "financeiro": {
        "nome": "Ana Rodrigues", "icone": "💰", "descricao": "Captação legal e controle de caixa.",
        "bonus": {"caixa": 12000, "credibilidade": -1, "allies": 1},
    },
    "comunicacao": {
        "nome": "Pedro Santos", "icone": "📰", "descricao": "Amplifica bons momentos e corta danos.",
        "bonus": {"media": 5, "viral": 8},
    },
    "politico": {
        "nome": "Helena Costa", "icone": "🤝", "descricao": "Negocia apoio, palanque e governabilidade.",
        "bonus": {"allies": 8, "time_tv": 3, "governabilidade": 6},
    },
    "juridico": {
        "nome": "Roberto Lima", "icone": "⚖️", "descricao": "Evita cassação e enquadra propaganda.",
        "bonus": {"risk": -8, "credibility": 2},
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
    "sobreviveu_crise": "🛡️ Sobreviveu à crise",
    "consequencia_mestre": "🧠 Mestre das consequências",
}

# =========================================================
# MODELS
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
# CONSEQUENCE FACTORY
# =========================================================
def cons_base_midia_negativa() -> Consequence:
    return Consequence(
        key="midia_negativa",
        title="Rodada de mídia negativa",
        desc="Seu movimento gerou manchetes ruins por alguns dias. O dano não vem de uma vez: ele pinga e corrói confiança.",
        duration=3,
        daily={"media": -2.0, "credibility": -1.2, "rejection": 0.5},
        severity="danger",
    )


def cons_onda_apoio() -> Consequence:
    return Consequence(
        key="onda_apoio",
        title="Onda de apoio orgânico",
        desc="A campanha entrou numa fase de boa maré. A cada dia, indecisos e apoiadores replicam seu discurso sem muito empurrão.",
        duration=3,
        daily={"intent": 0.7, "media": 1.2, "viral": 2.0, "momentum": 0.5},
        severity="good",
    )


def cons_pressao_tse() -> Consequence:
    return Consequence(
        key="pressao_tse",
        title="Pressão do TSE",
        desc="Sua campanha entrou no radar jurídico. Isso não mata sozinho, mas faz cada decisão seguinte parecer mais arriscada.",
        duration=3,
        daily={"risk": 2.4, "credibility": -0.8},
        severity="danger",
        followup_event="tse_julgamento",
        followup_chance=0.45,
    )


def cons_aliados_desconfiados() -> Consequence:
    return Consequence(
        key="aliados_desconfiados",
        title="Aliados desconfiados",
        desc="Sua base começa a perguntar se vale mesmo continuar contigo. Isso desgasta tempo de TV, palanque e articulação.",
        duration=3,
        daily={"allies": -2.1, "time_tv": -0.7, "governabilidade": -1.2},
        severity="warning",
        followup_event="traicao_aliado",
        followup_chance=0.35,
    )


def cons_base_animada() -> Consequence:
    return Consequence(
        key="base_animada",
        title="Base inflamou",
        desc="Sua militância comprou a narrativa e empurrou a campanha para frente. O lado ruim é que isso também deixa a campanha mais aguda.",
        duration=2,
        daily={"viral": 3.0, "intent": 0.6, "rejection": 0.25},
        severity="good",
    )


def cons_empresariado_feliz() -> Consequence:
    return Consequence(
        key="empresariado_feliz",
        title="Mercado abriu a carteira",
        desc="Seu discurso agradou setores produtivos. O caixa respira, mas o povão vai cobrar contrapartida social.",
        duration=3,
        daily={"cash": 7000.0, "credibility": 0.4, "intent": -0.15},
        severity="good",
    )


def cons_memes_crise() -> Consequence:
    return Consequence(
        key="memes_crise",
        title="Virou meme ruim",
        desc="Seu erro virou trend. O problema não é só a piada: é a repetição desgastando imagem por vários dias.",
        duration=3,
        daily={"viral": 2.0, "credibility": -1.5, "rejection": 0.9, "media": -1.0},
        severity="danger",
        followup_event="podcast_gafe_followup",
        followup_chance=0.4,
    )


# =========================================================
# EVENTS
# =========================================================
EVENTS: List[EventCard] = [
    EventCard(
        id="pesquisa_subiu",
        title="📊 Pesquisa nova te coloca em alta",
        desc="Você cresceu 3 pontos entre indecisos. A campanha agora precisa escolher se transforma isso em euforia, serenidade ou máquina de arrecadação.",
        category="pesquisa",
        tone="good",
        phase="all",
        tags=["pesquisa", "momento", "viral"],
        options=[
            Option(
                "Comemorar com humildade e foco em ampliar ponte com indecisos",
                "Você capitalizou sem parecer deslumbrado.",
                {"intent": 1.6, "credibility": 2.0, "media": 3.0, "momentum": 1.5},
                consequences=[cons_onda_apoio()],
            ),
            Option(
                "Lançar ofensiva de arrecadação dizendo que agora a vitória é possível",
                "O caixa respondeu, mas uma parte do eleitorado torceu o nariz.",
                {"cash": 26000.0, "intent": 0.8, "media": 2.0, "viral": 4.0, "rejection": 0.6},
            ),
            Option(
                "Zombar dos adversários e tratar a virada como inevitável",
                "A base gostou; o centro, nem tanto.",
                {"viral": 7.0, "intent": 0.7, "rejection": 1.8, "credibility": -1.5},
                risky=True,
                consequences=[cons_base_animada(), cons_memes_crise()],
            ),
        ],
    ),
    EventCard(
        id="debate_nacional",
        title="📺 Debate presidencial em rede nacional",
        desc="É o tipo de noite que cria candidato ou derrete favorito. O país está assistindo cada cara, pausa e resposta atravessada.",
        category="midia",
        tone="neutral",
        phase="all",
        tags=["debate", "TV", "reta crítica"],
        options=[
            Option(
                "Responder com firmeza, dados e um tom presidencial",
                "Você passou autoridade e ganhou respeito entre indecisos.",
                {"intent": 2.1, "credibility": 3.5, "media": 5.0, "energy": -8.0, "rejection": -0.5},
                requirement={"energy": 18},
                consequences=[cons_onda_apoio()],
            ),
            Option(
                "Partir para o ataque e buscar o corte mais viral da noite",
                "Funcionou com sua base, mas elevou rejeição.",
                {"viral": 10.0, "intent": 1.6, "media": 4.0, "rejection": 2.2, "energy": -6.0},
                risky=True,
                consequences=[cons_base_animada()],
            ),
            Option(
                "Fazer um debate morno, sem errar e sem brilhar",
                "Você saiu inteiro, mas deixou espaço para rivais crescerem.",
                {"credibility": 1.0, "media": 1.0, "energy": -4.0, "momentum": -0.5},
            ),
        ],
    ),
    EventCard(
        id="podcast_gafe",
        title="🎙️ Podcast gigante te chama ao vivo",
        desc="Milhões assistindo. A entrevista pode humanizar a campanha ou produzir um corte desastroso que não morre nunca mais.",
        category="digital",
        tone="neutral",
        phase="all",
        tags=["podcast", "internet", "clipe"],
        options=[
            Option(
                "Ir preparado e misturar leveza com proposta concreta",
                "Boa presença, bom corte, bom ganho.",
                {"viral": 8.0, "media": 3.0, "intent": 1.4, "credibility": 2.0, "energy": -5.0},
                consequences=[cons_onda_apoio()],
            ),
            Option(
                "Tentar lacrar em tudo para dominar as redes",
                "Você ganhou clipes, mas também abriu flanco para meme ruim.",
                {"viral": 12.0, "intent": 0.7, "rejection": 1.2, "credibility": -0.8},
                risky=True,
                consequences=[cons_memes_crise()],
            ),
            Option(
                "Recusar e dizer que campanha séria não é entretenimento",
                "Soou elitista e defensivo.",
                {"media": -4.0, "viral": -3.0, "intent": -1.0, "credibility": -0.8},
            ),
        ],
    ),
    EventCard(
        id="mercado_assustou",
        title="💹 Mercado reage mal a uma fala sua",
        desc="Dólar sobe, comentarista econômico bate, e a imprensa te cobra previsibilidade. Isso contamina o noticiário por dias se você errar de novo.",
        category="economia",
        tone="crisis",
        phase="all",
        tags=["economia", "mercado", "credibilidade"],
        options=[
            Option(
                "Recalibrar discurso com equipe técnica e metas claras",
                "Você acalmou parte do pânico e ganhou solidez.",
                {"credibility": 3.5, "intent": 0.9, "media": 2.0, "cash": 6000.0},
                consequences=[cons_empresariado_feliz()],
            ),
            Option(
                "Dobrar a aposta e bater no mercado financeiro",
                "Parte do eleitorado popular gostou, mas a desconfiança cresceu.",
                {"intent": 1.3, "viral": 4.0, "rejection": 1.1, "cash": -9000.0, "credibility": -1.8},
                risky=True,
                consequences=[cons_midia_negativa := cons_base_midia_negativa()],
            ),
            Option(
                "Fingir que nada aconteceu",
                "A narrativa ficou solta e a mídia ocupou o vácuo.",
                {"media": -5.0, "credibility": -2.2, "intent": -0.8},
                consequences=[cons_base_midia_negativa()],
            ),
        ],
    ),
    EventCard(
        id="apoio_governador",
        title="🏛️ Um governador importante quer subir no seu palanque",
        desc="O apoio traz tempo, estrutura e interiorização, mas também vem com cobrança por cargos e espaço futuro.",
        category="politica",
        tone="good",
        phase="mid_late",
        tags=["aliança", "governador", "palanque"],
        options=[
            Option(
                "Aceitar e compartilhar protagonismo com equilíbrio",
                "Boa operação: você ganhou capilaridade sem parecer refém.",
                {"allies": 7.0, "time_tv": 3.0, "intent": 1.4, "governabilidade": 5.0, "Sudeste": 2.0},
            ),
            Option(
                "Aceitar, mas entregar demais para fechar o apoio rápido",
                "Curto prazo forte, longo prazo caro.",
                {"allies": 10.0, "intent": 1.8, "time_tv": 4.0, "governabilidade": -3.0},
                risky=True,
                consequences=[cons_aliados_desconfiados()],
            ),
            Option(
                "Recusar para manter imagem de independência",
                "Você preservou pureza, mas perdeu estrutura.",
                {"credibility": 1.5, "allies": -5.0, "time_tv": -2.0, "intent": -0.6},
            ),
        ],
    ),
    EventCard(
        id="enchente_nacional",
        title="🌧️ Enchentes ganham o noticiário nacional",
        desc="O país espera postura de presidenciável. Explorar demais pega mal; sumir também pega mal. É o clássico campo minado brasileiro.",
        category="social",
        tone="crisis",
        phase="all",
        tags=["tragédia", "empatia", "liderança"],
        options=[
            Option(
                "Ir ao local, propor fundo emergencial e evitar politicagem",
                "Movimento forte, humano e difícil de atacar.",
                {"intent": 2.0, "credibility": 3.0, "media": 4.0, "energy": -9.0, "risk": -1.0},
                consequences=[cons_onda_apoio()],
            ),
            Option(
                "Comentar pelas redes e culpar adversários rapidamente",
                "Corte rápido, desgaste duradouro.",
                {"viral": 5.0, "intent": 0.4, "rejection": 1.6, "credibility": -2.2},
                risky=True,
                consequences=[cons_base_midia_negativa()],
            ),
            Option(
                "Esperar a poeira baixar para não parecer oportunista",
                "A intenção era correta, mas pareceu ausência.",
                {"media": -4.0, "intent": -1.1, "credibility": -1.4},
            ),
        ],
    ),
    EventCard(
        id="greve_caminhoneiros",
        title="🚚 Paralisação ameaça abastecimento",
        desc="Combustível e comida entram na pauta. O eleitor médio não quer tese: quer alguém que passe sensação de controle.",
        category="economia",
        tone="crisis",
        phase="all",
        tags=["abastecimento", "greve", "economia"],
        options=[
            Option(
                "Defender negociação imediata e plano temporário de abastecimento",
                "Você pareceu adulto na sala.",
                {"intent": 1.7, "credibility": 2.6, "media": 2.5, "risk": -1.0},
            ),
            Option(
                "Comprar briga e chamar tudo de sabotagem política",
                "Rende clipe, mas o caos pode colar em você.",
                {"viral": 6.0, "intent": 0.5, "rejection": 1.7, "credibility": -1.7},
                risky=True,
                consequences=[cons_base_midia_negativa(), cons_aliados_desconfiados()],
            ),
            Option(
                "Falar só para agradar um lado da categoria",
                "Você ganhou nicho e perdeu o resto.",
                {"agro": 3.0, "intent": 0.3, "credibility": -0.9, "rejection": 0.8},
            ),
        ],
    ),
    EventCard(
        id="igreja_apoio",
        title="⛪ Liderança evangélica sinaliza apoio",
        desc="A oportunidade é potente, mas qualquer gesto artificial cheira a voto por conveniência. E o Brasil percebe rápido.",
        category="valores",
        tone="good",
        phase="mid_late",
        tags=["evangélicos", "valores", "aliança"],
        options=[
            Option(
                "Receber o apoio com discurso de liberdade religiosa e responsabilidade social",
                "Funcionou sem caricatura.",
                {"evangelicos": 5.0, "intent": 1.4, "credibility": 2.0, "rejection": 0.3},
            ),
            Option(
                "Radicalizar o discurso para sugar toda a base de uma vez",
                "Ganhou nicho, perdeu parte do centro.",
                {"evangelicos": 7.0, "intent": 1.6, "rejection": 1.8, "credibility": -1.3},
                risky=True,
                consequences=[cons_base_animada()],
            ),
            Option(
                "Recusar para manter perfil laico sem ruído",
                "Coerente, mas custa voto e palanque.",
                {"credibility": 1.4, "evangelicos": -4.0, "intent": -0.8},
            ),
        ],
    ),
    EventCard(
        id="vaquinha_recorde",
        title="💸 Sua vaquinha online explode",
        desc="Quando a internet decide doar, a campanha ganha combustível — e também mais olhos fiscalizando tudo que você faz com cada centavo.",
        category="financas",
        tone="good",
        phase="all",
        tags=["doações", "digital", "caixa"],
        options=[
            Option(
                "Transformar a vaquinha em símbolo de independência popular",
                "A narrativa pegou bem.",
                {"cash": 26000.0, "intent": 1.5, "credibility": 2.2, "viral": 6.0},
                consequences=[cons_onda_apoio()],
            ),
            Option(
                "Arrecadar forte, mas sem falar muito sobre isso",
                "Menos brilho, mais disciplina.",
                {"cash": 21000.0, "credibility": 1.8},
            ),
            Option(
                "Forçar urgência emocional o tempo inteiro",
                "Arrecada mais hoje, desgasta amanhã.",
                {"cash": 32000.0, "intent": 0.4, "rejection": 1.1, "credibility": -1.5},
                risky=True,
                consequences=[cons_base_midia_negativa()],
            ),
        ],
    ),
    EventCard(
        id="operacao_pf_aliado",
        title="🚨 Operação atinge aliado do seu palanque",
        desc="Você não é o alvo, mas a notícia te atravessa como bala perdida. No Brasil político, bala perdida quase sempre acha alguém.",
        category="crise",
        tone="crisis",
        phase="mid_late",
        tags=["PF", "corrupção", "aliança"],
        options=[
            Option(
                "Romper publicamente e defender investigação total",
                "Doeu na articulação, mas blindou sua imagem.",
                {"credibility": 4.0, "rejection": -0.8, "allies": -6.0, "governabilidade": -2.0, "media": 2.0},
            ),
            Option(
                "Esperar mais informações antes de falar",
                "Pareceu prudência para uns e omissão para outros.",
                {"allies": 2.0, "intent": -0.6, "credibility": -1.0, "media": -2.0},
                consequences=[cons_base_midia_negativa()],
            ),
            Option(
                "Defender o aliado como vítima política",
                "Você amarrou o seu nome ao problema dele.",
                {"allies": 5.0, "intent": -1.4, "rejection": 2.4, "credibility": -3.5, "risk": 6.0},
                risky=True,
                consequences=[cons_pressao_tse(), cons_aliados_desconfiados()],
            ),
        ],
    ),
    EventCard(
        id="plano_social",
        title="🧺 Você vai anunciar uma proposta social forte",
        desc="A proposta pode te aproximar de quem precisa e assustar quem acha que tudo vai virar descontrole fiscal. É sempre esse cabo de guerra.",
        category="programa",
        tone="neutral",
        phase="all",
        tags=["social", "proposta", "economia"],
        options=[
            Option(
                "Apresentar programa com foco em renda, porta de saída e responsabilidade fiscal",
                "Você encaixou coração e planilha.",
                {"intent": 1.8, "periferia": 4.0, "credibility": 2.5, "media": 2.0},
            ),
            Option(
                "Prometer expansão agressiva sem explicar de onde vem o dinheiro",
                "Popular no curto prazo, perigoso no médio.",
                {"intent": 2.2, "periferia": 5.0, "credibility": -2.2, "risk": 2.0},
                risky=True,
                consequences=[cons_base_midia_negativa()],
            ),
            Option(
                "Adiar o anúncio até ter mais números",
                "Seguro demais para o momento.",
                {"credibility": 1.0, "intent": -0.5, "momentum": -1.0},
            ),
        ],
    ),
    EventCard(
        id="seguranca_publica",
        title="🚔 Caso de violência domina a pauta",
        desc="Ninguém ganha eleição só com segurança, mas muita gente perde quando parece despreparado nela.",
        category="seguranca",
        tone="neutral",
        phase="all",
        tags=["segurança", "comoção", "RJ/SP"],
        options=[
            Option(
                "Defender ação integrada, inteligência e pacto federativo",
                "Postura madura, sem cosplay de xerife.",
                {"intent": 1.5, "credibility": 2.8, "Sudeste": 2.0, "media": 2.0},
            ),
            Option(
                "Adotar tom bélico para dominar a pauta nas redes",
                "Você acendeu a base, mas assustou indecisos.",
                {"viral": 7.0, "intent": 0.8, "rejection": 1.4, "credibility": -0.8},
                risky=True,
            ),
            Option(
                "Escapar do assunto e falar de educação",
                "Boa pauta, timing péssimo.",
                {"media": -4.0, "intent": -1.0, "credibility": -1.2},
            ),
        ],
    ),
    EventCard(
        id="sabatina_jn",
        title="📰 Sabatina dura em jornal nacional",
        desc="Perguntas técnicas, cobrança de passado e armadilha em cada intervalo. O país não perdoa improviso confiante demais.",
        category="midia",
        tone="neutral",
        phase="late",
        tags=["televisão", "credibilidade", "reta final"],
        options=[
            Option(
                "Responder com precisão e admitir limites quando necessário",
                "Seriedade vende muito no fim.",
                {"credibility": 4.0, "media": 4.0, "intent": 1.2, "rejection": -0.5},
                consequences=[cons_onda_apoio()],
            ),
            Option(
                "Enfrentar jornalista e tentar dominar a entrevista no grito",
                "Teve corte, teve desgaste.",
                {"viral": 8.0, "intent": 0.5, "rejection": 2.0, "credibility": -2.2},
                risky=True,
                consequences=[cons_memes_crise()],
            ),
            Option(
                "Ser simpático e evitar atrito o tempo todo",
                "Passou leve demais num momento que pedia substância.",
                {"media": 1.5, "credibility": -0.6, "intent": 0.3},
            ),
        ],
    ),
    EventCard(
        id="ultimo_debate",
        title="🎯 Último debate antes da votação",
        desc="A reta final chegou. Agora é voto útil, medo de rejeição, sensação de viabilidade e quem erra na hora errada.",
        category="midia",
        tone="neutral",
        phase="late",
        tags=["debate final", "indecisos", "voto útil"],
        options=[
            Option(
                "Mirar o centro e falar como favorito responsável",
                "Boa para voto útil e rejeição.",
                {"intent": 2.3, "rejection": -1.1, "credibility": 3.0, "media": 4.0},
            ),
            Option(
                "Ir para o confronto total e tentar matar a eleição ali",
                "Ou vira mito, ou vira lembrança ruim.",
                {"intent": 2.8, "viral": 11.0, "rejection": 2.2, "media": 5.0},
                risky=True,
                consequences=[cons_base_animada(), cons_memes_crise()],
            ),
            Option(
                "Pedir voto útil com argumento de viabilidade e governabilidade",
                "Menos brilho, mais pragmatismo eleitoral.",
                {"intent": 2.0, "governabilidade": 3.0, "allies": 2.0, "credibility": 1.5},
            ),
        ],
    ),
    # FOLLOW-UP EVENTS
    EventCard(
        id="tse_julgamento",
        title="⚖️ TSE pauta representação contra sua campanha",
        desc="A consequência chegou. O problema anterior agora vira sessão, manchete e oportunidade para adversário posar de paladino.",
        category="juridico",
        tone="crisis",
        phase="all",
        tags=["TSE", "follow-up", "jurídico"],
        followup_only=True,
        options=[
            Option(
                "Responder tecnicamente, trocar a peça suspeita e baixar o tom",
                "Você estancou parte do dano.",
                {"risk": -7.0, "credibility": 2.5, "media": 1.0, "intent": 0.5},
            ),
            Option(
                "Dobrar a aposta e acusar perseguição eleitoral",
                "Mobiliza base, mas piora o problema institucional.",
                {"viral": 7.0, "intent": 0.4, "risk": 5.0, "rejection": 1.5, "credibility": -2.0},
                risky=True,
                consequences=[cons_pressao_tse()],
            ),
        ],
    ),
    EventCard(
        id="traicao_aliado",
        title="🗡️ Aliado vaza insatisfação e ameaça deserção",
        desc="O desgaste acumulado bateu na porta. Brasília fareja fragilidade como tubarão fareja sangue.",
        category="politica",
        tone="crisis",
        phase="all",
        tags=["follow-up", "aliança", "vazamento"],
        followup_only=True,
        options=[
            Option(
                "Recompor ponte com concessão limitada e jogo de cintura",
                "Você conteve a sangria sem se vender por completo.",
                {"allies": 4.0, "governabilidade": 2.0, "time_tv": 1.0, "cash": -6000.0},
            ),
            Option(
                "Comprar a briga e expor quem está chantagendo",
                "Pode parecer coragem; pode parecer descontrole.",
                {"viral": 6.0, "credibility": 0.5, "allies": -6.0, "governabilidade": -4.0, "rejection": 1.0},
                risky=True,
            ),
        ],
    ),
    EventCard(
        id="podcast_gafe_followup",
        title="😂 Sua fala virou trilha de meme nacional",
        desc="O que parecia só um corte bobo agora está em vídeo, remix, figurinha e programa de humor. É o Brasil fazendo churrasco da sua imagem.",
        category="digital",
        tone="crisis",
        phase="all",
        tags=["follow-up", "meme", "viral"],
        followup_only=True,
        options=[
            Option(
                "Entrar na piada, humanizar e puxar assunto sério logo depois",
                "Você reduziu a toxicidade do meme.",
                {"viral": 5.0, "credibility": 1.5, "rejection": -0.4, "intent": 0.6},
            ),
            Option(
                "Fingir que não aconteceu",
                "A internet ama quando o político finge que o incêndio acabou sozinho.",
                {"credibility": -1.4, "rejection": 1.2, "intent": -0.5},
                consequences=[cons_base_midia_negativa()],
            ),
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
    if progress < 0.65:
        return "mid"
    return "late"


def event_matches_phase(event_phase: str, day_phase: str) -> bool:
    mapping = {
        "all": {"early", "mid", "late"},
        "early": {"early"},
        "mid": {"mid"},
        "late": {"late"},
        "early_mid": {"early", "mid"},
        "mid_late": {"mid", "late"},
    }
    return day_phase in mapping.get(event_phase, {day_phase})


def fmt_money(v: float) -> str:
    return f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def metric_delta_chip(label: str, value: float) -> str:
    sign = "+" if value > 0 else ""
    return f"<span class='effect-chip'>{label} {sign}{value:.1f}</span>"


# =========================================================
# STATE INIT
# =========================================================
def init_state(reset_seed: bool = True):
    if reset_seed:
        st.session_state.seed = random.randint(10000, 999999)
    rnd = random.Random(st.session_state.get("seed", 12345))

    st.session_state.day = 1
    st.session_state.total_days = 35
    st.session_state.party = "centro"
    st.session_state.difficulty = "Normal"
    st.session_state.advisor = "estrategista"
    st.session_state.started = False
    st.session_state.game_over = False
    st.session_state.victory = False
    st.session_state.first_turn = False
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
    st.session_state.followup_queue = []
    st.session_state.active_consequences = []
    st.session_state.consequence_turns_survived = 0

    st.session_state.intent = 21.5
    st.session_state.rejection = 24.0
    st.session_state.credibility = 48.0
    st.session_state.cash = 130000.0
    st.session_state.energy = 80.0
    st.session_state.media = 44.0
    st.session_state.risk = 14.0
    st.session_state.allies = 52.0
    st.session_state.time_tv = 18.0
    st.session_state.momentum = 0.0
    st.session_state.narrative = 45.0
    st.session_state.viral = 10.0
    st.session_state.governabilidade = 42.0

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
        st.session_state.cash += 20000
        st.session_state.regions["Sudeste"] += 3
        st.session_state.segments["empreendedores"] += 5
        st.session_state.segments["agro"] += 2
        st.session_state.rejection += 1.2
    elif party == "verde":
        st.session_state.credibility += 5
        st.session_state.regions["Norte"] += 4
        st.session_state.segments["jovens"] += 4
        st.session_state.intent += 1.0

    for key, val in ASSESSORES[advisor]["bonus"].items():
        if key == "caixa":
            st.session_state.cash += val
        elif key == "credibilidade" or key == "credibility":
            st.session_state.credibility += val
        elif key == "media":
            st.session_state.media += val
        elif key == "viral":
            st.session_state.viral += val
        elif key == "allies":
            st.session_state.allies += val
        elif key == "time_tv":
            st.session_state.time_tv += val
        elif key == "risk":
            st.session_state.risk += val
        elif key == "narrativa":
            st.session_state.narrative += val
        elif key == "momentum":
            st.session_state.momentum += val
        elif key == "governabilidade":
            st.session_state.governabilidade += val

    if diff == "Fácil":
        st.session_state.intent += 3
        st.session_state.cash += 25000
        st.session_state.energy += 10
        st.session_state.rejection -= 2
        st.session_state.risk -= 4
    elif diff == "Difícil":
        st.session_state.intent -= 2
        st.session_state.cash -= 25000
        st.session_state.rejection += 2
        st.session_state.risk += 5
    elif diff == "Hardcore":
        st.session_state.intent -= 4
        st.session_state.cash -= 45000
        st.session_state.rejection += 4
        st.session_state.risk += 8
        st.session_state.energy -= 8

    generate_event()


# =========================================================
# ENGINE
# =========================================================
def get_available_events() -> List[EventCard]:
    day_phase = phase_for_day(st.session_state.day, st.session_state.total_days)
    pool = [
        e for e in EVENTS
        if not e.followup_only
        and event_matches_phase(e.phase, day_phase)
        and e.id not in st.session_state.used_events[-12:]
    ]
    if not pool:
        pool = [e for e in EVENTS if not e.followup_only and event_matches_phase(e.phase, day_phase)]
    return pool


def generate_event():
    if st.session_state.followup_queue:
        event_id = st.session_state.followup_queue.pop(0)
        for event in EVENTS:
            if event.id == event_id:
                st.session_state.event = event
                return
    pool = get_available_events()
    weights = []
    for event in pool:
        weight = 1.0
        if event.tone == "crisis" and st.session_state.risk > 35:
            weight += 0.6
        if event.category == "midia" and st.session_state.media > 55:
            weight += 0.4
        if event.category == "politica" and st.session_state.allies < 45:
            weight += 0.4
        if event.category == "digital" and st.session_state.viral > 28:
            weight += 0.4
        weights.append(weight)
    st.session_state.event = random.choices(pool, weights=weights, k=1)[0]


def option_enabled(option: Option) -> bool:
    if not option.requirement:
        return True
    req = option.requirement
    for key, min_value in req.items():
        current = getattr_proxy(key)
        if current < min_value:
            return False
    return True


def getattr_proxy(name: str) -> float:
    mapping = {
        "cash": st.session_state.cash,
        "energy": st.session_state.energy,
        "intent": st.session_state.intent,
        "rejection": st.session_state.rejection,
        "risk": st.session_state.risk,
        "allies": st.session_state.allies,
        "credibility": st.session_state.credibility,
    }
    return mapping.get(name, 0.0)


def apply_effects(effects: Dict[str, float], risky: bool = False):
    if not effects:
        return
    st.session_state.intent = clamp(st.session_state.intent + effects.get("intent", 0), 0, 70)
    st.session_state.rejection = clamp(st.session_state.rejection + effects.get("rejection", 0), 0, 80)
    st.session_state.credibility = clamp(st.session_state.credibility + effects.get("credibility", 0), 0, 100)
    st.session_state.cash = max(0.0, st.session_state.cash + effects.get("cash", 0))
    st.session_state.energy = clamp(st.session_state.energy + effects.get("energy", 0), 0, 100)
    st.session_state.media = clamp(st.session_state.media + effects.get("media", 0), 0, 100)
    st.session_state.risk = clamp(st.session_state.risk + effects.get("risk", 0), 0, 100)
    st.session_state.allies = clamp(st.session_state.allies + effects.get("allies", 0), 0, 100)
    st.session_state.time_tv = clamp(st.session_state.time_tv + effects.get("time_tv", 0), 0, 100)
    st.session_state.momentum = clamp(st.session_state.momentum + effects.get("momentum", 0), -20, 20)
    st.session_state.narrative = clamp(st.session_state.narrative + effects.get("narrative", 0), 0, 100)
    st.session_state.viral = clamp(st.session_state.viral + effects.get("viral", 0), 0, 100)
    st.session_state.governabilidade = clamp(st.session_state.governabilidade + effects.get("governabilidade", 0), 0, 100)

    region_key_map = {
        "Norte": "Norte",
        "Nordeste": "Nordeste",
        "Centro-Oeste": "Centro-Oeste",
        "Sudeste": "Sudeste",
        "Sul": "Sul",
    }
    for key in region_key_map:
        if key in effects:
            st.session_state.regions[key] = clamp(st.session_state.regions[key] + effects[key] * 0.8, 0, 80)

    for seg in st.session_state.segments.keys():
        if seg in effects:
            st.session_state.segments[seg] = clamp(st.session_state.segments[seg] + effects[seg] * 0.8, 0, 80)

    # thematic spillover
    if effects.get("periferia"):
        st.session_state.regions["Nordeste"] = clamp(st.session_state.regions["Nordeste"] + effects["periferia"] * 0.25, 0, 80)
    if effects.get("agro"):
        st.session_state.regions["Centro-Oeste"] = clamp(st.session_state.regions["Centro-Oeste"] + effects["agro"] * 0.4, 0, 80)
        st.session_state.regions["Sul"] = clamp(st.session_state.regions["Sul"] + effects["agro"] * 0.3, 0, 80)
    if effects.get("evangelicos"):
        st.session_state.regions["Nordeste"] = clamp(st.session_state.regions["Nordeste"] + effects["evangelicos"] * 0.18, 0, 80)
    if effects.get("empreendedores"):
        st.session_state.regions["Sudeste"] = clamp(st.session_state.regions["Sudeste"] + effects["empreendedores"] * 0.28, 0, 80)
    if effects.get("jovens"):
        st.session_state.viral = clamp(st.session_state.viral + effects["jovens"] * 0.25, 0, 100)

    if risky and (effects.get("risk", 0) > 0 or effects.get("rejection", 0) > 1.0):
        st.session_state.scandals += 1

    positive = effects.get("intent", 0) + effects.get("credibility", 0) / 4 - effects.get("rejection", 0)
    if positive > 0.8:
        st.session_state.combo += 1
    else:
        st.session_state.combo = 0
    st.session_state.max_combo = max(st.session_state.max_combo, st.session_state.combo)
    if st.session_state.combo >= 3:
        st.session_state.momentum = clamp(st.session_state.momentum + 1.0, -20, 20)


def add_consequence(cons: Consequence):
    entry = {
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
    }
    st.session_state.active_consequences.append(entry)


def process_consequences() -> List[str]:
    notes = []
    remaining = []
    for cons in st.session_state.active_consequences:
        apply_effects(cons["daily"])
        st.session_state.consequence_turns_survived += 1
        notes.append(f"{cons['title']}: efeitos contínuos aplicados.")
        if cons["followup_event"] and not cons["triggered_followup"] and random.random() < cons["followup_chance"]:
            st.session_state.followup_queue.append(cons["followup_event"])
            cons["triggered_followup"] = True
            notes.append(f"Consequência escalou para: {cons['followup_event'].replace('_', ' ')}")
        cons["days_left"] -= 1
        if cons["days_left"] <= 0:
            apply_effects(cons["end_effects"])
        else:
            remaining.append(cons)
    st.session_state.active_consequences = remaining
    return notes


def rival_turn():
    for _, rival in st.session_state.rivals.items():
        drift = random.uniform(-0.7, 0.9)
        if rival["perfil"] == "digital":
            drift += 0.16 if st.session_state.viral < 24 else -0.06
        if rival["perfil"] == "gestao":
            drift += 0.15 if st.session_state.credibility < 46 else -0.05
        if rival["perfil"] == "estrutura":
            drift += 0.14 if st.session_state.allies < 48 else -0.04
        rival["voto"] = clamp(rival["voto"] + drift, 8, 42)
        rival["rejeicao"] = clamp(rival["rejeicao"] + random.uniform(-0.4, 0.8), 10, 60)


def daily_decay_and_growth():
    st.session_state.energy = clamp(st.session_state.energy - random.uniform(2.5, 5.5), 0, 100)
    st.session_state.cash = max(0.0, st.session_state.cash - random.uniform(3500, 9000))
    st.session_state.media = clamp(st.session_state.media + random.uniform(-2.5, 2.5) + st.session_state.momentum * 0.05, 0, 100)
    st.session_state.risk = clamp(st.session_state.risk + random.uniform(-1.0, 2.0), 0, 100)

    region_avg = sum(st.session_state.regions.values()) / len(st.session_state.regions)
    segment_score = 0.0
    for seg, info in SEGMENTOS.items():
        segment_score += st.session_state.segments[seg] * info["peso"]
    segment_score /= sum(v["peso"] for v in SEGMENTOS.values())

    structural = (
        st.session_state.credibility * 0.18
        + st.session_state.media * 0.12
        + st.session_state.time_tv * 0.08
        + st.session_state.allies * 0.08
        + region_avg * 0.22
        + segment_score * 0.20
        + st.session_state.momentum * 0.55
        + st.session_state.viral * 0.07
        - st.session_state.rejection * 0.22
        - st.session_state.risk * 0.16
    )
    target_vote = clamp(12 + structural / 3.3, 6, 55)

    # voto útil na reta final
    if st.session_state.day >= st.session_state.total_days - 5 and st.session_state.intent > 23:
        target_vote += 1.4
    if st.session_state.day >= st.session_state.total_days - 3 and st.session_state.rejection > 36:
        target_vote -= 1.0

    st.session_state.intent = clamp(st.session_state.intent + (target_vote - st.session_state.intent) * 0.18, 4, 60)
    st.session_state.rejection = clamp(st.session_state.rejection + random.uniform(-0.5, 0.9), 4, 65)


def add_history(label: str, option_text: str):
    st.session_state.history.insert(0, f"Dia {st.session_state.day}: {label} → {option_text}")
    st.session_state.history = st.session_state.history[:18]


def unlock_achievements():
    if st.session_state.viral >= 25 and "primeiro_viral" not in st.session_state.achievements:
        st.session_state.achievements.append("primeiro_viral")
    if st.session_state.recovery_flag and st.session_state.intent >= 25 and "virou_o_jogo" not in st.session_state.achievements:
        st.session_state.achievements.append("virou_o_jogo")
    if st.session_state.cash >= 200000 and "caixa_forte" not in st.session_state.achievements:
        st.session_state.achievements.append("caixa_forte")
    if st.session_state.media >= 70 and "mestre_midia" not in st.session_state.achievements:
        st.session_state.achievements.append("mestre_midia")
    if st.session_state.risk <= 10 and st.session_state.day >= 18 and "blindado" not in st.session_state.achievements:
        st.session_state.achievements.append("blindado")
    if st.session_state.max_combo >= 4 and "furacao" not in st.session_state.achievements:
        st.session_state.achievements.append("furacao")
    if st.session_state.regions["Nordeste"] >= 33 and "lider_nordeste" not in st.session_state.achievements:
        st.session_state.achievements.append("lider_nordeste")
    if st.session_state.regions["Sudeste"] >= 31 and "lider_sudeste" not in st.session_state.achievements:
        st.session_state.achievements.append("lider_sudeste")
    if st.session_state.scandals == 0 and st.session_state.day >= 25 and "sem_escandalo" not in st.session_state.achievements:
        st.session_state.achievements.append("sem_escandalo")
    if st.session_state.consequence_turns_survived >= 6 and "consequencia_mestre" not in st.session_state.achievements:
        st.session_state.achievements.append("consequencia_mestre")
    if st.session_state.scandals >= 2 and st.session_state.intent >= 24 and "sobreviveu_crise" not in st.session_state.achievements:
        st.session_state.achievements.append("sobreviveu_crise")


def check_game_over():
    if st.session_state.intent <= 5:
        st.session_state.game_over = True
        st.session_state.victory = False
        st.session_state.result_text = "Sua intenção de voto derreteu. A campanha virou rodapé de análise e acabou antes da urna."
    elif st.session_state.cash <= 0:
        st.session_state.game_over = True
        st.session_state.victory = False
        st.session_state.result_text = "O caixa acabou. Você tinha discurso, mas não tinha gasolina eleitoral."
    elif st.session_state.energy <= 0:
        st.session_state.game_over = True
        st.session_state.victory = False
        st.session_state.result_text = "Você apagou no meio da campanha. O corpo não acompanhou o roteiro."
    elif st.session_state.risk >= 92:
        st.session_state.game_over = True
        st.session_state.victory = False
        st.session_state.result_text = "A campanha entrou em espiral jurídica. O noticiário te engoliu antes da reta final."


def simulate_final_result():
    region_vote = 0.0
    for region, info in REGIOES.items():
        region_vote += st.session_state.regions[region] * info["peso"]
    region_vote /= sum(v["peso"] for v in REGIOES.values())

    segment_vote = 0.0
    for seg, info in SEGMENTOS.items():
        segment_vote += st.session_state.segments[seg] * info["peso"]
    segment_vote /= sum(v["peso"] for v in SEGMENTOS.values())

    your_vote = clamp(
        st.session_state.intent * 0.44
        + region_vote * 0.20
        + segment_vote * 0.18
        + st.session_state.credibility * 0.10
        + st.session_state.time_tv * 0.04
        + st.session_state.governabilidade * 0.03
        + st.session_state.momentum * 0.15
        - st.session_state.rejection * 0.20,
        8,
        58,
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
        st.session_state.result_text = f"Você venceu no 1º turno com {your_vote:.1f}% dos votos válidos. O país entrou no modo ressaca eleitoral e seu nome virou assunto de mesa, feed e grupo de família."
        if "primeiro_turno" not in st.session_state.achievements:
            st.session_state.achievements.append("primeiro_turno")
        return

    transferable = max(0.0, 100 - your_vote - top_rival_vote)
    your_transfer = transferable * (
        0.49 + (st.session_state.credibility - st.session_state.rejection) / 220 + st.session_state.governabilidade / 320
    )
    rival_transfer = transferable - your_transfer
    second_you = clamp(your_vote + your_transfer, 20, 80)
    second_rival = clamp(top_rival_vote + rival_transfer, 20, 80)
    total2 = second_you + second_rival
    second_you = second_you * 100 / total2
    second_rival = second_rival * 100 / total2

    st.session_state.game_over = True
    if second_you > second_rival:
        st.session_state.victory = True
        st.session_state.result_text = f"Você foi ao 2º turno contra {st.session_state.rivals[top_rival_key]['nome']} e venceu por {second_you:.1f}% a {second_rival:.1f}%. Vitória sofrida, daquelas que deixam metade do país sem dormir e a outra metade sem voz."
    else:
        st.session_state.victory = False
        st.session_state.result_text = f"Você chegou ao 2º turno, mas perdeu para {st.session_state.rivals[top_rival_key]['nome']} por {second_rival:.1f}% a {second_you:.1f}%. Faltou um pouco de fôlego, viabilidade ou sangue frio."


def next_day(option: Option):
    notes = []
    apply_effects(option.effects, risky=option.risky)
    for cons in option.consequences:
        add_consequence(cons)
        notes.append(f"Consequência ativada: {cons.title}")

    cons_notes = process_consequences()
    notes.extend(cons_notes)

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

    st.session_state.last_feedback = option.summary + ("\n\n" + " | ".join(notes) if notes else "")
    check_game_over()
    if st.session_state.game_over:
        return

    st.session_state.day += 1
    if st.session_state.day > st.session_state.total_days:
        simulate_final_result()
    else:
        generate_event()


# =========================================================
# UI
# =========================================================
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
            st.markdown(
                f"<div class='metric-card'><h4>{title}</h4><h2>{value}</h2><span>{desc}</span></div>",
                unsafe_allow_html=True,
            )


def sidebar_panel():
    with st.sidebar:
        st.markdown("## 🎛️ Painel da campanha")
        st.caption(f"Seed: {st.session_state.get('seed', '-')}")
        if st.session_state.started:
            st.write(f"**Dia:** {st.session_state.day}/{st.session_state.total_days}")
            st.write(f"**Partido:** {PARTIDOS[st.session_state.party]['nome']}")
            st.write(f"**Assessor:** {ASSESSORES[st.session_state.advisor]['nome']}")
            st.write(f"**Dificuldade:** {st.session_state.difficulty}")
            st.progress(clamp(st.session_state.intent / 50, 0, 1), text="competitividade")
            st.progress(clamp((100 - st.session_state.rejection) / 100, 0, 1), text="aceitação")
            st.progress(clamp(st.session_state.energy / 100, 0, 1), text="energia")
            st.progress(clamp(st.session_state.governabilidade / 100, 0, 1), text="governabilidade")

            if st.session_state.combo >= 2:
                st.success(f"🔥 Combo ativo x{st.session_state.combo}")
            if st.session_state.active_consequences:
                st.warning(f"⚠️ {len(st.session_state.active_consequences)} consequência(s) ativa(s)")
            if st.session_state.risk > 55:
                st.error("🚨 Campanha flertando com crise grande")
            elif st.session_state.risk > 35:
                st.warning("⚠️ Risco subindo")
            if st.session_state.cash < 35000:
                st.warning("💸 Caixa crítico")
            if st.session_state.intent < 18:
                st.warning("📉 Você está vivo, mas não confortável")

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
                st.caption("Nenhuma desbloqueada ainda.")

            st.markdown("---")
            if st.button("🔄 Reiniciar campanha", use_container_width=True):
                init_state(True)
                st.rerun()


def render_charts():
    left, right = st.columns([1.2, 1])

    with left:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=st.session_state.day_history, y=st.session_state.poll_history, mode="lines+markers", name="Intenção"))
        fig.add_trace(go.Scatter(x=st.session_state.day_history, y=st.session_state.rej_history, mode="lines+markers", name="Rejeição"))
        fig.update_layout(height=310, margin=dict(l=10, r=10, t=30, b=10), title="Pesquisa da campanha")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("<div class='panel'><h4 style='margin-top:0'>Mapa por regiões</h4>", unsafe_allow_html=True)
        colors = {
            "Norte": "#0ea5e9",
            "Nordeste": "#f59e0b",
            "Centro-Oeste": "#22c55e",
            "Sudeste": "#6366f1",
            "Sul": "#ef4444",
        }
        for region, value in st.session_state.regions.items():
            st.markdown(
                f"<div class='region-row'><div style='display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px'><span><strong>{region}</strong></span><span>{value:.1f}%</span></div><div style='background:#e5e7eb;border-radius:999px;height:10px;overflow:hidden'><div style='background:{colors[region]};width:{max(1,value)}%;height:10px;border-radius:999px'></div></div></div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)


def render_setup():
    st.markdown(
        """
        <div class='hero'>
            <h1>🇧🇷 Candidato 2026: Viral Edition V4</h1>
            <p>Agora com consequências persistentes, follow-ups, 1º e 2º turno, governabilidade e campanha mais viva.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🏛️ Partido")
        party = st.radio(
            "Escolha sua base política",
            list(PARTIDOS.keys()),
            format_func=lambda k: f"{PARTIDOS[k]['nome']} — {PARTIDOS[k]['slogan']}",
            key="party_setup",
        )
    with c2:
        st.markdown("### 🧠 Assessor principal")
        advisor = st.radio(
            "Quem puxa sua campanha?",
            list(ASSESSORES.keys()),
            format_func=lambda k: f"{ASSESSORES[k]['icone']} {ASSESSORES[k]['nome']}",
            key="advisor_setup",
        )
    with c3:
        st.markdown("### ⚙️ Dificuldade")
        diff = st.radio("Nível", ["Fácil", "Normal", "Difícil", "Hardcore"], index=1, key="diff_setup")

    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.write("**O que mudou nesta versão**")
    st.write(
        "- respostas geram consequências por vários dias;\n"
        "- decisões ruins podem voltar como follow-up;\n"
        "- política, mídia, TSE e alianças se encadeiam;\n"
        "- vitória considera governabilidade e transferência de votos no 2º turno."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀 Começar campanha", use_container_width=True):
        init_state(False)
        st.session_state.party = party
        st.session_state.advisor = advisor
        st.session_state.difficulty = diff
        st.session_state.started = True
        apply_setup_choices()
        st.rerun()


def render_active_consequences():
    st.markdown("### ⏳ Consequências em andamento")
    if not st.session_state.active_consequences:
        st.info("Nenhuma consequência ativa agora. Aproveite enquanto o Brasil deixa.")
        return
    for cons in st.session_state.active_consequences:
        badge = "tag-red" if cons["severity"] == "danger" else "tag-green" if cons["severity"] == "good" else "tag-blue"
        chips = "".join(metric_delta_chip(k, v) for k, v in cons["daily"].items())
        st.markdown(
            f"<div class='consequence-card'><strong>{cons['title']}</strong> <span class='tag {badge}'>{cons['days_left']} dia(s)</span><div class='small-muted' style='margin-top:6px'>{cons['desc']}</div><div style='margin-top:8px'>{chips}</div></div>",
            unsafe_allow_html=True,
        )


def render_event():
    event = st.session_state.event
    tone_class = "event-box"
    if event.tone == "crisis":
        tone_class += " event-crisis"
    elif event.tone == "good":
        tone_class += " event-good"
    elif event.followup_only:
        tone_class += " event-followup"

    tag_class = "tag-blue"
    if event.tone == "crisis":
        tag_class = "tag-red"
    elif event.tone == "good":
        tag_class = "tag-green"
    elif event.followup_only:
        tag_class = "tag-purple"

    st.markdown(f"<div class='{tone_class}'>", unsafe_allow_html=True)
    st.markdown(f"### {event.title}")
    st.write(event.desc)
    tags_html = " ".join([f"<span class='tag {tag_class}'>{tag}</span>" for tag in event.tags])
    st.markdown(tags_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.last_feedback:
        st.markdown("<div class='success-strip'>" + st.session_state.last_feedback + "</div>", unsafe_allow_html=True)

    st.markdown("### Escolha sua resposta")
    for idx, option in enumerate(event.options):
        enabled = option_enabled(option)
        st.markdown("<div class='choice-box'>", unsafe_allow_html=True)
        st.markdown(f"<div class='choice-title'>{idx+1}. {option.text}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-muted'>{option.summary}</div>", unsafe_allow_html=True)
        if option.consequences:
            st.caption("Consequências possíveis: " + ", ".join(c.title for c in option.consequences))
        if option.requirement:
            st.caption("Exige: " + ", ".join(f"{k} ≥ {v}" for k, v in option.requirement.items()))
        if st.button("Escolher", key=f"choice_{event.id}_{idx}", use_container_width=True, disabled=not enabled):
            next_day(option)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def render_bottom_panels():
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='panel'><h4 style='margin-top:0'>Segmentos decisivos</h4>", unsafe_allow_html=True)
        for seg, info in SEGMENTOS.items():
            value = st.session_state.segments[seg]
            st.markdown(
                f"<div style='margin-bottom:10px'><div style='display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px'><span><strong>{info['nome']}</strong></span><span>{value:.1f}%</span></div><div style='background:#e5e7eb;border-radius:999px;height:10px;overflow:hidden'><div style='background:#8b5cf6;width:{max(1,value)}%;height:10px;border-radius:999px'></div></div></div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='panel'><h4 style='margin-top:0'>Diário de campanha</h4>", unsafe_allow_html=True)
        if st.session_state.history:
            for item in st.session_state.history[:8]:
                st.write("•", item)
        else:
            st.caption("Nenhum movimento registrado ainda.")
        st.markdown("</div>", unsafe_allow_html=True)


def render_results():
    color_class = "success-strip" if st.session_state.victory else "warning-strip"
    st.markdown(f"<div class='{color_class}'>{st.session_state.result_text}</div>", unsafe_allow_html=True)

    final_standing = sorted(
        [("Você", st.session_state.intent)] + [(v["nome"], v["voto"]) for v in st.session_state.rivals.values()],
        key=lambda x: x[1],
        reverse=True,
    )
    st.markdown("### 🗳️ Termômetro final")
    for name, value in final_standing:
        st.write(f"**{name}** — {value:.1f}%")

    if st.session_state.victory:
        govern_msg = "governo nasce com margem de manobra" if st.session_state.governabilidade >= 55 else "vitória veio, mas a governabilidade exigirá negociação pesada"
        st.markdown(
            f"<div class='gov-box'><h4 style='margin-top:0'>🏛️ Pós-vitória</h4><p style='margin-bottom:8px'>Sua governabilidade fechou em <strong>{st.session_state.governabilidade:.1f}</strong>. Isso significa que o {govern_msg}.</p><p style='margin:0'>Aliados: <strong>{st.session_state.allies:.1f}</strong> | Tempo de TV herdado: <strong>{st.session_state.time_tv:.1f}</strong> | Risco residual: <strong>{st.session_state.risk:.1f}</strong>%</p></div>",
            unsafe_allow_html=True,
        )

    if st.button("🔁 Jogar novamente", use_container_width=True):
        init_state(True)
        st.rerun()


def main():
    if "started" not in st.session_state:
        init_state(True)

    sidebar_panel()

    if not st.session_state.started:
        render_setup()
        return

    st.markdown(
        f"""
        <div class='hero'>
            <h1>🇧🇷 Corrida presidencial — Dia {st.session_state.day}</h1>
            <p>{PARTIDOS[st.session_state.party]['nome']} • {ASSESSORES[st.session_state.advisor]['icone']} {ASSESSORES[st.session_state.advisor]['nome']} • narrativa em disputa</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_metric_cards()
    st.write("")

    top_left, top_right = st.columns([1.35, 0.9])
    with top_left:
        if st.session_state.game_over:
            render_results()
        else:
            render_event()
    with top_right:
        render_active_consequences()

    st.write("")
    render_charts()
    st.write("")
    render_bottom_panels()


if __name__ == "__main__":
    main()
