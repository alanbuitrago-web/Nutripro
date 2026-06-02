import streamlit as st
import plotly.graph_objects as go

# --------------------------------
# CONFIGURACIÓN DE PÁGINA
# --------------------------------

st.set_page_config(
    page_title="NutriPro - Evaluación Física",
    page_icon="🥗",
    layout="wide"
)

# --------------------------------
# ESTILOS CSS
# --------------------------------

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.titulo {
    text-align: center;
    color: #2E8B57;
    font-size: 40px;
    font-weight: bold;
}

.subtitulo {
    text-align: center;
    color: gray;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# TÍTULO
# --------------------------------

st.markdown('<p class="titulo">🥗 NutriPro</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitulo">Sistema Inteligente de Evaluación Física y Nutricional</p>',
    unsafe_allow_html=True
)

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.header("📋 Ingresa tus datos")

nombre = st.sidebar.text_input("Nombre")

edad = st.sidebar.number_input(
    "Edad",
    min_value=10,
    max_value=100,
    value=18
)

sexo = st.sidebar.selectbox(
    "Sexo",
    ["Masculino", "Femenino"]
)

peso = st.sidebar.number_input(
    "Peso (kg)",
    min_value=30.0,
    max_value=200.0,
    value=70.0
)

altura = st.sidebar.number_input(
    "Altura (m)",
    min_value=1.0,
    max_value=2.5,
    value=1.70
)

actividad = st.sidebar.selectbox(
    "Nivel de actividad física",
    ["Sedentario", "Ligero", "Moderado", "Activo"]
)

objetivo = st.sidebar.selectbox(
    "Objetivo",
    ["Bajar de peso", "Mantener peso", "Ganar masa muscular"]
)

evaluar = st.sidebar.button("Evaluar mi estado")

# --------------------------------
# FUNCIONES
# --------------------------------

def clasificacion_imc(imc):
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"


def calcular_calorias(sexo, peso, altura, edad, actividad):

    if sexo == "Masculino":
        tmb = 88.36 + (13.4 * peso) + (4.8 * altura * 100) - (5.7 * edad)
    else:
        tmb = 447.6 + (9.2 * peso) + (3.1 * altura * 100) - (4.3 * edad)

    factores = {
        "Sedentario": 1.2,
        "Ligero": 1.375,
        "Moderado": 1.55,
        "Activo": 1.725
    }

    return tmb * factores[actividad]


def recetas_por_objetivo(objetivo):

    recetas = {
        "Bajar de peso": {
            "🍳 Desayuno":
                "Yogur griego con avena y frutas.",
            "🍛 Almuerzo":
                "Pollo a la plancha con arroz integral y ensalada.",
            "🥗 Cena":
                "Ensalada de atún con vegetales."
        },

        "Mantener peso": {
            "🍳 Desayuno":
                "Huevos revueltos con pan integral y fruta.",
            "🍛 Almuerzo":
                "Pechuga de pollo con quinoa y verduras.",
            "🥗 Cena":
                "Sopa de verduras con proteína ligera."
        },

        "Ganar masa muscular": {
            "🍳 Desayuno":
                "Avena con banano, mantequilla de maní y leche.",
            "🍛 Almuerzo":
                "Arroz, pollo, aguacate y vegetales.",
            "🥗 Cena":
                "Pasta integral con proteína magra."
        }
    }

    return recetas[objetivo]


# --------------------------------
# RESULTADOS
# --------------------------------

if evaluar:

    imc = peso / (altura ** 2)
    categoria = clasificacion_imc(imc)

    calorias = calcular_calorias(
        sexo,
        peso,
        altura,
        edad,
        actividad
    )

    # Ajuste según objetivo
    if objetivo == "Bajar de peso":
        calorias -= 300
    elif objetivo == "Ganar masa muscular":
        calorias += 300

    st.success(f"Hola {nombre} 👋")

    col1, col2, col3 = st.columns(3)

    col1.metric("⚖️ IMC", round(imc, 2))
    col2.metric("📌 Clasificación", categoria)
    col3.metric("🔥 Calorías/día", f"{round(calorias)} kcal")

    st.divider()

    # --------------------------------
    # GRÁFICA IMC
    # --------------------------------

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=imc,
        title={'text': "Tu IMC"},
        gauge={
            'axis': {'range': [0, 40]},
            'steps': [
                {'range': [0, 18.5], 'color': "lightblue"},
                {'range': [18.5, 25], 'color': "lightgreen"},
                {'range': [25, 30], 'color': "orange"},
                {'range': [30, 40], 'color': "red"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------
    # RECETAS
    # --------------------------------

    st.subheader("🍽️ Plan de recetas sugeridas para hoy")

    recetas = recetas_por_objetivo(objetivo)

    c1, c2, c3 = st.columns(3)

    comidas = list(recetas.items())

    with c1:
        st.info(comidas[0][0])
        st.write(comidas[0][1])

    with c2:
        st.info(comidas[1][0])
        st.write(comidas[1][1])

    with c3:
        st.info(comidas[2][0])
        st.write(comidas[2][1])

    st.divider()

    st.caption(
        "Las recomendaciones son orientativas y no sustituyen orientación profesional."
    )

else:
    st.info("👈 Completa tus datos en el panel lateral y presiona 'Evaluar mi estado'")