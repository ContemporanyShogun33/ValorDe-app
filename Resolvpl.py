import streamlit as st
import matplotlib.pyplot as plt
from google import genai
import pandas as pd

# Configuração premium da página web
st.set_page_config(page_title="ValorDe AI - Premium BI", layout="wide")

# --- CONEXÃO COM O GEMINI ---
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

st.sidebar.markdown("---")

# 3. ABA DE FEEDBACK
st.sidebar.subheader("💡 Sugestões e Erros")
nome_usuario = st.sidebar.text_input("Seu Nome:")
mensagem_feedback = st.sidebar.text_area("O que podemos melhorar no ValorDe?")
if st.sidebar.button("Enviar Feedback"):
    if nome_usuario and mensagem_feedback:
        st.sidebar.success(f"Obrigado, {nome_usuario}! Kaleb Machado recebeu seu feedback.")
    else:
        st.sidebar.warning("Preencha o nome e a mensagem.")

# --- 📊 PAINEL PRINCIPAL DIREITO ---
tab1, tab2 = st.tabs(["📊 Documentador Avançado", "💎 Planos Mensais"])

with tab1:
    st.title("Documentador de Atividades Diárias")
    st.subheader("Monitore a fuga de valor estratégico da sua holding")

    col_in1, col_in2 = st.columns(2)
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
                
                prompt_classificacao = (
                    "Você é o algoritmo de auditoria da holding ValorDe.\n"
                    "Analise a atividade e responda com OPERACIONAL ou ESTRATEGICO.\n"
                    f"Atividade: '{tarefa}'"
                )
                
                classe_final = "OPERACIONAL"
                if client and CHAVE_GEMINI != "SUA_CHAVE_GEMINI_AQUI":
                    try:
                        res_classe = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_classificacao)
                        classe_final = res_classe.text.strip().upper()
                    except Exception:
                        classe_final = "OPERACIONAL"
                else:
                    termos_op = ["limpar", "organizar", "caixa", "banco", "correio", "ajuda", "oi", "poeira", "pagar", "conta"]
                    if any(t in tarefa.lower() for t in termos_op) or len(tarefa) < 5:
                        classe_final = "OPERACIONAL"
                    else:
                        classe_final = "ESTRATEGICO"

                st.write("---")

                if "OPERACIONAL" in classe_final:
                    prejuizo_oculto = tempo_estimado_tarefa * valor_hora_ideal
                    st.session_state.historico["Operacional (Prejuízo)"] += tempo_estimado_tarefa
                    
                    st.error(f"⚠️ **STATUS: ATIVIDADE OPERACIONAL DETECTADA**")
                    st.markdown(f"🔴 **Custo de Oportunidade Desperdiçado:** R$ {prejuizo_oculto:.2f}")
                    
                    st.session_state.lista_atividades.append({
                        "Atividade": tarefa, "Horas": tempo_estimado_tarefa, "Tipo": "⚠️ Operacional", "Custo Oculto": f"R$ {prejuizo_oculto:.2f}"
                    })
                    
                    prompt_diagnostico = (
                        "Você é um consultor de eficiência de altíssimo nível (QI 140), especialista em reestruturação de holdings.\n"
                        "Gere um diagnóstico macroeconômico detalhado em Markdown usando jargões avançados.\n"
                        f"Atividade analisada: '{tarefa}'. Custo: R$ {prejuizo_oculto:.2f}."
                    )
                    
                    if client and CHAVE_GEMINI != "SUA_CHAVE_GEMINI_AQUI":
                        with st.spinner("Gerando Auditoria Avançada QI 140..."):
                            try:
                                resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_diagnostico)
                                st.markdown(resposta.text)
                            except Exception:
                                client = None
                    
                    if not client or CHAVE_GEMINI == "SUA_CHAVE_GEMINI_AQUI":
                        st.markdown(f"""
                        ### 🔍 1. ANÁLISE DO GARGALO OPERACIONAL (*CORE BUSINESS*)
                        A execução de microtarefas repetitivas e burocráticas pelo principal ativo estratégico da holding (o fundador) gera uma **anomalia de alocação tática**. Atividades que não escalam criam um teto técnico de crescimento, impedindo a descentralização de processos e a automação do ecossistema.
                        
                        ### 📉 2. DESTRUIÇÃO DE VALUATION E ROI
                        Ao submeter sua agenda a essa operação por {tempo_estimado_tarefa} horas, a empresa sofreu uma retração direta de **R$ {prejuizo_oculto:.2f}** em custo de oportunidade. Multiplicado pelo ano fiscal, esse vazamento invisível de caixa destrói a margem de **EBITDA**, reduzindo drasticamente o *Valuation* patrimonial para rodadas de investimento futuros.
                        
                        ### 🚀 3. ENGENHARIA DE SOLUÇÃO E ESCALA
                        *   **Curto Prazo:** Delegar a função imediatamente para um assistente virtual terceirizado (BPO Administrativo) ou contratar mão de obra júnior/estagiário focada puramente em execução.
                        *   **Médio Prazo:** Implementar ferramentas integradas de automação em nuvem (*SaaS*) para isolar o fundador do trabalho operacional e blindar as horas estratégicas focadas em tração comercial.
                        """)
                
                else:
                    st.session_state.historico["Estratégico"] += tempo_estimado_tarefa
                    st.success(f"🟢 **STATUS: ATIVIDADE ESTRATÉGICA CONFIRMADA**")
                    st.session_state.lista_atividades.append({
                        "Atividade": tarefa, "Horas": tempo_estimado_tarefa, "Tipo": "🟢 Estratégica", "Custo Oculto": "R$ 0,00"
                    })
                    st.markdown("""
                    ### 📈 PARECER DE GOVERNANÇA CORPORATIVA
                    A alocação de tempo atual está alinhada perfeitamente com os objetivos de alta escala do negócio. Concentrar os blocos de trabalho em inteligência comercial, expansão de produto ou aquisição de clientes gera um **retorno sobre o tempo (ROT)** exponencial, expandindo as métricas de tração e o valor de mercado (*Valuation*) do ecossistema.
                    """)

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
            valores = [estrat_val, operat_val]
            labels = ['Estratégico', 'Operacional']
            cores = ['#2e7d32', '#d32f2f']
            autopct = '%1.1f%%'

        ax.pie(valores, labels=labels, colors=cores, autopct=autopct, startangle=90, textprops=dict(color="white", size=10, weight="bold"), wedgeprops=dict(width=0.4, edgecolor='#0e1117', linewidth=2))
        ax.axis('equal')
        st.pyplot(fig)

    st.markdown("---")
    st.write("### 📜 Linha do Tempo de Atividades da Holding")
    if st.session_state.lista_atividades:
        df = pd.DataFrame(st.session_state.lista_atividades)
        st.dataframe(df, use_container_width=True)
    else:
        st.caption("Nenhuma atividade documentada no bloco atual.")

with tab2:
    st.title("💎 Nossos Planos - Seja Membro da Holding")
    st.write("Escolha o plano ideal para blindar o tempo da sua empresa e aumentar seus lucros.")
    st.markdown("---")
    
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("### 🥉 Plano Start\n**R$ 0,00** / Sempre Grátis\n* Análise básica de tarefas\n* Gráfico de rosca padrão")
        st.button("Plano Atual", disabled=True, key="b1")
        
    with p2:
        st.markdown("### 🥈 Plano Dono Pro\n**R$ 29,90** / Mês\n* **IA Gemini Avançada (QI 140)**\n* Relatórios mensais estruturados\n* Acesso ao Histórico Completo")
        st.button("Assinar Plano Pro", type="primary", key="b2")
        
    with p3:
        st.markdown("### 🥇 Plano Holding VIP\n**R$ 89,90** / Mês\n* Integração Pix automatizada\n* Consultoria de Processos com Kaleb")
        st.button("Falar com Consultor", key="b3")

if st.button("Limpar Histórico e Resetar Painel"):
