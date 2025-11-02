import streamlit as st
import random
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyttsx3

# ----------------------- Voice Alert Setup -----------------------
engine = pyttsx3.init()
engine.setProperty('rate', 165)
engine.setProperty('volume', 0.9)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

# ----------------------- UI Setup -----------------------
st.set_page_config(page_title="AI Red Teamer", page_icon="🧠", layout="wide")

st.title("🧠 AI Red Teamer – Autonomous Attack Simulation Framework")
st.caption("AI-powered Cyber Attack Emulator for Red-Team & Blue-Team Training (Safe Offline Demo)")
st.divider()

# ----------------------- Simulation Settings -----------------------
st.sidebar.header("⚙️ Simulation Controls")

simulation_speed = st.sidebar.slider("Simulation Speed", 0.2, 2.0, 1.0, 0.1)
num_phases = st.sidebar.slider("Attack Phases", 3, 10, 5)
defense_sensitivity = st.sidebar.slider("Blue Team Sensitivity", 0.1, 1.0, 0.6)
enable_voice = st.sidebar.checkbox("Enable Voice Alerts", True)

st.sidebar.write("---")
if st.sidebar.button("🚀 Start AI Red Team Simulation"):
    st.session_state["run_sim"] = True
    st.rerun()

if st.sidebar.button("🧹 Reset"):
    st.session_state.clear()
    st.rerun()

# ----------------------- Initialize Session -----------------------
if "run_sim" not in st.session_state:
    st.session_state["run_sim"] = False
if "attack_logs" not in st.session_state:
    st.session_state["attack_logs"] = []
if "attack_scores" not in st.session_state:
    st.session_state["attack_scores"] = []
if "defense_reactions" not in st.session_state:
    st.session_state["defense_reactions"] = []

# ----------------------- Attack & Defense Logic -----------------------
attack_phases = [
    "Reconnaissance",
    "Phishing Attempt",
    "Initial Access",
    "Privilege Escalation",
    "Lateral Movement",
    "Data Exfiltration",
    "Cover Tracks"
]

def run_simulation():
    for i in range(num_phases):
        phase = random.choice(attack_phases)
        risk_score = random.uniform(0.3, 1.0)
        detection = random.random() < defense_sensitivity
        defense_strength = round(random.uniform(0.3, 1.0), 2)
        timestamp = time.strftime("%H:%M:%S")

        log = {
            "Time": timestamp,
            "Phase": phase,
            "RiskScore": round(risk_score, 2),
            "Detected": "✅" if detection else "❌",
            "DefenseStrength": defense_strength
        }
        st.session_state["attack_logs"].append(log)
        st.session_state["attack_scores"].append(risk_score)
        st.session_state["defense_reactions"].append(defense_strength)

        with st.container():
            st.write(f"🕒 **{timestamp}** | Phase: **{phase}** | Risk Score: `{risk_score:.2f}` | Detection: {'🛡️ Blocked' if detection else '⚠️ Missed'}")
            if enable_voice and detection:
                speak(f"Defense triggered during {phase} phase. Threat neutralized.")
            elif enable_voice and not detection:
                speak(f"Warning! Undetected behavior during {phase} phase.")
            time.sleep(simulation_speed)

# ----------------------- Simulation Execution -----------------------
if st.session_state["run_sim"]:
    st.success("🔴 Simulation Running...")
    run_simulation()
    st.session_state["run_sim"] = False

# ----------------------- Dashboard Analytics -----------------------
if len(st.session_state["attack_logs"]) > 0:
    st.subheader("📊 Attack vs Defense Analytics")

    df = pd.DataFrame(st.session_state["attack_logs"])

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        ax.plot(df["RiskScore"], label="Attack Risk", marker='o')
        ax.plot(df["DefenseStrength"], label="Defense Strength", marker='x')
        ax.set_title("Attack vs Defense Strength")
        ax.legend()
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        defense_rate = sum(df["Detected"] == "✅") / len(df)
        ax.bar(["Detected", "Missed"], [defense_rate, 1 - defense_rate])
        ax.set_title("Detection Efficiency")
        st.pyplot(fig)

    st.dataframe(df, use_container_width=True)
else:
    st.info("🕹️ Click **Start Simulation** from sidebar to begin attack simulation.")

# ----------------------- Footer -----------------------
st.markdown("---")
st.markdown("🔐 **AI Red Teamer** | Ethical AI Cyber Range | Created by **Mukesh Kanna** 🧠")
st.caption("This project is for cybersecurity education and simulation only – no real attacks are executed.")
