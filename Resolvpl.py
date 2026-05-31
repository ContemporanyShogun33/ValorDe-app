import streamlit as st
import matplotlib.pyplot as plt
from google import genai

# Configuração da página web
st.set_page_config(page_title="ValorDe - Business Intelligence", layout="wide")

# --- CONEXÃO COM O GEMINI ---
# DICA: Para segurança total, substitua pelas aspas com a sua chave real do AI Studio do Google
CHAVE_GEMINI = "SUA_CHAVE_GEMINI_AQUI"

try:
    client = genai.Client(api_key=CHAVE_GEMINI)
except Exception:
    client = None

# Inicializa o histórico de tempo na sessão do navegador
if "historico" not in st.session_state:
    st.session_state.historico = {"Estratégico": 0.0, "Operacional (Prejuízo)": 0.0}

# --- 📐 PAINEL LATERAL ESQUERDO ---
st.sidebar.title("ValorDe AI 📊")
st.sidebar.markdown("---")

# 1. Configurações Financeiras
faturamento = st.sidebar.number_input("Meta de Faturamento Mensal (R$):", min_value=1.0, value=15000.0)
horas_mes = st.sidebar.number_input("Horas de Trabalho por Mês:", min_value=1.0, value=160.0)
valor_hora_ideal = faturamento / horas_mes
st.sidebar.metric(label="Sua Hora Ideal Deve Valer", value=f"R$ {valor_hora_ideal:.2f}/h")

st.sidebar.markdown("---")

# 2. SEÇÃO DE DOAÇÃO (PIX)
st.sidebar.subheader("Apoie o Projeto ☕")
st.sidebar.caption("Se este software ajudou sua holding a poupar tempo e dinheiro, contribua com qualquer valor para mantermos o servidor online!")
# Substitua o texto abaixo pela sua chave Pix real (pode ser e-mail, celular ou chave aleatória)
st.sidebar.code("suachavepix@email.com", language="text")
st.sidebar.markdown("<small>⚡ *Copie a chave Pix acima no app do seu banco*</small>", unsafe_allow_html=True)

st.sidebar.markdown("---")

# 3. ESPAÇO DA FÉ (SALMO 23)
st.sidebar.subheader("Momento de Fé 🙏")
st.sidebar.info("""
**Salmo 23:1**  
"O Senhor é o meu pastor, nada me faltará."
""")

# --- 📊 PAINEL PRINCIPAL DIREITO ---
st.title("Documentador de Atividades Diárias")
st.subheader("Monitore a fuga de valor estratégico da sua holding")

tarefa = st.text_input(label="Atividade Executada", placeholder="Digite aqui o que você executou hoje na empresa...")

col1, col2 = st.columns(2)

with col1:
    if st.button("Analisar Impacto Financeiro", type="primary"):
        if not tarefa:
            st.warning("Por favor, descreva a atividade antes de analisar.")
        else:
            tempo_estimado_tarefa = 2.0
            termos_operacionais = ["limpar", "limpando", "poeira", "organizar", "entregar", "empacotar", "lavar", "caixa", "banco", "correio", "ajuda", "reais", "ações"]
            
            # Operador 'in' varrendo os termos
            tarefa_e_perda_de_tempo = any(termo in tarefa.lower() for termo in termos_operacionais)

            if tarefa_e_perda_de_tempo is True:
                prejuizo_oculto = tempo_estimado_tarefa * valor_hora_ideal
                st.session_state.historico["Operacional (Prejuízo)"] += tempo_estimado_tarefa
                st.error(f"⚠️ **STATUS: ATIVIDADE OPERACIONAL DETECTADA**")
                st.markdown(f"🔴 **Custo de Oportunidade Desperdiçado:** R$ {prejuizo_oculto:.2f}")
                
                # Chamada inteligente para a IA do Gemini
                if client:
                    try:
                        prompt_sistema = (
                            "Você é o consultor de eficiência do aplicativo ValorDe.\n"
                            "O usuário perdeu tempo com uma tarefa operacional.\n"
                            "Dê uma sugestão prática de no máximo 2 linhas de como terceirizar ou automatizar isso gastando pouco."
                        )
                        resposta = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=f"{prompt_sistema}\n\nTarefa: {tarefa}"
                        )
                        st.info(f"💡 **Conselho do ValorDe IA:** {resposta.text}")
                    except Exception:
                        st.info("💡 **Conselho do ValorDe:** Terceirize essa função operacional para focar na estratégia!")
                else:
                    st.info("💡 **Conselho do ValorDe:** Invista em automação para não queimar seu tempo estratégico.")
            else:
                st.session_state.historico["Estratégico"] += tempo_estimado_tarefa
                st.success(f"🟢 **STATUS: ATIVIDADE ESTRATÉGICA CONFIRMADA**")
                st.markdown("Você agiu com foco no Valuation do seu ecossistema.")

with col2:
    st.write("### Divisão do Tempo do Dono")
    estrat_val = st.session_state.historico["Estratégico"]
    operat_val = st.session_state.historico["Operacional (Prejuízo)"]
    
    fig, ax = plt.subplots(figsize=(4, 3), facecolor='#0e1117')
    ax.set_facecolor('#0e1117')
    
    if estrat_val == 0 and operat_val == 0:
        valores = [1]
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

if st.button("Limpar Histórico"):
    st.session_state.historico = {"Estratégico": 0.0, "Operacional (Prejuízo)": 0.0}
    st.rerun()
