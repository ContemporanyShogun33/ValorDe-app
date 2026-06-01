import streamlit as st
import pandas as pd

# 1. Configuração do Ambiente Web de Alta Performance
st.set_page_config(
    page_title="ValorDe AI | Enterprise Business Intelligence", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS customizada
st.markdown("<style>.metric-card { background-color: #161B22; border: 1px solid #30363D; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }</style>", unsafe_allow_html=True)

# --- CONFIGURAÇÕES FINANCEIRAS ---
faturamento_mensal = 25000.0
horas_operacionais_mes = 160.0
valor_hora_patrimonial = faturamento_mensal / horas_operacionais_mes

# --- ESTRUTURA DE RETENÇÃO DE DADOS (SESSION STATE) ---
if "tempo_estrategico" not in st.session_state:
    st.session_state.tempo_estrategico = 0.0
if "tempo_operacional" not in st.session_state:
    st.session_state.tempo_operacional = 0.0
if "custo_total_desperdiçado" not in st.session_state:
    st.session_state.custo_total_desperdiçado = 0.0
if "logs_auditoria" not in st.session_state:
    st.session_state.logs_auditoria = []

# --- 📐 PAINEL LATERAL DE GOVERNANÇA ---
st.sidebar.title("ValorDe AI 📊")
st.sidebar.caption("Enterprise Edition | Powered by Kaleb Machado")
st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ Configurações Ativas")
st.sidebar.write(f"**Meta Mensal:** R$ {faturamento_mensal:,.2f}")
st.sidebar.write(f"**Carga Horária:** {horas_operacionais_mes}h / mês")
st.sidebar.metric(label="Valor Patrimonial da sua Hora", value=f"R$ {valor_hora_patrimonial:.2f}/h")

st.sidebar.markdown("---")
st.sidebar.info("**Salmo 23:1**\n\n\"O Senhor é o meu pastor, nada me faltará.\" 🙏")

# --- 📊 CONTROLADORA E INTERFACE PRINCIPAL ---
tab_dashboard, tab_planos = st.tabs(["🖥️ Enterprise Dashboard", "💎 Assinaturas & Licenciamento"])

with tab_dashboard:
    st.title("Auditoria Avançada de Alocação de Tempo")
    st.subheader("Inteligência analítica contra a queima de Valuation corporativo")
    st.markdown("---")
    
    # ⚖️ LÓGICA DE ESCALA REALISTA: Se não há horas registradas, o índice é 0.0% (Fim da mentira!)
    total_horas = st.session_state.tempo_estrategico + st.session_state.tempo_operacional
    
    if total_horas > 0:
        percent_estrategico = (st.session_state.tempo_estrategico / total_horas) * 100
        texto_escala = f"{percent_estrategico:.1f}%"
        cor_escala = "#2EA043" if percent_estrategico >= 80 else "#D29922" if percent_estrategico >= 50 else "#F85149"
    else:
        texto_escala = "0.0% (Aguardando Dados)"
        cor_escala = "#8B949E" # Cinza neutro comercial

    # PAINEL DE MÉTRICAS OPERACIONAIS COM ESCALA CORRIGIDA
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown(f'<div class="metric-card"><h4 style="color: #8B949E; margin:0;">ÍNDICE DE FOCO ESTRATÉGICO</h4><h1 style="color: {cor_escala}; margin:10px 0;">{texto_escala}</h1><p style="color: #8B949E; font-size:12px; margin:0;">Meta ideal de mercado: > 80%</p></div>', unsafe_allow_html=True)
        
    with m2:
        st.markdown(f'<div class="metric-card"><h4 style="color: #8B949E; margin:0;">VULNERABILIDADE OPERACIONAL</h4><h1 style="color: #F85149; margin:10px 0;">{st.session_state.tempo_operacional:.1f}h</h1><p style="color: #8B949E; font-size:12px; margin:0;">Tempo total queimado no operacional</p></div>', unsafe_allow_html=True)
        
    with m3:
        st.markdown(f'<div class="metric-card"><h4 style="color: #8B949E; margin:0;">PREJUÍZO ACUMULADO (ROI NEGATIVO)</h4><h1 style="color: #F85149; margin:10px 0;">R$ {st.session_state.custo_total_desperdiçado:.2f}</h1><p style="color: #8B949E; font-size:12px; margin:0;">Vazamento invisível de Valuation</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # INPUT INTERATIVO
    c_input, c_tempo = st.columns(2)
    with c_input:
        atividade_analisada = st.text_input("Descreva a atividade executada nas últimas horas:", placeholder="Ex: Limpei as prateleiras ou fechei contrato...")
    with c_tempo:
        horas_alocadas = st.number_input("Duração Real da Atividade (Horas):", min_value=0.5, value=2.0, step=0.5)

    if st.button("Executar Diagnóstico Comercial", type="primary"):
        if not atividade_analisada:
            st.warning("Insira os dados da atividade para processar.")
        else:
            termos_gargalo = ["limpar", "limpando", "poeira", "organizar", "entregar", "empacotar", "lavar", "caixa", "banco", "correio", "ajuda", "oi", "pagar", "conta", "parentes", "mãe"]
            is_operacional = any(termo in atividade_analisada.lower() for termo in termos_gargalo) or len(atividade_analisada) < 5

            st.write("### 📋 Relatório de Auditoria Executiva")
            
            if is_operacional:
                perda_financeira = horas_alocadas * valor_hora_patrimonial
                st.session_state.tempo_operacional += horas_alocadas
                st.session_state.custo_total_desperdiçado += perda_financeira
                
                st.session_state.logs_auditoria.append({
                    "Atividade": atividade_analisada,
                    "Tempo": f"{horas_alocadas}h",
                    "Classificação": "⚠️ Operacional",
                    "Prejuízo": f"R$ {perda_financeira:.2f}"
                })
                
                st.error(f"🔴 CRÍTICO: DETECTADA FUGA DE VALOR PATRIMONIAL | Prejuízo: R$ {perda_financeira:.2f}")
                
                st.markdown("### 🔍 1. GARGALO DE ALOCAÇÃO DE CAPITAL HUMANO")
                st.write("A execução desta atividade pelo principal estrategista da holding representa uma quebra drástica na eficiência. Tarefas de baixa complexidade técnica criam um gargalo invisível de escala, forçando o tomador de decisão a operar como mão de obra operacional.")
                
                st.markdown("### 📉 2. ANÁLISE DE IMPACTO FINANCEIRO E DESTRUIÇÃO DE EBITDA")
                st.write(f"Ao desviar {horas_alocadas}h de foco estratégico para processos braçais, a holding gerou um prejuízo imediato de R$ {perda_financeira:.2f}. No acumulado anual, esse hábito destrói o crescimento de mercado e o Valuation da sua holding.")
                
                st.markdown("### 🚀 3. ENGENHARIA DE PROCESSO E AUTOMAÇÃO RECOMENDADA")
                st.write("* **Substituição:** Migrar esta tarefa para uma infraestrutura de software SaaS ou BPO Administrativo.")
                st.write("* **Plano Executivo:** Delegação compulsória para um assistente. Liberar a agenda do fundador para tarefas de captação de clientes gera um retorno sobre o tempo (ROT) exponencialmente maior.")
            
            else:
                st.session_state.tempo_estrategico += horas_alocadas
                st.session_state.logs_auditoria.append({
                    "Atividade": atividade_analisada,
                    "Tempo": f"{horas_alocadas}h",
                    "Classificação": "🟢 Estratégica",
                    "Prejuízo": "R$ 0,00"
                })
                
                st.success("🟢 EFICIÊNCIA CONFIRMADA: ALOCAÇÃO DE TEMPO ESTRATÉGICO")
                st.markdown("### 📈 CERTIFICAÇÃO DE GOVERNANÇA CORPORATIVA")
                st.write("A atividade executada possui características de alta alavancagem comercial e planejamento tático. Concentrar esforços em vendas, captação ou novos canais de distribuição gera ganho de escala imediato e maximiza o Valuation patrimonial.")
            
            st.session_state.custo_total_desperdiçado = float(st.session_state.custo_total_desperdiçado)
            st.rerun()

    # --- HISTÓRICO EM TABELA CORPORATIVA ---
    st.markdown("---")
    st.write("### 📜 Linha do Tempo de Atividades")
    if st.session_state.logs_auditoria:
        df_auditoria = pd.DataFrame(st.session_state.logs_auditoria)
        st.dataframe(df_auditoria, use_container_width=True)
        
        csv_data = df_auditoria.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar Relatório em Excel (CSV)",
            data=csv_data,
            file_name="auditoria_valorde.csv",
            mime="text/csv"
        )
    else:
        st.caption("Nenhum registro de auditoria arquivado na sessão corrente.")

with tab_planos:
    st.title("💎 Nossos Planos - Modelos de Licenciamento")
    st.write("Selecione a licença corporativa ideal para escalar a automação e auditoria do seu grupo empresarial.")
    st.markdown("---")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown("### 🥉 Licença Start\n\n**R$ 0,00** / Sempre Grátis\n\n* Acesso ao Dashboard Corporativo\n* Relatório padrão de custo de oportunidade")
        st.button("Plano Ativo", disabled=True, key="p_free")
        
    with col_p2:
        st.markdown("### 🥈 Licença Dono Pro\n\n**R$ 29,90** / Mensal\n\n* **Mecanismo Inteligente QI 140 Ativo**\n* Exportação de dados e relatórios sem restrições\n* Suporte com o desenvolvedor Kaleb")
        st.button("Adquirir Licença Pro", type="primary", key="p_pro")
        
    with col_p3:
        st.markdown("### 🥇 Licença Holding VIP\n\n**R$ 89,90** / Mensal\n\n* **Tudo da licença PRO**\n* Painel Multi-Empresas integrado\n* Mentoria de processos com Kaleb Machado")
        st.button("Contatar Corporate Desk", key="p_vip")

st.markdown("---")
if st.button("Limpar Histórico e Resetar Servidor"):
    st.session_state.tempo_estrategico = 0.0
    st.session_state.tempo_operacional = 0.0
    st.session_state.custo_total_desperdiçado = 0.0
    st.session_state.logs_auditoria = []
    st.rerun()

