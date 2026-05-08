import streamlit as st
import time
from datetime import datetime, timedelta

# --- 1. ESTADO GLOBAL COMPARTIDO ---
@st.cache_resource
def get_game_state():
    return {
        "fase": "espera", # espera, apostando, resultados
        "pregunta_idx": 0,
        "limite_tiempo": None,
        "trapdoor_open": False,
        "jugadores": {
            "Iker":  {"dinero": 1000000, "apuesta": [0,0,0,0], "listo": False},
            "Roman": {"dinero": 1000000, "apuesta": [0,0,0,0], "listo": False},
            "Henry": {"dinero": 1000000, "apuesta": [0,0,0,0], "listo": False},
        }
    }

state = get_game_state()

# --- 2. PREGUNTAS (Resumidas para el código, añade las tuyas) ---
preguntas = [
    {"q": "¿Característica de redes de datos?", "ops": ["A) Retardo constante", "B) Reserva BW", "C) FIFO / Competición", "D) Circuitos"], "correct": 2},
    {"q": "¿Nyquist: Frecuencia mínima?", "ops": ["A) $f_{max}$", "B) $f_{max}/2$", "C) $2 \cdot f_{max}$", "D) $4 \cdot f_{max}$"], "correct": 2},
    {"q": "¿Marcado EF (Expedited Forwarding)?", "ops": ["A) 34", "B) 24", "C) 0", "D) 46"], "correct": 3},
]

# --- 3. IDENTIFICACIÓN POR URL ---
user = st.query_params.get("user", "Espectador")
st.set_page_config(page_title=f"Money Drop - {user}", layout="wide")

# --- 4. VISTA DEL PROFESOR (Panel de Control) ---
if user == "Profesor":
    st.title("👨‍🏫 Panel de Control del Profesor")
    
    # RANKING EN GRANDE
    cols = st.columns(3)
    for i, (nom, datos) in enumerate(state["jugadores"].items()):
        cols[i].metric(label=nom, value=f"${datos['dinero']:,}", delta=None)
        if datos["listo"]: cols[i].success("✅ Apuesta fijada")
        else: cols[i].warning("⏳ Pensando...")

    st.divider()

    # CONTROLES DE FLUJO
    c1, c2, c3 = st.columns(3)
    if c1.button("🚀 Start question (60s)"):
        state["fase"] = "apostando"
        state["limite_tiempo"] = datetime.now() + timedelta(seconds=60)
        state["trapdoor_open"] = False
        for n in state["jugadores"]: state["jugadores"][n]["listo"] = False
        st.rerun()

    if c2.button("💥 Open trapdoors (Manual cut)"):
        state["trapdoor_open"] = True
        state["fase"] = "resultados"
        st.rerun()

    if c3.button("➡️ Next question"):
        state["pregunta_idx"] += 1
        state["fase"] = "espera"
        st.rerun()
    
    if st.button("Reset Game"):
        get_game_state.clear()
        st.rerun()

    time.sleep(1) # Auto-refresh para el ranking
    st.rerun()

# --- 5. VISTA DEL ALUMNO ---
elif user in state["jugadores"]:
    st.title(f"💰 {user}")
    
    # Comprobar si el tiempo ha expirado
    if state["fase"] == "apostando" and datetime.now() > state["limite_tiempo"]:
        state["trapdoor_open"] = True
        state["fase"] = "resultados"

    # MOSTRAR PREGUNTA
    idx = state["pregunta_idx"]
    if idx >= len(preguntas):
        st.success("¡You survived!")
        st.stop()

    p = preguntas[idx]
    
    # HEADER: Dinero y Tiempo
    h1, h2 = st.columns(2)
    h1.header(f"Capital: ${state['jugadores'][user]['dinero']:,}")
    
    if state["fase"] == "apostando":
        restante = int((state["limite_tiempo"] - datetime.now()).total_seconds())
        h2.header(f"⏱️ Time: {max(0, restante)}s")
    else:
        h2.header("⏱️ TIME EXPIRED" if state["fase"] == "resultados" else "Waiting for the professor...")

    if state["fase"] != "espera":
        st.info(f"**QUESTION {idx+1}:** {p['q']}")

        # INTERFAZ DE APUESTA
        apuestas = [0,0,0,0]
        cols_ops = st.columns(4)
        
        def set_bet(trap_idx, fraction):
            total = state["jugadores"][user]["dinero"]
            other_bets = sum(st.session_state.get(f"q{idx}u{user}o{j}", 0) for j in range(4) if j != trap_idx)
            left = max(0, total - other_bets)
            st.session_state[f"q{idx}u{user}o{trap_idx}"] = int(round(left * fraction / 10000.0) * 10000)

        for i in range(4):
            with cols_ops[i]:
                # Deshabilitar si se abren trampillas o ya está listo
                disabled = state["trapdoor_open"] or state["jugadores"][user]["listo"]
                apuestas[i] = st.number_input(
                    p["ops"][i], 
                    min_value=0, 
                    max_value=state["jugadores"][user]["dinero"], 
                    step=10000, 
                    key=f"q{idx}u{user}o{i}",
                    disabled=disabled
                )

                if not disabled:
                    b1, b2 = st.columns(2)
                    b1.button("All", key=f"b_all_{idx}_{i}", on_click=set_bet, args=(i, 1.0), use_container_width=True)
                    b2.button("1/2", key=f"b_half_{idx}_{i}", on_click=set_bet, args=(i, 0.5), use_container_width=True)
                    b3, b4 = st.columns(2)
                    b3.button("1/4", key=f"b_14_{idx}_{i}", on_click=set_bet, args=(i, 0.25), use_container_width=True)
                    b4.button("3/4", key=f"b_34_{idx}_{i}", on_click=set_bet, args=(i, 0.75), use_container_width=True)

        # BOTÓN PARA CONFIRMAR
        if not state["jugadores"][user]["listo"] and state["fase"] == "apostando":
            if st.button("CONFIRMAR APUESTA"):
                if sum(apuestas) != state["jugadores"][user]["dinero"]:
                    st.error("Debes apostar todo tu capital.")
                elif apuestas.count(0) < 1:
                    st.error("Debes dejar al menos una trampilla vacía.")
                else:
                    state["jugadores"][user]["apuesta"] = apuestas
                    state["jugadores"][user]["listo"] = True
                    st.rerun()

        # RESOLUCIÓN AUTOMÁTICA (Cuando el profesor abre trampillas)
        if state["trapdoor_open"]:
            st.divider()
            correcta = p["correct"]
            dinero_salvado = state["jugadores"][user]["apuesta"][correcta]
            
            if dinero_salvado > 0:
                st.success(f"¡THE TRAPDOOR {p['ops'][correcta]} STAYED CLOSED! You saved ${dinero_salvado:,}")
                # Solo actualizamos el capital una vez al abrir
                if state["fase"] == "resultados":
                    state["jugadores"][user]["dinero"] = dinero_salvado
            else:
                st.error(f"¡BOOM! The money has fallen. The correct one was: {p['ops'][correcta]}")
                state["jugadores"][user]["dinero"] = 0

    # Auto-refresh cada segundo para ver el timer y las órdenes del prof
    time.sleep(1)
    st.rerun()

else:
    st.warning("Por favor, usa un enlace válido con ?user=Iker, Roman, Henry")