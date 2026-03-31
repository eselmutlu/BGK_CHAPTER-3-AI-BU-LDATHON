import hashlib
import json
import os
import sqlite3
from io import BytesIO
from datetime import datetime
from typing import Any

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from PIL import Image
import base64
import google.generativeai as genai

load_dotenv()

# Global ilaç hafızası - tüm sekmeler tarafından paylaşılır
if 'active_drug' not in st.session_state:
    st.session_state['active_drug'] = ''

if 'manual_drug' not in st.session_state:
    st.session_state['manual_drug'] = ''

st.set_page_config(page_title="Gumus Asistan", page_icon="💊", layout="wide")

st.markdown(
    """
<style>
/* --- Page background (purple/blue gradient) --- */
.stApp {
  background: radial-gradient(1200px 800px at 15% 10%, rgba(124, 58, 237, 0.45), transparent 60%),
              radial-gradient(1000px 700px at 85% 0%, rgba(59, 130, 246, 0.45), transparent 55%),
              linear-gradient(135deg, #0b1020 0%, #0d1633 35%, #0a0f1f 100%);
}

/* Reduce top padding and align content nicely */
.block-container {
  padding-top: 2rem;
  padding-bottom: 3rem;
  max-width: 1200px;
}

/* --- Hero header --- */
.ga-hero {
  border-radius: 20px;
  padding: 22px 22px;
  background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(59,130,246,0.18));
  border: 1px solid rgba(255,255,255,0.10);
  box-shadow: 0 20px 60px rgba(0,0,0,0.35);
  color: #e5e7eb;
  margin-bottom: 18px;
}
.ga-hero h1 {
  font-size: 34px;
  line-height: 1.15;
  margin: 0 0 6px 0;
  letter-spacing: -0.02em;
}
.ga-hero p {
  margin: 0;
  color: rgba(229,231,235,0.85);
  font-size: 15px;
}
.ga-badge {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  background: rgba(255,255,255,0.10);
  border: 1px solid rgba(255,255,255,0.12);
  margin-bottom: 10px;
}

/* --- Card surface --- */
.ga-card {
  background: rgba(255,255,255,0.96);
  border: 1px solid rgba(15,23,42,0.08);
  border-radius: 18px;
  padding: 18px 18px;
  box-shadow: 0 18px 45px rgba(0,0,0,0.25);
}
.ga-card h2, .ga-card h3 {
  color: #0f172a;
  margin-top: 0;
}
.ga-muted {
  color: rgba(15,23,42,0.70);
  font-size: 14px;
}

/* --- Result cards --- */
.ga-result {
  background: rgba(255,255,255,0.98);
  border: 1px solid rgba(15,23,42,0.10);
  border-radius: 16px;
  padding: 14px 14px;
  box-shadow: 0 14px 35px rgba(0,0,0,0.18);
}
.ga-result + .ga-result { margin-top: 12px; }
.ga-result-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 10px;
}
.ga-result-title h3 {
  margin: 0;
  font-size: 16px;
  color: #0f172a;
}
.ga-badge-risk {
  font-size: 12px;
  font-weight: 750;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(15,23,42,0.12);
}
.ga-risk-low    { background: rgba(16,185,129,0.15); color: #065f46; border-color: rgba(16,185,129,0.25); }
.ga-risk-medium { background: rgba(245,158,11,0.18); color: #92400e; border-color: rgba(245,158,11,0.28); }
.ga-risk-high   { background: rgba(239,68,68,0.15); color: #991b1b; border-color: rgba(239,68,68,0.25); }

.ga-kv {
  display: grid;
  grid-template-columns: 180px 1fr;
  gap: 8px 12px;
  align-items: start;
  font-size: 14px;
}
.ga-k { color: rgba(15,23,42,0.65); font-weight: 650; }
.ga-v { color: #0f172a; white-space: pre-wrap; }

/* --- Mobile responsiveness --- */
@media (max-width: 640px) {
  .block-container {
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 1.25rem;
  }

  .ga-hero {
    padding: 16px 16px;
    border-radius: 16px;
  }

  .ga-hero h1 {
    font-size: 28px;
  }

  .ga-card {
    padding: 14px 14px;
    border-radius: 16px;
  }

  /* Key/Value grid stacks */
  .ga-kv {
    grid-template-columns: 1fr;
    gap: 6px 0;
  }

  /* Risk header stacks */
  .ga-result-title {
    flex-direction: column;
    align-items: flex-start;
  }

  /* Full-width buttons */
  div[data-testid="stButton"] > button {
    width: 100% !important;
  }
}

/* --- Buttons (colorful) --- */
div[data-testid="stButton"] > button {
  background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%) !important;
  color: white !important;
  border: 0 !important;
  padding: 0.7rem 1rem !important;
  border-radius: 12px !important;
  font-weight: 650 !important;
  box-shadow: 0 10px 25px rgba(37, 99, 235, 0.35);
  transition: transform 120ms ease, box-shadow 120ms ease, filter 120ms ease;
}
div[data-testid="stButton"] > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 30px rgba(124, 58, 237, 0.35);
  filter: brightness(1.03);
}
div[data-testid="stButton"] > button:active {
  transform: translateY(0px) scale(0.99);
}

/* Inputs */
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
  border-radius: 12px !important;
}

/* Tabs look */
button[data-baseweb="tab"] {
  border-radius: 12px 12px 0 0 !important;
}
div[data-baseweb="tab-list"] {
  gap: 6px;
}

/* Code blocks to look cleaner */
pre {
  border-radius: 12px !important;
}

/* Hide Streamlit default footer/menu for cleaner look */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)


def init_db() -> None:
    conn = sqlite3.connect("gumus_asistan.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            input_text TEXT NOT NULL,
            output_text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medication_name TEXT NOT NULL,
            remind_time TEXT NOT NULL, -- HH:MM
            enabled INTEGER NOT NULL DEFAULT 1,
            last_trigger_date TEXT -- YYYY-MM-DD
        )
        """
    )
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    if len(username) < 3:
        return False, "Kullanici adi en az 3 karakter olmali."
    if len(password) < 4:
        return False, "Sifre en az 4 karakter olmali."

    conn = sqlite3.connect("gumus_asistan.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, hash_password(password), datetime.utcnow().isoformat()),
        )
        conn.commit()
        return True, "Kayit basarili. Giris yapabilirsiniz."
    except sqlite3.IntegrityError:
        return False, "Bu kullanici adi zaten kayitli."
    finally:
        conn.close()


def verify_user(username: str, password: str) -> bool:
    conn = sqlite3.connect("gumus_asistan.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password_hash FROM users WHERE username = ? LIMIT 1",
        (username.strip(),),
    )
    row = cursor.fetchone()
    conn.close()
    if not row:
        return False
    return row[0] == hash_password(password)


def render_auth_gate() -> bool:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    if st.session_state.logged_in:
        return True

    st.markdown(
        """
<div class="ga-card">
  <h3 style="margin:0 0 8px 0;">🔐 Kullanici Girisi</h3>
  <div class="ga-muted">Uygulamayi kullanmak icin giris yapin veya yeni hesap olusturun.</div>
</div>
""",
        unsafe_allow_html=True,
    )

    login_tab, register_tab = st.tabs(["🔑 Giris Yap", "🆕 Kayit Ol"])

    with login_tab:
        l_user = st.text_input("👤 Kullanici adi", key="login_user")
        l_pass = st.text_input("🔒 Sifre", type="password", key="login_pass")
        if st.button("✅ Giris Yap", key="login_btn", use_container_width=True):
            if verify_user(l_user, l_pass):
                st.session_state.logged_in = True
                st.session_state.username = l_user.strip()
                st.success("Giris basarili.")
                st.rerun()
            else:
                st.error("Kullanici adi veya sifre hatali.")

    with register_tab:
        r_user = st.text_input("👤 Yeni kullanici adi", key="register_user")
        r_pass = st.text_input("🔒 Yeni sifre", type="password", key="register_pass")
        if st.button("📝 Kayit Ol", key="register_btn", use_container_width=True):
            ok, msg = create_user(r_user, r_pass)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    return False


def save_analysis(kind: str, input_text: str, output_text: str) -> None:
    conn = sqlite3.connect("gumus_asistan.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO analyses (kind, input_text, output_text, created_at) VALUES (?, ?, ?, ?)",
        (kind, input_text, output_text, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def get_latest_analyses(limit: int = 10) -> list[tuple[Any, ...]]:
    conn = sqlite3.connect("gumus_asistan.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT kind, input_text, output_text, created_at FROM analyses ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_reminder(medication_name: str, remind_time: str) -> None:
    conn = sqlite3.connect("gumus_asistan.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reminders (medication_name, remind_time, enabled, last_trigger_date) VALUES (?, ?, 1, NULL)",
        (medication_name.strip(), remind_time.strip()),
    )
    conn.commit()
    conn.close()


def delete_reminder(reminder_id: int) -> None:
    conn = sqlite3.connect("gumus_asistan.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    conn.commit()
    conn.close()


def list_reminders() -> list[tuple[Any, ...]]:
    conn = sqlite3.connect("gumus_asistan.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, medication_name, remind_time, enabled, last_trigger_date FROM reminders ORDER BY remind_time ASC, id ASC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def mark_triggered(reminder_id: int, date_yyyy_mm_dd: str) -> None:
    conn = sqlite3.connect("gumus_asistan.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE reminders SET last_trigger_date = ? WHERE id = ?",
        (date_yyyy_mm_dd, reminder_id),
    )
    conn.commit()
    conn.close()


def notify_browser(title: str, body: str) -> None:
    # Uses browser Notification API; requires permission.
    # Streamlit reruns will re-inject this snippet when due reminders exist.
    safe_title = json.dumps(title, ensure_ascii=False)
    safe_body = json.dumps(body, ensure_ascii=False)
    components.html(
        f"""
<script>
(function() {{
  if (!("Notification" in window)) return;
  const title = {safe_title};
  const body = {safe_body};
  try {{
    if (Notification.permission === "granted") {{
      new Notification(title, {{ body }});
    }}
  }} catch (e) {{}}
}})();
</script>
""",
        height=0,
    )


def init_conversation_memory() -> None:
    if "memory_history" not in st.session_state:
        st.session_state.memory_history = []
    if "remembered_medications" not in st.session_state:
        st.session_state.remembered_medications = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    # Global ilaç bilgisi - tüm sekmeler tarafından paylaşılır
    if "current_drug" not in st.session_state:
        st.session_state.current_drug = st.session_state.get("remembered_medications", "")
    if "shared_drug" not in st.session_state:
        st.session_state.shared_drug = ""
    if "drug_source" not in st.session_state:
        st.session_state.drug_source = ""
    if "manual_drug" not in st.session_state:
        st.session_state.manual_drug = ""


def add_memory_entry(kind: str, content: str) -> None:
    history = st.session_state.memory_history
    history.append(
        {
            "ts": datetime.utcnow().isoformat(),
            "kind": kind,
            "content": content.strip(),
        }
    )
    # Keep only recent context to avoid oversized prompts.
    st.session_state.memory_history = history[-12:]


def format_memory_context() -> str:
    history = st.session_state.get("memory_history", [])
    if not history:
        return "Onceki konusma kaydi yok."
    lines = []
    for item in history[-8:]:
        lines.append(f"[{item['kind']}] {item['content']}")
    remembered = st.session_state.get("remembered_medications", "").strip()
    if remembered:
        lines.append(f"[remembered_medications] {remembered}")
    return "\n".join(lines)


def add_chat_history_entry(kind: str, user_input: str, assistant_output: str) -> None:
    history = st.session_state.get("chat_history", [])
    history.append(
        {
            "ts": datetime.utcnow().isoformat(),
            "kind": kind,
            "user_input": user_input.strip(),
            "assistant_output": assistant_output.strip(),
        }
    )
    st.session_state.chat_history = history[-10:]


def format_chat_history_context() -> str:
    history = st.session_state.get("chat_history", [])
    if not history:
        return "Onceki analiz gecmisi yok."
    lines: list[str] = []
    for item in history[-6:]:
        lines.append(f"[{item['kind']}] Kullanici: {item['user_input']}")
        lines.append(f"[{item['kind']}] Asistan: {item['assistant_output'][:240]}")
    return "\n".join(lines)


def build_ai_context() -> str:
    memory_context = format_memory_context()
    chat_context = format_chat_history_context()
    return f"{memory_context}\n\n--- Chat History ---\n{chat_context}"


def parse_medication_from_user_input(user_input: str) -> str:
    text = user_input.strip()
    if "Ilaclar=" in text:
        med = text.split("Ilaclar=", 1)[1].split(";", 1)[0].strip()
        return med if med else "Belirtilmedi"
    return "Belirtilmedi"


def parse_risk_display_from_output(raw_output: str) -> tuple[str, str]:
    parsed = try_parse_json(raw_output) or {}
    risk = normalize_risk(parsed.get("risk")) or normalize_risk(parsed.get("risk_level"))
    if risk == "high":
        return "🔴", "Yuksek"
    if risk == "medium":
        return "🟡", "Orta"
    if risk == "low":
        return "🟢", "Dusuk"
    return "⚪", "Belirsiz"


def extract_last_symptom_from_chat_history() -> str:
    history = st.session_state.get("chat_history", [])
    for item in reversed(history):
        if item.get("kind") != "symptom_analysis":
            continue
        user_input = str(item.get("user_input", ""))
        marker = "Semptomlar="
        if marker in user_input:
            return user_input.split(marker, 1)[1].strip()
        return user_input.strip()
    return ""


def render_reminder_permission_controls() -> None:
    st.markdown("**🔔 Bildirim izni**")
    st.caption("Hatırlatıcı bildirimleri için tarayıcı bildirim izni gerekir.")

    components.html(
        """
<script>
window.__ga_request_notif_perm = async function() {
  if (!("Notification" in window)) return "unsupported";
  const p = await Notification.requestPermission();
  return p;
}
</script>
""",
        height=0,
    )
    components.html(
        """
<button
  style="
    width:100%;
    padding:10px 12px;
    border-radius:12px;
    border:1px solid rgba(255,255,255,0.18);
    background: rgba(255,255,255,0.10);
    color: white;
    font-weight: 700;
    cursor: pointer;
  "
  onclick="window.__ga_request_notif_perm && window.__ga_request_notif_perm();"
>
  🔔 Bildirim izni ver
</button>
""",
        height=52,
    )


def run_due_reminders_tick() -> None:
    """
    Checks reminders once per rerun and triggers browser notifications when due.
    Strategy: user triggers a rerun via refresh button; when current HH:MM
    matches and reminder wasn't triggered today, send notification and mark triggered.
    """
    now = datetime.now()
    now_hhmm = now.strftime("%H:%M")
    today = now.strftime("%Y-%m-%d")

    rows = list_reminders()
    for reminder_id, medication_name, remind_time, enabled, last_trigger_date in rows:
        if not enabled:
            continue
        if remind_time != now_hhmm:
            continue
        if last_trigger_date == today:
            continue
        notify_browser("⏰ Ilac Hatirlatici", f"💊 {medication_name} - Saat {remind_time}")
        mark_triggered(int(reminder_id), today)


def extract_medication_name_with_gemini(image: Image.Image) -> str:
    """
    Google Gemini 1.5 Flash'ı kullanarak ilaç kutusundaki metinleri OCR yapar.
    Sadece ticari ilaç ismini (örn: Aferin Sinüs) döndürür.
    """
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Tanimlanamadi"
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Resmi base64'e çevir
        image_rgb = image.convert("RGB")
        buffered = BytesIO()
        image_rgb.save(buffered, format="JPEG")
        b64_image = base64.b64encode(buffered.getvalue()).decode()
        
        # Gemini'ye OCR ve ilaç ismi çıkarması için iste - DETAYLI TLİMATLAR
        prompt = """Sen uzman bir eczacı asistanısın. Görevin, yüklenen görseldeki ilaç kutusunun ticari markasını (brand name) tespit etmektir. Kutuda yazan yardımcı maddeleri (Parasetamol, Psödoefedrin vb.) değil, sadece kutunun en üstünde veya en büyük yazılan ismi döndür. Sonuç sadece ilaç ismi olmalı (Örn: 'Aferin Sinüs'), başka hiçbir açıklama yapma."""
        
        message = model.generate_content([
            {"mime_type": "image/jpeg", "data": b64_image},
            prompt
        ])
        
        medication_name = message.text.strip() if message.text else "Tanimlanamadi"
        # Sadece ilk satırı al ve temizle
        medication_name = medication_name.split('\n')[0].strip()
        return medication_name if medication_name and medication_name.lower() != "tanimlanamadi" else "Tanimlanamadi"
    
    except Exception as e:
        st.warning(f"⚠️ Google Gemini OCR hatası: {e}")
        return "Tanimlanamadi"


def try_parse_json(raw_text: str) -> dict[str, Any] | None:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
        return None
    except Exception:
        return None


def normalize_risk(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    v = value.strip().lower()
    if v in {"low", "medium", "high"}:
        return v
    return None


def build_pdf_report_bytes(
    report_title: str,
    created_at_iso: str,
    input_summary: str,
    raw_result: str,
) -> bytes | None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfgen import canvas
    except Exception:
        return None

    # Optional: register a Unicode-capable font if available on Windows.
    # If this fails, PDF will still be generated with default fonts.
    try:
        windows_font = r"C:\Windows\Fonts\arial.ttf"
        if os.path.exists(windows_font):
            pdfmetrics.registerFont(TTFont("GA_Arial", windows_font))
            font_name = "GA_Arial"
        else:
            font_name = "Helvetica"
    except Exception:
        font_name = "Helvetica"

    data = try_parse_json(raw_result) or {}
    risk = normalize_risk(data.get("risk")) or normalize_risk(data.get("risk_level"))

    medication_name = ""
    if isinstance(data, dict):
        medication_name = str(data.get("medication_name") or "").strip()
    if not medication_name:
        # best-effort: look for "Warfarin" etc. in input summary
        medication_name = input_summary.splitlines()[0].strip() if input_summary else ""

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x = 18 * mm
    y = height - 18 * mm
    line_h = 6 * mm

    def draw_line(text: str, bold: bool = False) -> None:
        nonlocal y
        if y < 18 * mm:
            c.showPage()
            y = height - 18 * mm
            c.setFont(font_name, 11)
        c.setFont(font_name, 12 if bold else 11)
        c.drawString(x, y, text[:1500])
        y -= line_h

    draw_line("Gumus Asistan - Analiz Raporu", bold=True)
    draw_line(report_title, bold=True)
    draw_line(f"Tarih: {created_at_iso[:19].replace('T', ' ')} (UTC)")
    if medication_name:
        draw_line(f"Ilac: {medication_name}")

    draw_line("")
    draw_line("Risk Durumu", bold=True)
    if risk == "high":
        draw_line("Seviye: YUKSEK")
    elif risk == "medium":
        draw_line("Seviye: ORTA")
    elif risk == "low":
        draw_line("Seviye: DUSUK")
    else:
        draw_line("Seviye: Belirtilmedi")

    draw_line("")
    draw_line("Analiz Ozeti", bold=True)

    # Only user-facing fields, no technical/internal keys.
    user_facing_key_order = [
        "summary",
        "possible_relation",
        "recommended_action",
        "next_step",
        "notes",
        "medication_name",
        "dosage",
        "confidence",
    ]
    key_labels = {
        "summary": "Kisa Aciklama",
        "possible_relation": "Olasi Iliski",
        "recommended_action": "Onerilen Adim",
        "next_step": "Sonraki Adim",
        "notes": "Not",
        "medication_name": "Tanimlanan Ilac",
        "dosage": "Dozaj",
        "confidence": "Guven Duzeyi",
    }

    rendered_any = False
    if isinstance(data, dict) and data:
        for k in user_facing_key_order:
            if k not in data:
                continue
            v = data.get(k)
            if v in (None, "", []):
                continue
            rendered_any = True
            value = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
            label = key_labels.get(k, k)
            if len(value) <= 110:
                draw_line(f"{label}: {value}")
            else:
                draw_line(f"{label}:")
                for i in range(0, len(value), 110):
                    draw_line(f"  {value[i:i+110]}")

    if not rendered_any:
        draw_line("Analiz sonucu olusturuldu. Ayrintilar uygulama ekraninda gorulebilir.")

    # Geçmiş Kayıtlar bölümünü ekle
    chat_history = st.session_state.get("chat_history", [])
    if chat_history:
        draw_line("")
        draw_line("Gecmis Kayitlar", bold=True)
        draw_line("(Son analizlerin ozeti)")
        
        # Son 5 analizi göster
        for idx, item in enumerate(reversed(chat_history[-5:])):
            ts = str(item.get("ts", ""))[:19].replace("T", " ")
            user_input = str(item.get("user_input", ""))[:100]
            item_kind = str(item.get("kind", "")).replace("_", " ").title()
            
            draw_line(f"#{idx + 1} {item_kind} - {ts}")
            draw_line(f"  Girdi: {user_input}")
            
            # Çıktıdan risk seviyesini çıkar
            assistant_output = str(item.get("assistant_output", ""))
            parsed_output = try_parse_json(assistant_output) or {}
            item_risk = normalize_risk(parsed_output.get("risk")) or normalize_risk(parsed_output.get("risk_level"))
            if item_risk:
                risk_text = {"low": "DUSUK", "medium": "ORTA", "high": "YUKSEK"}.get(item_risk, "")
                draw_line(f"  Risk: {risk_text}")

    draw_line("")
    draw_line("Hukuki Uyari", bold=True)
    draw_line("Bu rapor bilgilendirme amaclidir; doktor muayenesi veya tedavi onerisi yerine gecmez.")
    draw_line("Kisisel saglik verilerinizin gizliligi KVKK kapsaminda korunmalidir.")

    c.showPage()
    c.save()
    return buffer.getvalue()


def render_result_card(title: str, raw_result: str, *, input_summary: str = "", created_at_iso: str | None = None) -> None:
    data = try_parse_json(raw_result)
    risk = None
    if isinstance(data, dict):
        risk = normalize_risk(data.get("risk")) or normalize_risk(data.get("risk_level"))

    risk_label = {"low": "🟢 LOW", "medium": "🟡 MEDIUM", "high": "🔴 HIGH"}.get(risk, "ℹ️ RESULT")
    risk_class = {"low": "ga-risk-low", "medium": "ga-risk-medium", "high": "ga-risk-high"}.get(
        risk, ""
    )

    st.markdown(
        f"""
<div class="ga-result">
  <div class="ga-result-title">
    <h3>{title}</h3>
    <span class="ga-badge-risk {risk_class}">{risk_label}</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    created_at_iso = created_at_iso or datetime.utcnow().isoformat()
    pdf_bytes = build_pdf_report_bytes(title, created_at_iso, input_summary, raw_result)
    if pdf_bytes is None:
        st.caption("📄 PDF icin `reportlab` kurulumu gerekli. (pip install -r requirements.txt)")
    else:
        if "download_button_index" not in st.session_state:
            st.session_state.download_button_index = 0
        i = st.session_state.download_button_index
        st.session_state.download_button_index += 1

        safe_name = (
            title.lower()
            .replace(" ", "_")
            .replace("ı", "i")
            .replace("ğ", "g")
            .replace("ş", "s")
            .replace("ç", "c")
            .replace("ö", "o")
            .replace("ü", "u")
        )
        # Dosya ismine saat bilgisi ekle (HH:MM:SS)
        time_part = created_at_iso[11:19].replace(":", "-")
        st.download_button(
            "📄 PDF indir",
            data=pdf_bytes,
            file_name=f"gumus_asistan_{safe_name}_{created_at_iso[:10]}_{time_part}.pdf",
            mime="application/pdf",
            key=f"download_{i}",
            use_container_width=True,
        )

    if data:
        preferred_keys = [
            "medication_name",
            "dosage",
            "confidence",
            "summary",
            "recommended_action",
            "possible_relation",
            "next_step",
            "notes",
            "medical_disclaimer",
        ]
        shown = set()
        kv_items: list[tuple[str, Any]] = []
        for k in preferred_keys:
            if k in data:
                kv_items.append((k, data.get(k)))
                shown.add(k)
        for k, v in data.items():
            if k not in shown and k not in {"risk", "risk_level"}:
                kv_items.append((k, v))

        st.markdown('<div class="ga-kv">', unsafe_allow_html=True)
        for k, v in kv_items:
            st.markdown(f'<div class="ga-k">{k}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="ga-v">{json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("🔎 Ham JSON"):
            st.json(data)
    else:
        st.warning("Cikti JSON formatinda okunamadi. Ham sonuc asagida.")
        st.text(raw_result)


def identify_medication(image: Image.Image) -> str:
    """
    Google Gemini 1.5 Flash OCR kullanarak ilaç ismini tanımlar.
    Sadece ticari ilaç ismini döndürür (örn: Aferin Sinüs).
    """
    medication_name = extract_medication_name_with_gemini(image)
    result = {
        "medication_name": medication_name,
        "dosage": "Bilinmiyor",
        "confidence": 0.85 if medication_name and medication_name.lower() != "tanimlanamadi" else 0.2,
        "notes": "Sonuc, Google Gemini 1.5 Flash OCR modelinin kutudaki metinleri okuyarak uretilmistir.",
        "medical_disclaimer": "Bu uygulama tibbi tavsiye vermez.",
    }
    return json.dumps(result, ensure_ascii=False)


def analyze_food_interaction(medications: str, foods: str, memory_context: str) -> str:
    text = f"{medications} {foods} {memory_context}".lower()
    if "warfarin" in text and ("ispanak" in text or "spinach" in text):
        risk = "high"
        summary = "Warfarin ile ispanak birlikte kullanimi dikkat gerektirir."
        action = "Doz ve beslenme duzeni icin doktorunuza danisin."
    elif "greyfurt" in text or "grapefruit" in text:
        risk = "medium"
        summary = "Greyfurt bazi ilaclarla etkilesime girebilir."
        action = "Ilac prospektusunu kontrol edin ve eczaciya danisin."
    else:
        risk = "low"
        summary = "Belirgin kritik etkilesim sinyali bulunmadi."
        action = "Yine de profesyonel gorus almaniz onerilir."

    # Onceki analizleri kontrol et
    chat_history = st.session_state.get("chat_history", [])
    prior_context = ""
    if chat_history:
        prior_context = "Önceki analizinize göre, "

    result = {
        "risk": risk,
        "summary": f"{prior_context}{summary}" if prior_context else summary,
        "recommended_action": action,
        "context_used": memory_context[:500],
        "medical_disclaimer": "Bu uygulama tibbi tavsiye vermez.",
    }
    return json.dumps(result, ensure_ascii=False)


def analyze_symptoms(medications: str, symptoms: str, memory_context: str) -> str:
    system_message = (
        "Sen, yaslilara yardimci olan nazik, dikkatli ve guvenilir bir saglik asistanisin. "
        "Tibbi terimleri basitce acikla, riskli durumlarda mutlaka doktora yonlendir ve "
        "hukuki bir dille (KVKK uyarisi gibi) analizinin bir doktor tavsiyesi olmadigini belirt."
    )
    text = f"{medications} {symptoms} {memory_context}".lower()
    if any(x in text for x in ["nefes", "gogus agrisi", "bayilma", "chest pain", "faint"]):
        risk = "high"
        relation = "Ciddi bir durum olasiligi dislanamaz."
        next_step = "Acil saglik hizmetine basvurun."
    elif any(x in text for x in ["bas donmesi", "halsizlik", "mide bulantisi", "dizziness", "nausea"]):
        risk = "medium"
        relation = "Ilac yan etkisi veya farkli bir neden ile iliskili olabilir."
        next_step = "Kisa surede doktorunuza danisin ve semptom gunlugu tutun."
    else:
        risk = "low"
        relation = "Belirgin yuksek risk sinyali yok."
        next_step = "Semptomlar artarsa doktorunuza basvurun."

    last_symptom = extract_last_symptom_from_chat_history()
    if last_symptom:
        follow_up_question = (
            f"Onceki semptomunuz '{last_symptom}' idi. Bu belirtiye gore su an daha iyi misiniz, ayni mi, yoksa daha kotu mu?"
        )
    else:
        follow_up_question = (
            "Oncesinde paylastiginiz bilgilere gore, semptomlarinizda onceki duruma gore bir artis veya azalis oldu mu?"
        )

    # Onceki analizlere göre başlama mesajı
    chat_history = st.session_state.get("chat_history", [])
    prior_prefix = ""
    if chat_history:
        prior_prefix = "Önceki analizinize göre, "

    risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}[risk]
    markdown_response = f"""
### 🩺 Semptom Analizi Sonucu

| Alan | Deger |
|---|---|
| Risk Seviyesi | {risk_emoji} **{risk.upper()}** |
| Olasi Iliski | {prior_prefix}{relation} |
| Onerilen Adim | {next_step} |

#### 📌 Aciklama (Basit Dil)
- Semptomlariniz ilaclarla iliskili olabilir, ancak bu sonuc kesin tani koymaz.
- Belirtiler siddetlenirse gecikmeden saglik profesyoneline basvurun.

#### ⚖️ Hukuki Uyari (KVKK)
Bu analiz, kisinin paylastigi veriler uzerinden bilgilendirme amacli otomatik bir degerlendirmedir.  
**Doktor muayenesi, tani veya tedavi yerine gecmez.** Kisisel saglik verilerinizin gizliligi KVKK kapsaminda korunmalidir.

#### 💬 Gecmise Dayali Takip Sorusu
{follow_up_question}
"""

    result = {
        "system_message_profile": system_message,
        "possible_relation": f"{prior_prefix}{relation}" if prior_prefix else relation,
        "risk_level": risk,
        "next_step": next_step,
        "context_used": memory_context[:1000],
        "context_chat_history_attached": "chat history" in memory_context.lower(),
        "last_symptom_from_chat_history": last_symptom,
        "markdown_response": markdown_response.strip(),
        "medical_disclaimer": "Bu uygulama tibbi tavsiye vermez.",
    }
    return json.dumps(result, ensure_ascii=False)


def render_history() -> None:
    st.subheader("🕘 Son Analizler")
    rows = get_latest_analyses()
    if not rows:
        st.info("🗂️ Kayitli analiz yok.")
        return

    for kind, input_text, output_text, created_at in rows:
        with st.expander(f"🧾 {kind}  ·  {created_at}"):
            st.markdown("**🧩 Girdi**")
            st.code(input_text)
            st.markdown("**📤 Cikti**")
            render_result_card("📦 Kayitli sonuc", output_text, input_summary=input_text, created_at_iso=created_at)


def main() -> None:
    init_db()
    if not render_auth_gate():
        return
    init_conversation_memory()

    st.markdown(
        """
<div class="ga-hero">
  <div class="ga-badge">✨ AI-Powered Health Companion</div>
  <h1>💊 Gumus Asistan</h1>
  <p>Ilac yonetimi, gida etkilesimleri ve semptom takibi icin guvenlik odakli bir yol arkadasi.</p>
</div>
""",
        unsafe_allow_html=True,
    )
    st.info("⚠️ Bu uygulama tibbi tavsiye vermez.")

    # Fire due reminders on every rerun.
    run_due_reminders_tick()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📸 Ilac Tanima", "🍽️ Etkilesim Kontrolu", "🩺 Semptom Takibi", "🕘 Gecmis"]
    )

    st.sidebar.success(f"👤 {st.session_state.username}")
    if st.sidebar.button("🚪 Cikis Yap", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.memory_history = []
        st.session_state.remembered_medications = ""
        st.session_state.active_drug = ""
        st.session_state.current_drug = ""
        st.session_state.shared_drug = ""
        st.session_state.drug_source = ""
        st.session_state.manual_drug = ""
        st.session_state.chat_history = []
        st.rerun()
    st.sidebar.divider()

    st.sidebar.markdown("## ⏰ Hatırlatıcı")
    render_reminder_permission_controls()
    st.sidebar.caption("Bildirim kontrolu, sayfa yenilendiginde calisir.")
    if st.sidebar.button("🔄 Sayfayi yenile ve hatirlaticilari kontrol et", use_container_width=True):
        st.rerun()
    st.sidebar.divider()
    with st.sidebar.expander("➕ Yeni hatırlatıcı ekle", expanded=True):
        med_name = st.text_input("💊 İlac adı", placeholder="Orn: Metformin")
        remind_time = st.time_input("🕒 Saat", value=datetime.now().time().replace(second=0, microsecond=0))
        if st.button("➕ Hatırlatıcı ekle", key="add_reminder_btn", use_container_width=True):
            hhmm = remind_time.strftime("%H:%M")
            if not med_name.strip():
                st.sidebar.error("İlaç adı boş olamaz.")
            else:
                add_reminder(med_name, hhmm)
                st.sidebar.success("Hatırlatıcı eklendi.")

    st.sidebar.markdown("### 📋 Hatırlatıcılar")
    reminder_rows = list_reminders()
    if not reminder_rows:
        st.sidebar.caption("Henüz hatırlatıcı yok.")
    else:
        for rid, medication_name, hhmm, enabled, last_trigger_date in reminder_rows:
            cols = st.sidebar.columns([0.62, 0.20, 0.18])
            cols[0].markdown(f"**💊 {medication_name}**\n\n🕒 `{hhmm}`")
            cols[1].markdown("✅" if enabled else "⛔")
            if cols[2].button("🗑️", key=f"del_rem_{rid}", help="Sil"):
                delete_reminder(int(rid))
                st.rerun()

    remembered = st.session_state.get("remembered_medications", "").strip()
    st.sidebar.divider()
    st.sidebar.markdown("## 🧠 Konusma Bellegi")
    if remembered:
        st.sidebar.info(f"Hatirlanan ilac(lar): {remembered}")
    else:
        st.sidebar.caption("Henuz hatirlanan ilac bilgisi yok.")
    if st.sidebar.button("🧹 Bellegi temizle", use_container_width=True):
        st.session_state.memory_history = []
        st.session_state.remembered_medications = ""
        st.session_state.active_drug = ""
        st.session_state.current_drug = ""
        st.session_state.shared_drug = ""
        st.session_state.drug_source = ""
        st.session_state.manual_drug = ""
        st.session_state.chat_history = []
        st.rerun()

    st.sidebar.divider()
    st.sidebar.markdown("## 📜 Analiz Gecmisim")
    chat_items = st.session_state.get("chat_history", [])
    if not chat_items:
        st.sidebar.caption("Henuz analiz gecmisi yok.")
    else:
        for idx, item in enumerate(reversed(chat_items[-12:])):
            ts = str(item.get("ts", ""))[:19].replace("T", " ")
            user_input = str(item.get("user_input", ""))
            assistant_output = str(item.get("assistant_output", ""))
            med = parse_medication_from_user_input(user_input)
            risk_icon, risk_text = parse_risk_display_from_output(assistant_output)
            st.sidebar.markdown(
                f"**{ts}**\n\n💊 {med}\n\n{risk_icon} {risk_text}",
                help=f"Kayıt #{idx + 1}",
            )
            st.sidebar.caption("---")

    if st.sidebar.button("🗑️ Gecmisi Temizle", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    with tab1:
        st.markdown('<div class="ga-card">', unsafe_allow_html=True)
        st.subheader("📸 Fotograf ile Ilac Tanima")
        st.markdown(
            '<div class="ga-muted">🖼️ Ilac kutusu fotografini yukleyin. Sonuc bir tahmindir ve doktor gorusunun yerine gecmez.</div>',
            unsafe_allow_html=True,
        )
        
        # Global ilaç giriş kutusu - SADECE Tab 1'de input, diğer tab'larda read-only gösterilecek
        st.text_input('İlaç İsmi', value=st.session_state.get('active_drug', ''), key='main_drug_input')
        st.session_state['manual_drug'] = st.session_state.get('main_drug_input', '').strip()

        # Eğer bir değer varsa, active_drug'a ata ve tüm sekmelerde güncelle
        if st.session_state['manual_drug']:
            st.session_state['active_drug'] = st.session_state['manual_drug']
            st.session_state.drug_source = 'manual'
            st.session_state.current_drug = st.session_state['manual_drug']
            st.session_state.shared_drug = st.session_state['manual_drug']
            st.session_state.remembered_medications = st.session_state['manual_drug']
            add_memory_entry("medication_manual_input", f"{st.session_state['manual_drug']}")
        
        uploaded = st.file_uploader("🗂️ Ilac kutusu fotografi secin", type=["png", "jpg", "jpeg"])
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="🖼️ Yuklenen gorsel", use_container_width=True)
            if st.button("🔍 Ilaci Tanimla"):
                with st.spinner("✨ Analiz ediliyor..."):
                    try:
                        result = identify_medication(image)
                        parsed = try_parse_json(result) or {}
                        med_from_ai = str(parsed.get("medication_name", "")).strip()
                        if med_from_ai and med_from_ai.lower() != "tanimlanamadi":
                            # OCR başarılı oldu - Global ilaç hafızasına kaydet
                            st.session_state['active_drug'] = med_from_ai
                            st.session_state.drug_source = 'ocr'
                            st.session_state.current_drug = med_from_ai
                            st.session_state.shared_drug = med_from_ai
                            st.session_state.remembered_medications = med_from_ai
                            add_memory_entry("medication_from_image", f"{med_from_ai}")
                            # Success kutusunda göster
                            st.success(f"✅ **İlaç Başarıyla Tanımlandı!**\n\n💊 **{med_from_ai}**\n\nBu ilaç diğer sekmelerde otomatik olarak kullanılacaktır.")
                        else:
                            # OCR başarısız oldu
                            if st.session_state.get('drug_source') == 'manual':
                                # Eğer manuel giriş varsa, koru
                                st.info("❌ Yeni görsel tanınamadı, önceki manuel giriş korundu.")
                            else:
                                # Manuel giriş yoksa, yukarıdaki kutuyu kullanmasını söyle
                                st.error("❌ İlacı tanıyamadım, yukarıdaki 'İlaç İsmi' kutusuna manuel olarak yazın ve sayfayı yenileyin.")
                        
                        save_analysis("medication-identification", uploaded.name, result)
                        add_memory_entry("medication_identification_result", result[:400])
                        render_result_card(
                            "🧾 Ilac Tanima Sonucu",
                            result,
                            input_summary=f"Dosya: {uploaded.name}",
                            created_at_iso=datetime.utcnow().isoformat(),
                        )
                    except Exception as e:
                        st.error(f"❌ Hata: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="ga-card">', unsafe_allow_html=True)
        st.subheader("🍽️ Gida-Ilac Etkilesimi")
        st.markdown(
            '<div class="ga-muted">🧾 Ilaclari ve gidaları yazin. Sistem risk seviyesini ve onerilen aksiyonu ozetler.</div>',
            unsafe_allow_html=True,
        )
        # Active Drug'dan miras al
        current_drug = st.session_state.get('active_drug', '')
        if current_drug:
            # İlaç tanımlandıysa: uyarıyı gizle, başlık olarak göster
            st.markdown(f"#### 💊 **Seçili İlaçlar:** `{current_drug}`")
            medications = current_drug
        else:
            # İlaç tanılanmadıysa: uyarı göster, kullanıcı input alabilsin
            st.warning("💊 Lütfen önce İlaç Tanıma sekmesinde ilaç seçiniz.")
            medications = ""
        
        st.session_state.remembered_medications = medications.strip()
        
        foods = st.text_area("🥗 Gidalar (virgulle ayir)", "Ispanak")
        if st.button("🧪 Etkilesimi Analiz Et"):
            with st.spinner("✨ Analiz ediliyor..."):
                try:
                    add_memory_entry("food_query", f"Ilaclar={medications}; Gidalar={foods}")
                    memory_context = build_ai_context()
                    result = analyze_food_interaction(medications, foods, memory_context)
                    save_analysis("food-interaction", f"medications={medications}; foods={foods}", result)
                    add_memory_entry("food_result", result[:500])
                    add_chat_history_entry(
                        "food_interaction",
                        f"Ilaclar={medications}; Gidalar={foods}",
                        result,
                    )
                    render_result_card(
                        "🧾 Etkilesim Sonucu",
                        result,
                        input_summary=f"Ilaclar: {medications}\nGidalar: {foods}",
                        created_at_iso=datetime.utcnow().isoformat(),
                    )
                except Exception as e:
                    st.error(f"❌ Hata: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="ga-card">', unsafe_allow_html=True)
        st.subheader("🩺 Semptom Takibi")
        st.markdown(
            '<div class="ga-muted">🗣️ Semptomlari ve ilac listesini girin. Cikti kesin teshis degil, yonlendirici bilgidir.</div>',
            unsafe_allow_html=True,
        )
        # Active Drug'dan miras al
        current_drug = st.session_state.get('active_drug', '')
        if current_drug:
            # İlaç tanımlandıysa: uyarıyı gizle, başlık olarak göster
            st.markdown(f"#### 💊 **Seçili İlaçlar:** `{current_drug}`")
            current_meds = current_drug
        else:
            # İlaç tanılanmadıysa: uyarı göster
            st.warning("💊 Lütfen önce İlaç Tanıma sekmesinde ilaç seçiniz.")
            current_meds = ""
        
        st.session_state.remembered_medications = current_meds.strip()
        
        if "symptom_text" not in st.session_state:
            st.session_state.symptom_text = "Bas donmesi, halsizlik"

        symptoms = st.text_area("📝 Semptomlar", key="symptom_text")
        if st.button("🧠 Semptomu Analiz Et"):
            with st.spinner("✨ Analiz ediliyor..."):
                try:
                    add_memory_entry("symptom_query", f"Ilaclar={current_meds}; Semptomlar={symptoms}")
                    memory_context = build_ai_context()
                    result = analyze_symptoms(current_meds, symptoms, memory_context)
                    save_analysis("symptom-analysis", f"medications={current_meds}; symptoms={symptoms}", result)
                    add_memory_entry("symptom_result", result[:500])
                    add_chat_history_entry(
                        "symptom_analysis",
                        f"Ilaclar={current_meds}; Semptomlar={symptoms}",
                        result,
                    )
                    render_result_card(
                        "🧾 Semptom Analizi Sonucu",
                        result,
                        input_summary=f"Ilaclar: {current_meds}\nSemptomlar: {symptoms}",
                        created_at_iso=datetime.utcnow().isoformat(),
                    )
                    parsed_symptom = try_parse_json(result) or {}
                    md_output = str(parsed_symptom.get("markdown_response", "")).strip()
                    if md_output:
                        st.markdown(md_output)
                except Exception as e:
                    st.error(f"❌ Hata: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="ga-card">', unsafe_allow_html=True)
        render_history()
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()