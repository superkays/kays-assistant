import streamlit as st
from dotenv import load_dotenv
import os
import re

from openai import OpenAI

from database import (
    create_database,
    save_complaint
)


# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Kays Kitchen",
    page_icon="🍗",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# DATABASE
# =========================================================

create_database()


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# OPENAI API KEY
# =========================================================

api_key = None


# Prioritas 1: Streamlit Secrets
try:

    api_key = st.secrets["OPENAI_API_KEY"]

except Exception:

    pass


# Prioritas 2: .env / environment
if not api_key:

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )


# Jika API key tidak ditemukan
if not api_key:

    st.error(
        "⚠️ OpenAI API Key tidak ditemukan. "
        "Silakan periksa Secrets atau file .env."
    )

    st.stop()


# =========================================================
# OPENAI CLIENT
# =========================================================

client = OpenAI(
    api_key=api_key
)


# =========================================================
# KNOWLEDGE BASE
# =========================================================

knowledge_base = """
KAYS KITCHEN
UMKM Ricebowl Ayam Popcorn


MENU:

1. Kays Ricebowl - Rp18.000
   Varian: Sambal Matah

2. Kays Ricebowl - Rp18.000
   Varian: Sambal Bawang


OPERASIONAL:

- Buka setiap hari
- Jam buka: 09.00 - 21.00
- Lokasi: Jl. Pulau Damar


PEMESANAN:

- Mika tidak menerima pesanan.
- Mika tidak memproses pesanan.
- Pemesanan dilakukan melalui sistem pemesanan Kays Kitchen.
- Delivery: Bisa
- Area delivery: Sekitar Bandar Lampung
- Pembayaran: Transfer / QRIS


KEBIJAKAN:

- Pembatalan dapat dilakukan sebelum produk dikirim.
- Refund diberikan jika makanan rusak atau tumpah.
- Komplain dapat disampaikan melalui Mika.
- Komplain akan dicatat dan diteruskan kepada Admin Kays Kitchen.


PROMO:

- Pembelian di atas 20 pcs mendapatkan potongan harga.
- Nominal potongan harga belum ditentukan.
"""


# =========================================================
# AI INSTRUCTIONS
# =========================================================

instructions = f"""
Kamu adalah AI Customer Service Kays Kitchen
bernama Mika.

Tugas utama kamu hanya:

1. Menjawab pertanyaan customer.
2. Membantu customer yang ingin menyampaikan komplain.

Kamu BUKAN sistem pemesanan.


=========================================================
GAYA BICARA
=========================================================

- Ramah.
- Natural.
- Singkat.
- Jelas.
- Panggil customer dengan "kak".
- Jangan terlalu formal.
- Jangan memberikan informasi yang tidak diperlukan.


=========================================================
ATURAN INFORMASI
=========================================================

Jawab berdasarkan Knowledge Base.

Jangan mengarang informasi.

Jika informasi tidak tersedia:

"Maaf kak, informasi tersebut belum tersedia."


=========================================================
ATURAN PEMESANAN
=========================================================

Mika TIDAK menerima pesanan.

Mika TIDAK memproses pesanan.

Mika TIDAK menghitung total pesanan.

Mika TIDAK menghitung harga pesanan.

Mika TIDAK menyimpan data pesanan.

Jika customer mengatakan ingin memesan,
jelaskan bahwa Mika adalah Customer Service
dan tidak memproses pesanan.


JANGAN memberikan nomor WhatsApp Kays Kitchen.


=========================================================
ATURAN WHATSAPP
=========================================================

Mika TIDAK memiliki tugas memberikan nomor WhatsApp
Kays Kitchen.

Jangan pernah memberikan nomor WhatsApp Kays Kitchen.

Jika customer meminta nomor WhatsApp Admin untuk
komplain, jelaskan bahwa komplain dapat dicatat
langsung melalui Mika.


=========================================================
ATURAN KOMPLAIN
=========================================================

Jika customer menyampaikan komplain:

- Minta maaf.
- Tunjukkan bahwa Mika memahami masalah customer.
- Bantu proses pencatatan komplain.

Sistem akan meminta:

1. Nama customer.
2. Nomor WhatsApp customer.
3. Isi komplain.

Jangan meminta nomor WhatsApp Kays Kitchen.

Nomor yang diminta adalah nomor WhatsApp MILIK CUSTOMER.


=========================================================
ATURAN PENTING NAMA CUSTOMER
=========================================================

JANGAN pernah menganggap kata-kata seperti:

- tumpah
- kurang
- rusak
- bocor
- salah
- makanan
- pesanan
- komplain
- keluhan
- sambal
- nasi
- telat
- terlambat
- kendala
- masalah
- sedikit
- isinya sedikit

sebagai nama customer.

Nama customer harus berasal dari informasi yang jelas
dari customer.


=========================================================
SETELAH KOMPLAIN TERCATAT
=========================================================

Beritahu customer:

"Komplain kakak sudah berhasil saya catat dengan
nomor laporan #ID.

Komplain akan disampaikan kepada Admin Kays Kitchen
untuk ditindaklanjuti.

Admin akan menghubungi kakak melalui WhatsApp yang
sudah diberikan."

Nomor laporan HARUS berasal dari sistem database.

Jangan mengarang nomor laporan.


=========================================================
KNOWLEDGE BASE
=========================================================

{knowledge_base}
"""


# =========================================================
# CUSTOM CSS
# =========================================================

st.html("""
<style>

/* =====================================================
   MAIN APP
   ===================================================== */

.stApp {

    background:
        linear-gradient(
            180deg,
            #111827 0%,
            #172554 50%,
            #111827 100%
        );

}


/* =====================================================
   HIDE STREAMLIT DEFAULT ELEMENTS
   ===================================================== */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* =====================================================
   MAIN CONTAINER
   ===================================================== */

.block-container {

    max-width: 850px;

    padding-top: 2rem;
    padding-bottom: 7rem;

}


/* =====================================================
   KAYS HEADER
   ===================================================== */

.kays-header {

    width: 100%;

    margin-bottom: 25px;

}


.kays-brand {

    display: flex;

    align-items: center;

    gap: 16px;

}


.kays-logo {

    width: 62px;
    height: 62px;

    display: flex;

    align-items: center;
    justify-content: center;

    font-size: 38px;

    background: #f97316;

    border-radius: 18px;

    box-shadow:
        0 8px 25px
        rgba(249, 115, 22, 0.25);

}


.kays-title {

    font-size: 38px;

    font-weight: 800;

    color: white;

    line-height: 1.1;

}


.kays-subtitle {

    margin-top: 5px;

    font-size: 15px;

    color: #cbd5e1;

}


/* =====================================================
   ONLINE STATUS
   ===================================================== */

.kays-status {

    margin-top: 10px;

    display: inline-flex;

    align-items: center;

    gap: 7px;

    padding: 6px 12px;

    background:
        rgba(34, 197, 94, 0.12);

    border:
        1px solid
        rgba(34, 197, 94, 0.25);

    border-radius: 999px;

    color: #bbf7d0;

    font-size: 13px;

}


.status-dot {

    width: 8px;
    height: 8px;

    background: #22c55e;

    border-radius: 50%;

    box-shadow:
        0 0 8px #22c55e;

}


/* =====================================================
   INFO CARD
   ===================================================== */

.info-card {

    width: 100%;

    padding: 24px;

    margin-top: 25px;
    margin-bottom: 25px;

    background:
        rgba(255, 255, 255, 0.07);

    border:
        1px solid
        rgba(255, 255, 255, 0.10);

    border-radius: 22px;

    box-sizing: border-box;

}


.info-title {

    color: white;

    font-size: 18px;

    font-weight: 700;

    margin-bottom: 18px;

}


/* =====================================================
   INFO GRID
   ===================================================== */

.info-grid {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 12px;

}


.info-item {

    padding: 15px;

    background:
        rgba(255, 255, 255, 0.06);

    border-radius: 16px;

    text-align: center;

}


.info-icon {

    font-size: 24px;

    margin-bottom: 8px;

}


.info-label {

    color: #94a3b8;

    font-size: 12px;

    margin-bottom: 5px;

}


.info-value {

    color: white;

    font-size: 13px;

    font-weight: 600;

}


/* =====================================================
   CHAT TITLE
   ===================================================== */

.chat-title {

    color: white;

    font-size: 17px;

    font-weight: 700;

    margin-top: 20px;
    margin-bottom: 12px;

}


/* =====================================================
   FOOTER
   ===================================================== */

.kays-footer {

    margin-top: 35px;

    padding: 22px;

    text-align: center;

    color: #cbd5e1;

    background:
        rgba(255, 255, 255, 0.06);

    border:
        1px solid
        rgba(255, 255, 255, 0.08);

    border-radius: 18px;

    box-sizing: border-box;

}


.footer-main {

    color: white;

    font-weight: 600;

    margin-bottom: 12px;

}


.footer-copy {

    font-size: 13px;

    color: #94a3b8;

}


/* =====================================================
   CHAT INPUT
   ===================================================== */

div[data-testid="stChatInput"] {

    bottom: 15px;

}


div[data-testid="stChatInput"] textarea {

    border-radius: 18px !important;

    background:
        rgba(255, 255, 255, 0.10)
        !important;

    border:
        1px solid
        rgba(255, 255, 255, 0.18)
        !important;

    color: white !important;

}


div[data-testid="stChatInput"] textarea::placeholder {

    color: #94a3b8 !important;

}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 600px) {

    .block-container {

        padding-left: 14px;
        padding-right: 14px;

        padding-top: 1.2rem;
        padding-bottom: 6rem;

    }


    .kays-logo {

        width: 52px;
        height: 52px;

        font-size: 30px;

        border-radius: 15px;

    }


    .kays-title {

        font-size: 28px;

    }


    .kays-subtitle {

        font-size: 13px;

    }


    .info-card {

        padding: 16px;

        border-radius: 18px;

    }


    .info-grid {

        grid-template-columns:
            repeat(2, 1fr);

        gap: 9px;

    }


    .info-item {

        padding: 12px;

    }


    .info-value {

        font-size: 12px;

    }


    .chat-title {

        font-size: 16px;

    }

}

</style>
""")


# =========================================================
# HEADER
# =========================================================

st.html("""
<div class="kays-header">

    <div class="kays-brand">

        <div class="kays-logo">
            🎧
        </div>

        <div>

            <div class="kays-title">
                Mika
            </div>

            <div class="kays-subtitle">
                Kays Online Customer Service
            </div>

            <div class="kays-status">

                <span class="status-dot"></span>

                Always On

            </div>

        </div>

    </div>

</div>
""")


# =========================================================
# INFORMATION CARD
# =========================================================

st.html("""
<div class="info-card">

    <div class="info-title">
        ✨ Tentang Kays Kitchen
    </div>

    <div class="info-grid">

        <div class="info-item">

            <div class="info-icon">
                🍚
            </div>

            <div class="info-label">
                Menu
            </div>

            <div class="info-value">
                Ricebowl
            </div>

        </div>


        <div class="info-item">

            <div class="info-icon">
                🌶️
            </div>

            <div class="info-label">
                Varian
            </div>

            <div class="info-value">
                Matah & Bawang
            </div>

        </div>


        <div class="info-item">

            <div class="info-icon">
                🕘
            </div>

            <div class="info-label">
                Operasional
            </div>

            <div class="info-value">
                09.00 - 21.00
            </div>

        </div>


        <div class="info-item">

            <div class="info-icon">
                🛵
            </div>

            <div class="info-label">
                Delivery
            </div>

            <div class="info-value">
                Bandar Lampung
            </div>

        </div>

    </div>

</div>
""")


# =========================================================
# CHAT TITLE
# =========================================================

st.html("""
<div class="chat-title">
    💬 Chat dengan Mika
</div>
""")


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "complaint_active" not in st.session_state:

    st.session_state.complaint_active = False


if "complaint_step" not in st.session_state:

    st.session_state.complaint_step = None


if "customer_name" not in st.session_state:

    st.session_state.customer_name = ""


if "customer_whatsapp" not in st.session_state:

    st.session_state.customer_whatsapp = ""


if "complaint_text" not in st.session_state:

    st.session_state.complaint_text = ""


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# =========================================================
# PHONE NUMBER
# =========================================================

def extract_phone_number(text):

    if not text:

        return None


    patterns = [

        r"(?:\+62|62)[\s\-()]?\d[\d\s\-()]{7,15}",

        r"0\d[\d\s\-()]{8,14}"

    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )


        if not match:

            continue


        phone = re.sub(
            r"\D",
            "",
            match.group(0)
        )


        if phone.startswith("62"):

            phone = "0" + phone[2:]


        if (
            phone.startswith("08")
            and
            10 <= len(phone) <= 14
        ):

            return phone


    return None


# =========================================================
# EXTRACT CUSTOMER NAME
# =========================================================

def extract_customer_name(text):

    if not text:

        return None


    text_clean = text.strip()


    # -----------------------------------------------------
    # 1. FORMAT:
    # Nama: Prabowo
    # Nama = Prabowo
    # -----------------------------------------------------

    labeled_patterns = [

        r"\bnama\s*[:=]\s*([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{1,40})",

        r"\bnama\s+kakak\s*[:=]?\s*([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{1,40})"

    ]


    # -----------------------------------------------------
    # 2. FORMAT:
    # nama saya Prabowo
    # saya Prabowo
    # aku Prabowo
    # -----------------------------------------------------

    normal_patterns = [

        r"\bnama saya\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{1,40})",

        r"\bsaya\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{1,40})",

        r"\baku\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{1,40})"

    ]


    all_patterns = (
        labeled_patterns
        +
        normal_patterns
    )


    forbidden_words = {

        "mau",
        "ingin",
        "pesan",
        "pesanan",
        "order",
        "beli",
        "makan",
        "makanan",
        "minum",
        "komplain",
        "complain",
        "keluhan",
        "kendala",
        "masalah",
        "tumpah",
        "kurang",
        "kekurangan",
        "rusak",
        "bocor",
        "salah",
        "telat",
        "terlambat",
        "tidak",
        "ga",
        "gak",
        "nggak",
        "ada",
        "sambal",
        "nasi",
        "ayam",
        "sedikit"
        "tumpe"
        "tumpeh"
    }


    for pattern in all_patterns:

        match = re.search(
            pattern,
            text_clean,
            re.IGNORECASE
        )


        if not match:

            continue


        candidate = match.group(1).strip()


        # -------------------------------------------------
        # Berhenti di label berikutnya
        # -------------------------------------------------

        candidate = re.split(
            r"\b(?:wa|whatsapp|nomor|no|pesanan|keluhan|komplain)\b",
            candidate,
            maxsplit=1,
            flags=re.IGNORECASE
        )[0].strip()


        candidate = candidate.split(",")[0].strip()


        words = candidate.split()


        if not words:

            continue


        if len(words) > 4:

            continue


        if len(candidate) > 50:

            continue

        # -----------------------------------------------------
        # CEGAH KATA KOMPLAIN YANG DIPANJANGKAN
        # Contoh:
        # tumpahhhhh → tetap dianggap "tumpah"
        # kurangg    → tetap dianggap "kurang"
        # rusakkkk   → tetap dianggap "rusak"
        # -----------------------------------------------------

        is_forbidden = False

        for word in words:

            word_clean = word.lower().strip(
                ".,!?;:()[]{}"
            )

            for forbidden in forbidden_words:

                if (
                        word_clean == forbidden
                        or
                        word_clean.startswith(forbidden)
                ):
                    is_forbidden = True
                    break

            if is_forbidden:
                break

        if is_forbidden:
            continue


        if re.search(
            r"\d",
            candidate
        ):

            continue


        return candidate


    return None


# =========================================================
# NAME VALIDATION
# =========================================================

def looks_like_name(text):

    if not text:

        return False


    value = text.strip()


    words = value.split()


    if not words:

        return False


    if len(words) > 4:

        return False


    if len(value) > 50:

        return False


    forbidden_words = {

        "mau",
        "ingin",
        "pesan",
        "pesanan",
        "order",
        "beli",
        "makan",
        "makanan",
        "minum",
        "tumpah",
        "kurang",
        "kekurangan",
        "rusak",
        "bocor",
        "salah",
        "komplain",
        "complain",
        "keluhan",
        "kendala",
        "masalah",
        "telat",
        "terlambat",
        "tidak",
        "ga",
        "gak",
        "nggak",
        "ada",
        "sambal",
        "nasi",
        "ayam",
        "sedikit",
        "isinya"
    }


    lowered_words = [
        word.lower()
        for word in words
    ]


    if any(
        word in forbidden_words
        for word in lowered_words
    ):

        return False


    if extract_phone_number(value):

        return False


    if re.search(
        r"\d",
        value
    ):

        return False


    if not re.search(
        r"[A-Za-zÀ-ÿ]",
        value
    ):

        return False


    return True

# =========================================================
# INTENT DETECTION
# =========================================================

def detect_intent(text):

    if not text:
        return "general"

    text_lower = text.lower().strip()

    # -----------------------------------------------------
    # COMPLAINT
    # -----------------------------------------------------

    if is_complaint_message(text_lower):

        return "complaint"


    # -----------------------------------------------------
    # MENU / HARGA
    # -----------------------------------------------------

    menu_keywords = [
        "menu",
        "ricebowl",
        "ayam",
        "sambal",
        "matah",
        "bawang",
        "harga",
        "berapa",
        "harga berapa"
    ]

    if any(
        keyword in text_lower
        for keyword in menu_keywords
    ):

        return "faq"


    # -----------------------------------------------------
    # OPERASIONAL
    # -----------------------------------------------------

    operational_keywords = [
        "buka",
        "tutup",
        "jam buka",
        "jam berapa",
        "lokasi",
        "alamat",
        "dimana",
        "delivery",
        "antar",
        "kirim",
        "bandar lampung",
        "qris",
        "transfer",
        "pembayaran",
        "bayar"
    ]

    if any(
        keyword in text_lower
        for keyword in operational_keywords
    ):

        return "faq"


    # -----------------------------------------------------
    # DEFAULT
    # -----------------------------------------------------

    return "general"

# =========================================================
# COMPLAINT DETECTION
# =========================================================

def is_complaint_message(text):

    if not text:
        return False

    text = text.lower().strip()

    complaint_keywords = [

        # Komplain umum
        "komplain",
        "complain",
        "keluhan",
        "mengeluh",
        "kecewa",
        "kecewain",

        # Kondisi makanan
        "rusak",
        "tumpah",
        "bocor",
        "kurang",
        "kekurangan",

        # Porsi
        "cuma dikit"
        "cuma sedikit"
        "isinya sedikit",
        "isi sedikit",
        "porsinya sedikit",
        "porsi sedikit",
        "makanannya sedikit",
        "makanan sedikit",

        # Ketidaksesuaian
        "salah",
        "kesalahan",
        "beda",
        "berbeda",
        "tidak sesuai",
        "ga sesuai",
        "gak sesuai",

        # Tidak ada
        "tidak ada",
        "ga ada",
        "gak ada",

        # Pengiriman
        "belum datang",
        "belum sampai",
        "terlambat",
        "telat",

        # Masalah
        "masalah",
        "kendala",
        "buruk",
        "parah",

        # Makanan
        "makanan dingin",
        "nasi dingin",

        # Pesanan
        "pesanan salah",
        "pesanan kurang",

    ]

    return any(
        keyword in text
        for keyword in complaint_keywords
    )


# =========================================================
# EXTRACT LABELED COMPLAINT
# =========================================================

def extract_labeled_complaint(text):

    if not text:

        return None


    patterns = [

        r"\bkeluhan\s*[:=]\s*(.+?)(?=\n|$)",

        r"\bkomplain\s*[:=]\s*(.+?)(?=\n|$)",

        r"\bkendala\s*[:=]\s*(.+?)(?=\n|$)"

    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )


        if match:

            complaint = match.group(1).strip()


            if complaint:

                return complaint


    return None


# =========================================================
# CLEAN COMPLAINT TEXT
# =========================================================

def clean_complaint_text(text):

    if not text:

        return ""


    original = text.strip()


    # -----------------------------------------------------
    # PRIORITAS 1:
    # Kalau ada "Keluhan:" ambil hanya isinya.
    # -----------------------------------------------------

    labeled_complaint = extract_labeled_complaint(
        original
    )


    if labeled_complaint:

        return labeled_complaint.strip(
            " ,.-:"
        )


    complaint = original


    # -----------------------------------------------------
    # Hapus Nama
    # -----------------------------------------------------

    complaint = re.sub(

        r"\bnama\s*[:=]\s*[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{1,40}",

        "",

        complaint,

        flags=re.IGNORECASE

    )


    complaint = re.sub(

        r"\bnama saya\s+[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{1,40}",

        "",

        complaint,

        flags=re.IGNORECASE

    )


    # -----------------------------------------------------
    # Hapus nomor WA
    # -----------------------------------------------------

    phone = extract_phone_number(
        complaint
    )


    if phone:

        complaint = re.sub(
            re.escape(phone),
            "",
            complaint
        )


    # -----------------------------------------------------
    # Hapus label WA
    # -----------------------------------------------------

    complaint = re.sub(

        r"\b(?:no|nomor|wa|whatsapp)\s*[:=]?\s*",

        "",

        complaint,

        flags=re.IGNORECASE

    )


    # -----------------------------------------------------
    # Hapus informasi pesanan jika ada label
    # -----------------------------------------------------

    complaint = re.sub(

        r"\bpesanan\s*[:=]\s*.+?(?=\n|keluhan|komplain|$)",

        "",

        complaint,

        flags=re.IGNORECASE

    )


    # -----------------------------------------------------
    # Hapus spasi berlebih
    # -----------------------------------------------------

    complaint = re.sub(
        r"\s+",
        " ",
        complaint
    ).strip()


    complaint = complaint.strip(
        " ,.-:"
    )


    # -----------------------------------------------------
    # Kalau hasil masih berupa informasi identitas
    # -----------------------------------------------------

    if complaint.lower() in {

        "saya",

        "aku",

        "nama",

        "wa",

        "whatsapp"

    }:

        return ""


    return complaint


# =========================================================
# SAVE CURRENT COMPLAINT
# =========================================================

def save_current_complaint():

    name = st.session_state.customer_name.strip()

    whatsapp = st.session_state.customer_whatsapp.strip()

    complaint = st.session_state.complaint_text.strip()


    # -----------------------------------------------------
    # VALIDASI SEBELUM DATABASE
    # -----------------------------------------------------

    if not name:

        raise ValueError(
            "Nama customer belum tersedia."
        )


    if not whatsapp:

        raise ValueError(
            "Nomor WhatsApp customer belum tersedia."
        )


    if not complaint:

        raise ValueError(
            "Isi complaint belum tersedia."
        )


    # -----------------------------------------------------
    # SIMPAN
    # -----------------------------------------------------

    complaint_id = save_complaint(

        name,

        whatsapp,

        complaint

    )


    # -----------------------------------------------------
    # DATABASE HARUS MENGEMBALIKAN ID
    # -----------------------------------------------------

    if complaint_id is None:

        raise ValueError(
            "Database tidak mengembalikan nomor laporan."
        )


    return complaint_id


# =========================================================
# RESET COMPLAINT
# =========================================================

def reset_complaint_process():

    st.session_state.complaint_active = False

    st.session_state.complaint_step = None

    st.session_state.complaint_text = ""


# =========================================================
# COMPLETE COMPLAINT PROCESSOR
# =========================================================

def process_complete_complaint(prompt):

    # -----------------------------------------------------
    # Ambil semua informasi dari satu pesan
    # -----------------------------------------------------

    detected_name = extract_customer_name(
        prompt
    )


    detected_phone = extract_phone_number(
        prompt
    )


    detected_complaint = clean_complaint_text(
        prompt
    )


    # -----------------------------------------------------
    # Simpan yang ditemukan
    # -----------------------------------------------------

    if detected_name:

        st.session_state.customer_name = (
            detected_name
        )


    if detected_phone:

        st.session_state.customer_whatsapp = (
            detected_phone
        )


    if (
        detected_complaint
        and
        is_complaint_message(prompt)
    ):

        st.session_state.complaint_text = (
            detected_complaint
        )


    # -----------------------------------------------------
    # Cek kekurangan
    # -----------------------------------------------------

    missing_name = not bool(
        st.session_state.customer_name
    )


    missing_whatsapp = not bool(
        st.session_state.customer_whatsapp
    )


    missing_complaint = not bool(
        st.session_state.complaint_text
    )


    # =====================================================
    # SEMUA LENGKAP
    # =====================================================

    if not missing_name and not missing_whatsapp and not missing_complaint:

        try:

            complaint_id = save_current_complaint()


            reset_complaint_process()


            return (
                "Baik kak, terima kasih informasinya. 🙏\n\n"

                "Komplain kakak sudah berhasil saya catat "
                f"dengan nomor laporan **#{complaint_id}**.\n\n"

                "Komplain akan disampaikan kepada Admin "
                "Kays Kitchen untuk ditindaklanjuti.\n\n"

                "Admin akan menghubungi kakak melalui "
                "WhatsApp yang sudah diberikan."
            )


        except Exception as e:

            print(
                "ERROR SAVE COMPLETE COMPLAINT:",
                repr(e)
            )


            return (
                "Maaf kak, komplain belum berhasil "
                "disimpan. 😔\n\n"
                "Silakan coba lagi."
            )


    # =====================================================
    # NAMA KURANG
    # =====================================================

    if missing_name:

        st.session_state.complaint_active = True

        st.session_state.complaint_step = "name"


        return (
            "Mohon maaf ya kak atas kendalanya 🙏\n\n"

            "Saya bantu catat komplainnya agar dapat "
            "ditindaklanjuti oleh Admin Kays Kitchen.\n\n"

            "Boleh saya tahu nama kakak?"
        )


    # =====================================================
    # WHATSAPP KURANG
    # =====================================================

    if missing_whatsapp:

        st.session_state.complaint_active = True

        st.session_state.complaint_step = "whatsapp"


        return (
            f"Terima kasih, kak "
            f"{st.session_state.customer_name}. 😊\n\n"

            "Boleh saya minta nomor WhatsApp kakak "
            "yang bisa dihubungi Admin untuk "
            "menindaklanjuti komplain ini?"
        )


    # =====================================================
    # COMPLAINT KURANG
    # =====================================================

    if missing_complaint:

        st.session_state.complaint_active = True

        st.session_state.complaint_step = "complaint"


        return (
            f"Terima kasih, kak "
            f"{st.session_state.customer_name}. 🙏\n\n"

            "Sekarang boleh ceritakan secara detail "
            "kendala atau komplain yang kakak alami?"
        )


    return None


# =========================================================
# DETECT COMPLETE COMPLAINT
# =========================================================

def has_complete_complaint_data(text):

    if not text:
        return False

    name = extract_customer_name(text)

    phone = extract_phone_number(text)

    complaint = clean_complaint_text(text)

    complaint_detected = is_complaint_message(text)

    return (
        bool(name)
        and
        bool(phone)
        and
        bool(complaint)
        and
        complaint_detected
    )

# =========================================================
# USER INPUT
# =========================================================

prompt = st.chat_input(
    "Tulis pesan kamu..."
)


if prompt:

    # =====================================================
    # SAVE USER MESSAGE
    # =====================================================

    st.session_state.messages.append({

        "role": "user",

        "content": prompt

    })


    # =====================================================
    # DISPLAY USER MESSAGE
    # =====================================================

    with st.chat_message("user"):

        st.write(prompt)


    answer = None


    # =====================================================
    # ACTIVE COMPLAINT FLOW
    # =====================================================

    if st.session_state.complaint_active:

        # =================================================
        # STEP NAME
        # =================================================

        if st.session_state.complaint_step == "name":

            detected_name = extract_customer_name(
                prompt
            )


            if detected_name:

                st.session_state.customer_name = (
                    detected_name
                )


            elif looks_like_name(prompt):

                st.session_state.customer_name = (
                    prompt.strip()
                )


            else:

                # -----------------------------------------
                # Jangan kehilangan complaint
                # -----------------------------------------

                if is_complaint_message(prompt):

                    complaint = clean_complaint_text(
                        prompt
                    )


                    if complaint:

                        st.session_state.complaint_text = (
                            complaint
                        )


                answer = (
                    "Mohon maaf ya kak atas kendalanya 🙏\n\n"
                    "Saya bantu catat komplainnya.\n\n"
                    "Boleh saya tahu nama kakak?"
                )


            # ------------------------------------------------
            # Kalau nama berhasil
            # ------------------------------------------------

            if (
                not answer
                and
                st.session_state.customer_name
            ):

                phone = extract_phone_number(
                    prompt
                )


                if phone:

                    st.session_state.customer_whatsapp = (
                        phone
                    )


                if is_complaint_message(prompt):

                    complaint = clean_complaint_text(
                        prompt
                    )


                    if complaint:

                        st.session_state.complaint_text = (
                            complaint
                        )


                # --------------------------------------------
                # Semua lengkap
                # --------------------------------------------

                if (
                    st.session_state.customer_whatsapp
                    and
                    st.session_state.complaint_text
                ):

                    try:

                        complaint_id = save_current_complaint()


                        reset_complaint_process()


                        answer = (
                            "Baik kak, terima kasih informasinya. 🙏\n\n"
                            "Komplain kakak sudah berhasil saya catat "
                            f"dengan nomor laporan **#{complaint_id}**.\n\n"
                            "Komplain akan disampaikan kepada Admin "
                            "Kays Kitchen untuk ditindaklanjuti.\n\n"
                            "Admin akan menghubungi kakak melalui "
                            "WhatsApp yang sudah diberikan."
                        )


                    except Exception as e:

                        print(
                            "ERROR SAVE NAME STEP:",
                            repr(e)
                        )


                        answer = (
                            "Maaf kak, komplain belum berhasil "
                            "disimpan. 😔\n\n"
                            "Silakan coba lagi."
                        )


                elif not st.session_state.customer_whatsapp:

                    st.session_state.complaint_step = (
                        "whatsapp"
                    )


                    answer = (
                        f"Terima kasih, kak "
                        f"{st.session_state.customer_name}. 😊\n\n"
                        "Boleh saya minta nomor WhatsApp kakak "
                        "yang bisa dihubungi Admin untuk "
                        "menindaklanjuti komplain ini?"
                    )


                else:

                    st.session_state.complaint_step = (
                        "complaint"
                    )


                    answer = (
                        "Terima kasih, kak. 🙏\n\n"
                        "Sekarang boleh ceritakan secara detail "
                        "kendala atau komplain yang kakak alami?"
                    )


        # =================================================
        # STEP WHATSAPP
        # =================================================

        elif st.session_state.complaint_step == "whatsapp":

            phone = extract_phone_number(
                prompt
            )


            if not phone:

                answer = (
                    "Maaf kak, saya belum bisa mengenali "
                    "nomor WhatsAppnya. 🙏\n\n"

                    "Boleh kirim nomor WhatsApp kakak, "
                    "contohnya 081234567890?"
                )


            else:

                st.session_state.customer_whatsapp = (
                    phone
                )


                if st.session_state.complaint_text:

                    try:

                        complaint_id = save_current_complaint()


                        reset_complaint_process()


                        answer = (
                            "Terima kasih, kak. 🙏\n\n"
                            "Komplain kakak sudah berhasil saya "
                            f"catat dengan nomor laporan **#{complaint_id}**.\n\n"
                            "Komplain akan disampaikan kepada Admin "
                            "Kays Kitchen untuk ditindaklanjuti.\n\n"
                            "Admin akan menghubungi kakak melalui "
                            "WhatsApp yang sudah diberikan."
                        )


                    except Exception as e:

                        print(
                            "ERROR SAVE WHATSAPP STEP:",
                            repr(e)
                        )


                        answer = (
                            "Maaf kak, komplain belum berhasil "
                            "disimpan. 😔\n\n"
                            "Silakan coba lagi."
                        )


                else:

                    st.session_state.complaint_step = (
                        "complaint"
                    )


                    answer = (
                        "Terima kasih, kak. 🙏\n\n"
                        "Sekarang boleh ceritakan secara detail "
                        "kendala atau komplain yang kakak alami?"
                    )


        # =================================================
        # STEP COMPLAINT
        # =================================================

        elif st.session_state.complaint_step == "complaint":

            complaint = clean_complaint_text(
                prompt
            )


            if not complaint:

                answer = (
                    "Boleh ceritakan sedikit lebih detail "
                    "tentang kendalanya ya kak? 🙏"
                )


            else:

                st.session_state.complaint_text = (
                    complaint
                )


                try:

                    complaint_id = save_current_complaint()


                    reset_complaint_process()


                    answer = (
                        "Baik kak, terima kasih informasinya. 🙏\n\n"

                        "Komplain kakak sudah berhasil saya catat "
                        f"dengan nomor laporan **#{complaint_id}**.\n\n"

                        "Komplain akan disampaikan kepada Admin "
                        "Kays Kitchen untuk ditindaklanjuti.\n\n"

                        "Admin akan menghubungi kakak melalui "
                        "WhatsApp yang sudah diberikan."
                    )


                except Exception as e:

                    print(
                        "ERROR SAVE COMPLAINT STEP:",
                        repr(e)
                    )


                    answer = (
                        "Maaf kak, komplain belum berhasil "
                        "disimpan. 😔\n\n"
                        "Silakan coba lagi."
                    )


    # =====================================================
    # START NEW COMPLAINT
    # =====================================================

    # =====================================================

    # START NEW COMPLAINT

    # =====================================================

    elif (

            has_complete_complaint_data(prompt)

            or

            is_complaint_message(prompt)

    ):

        # -------------------------------------------------
        # PENTING:
        # Selalu proses pesan lengkap terlebih dahulu.
        # -------------------------------------------------

        answer = process_complete_complaint(
            prompt
        )


    # =====================================================
    # NORMAL CUSTOMER SERVICE
    # =====================================================

    if answer is None:

        try:

            chat_history = []


            for message in st.session_state.messages:

                chat_history.append({

                    "role": message["role"],

                    "content": message["content"]

                })


            response = client.responses.create(

                model="gpt-5-mini",

                instructions=instructions,

                input=chat_history

            )


            answer = response.output_text


        except Exception as e:

            print(
                "ERROR OPENAI:",
                repr(e)
            )


            answer = (
                "Maaf kak, Mika sedang mengalami "
                "gangguan koneksi. 😔\n\n"
                "Silakan coba beberapa saat lagi."
            )


    # =====================================================
    # DISPLAY ASSISTANT RESPONSE
    # =====================================================

    with st.chat_message(
        "assistant"
    ):

        st.write(answer)


    # =====================================================
    # SAVE ASSISTANT RESPONSE
    # =====================================================

    st.session_state.messages.append({

        "role": "assistant",

        "content": answer

    })


# =========================================================
# FOOTER
# =========================================================

st.html("""
<div class="kays-footer">

    <div class="footer-main">
        Online Customer Service
    </div>

    <div class="footer-copy">
        © 2026 Kays Kitchen
    </div>

</div>
""")