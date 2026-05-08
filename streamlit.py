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
        "trapdoor_open_time": None,
        "jugadores": {
            "Iker":  {"dinero": 1190000, "apuesta": [0,0,0,0], "listo": False},
            "Roman": {"dinero": 1000000, "apuesta": [0,0,0,0], "listo": False},
            "Henry": {"dinero": 3000000, "apuesta": [0,0,0,0], "listo": False},
        }
    }

state = get_game_state()

# --- 2. PREGUNTAS (Resumidas para el código, añade las tuyas) ---
preguntas = [
#  {
#    "q": "What is a primary characteristic of data networks regarding packet handling?",
#    "ops": [
#      "A) Constant and minimum delay",
#      "B) Bandwidth reserved for each communication",
#      "C) Packages compete for available bandwidth using FIFO management",
#      "D) Switching circuits and dedicated links"
#    ],
#    "correct": 2
#  },
#  {
#    "q": "What is the main challenge for voice and video traffic when transported over converged IP networks?",
#    "ops": [
#      "A) They require variable delay to function correctly",
#      "B) They are very sensitive to delay and bandwidth variations",
#      "C) They require TCP overload for reliable delivery",
#      "D) They cannot use packet switching under any circumstances"
#    ],
#    "correct": 1
#  },
#  {
#    "q": "Why is the TCP service generally unsuitable for real-time interactive multimedia flows?",
#    "ops": [
#      "A) It reduces flow and introduces delay due to its congestion control",
#      "B) It provides no guarantees for ordered delivery",
#      "C) It is too lightweight and lacks security",
#      "D) It cannot transport voice packets over IP networks"
#    ],
#    "correct": 0
#  },
#  {
#    "q": "Which of the following best describes the requirements for interactive real-time audio/video flows (e.g., telephony)?",
#    "ops": [
#      "A) The receiver can control the sender with RTSP",
#      "B) It allows for pause and rewind with medium delay requirements",
#      "C) Sending speed equals reproduction speed with very strict delay requirements (<150 ms)",
#      "D) It relies primarily on TCP retransmissions to handle heavy losses"
#    ],
#    "correct": 2
#  },
#  {
#    "q": "According to the Nyquist theorem, what is the minimum sampling frequency required for an audio signal?",
#    "ops": [
#      "A) Equal to the maximum frequency of the signal",
#      "B) Half of the maximum frequency of the signal",
#      "C) At least twice the maximum frequency of the signal",
#      "D) Four times the maximum frequency of the signal"
#    ],
#    "correct": 2
#  },
#  {
#    "q": "How do multimedia receivers compensate for the variable transit delay (jitter) of incoming packets?",
#    "ops": [
#      "A) By requesting TCP retransmissions for delayed packets",
#      "B) By delaying reproduction using a reception buffer to recover synchronism",
#      "C) By automatically changing the codec to a lower bandwidth version",
#      "D) By using RED algorithms to drop delayed packets"
#    ],
#    "correct": 1
#  },
#  {
#    "q": "Given the command: access-list 10 permit 192.168.0.0 0.0.255.255",
#    "ops": [
#      "A) It permits all traffic destined to the 192.168.0.0 network.",
#      "B) It denies traffic from the 192.168.0.0 network.",
#      "C) It permits all traffic originating from the 192.168.0.0/16 network.",
#      "D) It applies an extended ACL to the interface."
#    ],
#    "correct": 2
#  },
#  {
#    "q": "Given the command: access-list 120 permit icmp any any echo-reply",
#    "ops": [
#      "A) It creates a standard ACL to allow all pings.",
#      "B) It permits incoming ICMP echo-reply messages from any source to any destination.",
#      "C) It drops all unreachable ICMP messages.",
#      "D) It forces the router to reply to all ICMP messages."
#    ],
#    "correct": 1
#  },
#  {
#    "q": "Given the command: ip access-group 1 out applied in interface configuration mode",
#    "ops": [
#      "A) It deletes ACL 1 from the configured interface.",
#      "B) It creates a new ACL named \"out\".",
#      "C) It applies extended ACL 1 to the incoming flow of traffic.",
#      "D) It associates standard ACL 1 to filter the outgoing flow of traffic on that interface."
#    ],
#    "correct": 3
#  },
#  {
#    "q": "Given the command: access-list 105 permit tcp host 192.168.1.10 any eq www time-range MyHours",
#    "ops": [
#      "A) It allows the host to synchronize its clock via a web server.",
#      "B) It permits TCP web traffic from host 192.168.1.10 to any destination only during the times defined in the \"MyHours\" time-range.",
#      "C) It restricts the router's uptime to the MyHours range.",
#      "D) It creates a dynamic ACL that expires after a set amount of hours."
#    ],
#    "correct": 1
#  },
#  {
#    "q": "Given the command: permit tcp 192.168.1.0 0.0.0.255 any reflect TCP_TRAFFIC",
#    "ops": [
#      "A) It forces the router to loop the traffic back to the source.",
#      "B) It reflects malicious traffic back to an attacker.",
#      "C) It examines outgoing TCP connections and generates temporary rules to accept the returning incoming traffic.",
#      "D) It creates a lock-and-key dynamic ACL named TCP_TRAFFIC."
#    ],
#    "correct": 2
#  },
#  {
#    "q": "Given the command: access-list 100 dynamic router-telnet timeout 15 permit ip 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255",
#    "ops": [
#      "A) It adds a permanent extended rule allowing traffic between the two subnets.",
#      "B) It creates a lock-and-key ACL that blocks traffic until a user authenticates in the router, then adds a temporary rule for 15 minutes.",
#      "C) It dynamically changes the router's IP address every 15 minutes.",
#      "D) It allows reflexive routing of Telnet packets for 15 users."
#    ],
#    "correct": 1
#  },
#  {
#    "q": "Given the command: show access-list",
#    "ops": [
#      "A) It displays only the interfaces that have ACLs applied to them.",
#      "B) It configures a new standard ACL directly from the terminal.",
#      "C) It displays the defined ACLs along with the number of coincidences (matches) for each rule.",
#      "D) It adds a comment to an existing ACL."
#    ],
#    "correct": 2
#  },
#  {
#    "q": "Given the operational description: \"It protects all the original Datagram fields by encapsulating them, allowing communication between intermediate systems to implement VPNs.\"",
#    "ops": [
#      "A) Transport mode",
#      "B) Tunnel mode",
#      "C) Authentication Header (AH)",
#      "D) Standard Access List"
#    ],
#    "correct": 1
#  },
#  {
#    "q": "What is the purpose of Forward Error Correction (FEC) in voice transmission?",
#    "ops": [
#      "A) It requests the sender to retransmit lost packets immediately",
#      "B) It interleaves samples to separate them in time",
#      "C) It interpolates the medium between previous and posterior samples",
#      "D) It sends redundant information to rebuild lost samples"
#    ],
#    "correct": 3
#  },
  {
    "q": "What is the primary effect of using interleaved samples for loss recovery?",
    "ops": [
      "A) It decreases the bandwidth required for transmission",
      "B) It increases the delay without increasing the bandwidth",
      "C) It completely eliminates jitter from the network",
      "D) It relies on TCP to guarantee the delivery of all samples"
    ],
    "correct": 1
  },
  {
    "q": "What is the function of the Real-Time Control Protocol (RTCP)?",
    "ops": [
      "A) It compresses the IP and UDP headers to save bandwidth",
      "B) It identifies the type of multimedia flow using time stamps",
      "C) It sends periodic control data to exchange information on the quality of the exchange",
      "D) It actively controls and guarantees the Quality of Service (QoS) on IP routers"
    ],
    "correct": 2
  },
  {
    "q": "According to the first principle of Quality of Service (QoS), what allows network elements to differentiate between packages?",
    "ops": [
      "A) Resource reservation protocols",
      "B) Call Admission Control",
      "C) Classification and marking of packages",
      "D) Traffic shaping at the destination"
    ],
    "correct": 2
  },
  {
    "q": "According to the principles of QoS, what is Call Admission Control (CAC) used for?",
    "ops": [
      "A) To guarantee bandwidth for Best-Effort traffic",
      "B) To reject a new connection if the network lacks the required resources",
      "C) To dynamically change the codec of active calls during congestion",
      "D) To classify incoming packets into DiffServ classes"
    ],
    "correct": 1
  },
  {
    "q": "Which component of transit delay is calculated by dividing the bits of the package by the link speed?",
    "ops": [
      "A) Processing delay",
      "B) Waiting delay in queues",
      "C) Propagation delay",
      "D) Transmission or serialization delay"
    ],
    "correct": 3
  },
  {
    "q": "Under what condition are software queues activated in a router?",
    "ops": [
      "A) Only during normal traffic flow",
      "B) Only when encryption is enabled",
      "C) Only when there is congestion",
      "D) They are always active regardless of traffic"
    ],
    "correct": 2
  },
  {
    "q": "Which QoS model requires flow-based treatment where each information flow receives proper treatment from all elements of the network?",
    "ops": [
      "A) Differentiated Services (DiffServ)",
      "B) Integrated Services (IntServ)",
      "C) Best-Effort",
      "D) Class-Based Weighted Fair Queuing (CBWFQ)"
    ],
    "correct": 1
  },
  {
    "q": "In the DiffServ functional model, what is the primary role of the interior or core routers?",
    "ops": [
      "A) Classification, marking, and traffic conditioning",
      "B) Executing call admission control",
      "C) Applying PHB classification and treatment",
      "D) Initiating the RSVP signaling process"
    ],
    "correct": 2
  },
  {
    "q": "In a Token-Bucket traffic conditioning mechanism, what does 'policing' refer to?",
    "ops": [
      "A) Delaying packets in a buffer until tokens are available",
      "B) Discarding the packet when tokens are not available",
      "C) Automatically upgrading the packet's priority",
      "D) Re-routing the packet to a less congested path"
    ],
    "correct": 1
  },
  {
    "q": "What is a major disadvantage of using Priority Queuing (PQ) for traffic scheduling?",
    "ops": [
      "A) It requires complex RSVP signaling",
      "B) It limits the bandwidth of the highest priority queue",
      "C) It can cause starving of lower priority queues",
      "D) It processes all queues equally in a round-robin fashion"
    ],
    "correct": 2
  },
  {
    "q": "Which queuing algorithm dynamically creates queues for each traffic flow and prioritizes light traffic over heavy traffic?",
    "ops": [
      "A) Custom Queuing (CQ)",
      "B) Priority Queuing (PQ)",
      "C) Weighted Fair Queuing (WFQ)",
      "D) First In, First Out (FIFO)"
    ],
    "correct": 2
  },
  {
    "q": "What is the Low Latency Queuing (LLQ) algorithm composed of?",
    "ops": [
      "A) A combination of FIFO and CQ",
      "B) A combination of CBWFQ and PQ",
      "C) A combination of WFQ and RED",
      "D) A single strict priority queue for all traffic"
    ],
    "correct": 1
  },
  {
    "q": "What is the main advantage of the Random Early Detection (RED) mechanism over standard tail drop?",
    "ops": [
      "A) It ensures that UDP packets are never dropped",
      "B) It increases the maximum size of the queue infinitely",
      "C) Discards affect fewer TCP connections simultaneously and bandwidth is better used",
      "D) It guarantees zero latency for all multimedia traffic"
    ],
    "correct": 2
  },
  {
    "q": "What is the purpose of Link Fragmentation and Interleaving (LFI)?",
    "ops": [
      "A) To compress the headers of RTP packets on slow links",
      "B) To prevent intensive data traffic in large packages from increasing the delay of priority packages",
      "C) To dynamically change the DSCP marking of fragmented packets",
      "D) To encrypt data packets before serialization"
    ],
    "correct": 1
  },
  {
    "q": "Which protocol is used in the Integrated Services (IntServ) model to request a certain QoS and exchange this information along the route?",
    "ops": [
      "A) SIP",
      "B) RTCP",
      "C) MGCP",
      "D) RSVP"
    ],
    "correct": 3
  },
  {
    "q": "What is the first step in the Cisco MQC (Modular QoS CLI) configuration process?",
    "ops": [
      "A) Applying the policy to an interface",
      "B) Defining a traffic policy (policy-map)",
      "C) Creating a traffic class (class-map)",
      "D) Configuring RSVP signaling"
    ],
    "correct": 2
  },
  {
    "q": "When configuring a class-map, what does the 'match-all' parameter dictate?",
    "ops": [
      "A) Any packet automatically matches the class",
      "B) A packet must fulfill all the listed matching criteria to belong to the class",
      "C) A packet must fulfill at least one of the listed criteria to belong to the class",
      "D) All interfaces will apply this classification rule"
    ],
    "correct": 1
  },
  {
    "q": "How does the 'shape' command differ from the 'police' command in MQC?",
    "ops": [
      "A) 'shape' drops excess traffic immediately, while 'police' queues it",
      "B) 'shape' forms traffic by delaying flows to adapt them to a profile, rather than immediately dropping them",
      "C) 'shape' only applies to inbound traffic",
      "D) 'shape' assigns strict priority to voice traffic"
    ],
    "correct": 1
  },
  {
    "q": "What is the primary function of a Voice Gateway in a VoIP network?",
    "ops": [
      "A) To act as an interface and perform analog-to-digital conversion",
      "B) To register IP phones and manage admission control",
      "C) To establish multiconferences between three or more participants",
      "D) To route traditional IP data traffic to the internet"
    ],
    "correct": 0
  },
  {
    "q": "In VoIP networks, what is the role of a Call Agent or Media Gateway Controller (MGC)?",
    "ops": [
      "A) It performs the analog-to-digital conversion",
      "B) It controls the service of one or more gateways, facilitating centralized administration",
      "C) It provides the physical FXS ports for analog phones",
      "D) It strictly routes data packets over the IP network"
    ],
    "correct": 1
  },
  {
    "q": "What does an FXS (Foreign Exchange Station) port provide?",
    "ops": [
      "A) A connection to a digital E1 trunk",
      "B) Power and signaling to connect standard analog telephone terminals",
      "C) A gateway control connection to an MGC",
      "D) A connection to the public switched telephone network acting as a client"
    ],
    "correct": 1
  },
  {
    "q": "Which of the following is a master-slave protocol used for gateway control where the intelligence resides on the Call Agent?",
    "ops": [
      "A) SIP",
      "B) H.323",
      "C) MGCP",
      "D) RTP"
    ],
    "correct": 2
  },
  {
    "q": "How does the proprietary Cisco SCCP (Skinny) protocol manage terminal interactions?",
    "ops": [
      "A) It establishes full peer-to-peer sessions between terminals",
      "B) It sends a message for every single user action, such as picking up or pressing a digit",
      "C) It relies on SIP Proxy servers to route its text-based messages",
      "D) It only communicates during the initial call setup and leaves the rest to the gateway"
    ],
    "correct": 1
  },
  {
    "q": "What is the primary purpose of the Session Description Protocol (SDP)?",
    "ops": [
      "A) To transport voice samples across the IP network",
      "B) To reserve network bandwidth along a routing path",
      "C) To allow interlocutors to exchange data on the nature and characteristics of the multimedia session",
      "D) To provide physical analog-to-digital voice conversion"
    ],
    "correct": 2
  },
  {
    "q": "What type of messages are used in H.323 for automatic Gatekeeper discovery and endpoint registration?",
    "ops": [
      "A) SIP INVITE and ACK",
      "B) RAS (Registration, Admission, and Status)",
      "C) RSVP PATH and RESV",
      "D) RTCP Sender Reports"
    ],
    "correct": 1
  },
  {
    "q": "In the SIP architecture, what is the role of a Proxy Server?",
    "ops": [
      "A) To physically convert voice signals to data packets",
      "B) To act as a mediator, forwarding connection requests to another server",
      "C) To maintain the location database of all clients",
      "D) To redirect requests directly back to the client to find another domain"
    ],
    "correct": 1
  },
  {
    "q": "Which SIP method is used to initiate a session or reservoir request?",
    "ops": [
      "A) OPTIONS",
      "B) ACK",
      "C) REGISTER",
      "D) INVITE"
    ],
    "correct": 3
  },
  {
    "q": "Which SIP method is used by a User Agent to notify the Location Server of its current IP address?",
    "ops": [
      "A) SUBSCRIBE",
      "B) REGISTER",
      "C) INFO",
      "D) INVITE"
    ],
    "correct": 1
  },
  {
    "q": "What distinguishes SIP's encoding format from H.323's call control encoding?",
    "ops": [
      "A) SIP uses binary ASN.1 encoding, while H.323 uses text",
      "B) SIP uses text, while H.323 uses Abstract Syntax Notation One (ASN.1) basic encoding rules",
      "C) SIP relies solely on XML, while H.323 uses JSON",
      "D) Both protocols use identical binary encoding"
    ],
    "correct": 1
  },
  {
    "q": "Which of the following best describes SIP Forking?",
    "ops": [
      "A) Fragmenting a large data packet to let voice pass",
      "B) Sending an INVITE simultaneously to multiple known IP addresses for a single user",
      "C) Changing the codec dynamically mid-call",
      "D) Dropping low-priority packets during congestion"
    ],
    "correct": 1
  }
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
        if datos["listo"]: cols[i].success("✅ Bet fixed")
        else: cols[i].warning("⏳ Thinking...")

    st.divider()

    idx = state["pregunta_idx"]
    if idx < len(preguntas):
        p = preguntas[idx]
        st.write(p['q'])
        st.success(f"**Correct Answer:** {p['ops'][p['correct']]}")
    else:
        st.success("All questions completed!")

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
        state["trapdoor_open_time"] = datetime.now()
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
        state["trapdoor_open_time"] = datetime.now()

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
            if st.button("CONFIRM ANSWER"):
                if sum(apuestas) != state["jugadores"][user]["dinero"]:
                    st.error("You must bet all your capital.")
                elif apuestas.count(0) < 1:
                    st.error("You must leave at least one trapdoor empty.")
                else:
                    state["jugadores"][user]["apuesta"] = apuestas
                    state["jugadores"][user]["listo"] = True
                    st.rerun()

        # AUTO-SAVE BETS SI EL TIEMPO EXPIRÓ O EL PROFESOR CORTÓ
        if state["trapdoor_open"] and not state["jugadores"][user]["listo"]:
            current_bets = [st.session_state.get(f"q{idx}u{user}o{k}", 0) for k in range(4)]
            state["jugadores"][user]["apuesta"] = current_bets
            state["jugadores"][user]["listo"] = True

        # RESOLUCIÓN AUTOMÁTICA (Cuando el profesor abre trampillas)
        if state["trapdoor_open"]:
            st.divider()
            correcta = p["correct"]
            dinero_salvado = state["jugadores"][user]["apuesta"][correcta]
            
            if state["fase"] == "resultados":
                state["jugadores"][user]["dinero"] = dinero_salvado

    # Auto-refresh cada segundo para ver el timer y las órdenes del prof
    time.sleep(1)
    st.rerun()

else:
    st.warning("Por favor, usa un enlace válido con ?user=Iker, Roman, Henry")