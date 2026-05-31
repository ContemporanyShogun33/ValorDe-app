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

# --- BANCO DE DADOS EM MEMÓRIA (SESSÃO DO NAVEGADOR) ---
if "historico" not in st.session_state:
    st.session_state.historico = {"Estratégico": 0.0, "Operacional (Prejuízo)": 0.0}
if "lista_atividades" not in st.session_state:
    st.session_state.lista_atividades = []

# --- 📐 PAINEL LATERAL ESQUERDO ---
st.sidebar.title("ValorDe AI 📊")
st.sidebar.caption("Desenvolvido por Kaleb Machado | Versão 2.0 Premium")
st.sidebar.markdown("---")

# 1. Configurações Financeiras Avançadas
faturamento = st.sidebar.number_input("Meta de Faturamento Mensal (R$):", min_value=1.0, value=15000.0)
horas_mes = st.sidebar.number_input("Horas de Trabalho por Mês:", min_value=1.0, value=160.0)
valor_hora_ideal = faturamento / horas_mes
st.sidebar.metric(label="Sua Hora Ideal Deve Valer", value=f"R$ {valor_hora_ideal:.2f}/h")

st.sidebar.markdown("---")

# 2. MOMENTO DE FÉ (SALMO 23)
st.sidebar.info("""
**Salmo 23:1**  
"O Senhor é o meu pastor, nada me faltará."
""")

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

    # Inputs complexos: Tarefa + Tempo Real que o dono gastou
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
            elif not client:
                st.error("Configure a chave do Gemini para habilitar os diagnósticos complexos.")
            else:
                # 🤖 Camada 1: Classificação Avançada por IA
                with st.spinner("Processando dados estratégicos..."):
                    try:
                        prompt_classificacao = (
                            "Você é o motor de auditoria da holding ValorDe.\n"
                            "Analise a atividade e responda APENAS com uma palavra:\n"
                            "OPERACIONAL - Para burocracias, limpeza, contas de parentes, banco, empacotamento, suporte simples.\n"
                            "ESTRATEGICO - Para vendas, parcerias, marketing estruturado, produto, captação de clientes.\n"
                            f"Atividade: {tarefa}"
                        )
                        res_classe = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_classificacao)
                        classe_final = res_classe.text.strip().upper()
                    except Exception:
                        classe_final = "OPERACIONAL"

                # 🤖 Camada 2: Geração de Diagnóstico Detalhado
                if "OPERACIONAL" in classe_final:
                    prejuizo_oculto = tempo_gasto * valor_hora_ideal
                    st.session_state.historico["Operacional (Prejuízo)"] += tempo_gasto
                    
                    st.error(f"⚠️ **STATUS: ATIVIDADE OPERACIONAL DETECTADA**")
                    st.markdown(f"🔴 **Custo de Oportunidade Desperdiçado:** R$ {prejuizo_oculto:.2f}")
                    
                    # Adiciona ao histórico da tabela
                    st.session_state.lista_atividades.append({"Atividade": tarefa, "Horas": tempo_gasto, "Tipo": "⚠️ Operacional", "Custo Oculto": f"R$ {prejuizo_oculto:.2f}"})
                    
                    with st.spinner("Gerando Relatório de Soluções..."):
                        try:
                            prompt_diagnostico = (
                                "Você é um consultor sênior de Business Intelligence da holding ValorDe.\n"
                                "Gere um relatório detalhado estruturado exatamente com os seguintes tópicos em Markdown:\n"
                                "### ❌ O ERRO OPERACIONAL\n(Explique por que o dono não deve fazer isso)\n"
                                "### 📉 IMPACTO FINANCEIRO\n(Mostre o prejuízo de usar o tempo dele nisso)\n"
                                "### 🚀 PLANO DE AÇÃO REALISTA\n(Dê o nome de 1 ferramenta ou o perfil de funcionário/estagiário barato para assumir isso e libertar o dono)\n"
                                f"Atividade analisada: {tarefa}. Custo gerado: R$ {prejuizo_oculto:.2f}"
                            )
                            resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_diagnostico)
                            st.markdown(resposta.text)
                        except Exception:
                            st.info("Invista em delegação e softwares de automação para proteger sua agenda.")
                
                else:
                    st.session_state.historico["Estratégico"] += tempo_gasto
                    st.success(f"🟢 **STATUS: ATIVIDADE ESTRATÉGICA CONFIRMADA**")
                    st.session_state.lista_atividades.append({"Atividade": tarefa, "Horas": tempo_gasto, "Tipo": "🟢 Estratégica", "Custo Oculto": "R$ 0,00"})
                    
                    with st.spinner("Gerando Relatório de Crescimento..."):
                        try:
                            prompt_diagnostico = (
                                "Você é um consultor sênior da holding ValorDe.\n"
                                "O dono fez uma atividade correta e estratégica. Gere um feedback de 3 linhas em Markdown "
                                "elogiando a visão de negócios dele e explicando como isso aumenta o Valuation da holding a longo prazo.\n"
                                f"Atividade analisada: {tarefa}"
                            )
                            resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_diagnostico)
                            st.markdown(resposta.text)
                        except Exception:
                            st.markdown("Foco excelente. Continue aplicando seu tempo no crescimento comercial.")

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

    # --- RECURSO EXTRA: TABELA DE HISTÓRICO EM TEMPO REAL ---
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
    
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("### 🥉 Plano Start\n**R$ 0,00** / Sempre Grátis\n* Análise básica de tarefas\n* Gráfico de rosca padrão")
        st.button("Plano Atual", disabled=True, key="b1")
    with p2:
        st.markdown("### 🥈 Plano Dono Pro\n**R$ 29,90** / Mês\n* **IA Gemini Avançada**\n* Relatórios mensais estruturados\n* Acesso ao Histórico Completo")
        st.button("Assinar Plano Pro", type="primary", key="b2")
    with p3:
        st.markdown("### 🥇 Plano Holding VIP\n**R$ 89,90** / Mês\n* Integração Pix automatizada\n* Consultoria de Processos com Kaleb")
        st.button("Falar com Consultor", key="b3")

if st.button("Limpar Histórico e Resetar Painel"):
    st.session_state.historico = {"Estratégico": 0.0, "Operacional (Prejuízo)": 0.0}
    st.session_state.lista_atividades = []
    st.rerun()


