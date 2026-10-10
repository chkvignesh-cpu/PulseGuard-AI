import streamlit
import random
import time

streamlit.set_page_config(page_title="PulseGuard AI Prototype", layout="wide")

# -- 1. Triage Logic Engine --
def get_triage_color(spo2, hr, bp_sys, bp_dia):
    """Evaluates vitals against standard clinical thresholds and returns hex colors."""
    # SpO2 Logic
    if spo2 < 90:
        spo2_status = "#ff4b4b" # Red (Critical)
    elif 90 <= spo2 <= 94:
        spo2_status = "#ffa421" # Yellow (Warning)
    else:
        spo2_status = "#21c354" # Green (Normal)
        
    # Heart Rate Logic
    if hr < 50 or hr >= 120:
        hr_status = "#ff4b4b"
    elif (50 <= hr <= 59) or (101 <= hr <= 119):
        hr_status = "#ffa421"
    else:
        hr_status = "#21c354"
        
    # Blood Pressure Logic
    if bp_sys >= 180 or bp_dia >= 110:
        bp_status = "#ff4b4b"
    elif (120 <= bp_sys <= 179) or (80 <= bp_dia <= 109):
        bp_status = "#ffa421"
    else:
        bp_status = "#21c354"
        
    return spo2_status, hr_status, bp_status

# -- 2. Simulated Data Engine --
def generate_vitals(patient_type):
    """Generates mock payload data depending on the patient's selected state."""
    if patient_type == "Healthy Patient":
        return {
            "spo2": random.randint(96, 100),
            "hr": random.randint(65, 85),
            "bp_sys": random.randint(110, 118),
            "bp_dia": random.randint(70, 78)
        }
    elif patient_type == "At-Risk Patient":
        # Introduces a high chance of extreme, volatile fluctuations
        return {
            "spo2": random.choice([random.randint(95, 98), random.randint(85, 92)]),
            "hr": random.choice([random.randint(70, 100), random.randint(110, 130)]),
            "bp_sys": random.choice([random.randint(120, 140), random.randint(170, 190)]),
            "bp_dia": random.choice([random.randint(80, 90), random.randint(105, 120)])
        }

# -- 3. Dashboard UI Assembly --
streamlit.title("PulseGuard AI - Real-Time Vitals")
streamlit.write("Visual triage dashboard. Colors automatically shift based on patient status.")

# Sidebar Controls
streamlit.sidebar.header("Simulation Controls")
patient_type = streamlit.sidebar.radio("Select Patient Profile", ["Healthy Patient", "At-Risk Patient"])

# The fragment decorator reruns just this block every 2 seconds
@streamlit.fragment(run_every=2)
def live_dashboard():
    # Fetch simulated data
    vitals = generate_vitals(patient_type)
    
    # Process through triage logic
    spo2_color, hr_color, bp_color = get_triage_color(
        vitals["spo2"], vitals["hr"], vitals["bp_sys"], vitals["bp_dia"]
    )
    
    # Custom HTML/CSS card template for dynamic backgrounds
    card_html = """
    <div style="background-color: {color}; padding: 20px; border-radius: 10px; color: white; text-align: center; font-family: sans-serif; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 10px;">
        <h3 style="margin: 0; padding-bottom: 10px; opacity:
