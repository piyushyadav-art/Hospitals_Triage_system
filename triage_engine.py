from dataclasses import dataclass, field
from datetime import datetime


PRIORITY_LEVELS = {
    1: ("RESUSCITATION", "P1", "#D92D20"),
    2: ("EMERGENT", "P2", "#F97316"),
    3: ("URGENT", "P3", "#EAB308"),
    4: ("LESS URGENT", "P4", "#16A34A"),
    5: ("NON-URGENT", "P5", "#2563EB"),
}

DEPARTMENT_META = {
    "Cardiology": {"icon": "❤️", "color": "#DC2626"},
    "Pulmonology": {"icon": "🫁", "color": "#0891B2"},
    "Neurology": {"icon": "🧠", "color": "#7C3AED"},
    "Gastroenterology": {"icon": "🩺", "color": "#CA8A04"},
    "Orthopaedics": {"icon": "🦴", "color": "#475569"},
    "Dermatology": {"icon": "🖐️", "color": "#DB2777"},
    "ENT": {"icon": "👂", "color": "#0D9488"},
    "Ophthalmology": {"icon": "👁️", "color": "#4F46E5"},
    "Urology": {"icon": "💧", "color": "#0284C7"},
    "Gynaecology": {"icon": "♀️", "color": "#BE185D"},
    "Psychiatry": {"icon": "🧘", "color": "#9333EA"},
    "Endocrinology": {"icon": "🧪", "color": "#EA580C"},
    "General Medicine": {"icon": "⚕️", "color": "#15803D"},
}


@dataclass
class Patient:
    name: str
    age: int
    chief_complaint: str
    heart_rate: int
    bp_systolic: int
    spo2: int
    pain_score: int
    consciousness: str
    temperature: float = 37.0
    arrival_time: datetime = field(default_factory=datetime.now)
    priority: int = 5
    id: str = ""


def calculate_priority(patient: Patient) -> int:
    score = 0

    avpu = {"Alert": 0, "Verbal": 1, "Pain": 2, "Unresponsive": 3}
    score += avpu.get(patient.consciousness, 0) * 3

    if patient.heart_rate > 120 or patient.heart_rate < 50:
        score += 3
    elif patient.heart_rate > 100:
        score += 1

    if patient.bp_systolic < 90:
        score += 4
    elif patient.bp_systolic > 180:
        score += 2

    if patient.spo2 < 90:
        score += 4
    elif patient.spo2 < 95:
        score += 2

    if patient.temperature > 39.0:
        score += 2
    elif patient.temperature > 38.0:
        score += 1

    score += patient.pain_score // 3

    if score >= 10:
        return 1
    if score >= 7:
        return 2
    if score >= 4:
        return 3
    if score >= 2:
        return 4
    return 5


DEPT_RULES = [
    (
        "Cardiology",
        ["chest pain", "palpitation", "palpitations", "heart", "angina", "arrhythmia"],
        lambda p: p.heart_rate > 120 or p.heart_rate < 50 or p.bp_systolic < 90 or p.bp_systolic > 180,
    ),
    (
        "Pulmonology",
        ["cough", "asthma", "wheeze", "wheezing", "breathing", "breathless", "shortness of breath"],
        lambda p: p.spo2 < 95,
    ),
    (
        "Neurology",
        ["headache", "seizure", "stroke", "dizziness", "paralysis", "weakness", "numbness"],
        lambda p: p.consciousness != "Alert",
    ),
    (
        "Gastroenterology",
        ["stomach pain", "stomach", "nausea", "vomiting", "vomit", "jaundice", "abdominal", "diarrhea"],
        lambda p: False,
    ),
    (
        "Orthopaedics",
        ["fracture", "bone", "back pain", "joint", "fall", "knee", "spine", "sprain"],
        lambda p: False,
    ),
    (
        "Dermatology",
        ["rash", "itch", "itching", "skin", "burn", "allergy", "hives", "wound"],
        lambda p: False,
    ),
    (
        "ENT",
        ["ear", "nose", "throat", "sinus", "cold", "tonsil", "hearing"],
        lambda p: False,
    ),
    (
        "Ophthalmology",
        ["eye", "vision", "blurred", "blurred vision", "red eye", "redness", "blindness"],
        lambda p: False,
    ),
    (
        "Urology",
        ["urine", "kidney", "uti", "stone", "burning urination", "flank pain", "bladder"],
        lambda p: False,
    ),
    (
        "Gynaecology",
        ["pregnancy", "pregnant", "menstrual", "period", "ovary", "vaginal", "pelvic"],
        lambda p: False,
    ),
    (
        "Psychiatry",
        ["anxiety", "depression", "panic", "insomnia", "suicidal", "stress", "psychosis"],
        lambda p: False,
    ),
    (
        "Endocrinology",
        ["diabetes", "diabetic", "thyroid", "sugar", "hypoglycemia", "hyperglycemia"],
        lambda p: p.temperature > 38.5,
    ),
    ("General Medicine", [], lambda p: False),
]


def predict_opd(patient: Patient) -> str:
    complaint = patient.chief_complaint.lower()
    best_department = "General Medicine"
    best_score = 0

    for department, keywords, vital_rule in DEPT_RULES:
        keyword_score = sum(len(keyword.split()) for keyword in keywords if keyword in complaint)
        vital_score = 3 if vital_rule(patient) else 0
        score = keyword_score + vital_score

        if score > best_score:
            best_score = score
            best_department = department

    return best_department
