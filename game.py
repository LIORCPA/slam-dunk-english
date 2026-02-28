import streamlit as st
import random
import json
import os
import base64
import streamlit.components.v1 as components
import requests

# Optional Lottie — app works fine without it
try:
    from streamlit_lottie import st_lottie
    LOTTIE_OK = True
except ImportError:
    LOTTIE_OK = False

st.set_page_config(page_title="Slam Dunk English 🏀", layout="centered", initial_sidebar_state="collapsed")

# ===== CSS =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&display=swap');

/* === GLOBAL DIRECTION & LTR HELPERS === */
html, body, .stApp { direction: rtl; }
.ltr { direction: ltr; unicode-bidi: plaintext; }

/* === ACCESSIBILITY: Respect Reduced Motion === */
@media (prefers-reduced-motion: reduce){
  * { animation: none !important; transition: none !important; }
}

/* === BACKGROUND - Dark Navy with Grid (like NBA game) === */
.stApp {
    background:
        repeating-linear-gradient(0deg, transparent, transparent 49px, rgba(255,255,255,0.03) 49px, rgba(255,255,255,0.03) 50px),
        repeating-linear-gradient(90deg, transparent, transparent 49px, rgba(255,255,255,0.03) 49px, rgba(255,255,255,0.03) 50px),
        linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
}

/* === MAIN CARD === */
.main .block-container {
    background: linear-gradient(180deg, #f8f8f8 0%, #ffffff 100%) !important;
    border-radius: 30px !important;
    padding: clamp(18px,3vw,35px) clamp(16px,3vw,28px) clamp(16px,3vw,30px) !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.55) !important;
    outline: 7px solid #ff6b35;
    max-width: 600px !important;
    margin-top: 18px !important;
    margin-bottom: 18px !important;
}

/* === TYPOGRAPHY - Bangers for headings & game UI === */
h1, h2, h3, h4 {
    font-family: 'Bangers', 'Arial Black', Arial, sans-serif !important;
    letter-spacing: 2px !important;
}
p, div, span, label, .stMarkdown {
    font-family: 'Arial Black', Arial, sans-serif !important;
}
h1 {
    color: #ff6b35 !important;
    text-shadow: 3px 3px 0px rgba(0,0,0,0.15) !important;
    font-weight: 400 !important;
    letter-spacing: 3px !important;
    text-align: center !important;
}
h2, h3 { color: #1a1a2e !important; }

/* === BUTTONS - Neon Glow Arcade style === */
.stButton > button {
    width: 100% !important;
    border-radius: 15px !important;
    height: 3.6em !important;
    font-size: 1.15em !important;
    font-weight: 900 !important;
    font-family: 'Bangers', 'Arial Black', Arial, sans-serif !important;
    letter-spacing: 2px !important;
    border: 2px solid rgba(255,107,53,0.3) !important;
    color: white !important;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.4) !important;
    margin-bottom: 10px !important;
    background: linear-gradient(145deg, #e74c3c 0%, #c0392b 100%) !important;
    box-shadow: 0 8px 0 rgba(100,0,0,0.5), 0 10px 22px rgba(0,0,0,0.30), 0 0 15px rgba(231,76,60,0.3) !important;
    transition: transform 0.1s, box-shadow 0.1s !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 11px 0 rgba(100,0,0,0.45), 0 14px 28px rgba(0,0,0,0.35), 0 0 30px rgba(255,107,53,0.7) !important;
    background: linear-gradient(145deg, #f05545 0%, #d32f2f 100%) !important;
    border: 2px solid rgba(255,107,53,0.7) !important;
}
.stButton > button:active {
    transform: translateY(5px) scale(0.97) !important;
    box-shadow: 0 2px 0 rgba(100,0,0,0.5), 0 0 10px rgba(231,76,60,0.5) !important;
}

/* === BIG WORD DISPLAY === */
.big-word {
    font-size: clamp(1.8rem, 4vw, 2.8rem);
    font-family: 'Bangers', 'Arial Black', Arial, sans-serif !important;
    font-weight: 400;
    text-align: center;
    padding: clamp(14px,3vw,25px) clamp(12px,3vw,15px);
    background: linear-gradient(135deg, #FF6B00 0%, #FF9500 100%);
    color: white;
    border-radius: 20px;
    margin: 12px 0 24px 0;
    letter-spacing: clamp(2px, 0.8vw, 4px);
    box-shadow: 0 8px 0 rgba(180,60,0,0.55), 0 14px 30px rgba(255,107,0,0.40), 0 0 20px rgba(255,107,0,0.25);
    text-shadow: 2px 2px 5px rgba(0,0,0,0.30);
}

/* === SCORE / STREAK / TOPIC BOXES === */
.score-box {
    font-size: 1.2em;
    font-weight: 900;
    text-align: center;
    padding: 14px 8px;
    background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
    border-radius: 15px;
    color: white;
    box-shadow: 0 6px 0 rgba(0,100,0,0.45), 0 10px 18px rgba(39,174,96,0.35);
    font-family: 'Bangers', 'Arial Black', Arial, sans-serif !important;
    letter-spacing: 1px;
}
.streak-box {
    font-size: 1.1em;
    text-align: center;
    padding: 14px 8px;
    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
    border-radius: 15px;
    color: white;
    font-weight: 900;
    box-shadow: 0 6px 0 rgba(140,0,0,0.45), 0 10px 18px rgba(231,76,60,0.35);
    font-family: 'Bangers', 'Arial Black', Arial, sans-serif !important;
    letter-spacing: 1px;
}
/* 🔥 Streak >= 5: box glows like fire */
.streak-box-fire {
    font-size: 1.1em;
    text-align: center;
    padding: 14px 8px;
    background: linear-gradient(135deg, #ff4500 0%, #ff6b00 50%, #ff9500 100%);
    border-radius: 15px;
    color: white;
    font-weight: 900;
    font-family: 'Bangers', 'Arial Black', Arial, sans-serif !important;
    letter-spacing: 1px;
    animation: fireFlicker 0.6s ease-in-out infinite alternate;
}
@keyframes fireFlicker {
    from { box-shadow: 0 6px 0 rgba(180,50,0,0.6), 0 10px 20px rgba(255,69,0,0.4), 0 0 15px rgba(255,150,0,0.5); }
    to   { box-shadow: 0 6px 0 rgba(180,50,0,0.6), 0 10px 30px rgba(255,69,0,0.7), 0 0 35px rgba(255,200,0,0.9); }
}
.topic-badge {
    font-size: 1.2em;
    text-align: center;
    padding: 14px 8px;
    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
    border-radius: 15px;
    color: white;
    font-weight: 900;
    box-shadow: 0 6px 0 rgba(0,80,160,0.45), 0 10px 18px rgba(52,152,219,0.35);
    font-family: 'Bangers', 'Arial Black', Arial, sans-serif !important;
    letter-spacing: 1px;
}

/* === BASKETBALL LIVES BAR === */
.lives-bar {
    text-align: center;
    font-size: 1.3em;
    margin: 4px 0 10px 0;
    letter-spacing: 1px;
    direction: ltr;
}

/* === WELCOME BOX === */
.welcome-box {
    background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
    border-radius: 28px;
    padding: 30px 22px 26px 22px;
    text-align: center;
    color: white;
    box-shadow: 0 9px 0 rgba(180,55,0,0.5), 0 16px 42px rgba(255,107,53,0.55);
    margin-bottom: 24px;
    border: 4px solid rgba(255,255,255,0.28);
}

/* === SPORTS ROW === */
.sports-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
    margin-bottom: 18px;
}

/* === INPUT FIELD === */
.stTextInput > div > div > input {
    border-radius: 15px !important;
    border: 3px solid #ff6b35 !important;
    font-size: 1.15em !important;
    font-weight: 700 !important;
    padding: 10px 16px !important;
    font-family: 'Arial Black', Arial, sans-serif !important;
    background: #fff8f0 !important;
    color: #1a1a2e !important;
}
.stTextInput > div > div > input:focus {
    border-color: #f7931e !important;
    box-shadow: 0 0 0 3px rgba(255,107,53,0.25) !important;
}

/* === ALERTS === */
.stSuccess > div, .stError > div, .stWarning > div, .stInfo > div {
    border-radius: 15px !important;
    font-weight: 700 !important;
    font-family: 'Arial Black', Arial, sans-serif !important;
}

/* === PROGRESS BAR === */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #ff6b35, #f7931e) !important;
    border-radius: 10px !important;
}

/* === DIVIDER === */
hr { border-color: rgba(255,107,53,0.3) !important; margin: 14px 0 !important; }

/* === TROPHY CABINET === */
.trophy-card {
    background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
    border-radius: 16px;
    padding: 14px 8px;
    text-align: center;
    box-shadow: 0 5px 0 rgba(180,130,0,0.4), 0 8px 18px rgba(253,203,110,0.5);
    border: 3px solid rgba(255,255,255,0.6);
    margin-bottom: 10px;
    font-family: 'Arial Black', Arial, sans-serif !important;
}
.trophy-locked {
    background: linear-gradient(135deg, #dfe6e9 0%, #b2bec3 100%);
    border-radius: 16px;
    padding: 14px 8px;
    text-align: center;
    box-shadow: 0 4px 0 rgba(0,0,0,0.15);
    opacity: 0.5;
    margin-bottom: 10px;
    font-family: 'Arial Black', Arial, sans-serif !important;
}
.new-trophy-banner {
    background: linear-gradient(135deg, #f9ca24 0%, #f0932b 100%);
    border-radius: 20px;
    padding: 18px;
    text-align: center;
    color: white;
    font-weight: 900;
    font-size: 1.3em;
    box-shadow: 0 8px 0 rgba(180,100,0,0.5), 0 0 30px rgba(249,202,36,0.6);
    animation: glowPulse 1s ease-in-out infinite alternate;
    margin: 10px 0;
}
@keyframes glowPulse {
    from { box-shadow: 0 8px 0 rgba(180,100,0,0.5), 0 0 20px rgba(249,202,36,0.5); }
    to   { box-shadow: 0 8px 0 rgba(180,100,0,0.5), 0 0 40px rgba(249,202,36,0.9); }
}

/* === ANIMATIONS === */
@keyframes floatBall {
    0%,100% { transform: translateY(0px) rotate(0deg); }
    33%      { transform: translateY(-14px) rotate(12deg); }
    66%      { transform: translateY(-6px)  rotate(-6deg); }
}
@keyframes bounceIn {
    0%   { transform: scale(0.5); opacity: 0; }
    70%  { transform: scale(1.08); }
    100% { transform: scale(1); opacity: 1; }
}

.b1{display:inline-block;font-size:2.8em;animation:floatBall 2.0s ease-in-out infinite 0.0s;}
.b2{display:inline-block;font-size:2.4em;animation:floatBall 2.3s ease-in-out infinite 0.2s;}
.b3{display:inline-block;font-size:2.6em;animation:floatBall 1.9s ease-in-out infinite 0.4s;}
.b4{display:inline-block;font-size:2.2em;animation:floatBall 2.5s ease-in-out infinite 0.6s;}
.b5{display:inline-block;font-size:2.8em;animation:floatBall 2.1s ease-in-out infinite 0.8s;}
.b6{display:inline-block;font-size:2.3em;animation:floatBall 2.4s ease-in-out infinite 1.0s;}
.b7{display:inline-block;font-size:2.5em;animation:floatBall 1.8s ease-in-out infinite 1.2s;}
.b8{display:inline-block;font-size:2.2em;animation:floatBall 2.2s ease-in-out infinite 1.4s;}
</style>
""", unsafe_allow_html=True)

# ===== Lottie Animations =====
@st.cache_data(ttl=3600)
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def show_lottie(anim, height=160):
    if LOTTIE_OK and anim:
        st_lottie(anim, height=height, loop=False)

# Load once (cached)
LOTTIE_SUCCESS  = load_lottie("https://assets5.lottiefiles.com/packages/lf20_at4qzj7p.json")   # ✅ V ירוק
LOTTIE_FAIL     = load_lottie("https://assets5.lottiefiles.com/packages/lf20_qpwb7qsq.json")   # ❌ X אדום
LOTTIE_TROPHY   = load_lottie("https://assets7.lottiefiles.com/packages/lf20_gn0tojrd.json")   # 🏆 גביע
LOTTIE_BALL     = load_lottie("https://assets2.lottiefiles.com/packages/lf20_m6cu96y5.json")   # 🏀 כדור
LOTTIE_FIRE     = load_lottie("https://assets9.lottiefiles.com/packages/lf20_f7p9pxm2.json")   # 🔥 אש

# ===== Word Database =====
WORD_DATA = {
    "כדורסל 🏀": [
        {"he": "כדור", "en": "Ball"},
        {"he": "סל", "en": "Basket"},
        {"he": "קבוצה", "en": "Team"},
        {"he": "מגרש", "en": "Court"},
        {"he": "שחקן", "en": "Player"},
        {"he": "אימון", "en": "Practice"},
        {"he": "ניצחון", "en": "Win"},
        {"he": "מאמן", "en": "Coach"},
        {"he": "זריקה", "en": "Throw"},
        {"he": "הגנה", "en": "Defense"},
    ],
    "ספורט 🏅": [
        {"he": "כדורגל", "en": "Football"},
        {"he": "טניס", "en": "Tennis"},
        {"he": "כדורעף", "en": "Volleyball"},
        {"he": "שחייה", "en": "Swimming"},
        {"he": "ריצה", "en": "Running"},
        {"he": "גול", "en": "Goal"},
        {"he": "שופט", "en": "Referee"},
        {"he": "אצטדיון", "en": "Stadium"},
        {"he": "מדליה", "en": "Medal"},
        {"he": "אולימפיאדה", "en": "Olympics"},
        {"he": "אליפות", "en": "Championship"},
        {"he": "ניקוד", "en": "Score"},
        {"he": "הפסד", "en": "Loss"},
        {"he": "בעיטה", "en": "Kick"},
        {"he": "ספרינט", "en": "Sprint"},
    ],
    "חיות 🦁": [
        {"he": "כלב", "en": "Dog"},
        {"he": "חתול", "en": "Cat"},
        {"he": "אריה", "en": "Lion"},
        {"he": "פיל", "en": "Elephant"},
        {"he": "קוף", "en": "Monkey"},
        {"he": "נחש", "en": "Snake"},
        {"he": "ברווז", "en": "Duck"},
        {"he": "דב", "en": "Bear"},
        {"he": "סוס", "en": "Horse"},
        {"he": "פרה", "en": "Cow"},
        {"he": "ארנב", "en": "Rabbit"},
        {"he": "צב", "en": "Turtle"},
    ],
    "צבעים 🎨": [
        {"he": "אדום", "en": "Red"},
        {"he": "כחול", "en": "Blue"},
        {"he": "ירוק", "en": "Green"},
        {"he": "צהוב", "en": "Yellow"},
        {"he": "כתום", "en": "Orange"},
        {"he": "סגול", "en": "Purple"},
        {"he": "לבן", "en": "White"},
        {"he": "שחור", "en": "Black"},
        {"he": "ורוד", "en": "Pink"},
        {"he": "חום", "en": "Brown"},
    ],
    "אוכל 🍕": [
        {"he": "לחם", "en": "Bread"},
        {"he": "חלב", "en": "Milk"},
        {"he": "תפוח", "en": "Apple"},
        {"he": "בננה", "en": "Banana"},
        {"he": "עוגה", "en": "Cake"},
        {"he": "ביצה", "en": "Egg"},
        {"he": "גבינה", "en": "Cheese"},
        {"he": "עוף", "en": "Chicken"},
        {"he": "דג", "en": "Fish"},
        {"he": "אורז", "en": "Rice"},
        {"he": "עגבנייה", "en": "Tomato"},
        {"he": "מלפפון", "en": "Cucumber"},
    ],
    "בית ספר 📚": [
        {"he": "עיפרון", "en": "Pencil"},
        {"he": "ספר", "en": "Book"},
        {"he": "מחברת", "en": "Notebook"},
        {"he": "מחק", "en": "Eraser"},
        {"he": "שולחן", "en": "Desk"},
        {"he": "כיסא", "en": "Chair"},
        {"he": "לוח", "en": "Board"},
        {"he": "מורה", "en": "Teacher"},
        {"he": "כיתה", "en": "Classroom"},
        {"he": "תיק", "en": "Bag"},
        {"he": "מספריים", "en": "Scissors"},
        {"he": "סרגל", "en": "Ruler"},
    ],
    "גוף 🦴": [
        {"he": "ראש", "en": "Head"},
        {"he": "עיניים", "en": "Eyes"},
        {"he": "אף", "en": "Nose"},
        {"he": "פה", "en": "Mouth"},
        {"he": "יד", "en": "Hand"},
        {"he": "רגל", "en": "Leg"},
        {"he": "אוזן", "en": "Ear"},
        {"he": "שיניים", "en": "Teeth"},
        {"he": "גב", "en": "Back"},
        {"he": "בטן", "en": "Stomach"},
        {"he": "אצבע", "en": "Finger"},
        {"he": "כתף", "en": "Shoulder"},
    ],
    "משפחה 👨‍👩‍👧": [
        {"he": "אמא", "en": "Mom"},
        {"he": "אבא", "en": "Dad"},
        {"he": "אח", "en": "Brother"},
        {"he": "אחות", "en": "Sister"},
        {"he": "סבא", "en": "Grandpa"},
        {"he": "סבתא", "en": "Grandma"},
        {"he": "דוד", "en": "Uncle"},
        {"he": "דודה", "en": "Aunt"},
        {"he": "ילד", "en": "Child"},
        {"he": "תינוק", "en": "Baby"},
    ],
    "טבע 🌳": [
        {"he": "עץ", "en": "Tree"},
        {"he": "פרח", "en": "Flower"},
        {"he": "ים", "en": "Sea"},
        {"he": "הר", "en": "Mountain"},
        {"he": "שמש", "en": "Sun"},
        {"he": "ירח", "en": "Moon"},
        {"he": "כוכב", "en": "Star"},
        {"he": "גשם", "en": "Rain"},
        {"he": "שלג", "en": "Snow"},
        {"he": "רוח", "en": "Wind"},
        {"he": "אדמה", "en": "Earth"},
        {"he": "נהר", "en": "River"},
    ],
    "מספרים 🔢": [
        {"he": "אחד", "en": "One"},
        {"he": "שניים", "en": "Two"},
        {"he": "שלושה", "en": "Three"},
        {"he": "ארבעה", "en": "Four"},
        {"he": "חמישה", "en": "Five"},
        {"he": "שישה", "en": "Six"},
        {"he": "שבעה", "en": "Seven"},
        {"he": "שמונה", "en": "Eight"},
        {"he": "תשעה", "en": "Nine"},
        {"he": "עשרה", "en": "Ten"},
    ],
    "בית 🏠": [
        {"he": "דלת", "en": "Door"},
        {"he": "חלון", "en": "Window"},
        {"he": "מיטה", "en": "Bed"},
        {"he": "ספה", "en": "Sofa"},
        {"he": "מטבח", "en": "Kitchen"},
        {"he": "שירותים", "en": "Bathroom"},
        {"he": "חדר", "en": "Room"},
        {"he": "מקרר", "en": "Fridge"},
        {"he": "כוס", "en": "Cup"},
        {"he": "צלחת", "en": "Plate"},
        {"he": "כיסא", "en": "Chair"},
        {"he": "מנורה", "en": "Lamp"},
    ],
}

# ===== Stats =====
STATS_FILE = os.path.join(os.path.dirname(__file__), "stats.json")

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Migrate: add trophies field if missing
        if "trophies" not in data:
            data["trophies"] = []
        return data
    return {
        "total_correct": 0,
        "total_wrong": 0,
        "best_streak": 0,
        "words": {},
        "topics": {},
        "trophies": [],
    }

def save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def record_answer(word_en, topic, correct):
    stats = load_stats()
    if word_en not in stats["words"]:
        stats["words"][word_en] = {"correct": 0, "wrong": 0}
    if topic not in stats["topics"]:
        stats["topics"][topic] = {"correct": 0, "wrong": 0}
    if correct:
        stats["total_correct"] += 1
        stats["words"][word_en]["correct"] += 1
        stats["topics"][topic]["correct"] += 1
        st.session_state.streak += 1
        st.session_state.score += 1
        if st.session_state.streak > stats["best_streak"]:
            stats["best_streak"] = st.session_state.streak
    else:
        stats["total_wrong"] += 1
        stats["words"][word_en]["wrong"] += 1
        stats["topics"][topic]["wrong"] += 1
        st.session_state.streak = 0
    save_stats(stats)

    # Track last 15 answers for basketball lives bar
    hist = st.session_state.answer_history
    hist.append(correct)
    if len(hist) > 15:
        hist.pop(0)
    st.session_state.answer_history = hist

# ===== Trophy System =====
TROPHIES_DEF = [
    # (type, threshold, emoji, name, desc)
    ("streak",  3,   "🥉", "צלף שלוש",      "3 תשובות ברצף"),
    ("streak",  5,   "🥈", "מלך המגרש",     "5 ברצף"),
    ("streak",  7,   "🥇", "He's On Fire!", "7 ברצף"),
    ("streak",  10,  "🏆", "MVP!",           "10 ברצף — אגדה!"),
    ("streak",  15,  "👑", "Hall of Fame",  "15 ברצף — אלוף העולם!"),
    ("total",   10,  "🎖️", "מתחיל",          "10 תשובות נכונות"),
    ("total",   25,  "⭐", "שחקן",           "25 תשובות נכונות"),
    ("total",   50,  "🌟", "כוכב",           "50 תשובות נכונות"),
    ("total",   100, "💎", "אגדה",           "100 תשובות נכונות"),
]

def check_trophies():
    """Check if new trophies earned this render. Returns list of (emoji, name, desc)."""
    stats = load_stats()
    earned = set(stats.get("trophies", []))
    new_trophies = []
    streak = st.session_state.streak
    total  = stats["total_correct"]

    for t_type, threshold, emoji, name, desc in TROPHIES_DEF:
        tid = f"{t_type}_{threshold}"
        if tid not in earned:
            if t_type == "streak" and streak >= threshold:
                earned.add(tid)
                new_trophies.append((emoji, name, desc))
            elif t_type == "total" and total >= threshold:
                earned.add(tid)
                new_trophies.append((emoji, name, desc))

    if new_trophies:
        stats["trophies"] = list(earned)
        save_stats(stats)
    return new_trophies

def show_trophy_cabinet(compact=False):
    """Show the trophy cabinet. compact=True for menu, False for full stats view."""
    stats = load_stats()
    earned = set(stats.get("trophies", []))
    if not earned:
        return

    earned_trophies = [
        (e, n, d) for t, thr, e, n, d in TROPHIES_DEF
        if f"{t}_{thr}" in earned
    ]

    st.divider()
    st.markdown(f"### 🏆 ארון הגביעים ({len(earned_trophies)}/{len(TROPHIES_DEF)})")

    if compact:
        row = "  ".join(e for e, n, d in earned_trophies)
        st.markdown(
            f'<div style="font-size:2.2em;text-align:center;letter-spacing:6px">{row}</div>',
            unsafe_allow_html=True
        )
    else:
        # Show all trophies — earned + locked
        cols = st.columns(4)
        idx = 0
        for t_type, threshold, emoji, name, desc in TROPHIES_DEF:
            tid = f"{t_type}_{threshold}"
            with cols[idx % 4]:
                if tid in earned:
                    st.markdown(f"""
                    <div class="trophy-card">
                        <div style="font-size:2.2em">{emoji}</div>
                        <div style="font-weight:900;font-size:0.85em">{name}</div>
                        <div style="font-size:0.72em;opacity:0.75">{desc}</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="trophy-locked">
                        <div style="font-size:2.2em">🔒</div>
                        <div style="font-weight:900;font-size:0.85em">{name}</div>
                        <div style="font-size:0.72em">{desc}</div>
                    </div>""", unsafe_allow_html=True)
            idx += 1

# ===== Text-to-Speech (Web Speech API) =====
def speak(text):
    safe_text = text.replace('"', '').replace("'", "")
    components.html(f"""
    <script>
        window.speechSynthesis.cancel();
        var u = new SpeechSynthesisUtterance("{safe_text}");
        u.lang = 'en-US';
        u.rate = 0.8;
        u.pitch = 1.0;
        window.speechSynthesis.speak(u);
    </script>
    """, height=0, width=0)

# ===== Sound Effects (MP3 files) =====
@st.cache_data
def _load_b64(filename):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def _play_mp3(filename, volume=0.85):
    b64 = _load_b64(filename)
    if not b64:
        return
    components.html(f"""<script>(function(){{
        try{{
            var a=new Audio("data:audio/mp3;base64,{b64}");
            a.volume={volume};
            a.play().catch(function(){{}});
        }}catch(e){{}}
    }})();</script>""", height=0, width=0)

# ===== Sound Pools =====
_SOUNDS_CORRECT = [
    "nba02.mp3",
    "basketball-swish_OMsr9CN.mp3",
    "jontron-yes.mp3",
    "point-basket.mp3",
    "its-a-very-nice.mp3",
    "bang-basketball_Y4765Ub.mp3",
    "ohhh-maaaah-gahhhhd.mp3",
    "pac-man-waka-waka.mp3",
]
_SOUNDS_TRIPLE = [
    "raul-lopez-triple-ratatatatatatata-mp3cut.mp3",
    "air-horn-basketball.mp3",
    "67_SQlv2Xv.mp3",
    "fighting.mp3",
    "faceit_accept_sound_epic_-8962405019821701368.mp3",
]
_SOUNDS_HEATING = [
    "hes-heating-up_e6Y3nOZ.mp3",
    "lebroooon-james.mp3",
    "who-r-u-1.mp3",
    "power-rangers-3-sec.mp3",
]
_SOUNDS_ON_FIRE = [
    "hes-on-fire-nba-jam.mp3",
    "ho-my-hes-on-fire.mp3",
    "dsp-baby.mp3",
    "faceit_accept_sound_epic_-8962405019821701368.mp3",
]
_SOUNDS_MVP = [
    "mvp-chant.mp3",
    "crowd-chanting-at-stadium.mp3",
    "what-are-you-playing-basketball-touchdown.mp3",
    "a-nba-1.mp3",
    "power-rangers-3-sec.mp3",
]
_SOUNDS_WRONG = [
    "defense-nba_BFEmUA8.mp3",
    "oh-stanley.mp3",
    "punch-gaming-sound-effect-hd_RzlG1GE.mp3",
    "finish-him.mp3",
    "67-meme_cdLcL5q.mp3",
    "hohoho-brook-risa.mp3",
    "universfield-game-over-deep-male-voice-clip-352695.mp3",
]

def play_success_sound(streak):
    if streak >= 10:
        _play_mp3(random.choice(_SOUNDS_MVP), 0.9)
    elif streak >= 7:
        _play_mp3(random.choice(_SOUNDS_ON_FIRE), 0.9)
    elif streak >= 5:
        _play_mp3(random.choice(_SOUNDS_HEATING), 0.85)
    elif streak >= 3:
        _play_mp3(random.choice(_SOUNDS_TRIPLE), 0.85)
    else:
        _play_mp3(random.choice(_SOUNDS_CORRECT), 0.8)

def play_error_sound():
    _play_mp3(random.choice(_SOUNDS_WRONG), 0.75)

# ===== Session State Init =====
def init_session():
    defaults = {
        "screen": "menu",
        "score": 0,
        "streak": 0,
        "current_topic": None,
        "current_question": None,
        "options": [],
        "game_mode": None,
        "feedback": None,
        "questions_answered": 0,
        "_actual_topic": None,
        "pending_sound": None,
        "player_name": None,
        "seen_words": [],
        "answer_history": [],   # last 5 answers: True=correct, False=wrong
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ===== Helper: Get Question =====
def get_new_question(topic, mode, seen_words):
    all_topic_words = WORD_DATA[topic]

    # Filter out recently seen words; if all were seen, reset history
    available = [w for w in all_topic_words if w['en'] not in seen_words]
    if not available:
        available = all_topic_words
        st.session_state.seen_words = []

    question = random.choice(available)

    # Build wrong options from all words except the correct one
    all_words = [(w['en'], w['he']) for t, wlist in WORD_DATA.items()
                 for w in wlist if w['en'] != question['en']]
    wrong_samples = random.sample(all_words, min(3, len(all_words)))
    if mode == "multiple_choice":
        options = [question['en']] + [w[0] for w in wrong_samples]
    else:
        options = [question['he']] + [w[1] for w in wrong_samples]
    random.shuffle(options)
    return question, options

def load_next_question():
    topic = st.session_state.current_topic
    mode = st.session_state.game_mode
    if topic == "all":
        actual = random.choice(list(WORD_DATA.keys()))
        st.session_state._actual_topic = actual
    else:
        st.session_state._actual_topic = topic

    seen = st.session_state.seen_words
    q, opts = get_new_question(st.session_state._actual_topic, mode, seen)

    # Track seen words — keep history at most half the topic size
    topic_size = len(WORD_DATA[st.session_state._actual_topic])
    max_history = max(1, topic_size // 2)
    seen.append(q['en'])
    if len(seen) > max_history:
        seen.pop(0)
    st.session_state.seen_words = seen

    st.session_state.current_question = q
    st.session_state.options = opts

# ===== SCREEN: Name Entry =====
def show_name_screen():
    st.markdown("""
    <div class="sports-row">
        <span class="b1">🏀</span>
        <span class="b2">⚽</span>
        <span class="b3">🎾</span>
        <span class="b4">🏐</span>
        <span class="b5">🏆</span>
        <span class="b6">⚾</span>
        <span class="b7">🏓</span>
        <span class="b8">🥊</span>
    </div>
    """, unsafe_allow_html=True)

    # Lottie basketball animation on welcome screen
    if LOTTIE_OK and LOTTIE_BALL:
        col_l, col_anim, col_r = st.columns([1, 2, 1])
        with col_anim:
            st_lottie(LOTTIE_BALL, height=130, loop=True, key="welcome_ball")

    st.markdown("""
    <div class="welcome-box">
        <div style="font-size:2.5em; font-weight:900; letter-spacing:1px; margin-bottom:10px;">
            🌟 Slam Dunk English 🌟
        </div>
        <div style="font-size:1.15em; opacity:0.92; margin-bottom:8px;">
            למד מילים באנגלית תוך כדי משחק!
        </div>
        <div style="font-size:1.4em; margin-top:10px;">
            🏀 &nbsp; ⚽ &nbsp; 🎾 &nbsp; 🏐 &nbsp; 🏈
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex; justify-content:space-around; margin:10px 0 20px 0; font-size:2em;">
        <span title="כדורסל">🏀</span>
        <span title="כדורגל">⚽</span>
        <span title="טניס">🎾</span>
        <span title="כדורעף">🏐</span>
        <span title="אמריקאי">🏈</span>
        <span title="בייסבול">⚾</span>
        <span title="פינג-פונג">🏓</span>
        <span title="אגרוף">🥊</span>
        <span title="שחייה">🏊</span>
        <span title="אופניים">🚴</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✍️ מה השם שלך?")
    name = st.text_input("שם", placeholder="כתוב את השם שלך כאן...",
                         label_visibility="collapsed", key="name_input")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 בוא נשחק!", key="start_btn"):
            if name.strip():
                st.session_state.player_name = name.strip()
                st.rerun()
            else:
                st.warning("✍️ כתוב את השם שלך קודם! 😊")

# ===== SCREEN: Menu =====
def show_menu():
    name = st.session_state.player_name
    st.markdown("""
    <div style="text-align:center;padding:5px 0">
        <span style="font-size:3em">🏀</span>
        <span style="font-size:2.5em"> ⚽ </span>
        <span style="font-size:3em">🏀</span>
    </div>
    """, unsafe_allow_html=True)
    st.title("Slam Dunk English")
    st.markdown(f"### 👋 שלום {name}! בחר מצב משחק:")

    stats = load_stats()
    total = stats["total_correct"] + stats["total_wrong"]
    accuracy = int(stats["total_correct"] / total * 100) if total > 0 else 0
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="score-box">✅ {stats["total_correct"]}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="streak-box">🔥 {stats.get("best_streak", 0)}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="topic-badge">🎯 {accuracy}%</div>', unsafe_allow_html=True)

    st.write("")
    modes = [
        ("🔤 רב ברירה", "multiple_choice", "עברית ← בחר באנגלית"),
        ("🔁 הפוך", "reverse", "אנגלית ← בחר בעברית"),
        ("🎧 הקשב", "listen", "שמע מילה ← בחר פירוש"),
        ("✏️ כתוב", "type_mode", "עברית ← כתוב באנגלית"),
    ]
    for label, mode, desc in modes:
        if st.button(f"{label}  —  {desc}", key=f"mode_{mode}"):
            st.session_state.game_mode = mode
            st.session_state.screen = "topic_select"
            st.rerun()

    st.divider()
    if st.button("📊 סטטיסטיקות שלי"):
        st.session_state.screen = "stats"
        st.rerun()

    # Trophy cabinet (compact view on menu)
    show_trophy_cabinet(compact=True)

# ===== SCREEN: Topic Select =====
def show_topic_select():
    mode_names = {
        "multiple_choice": "🔤 רב ברירה",
        "reverse": "🔁 הפוך",
        "listen": "🎧 הקשב",
        "type_mode": "✏️ כתוב",
    }
    st.title("בחר נושא")
    st.caption(f"מצב: {mode_names[st.session_state.game_mode]}")

    def start_game(topic):
        st.session_state.current_topic = topic
        st.session_state.score = 0
        st.session_state.streak = 0
        st.session_state.questions_answered = 0
        st.session_state.feedback = None
        st.session_state.answer_history = []
        st.session_state.seen_words = []
        load_next_question()
        st.session_state.screen = "game"
        st.rerun()

    if st.button("🌟 כל הנושאים יחד"):
        start_game("all")

    st.divider()
    for topic in WORD_DATA.keys():
        if st.button(topic):
            start_game(topic)

    if st.button("⬅️ חזרה לתפריט"):
        st.session_state.screen = "menu"
        st.rerun()

# ===== SCREEN: Game =====
def show_game():
    # Play pending sound (set during previous answer)
    if st.session_state.pending_sound:
        snd_type, snd_streak = st.session_state.pending_sound
        if snd_type == "correct":
            play_success_sound(snd_streak)
        else:
            play_error_sound()
        st.session_state.pending_sound = None

    mode = st.session_state.game_mode
    actual_topic = st.session_state._actual_topic or ""
    q = st.session_state.current_question
    if not q:
        st.error("שגיאה: אין שאלה. חוזר לתפריט...")
        st.session_state.screen = "menu"
        st.rerun()
        return

    # Header stats
    streak = st.session_state.streak
    streak_class = "streak-box-fire" if streak >= 5 else "streak-box"
    fires = "🔥" * min(streak, 5) if streak > 0 else "💤"
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="score-box">✅ {st.session_state.score}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="{streak_class}">{fires} {streak}</div>', unsafe_allow_html=True)
    with col3:
        emoji = actual_topic.split()[-1] if actual_topic else "?"
        st.markdown(f'<div class="topic-badge">{emoji}</div>', unsafe_allow_html=True)

    # 🔥 Fire Lottie when streak >= 5
    if streak >= 5 and LOTTIE_OK and LOTTIE_FIRE:
        col_l, col_mid, col_r = st.columns([1, 2, 1])
        with col_mid:
            st_lottie(LOTTIE_FIRE, height=90, loop=True, key=f"fire_{streak}")

    # 🏀 Basketball Lives Bar (last 5 answers)
    hist = st.session_state.answer_history
    if hist:
        balls = "".join("🏀" if h else "💀" for h in hist)
        empty = "⬜" * (15 - len(hist))
        st.markdown(f'<div class="lives-bar">{empty}{balls}</div>', unsafe_allow_html=True)

    st.write("")

    # --- Multiple Choice Mode ---
    if mode == "multiple_choice":
        st.markdown(f'<div class="big-word">{q["he"]}</div>', unsafe_allow_html=True)
        st.write("##### איך אומרים זאת באנגלית?")
        if st.button("🔊 הקשב לתשובה הנכונה"):
            speak(q["en"])
        for opt in st.session_state.options:
            if st.button(opt, key=f"opt_{st.session_state.screen}_{st.session_state.questions_answered}_{opt}"):
                correct = (opt == q["en"])
                record_answer(q["en"], actual_topic, correct)
                st.session_state.feedback = ("correct", q["en"]) if correct else ("wrong", q["en"])
                st.session_state.pending_sound = ("correct", st.session_state.streak) if correct else ("wrong", 0)
                st.session_state.questions_answered += 1
                if correct:
                    load_next_question()
                st.rerun()

    # --- Reverse Mode ---
    elif mode == "reverse":
        st.markdown(f'<div class="big-word"><span class="ltr">{q["en"]}</span></div>', unsafe_allow_html=True)
        if st.button("🔊 הקשב"):
            speak(q["en"])
        st.write("##### מה המשמעות בעברית?")
        for opt in st.session_state.options:
            if st.button(opt, key=f"opt_{st.session_state.screen}_{st.session_state.questions_answered}_{opt}"):
                correct = (opt == q["he"])
                record_answer(q["en"], actual_topic, correct)
                st.session_state.feedback = ("correct", q["he"]) if correct else ("wrong", q["he"])
                st.session_state.pending_sound = ("correct", st.session_state.streak) if correct else ("wrong", 0)
                st.session_state.questions_answered += 1
                if correct:
                    load_next_question()
                st.rerun()

    # --- Listen Mode ---
    elif mode == "listen":
        st.write("### 🎧 הקשב למילה ובחר את המשמעות בעברית")
        col_play, col_slow = st.columns(2)
        with col_play:
            if st.button("▶️ נגן מילה", key="play_normal"):
                speak(q["en"])
        with col_slow:
            if st.button("🐢 לאט יותר", key="play_slow"):
                safe = q["en"].replace('"', '').replace("'", "")
                components.html(f"""
                <script>
                    window.speechSynthesis.cancel();
                    var u = new SpeechSynthesisUtterance("{safe}");
                    u.lang = 'en-US'; u.rate = 0.5;
                    window.speechSynthesis.speak(u);
                </script>""", height=0, width=0)
        st.write("##### מה שמעת?")
        for opt in st.session_state.options:
            if st.button(opt, key=f"opt_{st.session_state.screen}_{st.session_state.questions_answered}_{opt}"):
                correct = (opt == q["he"])
                record_answer(q["en"], actual_topic, correct)
                st.session_state.feedback = ("correct", q["he"]) if correct else ("wrong", q["he"])
                st.session_state.pending_sound = ("correct", st.session_state.streak) if correct else ("wrong", 0)
                st.session_state.questions_answered += 1
                if correct:
                    load_next_question()
                st.rerun()

    # --- Type Mode ---
    elif mode == "type_mode":
        st.markdown(f'<div class="big-word">{q["he"]}</div>', unsafe_allow_html=True)
        st.write("##### כתוב באנגלית:")
        answer = st.text_input("תשובה", key=f"type_{st.session_state.questions_answered}",
                               placeholder="Type the English word...",
                               label_visibility="collapsed")
        col_check, col_hint, col_speak = st.columns(3)
        with col_check:
            if st.button("✅ בדוק"):
                if answer.strip():
                    correct = answer.strip().lower() == q["en"].lower()
                    record_answer(q["en"], actual_topic, correct)
                    st.session_state.feedback = ("correct", q["en"]) if correct else ("wrong", q["en"])
                    st.session_state.pending_sound = ("correct", st.session_state.streak) if correct else ("wrong", 0)
                    st.session_state.questions_answered += 1
                    if correct:
                        load_next_question()
                    st.rerun()
        with col_hint:
            if st.button("💡 רמז"):
                hint = q["en"][0] + " _ " * (len(q["en"]) - 1)
                st.info(f"רמז: **{hint}** ({len(q['en'])} אותיות)")
        with col_speak:
            if st.button("🔊 שמע"):
                speak(q["en"])

    # --- Feedback (with Lottie + Trophy Check) ---
    st.write("")
    if st.session_state.feedback:
        fb_type, correct_answer = st.session_state.feedback
        qa = st.session_state.questions_answered  # unique key suffix

        if fb_type == "correct":
            # Lottie success animation
            if LOTTIE_OK and LOTTIE_SUCCESS:
                col_l, col_mid, col_r = st.columns([1, 2, 1])
                with col_mid:
                    st_lottie(LOTTIE_SUCCESS, height=160, loop=False, key=f"lottie_ok_{qa}")

            # Success message
            streak = st.session_state.streak
            name = st.session_state.player_name
            if streak >= 10:
                st.success(f"👑 MVP! MVP! {name} — עשרה ברצף! אתה אגדה!! 🏀🏆🏀  **{correct_answer}**")
            elif streak >= 7:
                st.success(f"🔥 HE'S ON FIRE! {name} — שבע ברצף! בלתי עצור!  **{correct_answer}**")
            elif streak >= 5:
                st.success(f"♨️ He's heating up! {name} — חמש ברצף! אש!  **{correct_answer}**")
            elif streak >= 3:
                st.success(f"🎯 Triple! {name} — שלוש ברצף! כל הכבוד!  **{correct_answer}**")
            else:
                msgs = [
                    f"⚽ Goal! נכון, {name}!  **{correct_answer}**",
                    f"🏀 Slam Dunk! כל הכבוד {name}!  **{correct_answer}**",
                    f"🌟 מעולה {name}! נכון לגמרי!  **{correct_answer}**",
                    f"🎯 פגעת! כן {name}!  **{correct_answer}**",
                ]
                st.success(random.choice(msgs))

            if mode in ["multiple_choice", "type_mode"]:
                speak(correct_answer)

            # 🏆 Check for new trophies
            new_trophies = check_trophies()
            for emoji, t_name, t_desc in new_trophies:
                st.balloons()
                st.markdown(
                    f'<div class="new-trophy-banner">🎉 גביע חדש! {emoji} <strong>{t_name}</strong> — {t_desc}</div>',
                    unsafe_allow_html=True
                )
                if LOTTIE_OK and LOTTIE_TROPHY:
                    col_l, col_mid, col_r = st.columns([1, 2, 1])
                    with col_mid:
                        st_lottie(LOTTIE_TROPHY, height=130, loop=False, key=f"lottie_trophy_{qa}_{t_name}")

        else:
            # Lottie fail animation
            if LOTTIE_OK and LOTTIE_FAIL:
                col_l, col_mid, col_r = st.columns([1, 2, 1])
                with col_mid:
                    st_lottie(LOTTIE_FAIL, height=160, loop=False, key=f"lottie_fail_{qa}")

            st.error(f"❌ לא נכון. התשובה הנכונה היא: **{correct_answer}**")
            col_retry, col_next = st.columns(2)
            with col_retry:
                if st.button("🔄 נסה שוב"):
                    st.session_state.feedback = None
                    st.rerun()
            with col_next:
                if st.button("⏭️ שאלה הבאה"):
                    st.session_state.feedback = None
                    load_next_question()
                    st.rerun()

    st.divider()
    if st.button("🏠 תפריט ראשי"):
        st.session_state.screen = "menu"
        st.session_state.feedback = None
        st.rerun()

# ===== SCREEN: Stats =====
def show_stats():
    name = st.session_state.player_name
    st.title(f"📊 הסטטיסטיקות של {name}")
    stats = load_stats()
    total = stats["total_correct"] + stats["total_wrong"]
    accuracy = int(stats["total_correct"] / total * 100) if total > 0 else 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ תשובות נכונות", stats["total_correct"])
        st.metric("🎯 דיוק", f"{accuracy}%")
    with col2:
        st.metric("❌ תשובות שגויות", stats["total_wrong"])
        st.metric("🔥 שיא רצף", stats.get("best_streak", 0))

    st.divider()

    # Topic breakdown
    if stats.get("topics"):
        st.write("### ביצועים לפי נושא:")
        for topic, t_stats in sorted(stats["topics"].items(),
                                     key=lambda x: x[1]["correct"], reverse=True):
            t_total = t_stats["correct"] + t_stats["wrong"]
            t_acc = int(t_stats["correct"] / t_total * 100) if t_total > 0 else 0
            stars = "⭐" * (t_acc // 20)
            st.progress(t_acc / 100, text=f"{topic}  —  {t_acc}% {stars}  ({t_stats['correct']}/{t_total})")

    # Words needing practice
    if stats.get("words"):
        hard_words = [(w, d) for w, d in stats["words"].items()
                      if d["wrong"] > d.get("correct", 0)]
        if hard_words:
            st.divider()
            st.write("### 💪 מילים שכדאי לתרגל יותר:")
            for word, d in sorted(hard_words, key=lambda x: x[1]["wrong"], reverse=True)[:8]:
                if st.button(f"🔊 {word}  ({d['wrong']} שגיאות)", key=f"speak_{word}"):
                    speak(word)

    # Full trophy cabinet
    show_trophy_cabinet(compact=False)

    st.divider()
    col_back, col_reset = st.columns(2)
    with col_back:
        if st.button("⬅️ חזרה לתפריט"):
            st.session_state.screen = "menu"
            st.rerun()
    with col_reset:
        if st.button("🗑️ אפס סטטיסטיקות"):
            save_stats({"total_correct": 0, "total_wrong": 0,
                        "best_streak": 0, "words": {}, "topics": {}, "trophies": []})
            st.success("הסטטיסטיקות אופסו!")
            st.rerun()

# ===== Router =====
if not st.session_state.player_name:
    show_name_screen()
else:
    screen = st.session_state.screen
    if screen == "menu":
        show_menu()
    elif screen == "topic_select":
        show_topic_select()
    elif screen == "game":
        show_game()
    elif screen == "stats":
        show_stats()
