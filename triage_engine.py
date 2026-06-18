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
        ["headache","migraine","seizure","epilepsy","stroke","dizziness","vertigo","paralysis","weakness","numbness","tingling","loss of sensation","tremor","shaking","muscle spasm","muscle twitching","difficulty walking","unsteady gait","balance problems","coordination problems","ataxia","fainting","syncope","loss of consciousness","confusion","memory loss","forgetfulness",
        "difficulty speaking","slurred speech","speech difficulty","difficulty swallowing","vision loss",
        "blurred vision","double vision","facial droop","facial weakness","hearing loss","ringing in ears",
        "neuropathy","burning sensation","nerve pain","chronic pain","back pain with numbness","neck stiffness","altered mental status","brain fog",
        "difficulty concentrating","sleep attacks","excessive sleepiness","movement disorder","involuntary movements",
        "restless legs","nerve injury","cranial nerve palsy"],
        lambda p: p.consciousness != "Alert",
    ),
    (
        "Gastroenterology",
        ["stomach pain","stomach ache","abdominal pain","abdomen pain","abdominal cramps","stomach",
        "nausea","vomiting","vomit","retching","diarrhea","loose stools","constipation","bloating",
        "gas","flatulence","indigestion","heartburn","acid reflux","acidity","burping","belching",
        "jaundice","yellow eyes","yellow skin","loss of appetite","poor appetite","abdominal swelling",
        "distended abdomen","blood in stool","black stool","dark stool","rectal bleeding","bloody diarrhea",
        "difficulty swallowing","painful swallowing","food stuck in throat","weight loss","unexplained weight loss","liver pain","right upper abdominal pain","gallbladder pain",
        "pelvic abdominal pain","cramping","stomach discomfort","early satiety","fullness after eating","frequent bowel movements","fecal incontinence","mucus in stool",
        "change in bowel habits","abdominal tenderness","burning stomach","peptic ulcer","gastric pain"],
        lambda p: False,
    ),
    (
        "Orthopaedics",
        ["fracture","broken bone","bone","bone pain","back pain","lower back pain","upper back pain",
        "neck pain","spine","spinal pain","joint","joint pain","joint swelling","joint stiffness",
        "arthritis","sprain", "strain","ligament injury","tendon injury","torn ligament","dislocation","shoulder dislocation",
        "fall", "injury", "trauma", "sports injury", "knee", "knee pain", "hip pain", "ankle pain", "foot pain",
        "heel pain", "shoulder pain", "elbow pain", "wrist pain", "hand pain", "finger pain", "leg pain",
        "arm pain", "swollen joint","swelling", "bruising","difficulty walking","limping",
        "cannot bear weight","reduced mobility", "restricted movement", "stiffness", "muscle pain",
        "muscle injury","muscle weakness", "tendonitis", "bursitis", "osteoporosis", "scoliosis",
        "slipped disc", "herniated disc","sciatica","frozen shoulder","carpal tunnel","deformity","post fracture pain"],
        lambda p: False,
    ),
    (
        "Dermatology",
        ["rash","skin rash","itch","itching","itchy skin","skin","dry skin","flaky skin","peeling skin",
        "redness","red skin","skin irritation","burn","sunburn","allergy","allergic reaction","hives","urticaria",
        "wound","cut","abrasion","laceration","ulcer","blister","blisters","boil","abscess",
        "pimple","pimples", "acne", "blackheads", "whiteheads", "eczema", "dermatitis", "psoriasis",
        "skin infection", "fungal infection", "ringworm", "athlete's foot", "skin discoloration", "dark spots",
        "pigmentation", "mole", "wart", "warts", "skin tag", "scab", "swelling", "skin swelling",
        "pus","oozing skin", "cracked skin", "scaly skin", "sensitive skin", "burning skin",
        "hair loss","alopecia","dandruff","scalp itching","scalp redness","nail infection","brittle nails","ingrown nail"],
        lambda p: False,
    ),
    (
        "ENT",
        [
        "ear",
        "ear pain",
        "earache",
        "ear infection",
        "ear discharge",
        "ear ringing",
        "tinnitus",
        "hearing",
        "hearing loss",
        "reduced hearing",
        "deafness",
        "blocked ear",
        "nose",
        "runny nose",
        "stuffy nose",
        "blocked nose",
        "nasal congestion",
        "nosebleed",
        "bleeding nose",
        "loss of smell",
        "reduced smell",
        "sinus",
        "sinus pain",
        "sinusitis",
        "facial pressure",
        "facial pain",
        "postnasal drip",
        "cold",
        "common cold",
        "sneezing",
        "throat",
        "sore throat",
        "throat pain",
        "throat irritation",
        "dry throat",
        "difficulty swallowing",
        "painful swallowing",
        "hoarseness",
        "hoarse voice",
        "voice change",
        "loss of voice",
        "tonsil",
        "tonsillitis",
        "swollen tonsils",
        "mouth ulcer",
        "oral ulcer",
        "bad breath",
        "snoring",
        "sleep apnea",
        "neck swelling",
        "swollen glands",
        "swollen lymph nodes",
        "persistent cough",
        "pharyngitis",
        "laryngitis",
        "nasal polyps",
        "vertigo",
        "dizziness related to ear"
    ],
        lambda p: False,
    ),
    (
        "Ophthalmology",
        [
        "eye",
        "eye pain",
        "eye redness",
        "red eye",
        "redness",
        "vision",
        "blurred",
        "blurred vision",
        "loss of vision",
        "vision loss",
        "blindness",
        "partial blindness",
        "double vision",
        "decreased vision",
        "poor vision",
        "difficulty seeing",
        "night blindness",
        "floaters",
        "flashes of light",
        "spots in vision",
        "eye strain",
        "eye fatigue",
        "dry eye",
        "dry eyes",
        "watery eyes",
        "tearing",
        "excessive tearing",
        "itchy eyes",
        "burning eyes",
        "swollen eyelid",
        "eyelid swelling",
        "eyelid pain",
        "stye",
        "chalazion",
        "foreign body in eye",
        "eye injury",
        "eye trauma",
        "light sensitivity",
        "photophobia",
        "glare sensitivity",
        "eye discharge",
        "pus from eye",
        "conjunctivitis",
        "pink eye",
        "cataract",
        "glaucoma",
        "retinal detachment",
        "macular degeneration",
        "color vision problems",
        "visual disturbance",
        "halo around lights",
        "sudden vision loss",
        "eye infection"
    ],
        lambda p: False,
    ),
    (
        "Urology",
        [
        "urine",
        "urination",
        "urinary",
        "burning urination",
        "painful urination",
        "dysuria",
        "frequent urination",
        "urgency",
        "urinary urgency",
        "urinary frequency",
        "difficulty urinating",
        "trouble urinating",
        "weak urine stream",
        "poor urine flow",
        "dribbling urine",
        "urinary retention",
        "incomplete emptying",
        "blood in urine",
        "hematuria",
        "cloudy urine",
        "foul smelling urine",
        "dark urine",
        "kidney",
        "kidney pain",
        "kidney infection",
        "uti",
        "urinary tract infection",
        "bladder",
        "bladder pain",
        "overactive bladder",
        "stone",
        "kidney stone",
        "renal stone",
        "ureteric stone",
        "flank pain",
        "side pain",
        "lower abdominal pain",
        "pelvic pain",
        "groin pain",
        "nocturia",
        "nighttime urination",
        "urinary incontinence",
        "leaking urine",
        "bedwetting",
        "swollen testicle",
        "testicular pain",
        "scrotal pain",
        "epididymitis",
        "hydrocele",
        "varicocele",
        "prostate enlargement",
        "enlarged prostate",
        "prostate pain",
        "erectile dysfunction",
        "painful ejaculation",
        "recurrent uti"
    ],
        lambda p: False,
    ),
    (
        "Gynaecology",
        [
        "pregnancy",
        "pregnant",
        "missed period",
        "missed periods",
        "positive pregnancy test",
        "morning sickness",
        "menstrual",
        "menstruation",
        "period",
        "period pain",
        "painful periods",
        "heavy periods",
        "irregular periods",
        "absent periods",
        "spotting",
        "abnormal bleeding",
        "vaginal bleeding",
        "vaginal",
        "vaginal discharge",
        "abnormal discharge",
        "vaginal itching",
        "vaginal pain",
        "vaginal infection",
        "yeast infection",
        "pelvic",
        "pelvic pain",
        "pelvic pressure",
        "ovary",
        "ovarian cyst",
        "pcos",
        "polycystic ovary syndrome",
        "endometriosis",
        "fibroids",
        "uterine fibroids",
        "uterus pain",
        "cervical pain",
        "pain during intercourse",
        "pain after intercourse",
        "infertility",
        "difficulty conceiving",
        "fertility issues",
        "menopause",
        "hot flashes",
        "postmenopausal bleeding",
        "breast pain",
        "breast lump",
        "nipple discharge",
        "lower abdominal pain",
        "miscarriage",
        "ectopic pregnancy",
        "labor pain",
        "contractions",
        "postpartum bleeding",
        "postpartum pain",
        "vulvar pain",
        "genital itching"
    ],
        lambda p: False,
    ),
    (
        "Psychiatry",
        [
        "anxiety",
        "anxious",
        "depression",
        "depressed",
        "low mood",
        "sadness",
        "feeling sad",
        "panic",
        "panic attack",
        "panic attacks",
        "stress",
        "stressed",
        "insomnia",
        "difficulty sleeping",
        "can't sleep",
        "poor sleep",
        "sleep disturbance",
        "excessive sleeping",
        "suicidal",
        "suicidal thoughts",
        "self harm",
        "self-harm",
        "hopelessness",
        "worthlessness",
        "guilt",
        "loss of interest",
        "lack of motivation",
        "fatigue",
        "emotional distress",
        "mood swings",
        "irritability",
        "anger issues",
        "psychosis",
        "hallucinations",
        "hearing voices",
        "seeing things",
        "delusions",
        "paranoia",
        "suspiciousness",
        "manic",
        "mania",
        "bipolar",
        "racing thoughts",
        "obsessive thoughts",
        "ocd",
        "compulsions",
        "social anxiety",
        "phobia",
        "fearfulness",
        "concentration problems",
        "attention problems",
        "memory problems",
        "restlessness",
        "agitation",
        "emotional numbness",
        "dissociation",
        "nightmares",
        "ptsd",
        "trauma",
        "grief",
        "eating disorder"
    ],
        lambda p: False,
    ),
    (
        "Endocrinology",
        [
        "diabetes",
        "diabetic",
        "high blood sugar",
        "low blood sugar",
        "sugar",
        "blood sugar",
        "hypoglycemia",
        "hyperglycemia",
        "thyroid",
        "hypothyroidism",
        "hyperthyroidism",
        "goiter",
        "thyroid swelling",
        "thyroid nodule",
        "excessive thirst",
        "increased thirst",
        "polydipsia",
        "frequent urination",
        "polyuria",
        "increased hunger",
        "polyphagia",
        "unexplained weight loss",
        "unexplained weight gain",
        "fatigue",
        "tiredness",
        "weakness",
        "blurred vision",
        "slow wound healing",
        "recurrent infections",
        "numbness in feet",
        "tingling in feet",
        "burning feet",
        "cold intolerance",
        "heat intolerance",
        "excessive sweating",
        "dry skin",
        "hair loss",
        "constipation",
        "diarrhea",
        "palpitations",
        "rapid heartbeat",
        "tremor",
        "anxiety",
        "irritability",
        "moon face",
        "buffalo hump",
        "cushing syndrome",
        "adrenal disorder",
        "addison disease",
        "hormonal imbalance",
        "growth problems",
        "delayed puberty",
        "early puberty",
        "erectile dysfunction",
        "low libido",
        "menstrual irregularities",
        "pcos",
        "polycystic ovary syndrome",
        "osteoporosis"
    ],
        lambda p: p.temperature > 38.5,
    ),
    ("General Medicine", [
        "fever",
        "high fever",
        "low grade fever",
        "chills",
        "fatigue",
        "tiredness",
        "weakness",
        "body ache",
        "body pain",
        "malaise",
        "loss of appetite",
        "weight loss",
        "weight gain",
        "night sweats",
        "dehydration",
        "dizziness",
        "lightheadedness",
        "fainting",
        "swelling",
        "generalized swelling",
        "edema",
        "pain",
        "chronic pain",
        "joint pain",
        "muscle pain",
        "cough",
        "persistent cough",
        "shortness of breath",
        "breathlessness",
        "chest discomfort",
        "palpitations",
        "high blood pressure",
        "low blood pressure",
        "infection",
        "viral illness",
        "flu",
        "influenza",
        "covid",
        "covid19",
        "sore throat",
        "headache",
        "nausea",
        "vomiting",
        "diarrhea",
        "constipation",
        "abdominal pain",
        "rash",
        "allergy",
        "anemia",
        "pale skin",
        "sleep problems",
        "insomnia",
        "general checkup",
        "health checkup",
        "follow up",
        "routine examination",
        "multiple complaints",
        "not feeling well"
    ], lambda p: False),
]

def weighted_match(complaint, keywords, weight_map=None, default_weight=1.0):
    complaint = complaint.lower()
    score = 0.0
    for kw in keywords:
        if kw in complaint:
            score += weight_map.get(kw, default_weight) if weight_map else default_weight
    return score

DEPT_WEIGHTS = {
    "Cardiology": 3.0,
    "Pulmonology": 2.5,
    "Neurology": 2.8,
    "Gastroenterology": 2.0,
    "Orthopaedics": 2.2,
    "Dermatology": 1.8,
    "ENT": 1.8,
    "Ophthalmology": 1.8,
    "Urology": 2.0,
    "Gynaecology": 2.0,
    "Psychiatry": 2.0,
    "Endocrinology": 2.2,
    "General Medicine": 0.8,
}

def predict_opd(patient: Patient) -> str:
    complaint = patient.chief_complaint.lower()
    best_department = "General Medicine"
    best_score = 0.0

    for department, keywords, vital_rule in DEPT_RULES:
        keyword_score = weighted_match(complaint, keywords)
        vital_score = 3.0 if vital_rule(patient) else 0.0
        department_weight = DEPT_WEIGHTS.get(department, 1.0)

        total_score = keyword_score * department_weight + vital_score

        if total_score > best_score:
            best_score = total_score
            best_department = department

    return best_department
    
# def predict_opd(patient: Patient) -> str:
#     complaint = patient.chief_complaint.lower()
#     best_department = "General Medicine"
#     best_score = 0

#     for department, keywords, vital_rule in DEPT_RULES:
#         keyword_score = sum(len(keyword.split()) for keyword in keywords if keyword in complaint)
#         vital_score = 3 if vital_rule(patient) else 0
#         score = keyword_score + vital_score

#         if score > best_score:
#             best_score = score
#             best_department = department

#     return best_department
