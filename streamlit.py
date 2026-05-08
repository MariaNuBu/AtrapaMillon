import streamlit as st
import time

# --- CONFIGURACIÓN GLOBAL (COMPARTIDA ENTRE TODOS) ---
@st.cache_resource
def get_global_state():
    # Diccionario para trackear el dinero de los 3 alumnos en tiempo real
    return {"Alumno 1": 1000000, "Alumno 2": 1000000, "Alumno 3": 1000000, "logs": []}

global_data = get_global_state()

# --- BASE DE DATOS DE PREGUNTAS ---
preguntas = [
    {
        "q": "¿Cuál es la característica principal de las redes de datos respecto al manejo de paquetes?",
        "ops": ["A) Retardo constante.", "B) Reserva de ancho de banda.", "C) Competición FIFO.", "D) Conmutación de circuitos."],
        "correct": 2
    },
    {
        "q": "Según Nyquist, ¿frecuencia mínima de muestreo para una señal de audio de frecuencia máxima $f_{max}$?",
        "ops": ["A) $f_{max}$", "B) $f_{max}/2$", "C) $2 \cdot f_{max}$", "D) $4 \cdot f_{max}$"],
        "correct": 2
    },
    {
        "q": "¿Qué valor decimal tiene el marcado Expedited Forwarding (EF)?",
        "ops": ["A) 34", "B) 24", "C) 0", "D) 46"],
        "correct": 3
    }
    # Añade aquí las 50 preguntas siguiendo el mismo formato
]

# --- LÓGICA DE SESIÓN INDIVIDUAL ---
query_params = st.query_params
user_name = query_params.get("user", "Espectador")

st.set_page_config(page_title=f"Money Drop - {user_name}", layout="wide")

# Título y Sidebar de Ranking
st.title(f"💸 Atrapa un Millón: {user_name}")

with st.sidebar:
    st.header("🏆 Ranking en Vivo")
    for user, money in global_data.items():
        if user != "logs":
            st.metric(label=user, value=f"${money:,}")
    if st.button("🔄 Refrescar Ranking"):
        st.rerun()

if user_name == "Espectador":
    st.warning("Accede usando el enlace personalizado (ej: ?user=Alumno 1)")
    st.stop()

# Inicializar estado del jugador
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.money = 1000000
    st.session_state.game_over = False

# --- PANTALLA DE JUEGO ---
if not st.session_state.game_over and st.session_state.step < len(preguntas):
    p = preguntas[st.session_state.step]
    
    st.subheader(f"Pregunta {st.session_state.step + 1}")
    st.info(p["q"])
    
    st.write(f"### Tu capital: **${st.session_state.money:,}**")
    
    # Inputs de apuestas
    cols = st.columns(4)
    apuestas = []
    for i, op in enumerate(p["ops"]):
        apuestas.append(cols[i].number_input(op, min_value=0, max_value=st.session_state.money, step=10000, key=f"p{st.session_state.step}o{i}"))

    total_apostado = sum(apuestas)
    vacias = apuestas.count(0)

    if st.button("¡ABRIR TRAMPILLAS!", use_container_width=True):
        if total_apostado != st.session_state.money:
            st.error(f"Debes apostar TODO. Te faltan ${st.session_state.money - total_apostado:,}")
        elif vacias < 1:
            st.error("¡REGLA! Al menos una trampilla debe quedar vacía.")
        else:
            correcta = p["correct"]
            ganado = apuestas[correcta]
            
            if ganado > 0:
                st.success(f"¡Salvado! Mantienes ${ganado:,}. La correcta era la {p['ops'][correcta]}")
                st.session_state.money = ganado
                st.session_state.step += 1
                # Actualizar el ranking global
                global_data[user_name] = ganado
                time.sleep(2)
                st.rerun()
            else:
                st.error(f"¡BOOM! Perdiste todo. La correcta era la {p['ops'][correcta]}")
                st.session_state.money = 0
                st.session_state.game_over = True
                global_data[user_name] = 0
                st.rerun()

elif st.session_state.game_over or st.session_state.money <= 0:
    st.error("💸 FIN DEL JUEGO. Te has quedado sin fondos.")
    if st.button("Reiniciar"):
        st.session_state.step = 0
        st.session_state.money = 1000000
        st.session_state.game_over = False
        global_data[user_name] = 1000000
        st.rerun()
else:
    st.balloons()
    st.success(f"¡FIN DEL EXAMEN! Puntuación final: ${st.session_state.money:,}")