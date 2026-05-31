import streamlit as st
import matplotlib.pyplot as plt
from google import genai
import pandas as pd

# Configuração premium da página web
st.set_page_config(page_title="ValorDe AI - Premium BI", layout="wide")

# --- CONEXÃO COM O GEMINI ---
# IMPORTANTÍSSIMO: Cole sua chave real do Google AI Studio (pega em ://google.com) entre as aspas abaixo:
CHAVE_GEMINI = "SUA_CHAVE_GEMINI_AQUI"

try:
    client = genai.Client(api_key=CHAVE_GEMINI)
except Exception:
    client = None

# --- BANCO DE DADOS EM MEMÓRIA ---
if "historico" not in st.session_state:
    st.session_state.historico = {"Estratégico": 0.0, "Operacional (Prejuízo)": 0.0}
if "lista_atividades" not in st.session_state:
    st.session_state.lista_atividades = []

# --- 📐 PAINEL LATERAL ESQUERDO ---
st.sidebar.title("ValorDe AI 📊")
st.sidebar.caption("Desenvolvido por Kaleb Machado | Engenharia de Prompt QI 140")
st.sidebar.markdown("---")

faturamento = st.sidebar.number_input("Meta de Faturamento Mensal (R$):", min_value=1.0, value=15000.0)
horas_mes = st.sidebar.number_input("Horas de Trabalho por Mês:", min_value=1.0, value=160.0)
valor_hora_ideal = faturamento / horas_mes
st.sidebar.metric(label="Sua Hora Ideal Deve Valer", value=f"R$ {valor_hora_ideal:.2f}/h")

st.sidebar.markdown("---")
st.sidebar.info("**Salmo 23:1**\n\n\"O Senhor é o meu pastor, nada me faltará.\" 🙏")

# --- 📊 PAINEL PRINCIPAL DIREITO ---
tab1, tab2 = st.tabs(["📊 Documentador Avançado", "💎 Planos Mensais"])

with tab1:
    st.title("Documentador de Atividades Diárias")
    st.subheader("Monitore a fuga de valor estratégico da sua holding")

    col_in1, col_in2 = st.columns([3, 1])
    with col_in1:
        tarefa = st.text_input(label="Atividade Executada", placeholder="Ex: Passei a tarde organizando notas fiscais velhas...")
    with col_in2:
        tempo_gasto = st.number_input("Horas Gastas:", min_value=0.5, value=2.0, step=0.5)

    col_dados, col_grafico = st.columns(2)

    with col_dados:
        if st.button("Analisar Impacto Financeiro", type="primary"):
            if not tarefa:
                st.warning("Por favor, descreva a atividade antes de analisar.")
            else:
                tempo_estimado_tarefa = tempo_gasto
                
                # Engenharia de Prompt Avançada para Classificação Estrita
                prompt_classificacao = (
                    "Você é o algoritmo central de auditoria da holding ValorDe. Sua inteligência é analítica, fria e precisa.\n"
                    "Analise a atividade executada pelo dono da empresa e responda RIGOROSAMENTE com apenas uma palavra (OPERACIONAL ou ESTRATEGICO).\n"
                    "Regra: Se a atividade envolver tarefas braçais, burocracias, resolver problemas de parentes, ir ao banco, empacotar produtos, limpar a empresa ou responder mensagens repetitivas, classifique como OPERACIONAL.\n"
                    f"Atividade: '{tarefa}'"
                )
                
                classe_final = "OPERACIONAL"
                if client:
                    try:
                        res_classe = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_classificacao)
                        classe_final = res_classe.text.strip().upper()
                    except Exception:
                        classe_final = "OPERACIONAL"

                st.clear_cache()
                st.write("---")

                if "OPERACIONAL" in classe_final:
                    prejuizo_oculto = tempo_estimado_tarefa * valor_hora_ideal
                    st.session_state.historico["Operacional (Prejuízo)"] += tempo_estimado_tarefa
                    
                    st.error(f"⚠️ **STATUS: ATIVIDADE OPERACIONAL DETECTADA**")
                    st.markdown(f"🔴 **Custo de Oportunidade Desperdiçado:** R$ {prejuizo_oculto:.2f} (Baseado no tempo gasto de {tempo_estimado_tarefa}h)")
                    
                    st.session_state.lista_atividades.append({
                        "Atividade": tarefa, "Horas": tempo_estimado_tarefa, "Tipo": "⚠️ Operacional", "Custo Oculto": f"R$ {prejuizo_oculto:.2f}"
                    })
                    
                    # PROMPT QI 140: Força o Gemini a escrever de forma sofisticada e corporativa
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
                        f"Atividade analisada: '{tarefa}'. Custo de oportunidade direto: R$ {prejuizo_oculto:.2f}."
                    )
                    
                    with st.spinner("Gerando Auditoria Avançada QI 140..."):
                        if client:
                            try:
                                resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_diagnostico)
                                st.markdown(resposta.text)
                            except Exception as e:
                                st.warning(f"Erro na conexão com a IA: {e}. Exibindo relatório padrão.")
                        else:
                            # Relatório padrão muito mais denso caso a chave não esteja configurada
                            st.markdown(f"""
                            ### 🔍 1. ANÁLISE DETALHADA DO GARGALO OPERACIONAL
                            A execução de microtarefas administrativas pelo principal tomador de decisão da empresa representa um severo desvio de foco do *Core Business*. Atividades repetitivas funcionam como um teto de crescimento invisível, limitando a capacidade de expansão da holding.
                            
                            ### 📉 2. DESTRUIÇÃO DE VALUATION E IMPACTO FINANCEIRO
                            Ao queimar {tempo_estimado_tarefa} horas nesta operação, a empresa sofreu uma perda direta de **R$ {prejuizo_oculto:.2f}** em poder de tração. No acumulado anual, esse hábito pode destruir dezenas de milhares de reais que deveriam estar sendo convertidos em margem de EBITDA ou novos clientes.
                            
                            ### 🚀 3. PLANO DE MITIGAÇÃO E AUTOMAÇÃO ESCALÁVEL
                            Recomenda-se a imediata substituição da força de trabalho do fundador por sistemas de automação de processos (SaaS) ou pela contratação de um assistente virtual terceirizado (BPO Financeiro/Administrativo). Isolar o fundador dessas tarefas é a única forma de destravar o ganho de escala.
                            """)
                
                else:
                    st.session_state.historico["Estratégico"] += tempo_estimado_tarefa
                    st.success(f"🟢 **STATUS: ATIVIDADE ESTRATÉGICA CONFIRMADA**")
                    st.session_state.lista_atividades.append({
                        "Atividade": tarefa, "Horas": tempo_estimado_tarefa, "Tipo": "🟢 Estratégica", "Custo Oculto": "R$ 0,00"
                    })
                    
                    prompt_diagnostico = (
                        "Você é um consultor sênior QI 140. O dono da holding executou uma atividade de alto valor estratégico.\n"
                        "Escreva um parecer corporativo sofisticado de 4 linhas explicando como essa alocação eficiente de tempo "
                        "maximiza o ROI, acelera a tração de mercado e expande o Valuation da empresa no longo prazo.\n"
                        f"Atividade executada: '{tarefa}'"
                    )
                    
                    with st.spinner("Gerando Relatório de Crescimento..."):
                        if client:
                            try:
                                resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_diagnostico)
                                st.markdown(resposta.text)
                            except Exception:
                                st.markdown("Alocação de tempo altamente eficiente. Focar no crescimento de alto nível expande o Valuation e a governança corporativa do seu ecossistema.")
                        else:
                            st.markdown("Alocação de tempo altamente eficiente. Focar no crescimento de alto nível expande o Valuation e a governança corporativa do seu ecossistema.")

    with col_grafico:
        st.write("### Divisão do Tempo do Dono")
        estrat_val = st.session_state.historico["Estratégico"]
        operat_val = st.session_state.historico["Operacional (Prejuízo)"]
        
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#0e1117')
        ax.set_facecolor('#0e1117')
        
        if estrat_val == 0 and operat_val == 0:
            valores = [1.0]
            labels = ['Sem dados']
            cores = ['#262730']
            autopct = None
        else:


