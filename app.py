import streamlit as st
import random
import plotly.graph_objects as go
from datetime import datetime
import math

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
# CSS PROFISSIONAL
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        margin: 10px 0;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 12px;
        opacity: 0.7;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .metric-card h1 {
        margin: 15px 0 0 0;
        font-size: 36px;
        font-weight: 800;
    }
    .metric-card .trend {
        font-size: 14px;
        margin-top: 10px;
    }
    .trend.up { color: #00ff88; }
    .trend.down { color: #ff4757; }
    
    .event-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 35px;
        border-radius: 20px;
        border-left: 8px solid #667eea;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        margin: 25px 0;
    }
    .event-card.crisis {
        border-left-color: #ff4757;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe0e0 100%);
    }
    .event-card.opportunity {
        border-left-color: #00ff88;
        background: linear-gradient(135deg, #f0fff4 0%, #e0ffe8 100%);
    }
    
    .victory-screen {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 50px;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 15px 50px rgba(0,255,136,0.3);
    }
    .defeat-screen {
        background: linear-gradient(135deg, #cb2d3e 0%, #ef473a 100%);
        padding: 50px;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 15px 50px rgba(255,71,87,0.3);
    }
    
    .advisor-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 10px 0;
        border: 2px solid transparent;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .advisor-card:hover {
        border-color: #667eea;
        transform: translateY(-3px);
    }
    .advisor-card.selected {
        border-color: #00ff88;
        background: #f0fff4;
    }
    
    .coalition-meter {
        background: #e0e0e0;
        border-radius: 10px;
        padding: 3px;
        margin: 8px 0;
        height: 25px;
        position: relative;
    }
    .coalition-fill {
        height: 100%;
        border-radius: 8px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 11px;
    }
    
    .news-ticker {
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        overflow: hidden;
        white-space: nowrap;
    }
    
    .scandal-warning {
        background: linear-gradient(135deg, #ff4757 0%, #ff6b81 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255,71,87,0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255,71,87,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,71,87,0); }
    }
    
    .stButton>button {
        border-radius: 10px;
        font-weight: 700;
        padding: 15px 30px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        font-size: 14px;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .hidden-info {
        background: #f0f0f0;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 15px 0;
        font-style: italic;
        color: #555;
    }
    
    .state-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.1);
        margin: 8px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .state-card.winning {
        border: 2px solid #00ff88;
    }
    .state-card.losing {
        border: 2px solid #ff4757;
    }
    
    .turn-indicator {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 25px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SISTEMA DE ASSESSORES (CADA UM COM VIÉS DIFERENTE)
# ============================================================================
ASSESSORES = {
    "estrategista": {
        "nome": "Carlos Mendes",
        "cargo": "Estrategista Chefe",
        "icone": "🎯",
        "confiabilidade": 0.85,
        "especialidade": "popularidade",
        "descricao": "Focado em pesquisas e estratégia eleitoral"
    },
    "financeiro": {
        "nome": "Ana Rodrigues",
        "cargo": "Diretora Financeira",
        "icone": "💰",
        "confiabilidade": 0.90,
        "especialidade": "caixa",
        "descricao": "Especialista em orçamento e doações"
    },
    "comunicacao": {
        "nome": "Pedro Santos",
        "cargo": "Diretor de Comunicação",
        "icone": "📰",
        "confiabilidade": 0.75,
        "especialidade": "midia",
        "descricao": "Responsável pela relação com a imprensa"
    },
    "politico": {
        "nome": "Dra. Helena Costa",
        "cargo": "Articuladora Política",
        "icone": "🤝",
        "confiabilidade": 0.80,
        "especialidade": "coalizao",
        "descricao": "Negocia com partidos e aliados"
    },
    "juridico": {
        "nome": "Dr. Roberto Lima",
        "cargo": "Advogado Eleitoral",
        "icone": "⚖️",
        "confiabilidade": 0.95,
        "especialidade": "risco",
        "descricao": "Previne problemas jurídicos e escândalos"
    }
}

# ============================================================================
# PARTIDOS DA COALIZÃO
# ============================================================================
PARTIDOS_COALIZAO = {
    "base": {
        "nome": "Partido da Base",
        "sigla": "PDB",
        "cor": "#DC143C",
        "apoio_inicial": 80,
        "prioridades": ["popularidade", "caixa"]
    },
    "centrao": {
        "nome": "Centrão Unido",
        "sigla": "CPU",
        "cor": "#FFD700",
        "apoio_inicial": 60,
        "prioridades": ["caixa", "coalizao"]
    },
    "progressista": {
        "nome": "Frente Progressista",
        "sigla": "FPP",
        "cor": "#228B22",
        "apoio_inicial": 70,
        "prioridades": ["popularidade", "midia"]
    },
    "liberal": {
        "nome": "Aliança Liberal",
        "sigla": "ALB",
        "cor": "#0066CC",
        "apoio_inicial": 55,
        "prioridades": ["caixa", "midia"]
    }
}

# ============================================================================
# ESTADOS DECISIVOS
# ============================================================================
ESTADOS_DECISIVOS = {
    "SP": {"eleitores": 22.5, "peso": 5, "cor": "#667eea"},
    "MG": {"eleitores": 10.8, "peso": 3, "cor": "#228B22"},
    "RJ": {"eleitores": 8.9, "peso": 3, "cor": "#FFD700"},
    "BA": {"eleitores": 8.2, "peso": 3, "cor": "#FFA500"},
    "RS": {"eleitores": 5.8, "peso": 2, "cor": "#DC143C"},
    "PR": {"eleitores": 5.7, "peso": 2, "cor": "#228B22"},
    "PE": {"eleitores": 4.8, "peso": 2, "cor": "#FFA500"},
    "CE": {"eleitores": 4.6, "peso": 2, "cor": "#FFA500"},
    "DF": {"eleitores": 1.5, "peso": 1, "cor": "#667eea"},
    "GO": {"eleitores": 3.8, "peso": 1, "cor": "#FFD700"}
}

# ============================================================================
# EVENTOS COMPLEXOS (CENÁRIO BRASILEIRO REALISTA)
# ============================================================================
EVENTOS = {
    "geral": [
        {
            "id": "debate_tv",
            "titulo": "Debate Presidencial Transmitido Nacionalmente",
            "desc": """
            O maior debate eleitoral do ano está no ar. Todos os candidatos estão presentes 
            e 60 milhões de brasileiros estão assistindo. Sua performance pode definir 
            o rumo da campanha. A imprensa está analisando cada palavra.
            
            **Contexto:** Pesquisas recentes mostram que 40% dos eleitores indecisos 
            baseiam seu voto em debates televisionados. Um erro pode custar caro.
            """,
            "icon": "📺",
            "tipo": "debate",
            "impacto": "critico",
            "duracao": 2,
            "opcoes": [
                {
                    "texto": "Atacar adversários com dados e fatos concretos",
                    "descricao_oculta": "Alto risco, alta recompensa. Pode impressionar eleitores informados mas alienar moderados.",
                    "efeito_base": {"pop": 10, "caixa": 0, "energia": -20, "midia": 8, "risco": 15},
                    "condicoes": {"pop_minima": 30, "midia_minima": 40}
                },
                {
                    "texto": "Focar em propostas emocionais e conexão com o povo",
                    "descricao_oculta": "Bom para popularidade, mas pode parecer superficial para eleitores técnicos.",
                    "efeito_base": {"pop": 12, "caixa": -3000, "energia": -25, "midia": 5, "risco": 8},
                    "condicoes": {}
                },
                {
                    "texto": "Postura conciliadora e acima das brigas",
                    "descricao_oculta": "Seguro mas pouco impactante. Bom para manter, ruim para crescer.",
                    "efeito_base": {"pop": 4, "caixa": 0, "energia": -15, "midia": 12, "risco": 3},
                    "condicoes": {}
                },
                {
                    "texto": "Ignorar ataques e focar exclusivamente no futuro",
                    "descricao_oculta": "Pode parecer evasivo. Bom se estiver liderando, ruim se estiver atrás.",
                    "efeito_base": {"pop": 2, "caixa": 0, "energia": -18, "midia": 6, "risco": 10},
                    "condicoes": {"pop_minima": 40}
                }
            ]
        },
        {
            "id": "escandalo_corrupcao",
            "titulo": "🚨 ESCÂNDALO: Aliado Envolvido em Esquema de Corrupção",
            "desc": """
            Uma investigação da Polícia Federal vazou para a imprensa. Um importante 
            aliado da sua coalizão foi pego em um esquema de desvio de verbas públicas. 
            O valor envolvido é de R$ 50 milhões.
            
            **Contexto:** A imprensa está pedindo posicionamento imediato. Seu advogado 
            alerta que qualquer declaração pode ser usada juridicamente. Sua base exige 
            ação, mas romper a aliança pode custar votos no Congresso.
            
            ⚠️ **ALERTA:** Esta crise pode afetar múltiplas métricas simultaneamente.
            """,
            "icon": "🚨",
            "tipo": "crise",
            "impacto": "critico",
            "duracao": 3,
            "opcoes": [
                {
                    "texto": "Romper aliança imediatamente e condenar publicamente",
                    "descricao_oculta": "Ganha imagem de íntegro mas perde apoio político. Risco de retaliação.",
                    "efeito_base": {"pop": 8, "caixa": -8000, "energia": -25, "midia": -5, "risco": 20, "coalizao": -15},
                    "condicoes": {}
                },
                {
                    "texto": "Aguardar conclusão da investigação antes de se posicionar",
                    "descricao_oculta": "Seguro juridicamente, mas eleitores podem interpretar como omissão ou conivência.",
                    "efeito_base": {"pop": -12, "caixa": 0, "energia": -15, "midia": -15, "risco": 5, "coalizao": 5},
                    "condicoes": {}
                },
                {
                    "texto": "Defender aliado publicamente até prova definitiva",
                    "descricao_oculta": "Mantém coalizão unida mas associa sua imagem ao escândalo. Altíssimo risco.",
                    "efeito_base": {"pop": -20, "caixa": 0, "energia": -20, "midia": -25, "risco": 35, "coalizao": 10},
                    "condicoes": {"coalizao_minima": 60}
                },
                {
                    "texto": "Criar CPI para investigar e mostrar ação",
                    "descricao_oculta": "Mostra proatividade mas gasta capital político. Pode backfire se aliado for inocentado.",
                    "efeito_base": {"pop": 5, "caixa": -15000, "energia": -30, "midia": 8, "risco": 25, "coalizao": -10},
                    "condicoes": {"caixa_minima": 50000}
                }
            ]
        },
        {
            "id": "crise_economica",
            "titulo": "💸 CRISE ECONÔMICA INTERNACIONAL AFETA BRASIL",
            "desc": """
            Mercados internacionais estão em turbulência. O dólar disparou 15% em uma semana, 
            a bolsa caiu 8% e o FMI emitiu alerta sobre a economia brasileira. 
            A inflação está subindo e o desemprego preocupa.
            
            **Contexto:** Eleitores das classes C e D estão especialmente sensíveis 
            a questões econômicas. Empresários cobram definições sobre política fiscal.
            
            📊 **Dado:** 67% dos eleitores citam economia como principal preocupação.
            """,
            "icon": "💸",
            "tipo": "economia",
            "impacto": "critico",
            "duracao": 2,
            "opcoes": [
                {
                    "texto": "Prometer controle rigoroso de preços e combate à especulação",
                    "descricao_oculta": "Muito popular a curto prazo mas economistas alertam para efeitos negativos.",
                    "efeito_base": {"pop": 12, "caixa": -15000, "energia": -20, "midia": 5, "risco": 18},
                    "condicoes": {}
                },
                {
                    "texto": "Defender autonomia total do Banco Central e metas fiscais",
                    "descricao_oculta": "Mercado aprova mas pode ser impopular. Bom para eleitores de alta renda.",
                    "efeito_base": {"pop": -5, "caixa": 8000, "energia": -15, "midia": 12, "risco": 8},
                    "condicoes": {}
                },
                {
                    "texto": "Anunciar pacote emergencial de R$ 30 bilhões",
                    "descricao_oculta": "Alto impacto imediato mas drena recursos da campanha. Sustentável?",
                    "efeito_base": {"pop": 15, "caixa": -35000, "energia": -25, "midia": 10, "risco": 12},
                    "condicoes": {"caixa_minima": 80000}
                },
                {
                    "texto": "Culpar governo anterior e prometer mudanças estruturais",
                    "descricao_oculta": "Fácil politicamente mas pode parecer evasivo se não houver propostas concretas.",
                    "efeito_base": {"pop": 6, "caixa": 0, "energia": -12, "midia": -3, "risco": 10},
                    "condicoes": {}
                }
            ]
        },
        {
            "id": "crise_saude",
            "titulo": "🏥 CRISE DE SAÚDE PÚBLICA: HOSPITAIS LOTADOS",
            "desc": """
            Um novo surto de doença respiratória sobrecarregou o sistema de saúde. 
            Hospitais estão com UTIs lotadas e há fila de espera para vacinação. 
            Imagens de pacientes em corredores viralizaram nas redes sociais.
            
            **Contexto:** A oposição já está usando a crise na propaganda. 
            Familiares de vítimas estão organizando protestos.
            
            ⚠️ **Urgente:** Ação necessária nas próximas 48 horas.
            """,
            "icon": "🏥",
            "tipo": "saude",
            "impacto": "alto",
            "duracao": 2,
            "opcoes": [
                {
                    "texto": "Visitar hospitais pessoalmente e conversar com pacientes",
                    "descricao_oculta": "Humaniza a imagem mas há risco de contágio. Consome muita energia.",
                    "efeito_base": {"pop": 10, "caixa": -5000, "energia": -35, "midia": 8, "risco": 15},
                    "condicoes": {"energia_minima": 50}
                },
                {
                    "texto": "Anunciar verba emergencial de R$ 5 bilhões para saúde",
                    "descricao_oculta": "Ação concreta e mensurável. Caro mas eficaz.",
                    "efeito_base": {"pop": 8, "caixa": -25000, "energia": -15, "midia": 10, "risco": 5},
                    "condicoes": {"caixa_minima": 60000}
                },
                {
                    "texto": "Convocar coletiva com cientistas e apresentar plano técnico",
                    "descricao_oculta": "Mostra competência mas pode parecer frio em momento emocional.",
                    "efeito_base": {"pop": 5, "caixa": -3000, "energia": -20, "midia": 15, "risco": 3},
                    "condicoes": {}
                },
                {
                    "texto": "Culpar gestão anterior e prometer investigação",
                    "descricao_oculta": "Político mas pode parecer insensível com vítimas. Risco de backfire.",
                    "efeito_base": {"pop": -8, "caixa": 0, "energia": -10, "midia": -10, "risco": 20},
                    "condicoes": {}
                }
            ]
        },
        {
            "id": "amazonia_queimadas",
            "titulo": "🌳 QUEIMADAS NA AMAZÔNIA: PRESSÃO INTERNACIONAL",
            "desc": """
            Imagens de satélite da NASA mostram aumento de 45% nas queimadas. 
            Líderes europeus ameaçam bloquear acordo comercial. 
            Investidores estrangeiros estão reavaliando posições no Brasil.
            
            **Contexto:** Ruralistas apoiam desenvolvimento, ambientalistas exigem proteção. 
            Você precisa equilibrar interesses contraditórios.
            
            🌍 **Impacto:** Pode afetar doações internacionais e imagem no exterior.
            """,
            "icon": "🌳",
            "tipo": "ambiente",
            "impacto": "alto",
            "duracao": 1,
            "opcoes": [
                {
                    "texto": "Enviar tropas e IBAMA para fiscalização imediata",
                    "descricao_oculta": "Ação firme agrada ambientalistas mas irrita ruralistas da base.",
                    "efeito_base": {"pop": 8, "caixa": -20000, "energia": -25, "midia": 12, "risco": 15, "coalizao": -8},
                    "condicoes": {}
                },
                {
                    "texto": "Negociar com governadores da região plano conjunto",
                    "descricao_oculta": "Solução política mais lenta. Mantém aliados mas ação parece fraca.",
                    "efeito_base": {"pop": 3, "caixa": -8000, "energia": -20, "midia": 5, "risco": 8, "coalizao": 5},
                    "condicoes": {}
                },
                {
                    "texto": "Propor fundo internacional de US$ 2 bilhões",
                    "descricao_oculta": "Solução criativa que traz recursos mas depende de aprovação externa.",
                    "efeito_base": {"pop": 6, "caixa": 15000, "energia": -20, "midia": 15, "risco": 10},
                    "condicoes": {"midia_minima": 50}
                },
                {
                    "texto": "Priorizar desenvolvimento sustentável da região",
                    "descricao_oculta": "Discurso equilibrado mas vago. Pode não satisfazer nenhum lado.",
                    "efeito_base": {"pop": 2, "caixa": -5000, "energia": -15, "midia": 3, "risco": 12},
                    "condicoes": {}
                }
            ]
        },
        {
            "id": "pesquisa_vazada",
            "titulo": "📊 PESQUISA INTERNA VAZA PARA A IMPRENSA",
            "desc": """
            Uma pesquisa encomendada pela sua campanha vazou. Os números são 
            preocupantes: você está 8 pontos atrás do principal adversário em 
            estados decisivos. A equipe está desmoralizada.
            
            **Contexto:** A imprensa está especulando sobre possível troca de candidato. 
            Doadores estão hesitando. Sua equipe pede definição.
            
            ⚠️ **Risco:** Moral da equipe e confiança de doadores em jogo.
            """,
            "icon": "📊",
            "tipo": "crise",
            "impacto": "alto",
            "duracao": 2,
            "opcoes": [
                {
                    "texto": "Confirmar autenticidade e anunciar reestruturação da campanha",
                    "descricao_oculta": "Honestidade pode recuperar confiança mas admite fraqueza.",
                    "efeito_base": {"pop": 3, "caixa": -10000, "energia": -20, "midia": 8, "risco": 12},
                    "condicoes": {}
                },
                {
                    "texto": "Negar autenticidade e processar responsável pelo vazamento",
                    "descricao_oculta": "Contém dano imediato mas se descobrirem a verdade, crise piora.",
                    "efeito_base": {"pop": 0, "caixa": -8000, "energia": -15, "midia": -5, "risco": 25},
                    "condicoes": {}
                },
                {
                    "texto": "Ignorar e focar em eventos positivos para mudar narrativa",
                    "descricao_oculta": "Espera a poeira baixar. Funciona se houver bons resultados em seguida.",
                    "efeito_base": {"pop": -3, "caixa": 0, "energia": -10, "midia": -8, "risco": 15},
                    "condicoes": {}
                },
                {
                    "texto": "Divulgar pesquisa própria mostrando cenários favoráveis",
                    "descricao_oculta": "Contra-ataque informativo. Pode parecer manipulação se exagerado.",
                    "efeito_base": {"pop": 5, "caixa": -12000, "energia": -18, "midia": 5, "risco": 18},
                    "condicoes": {"caixa_minima": 40000}
                }
            ]
        },
        {
            "id": "alianca_partidaria",
            "titulo": "🤝 PROPOSTA DE ALIANÇA COM PARTIDO CHAVE",
            "desc": """
            Um partido com 65 deputados federais e 8 governadores está oferecendo 
            apoio formal. Em troca, exigem 5 ministérios e R$ 200 milhões em 
            emendas parlamentares.
            
            **Contexto:** Esta aliança pode ser decisiva para governabilidade. 
            Porém, o partido tem histórico de trocar de lado. Sua base questiona 
            se vale o preço.
            
            📈 **Análise:** Pode adicionar 8-12% de votos mas custa recursos.
            """,
            "icon": "🤝",
            "tipo": "politica",
            "impacto": "alto",
            "duracao": 1,
            "opcoes": [
                {
                    "texto": "Aceitar todas as exigências e fechar aliança",
                    "descricao_oculta": "Ganha apoio político imediato mas esvazia caixa e irrita base ideológica.",
                    "efeito_base": {"pop": -5, "caixa": 25000, "energia": -15, "midia": -8, "risco": 20, "coalizao": 15},
                    "condicoes": {}
                },
                {
                    "texto": "Negociar: 3 ministérios e R$ 100 milhões",
                    "descricao_oculta": "Meio-termo arriscado. Podem aceitar ou recusar e ficar inimigos.",
                    "efeito_base": {"pop": 2, "caixa": 12000, "energia": -20, "midia": 3, "risco": 15, "coalizao": 8},
                    "condicoes": {}
                },
                {
                    "texto": "Recusar mantendo coerência programática",
                    "descricao_oculta": "Mantém imagem limpa mas perde apoio crucial. Pode custar eleição.",
                    "efeito_base": {"pop": 8, "caixa": 0, "energia": 5, "midia": 12, "risco": 5, "coalizao": -10},
                    "condicoes": {}
                },
                {
                    "texto": "Pedir tempo para consultar a base do partido",
                    "descricao_oculta": "Adia decisão mas pode parecer indeciso. Eles podem fechar com adversário.",
                    "efeito_base": {"pop": 0, "caixa": 0, "energia": -8, "midia": -3, "risco": 18, "coalizao": -5},
                    "condicoes": {}
                }
            ]
        },
        {
            "id": "horario_eleitoral",
            "titulo": "🎬 HORÁRIO ELEITORAL GRATUITO - SUA VEZ",
            "desc": """
            Você tem 5 minutos no rádio e TV para alcançar 80 milhões de eleitores. 
            Esta é uma das últimas oportunidades antes da eleição. 
            Cada segundo conta.
            
            **Contexto:** Pesquisas mostram que 35% dos eleitores decidem o voto 
            baseado no horário eleitoral. Produção de qualidade custa caro.
            
            📺 **Audiência estimada:** 80 milhões de espectadores
            """,
            "icon": "🎬",
            "tipo": "midia",
            "impacto": "alto",
            "duracao": 1,
            "opcoes": [
                {
                    "texto": "Propostas detalhadas com dados e especialistas",
                    "descricao_oculta": "Atrai eleitores informados mas pode ser técnico demais para massas.",
                    "efeito_base": {"pop": 6, "caixa": -12000, "energia": -20, "midia": 10, "risco": 5},
                    "condicoes": {}
                },
                {
                    "texto": "Emoção e esperança com depoimentos reais",
                    "descricao_oculta": "Conexão emocional forte. Pode parecer populista para críticos.",
                    "efeito_base": {"pop": 10, "caixa": -12000, "energia": -18, "midia": 6, "risco": 8},
                    "condicoes": {}
                },
                {
                    "texto": "Ataques diretos aos adversários com comparações",
                    "descricao_oculta": "Mobiliza base mas pode afastar indecisos. Polariza eleição.",
                    "efeito_base": {"pop": 8, "caixa": -12000, "energia": -15, "midia": -5, "risco": 15},
                    "condicoes": {}
                },
                {
                    "texto": "Foco em realizações passadas e experiência",
                    "descricao_oculta": "Bom se tiver histórico positivo. Ruim se estiver sendo avaliado por promessas.",
                    "efeito_base": {"pop": 5, "caixa": -12000, "energia": -12, "midia": 5, "risco": 10},
                    "condicoes": {"pop_minima": 35}
                }
            ]
        },
        {
            "id": "greve_geral",
            "titulo": "👊 GREVE GERAL CONVOCADA POR CENTRAIS SINDICAIS",
            "desc": """
            As principais centrais sindicais convocaram greve geral para próxima semana. 
            Milhões de trabalhadores devem parar. Eles pedem seu posicionamento público.
            
            **Contexto:** Apoiar pode ganhar votos da classe trabalhadora mas 
            afasta empresários e classe média. Neutralidade irrita sindicatos.
            
            📊 **Eleitores impactados:** 25 milhões de trabalhadores formais
            """,
            "icon": "👊",
            "tipo": "trabalho",
            "impacto": "alto",
            "duracao": 2,
            "opcoes": [
                {
                    "texto": "Apoiar publicamente a greve e participar de ato",
                    "descricao_oculta": "Fortalece base trabalhista mas afasta empresários e moderados.",
                    "efeito_base": {"pop": 12, "caixa": -8000, "energia": -30, "midia": -8, "risco": 18},
                    "condicoes": {}
                },
                {
                    "texto": "Chamar ambos os lados para negociação imediata",
                    "descricao_oculta": "Posição de mediador. Pode agradar moderados mas irrita extremos.",
                    "efeito_base": {"pop": 4, "caixa": -3000, "energia": -25, "midia": 8, "risco": 10},
                    "condicoes": {}
                },
                {
                    "texto": "Manter neutralidade e focar em propostas de longo prazo",
                    "descricao_oculta": "Seguro mas pode parecer omisso em momento crucial.",
                    "efeito_base": {"pop": -6, "caixa": 0, "energia": -10, "midia": 0, "risco": 12},
                    "condicoes": {}
                },
                {
                    "texto": "Criticar greve e defender diálogo sem paralisação",
                    "descricao_oculta": "Agrada empresários mas sindicatos podem fazer campanha contra.",
                    "efeito_base": {"pop": -10, "caixa": 10000, "energia": -15, "midia": 5, "risco": 20},
                    "condicoes": {}
                }
            ]
        },
        {
            "id": "seguranca_publica",
            "titulo": "🔫 ONDA DE VIOLÊNCIA: POPULAÇÃO EXIGE AÇÕES",
            "desc": """
            Uma série de assaltos violentos e homicídios chocou o país. 
            Famílias de vítimas estão protestando. A oposição cobra 
            posicionamento sobre segurança pública.
            
            **Contexto:** Segurança é tema sensível. Medidas duras são populares 
            mas podem violar direitos humanos. Abordagem social é lenta.
            
            📈 **Pesquisa:** 72% citam segurança como prioridade máxima
            """,
            "icon": "🔫",
            "tipo": "seguranca",
            "impacto": "alto",
            "duracao": 2,
            "opcoes": [
                {
                    "texto": "Anunciar investimento massivo em policiamento",
                    "descricao_oculta": "Muito popular mas caro. Resultados levam tempo para aparecer.",
                    "efeito_base": {"pop": 10, "caixa": -30000, "energia": -20, "midia": 8, "risco": 8},
                    "condicoes": {"caixa_minima": 70000}
                },
                {
                    "texto": "Propor intervenção federal em estados críticos",
                    "descricao_oculta": "Medida extrema. Popular mas questionada constitucionalmente.",
                    "efeito_base": {"pop": 8, "caixa": -35000, "energia": -30, "midia": 12, "risco": 22},
                    "condicoes": {}
                },
                {
                    "texto": "Focar em prevenção social e inteligência policial",
                    "descricao_oculta": "Abordagem técnica e de longo prazo. Menos popular mas sustentável.",
                    "efeito_base": {"pop": 4, "caixa": -20000, "energia": -25, "midia": 10, "risco": 5},
                    "condicoes": {}
                },
                {
                    "texto": "Culpar governo anterior e prometer mudanças",
                    "descricao_oculta": "Fácil politicamente mas pode parecer evasivo sem ações concretas.",
                    "efeito_base": {"pop": 5, "caixa": 0, "energia": -12, "midia": -5, "risco": 15},
                    "condicoes": {}
                }
            ]
        },
        {
            "id": "fake_news",
            "titulo": "📱 FAKE NEWS VIRALIZA CONTRA VOCÊ",
            "desc": """
            Um vídeo manipulado com deepfake seu está circulando no WhatsApp. 
            5 milhões de pessoas já viram antes do desmentido. 
            O vídeo mostra você dizendo coisas que nunca disse.
            
            **Contexto:** Desmentir dá mais visibilidade à fake news. 
            Ignorar permite que se espalhe. Plataformas são lentas para agir.
            
            ⚠️ **Urgente:** Cada hora aumenta o dano exponencialmente.
            """,
            "icon": "📱",
            "tipo": "midia",
            "impacto": "alto",
            "duracao": 2,
            "opcoes": [
                {
                    "texto": "Processar criadores e exigir remoção imediata",
                    "descricao_oculta": "Ação jurídica mostra seriedade mas processo é lento.",
                    "efeito_base": {"pop": 3, "caixa": -15000, "energia": -20, "midia": 8, "risco": 10},
                    "condicoes": {"caixa_minima": 40000}
                },
                {
                    "texto": "Desmentir em rede nacional com provas",
                    "descricao_oculta": "Resposta rápida e transparente. Caro mas eficaz.",
                    "efeito_base": {"pop": 6, "caixa": -10000, "energia": -25, "midia": 12, "risco": 5},
                    "condicoes": {}
                },
                {
                    "texto": "Pedir ajuda às plataformas digitais oficialmente",
                    "descricao_oculta": "Solução técnica mas plataformas podem demorar para agir.",
                    "efeito_base": {"pop": 2, "caixa": -5000, "energia": -15, "midia": 6, "risco": 12},
                    "condicoes": {}
                },
                {
                    "texto": "Ignorar e não dar mais visibilidade ao assunto",
                    "descricao_oculta": "Estratégia de starve the troll. Funciona às vezes, falha outras.",
                    "efeito_base": {"pop": -12, "caixa": 0, "energia": -8, "midia": -15, "risco": 25},
                    "condicoes": {}
                }
            ]
        }
    ],
    "esquerda": [
        {
            "id": "nacionalizacao",
            "titulo": "🏛️ DESCOBERTA DE RESERVA ESTRATÉGICA",
            "desc": """
            Geólogos descobriram uma das maiores reservas de minerais raros do mundo 
            em território nacional. Empresas estrangeiras já estão fazendo ofertas. 
            O debate: estatal exclusiva ou parceria privado-estatal?
            
            **Contexto:** Este tema define sua identidade ideológica. 
            A decisão será lembrada por décadas.
            """,
            "icon": "🏛️",
            "tipo": "economia",
            "impacto": "critico",
            "duracao": 2,
            "opcoes": [
                {"texto": "Defender monopólio estatal total", "descricao_oculta": "Base progressista apoia mas mercado reage negativamente.", "efeito_base": {"pop": 15, "caixa": -15000, "energia": -25, "midia": 8, "risco": 18}, "condicoes": {}},
                {"texto": "Parceria com maioria estatal (51%)", "descricao_oculta": "Meio-termo. Atrai alguns investidores mas não satisfaz base purista.", "efeito_base": {"pop": 6, "caixa": 20000, "energia": -20, "midia": 5, "risco": 12}, "condicoes": {}},
                {"texto": "Leilão total para iniciativa privada", "descricao_oculta": "Mercado celebra mas base considera traição ideológica.", "efeito_base": {"pop": -20, "caixa": 40000, "energia": -15, "midia": -15, "risco": 30}, "condicoes": {}}
            ]
        }
    ],
    "centro": [
        {
            "id": "reforma_politica",
            "titulo": "⚖️ REFORMA DO SISTEMA ELEITORAL EM PAUTA",
            "desc": """
            Congresso está votando mudança no sistema eleitoral. 
            Sua posição pode definir o futuro da política brasileira. 
            Todos os lados cobram posicionamento.
            """,
            "icon": "⚖️",
            "tipo": "politica",
            "impacto": "alto",
            "duracao": 2,
            "opcoes": [
                {"texto": "Apoiar reforma completa e imediata", "descricao_oculta": "Imagem de reformador mas cria inimigos no establishment.", "efeito_base": {"pop": 8, "caixa": -8000, "energia": -25, "midia": 12, "risco": 20}, "condicoes": {}},
                {"texto": "Propor reforma gradual em 4 anos", "descricao_oculta": "Prudência elogiada mas pode parecer falta de coragem.", "efeito_base": {"pop": 4, "caixa": -3000, "energia": -18, "midia": 6, "risco": 10}, "condicoes": {}},
                {"texto": "Manter sistema atual com ajustes menores", "descricao_oculta": "Seguro para aliados mas perde imagem de mudança.", "efeito_base": {"pop": -5, "caixa": 5000, "energia": -10, "midia": -8, "risco": 8}, "condicoes": {}}
            ]
        }
    ],
    "direita": [
        {
            "id": "privatizacoes",
            "titulo": "💼 CARTERA DE PRIVATIZAÇÕES PRONTA",
            "desc": """
            Equipe econômica preparou lista de 15 estatais para privatização. 
            Estimativa: R$ 200 bilhões em arrecadação. 
            Sindicatos já anunciaram oposição.
            """,
            "icon": "💼",
            "tipo": "economia",
            "impacto": "critico",
            "duracao": 2,
            "opcoes": [
                {"texto": "Acelerar todas as privatizações imediatamente", "descricao_oculta": "Mercado elege você mas sindicatos fazem oposição ferrenha.", "efeito_base": {"pop": 10, "caixa": 50000, "energia": -30, "midia": 8, "risco": 25}, "condicoes": {}},
                {"texto": "Privatizar apenas as deficitárias", "descricao_oculta": "Seletivo. Menos impacto financeiro mas também menos oposição.", "efeito_base": {"pop": 5, "caixa": 20000, "energia": -20, "midia": 5, "risco": 15}, "condicoes": {}},
                {"texto": "Congelar privatizações até após eleição", "descricao_oculta": "Adia polêmica mas base econômica fica frustrada.", "efeito_base": {"pop": -8, "caixa": 0, "energia": -10, "midia": -10, "risco": 18}, "condicoes": {}}
            ]
        }
    ]
}

# ============================================================================
# INICIALIZAÇÃO DO JOGO
# ============================================================================

def init_game(dificuldade="normal"):
    """Inicializa todas as variáveis do jogo"""
    st.session_state.dia = 1
    st.session_state.total_dias = 45  # Aumentado para mais desafio
    st.session_state.popularidade = 22.0  # Começa mais baixo
    st.session_state.caixa = 120000.00  # Menos recursos
    st.session_state.energia = 80  # Começa com menos energia
    st.session_state.midia = 45
    st.session_state.risco_escandalo = 10  # Novo: meter de escândalo oculto
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
    st.session_state.eventos_escolhidos = []
    st.session_state.crise_ativa = None
    st.session_state.dias_crise = 0
    st.session_state.total_escandalos = 0
    
    # Ajustes por dificuldade (MAIS DIFÍCIL)
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
# LÓGICA AVANÇADA DO JOGO
# ============================================================================

def get_assessor_advice(evento, opcao_index):
    """Gera conselho do assessor com margem de erro"""
    assessor = ASSESSORES[st.session_state.assessor_selecionado]
    opcao = evento['opcoes'][opcao_index]
    
    # Conselhos baseados na especialidade do assessor
    if assessor['especialidade'] == 'popularidade':
        if opcao['efeito_base']['pop'] > 5:
            return f"✅ {assessor['nome']}: 'Esta opção pode aumentar significativamente sua popularidade.'"
        elif opcao['efeito_base']['pop'] < -5:
            return f"⚠️ {assessor['nome']}: 'Cuidado, isso pode prejudicar suas pesquisas.'"
        else:
            return f"➡️ {assessor['nome']}: 'Impacto neutro na popularidade.'"
    
    elif assessor['especialidade'] == 'caixa':
        if opcao['efeito_base']['caixa'] > 5000:
            return f"✅ {assessor['nome']}: 'Esta opção melhora nossa situação financeira.'"
        elif opcao['efeito_base']['caixa'] < -10000:
            return f"⚠️ {assessor['nome']}: 'Isso vai drenar nossos recursos rapidamente.'"
        else:
            return f"➡️ {assessor['nome']}: 'Impacto financeiro moderado.'"
    
    elif assessor['especialidade'] == 'risco':
        if opcao['efeito_base'].get('risco', 0) > 20:
            return f"🚨 {assessor['nome']}: 'ALTO RISCO JURÍDICO detectado nesta opção.'"
        elif opcao['efeito_base'].get('risco', 0) > 10:
            return f"⚠️ {assessor['nome']}: 'Risco moderado. Proceda com cautela.'"
        else:
            return f"✅ {assessor['nome']}: 'Risco jurídico aceitável.'"
    
    else:
        # Conselhos genéricos com confiabilidade
        if random.random() < assessor['confiabilidade']:
            if opcao['efeito_base']['pop'] > 0:
                return f"✅ {assessor['nome']}: 'Esta parece ser uma boa opção estrategicamente.'"
            else:
                return f"⚠️ {assessor['nome']}: 'Considere alternativas menos arriscadas.'"
        else:
            # Conselho errado (assessor não é 100% confiável)
            if opcao['efeito_base']['pop'] > 0:
                return f"⚠️ {assessor['nome']}: 'Não recomendo esta opção neste momento.'"
            else:
                return f"✅ {assessor['nome']}: 'Esta opção pode funcionar.'"

def check_condicoes_opcao(opcao):
    """Verifica se as condições para a opção são atendidas"""
    condicoes = opcao.get('condicoes', {})
    
    if 'pop_minima' in condicoes and st.session_state.popularidade < condicoes['pop_minima']:
        return False, f"Requer {condicoes['pop_minima']}% de popularidade (você tem {st.session_state.popularidade:.1f}%)"
    
    if 'caixa_minima' in condicoes and st.session_state.caixa < condicoes['caixa_minima']:
        return False, f"Requer R$ {condicoes['caixa_minima']:,} em caixa (você tem R$ {st.session_state.caixa:,.0f})"
    
    if 'energia_minima' in condicoes and st.session_state.energia < condicoes['energia_minima']:
        return False, f"Requer {condicoes['energia_minima']}% de energia (você tem {st.session_state.energia}%)"
    
    if 'midia_minima' in condicoes and st.session_state.midia < condicoes['midia_minima']:
        return False, f"Requer {condicoes['midia_minima']} de relação com mídia (você tem {st.session_state.midia:.0f})"
    
    if 'coalizao_minima' in condicoes:
        media_coalizao = sum(st.session_state.coalizao_apoio.values()) / len(st.session_state.coalizao_apoio)
        if media_coalizao < condicoes['coalizao_minima']:
            return False, f"Requer {condicoes['coalizao_minima']}% de apoio da coalizão"
    
    return True, ""

def aplicar_consequencias(opcao):
    """Aplica consequências com variabilidade e imprevisibilidade"""
    bonus = {"pop": 0, "caixa": 0, "energia": 0, "midia": 0}
    
    # Bônus do partido
    if st.session_state.partido_escolhido == "esquerda":
        bonus = {"pop": 1, "caixa": -500, "energia": 2, "midia": 1}
    elif st.session_state.partido_escolhido == "centro":
        bonus = {"pop": 0, "caixa": 1000, "energia": 1, "midia": 2}
    elif st.session_state.partido_escolhido == "direita":
        bonus = {"pop": -1, "caixa": 2000, "energia": 0, "midia": 0}
    
    # Multiplicador de dificuldade
    mult = 1.0
    if st.session_state.dificuldade == "facil":
        mult = 1.1
    elif st.session_state.dificuldade == "dificil":
        mult = 0.85
    elif st.session_state.dificuldade == "hardcore":
        mult = 0.7
    
    # Variabilidade aleatória (±20%) - AUMENTA IMPREVISIBILIDADE
    variabilidade = random.uniform(0.8, 1.2)
    
    # Aplicar efeitos
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
    
    # Atualizar coalizão
    if efeito_coalizao != 0:
        for partido in st.session_state.coalizao_apoio:
            st.session_state.coalizao_apoio[partido] += efeito_coalizao * random.uniform(0.8, 1.2)
            st.session_state.coalizao_apoio[partido] = max(0, min(100, st.session_state.coalizao_apoio[partido]))
    
    # Atualizar estados
    for estado in st.session_state.estados_support:
        variacao = random.uniform(-3, 4)
        if efeito_pop > 0:
            variacao += 1
        st.session_state.estados_support[estado] += variacao
        st.session_state.estados_support[estado] = max(0, min(100, st.session_state.estados_support[estado]))
    
    # Limites
    st.session_state.popularidade = max(0, min(100, st.session_state.popularidade))
    st.session_state.energia = max(0, min(100, st.session_state.energia))
    st.session_state.midia = max(0, min(100, st.session_state.midia))
    st.session_state.risco_escandalo = max(0, min(100, st.session_state.risco_escandalo))
    
    # Combo system
    if efeito_pop > 3:
        st.session_state.combo += 1
    else:
        st.session_state.combo = 0
    
    # Atualizar histórico
    st.session_state.evolucao_popularidade.append(st.session_state.popularidade)
    st.session_state.evolucao_dias.append(st.session_state.dia)
    
    st.session_state.pesquisas.append({
        'dia': st.session_state.dia,
        'pop': st.session_state.popularidade + random.uniform(-3, 3),  # Margem de erro
        'margem': 3
    })
    
    st.session_state.historico.append({
        'dia': st.session_state.dia,
        'evento': st.session_state.evento_atual['titulo'] if st.session_state.evento_atual else 'N/A',
        'pop': st.session_state.popularidade,
        'caixa': st.session_state.caixa,
        'energia': st.session_state.energia
    })
    
    # Verificar escândalo
    if st.session_state.risco_escandalo >= 80:
        st.session_state.total_escandalos += 1
        st.session_state.risco_escandalo = 30
        st.session_state.popularidade -= 15
        st.session_state.midia -= 20
        st.error("🚨 ESCÂNDALO EXPLODIU! Sua popularidade caiu drasticamente!")
    
    # Recuperar energia diária
    st.session_state.energia = min(100, st.session_state.energia + 3)
    
    # Bônus de caixa diário
    st.session_state.caixa += bonus['caixa']

def verificar_condicoes():
    """Verifica condições de vitória/derrota (MAIS RIGOROSO)"""
    # Derrotas imediatas
    if st.session_state.popularidade <= 3:
        st.session_state.game_over = True
        return "DERROTA: Popularidade abaixo de 3%. Partido retirou sua candidatura."
    
    if st.session_state.caixa <= 0:
        st.session_state.game_over = True
        return "DERROTA: Campanha falida. TSE cassou sua candidatura por irregularidades."
    
    if st.session_state.energia <= 0:
        st.session_state.game_over = True
        return "DERROTA: Colapso de saúde. Candidato hospitalizado às pressas."
    
    if st.session_state.midia <= 5:
        st.session_state.game_over = True
        return "DERROTA: Imprensa hostil destruiu completamente sua imagem pública."
    
    # Verificar coalizão
    media_coalizao = sum(st.session_state.coalizao_apoio.values()) / len(st.session_state.coalizao_apoio)
    if media_coalizao <= 20:
        st.session_state.game_over = True
        return "DERROTA: Coalizão desfeita. Sem apoio no Congresso, campanha inviável."
    
    # Fim dos dias
    if st.session_state.dia > st.session_state.total_dias:
        st.session_state.game_over = True
        
        # Calcular votos por estado
        votos_totais = 0
        eleitores_totais = sum(ESTADOS_DECISIVOS[e]['eleitores'] for e in ESTADOS_DECISIVOS.keys())
        
        for estado, apoio in st.session_state.estados_support.items():
            if apoio >= 45:  # Precisa de 45% no estado
                votos_totais += ESTADOS_DECISIVOS[estado]['eleitores']
        
        percentual_votos = (votos_totais / eleitores_totais) * 100
        
        if percentual_votos >= 50:
            st.session_state.vitoria = True
            return f"VITÓRIA NO 1º TURNO! Você conquistou {percentual_votos:.1f}% dos votos válidos!"
        elif percentual_votos >= 40:
            st.session_state.vitoria = True
            return f"CLASSIFICADO PARA 2º TURNO! Você teve {percentual_votos:.1f}% dos votos."
        else:
            st.session_state.vitoria = False
            return f"ELIMINADO! Você teve apenas {percentual_votos:.1f}% dos votos. Insuficiente para 2º turno."
    
    return None

def gerar_evento():
    """Gera evento com lógica avançada"""
    # Chance de crise baseada no risco
    if st.session_state.risco_escandalo >= 50 and random.random() < 0.3:
        crises = [e for e in EVENTOS['geral'] if e['tipo'] == 'crise']
        if crises:
            return random.choice(crises)
    
    # Eventos baseados no partido
    eventos_gerais = EVENTOS["geral"]
    eventos_ideologia = EVENTOS.get(st.session_state.partido_escolhido, [])
    
    if eventos_ideologia and random.random() < 0.25:
        pool_eventos = eventos_ideologia
    else:
        pool_eventos = eventos_gerais
    
    # Filtrar eventos já usados
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
    """Cria gráfico da evolução"""
    fig = go.Figure()
    
    partido_cor = PARTIDOS_COALIZAO['base']['cor'] if st.session_state.partido_escolhido == 'esquerda' else \
                  PARTIDOS_COALIZAO['centrao']['cor'] if st.session_state.partido_escolhido == 'centro' else \
                  PARTIDOS_COALIZAO['liberal']['cor']
    
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
    fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Zona de Eliminação")
    
    fig.update_layout(
        title='📈 Evolução da Popularidade',
        xaxis_title='Dia de Campanha',
        yaxis_title='Popularidade (%)',
        yaxis_range=[0, 100],
        height=350,
        template='plotly_white'
    )
    
    return fig

def criar_grafico_estados():
    """Cria mapa de apoio por estado"""
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
    
    fig.add_hline(y=45, line_dash="dash", line_color="green", annotation_text="Meta por Estado")
    
    fig.update_layout(
        title='🗺️ Apoio por Estado Decisivo',
        yaxis_range=[0, 100],
        height=350,
        template='plotly_white',
        showlegend=False
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
    
    fig.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="Apoio Mínimo")
    
    fig.update_layout(
        title='🤝 Apoio da Coalizão Partidária',
        yaxis_range=[0, 100],
        height=300,
        template='plotly_white',
        showlegend=False
    )
    
    return fig

# ============================================================================
# TELAS DO JOGO
# ============================================================================

def mostrar_tela_inicial():
    """Tela inicial completa"""
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px;">
        <h1 style="font-size: 56px; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🇧🇷 CANDIDATO 2026</h1>
        <p style="font-size: 22px; color: #666; margin: 15px 0;">Simulador Presidencial HARDCORE</p>
        <p style="font-size: 14px; color: #999;">A campanha eleitoral mais realista e desafiadora já criada</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎮 MECÂNICAS AVANÇADAS
        
        | Recurso | Descrição |
        |---------|-----------|
        | 🎯 **Consequências Ocultas** | Não veja números exatos antes de decidir |
        | 👥 **5 Assessores** | Cada um com especialidade e confiabilidade diferente |
        | 🤝 **Coalizão Partidária** | Mantenha 4 partidos aliados felizes |
        | 🗺️ **10 Estados Decisivos** | Precisa ganhar estados específicos |
        | 🚨 **Escândalos Ocultos** | Risk meter que pode explodir a qualquer momento |
        | 📊 **Pesquisas com Margem** | Dados não são 100% precisos |
        | ⚡ **Crises Aleatórias** | Eventos imprevisíveis baseados no seu risco |
        | 🏆 **Conquistas** | 15 achievements para desbloquear |
        
        ### ⚠️ AVISO DE DIFICULDADE
        
        Este jogo é **INTENCIONALMENTE DIFÍCIL**. A maioria dos jogadores 
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
            "Fácil - Aprendizado": "facil",
            "Normal - Experiência Real": "normal",
            "Difícil - Desafio": "dificil",
            "HARDCORE - Somente Expert": "hardcore"
        }
        st.session_state.dificuldade_temp = diff_map[dificuldade]
    
    with col2:
        st.markdown("### 🏆 Recorde Atual")
        hs = load_high_score()
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Maior Popularidade</h3>
            <h1>{hs['score']:.1f}%</h1>
            <p>{hs['partido']}</p>
            <p style="font-size: 12px;">{hs['dificuldade']} | {hs['data']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        total_ach = 15
        unlocked = len(st.session_state.get('conquistas_unlocked', []))
        st.write(f"### 🏅 Conquistas: {unlocked}/{total_ach}")
        st.progress(unlocked / total_ach)
    
    st.divider()
    
    st.markdown("### 🎭 Escolha Sua Ideologia")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);">
            <h2 style="font-size: 48px; margin: 0;">🔴</h2>
            <h3>ESQUERDA</h3>
            <p>Frente Progressista</p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p style="font-size: 13px;">+1% Popularidade por decisão</p>
            <p style="font-size: 13px;">+2 Energia/dia</p>
            <p style="font-size: 13px;">-R$ 500 Caixa/dia</p>
            <p style="font-size: 13px;">✅ Eventos sociais exclusivos</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔴 Jogar como Esquerda", key="btn_esq", use_container_width=True, type="primary"):
            st.session_state.partido_escolhido = "esquerda"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);">
            <h2 style="font-size: 48px; margin: 0;">🟡</h2>
            <h3>CENTRO</h3>
            <p>Aliança Democrática</p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p style="font-size: 13px;">±0% Popularidade (Neutro)</p>
            <p style="font-size: 13px;">+1 Energia/dia</p>
            <p style="font-size: 13px;">+R$ 1.000 Caixa/dia</p>
            <p style="font-size: 13px;">✅ Eventos de reforma exclusivos</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🟡 Jogar como Centro", key="btn_cen", use_container_width=True, type="primary"):
            st.session_state.partido_escolhido = "centro"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #0066CC 0%, #003366 100%);">
            <h2 style="font-size: 48px; margin: 0;">🔵</h2>
            <h3>DIREITA</h3>
            <p>Movimento Liberal</p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p style="font-size: 13px;">-1% Popularidade por decisão</p>
            <p style="font-size: 13px;">±0 Energia/dia</p>
            <p style="font-size: 13px;">+R$ 2.000 Caixa/dia</p>
            <p style="font-size: 13px;">✅ Eventos econômicos exclusivos</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔵 Jogar como Direita", key="btn_dir", use_container_width=True, type="primary"):
            st.session_state.partido_escolhido = "direita"
            init_game(st.session_state.dificuldade_temp)
            st.rerun()

def mostrar_jogo():
    """Tela principal do jogo"""
    partido_info = PARTIDOS_COALIZAO.get('base', {'cor': '#667eea'})
    
    # Header
    col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
    with col_h1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 25px; border-radius: 15px; color: white;">
            <h2 style="margin: 0;">🇧🇷 CAMPANHA PRESIDENCIAL 2026</h2>
            <p style="margin: 10px 0 0 0; opacity: 0.8;">Dia {st.session_state.dia}/{st.session_state.total_dias} | {st.session_state.dificuldade.upper()} | {st.session_state.partido_escolhido.upper()}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_h2:
        if st.button("📊 Gráficos", use_container_width=True):
            st.session_state.show_stats = not st.session_state.show_stats
    with col_h3:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.partido_escolhido = None
            st.rerun()
    
    # Alerta de escândalo
    if st.session_state.risco_escandalo >= 60:
        st.markdown(f"""
        <div class="scandal-warning">
            <h2 style="margin: 0;">🚨 ALERTA DE ESCÂNDALO IMINENTE</h2>
            <p style="margin: 10px 0 0 0;">Risco: {st.session_state.risco_escandalo:.0f}% - Tome cuidado com decisões arriscadas!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Combo
    if st.session_state.combo >= 3:
        st.markdown(f"""
        <div style="text-align: center;">
            <div class="turn-indicator">
                🔥 COMBO x{st.session_state.combo} - Bônus de Popularidade Ativo!
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats em cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Popularidade</h3>
            <h1>{st.session_state.popularidade:.1f}%</h1>
            <p class="trend {'up' if st.session_state.combo >= 3 else ''}">Meta: 40%+</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.popularidade / 100)
    
    with col2:
        cor_caixa = "#00ff88" if st.session_state.caixa > 80000 else "#ffa500" if st.session_state.caixa > 30000 else "#ff4757"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {cor_caixa} 0%, #333 100%);">
            <h3>💰 Caixa</h3>
            <h1>R$ {st.session_state.caixa:,.0f}</h1>
            <p>{'Saudável' if st.session_state.caixa > 80000 else 'Atenção' if st.session_state.caixa > 30000 else 'CRÍTICO'}</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(st.session_state.caixa / 200000, 1.0))
    
    with col3:
        cor_energia = "#00ff88" if st.session_state.energia > 60 else "#ffa500" if st.session_state.energia > 30 else "#ff4757"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {cor_energia} 0%, #333 100%);">
            <h3>⚡ Energia</h3>
            <h1>{st.session_state.energia}%</h1>
            <p>{'Bom' if st.session_state.energia > 60 else 'Cansado' if st.session_state.energia > 30 else 'EXAUSTO'}</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.energia / 100)
    
    with col4:
        cor_midia = "#00ff88" if st.session_state.midia > 60 else "#ffa500" if st.session_state.midia > 30 else "#ff4757"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {cor_midia} 0%, #333 100%);">
            <h3>📰 Mídia</h3>
            <h1>{st.session_state.midia:.0f}</h1>
            <p>{'Favorável' if st.session_state.midia > 60 else 'Neutra' if st.session_state.midia > 30 else 'HOSTIL'}</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.midia / 100)
    
    with col5:
        cor_risco = "#00ff88" if st.session_state.risco_escandalo < 30 else "#ffa500" if st.session_state.risco_escandalo < 60 else "#ff4757"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {cor_risco} 0%, #333 100%);">
            <h3>🚨 Risco</h3>
            <h1>{st.session_state.risco_escandalo:.0f}%</h1>
            <p>{'Seguro' if st.session_state.risco_escandalo < 30 else 'Atenção' if st.session_state.risco_escandalo < 60 else 'PERIGO'}</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.risco_escandalo / 100)
    
    st.divider()
    
    # Assessores
    st.markdown("### 👥 Selecione Seu Assessor para Conselho")
    cols_assessores = st.columns(5)
    for i, (key, assessor) in enumerate(ASSESSORES.items()):
        with cols_assessores[i]:
            selected = st.session_state.assessor_selecionado == key
            st.markdown(f"""
            <div class="advisor-card {'selected' if selected else ''}">
                <div style="font-size: 24px;">{assessor['icone']}</div>
                <strong>{assessor['nome']}</strong><br>
                <small>{assessor['cargo']}</small><br>
                <small>Confiabilidade: {assessor['confiabilidade']*100:.0f}%</small>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Selecionar", key=f"assessor_{key}", use_container_width=True):
                st.session_state.assessor_selecionado = key
                st.rerun()
    
    # Gráficos
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
            st.markdown("### 🗺️ Estados Decisivos")
            for estado, dados in ESTADOS_DECISIVOS.items():
                apoio = st.session_state.estados_support[estado]
                status = "✅" if apoio >= 45 else "❌"
                st.write(f"{status} **{estado}** ({dados['eleitores']}M): {apoio:.1f}%")
        
        st.divider()
    
    # Área do evento
    if st.session_state.game_over:
        if st.session_state.vitoria:
            st.balloons()
            st.markdown(f"""
            <div class="victory-screen">
                <h1 style="font-size: 56px; margin: 0;">🎉 VITÓRIA!</h1>
                <p style="font-size: 24px; margin: 25px 0;">Sua campanha entrou para a história!</p>
                <p style="font-size: 20px;">Popularidade final: <strong>{st.session_state.popularidade:.1f}%</strong></p>
                <p style="font-size: 18px;">Dias completados: <strong>{st.session_state.dia}</strong></p>
                <p style="font-size: 16px;">Escândalos sobrevividos: <strong>{st.session_state.total_escandalos}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            if save_high_score(st.session_state.popularidade, st.session_state.dia, st.session_state.partido_escolhido, st.session_state.dificuldade):
                st.success("🏆 NOVO RECORDE PESSOAL!")
        else:
            st.markdown(f"""
            <div class="defeat-screen">
                <h1 style="font-size: 56px; margin: 0;">😞 DERROTA</h1>
                <p style="font-size: 24px; margin: 25px 0;">A política é implacável...</p>
                <p style="font-size: 20px;">Popularidade final: <strong>{st.session_state.popularidade:.1f}%</strong></p>
                <p style="font-size: 18px;">Causa: <strong>{st.session_state.get('msg_fim', 'Desconhecida')}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Conquistas
        if st.session_state.conquistas_unlocked:
            st.markdown("### 🏅 Conquistas Desbloqueadas")
            cols = st.columns(3)
            for i, ach_id in enumerate(st.session_state.conquistas_unlocked):
                ach = ACHIEVEMENTS.get(ach_id, {'name': 'Unknown', 'desc': '', 'icon': '🏆'})
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="achievement-card">
                        <strong>{ach['icon']} {ach['name']}</strong><br>
                        <small>{ach['desc']}</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        if st.button("🎮 Jogar Novamente", use_container_width=True, type="primary"):
            st.session_state.partido_escolhido = None
            st.rerun()
            
    else:
        # Gerar evento
        if st.session_state.evento_atual is None:
            st.session_state.evento_atual = gerar_evento()
        
        evento = st.session_state.evento_atual
        
        # Card do evento
        classe_evento = "crisis" if evento['tipo'] == 'crise' else "opportunity" if evento['impacto'] == 'critico' else ""
        st.markdown(f"""
        <div class="event-card {classe_evento}">
            <div style="font-size: 56px; margin-bottom: 15px;">{evento['icon']}</div>
            <h2 style="margin: 0 0 15px 0; color: #333; font-size: 28px;">{evento['titulo']}</h2>
            <div style="font-size: 16px; color: #555; line-height: 1.8;">{evento['desc']}</div>
            <div style="margin-top: 20px;">
                <span style="background: #667eea; color: white; padding: 8px 15px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                    IMPACTO: {evento['impacto'].upper()}
                </span>
                <span style="background: #764ba2; color: white; padding: 8px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-left: 10px;">
                    DURAÇÃO: {evento['duracao']} DIAS
                </span>
                <span style="background: #ff4757; color: white; padding: 8px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-left: 10px;">
                    TIPO: {evento['tipo'].upper()}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Conselho do assessor
        assessor = ASSESSORES[st.session_state.assessor_selecionado]
        st.markdown(f"""
        <div class="hidden-info">
            <strong>{assessor['icone']} {assessor['nome']} diz:</strong><br>
            <em>"{assessor['descricao']}. Minha especialidade é {assessor['especialidade']}."</em>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🤔 Qual sua decisão? (Consequências OCULTAS)")
        
        st.info("""
        ⚠️ **IMPORTANTE:** Os números exatos das consequências estão ocultos. 
        Você deve confiar no conselho do seu assessor, analisar o contexto 
        e tomar decisões baseadas em estratégia, não em números. 
        Esta é a realidade da política!
        """)
        
        # Botões de opção
        for i, opcao in enumerate(evento['opcoes']):
            # Verificar condições
            pode_escolher, motivo = check_condicoes_opcao(opcao)
            
            # Conselho do assessor
            conselho = get_assessor_advice(evento, i)
            
            with st.container():
                col_btn, col_info = st.columns([3, 1])
                
                with col_btn:
                    if pode_escolher:
                        if st.button(f"Opção {i+1}: {opcao['texto']}", key=f"opt_{i}", use_container_width=True):
                            aplicar_consequencias(opcao)
                            st.session_state.evento_atual = None
                            st.session_state.dia += 1
                            
                            msg = verificar_condicoes()
                            if msg:
                                st.session_state.msg_fim = msg
                            
                            st.rerun()
                    else:
                        st.button(f"Opção {i+1}: {opcao['texto']} 🔒", key=f"opt_{i}", use_container_width=True, disabled=True)
                
                with col_info:
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; font-size: 13px;">
                        <strong>Condições:</strong><br>
                        {motivo if not pode_escolher else '✅ Disponíveis'}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background: #f0f0f0; padding: 15px; border-radius: 10px; margin: 10px 0 20px 0; border-left: 4px solid #667eea;">
                    <strong>📋 Descrição:</strong> {opcao['descricao_oculta']}<br><br>
                    <strong>💡 Conselho:</strong> {conselho}
                </div>
                """, unsafe_allow_html=True)
        
        # Feedback
        if st.session_state.mensagem_feedback:
            st.info(f"💬 {st.session_state.mensagem_feedback}")
        
        # Dicas
        with st.expander("💡 Dicas de Estratégia HARDCORE"):
            st.write("""
            ### 📖 Guia de Sobrevivência
            
            **GERENCIAMENTO DE RECURSOS:**
            - Nunca deixe energia abaixo de 30%
            - Mantenha caixa acima de R$ 50.000 para emergências
            - Mídia abaixo de 30% é zona de perigo extremo
            
            **COALIZÃO:**
            - Média de apoio deve ficar acima de 50%
            - Partidos com menos de 30% podem abandonar
            - Negocie antes que seja tarde
            
            **ESTADOS:**
            - Foque em estados com mais eleitores (SP, MG, RJ)
            - Precisa de 45% em cada estado para vencer
            - Não negligencie estados pequenos
            
            **RISCO DE ESCÂNDALO:**
            - Acima de 60% = perigo iminente
            - Escolha opções com baixo risco quando estiver alto
            - Escândalos causam -15% popularidade instantânea
            
            **ASSESSORES:**
            - Estrategista: Melhor para popularidade
            - Financeiro: Mais confiável para caixa
            - Jurídico: Essencial quando risco está alto
            - Nenhum assessor é 100% confiável!
            """)

# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar():
    """Sidebar completa"""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/ballot-box-with-ball.png", width=80)
        st.title("🎛️ Painel")
        
        if 'partido_escolhido' in st.session_state and st.session_state.partido_escolhido:
            st.write(f"**Partido:** {st.session_state.partido_escolhido.upper()}")
            st.write(f"**Dificuldade:** {st.session_state.dificuldade.upper()}")
            st.divider()
            
            st.write("### 📊 Status Atual")
            st.write(f"📈 Popularidade: {st.session_state.popularidade:.1f}%")
            st.write(f"💰 Caixa: R$ {st.session_state.caixa:,.0f}")
            st.write(f"⚡ Energia: {st.session_state.energia}%")
            st.write(f"📰 Mídia: {st.session_state.midia:.0f}")
            st.write(f"🚨 Risco: {st.session_state.risco_escandalo:.0f}%")
            st.divider()
            
            if st.session_state.combo >= 2:
                st.write(f"🔥 **Combo:** x{st.session_state.combo}")
            
            st.write("### 🤝 Coalizão")
            for partido, apoio in st.session_state.coalizao_apoio.items():
                cor = PARTIDOS_COALIZAO[partido]['cor']
                st.write(f"{PARTIDOS_COALIZAO[partido]['sigla']}: {apoio:.1f}%")
            
            st.divider()
            
            st.write("### 🏅 Conquistas")
            total = 15
            unlocked = len(st.session_state.conquistas_unlocked)
            st.write(f"{unlocked}/{total}")
            st.progress(unlocked / total)
        
        st.divider()
        st.warning("""
        **⚠️ LEMBRETE:**
        - Consequências são OCULTAS
        - Assessores podem ERRAR
        - Crises são ALEATÓRIAS
        - Coalizão pode DESFAZER
        - Risco pode EXPLODIR
        
        **Boa sorte, candidato!**
        """)

# ============================================================================
# SISTEMA DE CONQUISTAS
# ============================================================================

ACHIEVEMENTS = {
    "first_day": {"name": "Primeiro Dia", "desc": "Complete o dia 1", "icon": "🗳️"},
    "pop_30": {"name": "Emergindo", "desc": "Alcance 30% de popularidade", "icon": "📈"},
    "pop_50": {"name": "Favorito", "desc": "Alcance 50% de popularidade", "icon": "👑"},
    "pop_70": {"name": "Lenda", "desc": "Alcance 70% de popularidade", "icon": "🏆"},
    "rich": {"name": "Caixa Cheio", "desc": "Tenha R$ 500.000 em caixa", "icon": "💰"},
    "survivor": {"name": "Sobrevivente", "desc": "Sobreviva a 3 escândalos", "icon": "🛡️"},
    "coalition": {"name": "Negociador", "desc": "Mantenha coalizão acima de 70%", "icon": "🤝"},
    "states": {"name": "Estrategista", "desc": "Lidere em 8+ estados", "icon": "🗺️"},
    "combo_10": {"name": "Combo Master", "desc": "Alcance combo x10", "icon": "🔥"},
    "victory_1st": {"name": "Vitória 1º Turno", "desc": "Vença no primeiro turno", "icon": "🎉"},
    "hardcore": {"name": "HARDCORE", "desc": "Complete no modo HARDCORE", "icon": "💀"},
    "marathon": {"name": "Maratonista", "desc": "Complete todos os dias", "icon": "🏃"},
    "no_scandal": {"name": "Limpo", "desc": "Termine sem escândalos", "icon": "✨"},
    "comeback": {"name": "Comeback", "desc": "Volte de <15% para vitória", "icon": "🔄"},
    "advisor": {"name": "Confiável", "desc": "Use todos os assessores", "icon": "👥"}
}

def check_achievements():
    """Verifica conquistas"""
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
    
    media_coalizao = sum(st.session_state.coalizao_apoio.values()) / len(st.session_state.coalizao_apoio)
    if media_coalizao >= 70 and "coalition" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("coalition")
        new_achievements.append("coalition")
    
    estados_liderando = sum(1 for v in st.session_state.estados_support.values() if v >= 45)
    if estados_liderando >= 8 and "states" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("states")
        new_achievements.append("states")
    
    if st.session_state.combo >= 10 and "combo_10" not in st.session_state.conquistas_unlocked:
        st.session_state.conquistas_unlocked.append("combo_10")
        new_achievements.append("combo_10")
    
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
    
    render_sidebar()
    
    if 'partido_escolhido' not in st.session_state or st.session_state.partido_escolhido is None:
        mostrar_tela_inicial()
    else:
        # Check achievements
        new_achs = check_achievements()
        if new_achs:
            for ach_id in new_achs:
                ach = ACHIEVEMENTS.get(ach_id, {})
                st.success(f"🏆 CONQUISTA: {ach.get('icon', '🏆')} {ach.get('name', 'Unknown')}!")
        
        mostrar_jogo()

if __name__ == "__main__":
    main()
