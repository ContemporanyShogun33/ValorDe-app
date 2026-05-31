import streamlit as st
import matplotlib.pyplot as plt
from google import genai

# Configuração da página web
st.set_page_config(page_title="ValorDe AI - Business Intelligence", layout="wide")

# --- CONEXÃO COM O GEMINI ---
# Coloque sua chave do Google AI Studio entre as aspas abaixo
CHAVE_GEMINI = "SUA_CHAVE_GEMINI_AQUI"
try:
    client = genai.Client(api_key=CHAVE_GEMINI)
except Exception:
    client = None

if "historico" not in st.session_state:
    st.session_state.historico = {"Estratégico": 0.0, "Operacional (Prejuízo)": 0.0}

# --- 📐 PAINEL LATERAL ESQUERDO ---
st.sidebar.title("ValorDe AI 📊")
st.sidebar.caption("Desenvolvido por Kaleb Machado")
st.sidebar.markdown("---")

# 1. Configurações Financeiras
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
tab1, tab2 = st.tabs(["📊 Documentador Diário", "💎 Planos Mensais"])

with tab1:
    st.title("Documentador de Atividades Diárias")
    st.subheader("Monitore a fuga de valor estratégico da sua holding")

    tarefa = st.text_input(label="Atividade Executada", placeholder="Digite aqui o que você executou hoje na empresa...")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Analisar Impacto Financeiro", type="primary"):
            if not tarefa:
                st.warning("Por favor, descreva a atividade antes de analisar.")
            elif not client:
                st.error("Por favor, configure sua chave do Gemini para usar a inteligência do app.")
            else:
                tempo_estimado_tarefa = 2.0
                
                # --- INTELIGÊNCIA ARTIFICIAL: CAMADA 1 (CLASSIFICAÇÃO DINÂMICA) ---
                with st.spinner("Analisando atividade estrategicamente..."):
                    try:
                        prompt_classificacao = (
                            "Você é o motor de classificação do aplicativo ValorDe.\n"
                            "Analise a atividade de um microempresário e responda APENAS com uma palavra:\n"
                            "Responda 'OPERACIONAL' se for uma tarefa braçal, administrativa simples, limpeza, entrega, ou despesa pessoal.\n"
                            "Responda 'ESTRATEGICO' se for uma tarefa de vendas, expansão, parcerias, marketing ou planejamento.\n"
                            f"Atividade: {tarefa}"
                        )
                        res_classe = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt_classificacao
                        )
                        classe_final = res_classe.text.strip().upper()
                    except Exception:
                        classe_final = "OPERACIONAL" # Caso falhe, mantém a segurança padrão

                # Processamento com base na resposta da IA usando o operador 'is'
                if "OPERACIONAL" in classe_final:
                    prejuizo_oculto = tempo_estimado_tarefa * valor_hora_ideal
                    st.session_state.historico["Operacional (Prejuízo)"] += tempo_estimado_tarefa
                    st.error(f"⚠️ **STATUS: ATIVIDADE OPERACIONAL DETECTADA**")
                    st.markdown(f"🔴 **Custo de Oportunidade Desperdiçado:** R$ {prejuizo_oculto:.2f}")
                    
                    # --- INTELIGÊNCIA ARTIFICIAL: CAMADA 2 (DIAGNÓSTICO PERSONALIZADO) ---
                    try:
                        prompt_sistema = "Você é o consultor do ValorDe. Dê uma dica curta de até 2 linhas de como delegar ou automatizar essa tarefa específica."
                        resposta = client.models.generate_content(model='gemini-2.5-flash', contents=f"{prompt_sistema}\n\nTarefa: {tarefa}")
                        st.info(f"💡 **Conselho do ValorDe IA:** {resposta.text}")
                    except Exception:
                        st.info("💡 **Conselho do ValorDe:** Terceirize essa função para focar na estratégia!")
                else:
                    st.session_state.historico["Estratégico"] += tempo_estimado_tarefa
                    st.success(f"🟢 **STATUS: ATIVIDADE ESTRATÉGICA CONFIRMADA**")
                    st.markdown("Você agiu com foco no Valuation e crescimento do seu ecossistema.")

    with col2:
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

with tab2:
    st.title("💎 Nossos Planos - Seja Membro da Holding")
    st.write("Escolha o plano ideal para blindar o tempo da sua empresa e aumentar seus lucros.")
    
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("### 🥉 Plano Start\n**R$ 0,00** / Sempre Grátis\n* Análise básica de tarefas\n* Gráfico de rosca padrão")
        st.button("Plano Actual", disabled=True, key="b1")
    with p2:
        st.markdown("### 🥈 Plano Dono Pro\n**R$ 29,90** / Mês\n* **IA Gemini Avançada**\n* Relatórios mensais")
        st.button("Assinar Plano Pro", type="primary", key="b2")
    with p3:
        st.markdown("### 🥇 Plano Holding VIP\n**R$ 89,90** / Mês\n* Integração Pix automatizada")
        st.button("Falar com Consultor", key="b3")

if st.button("Limpar Histórico"):
    st.session_state.historico = {"Estratégico": 0.0, "Operacional (Prejuízo)": 0.0}
    st.rerun()

