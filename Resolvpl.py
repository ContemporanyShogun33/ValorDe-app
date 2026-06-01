import streamlit as st
import pandas as pd

# 1. Configuração de Arquitetura Web de Elite
st.set_page_config(
    page_title="ValorDe AI | Enterprise Business Intelligence", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS de Terminal Executivo Premium
st.markdown("""
<style>
    .metric-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 22px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .kpi-title { color: #8B949E; font-size:13px; font-weight: 600; text-transform: uppercase; margin:0; }
    .kpi-value { font-size: 32px; font-weight: bold; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# --- MATRIZ CONFIGURATIVA FINANCEIRA ---
faturamento_mensal = 25000.0
horas_operacionais_mes = 160.0
valor_hora_patrimonial = faturamento_mensal / horas_operacionais_mes
custo_ociosidade_inicial = 2.0 * valor_hora_patrimonial

# --- ESTRUTURA DE RETENÇÃO DE DADOS (SESSION STATE) ---
if "tempo_estrategico" not in st.session_state:
    st.session_state.tempo_estrategico = 0.0
if "tempo_operacional" not in st.session_state:
    st.session_state.tempo_operacional = 0.0
if "custo_total_desperdiçado" not in st.session_state:
    st.session_state.custo_total_desperdiçado = custo_ociosidade_inicial
if "logs_auditoria" not in st.session_state:
    st.session_state.logs_auditoria = []

# --- 📐 PAINEL LATERAL DE GOVERNANÇA CORPORATIVA ---
st.sidebar.title("ValorDe AI 📊")
st.sidebar.caption("Enterprise Platform | Core Engine v3.0")
st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ Parâmetros Financeiros")
st.sidebar.write(f"**Meta de Caixa Mensal:** R$ {faturamento_mensal:,.2f}")
st.sidebar.write(f"**Capacidade Operacional:** {horas_operacionais_mes}h / mês")
st.sidebar.metric(label="Valuation Real da sua Hora", value=f"R$ {valor_hora_patrimonial:.2f}/h")

st.sidebar.markdown("---")
st.sidebar.info("**Salmo 23:1**\n\n\"O Senhor é o meu pastor, nada me faltará.\" 🙏")

# --- 📊 CONTROLADORA E INTERFACE PRINCIPAL ---
tab_dashboard, tab_planos = st.tabs(["🖥️ Enterprise BI Engine", "💎 Licenciamento & Monetização"])

with tab_dashboard:
    st.title("Auditoria Avançada de Alocação de Tempo")
    st.subheader("Análise quantitativa de queima de ativos e Valuation corporativo")
    st.markdown("---")
    
    # ⚖️ MÁQUINA MATEMÁTICA ANALÍTICA DE MERCADO
    total_horas_registradas = st.session_state.tempo_estrategico + st.session_state.tempo_operacional
    
    if total_horas_registradas > 0:
        percent_estrategico = (st.session_state.tempo_estrategico / total_horas_registradas) * 100
        texto_escala = f"{percent_estrategico:.1f}%"
        cor_escala = "#2EA043" if percent_estrategico >= 80 else "#D29922" if percent_estrategico >= 50 else "#F85149"
        texto_vulnerabilidade = f"{st.session_state.tempo_operacional:.1f}h"
    else:
        percent_estrategico = 0.0
        texto_escala = "0.0% (Gargalo de Ociosidade)"
        cor_escala = "#8B949E"
        texto_vulnerabilidade = "2.0h (Inércia Inicial)"

    # Cards Executivos Customizados via HTML/CSS
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown(f'<div class="metric-card"><p class="kpi-title">ÍNDICE DE ALOCAÇÃO ESTRATÉGICA</p><div class="kpi-value" style="color: {cor_escala};">{texto_escala}</div><p style="color: #8B949E; font-size:12px; margin:0;">Eficiência mínima exigida: > 80%</p></div>', unsafe_allow_html=True)
        
    with m2:
        st.markdown(f'<div class="metric-card"><p class="kpi-title">VULNERABILIDADE OPERACIONAL</p><div class="kpi-value" style="color: #F85149;">{texto_vulnerabilidade}</div><p style="color: #8B949E; font-size:12px; margin:0;">Volume de horas queimadas no operacional</p></div>', unsafe_allow_html=True)
        
    with m3:
        st.markdown(f'<div class="metric-card"><p class="kpi-title">ROI DESPERDIÇADO ACUMULADO</p><div class="kpi-value" style="color: #F85149;">R$ {st.session_state.custo_total_desperdiçado:.2f}</div><p style="color: #8B949E; font-size:12px; margin:0;">Fuga invisível de capital patrimonial</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Barras Progressivas Visuais Nativas do Streamlit
    st.write("### 📈 Painel Volométrico de Desempenho")
    st.write("**Aproveitamento Estratégico da Holding:**")
    st.progress(float(percent_estrategico / 100))
    
    st.markdown("---")
    
    # INTERFACE DE CAPTAÇÃO DE DADOS
    c_input, c_tempo = st.columns(2)
    with c_input:
        atividade_analisada = st.text_input("Descreva o processo executado na empresa para fins de auditoria:", placeholder="Ex: Desenvolvi o roadmap de expansão da holding...")
    with c_tempo:
        horas_alocadas = st.number_input("Janela de Tempo Alocada (Horas):", min_value=0.5, value=2.0, step=0.5)

    if st.button("Disparar Auditoria de Processos", type="primary"):
        if not atividade_analisada:
            st.warning("Insira a descrição da atividade para alimentar os algoritmos de BI.")
        else:
            termos_gargalo = ["limpar", "limpando", "poeira", "organizar", "entregar", "empacotar", "lavar", "caixa", "banco", "correio", "ajuda", "oi", "pagar", "conta", "parentes", "mãe"]
            is_operacional = any(termo in atividade_analisada.lower() for termo in termos_gargalo) or len(atividade_analisada) < 5

            st.write("### 📋 Parecer de Auditoria Analítica")
            
            if st.session_state.tempo_estrategico == 0.0 and st.session_state.tempo_operacional == 0.0:
                st.session_state.custo_total_desperdiçado = 0.0

            if is_operacional:
                perda_financeira = horas_alocadas * valor_hora_patrimonial
                st.session_state.tempo_operacional += horas_alocadas
                st.session_state.custo_total_desperdiçado += perda_financeira
                
                st.session_state.logs_auditoria.append({
                    "Atividade Executada": atividade_analisada,
                    "Carga Horária": f"{horas_alocadas}h",
                    "Veredito de BI": "⚠️ Gargalo Operacional",
                    "Impacto Financeiro": f"R$ {perda_financeira:.2f}"
                })
                
                st.error(f"🔴 ALERTA DE VULNERABILIDADE | Prejuízo de Oportunidade Computado: R$ {perda_financeira:.2f}")
                
                st.markdown("#### 🔍 1. DIAGNÓSTICO DE DESVIO DE CORE BUSINESS")
                st.write("A alocação da força de trabalho do tomador de decisão em microtarefas acessórias quebra o ganho de escala. Esse gargalo impede a automação corporativa e bloqueia o desenvolvimento de novos canais de receita estruturada.")
                
                st.markdown("#### 📉 2. CORROSÃO DE EBITDA E VALUATION")
                st.write(f"Queimar {horas_alocadas}h in sub-processos braçais drena R$ {perda_financeira:.2f} do caixa operacional implícito. No longo prazo, esse hábito corrói a margem líquida da empresa, inviabilizando rodadas de captação de investimento.")
                
                st.markdown("#### 🚀 3. ENGENHARIA DE CORREÇÃO")
                st.write("Recomenda-se a contratação urgente de um assistente virtual terceirizado (BPO) ou implementação de ferramentas de automação SaaS para assumir o processo e blindar o tempo estratégico do fundador.")
            
            else:
                st.session_state.tempo_estrategico += horas_alocadas
                st.session_state.logs_auditoria.append({
                    "Atividade Executada": atividade_analisada,
                    "Carga Horária": f"{horas_alocadas}h",
                    "Veredito de BI": "🟢 Alta Estratégia",
                    "Impacto Financeiro": "R$ 0,00"
                })
                
                st.success("🟢 EFICIÊNCIA CONFIRMADA: PRODUTIVIDADE DE ALTO VALOR PATRIMONIAL")
                st.markdown("#### 📈 STATUS DE GOVERNANÇA CORPORATIVA")
                st.write("Ação estratégica com alta alavancagem de mercado confirmada. O foco em expansão comercial, atração de clientes e melhoria de produto acelera os indicadores de tração do ecossistema e expande de forma escalável o Valuation total da empresa.")
            
            st.rerun()

    # --- HISTÓRICO EM TABELA CORPORATIVA ---
    st.markdown("---")
    st.write("### 📜 Histórico de Registros Auditados")
    if st.session_state.logs_auditoria:
        df_auditoria = pd.DataFrame(st.session_state.logs_auditoria)
        st.dataframe(df_auditoria, use_container_width=True)
        
        csv_data = df_auditoria.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar Dados para Excel (CSV)",
            data=csv_data,
            file_name="auditoria_valorde.csv",
            mime="text/csv"
        )
    else:
        st.caption("Nenhum registro armazenado na sessão corrente.")

with tab_planos:
    st.title("💎 Modelos de Licenciamento Empresarial")
    st.write("Selecione a licença corporativa ideal para escalar o monitoramento e blindar a lucratividade do seu ecossistema.")
    st.markdown("---")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown("### 🥉 Licença Start\n\n**R$ 0,00** / Sempre Grátis\n\n* Acesso ao Dashboard Corporativo\n* Relatório padrão de custo de oportunidade")
        st.button("Licença Ativa", disabled=True, key="p_free")
        
    with col_p2:
        st.markdown("### 🥈 Licença Dono Pro\n\n**R$ 29,90** / Mensal\n\n* **Mecanismo Inteligente Ativo**\n* Exportação de dados e relatórios sem restrições\n* Canal de suporte direto com Kaleb")
        st.button("Adquirir Licença Pro", type="primary", key="p_pro")
        
    with col_p3:
        st.markdown("### 🥇 Licença Holding VIP\n\n**R$ 89,90** / Mensal\n\n* **Recursos Avançados Desbloqueados**\n* Painel Multi-Empresas integrado\n* Mentoria de processos e arquitetura com Kaleb Machado")

