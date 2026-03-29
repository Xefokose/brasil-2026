import streamlit as st
import random
import plotly.graph_objects as go

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================
st.set_page_config(page_title="🇧🇷 Candidato 2026", page_icon="🗳️", layout="wide")

# CSS
st.markdown("""
<style>
    .metric {background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 20px; border-radius: 12px; color: white; text-align: center;}
    .metric h3 {margin: 0; font-size: 13px; opacity: 0.8;}
    .metric h1 {margin: 12px 0 0 0; font-size: 30px;}
    .event {background: white; padding: 25px; border-radius: 15px; border-left: 6px solid #667eea; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);}
    .victory {background: linear-gradient(135deg, #11998e, #38ef7d); padding: 40px; border-radius: 20px; color: white; text-align: center;}
    .defeat {background: linear-gradient(135deg, #cb2d3e, #ef473a); padding: 40px; border-radius: 20px; color: white; text-align: center;}
    .stButton>button {border-radius: 8px; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# EVENTOS DO JOGO
# ============================================================================
EVENTOS = [
    {
        "titulo": "📺 Debate Presidencial na TV",
        "desc": "60 milhões de brasileiros assistindo. Sua performance pode definir a eleição.",
        "opcoes": [
            {"texto": "Atacar adversários com dados", "pop": 10, "caixa": 0, "energia": -20},
            {"texto": "Focar em propostas emocionais", "pop": 12, "caixa": -3000, "energia": -25},
            {"texto": "Postura conciliadora", "pop": 4, "caixa": 0, "energia": -15},
        ]
    },
    {
        "titulo": "🚨 Escândalo de Corrupção",
        "desc": "Aliado da coalizão pego em esquema. Imprensa cobra posição imediata.",
        "opcoes": [
            {"texto": "Romper aliança imediatamente", "pop": 8, "caixa": -8000, "energia": -25},
            {"texto": "Aguardar investigação", "pop": -12, "caixa": 0, "energia": -15},
            {"texto": "Defender aliado publicamente", "pop": -20, "caixa": 0, "energia": -20},
        ]
    },
    {
        "titulo": "💸 Crise Econômica Internacional",
        "desc": "Dólar dispara 15%, bolsa cai. Eleitores preocupados com emprego.",
        "opcoes": [
            {"texto": "Prometer controle de preços", "pop": 12, "caixa": -15000, "energia": -20},
            {"texto": "Defender Banco Central", "pop": -5, "caixa": 8000, "energia": -15},
            {"texto": "Pacote emergencial", "pop": 15, "caixa": -35000, "energia": -25},
        ]
    },
    {
        "titulo": "🏥 Crise de Saúde Pública",
        "desc": "Hospitais lotados. População cobra ação urgente.",
        "opcoes": [
            {"texto": "Visitar hospitais", "pop": 10, "caixa": -5000, "energia": -35},
            {"texto": "Verba emergencial", "pop": 8, "caixa": -25000, "energia": -15},
            {"texto": "Coletiva com cientistas", "pop": 5, "caixa": -3000, "energia": -20},
        ]
    },
    {
        "titulo": "🤝 Proposta de Aliança Partidária",
        "desc": "Partido com 65 deputados oferece apoio em troca de cargos.",
        "opcoes": [
            {"texto": "Aceitar todas exigências", "pop": -5, "caixa": 25000, "energia": -15},
            {"texto": "Negociar termos", "pop": 2, "caixa": 12000, "energia": -20},
            {"texto": "Recusar mantendo coerência", "pop": 8, "caixa": 0, "energia": 5},
        ]
    },
    {
        "titulo": "🎬 Horário Eleitoral Gratuito",
        "desc": "5 minutos no rádio e TV para alcançar 80 milhões de eleitores.",
        "opcoes": [
            {"texto": "Propostas detalhadas", "pop": 6, "caixa": -12000, "energia": -20},
            {"texto": "Emoção e esperança", "pop": 10, "caixa": -12000, "energia": -18},
            {"texto": "Ataques aos adversários", "pop": 8, "caixa": -12000, "energia": -15},
        ]
    },
    {
        "titulo": "🔫 Segurança Pública",
        "desc": "Onda de violência choca país. População exige ações.",
        "opcoes": [
            {"texto": "Mais policiamento", "pop": 10, "caixa": -30000, "energia": -20},
            {"texto": "Intervenção federal", "pop": 8, "caixa": -35000, "energia": -30},
            {"texto": "Prevenção social", "pop": 4, "caixa": -20000, "energia": -25},
        ]
    },
    {
        "titulo": "📱 Fake News Viraliza",
        "desc": "Vídeo manipulado circula no WhatsApp. 5 milhões já viram.",
        "opcoes": [
            {"texto": "Processar criadores", "pop": 3, "caixa": -15000, "energia": -20},
            {"texto": "Desmentir em rede nacional", "pop": 6, "caixa": -10000, "energia": -25},
            {"texto": "Ignorar assunto", "pop": -12, "caixa": 0, "energia": -8},
        ]
    },
]

# ============================================================================
# INICIALIZAÇÃO DO JOGO (TODAS VARIÁVEIS AQUI!)
# ============================================================================
def init_game():
    """Inicializa TODAS as variáveis do jogo em um só lugar"""
    # Stats principais
    st.session_state.dia = 1
    st.session_state.total_dias = 30
    st.session_state.popularidade = 25.0
    st.session_state.caixa = 150000.00
    st.session_state.energia = 80
    
    # Estado do jogo
    st.session_state.game_over = False
    st.session_state.vitoria = False
    st.session_state.msg_fim = ""
    
    # Dados do jogo
    st.session_state.evento_atual = None
    st.session_state.historico = []
    st.session_state.evolucao_pop = [25.0]
    st.session_state.evolucao_dias = [1]
    
    # Configurações
    st.session_state.partido = st.session_state.get('partido', 'centro')
    st.session_state.dificuldade = st.session_state.get('dificuldade', 'Normal')
    
    # UI
    st.session_state.mostrar_grafico = False
    
    # Ajustes por dificuldade
    if st.session_state.dificuldade == "Fácil":
        st.session_state.caixa = 200000.00
        st.session_state.popularidade = 30.0
        st.session_state.energia = 90
    elif st.session_state.dificuldade == "Difícil":
        st.session_state.caixa = 100000.00
        st.session_state.popularidade = 20.0
        st.session_state.energia = 70

# ============================================================================
# LÓGICA DO JOGO
# ============================================================================
def verificar_fim():
    """Verifica condições de vitória ou derrota"""
    # Derrotas
    if st.session_state.popularidade <= 5:
        st.session_state.game_over = True
        st.session_state.vitoria = False
        st.session_state.msg_fim = "Popularidade abaixo de 5%. Candidatura encerrada."
        return True
    
    if st.session_state.caixa <= 0:
        st.session_state.game_over = True
        st.session_state.vitoria = False
        st.session_state.msg_fim = "Caixa zerado. TSE cassou a candidatura."
        return True
    
    if st.session_state.energia <= 0:
        st.session_state.game_over = True
        st.session_state.vitoria = False
        st.session_state.msg_fim = "Energia zerada. Candidato hospitalizado."
        return True
    
    # Fim dos dias
    if st.session_state.dia > st.session_state.total_dias:
        st.session_state.game_over = True
        if st.session_state.popularidade >= 45:
            st.session_state.vitoria = True
            st.session_state.msg_fim = f"🎉 VITÓRIA NO 1º TURNO! {st.session_state.popularidade:.1f}% dos votos!"
        elif st.session_state.popularidade >= 35:
            st.session_state.vitoria = True
            st.session_state.msg_fim = f"✅ CLASSIFICADO PARA 2º TURNO! {st.session_state.popularidade:.1f}% dos votos."
        else:
            st.session_state.vitoria = False
            st.session_state.msg_fim = f"❌ ELIMINADO! Apenas {st.session_state.popularidade:.1f}% dos votos."
        return True
    
    return False

def gerar_evento():
    """Seleciona um evento aleatório"""
    return random.choice(EVENTOS)

def aplicar_consequencias(opcao):
    """Aplica os efeitos da escolha do jogador"""
    # Multiplicador por partido
    mult_pop = 1.0
    if st.session_state.partido == "esquerda":
        mult_pop = 1.15  # Bônus de popularidade
    elif st.session_state.partido == "direita":
        mult_pop = 0.90  # Penalidade de popularidade
    
    # Aplicar efeitos
    st.session_state.popularidade += opcao["pop"] * mult_pop
    st.session_state.caixa += opcao["caixa"]
    st.session_state.energia += opcao["energia"]
    
    # Limites
    st.session_state.popularidade = max(0, min(100, st.session_state.popularidade))
    st.session_state.energia = max(0, min(100, st.session_state.energia))
    
    # Registrar evolução
    st.session_state.evolucao_pop.append(st.session_state.popularidade)
    st.session_state.evolucao_dias.append(st.session_state.dia)
    st.session_state.historico.append(f"Dia {st.session_state.dia}: {opcao['texto']}")
    
    # Recuperação diária
    st.session_state.energia = min(100, st.session_state.energia + 5)
    
    # Bônus diário por partido
    if st.session_state.partido == "esquerda":
        st.session_state.caixa -= 500
    elif st.session_state.partido == "centro":
        st.session_state.caixa += 1000
    elif st.session_state.partido == "direita":
        st.session_state.caixa += 2000

# ============================================================================
# GRÁFICOS
# ============================================================================
def criar_grafico():
    """Cria gráfico de evolução da popularidade"""
    cor = "#DC143C" if st.session_state.partido == "esquerda" else "#FFD700" if st.session_state.partido == "centro" else "#0066CC"
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=st.session_state.evolucao_dias,
        y=st.session_state.evolucao_pop,
        mode='lines+markers',
        line=dict(color=cor, width=3),
        marker=dict(size=8)
    ))
    fig.add_hline(y=45, line_dash="dash", line_color="#00ff88", annotation_text="Vitória 1º Turno")
    fig.add_hline(y=35, line_dash="dash", line_color="#ffa500", annotation_text="2º Turno")
    
    fig.update_layout(
        title='📈 Evolução da Popularidade',
        xaxis_title='Dia de Campanha',
        yaxis_title='Popularidade (%)',
        yaxis_range=[0, 100],
        height=300,
        template='plotly_white',
        margin=dict(l=40, r=20, t=40, b=40)
    )
    return fig

# ============================================================================
# TELAS
# ============================================================================
def tela_inicial():
    """Tela de seleção de partido e dificuldade"""
    st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>🇧🇷 CANDIDATO 2026</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #666; margin-bottom: 30px;'>Simulador de Campanha Presidencial</p>", unsafe_allow_html=True)
    
    col_info, col_rec = st.columns([2, 1])
    
    with col_info:
        st.markdown("""
        ### 🎮 Como Jogar
        1. **Escolha sua ideologia** - Cada uma tem bônus diferentes
        2. **Tome decisões** - 30 dias de campanha com eventos reais
        3. **Gerencie recursos** - Popularidade, Caixa e Energia
        4. **Vença a eleição** - Chegue ao dia 30 com 35%+ para 2º turno
        
        ### ⚠️ Condições de Derrota
        - 📉 Popularidade ≤ 5% = Candidatura encerrada
        - 💰 Caixa ≤ R$ 0 = Cassação pelo TSE
        - ⚡ Energia ≤ 0% = Hospitalização
        """)
        
        st.session_state.dificuldade = st.selectbox("🎯 Nível de Dificuldade:", ["Fácil", "Normal", "Difícil"], key="sel_diff")
    
    with col_rec:
        st.markdown("### 🏆 Seu Recorde")
        if 'recorde_pop' not in st.session_state:
            st.session_state.recorde_pop = 0.0
        st.metric("Maior Popularidade", f"{st.session_state.recorde_pop:.1f}%")
    
    st.divider()
    
    st.markdown("### 🎭 Escolha Sua Ideologia")
    
    col_esq, col_cen, col_dir = st.columns(3)
    
    with col_esq:
        st.markdown("""
        <div class="metric" style="background: linear-gradient(135deg, #DC143C, #8B0000);">
            <h3>🔴 ESQUERDA</h3>
            <h1>+15% Pop</h1>
            <p style="color: #ff6b6b;">-R$ 500/dia</p>
            <p style="font-size: 12px; margin-top: 10px;">Foco em direitos sociais</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔴 Jogar como Esquerda", key="btn_esq", use_container_width=True, type="primary"):
            st.session_state.partido = "esquerda"
            init_game()
            st.rerun()
    
    with col_cen:
        st.markdown("""
        <div class="metric" style="background: linear-gradient(135deg, #FFD700, #FFA500);">
            <h3>🟡 CENTRO</h3>
            <h1>Equilibrado</h1>
            <p style="color: #90ee90;">+R$ 1.000/dia</p>
            <p style="font-size: 12px; margin-top: 10px;">Diálogo e reformas</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🟡 Jogar como Centro", key="btn_cen", use_container_width=True, type="primary"):
            st.session_state.partido = "centro"
            init_game()
            st.rerun()
    
    with col_dir:
        st.markdown("""
        <div class="metric" style="background: linear-gradient(135deg, #0066CC, #003366);">
            <h3>🔵 DIREITA</h3>
            <h1>-10% Pop</h1>
            <p style="color: #90ee90;">+R$ 2.000/dia</p>
            <p style="font-size: 12px; margin-top: 10px;">Liberdade econômica</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔵 Jogar como Direita", key="btn_dir", use_container_width=True, type="primary"):
            st.session_state.partido = "direita"
            init_game()
            st.rerun()

def tela_jogo():
    """Tela principal do jogo"""
    # Header
    col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
    with col_h1:
        nome_partido = "🔴 Esquerda" if st.session_state.partido == "esquerda" else "🟡 Centro" if st.session_state.partido == "centro" else "🔵 Direita"
        st.markdown(f"""
        <div class="metric">
            <h2>🇧🇷 CAMPANHA PRESIDENCIAL</h2>
            <p style="margin: 8px 0 0 0;">{nome_partido} | Dia {st.session_state.dia}/{st.session_state.total_dias} | {st.session_state.dificuldade}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_h2:
        if st.button("📊 Gráfico", use_container_width=True):
            st.session_state.mostrar_grafico = not st.session_state.mostrar_grafico
    with col_h3:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.partido = None
            st.rerun()
    
    # Stats em cards
    col_pop, col_caixa, col_energia = st.columns(3)
    
    with col_pop:
        cor_pop = "#00ff88" if st.session_state.popularidade >= 35 else "#ffa500" if st.session_state.popularidade >= 20 else "#ff4757"
        st.markdown(f"""
        <div class="metric" style="background: linear-gradient(135deg, {cor_pop}, #333);">
            <h3>📊 Popularidade</h3>
            <h1>{st.session_state.popularidade:.1f}%</h1>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.popularidade / 100)
    
    with col_caixa:
        cor_caixa = "#00ff88" if st.session_state.caixa >= 50000 else "#ffa500" if st.session_state.caixa >= 20000 else "#ff4757"
        st.markdown(f"""
        <div class="metric" style="background: linear-gradient(135deg, {cor_caixa}, #333);">
            <h3>💰 Caixa</h3>
            <h1>R$ {st.session_state.caixa:,.0f}</h1>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(st.session_state.caixa / 200000, 1.0))
    
    with col_energia:
        cor_energia = "#00ff88" if st.session_state.energia >= 50 else "#ffa500" if st.session_state.energia >= 25 else "#ff4757"
        st.markdown(f"""
        <div class="metric" style="background: linear-gradient(135deg, {cor_energia}, #333);">
            <h3>⚡ Energia</h3>
            <h1>{st.session_state.energia}%</h1>
        </div>
        """, unsafe_allow_html=True)
        st.progress(st.session_state.energia / 100)
    
    st.divider()
    
    # Gráfico (opcional)
    if st.session_state.mostrar_grafico:
        st.plotly_chart(criar_grafico(), use_container_width=True)
        st.divider()
    
    # Tela de fim de jogo
    if st.session_state.game_over:
        if st.session_state.vitoria:
            st.balloons()
            st.markdown(f"""
            <div class="victory">
                <h1 style="margin: 0; font-size: 48px;">🎉 VITÓRIA!</h1>
                <p style="font-size: 22px; margin: 20px 0;">{st.session_state.msg_fim}</p>
                <p style="font-size: 18px;">Popularidade final: <strong>{st.session_state.popularidade:.1f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Atualizar recorde
            if st.session_state.popularidade > st.session_state.recorde_pop:
                st.session_state.recorde_pop = st.session_state.popularidade
                st.success(f"🏆 NOVO RECORDE PESSOAL: {st.session_state.recorde_pop:.1f}%!")
        else:
            st.markdown(f"""
            <div class="defeat">
                <h1 style="margin: 0; font-size: 48px;">😞 DERROTA</h1>
                <p style="font-size: 22px; margin: 20px 0;">{st.session_state.msg_fim}</p>
                <p style="font-size: 18px;">Popularidade final: <strong>{st.session_state.popularidade:.1f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Botão de jogar novamente
        if st.button("🎮 Jogar Novamente", use_container_width=True, type="primary"):
            st.session_state.partido = None
            st.rerun()
        
        # Histórico
        with st.expander("📜 Histórico de Decisões", expanded=False):
            if st.session_state.historico:
                for item in st.session_state.historico:
                    st.write(f"• {item}")
            else:
                st.write("Nenhuma decisão registrada ainda.")
    
    else:
        # Gerar evento se necessário
        if st.session_state.evento_atual is None:
            st.session_state.evento_atual = gerar_evento()
        
        evento = st.session_state.evento_atual
        
        # Card do evento
        st.markdown(f"""
        <div class="event">
            <h2 style="margin: 0 0 15px 0; color: #333;">{evento['titulo']}</h2>
            <p style="font-size: 16px; line-height: 1.6; color: #555;">{evento['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🤔 Qual sua decisão?")
        
        # Botões de opção
        for i, opcao in enumerate(evento['opcoes']):
            col_btn, col_preview = st.columns([3, 1])
            
            with col_btn:
                if st.button(f"Opção {i+1}: {opcao['texto']}", key=f"opt_{i}", use_container_width=True):
                    aplicar_consequencias(opcao)
                    st.session_state.evento_atual = None
                    st.session_state.dia += 1
                    verificar_fim()
                    st.rerun()
            
            with col_preview:
                pop_sign = "📈" if opcao['pop'] > 0 else "📉" if opcao['pop'] < 0 else "➡️"
                caixa_sign = "💰" if opcao['caixa'] > 0 else "💸" if opcao['caixa'] < 0 else "➡️"
                energia_sign = "⚡" if opcao['energia'] > 0 else "🔋" if opcao['energia'] < 0 else "➡️"
                st.write(f"{pop_sign} Pop: {opcao['pop']:+}")
                st.write(f"{caixa_sign} Caixa: {opcao['caixa']:+,}")
                st.write(f"{energia_sign} Energia: {opcao['energia']:+}")
        
        # Dicas
        with st.expander("💡 Dicas de Estratégia"):
            st.write("""
            **GERENCIAMENTO DE RECURSOS:**
            - Mantenha Popularidade acima de 20% para segurança
            - Deixe sempre R$ 30.000+ no caixa para emergências
            - Energia abaixo de 30% = priorize descanso
            
            **POR PARTIDO:**
            - 🔴 Esquerda: Ganha mais popularidade, perde caixa
            - 🟡 Centro: Equilibrado, bônus diário de caixa
            - 🔵 Direita: Ganha muito caixa, mas perde popularidade
            
            **VITÓRIA:**
            - 45%+ no dia 30 = Vitória no 1º turno 🎉
            - 35%+ no dia 30 = 2º turno ✅
            - Abaixo de 35% = Eliminado ❌
            """)

def sidebar():
    """Sidebar com informações rápidas"""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/ballot-box-with-ball.png", width=80)
        st.title("🎛️ Painel")
        
        if st.session_state.get('partido'):
            st.write(f"**🎭 Partido:** {st.session_state.partido.upper()}")
            st.write(f"**🎯 Dificuldade:** {st.session_state.dificuldade}")
            st.divider()
            
            st.write("### 📊 Status Atual")
            st.write(f"📅 **Dia:** {st.session_state.dia}/{st.session_state.total_dias}")
            st.write(f"📈 **Popularidade:** {st.session_state.popularidade:.1f}%")
            st.write(f"💰 **Caixa:** R$ {st.session_state.caixa:,.0f}")
            st.write(f"⚡ **Energia:** {st.session_state.energia}%")
            
            # Alertas
            if st.session_state.popularidade < 20:
                st.warning("⚠️ Popularidade baixa!")
            if st.session_state.caixa < 30000:
                st.warning("⚠️ Caixa crítico!")
            if st.session_state.energia < 30:
                st.warning("⚠️ Energia baixa!")
            
            st.divider()
            st.info("💡 Dica: Clique em 'Gráfico' para ver sua evolução!")

# ============================================================================
# MAIN - PONTO DE ENTRADA
# ============================================================================
def main():
    """Função principal - inicializa tudo corretamente"""
    
    # Inicializar TODAS as variáveis de sessão que podem ser acessadas
    if 'partido' not in st.session_state:
        st.session_state.partido = None
    if 'recorde_pop' not in st.session_state:
        st.session_state.recorde_pop = 0.0
    if 'mostrar_grafico' not in st.session_state:
        st.session_state.mostrar_grafico = False
    
    # Se o jogo já começou, garantir que todas as variáveis existem
    if st.session_state.partido is not None:
        vars_necessarias = [
            'dia', 'total_dias', 'popularidade', 'caixa', 'energia',
            'game_over', 'vitoria', 'msg_fim', 'evento_atual',
            'historico', 'evolucao_pop', 'evolucao_dias', 'dificuldade'
        ]
        for var in vars_necessarias:
            if var not in st.session_state:
                init_game()
                break
    
    # Renderizar sidebar
    sidebar()
    
    # Renderizar tela apropriada
    if st.session_state.partido is None:
        tela_inicial()
    else:
        tela_jogo()

# ============================================================================
# EXECUÇÃO
# ============================================================================
if __name__ == "__main__":
    main()
