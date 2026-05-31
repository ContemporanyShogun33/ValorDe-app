import streamlit as st
import matplotlib.pyplot as plt

# Configuração da página web
st.set_page_config(page_title="ValorDe - Business Intelligence", layout="wide")

if "historico" not in st.session_state:
    st.session_state.historico = {"Estratégico": 0.0, "Operacional (Prejuízo)": 0.0}

# --- PAINEL LATERAL ---
st.sidebar.title("ValorDe AI 📊")
st.sidebar.markdown("---")

faturamento = st.sidebar.number_input("Meta de Faturamento Mensal (R$):", min_value=1.0, value=15000.0)
horas_mes = st.sidebar.number_input("Horas de Trabalho por Mês:", min_value=1.0, value=160.0)
valor_hora_ideal = faturamento / horas_mes
st.sidebar.metric(label="Sua Hora Ideal Deve Valer", value=f"R$ {valor_hora_ideal:.2f}/h")

# --- PAINEL PRINCIPAL ---
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
            tarefa_e_perda_de_tempo = any(termo in tarefa.lower() for termo in termos_operacionais)

            if tarefa_e_perda_de_tempo:
                prejuizo_oculto = tempo_estimado_tarefa * valor_hora_ideal
                st.session_state.historico["Operacional (Prejuízo)"] += tempo_estimado_tarefa
                st.error(f"⚠️ **STATUS: ATIVIDADE OPERACIONAL DETECTADA**")
                st.markdown(f"🔴 **Custo de Oportunidade Desperdiçado:** R$ {prejuizo_oculto:.2f}")
            else:
                st.session_state.historico["Estratégico"] += tempo_estimado_tarefa
                st.success(f"🟢 **STATUS: ATIVIDADE ESTRATÉGICA CONFIRMADA**")

with col2:
    st.write("### Divisão do Tempo do Dono")
    estrat_val = st.session_state.historico["Estratégico"]
    operat_val = st.session_state.historico["Operacional (Prejuízo)"]
    
    fig, ax = plt.subplots(figsize=(4, 3), facecolor='#0e1117')
    ax.set_facecolor('#0e1117')
    
    if estrat_val == 0 and operat_val == 0:
        valores = [1, 1]
        labels = ['Sem dados', 'Sem dados']
        cores = ['#262730', '#31333f']
    else:
        valores = [estrat_val, operat_val]
        labels = ['Estratégico', 'Operacional']
        cores = ['#2e7d32', '#d32f2f']

    ax.pie(valores, labels=labels, colors=cores, startangle=90, textprops=dict(color="white", size=10, weight="bold"), wedgeprops=dict(width=0.4, edgecolor='#0e1117', linewidth=2))
    ax.axis('equal')
    st.pyplot(fig)

if st.button("Limpar Histórico"):
    st.session_state.historico = {"Estratégico": 0.0, "Operacional (Prejuízo)": 0.0}
    st.rerun()
