import uuid
from html import escape

import pandas as pd
import streamlit as st

from triage_engine import DEPARTMENT_META, PRIORITY_LEVELS, Patient, calculate_priority, predict_opd


def department_badge(department: str) -> str:
    meta = DEPARTMENT_META[department]
    return (
        f'<span class="dept-badge" style="background-color:{meta["color"]};">'
        f'{meta["icon"]} {department}</span>'
    )


st.set_page_config(page_title="Hospital Triage System", layout="wide", page_icon="🏥")

st.markdown(
    """
    <style>
    .dept-badge {
        border-radius: 999px;
        color: white;
        display: inline-block;
        font-size: 0.78rem;
        font-weight: 700;
        line-height: 1;
        padding: 0.38rem 0.62rem;
        white-space: nowrap;
    }
    .patient-row {
        align-items: center;
        border-bottom: 1px solid rgba(49, 51, 63, 0.15);
        display: grid;
        gap: 0.75rem;
        grid-template-columns: 1fr 1.1fr 0.8fr 0.9fr 0.7fr 0.7fr 0.7fr 0.7fr;
        padding: 0.75rem 0;
    }
    .patient-row.header {
        color: rgba(49, 51, 63, 0.75);
        font-size: 0.82rem;
        font-weight: 700;
        padding-top: 0;
    }
    .priority-chip {
        border-radius: 999px;
        color: white;
        display: inline-block;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.38rem 0.62rem;
        white-space: nowrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "patients" not in st.session_state:
    st.session_state.patients = []

PATIENT_FORM_DEFAULTS = {
    "patient_name": "",
    "patient_age": 30,
    "patient_complaint": "",
    "patient_hr": 80,
    "patient_bp": 120,
    "patient_spo2": 98,
    "patient_temperature": 37.0,
    "patient_pain": 3,
    "patient_avpu": "Alert",
}

for key, value in PATIENT_FORM_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def add_patient(name, age, complaint, hr, bp, spo2, pain, avpu, temperature):
    patient = Patient(name, age, complaint, hr, bp, spo2, pain, avpu, temperature)
    patient.priority = calculate_priority(patient)
    patient.id = str(uuid.uuid4())[:8].upper()
    st.session_state.patients.append(patient)
    return patient, predict_opd(patient)


def reset_patient_form():
    for key, value in PATIENT_FORM_DEFAULTS.items():
        st.session_state[key] = value


with st.sidebar:
    st.title("🏥 Hospital Triage System")
    st.header("Register New Patient")
    st.caption("Use this form to add a new patient to the triage queue.")

    name = st.text_input("Full Name", key="patient_name")
    age = st.number_input("Age", 1, 120, key="patient_age")
    complaint = st.text_area("Chief Complaint", key="patient_complaint")

    st.subheader("Vital Signs")
    hr = st.slider("Heart Rate (bpm)", 30, 200, key="patient_hr")
    bp = st.slider("BP Systolic (mmHg)", 60, 220, key="patient_bp")
    spo2 = st.slider("SpO2 (%)", 70, 100, key="patient_spo2")
    temperature = st.slider("Temperature (C)", 34.0, 42.0, key="patient_temperature", step=0.1)
    pain = st.slider("Pain score (0-10)", 0, 10, key="patient_pain")
    avpu = st.selectbox("Consciousness", ["Alert", "Verbal", "Pain", "Unresponsive"], key="patient_avpu")

    add_col, new_col = st.columns(2)
    if add_col.button("+ Add Patient", type="primary"):
        if name and complaint:
            patient, department = add_patient(name, age, complaint, hr, bp, spo2, pain, avpu, temperature)
            st.success(f"Patient {name} added - Priority {patient.priority}, OPD: {department}")
        else:
            st.error("Name and complaint are required")

    new_col.button("Add New", on_click=reset_patient_form)

st.title("🏥 Hospital Triage Dashboard")

patients = sorted(st.session_state.patients, key=lambda p: p.priority)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients", len(patients))
col2.metric("Critical (P1/P2)", sum(1 for p in patients if p.priority <= 2))
col3.metric("Urgent (P3)", sum(1 for p in patients if p.priority == 3))
col4.metric("Non-Urgent (P4/P5)", sum(1 for p in patients if p.priority >= 4))

st.divider()

if patients:
    rows = []
    for patient in patients:
        level, code, color = PRIORITY_LEVELS[patient.priority]
        department = predict_opd(patient)
        rows.append(
            {
                "ID": patient.id,
                "Priority": f"{code} - {level}",
                "OPD": department,
                "Name": patient.name,
                "Age": patient.age,
                "Complaint": patient.chief_complaint,
                "HR": patient.heart_rate,
                "BP": patient.bp_systolic,
                "SpO2": f"{patient.spo2}%",
                "Temp": f"{patient.temperature:.1f} C",
                "Pain": patient.pain_score,
                "Arrived": patient.arrival_time.strftime("%H:%M:%S"),
            }
        )

        priority_badge = (
            f'<span class="priority-chip" style="background-color:{color};">{code} {level}</span>'
        )
        safe_name = escape(patient.name)
        safe_id = escape(patient.id)
        safe_complaint = escape(patient.chief_complaint)
        st.markdown(
            f"""
            <div class="patient-row">
                <div><strong>{safe_name}</strong><br><small>{safe_id}</small></div>
                <div>{department_badge(department)}</div>
                <div>{priority_badge}</div>
                <div>{safe_complaint}</div>
                <div>HR {patient.heart_rate}</div>
                <div>BP {patient.bp_systolic}</div>
                <div>SpO2 {patient.spo2}%</div>
                <div>{patient.temperature:.1f} C</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("View full queue table"):
        df = pd.DataFrame(rows)
        st.dataframe(df, width="stretch", hide_index=True)
else:
    st.info("No patients registered yet. Use the sidebar to add one.")



