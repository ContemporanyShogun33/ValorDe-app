import streamlit as st
from google import genai
import pandas as pd

# 1. Configuração do Ambiente Web de Alta Performance
st.set_page_config(
    page_title="ValorDe AI | Enterprise Business Intelligence", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS customizada para criar uma interface executiva e limpa
st.markdown("""
<style>
    .metric-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- CONEXÃO COM O MOTOR DE IA GEMINI ---
# IMPORTANTÍSSIMO: Cole sua chave do Google AI Studio dentro das aspas abaixo!
CHAVE_GEMINI = "SUA_CHAVE_GEMINI_AQUI"

try:
    client = genai.Client(api_key=CHAVE_GEMINI)
except Exception:
    client = None

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

faturamento_mensal = st.sidebar.number_input("Meta de Faturamento Mensal (R$):", min_value=1.0, value=25000.0, step=1000.0)
horas_operacionais_mes = st.sidebar.number_input("Horas de Trabalho Mensais:", min_value=1.0, value=160.0, step=10.0)

valor_hora_patrimonial = faturamento_mensal / horas_operacionais_mes
st.sidebar.metric(label="Valor Patrimonial da sua Hora", value=f"R$ {valor_hora_patrimonial:.2f}/h")

st.sidebar.markdown("---")
st.sidebar.info("**Salmo 23:1**\n\n\"O Senhor é o meu pastor, nada me faltará.\" 🙏")

st.sidebar.markdown("---")
st.sidebar.subheader("💡 Central de Melhorias")
user_ref = st.sidebar.text_input("Organização:")
feed_text = st.sidebar.text_area("O que precisa ser implementado na próxima Sprint?")
if st.sidebar.button("Registrar Requisição"):
    if user_ref and feed_text:
        st.sidebar.success("Feedback indexado ao pipeline de desenvolvimento da holding.")

# --- 📊 CONTROLADORA E INTERFACE PRINCIPAL ---
tab_dashboard, tab_planos = st.tabs(["🖥️ Enterprise Dashboard", "💎 Assinaturas & Licenciamento"])

with tab_dashboard:
    st.title("Auditoria Avançada de Alocação de Tempo")
    st.subheader("Inteligência analítica contra a queima de Valuation corporativo")
    st.markdown("---")
    
    # PAINEL DE MÉTRICAS OPERACIONAIS
    m1, m2, m3 = st.columns(3)
    total_horas = st.session_state.tempo_estrategico + st.session_state.tempo_operacional
    percent_estrategico = (st.session_state.tempo_estrategico / total_horas * 100) if total_horas > 0 else 0.0
    
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style='color: #8B949E; margin:0;'>ÍNDICE DE FOCO ESTRATÉGICO</h4>
            <h1 style='color: #2EA043; margin:10px 0;'>{percent_estrategico:.1f}%</h1>
            <p style='color: #8B949E; font-size:12px; margin:0;'>Meta ideal de mercado: > 80%</p>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style='color: #8B949E; margin:0;'>VULNERABILIDADE OPERACIONAL</h4>
            <h1 style='color: #F85149; margin:10px 0;'>{st.session_state.tempo_operacional:.1f}h</h1>
            <p style='color: #8B949E; font-size:12px; margin:0;'>Tempo total queimado no operacional</p>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style='color: #8B949E; margin:0;'>PREJUÍZO ACUMULADO (ROI NEGATIVO)</h4>
            <h1 style='color: #F85149; margin:10px 0;'>R$ {st.session_state.custo_total_desperdiçado:.2f}</h1>
            <p style='color: #8B949E; font-size:12px; margin:0;'>Vazamento invisível de Valuation</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    c_input, c_tempo = st.columns(2)
    with c_input:
        atividade_analisada = st.text_input("Descreva minuciosamente a atividade executada nas últimas horas:", placeholder="Ex: Analisei as planilhas de margem líquida e fechei contrato com 2 clientes...")
    with c_tempo:
        horas_alocadas = st.number_input("Duração Real da Atividade (Horas):", min_value=0.5, value=2.0, step=0.5)

    if st.button("Executar Diagnóstico com Inteligência Artificial", type="primary"):
        if not atividade_analisada:
            st.warning("Insira os dados da atividade para processar os algoritmos de BI.")
        else:
            tempo_estimado_tarefa = horas_alocadas
            
            prompt_classificacao = (
                "Você é o algoritmo central de auditoria da holding ValorDe. Sua inteligência é analítica, fria e precisa.\n"
                "Analise a atividade executada pelo dono da empresa e responda RIGOROSAMENTE com apenas uma palavra (OPERACIONAL ou ESTRATEGICO).\n"
                f"Atividade: '{atividade_analisada}'"
            )
            
            classe_final = "OPERACIONAL"
            if client and CHAVE_GEMINI != "SUA_CHAVE_GEMINI_AQUI":
                try:
                    res_classe = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_classificacao)
                    classe_final = res_classe.text.strip().upper()
                except Exception:
                    classe_final = "OPERACIONAL"
            else:
                termos_gargalo = ["limpar", "limpando", "poeira", "organizar", "entregar", "empacotar", "lavar", "caixa", "banco", "correio", "ajuda", "oi", "pagar", "conta", "parentes", "mãe"]
                if any(termo in atividade_analisada.lower() for termo in termos_gargalo) or len(atividade_analisada) < 6:
                    classe_final = "OPERACIONAL"
                else:
                    classe_final = "ESTRATEGICO"

            st.markdown("### 📋 Relatório de Auditoria Executiva")
            
            if "OPERACIONAL" in classe_final:
                perda_financeira = tempo_estimado_tarefa * valor_hora_patrimonial
                st.session_state.tempo_operacional += tempo_estimado_tarefa
                st.session_state.custo_total_desperdiçado += perda_financeira
                
                st.session_state.logs_auditoria.append({
                    "Atividade Analisada": atividade_analisada,
                    "Alocação Temporal": f"{tempo_estimado_tarefa}h",
                    "Classificação": "⚠️ Operacional (Prejuízo)",
                    "Dano ao Valuation": f"R$ {perda_financeira:.2f}"
                })
                
                st.error(f"🔴 **CRÍTICO: DETECTADA FUGA DE VALOR PATRIMONIAL** | Custo de Oportunidade Desperdiçado: R$ {perda_financeira:.2f}")
                
                prompt_diagnostico = (
                    "Você é um consultor de eficiência corporativa de altíssimo nível (QI 140), especialista em Venture Capital e reestruturação de holdings.\n"
                    "Gere um diagnóstico macroeconômico e de processos ultra detalhado, denso e técnico sobre o erro do empresário.\n"
                    "Use termos corporativos avançados (Valuation, Gargalo de Escala, Core Business, Alocação Eficiente de Capital, EBITDA).\n\n"
                    "Estruture sua resposta EXATAMENTE com os seguintes tópicos em Markdown:\n"
                    "### 🔍 1. ANÁLISE DETALHADA DO GARGALO OPERACIONAL\n"
                    "(Explique cientificamente o erro tático de o tomador de decisão da holding desviar seu foco para essa atividade específica)\n\n"
                    "### 📉 2. DESTRUIÇÃO DE VALUATION E IMPACTO FINANCEIRO\n"
                    "(Mostre o impacto financeiro de longo prazo com base no custo de oportunidade gerado)\n\n"
                    "### 🚀 3. PLANO DE MITIGAÇÃO E AUTOMAÇÃO ESCALÁVEL\n"
                    "(Apresente uma solução prática: cite o nome de um software específico do mercado ou o perfil exato de um profissional terceirizado ou estagiário que deveria assumir isso para destravar o crescimento do negócio)\n\n"
                    f"Atividade analisada: '{atividade_analisada}'. Custo de oportunidade direto: R$ {perda_financeira:.2f}."
                )
                
                if client and CHAVE_GEMINI != "SUA_CHAVE_GEMINI_AQUI":
                    with st.spinner("Gerando Auditoria Avançada QI 140..."):
                        try:
                            resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_diagnostico)
                            st.markdown(resposta.text)
                        except Exception:
                            client = None
                
                if not client or CHAVE_GEMINI == "SUA_CHAVE_GEMINI_AQUI":
                    # CORREÇÃO DA ASMA TRIPLA: Texto estático blindado e formatado
                    st.markdown(f"""
### 🔍 1. GARGALO DE ALOCAÇÃO DE CAPITAL HUMANO
A execução desta atividade pelo principal estrategista da holding representa uma quebra drástica na eficiência dos processos corporativos. Tarefas de baixa complexidade técnica criam um **gargalo invisível de escala**, forçando o tomador de decisão a operar como mão de obra operacional de baixo valor agregado, em vez de focar no *Core Business*.

### 📉 2. ANÁLISE DE IMPACTO FINANCEIRO E DESTRUIÇÃO DE EBITDA

