
import streamlit as st
import random
import math
from copy import deepcopy
from datetime import datetime
import plotly.graph_objects as go

# =============================================================================
# CONFIG
# =============================================================================
st.set_page_config(
    page_title="🇧🇷 Candidato 2026 V2",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CSS
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    * { font-family: 'Inter', sans-serif; box-sizing: border-box; }

    .game-header {
        background: linear-gradient(135deg, #0f172a 0%, #172554 40%, #1e3a8a 100%);
        padding: 26px 28px;
        border-radius: 22px;
        color: white;
        margin-bottom: 18px;
        box-shadow: 0 16px 45px rgba(15,23,42,0.35);
        border: 1px solid rgba(255,255,255,0.08);
    }

    .panel-card {
        background: white;
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.06);
        border: 1px solid #eef2f7;
        margin-bottom: 12px;
    }

    .metric-card {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        padding: 18px 14px;
        border-radius: 18px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 24px rgba(0,0,0,0.22);
        margin: 4px 0;
    }
    .metric-card h3 { margin: 0; font-size: 11px; opacity: .78; text-transform: uppercase; letter-spacing: 1.1px; }
    .metric-card h1 { margin: 8px 0 0 0; font-size: 28px; font-weight: 800; }

    .event-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 24px;
        border-radius: 22px;
        border-left: 7px solid #2563eb;
        box-shadow: 0 10px 35px rgba(0,0,0,0.10);
        margin: 16px 0 20px 0;
    }
    .event-card.crise { border-left-color: #dc2626; background: linear-gradient(135deg, #fff5f5 0%, #fff1f2 100%); }
    .event-card.oportunidade { border-left-color: #16a34a; background: linear-gradient(135deg, #f0fdf4 0%, #f7fee7 100%); }
    .event-card.final { border-left-color: #7c3aed; background: linear-gradient(135deg, #faf5ff 0%, #f5f3ff 100%); }

    .tag {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
        margin-right: 6px;
        margin-top: 10px;
        color: white;
    }

    .option-box {
        background: white;
        padding: 16px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 5px 18px rgba(0,0,0,0.04);
        margin-bottom: 10px;
    }

    .advisor-note {
        background: linear-gradient(135deg, #eff6ff 0%, #eef2ff 100%);
        border-left: 4px solid #2563eb;
        padding: 12px 14px;
        border-radius: 12px;
        font-size: 13px;
        margin: 10px 0;
        color: #1e293b;
    }

    .small-note {
        background: #f8fafc;
        border-left: 4px solid #94a3b8;
        padding: 10px 12px;
        border-radius: 10px;
        color: #334155;
        font-size: 13px;
        margin: 8px 0;
    }

    .good-box {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 5px solid #16a34a;
        color: #14532d;
        padding: 14px 16px;
        border-radius: 14px;
        font-weight: 600;
        margin: 12px 0;
    }

    .bad-box {
        background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
        border-left: 5px solid #dc2626;
        color: #7f1d1d;
        padding: 14px 16px;
        border-radius: 14px;
        font-weight: 600;
        margin: 12px 0;
    }

    .final-box {
        color: white;
        padding: 36px 28px;
        border-radius: 26px;
        text-align: center;
        margin: 18px 0;
        box-shadow: 0 18px 55px rgba(0,0,0,0.18);
    }

    .victory { background: linear-gradient(135deg, #059669 0%, #10b981 50%, #22c55e 100%); }
    .defeat { background: linear-gradient(135deg, #b91c1c 0%, #ef4444 50%, #f97316 100%); }
    .second-turn { background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 50%, #2563eb 100%); }

    .region-line {
        background: #fff;
        border: 1px solid #e5e7eb;
        padding: 10px 12px;
        border-radius: 12px;
        margin-bottom: 8px;
    }

    .history-item {
        padding: 12px 14px;
        border-radius: 12px;
        background: #fff;
        border: 1px solid #e5e7eb;
        margin-bottom: 8px;
    }

    .phase-chip {
        display: inline-block;
        color: white;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
    }

    .stButton>button {
        width: 100%;
        border-radius: 12px !important;
        border: none !important;
        background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 12px 16px !important;
        box-shadow: 0 8px 20px rgba(37,99,235,0.25) !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 26px rgba(37,99,235,0.30) !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# CONSTANTS
# =============================================================================
PHASES = [
    ("Pré-campanha", 1, 10),
    ("Lançamento", 11, 20),
    ("Consolidação", 21, 32),
    ("Pressão máxima", 33, 40),
    ("Reta final", 41, 45),
]

REGION_GROUPS = {
    "SE": ["SP", "MG", "RJ"],
    "NE": ["BA", "PE", "CE"],
    "SUL": ["RS", "PR"],
}

ESTADOS = {
    "SP": {"peso": 22.5, "perfil": ["economia", "gestao", "corrupcao", "classe_media"], "base": 16},
    "MG": {"peso": 10.8, "perfil": ["economia", "saude", "interior", "gestao"], "base": 18},
    "RJ": {"peso": 8.9, "perfil": ["seguranca", "midia", "corrupcao"], "base": 15},
    "BA": {"peso": 8.2, "perfil": ["social", "preco", "programa_social", "popular"], "base": 22},
    "RS": {"peso": 5.8, "perfil": ["agro", "impostos", "seguranca"], "base": 15},
    "PR": {"peso": 5.7, "perfil": ["agro", "economia", "seguranca"], "base": 14},
    "PE": {"peso": 4.8, "perfil": ["social", "preco", "saude", "popular"], "base": 21},
    "CE": {"peso": 4.6, "perfil": ["social", "educacao", "popular"], "base": 21},
}

BLOCOS = {
    "baixa_renda": {"base": 24, "tags": ["social", "programa_social", "preco", "saude", "popular"]},
    "classe_media": {"base": 18, "tags": ["economia", "corrupcao", "seguranca", "gestao", "impostos"]},
    "empresariado": {"base": 14, "tags": ["economia", "mercado", "estabilidade", "impostos"]},
    "evangelicos": {"base": 20, "tags": ["familia", "igreja", "costumes", "seguranca"]},
    "jovens": {"base": 17, "tags": ["redes", "educacao", "emprego", "inovacao"]},
    "agro": {"base": 15, "tags": ["agro", "infraestrutura", "impostos", "ambiental"]},
    "servidores": {"base": 18, "tags": ["gestao", "salario", "estabilidade", "saude", "educacao"]},
    "mulheres": {"base": 20, "tags": ["saude", "seguranca", "respeito", "preco"]},
}

ADVISORS = {
    "estrategista": {"nome": "Carlos Mendes", "cargo": "Estrategista", "confiabilidade": 0.86, "area": "voto"},
    "comunicacao": {"nome": "Pedro Santos", "cargo": "Comunicação", "confiabilidade": 0.74, "area": "narrativa"},
    "juridico": {"nome": "Dra. Helena Lima", "cargo": "Jurídico", "confiabilidade": 0.96, "area": "risco"},
    "financeiro": {"nome": "Ana Rodrigues", "cargo": "Financeiro", "confiabilidade": 0.92, "area": "caixa"},
    "politico": {"nome": "Roberto Costa", "cargo": "Articulação", "confiabilidade": 0.79, "area": "coalizao"},
}

ACHIEVEMENTS = {
    "primeira": {"icon": "🎯", "name": "Primeira decisão"},
    "acima_30": {"icon": "📈", "name": "Em ascensão"},
    "acima_40": {"icon": "🔥", "name": "Entrou no jogo"},
    "acima_50": {"icon": "👑", "name": "Líder das pesquisas"},
    "sem_crise": {"icon": "🛡️", "name": "Blindado"},
    "caixa_200": {"icon": "💰", "name": "Cofre cheio"},
    "virada": {"icon": "🔄", "name": "Virada histórica"},
}

# =============================================================================
# EVENT BANK
# =============================================================================
EVENTS = [
    {
        "id": "pesquisa_vazou",
        "titulo": "📊 Pesquisa interna vaza para a imprensa",
        "descricao": "Um recorte parcial de uma pesquisa da sua equipe foi parar em grupos de jornalistas. O vazamento mostra desempenho fraco no Sudeste, mas crescimento no Nordeste.",
        "categoria": "midia",
        "fase_min": 1,
        "fase_max": 5,
        "duracao": 1,
        "tags": ["midia", "narrativa", "regioes"],
        "classe": "oportunidade",
        "publicos": ["classe_media", "baixa_renda", "jovens"],
        "regioes": ["SE", "NE"],
        "opcoes": [
            {
                "texto": "Assumir os números e vender a ideia de crescimento",
                "efeitos": {"voto": 1.6, "narrativa": 6, "midia": 5, "energia": -5, "risco": -2},
                "tags": ["narrativa", "midia", "popular"],
                "conseq": [{"id": "onda_otimismo", "dias": 2, "efeitos": {"narrativa": 1.4, "voto": 0.4}}],
                "tempo": 1
            },
            {
                "texto": "Negar a pesquisa e acusar manipulação",
                "efeitos": {"voto": -1.2, "narrativa": -4, "midia": -6, "energia": -3, "risco": 4},
                "tags": ["midia", "corrupcao"],
                "conseq": [{"id": "checagem_negativa", "dias": 2, "efeitos": {"midia": -1.5, "rejeicao": 0.6}}],
                "tempo": 1
            },
            {
                "texto": "Silêncio estratégico e agenda positiva",
                "efeitos": {"voto": 0.5, "narrativa": 1, "midia": -2, "energia": 2, "risco": 0},
                "tags": ["gestao"],
                "conseq": [],
                "tempo": 1
            },
        ]
    },
    {
        "id": "debate_inflacao",
        "titulo": "📺 Debate nacional: inflação e preço dos alimentos",
        "descricao": "No maior debate da campanha, o foco é o custo de vida. O eleitor quer resposta direta para mercado, supermercado e botijão.",
        "categoria": "debate",
        "fase_min": 2,
        "fase_max": 5,
        "duracao": 2,
        "tags": ["economia", "preco", "popular"],
        "classe": "crise",
        "publicos": ["baixa_renda", "classe_media", "mulheres"],
        "regioes": ["SE", "NE"],
        "opcoes": [
            {
                "texto": "Anunciar pacote emergencial contra alta dos alimentos",
                "efeitos": {"voto": 2.4, "narrativa": 7, "caixa": -18000, "energia": -10, "risco": 2, "mercado": -4},
                "tags": ["social", "programa_social", "preco", "popular"],
                "conseq": [{"id": "editorial_mercado", "dias": 3, "efeitos": {"midia": -0.7, "empresariado": -1.2}}],
                "tempo": 2
            },
            {
                "texto": "Defender ajuste fiscal, metas e credibilidade",
                "efeitos": {"voto": -0.8, "narrativa": 3, "caixa": 5000, "energia": -8, "risco": -2, "mercado": 6},
                "tags": ["economia", "mercado", "estabilidade"],
                "conseq": [{"id": "apoio_mercado", "dias": 3, "efeitos": {"caixa": 4000, "empresariado": 1.5}}],
                "tempo": 2
            },
            {
                "texto": "Atacar adversários e culpar os últimos governos",
                "efeitos": {"voto": 0.3, "narrativa": -3, "energia": -7, "midia": -3, "risco": 2},
                "tags": ["corrupcao", "midia"],
                "conseq": [{"id": "falta_proposta", "dias": 2, "efeitos": {"classe_media": -1.2, "midia": -1.0}}],
                "tempo": 2
            },
        ]
    },
    {
        "id": "crime_repercussao",
        "titulo": "🚔 Crime de grande repercussão domina o noticiário",
        "descricao": "Um caso brutal monopoliza a imprensa e as redes. Segurança pública vira o tema número 1 do país por 72 horas.",
        "categoria": "seguranca",
        "fase_min": 2,
        "fase_max": 5,
        "duracao": 1,
        "tags": ["seguranca", "midia"],
        "classe": "crise",
        "publicos": ["classe_media", "mulheres", "evangelicos"],
        "regioes": ["RJ", "SE"],
        "opcoes": [
            {
                "texto": "Apresentar plano firme de segurança com metas",
                "efeitos": {"voto": 1.8, "narrativa": 5, "energia": -6, "risco": 0},
                "tags": ["seguranca", "gestao"],
                "conseq": [{"id": "cobranca_resultados", "dias": 2, "efeitos": {"narrativa": 0.8}}],
                "tempo": 1
            },
            {
                "texto": "Discurso emocional e visita às famílias",
                "efeitos": {"voto": 1.0, "narrativa": 4, "midia": 2, "energia": -8, "risco": 1},
                "tags": ["respeito", "popular"],
                "conseq": [],
                "tempo": 1
            },
            {
                "texto": "Falar pouco e evitar exploração política",
                "efeitos": {"voto": -1.0, "narrativa": -2, "energia": 2, "risco": -1},
                "tags": ["gestao"],
                "conseq": [{"id": "imagem_fria", "dias": 2, "efeitos": {"mulheres": -1.0, "midia": -0.8}}],
                "tempo": 1
            },
        ]
    },
    {
        "id": "pastor_ambig",
        "titulo": "⛪ Pastor influente faz apoio ambíguo",
        "descricao": "Um líder religioso enorme elogia seu discurso sobre família, mas evita dizer se o apoio é oficial. A imprensa pressiona por uma resposta.",
        "categoria": "religiao",
        "fase_min": 1,
        "fase_max": 5,
        "duracao": 1,
        "tags": ["igreja", "familia", "midia"],
        "classe": "oportunidade",
        "publicos": ["evangelicos", "mulheres"],
        "regioes": ["NE", "SE"],
        "opcoes": [
            {
                "texto": "Agradecer sem transformar em palanque",
                "efeitos": {"voto": 1.2, "narrativa": 4, "risco": -1, "energia": -2},
                "tags": ["igreja", "respeito", "familia"],
                "conseq": [],
                "tempo": 1
            },
            {
                "texto": "Explorar o apoio como se fosse oficial",
                "efeitos": {"voto": 1.8, "narrativa": 3, "midia": -3, "risco": 5},
                "tags": ["igreja", "midia"],
                "conseq": [{"id": "desmentido_lider", "dias": 2, "efeitos": {"midia": -2.0, "rejeicao": 0.8}}],
                "tempo": 1
            },
            {
                "texto": "Evitar o tema e focar em economia",
                "efeitos": {"voto": 0.1, "narrativa": -1, "energia": 1, "risco": 0},
                "tags": ["economia"],
                "conseq": [],
                "tempo": 1
            },
        ]
    },
    {
        "id": "pf_aliado",
        "titulo": "🚨 Operação da PF atinge aliado regional",
        "descricao": "Um aliado importante em um estado decisivo é alvo de busca e apreensão. Seu adversário exige rompimento imediato.",
        "categoria": "corrupcao",
        "fase_min": 2,
        "fase_max": 5,
        "duracao": 2,
        "tags": ["corrupcao", "midia", "coalizao"],
        "classe": "crise",
        "publicos": ["classe_media", "servidores", "mulheres"],
        "regioes": ["MG", "BA", "SE"],
        "opcoes": [
            {
                "texto": "Romper apoio publicamente e abrir auditoria interna",
                "efeitos": {"voto": 2.1, "narrativa": 6, "coalizao": -8, "caixa": -6000, "energia": -9, "risco": -4},
                "tags": ["corrupcao", "gestao"],
                "conseq": [{"id": "ressaca_coalizao", "dias": 3, "efeitos": {"coalizao": -1.2}}],
                "tempo": 2
            },
            {
                "texto": "Defender presunção de inocência e esperar fatos",
                "efeitos": {"voto": -1.8, "narrativa": -4, "coalizao": 3, "midia": -5, "risco": 4},
                "tags": ["corrupcao", "politica"],
                "conseq": [{"id": "editorial_duro", "dias": 3, "efeitos": {"midia": -1.4, "rejeicao": 0.7}}],
                "tempo": 2
            },
            {
                "texto": "Criar comitê de compliance e congelar agenda conjunta",
                "efeitos": {"voto": 0.9, "narrativa": 4, "coalizao": -3, "caixa": -4000, "risco": -2},
                "tags": ["gestao", "corrupcao"],
                "conseq": [],
                "tempo": 2
            },
        ]
    },
    {
        "id": "governador_ba",
        "titulo": "🤝 Governador da Bahia oferece palanque conjunto",
        "descricao": "Um governador com força regional quer dividir palco em Salvador e interior. O apoio pode te impulsionar no Nordeste, mas gerar reação em outros polos.",
        "categoria": "regional",
        "fase_min": 1,
        "fase_max": 4,
        "duracao": 1,
        "tags": ["regioes", "nordeste", "coalizao"],
        "classe": "oportunidade",
        "publicos": ["baixa_renda", "servidores"],
        "regioes": ["BA", "NE"],
        "opcoes": [
            {
                "texto": "Aceitar o palanque e regionalizar o discurso",
                "efeitos": {"voto": 1.7, "narrativa": 4, "coalizao": 5, "energia": -5},
                "tags": ["social", "popular", "regioes"],
                "conseq": [{"id": "reacao_sul", "dias": 2, "efeitos": {"RS": -0.5, "PR": -0.4}}],
                "tempo": 1
            },
            {
                "texto": "Negociar apoio discreto sem dividir palco",
                "efeitos": {"voto": 0.9, "narrativa": 2, "coalizao": 3, "energia": -2},
                "tags": ["politica", "gestao"],
                "conseq": [],
                "tempo": 1
            },
            {
                "texto": "Recusar para parecer independente",
                "efeitos": {"voto": -0.6, "narrativa": 1, "coalizao": -4, "energia": 1},
                "tags": ["narrativa"],
                "conseq": [{"id": "prefeitos_irritados", "dias": 2, "efeitos": {"coalizao": -1.0}}],
                "tempo": 1
            },
        ]
    },
    {
        "id": "tiktok_agressivo",
        "titulo": "📱 Equipe propõe campanha agressiva no TikTok",
        "descricao": "Seu time digital quer usar cortes irônicos, humor ácido e ataques rápidos contra rivais para ganhar tração entre jovens.",
        "categoria": "redes",
        "fase_min": 1,
        "fase_max": 5,
        "duracao": 1,
        "tags": ["redes", "jovens", "narrativa"],
        "classe": "oportunidade",
        "publicos": ["jovens", "classe_media"],
        "regioes": ["SE", "SUL", "NE"],
        "opcoes": [
            {
                "texto": "Liberar a estratégia com limite jurídico e revisão",
                "efeitos": {"voto": 1.5, "narrativa": 5, "energia": -4, "risco": 1},
                "tags": ["redes", "inovacao"],
                "conseq": [{"id": "viral_positivo", "dias": 2, "efeitos": {"jovens": 1.2, "narrativa": 1.0}}],
                "tempo": 1
            },
            {
                "texto": "Fazer campanha leve, sem ataques diretos",
                "efeitos": {"voto": 0.8, "narrativa": 2, "risco": -1},
                "tags": ["redes", "respeito"],
                "conseq": [],
                "tempo": 1
            },
            {
                "texto": "Bloquear tudo para não correr risco",
                "efeitos": {"voto": -0.7, "narrativa": -2, "energia": 1, "risco": -2},
                "tags": ["gestao"],
                "conseq": [{"id": "campanha_sem_pulso", "dias": 2, "efeitos": {"jovens": -1.0}}],
                "tempo": 1
            },
        ]
    },
    {
        "id": "enchente",
        "titulo": "🌧️ Enchente em estado decisivo muda a pauta",
        "descricao": "Uma enchente grave desloca famílias e colapsa a rotina de uma região importante. O país espera solidariedade, proposta e presença.",
        "categoria": "tragedia",
        "fase_min": 2,
        "fase_max": 5,
        "duracao": 2,
        "tags": ["saude", "respeito", "gestao"],
        "classe": "crise",
        "publicos": ["mulheres", "baixa_renda", "servidores"],
        "regioes": ["MG", "RJ", "BA"],
        "opcoes": [
            {
                "texto": "Ir ao local, anunciar ajuda e suspender ataques políticos",
                "efeitos": {"voto": 2.0, "narrativa": 6, "caixa": -12000, "energia": -12, "risco": -1},
                "tags": ["respeito", "saude", "popular"],
                "conseq": [{"id": "cobertura_humana", "dias": 2, "efeitos": {"midia": 1.2, "mulheres": 1.0}}],
                "tempo": 2
            },
            {
                "texto": "Mandar equipe e manter agenda normal",
                "efeitos": {"voto": 0.4, "narrativa": 1, "energia": -3},
                "tags": ["gestao"],
                "conseq": [],
                "tempo": 1
            },
            {
                "texto": "Politizar a tragédia e culpar adversários",
                "efeitos": {"voto": -1.6, "narrativa": -4, "midia": -5, "risco": 2},
                "tags": ["midia"],
                "conseq": [{"id": "reacao_negativa", "dias": 3, "efeitos": {"rejeicao": 0.7, "midia": -1.5}}],
                "tempo": 1
            },
        ]
    },
    {
        "id": "carta_empresarios",
        "titulo": "🏦 Setor empresarial exige carta de compromisso",
        "descricao": "Lideranças empresariais querem um documento público sobre metas, impostos, responsabilidade fiscal e segurança jurídica.",
        "categoria": "economia",
        "fase_min": 1,
        "fase_max": 5,
        "duracao": 1,
        "tags": ["economia", "mercado", "estabilidade"],
        "classe": "oportunidade",
        "publicos": ["empresariado", "classe_media"],
        "regioes": ["SP", "PR", "RS"],
        "opcoes": [
            {
                "texto": "Assinar carta técnica com metas e linguagem de estabilidade",
                "efeitos": {"voto": 0.8, "narrativa": 3, "caixa": 12000, "risco": -2, "mercado": 6},
                "tags": ["economia", "mercado", "gestao"],
                "conseq": [{"id": "doador_animado", "dias": 2, "efeitos": {"caixa": 5000, "empresariado": 1.0}}],
                "tempo": 1
            },
            {
                "texto": "Fazer carta genérica para agradar a todos",
                "efeitos": {"voto": 0.2, "narrativa": -1, "caixa": 3000, "risco": 1},
                "tags": ["economia"],
                "conseq": [{"id": "mercado_desconfiado", "dias": 2, "efeitos": {"empresariado": -0.8}}],
                "tempo": 1
            },
            {
                "texto": "Recusar e dizer que governo não se negocia em carta",
                "efeitos": {"voto": -0.6, "narrativa": 1, "caixa": -2000, "risco": 0},
                "tags": ["popular"],
                "conseq": [{"id": "fechou_torneira", "dias": 2, "efeitos": {"caixa": -4000}}],
                "tempo": 1
            },
        ]
    },
    {
        "id": "sindicalistas",
        "titulo": "🏭 Sindicalistas cobram compromisso com emprego e salário",
        "descricao": "Centrais sindicais querem um gesto público sobre salário mínimo, proteção do emprego e negociação coletiva.",
        "categoria": "trabalho",
        "fase_min": 1,
        "fase_max": 4,
        "duracao": 1,
        "tags": ["emprego", "social", "salario"],
        "classe": "oportunidade",
        "publicos": ["baixa_renda", "servidores"],
        "regioes": ["NE", "SE"],
        "opcoes": [
            {
                "texto": "Assumir compromisso gradual e fiscalmente viável",
                "efeitos": {"voto": 1.4, "narrativa": 4, "caixa": -5000, "mercado": -2},
                "tags": ["social", "emprego", "popular"],
                "conseq": [],
                "tempo": 1
            },
            {
                "texto": "Prometer tudo para inflamar a base",
                "efeitos": {"voto": 2.2, "narrativa": 3, "caixa": -10000, "risco": 3, "mercado": -5},
                "tags": ["social", "popular"],
                "conseq": [{"id": "conta_chega", "dias": 2, "efeitos": {"classe_media": -0.7, "empresariado": -1.2}}],
                "tempo": 1
            },
            {
                "texto": "Manter distância e focar em empreendedorismo",
                "efeitos": {"voto": -0.8, "narrativa": 0, "mercado": 2},
                "tags": ["mercado", "inovacao"],
                "conseq": [],
                "tempo": 1
            },
        ]
    },
    {
        "id": "audio_whatsapp",
        "titulo": "📣 Áudio de bastidor vaza em grupos de WhatsApp",
        "descricao": "Um áudio seu com tom duro sobre aliados saiu de contexto e está circulando pesado em grupos políticos.",
        "categoria": "redes",
        "fase_min": 2,
        "fase_max": 5,
        "duracao": 1,
        "tags": ["redes", "midia", "coalizao"],
        "classe": "crise",
        "publicos": ["mulheres", "classe_media", "servidores"],
        "regioes": ["SE", "NE"],
        "opcoes": [
            {
                "texto": "Divulgar o áudio completo e contextualizar",
                "efeitos": {"voto": 1.0, "narrativa": 4, "midia": 3, "risco": -1, "energia": -5},
                "tags": ["midia", "respeito"],
                "conseq": [],
                "tempo": 1
            },
            {
                "texto": "Processar e dobrar a aposta na guerra digital",
                "efeitos": {"voto": -0.5, "narrativa": -2, "midia": -3, "risco": 3, "energia": -4},
                "tags": ["redes"],
                "conseq": [{"id": "efeito_streisand", "dias": 2, "efeitos": {"midia": -1.0, "rejeicao": 0.5}}],
                "tempo": 1
            },
            {
                "texto": "Pedir desculpa pelo tom e pacificar",
                "efeitos": {"voto": 0.8, "narrativa": 3, "coalizao": 2, "energia": -3},
                "tags": ["respeito", "politica"],
                "conseq": [],
                "tempo": 1
            },
        ]
    },
    {
        "id": "voto_util",
        "titulo": "🗳️ Pressão pelo voto útil cresce na reta final",
        "descricao": "Faltando poucos dias, parte do eleitorado quer escolher entre quem realmente tem chance de chegar ao segundo turno.",
        "categoria": "reta_final",
        "fase_min": 5,
        "fase_max": 5,
        "duracao": 1,
        "tags": ["narrativa", "reta_final", "pesquisa"],
        "classe": "final",
        "publicos": ["classe_media", "jovens", "mulheres"],
        "regioes": ["SE", "NE", "SUL"],
        "opcoes": [
            {
                "texto": "Fazer campanha explícita pelo voto útil",
                "efeitos": {"voto": 2.0, "narrativa": 5, "energia": -5},
                "tags": ["narrativa", "popular"],
                "conseq": [],
                "tempo": 1
            },
            {
                "texto": "Manter discurso amplo sem tocar no tema",
                "efeitos": {"voto": 0.4, "narrativa": 1},
                "tags": ["gestao"],
                "conseq": [],
                "tempo": 1
            },
            {
                "texto": "Atacar o rival mais próximo para polarizar",
                "efeitos": {"voto": 0.8, "narrativa": 1, "rejeicao": 0.8, "midia": -2},
                "tags": ["midia", "corrupcao"],
                "conseq": [],
                "tempo": 1
            },
        ]
    },
    {
        "id": "debate_final",
        "titulo": "🎤 Último debate antes da votação",
        "descricao": "É a última grande chance de virar voto, consolidar sua narrativa e não cometer um erro fatal ao vivo.",
        "categoria": "reta_final",
        "fase_min": 5,
        "fase_max": 5,
        "duracao": 2,
        "tags": ["debate", "narrativa", "reta_final"],
        "classe": "final",
        "publicos": ["classe_media", "mulheres", "jovens", "baixa_renda"],
        "regioes": ["SE", "NE", "SUL"],
        "opcoes": [
            {
                "texto": "Ser propositivo, firme e didático",
                "efeitos": {"voto": 2.4, "narrativa": 7, "energia": -10, "risco": -1},
                "tags": ["gestao", "economia", "seguranca", "saude"],
                "conseq": [],
                "tempo": 2
            },
            {
                "texto": "Partir para o confronto total",
                "efeitos": {"voto": 1.2, "narrativa": 2, "rejeicao": 1.5, "midia": -2, "energia": -9},
                "tags": ["midia", "corrupcao"],
                "conseq": [],
                "tempo": 2
            },
            {
                "texto": "Jogar na defensiva para não errar",
                "efeitos": {"voto": -0.7, "narrativa": -2, "energia": -4, "risco": -1},
                "tags": ["gestao"],
                "conseq": [],
                "tempo": 2
            },
        ]
    },
    {
        "id": "apagao",
        "titulo": "⚡ Apagão nacional reacende debate sobre gestão",
        "descricao": "Uma sequência de falhas energéticas atinge cidades grandes e pequenas. A palavra do dia vira competência administrativa.",
        "categoria": "gestao",
        "fase_min": 2,
        "fase_max": 5,
        "duracao": 1,
        "tags": ["gestao", "economia", "midia"],
        "classe": "crise",
        "publicos": ["classe_media", "empresariado", "servidores"],
        "regioes": ["SE", "NE", "SUL"],
        "opcoes": [
            {
                "texto": "Apresentar plano técnico com investimento e meta",
                "efeitos": {"voto": 1.3, "narrativa": 4, "risco": -1},
                "tags": ["gestao", "economia", "infraestrutura"],
                "conseq": [],
                "tempo": 1
            },
            {
                "texto": "Usar o caso para atacar a incompetência geral",
                "efeitos": {"voto": 0.5, "narrativa": 1, "midia": -1},
                "tags": ["midia"],
                "conseq": [],
                "tempo": 1
            },
            {
                "texto": "Ficar genérico e dizer que o país precisa mudar",
                "efeitos": {"voto": -0.9, "narrativa": -2},
                "tags": ["narrativa"],
                "conseq": [],
                "tempo": 1
            },
        ]
    },
]

SECOND_TURN_RIVALS = [
    {"nome": "Governista", "base": 31, "rejeicao": 35, "forca": "máquina"},
    {"nome": "Outsider", "base": 26, "rejeicao": 44, "forca": "redes"},
    {"nome": "Moderado", "base": 21, "rejeicao": 26, "forca": "centro"},
]

# =============================================================================
# HELPERS
# =============================================================================
def clamp(value, min_v, max_v):
    return max(min_v, min(max_v, value))

def get_phase_number(day):
    for i, (_, start, end) in enumerate(PHASES, start=1):
        if start <= day <= end:
            return i
    return 5

def get_phase_name(day):
    for name, start, end in PHASES:
        if start <= day <= end:
            return name
    return PHASES[-1][0]

def weighted_choice(options, weight_fn):
    weights = [max(0.1, weight_fn(o)) for o in options]
    return random.choices(options, weights=weights, k=1)[0]

def progress_percent():
    s = st.session_state.game
    return int(((s["day"] - 1) / s["max_days"]) * 100)

def current_poll():
    return round(st.session_state.game["public"]["voto"], 1)

def fmt_money(v):
    return f"R$ {v:,.0f}".replace(",", ".")

# =============================================================================
# STATE INIT
# =============================================================================
def default_state():
    return {
        "seed": random.randint(1000, 999999),
        "day": 1,
        "max_days": 45,
        "difficulty": "Normal",
        "game_over": False,
        "result": None,
        "result_text": "",
        "active_event": None,
        "used_events": [],
        "history": [],
        "messages": [],
        "consequences": [],
        "last_resolution": None,
        "advisor_focus": "estrategista",
        "achievements": [],
        "second_turn": None,
        "adversaries": deepcopy(SECOND_TURN_RIVALS),
        "candidate": {
            "nome": "Seu Candidato",
            "ideologia": "Centro",
            "carisma": 58,
            "disciplina": 62,
            "credibilidade": 51,
        },
        "resources": {
            "caixa": 120000.0,
            "energia": 82.0,
            "equipe": 70.0,
            "estrutura_rua": 50.0,
            "estrutura_digital": 54.0,
            "tempo_tv": 18.0,
        },
        "public": {
            "voto": 19.5,
            "rejeicao": 22.0,
            "conhecimento": 34.0,
            "confianca": 47.0,
            "narrativa": 44.0,
            "midia": 46.0,
            "risco": 11.0,
            "mercado": 50.0,
            "coalizao": 58.0,
        },
        "blocos": {k: {"apoio": v["base"]} for k, v in BLOCOS.items()},
        "states": {
            uf: {
                "voto": ESTADOS[uf]["base"] + random.uniform(-1.5, 1.5),
                "rejeicao": 20 + random.uniform(-3, 3),
                "tendencia": 0.0,
            } for uf in ESTADOS
        },
        "polls": [],
        "progress": {
            "days": [1],
            "vote": [19.5],
            "reject": [22.0],
            "cash": [120000.0],
        }
    }

def init_game():
    st.session_state.game = default_state()

def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_game()
    st.rerun()

if "game" not in st.session_state:
    init_game()

# =============================================================================
# CORE ENGINE
# =============================================================================
def add_message(text, kind="good"):
    st.session_state.game["messages"].append({"text": text, "kind": kind})

def award(key):
    g = st.session_state.game
    if key not in g["achievements"]:
        g["achievements"].append(key)

def process_achievements():
    g = st.session_state.game
    p = g["public"]
    r = g["resources"]
    if len(g["history"]) >= 1:
        award("primeira")
    if p["voto"] >= 30:
        award("acima_30")
    if p["voto"] >= 40:
        award("acima_40")
    if p["voto"] >= 50:
        award("acima_50")
    if p["risco"] <= 10 and g["day"] >= 35:
        award("sem_crise")
    if r["caixa"] >= 200000:
        award("caixa_200")
    if g["progress"]["vote"][0] < 15 and p["voto"] > 35:
        award("virada")

def advisor_hint(event):
    focus = st.session_state.game["advisor_focus"]
    adv = ADVISORS[focus]
    reliable = random.random() <= adv["confiabilidade"]

    if focus == "juridico":
        if reliable:
            best = sorted(event["opcoes"], key=lambda o: o["efeitos"].get("risco", 0))[0]
            return f"**{adv['nome']} ({adv['cargo']})**: A opção mais segura juridicamente é **“{best['texto']}”**."
        return f"**{adv['nome']} ({adv['cargo']})**: Cuidado com promessas e ataques. O risco pode estar escondido."
    if focus == "financeiro":
        if reliable:
            best = sorted(event["opcoes"], key=lambda o: o["efeitos"].get("caixa", 0), reverse=True)[0]
            return f"**{adv['nome']} ({adv['cargo']})**: Pensando em caixa, a melhor saída agora é **“{best['texto']}”**."
        return f"**{adv['nome']} ({adv['cargo']})**: Não gaste demais nesta fase. A reta final cobra caro."
    if focus == "comunicacao":
        if reliable:
            best = sorted(event["opcoes"], key=lambda o: o["efeitos"].get("narrativa", 0), reverse=True)[0]
            return f"**{adv['nome']} ({adv['cargo']})**: A narrativa mais forte vem de **“{best['texto']}”**."
        return f"**{adv['nome']} ({adv['cargo']})**: O público quer firmeza, mas sem parecer artificial."
    if focus == "politico":
        if reliable:
            best = sorted(event["opcoes"], key=lambda o: o["efeitos"].get("coalizao", 0), reverse=True)[0]
            return f"**{adv['nome']} ({adv['cargo']})**: Para manter apoio político, eu iria de **“{best['texto']}”**."
        return f"**{adv['nome']} ({adv['cargo']})**: Base política adora gesto, mas não gosta de humilhação pública."
    if reliable:
        best = sorted(event["opcoes"], key=lambda o: o["efeitos"].get("voto", 0) + 0.6*o["efeitos"].get("narrativa",0), reverse=True)[0]
        return f"**{adv['nome']} ({adv['cargo']})**: Se você quer crescer, a melhor leitura é **“{best['texto']}”**."
    return f"**{adv['nome']} ({adv['cargo']})**: Crescimento agora depende de narrativa e timing, não só de barulho."

def pick_event():
    g = st.session_state.game
    phase = get_phase_number(g["day"])
    valid = []
    for ev in EVENTS:
        if ev["id"] in g["used_events"]:
            continue
        if ev["fase_min"] <= phase <= ev["fase_max"]:
            score = 1.0
            if g["public"]["risco"] > 25 and ev["categoria"] in ("corrupcao", "redes", "midia"):
                score += 1.5
            if g["public"]["voto"] < 22 and ev["categoria"] in ("regional", "trabalho", "redes"):
                score += 1.2
            if g["day"] >= 40 and ev["categoria"] in ("reta_final", "debate"):
                score += 2.4
            valid.append((ev, score))
    if not valid:
        candidates = [e for e in EVENTS if e["fase_min"] <= phase <= e["fase_max"]]
        if not candidates:
            candidates = EVENTS[:]
        ev = random.choice(candidates)
    else:
        ev = random.choices([x[0] for x in valid], weights=[x[1] for x in valid], k=1)[0]
    g["active_event"] = ev

def apply_consequences():
    g = st.session_state.game
    remain = []
    messages = []
    for cons in g["consequences"]:
        effects = cons.get("efeitos", {})
        apply_delta_bundle(effects, consequence_mode=True)
        cons["dias"] -= 1
        messages.append(f"Efeito contínuo: {cons['id'].replace('_', ' ').title()}")
        if cons["dias"] > 0:
            remain.append(cons)
    g["consequences"] = remain
    for m in messages[:2]:
        add_message(m, "good")

def apply_delta_bundle(bundle, consequence_mode=False):
    g = st.session_state.game
    p = g["public"]
    r = g["resources"]

    for key, val in bundle.items():
        if key in ("voto", "rejeicao", "conhecimento", "confianca", "narrativa", "midia", "risco", "mercado", "coalizao"):
            p[key] = p.get(key, 0) + val
        elif key in ("caixa", "energia", "equipe", "estrutura_rua", "estrutura_digital", "tempo_tv"):
            r[key] = r.get(key, 0) + val
        elif key in g["blocos"]:
            g["blocos"][key]["apoio"] += val
        elif key in g["states"]:
            g["states"][key]["voto"] += val

    # clamps
    p["voto"] = clamp(p["voto"], 0, 65)
    p["rejeicao"] = clamp(p["rejeicao"], 0, 80)
    p["conhecimento"] = clamp(p["conhecimento"], 0, 100)
    p["confianca"] = clamp(p["confianca"], 0, 100)
    p["narrativa"] = clamp(p["narrativa"], 0, 100)
    p["midia"] = clamp(p["midia"], 0, 100)
    p["risco"] = clamp(p["risco"], 0, 100)
    p["mercado"] = clamp(p["mercado"], 0, 100)
    p["coalizao"] = clamp(p["coalizao"], 0, 100)

    r["caixa"] = max(-50000, r["caixa"])
    r["energia"] = clamp(r["energia"], 0, 100)
    r["equipe"] = clamp(r["equipe"], 0, 100)
    r["estrutura_rua"] = clamp(r["estrutura_rua"], 0, 100)
    r["estrutura_digital"] = clamp(r["estrutura_digital"], 0, 100)
    r["tempo_tv"] = clamp(r["tempo_tv"], 0, 100)

def apply_block_impacts(tags):
    g = st.session_state.game
    p = g["public"]
    for bloco, data in BLOCOS.items():
        delta = 0.0
        overlap = len(set(tags).intersection(data["tags"]))
        if overlap:
            delta += overlap * 0.9
        delta += (p["narrativa"] - 50) * 0.01
        delta -= max(0, p["rejeicao"] - 30) * 0.03
        if bloco == "empresariado":
            delta += (p["mercado"] - 50) * 0.03
        if bloco == "jovens":
            delta += (g["resources"]["estrutura_digital"] - 50) * 0.02
        if bloco == "baixa_renda":
            delta += (100 - min(100, max(0, p["mercado"]))) * 0.002
        g["blocos"][bloco]["apoio"] = clamp(g["blocos"][bloco]["apoio"] + delta, 0, 100)

def influence_bloco_on_state(uf):
    profiles = ESTADOS[uf]["perfil"]
    score = 0.0
    for bloco, meta in BLOCOS.items():
        overlap = len(set(profiles).intersection(meta["tags"]))
        if overlap:
            score += overlap * (st.session_state.game["blocos"][bloco]["apoio"] - meta["base"]) * 0.06
    return score

def region_bonus_from_tags(uf, tags):
    bonus = 0.0
    if uf in ("BA", "PE", "CE") and any(t in tags for t in ["social", "programa_social", "preco", "popular"]):
        bonus += 0.8
    if uf in ("SP", "MG", "PR", "RS") and any(t in tags for t in ["economia", "mercado", "gestao", "impostos"]):
        bonus += 0.7
    if uf == "RJ" and "seguranca" in tags:
        bonus += 1.0
    if uf in ("RS", "PR") and "agro" in tags:
        bonus += 0.9
    return bonus

def recalc_states(tags=None):
    g = st.session_state.game
    p = g["public"]
    tags = tags or []
    for uf in g["states"]:
        base = ESTADOS[uf]["base"]
        bloco_inf = influence_bloco_on_state(uf)
        media_bonus = (p["midia"] - 50) * 0.03
        narrative_bonus = (p["narrativa"] - 50) * 0.025
        reject_penalty = (p["rejeicao"] - 20) * 0.06
        local_bonus = region_bonus_from_tags(uf, tags)
        trend = g["states"][uf]["tendencia"] * 0.5
        noise = random.uniform(-0.25, 0.25)
        new_vote = base + bloco_inf + media_bonus + narrative_bonus - reject_penalty + local_bonus + trend + noise
        g["states"][uf]["voto"] = clamp(new_vote, 5, 65)
        g["states"][uf]["rejeicao"] = clamp(p["rejeicao"] + random.uniform(-2.0, 2.0), 5, 80)
        g["states"][uf]["tendencia"] = clamp(g["states"][uf]["voto"] - base, -10, 10)

def recalc_national_vote():
    g = st.session_state.game
    weighted = sum(g["states"][uf]["voto"] * ESTADOS[uf]["peso"] for uf in ESTADOS)
    total_w = sum(ESTADOS[uf]["peso"] for uf in ESTADOS)
    regional_vote = weighted / total_w

    blocos_media = sum(g["blocos"][b]["apoio"] for b in g["blocos"]) / len(g["blocos"])
    p = g["public"]

    vote = (
        regional_vote * 0.58
        + blocos_media * 0.20
        + p["conhecimento"] * 0.08
        + p["narrativa"] * 0.10
        + p["midia"] * 0.04
        - p["rejeicao"] * 0.18
    )
    p["voto"] = clamp(vote, 0, 65)

def update_world_after_choice(option):
    g = st.session_state.game
    p = g["public"]
    r = g["resources"]

    # desgaste natural
    r["energia"] = clamp(r["energia"] - 1.2, 0, 100)
    r["caixa"] -= 1200
    p["conhecimento"] = clamp(p["conhecimento"] + 0.8, 0, 100)

    # penalidades/bonificações sistêmicas
    if r["energia"] < 25:
        p["narrativa"] = clamp(p["narrativa"] - 1.0, 0, 100)
    if r["caixa"] < 20000:
        p["narrativa"] = clamp(p["narrativa"] - 0.7, 0, 100)
        p["voto"] = clamp(p["voto"] - 0.3, 0, 65)
    if p["risco"] > 30:
        p["rejeicao"] = clamp(p["rejeicao"] + 0.4, 0, 80)
    if p["coalizao"] < 35:
        p["narrativa"] = clamp(p["narrativa"] - 0.5, 0, 100)
        r["tempo_tv"] = clamp(r["tempo_tv"] - 0.4, 0, 100)
    if p["mercado"] > 65:
        r["caixa"] += 1500

def publish_poll_if_needed():
    g = st.session_state.game
    if g["day"] % 5 != 0 or g["day"] == 0:
        return
    p = g["public"]
    poll = {
        "dia": g["day"],
        "voto": round(p["voto"] + random.uniform(-0.8, 0.8), 1),
        "rejeicao": round(p["rejeicao"] + random.uniform(-1.0, 1.0), 1),
        "lidera_estados": sum(1 for uf in g["states"] if g["states"][uf]["voto"] >= 30)
    }
    g["polls"].append(poll)
    add_message(f"Nova pesquisa publicada: {poll['voto']}% de intenção de voto e {poll['rejeicao']}% de rejeição.", "good")

def advance_days(days):
    g = st.session_state.game
    g["day"] += days
    if g["day"] > g["max_days"]:
        g["day"] = g["max_days"]

def resolve_choice(option):
    g = st.session_state.game
    event = g["active_event"]
    p_before = g["public"]["voto"]

    apply_delta_bundle(option["efeitos"])
    apply_block_impacts(option.get("tags", []))
    for c in option.get("conseq", []):
        g["consequences"].append(deepcopy(c))
    recalc_states(option.get("tags", []))
    recalc_national_vote()
    update_world_after_choice(option)
    advance_days(option.get("tempo", event.get("duracao", 1)))
    publish_poll_if_needed()
    process_achievements()

    delta = round(g["public"]["voto"] - p_before, 1)
    hist = {
        "dia": g["day"],
        "evento": event["titulo"],
        "escolha": option["texto"],
        "delta": delta,
        "voto": round(g["public"]["voto"], 1),
    }
    g["history"].append(hist)
    g["last_resolution"] = hist
    g["used_events"].append(event["id"])
    g["active_event"] = None

    if delta >= 0:
        add_message(f"Sua decisão em **{event['titulo']}** rendeu {delta:+.1f} ponto(s) nas intenções de voto.", "good")
    else:
        add_message(f"Sua decisão em **{event['titulo']}** custou {delta:+.1f} ponto(s) nas intenções de voto.", "bad")

    g["progress"]["days"].append(g["day"])
    g["progress"]["vote"].append(g["public"]["voto"])
    g["progress"]["reject"].append(g["public"]["rejeicao"])
    g["progress"]["cash"].append(g["resources"]["caixa"])

    check_game_over()

def check_game_over():
    g = st.session_state.game
    p = g["public"]
    r = g["resources"]

    if r["caixa"] <= -30000:
        g["game_over"] = True
        g["result"] = "defeat"
        g["result_text"] = "A campanha colapsou financeiramente. Você ficou sem capacidade operacional antes da reta final."
        return
    if p["rejeicao"] >= 70:
        g["game_over"] = True
        g["result"] = "defeat"
        g["result_text"] = "Sua rejeição explodiu. O teto eleitoral fechou antes da votação."
        return
    if p["risco"] >= 85:
        g["game_over"] = True
        g["result"] = "defeat"
        g["result_text"] = "O risco jurídico saiu de controle e destruiu a viabilidade da campanha."
        return

    if g["day"] >= g["max_days"]:
        finish_campaign()

def finish_campaign():
    g = st.session_state.game
    p = g["public"]
    vote = p["voto"]

    rivals = []
    for adv in g["adversaries"]:
        score = adv["base"] + random.uniform(-2.2, 2.2)
        # seu crescimento drena um pouco dos rivais
        score -= max(0, (vote - 20)) * 0.08
        score = clamp(score, 8, 45)
        rivals.append({"nome": adv["nome"], "voto": round(score, 1), "rejeicao": adv["rejeicao"], "forca": adv["forca"]})
    rivals_sorted = sorted(rivals, key=lambda x: x["voto"], reverse=True)

    ranking = [{"nome": g["candidate"]["nome"], "voto": round(vote, 1), "rejeicao": round(p["rejeicao"], 1)}] + rivals_sorted
    ranking = sorted(ranking, key=lambda x: x["voto"], reverse=True)
    g["second_turn"] = ranking

    if ranking[0]["nome"] == g["candidate"]["nome"] and vote >= 50:
        g["game_over"] = True
        g["result"] = "victory"
        g["result_text"] = f"Vitória no 1º turno com {vote:.1f}%! Você dominou narrativa, regiões e reta final."
        return

    top2 = ranking[:2]
    names_top2 = [x["nome"] for x in top2]
    if g["candidate"]["nome"] in names_top2:
        rival = top2[0] if top2[0]["nome"] != g["candidate"]["nome"] else top2[1]
        score_2t = (
            vote
            + (100 - p["rejeicao"]) * 0.18
            + p["narrativa"] * 0.08
            + p["coalizao"] * 0.07
            + max(0, g["resources"]["energia"] - 25) * 0.03
            - random.uniform(0, 6)
        )
        rival_score = (
            rival["voto"]
            + (100 - rival["rejeicao"]) * 0.16
            + random.uniform(0, 7)
        )
        g["game_over"] = True
        if score_2t >= rival_score:
            g["result"] = "second_turn"
            g["result_text"] = f"Você chegou ao 2º turno e venceu a virada final contra {rival['nome']}. Campanha no limite, mas vencedora."
        else:
            g["result"] = "defeat"
            g["result_text"] = f"Você chegou ao 2º turno, mas perdeu para {rival['nome']} na reta decisiva."
        return

    g["game_over"] = True
    g["result"] = "defeat"
    g["result_text"] = f"Você terminou fora do 2º turno com {vote:.1f}%. A campanha cresceu, mas não o suficiente."

def run_day_setup():
    g = st.session_state.game
    if g["game_over"]:
        return
    if g["active_event"] is None:
        apply_consequences()
        pick_event()

# =============================================================================
# UI
# =============================================================================
def render_header():
    g = st.session_state.game
    phase_name = get_phase_name(g["day"])
    st.markdown(f"""
    <div class="game-header">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:18px; flex-wrap:wrap;">
            <div>
                <h1 style="margin:0 0 8px 0;">🇧🇷 Candidato 2026 V2 — Campanha Total</h1>
                <div style="opacity:.92; font-size:15px;">Simulador político brasileiro com fases, rejeição, blocos eleitorais, estados decisivos, consequências persistentes e reta final.</div>
            </div>
            <div>
                <span class="phase-chip">{phase_name}</span>
                <div style="margin-top:10px; font-size:13px; opacity:.9;">Dia {g['day']} de {g['max_days']} · Progresso {progress_percent()}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metrics():
    g = st.session_state.game
    p = g["public"]
    r = g["resources"]
    cols = st.columns(6)
    items = [
        ("Voto", f"{p['voto']:.1f}%"),
        ("Rejeição", f"{p['rejeicao']:.1f}%"),
        ("Narrativa", f"{p['narrativa']:.0f}"),
        ("Caixa", fmt_money(r['caixa'])),
        ("Energia", f"{r['energia']:.0f}"),
        ("Coalizão", f"{p['coalizao']:.0f}"),
    ]
    for col, (title, value) in zip(cols, items):
        with col:
            st.markdown(f'<div class="metric-card"><h3>{title}</h3><h1>{value}</h1></div>', unsafe_allow_html=True)

def render_sidebar():
    g = st.session_state.game
    st.sidebar.markdown("## ⚙️ Painel da campanha")

    focus = st.sidebar.selectbox(
        "Assessor em destaque",
        list(ADVISORS.keys()),
        index=list(ADVISORS.keys()).index(g["advisor_focus"])
    )
    g["advisor_focus"] = focus
    adv = ADVISORS[focus]
    st.sidebar.markdown(f"**{adv['nome']}** — {adv['cargo']}")
    st.sidebar.caption(f"Confiabilidade: {int(adv['confiabilidade']*100)}%")

    st.sidebar.progress(min(100, max(0, progress_percent())) / 100.0)
    st.sidebar.caption(f"Fase atual: {get_phase_name(g['day'])}")

    if st.sidebar.button("🔄 Reiniciar campanha"):
        reset_game()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏆 Conquistas")
    if g["achievements"]:
        for key in g["achievements"][-6:]:
            ach = ACHIEVEMENTS[key]
            st.sidebar.markdown(f"{ach['icon']} **{ach['name']}**")
    else:
        st.sidebar.caption("Nenhuma conquista ainda.")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📌 Diagnóstico")
    p = g["public"]
    r = g["resources"]
    diagnosis = []
    if p["voto"] >= 30:
        diagnosis.append("Você entrou forte na disputa.")
    if p["rejeicao"] >= 35:
        diagnosis.append("Rejeição começando a travar expansão.")
    if r["caixa"] < 30000:
        diagnosis.append("Caixa apertado para a reta final.")
    if p["coalizao"] < 45:
        diagnosis.append("Base política oscilando.")
    if r["energia"] < 30:
        diagnosis.append("Equipe e candidato sentindo desgaste.")
    if not diagnosis:
        diagnosis = ["Campanha equilibrada neste momento."]
    for line in diagnosis:
        st.sidebar.caption(f"• {line}")

def render_event():
    g = st.session_state.game
    event = g["active_event"]
    if not event:
        st.info("Nenhum evento disponível no momento.")
        return

    cls = event.get("classe", "")
    st.markdown(
        f"""
        <div class="event-card {cls}">
            <h2 style="margin:0 0 8px 0;">{event['titulo']}</h2>
            <div style="font-size:15px; color:#334155; line-height:1.55;">{event['descricao']}</div>
            <div>
                <span class="tag" style="background:#2563eb;">{event['categoria'].upper()}</span>
                <span class="tag" style="background:#7c3aed;">DURAÇÃO {event['duracao']} DIA(S)</span>
                <span class="tag" style="background:#0f766e;">FASE {get_phase_name(g['day']).upper()}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f'<div class="advisor-note">{advisor_hint(event)}</div>', unsafe_allow_html=True)

    st.markdown("### Escolha sua resposta")
    cols = st.columns(len(event["opcoes"]))
    for idx, (col, opt) in enumerate(zip(cols, event["opcoes"]), start=1):
        with col:
            st.markdown(f"""
            <div class="option-box">
                <div style="font-weight:800; font-size:15px; margin-bottom:6px;">Opção {idx}</div>
                <div style="font-size:14px; line-height:1.45; min-height:92px;">{opt['texto']}</div>
                <div class="small-note">
                    Impacto-base: voto {opt['efeitos'].get('voto',0):+}, narrativa {opt['efeitos'].get('narrativa',0):+}, risco {opt['efeitos'].get('risco',0):+}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Escolher opção {idx}", key=f"opt_{event['id']}_{idx}"):
                resolve_choice(opt)
                st.rerun()

def render_charts():
    g = st.session_state.game

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=g["progress"]["days"],
        y=g["progress"]["vote"],
        mode="lines+markers",
        name="Voto"
    ))
    fig.add_trace(go.Scatter(
        x=g["progress"]["days"],
        y=g["progress"]["reject"],
        mode="lines+markers",
        name="Rejeição"
    ))
    fig.update_layout(
        title="Evolução da campanha",
        height=340,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h"),
    )
    st.plotly_chart(fig, use_container_width=True)

def render_states():
    g = st.session_state.game
    st.markdown("### 🗺️ Estados decisivos")
    sorted_states = sorted(g["states"].items(), key=lambda kv: ESTADOS[kv[0]]["peso"], reverse=True)
    for uf, data in sorted_states:
        val = data["voto"]
        st.markdown(
            f"""
            <div class="region-line">
                <div style="display:flex; justify-content:space-between; gap:10px; align-items:center;">
                    <div><strong>{uf}</strong> · peso eleitoral {ESTADOS[uf]['peso']}</div>
                    <div><strong>{val:.1f}%</strong></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.progress(min(100, max(0, val)) / 100.0)

def render_blocos():
    g = st.session_state.game
    st.markdown("### 👥 Blocos eleitorais")
    for bloco, meta in g["blocos"].items():
        label = bloco.replace("_", " ").title()
        st.markdown(f"**{label}** — {meta['apoio']:.1f}")
        st.progress(min(100, max(0, meta["apoio"])) / 100.0)

def render_messages():
    g = st.session_state.game
    if not g["messages"]:
        return
    st.markdown("### 🧠 Leituras da campanha")
    for msg in g["messages"][-4:]:
        cls = "good-box" if msg["kind"] == "good" else "bad-box"
        st.markdown(f'<div class="{cls}">{msg["text"]}</div>', unsafe_allow_html=True)

def render_history():
    g = st.session_state.game
    st.markdown("### 📝 Histórico recente")
    if not g["history"]:
        st.caption("Ainda sem decisões registradas.")
        return
    for item in reversed(g["history"][-6:]):
        sign = "📈" if item["delta"] >= 0 else "📉"
        st.markdown(
            f"""
            <div class="history-item">
                <strong>{sign} Dia {item['dia']}</strong><br>
                <span style="font-size:14px;">{item['evento']}</span><br>
                <span style="font-size:13px; color:#334155;">Escolha: {item['escolha']}</span><br>
                <span style="font-size:13px; color:#475569;">Resultado: {item['delta']:+.1f} ponto(s) · voto atual {item['voto']:.1f}%</span>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_final():
    g = st.session_state.game
    result = g["result"]
    cls = "victory" if result == "victory" else "second-turn" if result == "second_turn" else "defeat"
    title = "🏆 Vitória no 1º turno" if result == "victory" else "🥊 Vitória no 2º turno" if result == "second_turn" else "❌ Derrota"
    st.markdown(
        f"""
        <div class="final-box {cls}">
            <h1 style="margin:0 0 8px 0;">{title}</h1>
            <div style="font-size:16px; line-height:1.5;">{g['result_text']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if g["second_turn"]:
        st.markdown("### 📊 Resultado do 1º turno")
        for pos, item in enumerate(g["second_turn"], start=1):
            st.write(f"**{pos}º** {item['nome']} — {item['voto']:.1f}%")
    if st.button("Jogar novamente"):
        reset_game()

# =============================================================================
# MAIN
# =============================================================================
run_day_setup()
render_sidebar()
render_header()
render_metrics()

if st.session_state.game["game_over"]:
    render_final()
else:
    col1, col2 = st.columns([1.45, 1.0])
    with col1:
        render_messages()
        render_event()
        render_charts()
    with col2:
        render_states()
        st.markdown("---")
        render_blocos()
        st.markdown("---")
        render_history()
