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
# LOAD OPENAI API KEY
# =========================================================

api_key = None


# Prioritas 1: Streamlit Secrets
try:

    api_key = st.secrets["OPENAI_API_KEY"]

except Exception:

    pass


# Prioritas 2: .env / environment variable
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

Jika customer mengatakan:

"saya mau pesan"

atau:

"mau order"

atau:

"saya mau beli"

jawab dengan sopan bahwa Mika adalah Customer Service
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

sebagai nama customer.

Nama customer harus berasal dari informasi yang jelas
dari customer.


=========================================================
SETELAH KOMPLAIN TERCATAT
=========================================================

Beritahu customer:

"Komplain kakak sudah berhasil saya catat dan akan
disampaikan kepada Admin Kays Kitchen untuk
ditindaklanjuti.

Admin akan menghubungi kakak melalui WhatsApp yang
sudah diberikan."


Jangan mengatakan Admin sudah menghubungi customer
sebelum benar-benar dilakukan.


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
            🍗
        </div>

        <div>

            <div class="kays-title">
                CS Mika
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


# ---------------------------------------------------------
# COMPLAINT STATE
# ---------------------------------------------------------

if "complaint_active" not in st.session_state:

    st.session_state.complaint_active = False


if "complaint_step" not in st.session_state:

    st.session_state.complaint_step = None


# ---------------------------------------------------------
# CUSTOMER PROFILE
# ---------------------------------------------------------

if "customer_name" not in st.session_state:

    st.session_state.customer_name = ""


if "customer_whatsapp" not in st.session_state:

    st.session_state.customer_whatsapp = ""


# ---------------------------------------------------------
# CURRENT COMPLAINT
# ---------------------------------------------------------

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
# PHONE NUMBER VALIDATION
# =========================================================

def extract_phone_number(text):

    match = re.search(
        r"(?:\+62|62|0)[\s\-()]?\d[\d\s\-()]{7,15}",
        text
    )

    if not match:

        return None


    phone = match.group(0)


    # Hapus karakter selain angka
    phone = re.sub(
        r"\D",
        "",
        phone
    )


    # Normalisasi +62 / 62 menjadi 0
    if phone.startswith("62"):

        phone = "0" + phone[2:]


    # Validasi nomor Indonesia sederhana
    if (
        phone.startswith("08")
        and
        10 <= len(phone) <= 14
    ):

        return phone


    return None


# =========================================================
# EXTRACT NAME
# =========================================================

def extract_customer_name(text):

    text_clean = text.strip()


    # -----------------------------------------------------
    # Pola:
    # "saya Budi"
    # "nama saya Budi"
    # "aku Budi"
    # -----------------------------------------------------

    patterns = [

        r"\bnama saya\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{1,40})",

        r"\bsaya\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{1,40})",

        r"\baku\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{1,40})"

    ]


    # -----------------------------------------------------
    # Kata yang TIDAK BOLEH dianggap nama
    # -----------------------------------------------------

    forbidden_words = [

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
        "ayam"
    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            text_clean,
            re.IGNORECASE
        )

        if match:

            candidate = match.group(1).strip()


            # Hapus bagian setelah koma
            candidate = candidate.split(",")[0].strip()


            # Hapus bagian setelah nomor WA
            candidate = re.split(
                r"\b(?:no|nomor|wa|whatsapp)\b",
                candidate,
                flags=re.IGNORECASE
            )[0].strip()


            words = candidate.split()


            if not words:
                continue


            # Jangan terlalu panjang
            if len(words) > 4:
                continue


            # Jika salah satu kata merupakan kata komplain,
            # jangan dianggap sebagai nama
            if any(
                word.lower() in forbidden_words
                for word in words
            ):
                continue


            return candidate


    return None


# =========================================================
# NAME VALIDATION
# =========================================================

def looks_like_name(text):

    value = text.strip()


    if not value:

        return False


    # -----------------------------------------------------
    # Maksimal 4 kata
    # -----------------------------------------------------

    words = value.split()


    if len(words) > 4:

        return False


    # -----------------------------------------------------
    # Jangan menerima kalimat panjang sebagai nama
    # -----------------------------------------------------

    if len(value) > 50:

        return False


    # -----------------------------------------------------
    # Kata-kata yang jelas bukan nama
    # -----------------------------------------------------

    forbidden_words = [

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
        "pesanannya",
        "pesanan saya",
        "makanan saya"
    ]


    lowered = value.lower()


    for forbidden in forbidden_words:

        if forbidden in lowered:

            return False


    # -----------------------------------------------------
    # Jika ada nomor WA, bukan nama murni
    # -----------------------------------------------------

    if extract_phone_number(value):

        return False


    # -----------------------------------------------------
    # Nama tidak boleh mengandung angka
    # -----------------------------------------------------

    if re.search(
        r"\d",
        value
    ):

        return False


    # -----------------------------------------------------
    # Nama harus berisi huruf
    # -----------------------------------------------------

    if not re.search(
        r"[A-Za-zÀ-ÿ]",
        value
    ):

        return False


    return True


# =========================================================
# COMPLAINT DETECTION
# =========================================================

def is_complaint_message(text):

    text = text.lower().strip()


    complaint_keywords = [

        "komplain",
        "complain",
        "keluhan",
        "mengeluh",

        "kecewa",
        "kecewain",

        "rusak",
        "tumpah",
        "bocor",

        "kurang",
        "kekurangan",

        "salah",
        "kesalahan",

        "beda",
        "berbeda",
        "tidak sesuai",
        "ga sesuai",
        "gak sesuai",

        "tidak ada",
        "ga ada",
        "gak ada",

        "belum datang",
        "belum sampai",

        "terlambat",
        "telat",

        "masalah",
        "kendala",

        "buruk",
        "parah",

        "porsi sedikit",
        "makanan sedikit",

        "makanan dingin",
        "nasi dingin",

        "pesanan salah",
        "pesanan kurang"

    ]


    return any(
        keyword in text
        for keyword in complaint_keywords
    )


# =========================================================
# CLEAN COMPLAINT TEXT
# =========================================================

def clean_complaint_text(text):

    complaint = text.strip()


    # -----------------------------------------------------
    # Hapus informasi nama
    # -----------------------------------------------------

    complaint = re.sub(
        r"\bnama saya\s+[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{1,40}",
        "",
        complaint,
        flags=re.IGNORECASE
    )


    complaint = re.sub(
        r"\bsaya\s+[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]{1,40}",
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

        complaint = complaint.replace(
            phone,
            ""
        )


    # -----------------------------------------------------
    # Hapus label umum
    # -----------------------------------------------------

    complaint = re.sub(
        r"\b(?:no|nomor|wa|whatsapp)\b",
        "",
        complaint,
        flags=re.IGNORECASE
    )


    complaint = re.sub(
        r"\s+",
        " ",
        complaint
    ).strip()


    complaint = complaint.strip(
        " ,.-:"
    )


    return complaint


# =========================================================
# SAVE CURRENT COMPLAINT
# =========================================================

def save_current_complaint():

    complaint_id = save_complaint(

        st.session_state.customer_name,

        st.session_state.customer_whatsapp,

        st.session_state.complaint_text

    )


    return complaint_id


# =========================================================
# RESET COMPLAINT PROCESS
# =========================================================

def reset_complaint_process():

    # -----------------------------------------------------
    # PENTING:
    # Nama dan WhatsApp TIDAK dihapus.
    # -----------------------------------------------------

    st.session_state.complaint_active = False

    st.session_state.complaint_step = None

    st.session_state.complaint_text = ""


# =========================================================
# START COMPLAINT FROM COMPLETE MESSAGE
# =========================================================

def process_complete_complaint(prompt):

    phone = extract_phone_number(
        prompt
    )


    name = extract_customer_name(
        prompt
    )


    complaint = clean_complaint_text(
        prompt
    )


    # -----------------------------------------------------
    # Jika nama ditemukan
    # -----------------------------------------------------

    if name:

        st.session_state.customer_name = name


    # -----------------------------------------------------
    # Jika WA ditemukan
    # -----------------------------------------------------

    if phone:

        st.session_state.customer_whatsapp = phone


    # -----------------------------------------------------
    # Jika complaint terdeteksi
    # -----------------------------------------------------

    if complaint and is_complaint_message(prompt):

        st.session_state.complaint_text = complaint


    # -----------------------------------------------------
    # Tentukan data yang masih kurang
    # -----------------------------------------------------

    missing_name = (
        not st.session_state.customer_name
    )


    missing_whatsapp = (
        not st.session_state.customer_whatsapp
    )


    missing_complaint = (
        not st.session_state.complaint_text
    )


    # -----------------------------------------------------
    # SEMUA LENGKAP
    # -----------------------------------------------------

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
                "ERROR COMPLETE COMPLAINT:",
                e
            )


            return (
                "Maaf kak, komplain belum berhasil "
                "disimpan. 😔\n\n"
                "Silakan coba kirim kembali informasinya."
            )


    # -----------------------------------------------------
    # NAMA BELUM ADA
    # -----------------------------------------------------

    if missing_name:

        st.session_state.complaint_active = True

        st.session_state.complaint_step = "name"


        return (
            "Mohon maaf ya kak atas kendalanya 🙏\n\n"
            "Saya bantu catat komplainnya agar dapat "
            "ditindaklanjuti oleh Admin Kays Kitchen.\n\n"
            "Boleh saya tahu nama kakak?"
        )


    # -----------------------------------------------------
    # WHATSAPP BELUM ADA
    # -----------------------------------------------------

    if missing_whatsapp:

        st.session_state.complaint_active = True

        st.session_state.complaint_step = "whatsapp"


        return (
            f"Baik kak {st.session_state.customer_name}. "
            "Saya bantu catat komplainnya. 🙏\n\n"
            "Boleh saya minta nomor WhatsApp kakak "
            "yang bisa dihubungi Admin?"
        )


    # -----------------------------------------------------
    # COMPLAINT BELUM ADA
    # -----------------------------------------------------

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

        if (
            st.session_state.complaint_step
            == "name"
        ):

            # ------------------------------------------------
            # Coba cari nama dari kalimat
            # ------------------------------------------------

            detected_name = extract_customer_name(
                prompt
            )


            # ------------------------------------------------
            # Jika nama ditemukan
            # ------------------------------------------------

            if detected_name:

                st.session_state.customer_name = (
                    detected_name
                )


            # ------------------------------------------------
            # Jika user hanya memberikan nama
            # ------------------------------------------------

            elif looks_like_name(prompt):

                st.session_state.customer_name = (
                    prompt.strip()
                )


            # ------------------------------------------------
            # Jika ternyata masih isi komplain
            # ------------------------------------------------

            else:

                # --------------------------------------------
                # PENTING:
                # Jangan buang komplain awal.
                # --------------------------------------------

                if is_complaint_message(prompt):

                    st.session_state.complaint_text = (
                        clean_complaint_text(prompt)
                    )


                answer = (
                    "Mohon maaf ya kak atas kendalanya 🙏\n\n"
                    "Saya bantu catat komplainnya.\n\n"
                    "Boleh saya tahu nama kakak?"
                )


            # ------------------------------------------------
            # Kalau nama berhasil ditemukan
            # ------------------------------------------------

            if (
                not answer
                and
                st.session_state.customer_name
            ):

                # --------------------------------------------
                # Jika WA juga ada dalam pesan yang sama
                # --------------------------------------------

                phone = extract_phone_number(
                    prompt
                )


                if phone:

                    st.session_state.customer_whatsapp = (
                        phone
                    )


                # --------------------------------------------
                # Kalau complaint juga ada
                # --------------------------------------------

                if is_complaint_message(prompt):

                    complaint = clean_complaint_text(
                        prompt
                    )


                    if complaint:

                        st.session_state.complaint_text = (
                            complaint
                        )


                # --------------------------------------------
                # Tentukan langkah berikutnya
                # --------------------------------------------

                if not st.session_state.customer_whatsapp:

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


                elif not st.session_state.complaint_text:

                    st.session_state.complaint_step = (
                        "complaint"
                    )


                    answer = (
                        "Terima kasih, kak. 🙏\n\n"
                        "Sekarang boleh ceritakan secara detail "
                        "kendala atau komplain yang kakak alami?"
                    )


                else:

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
                            "ERROR SAVE COMPLAINT:",
                            e
                        )


                        answer = (
                            "Maaf kak, komplain belum berhasil "
                            "disimpan. 😔\n\n"
                            "Silakan coba lagi."
                        )


        # =================================================
        # STEP WHATSAPP
        # =================================================

        elif (
            st.session_state.complaint_step
            == "whatsapp"
        ):

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


                # --------------------------------------------
                # Kalau complaint sudah disimpan sementara
                # --------------------------------------------

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
                            "ERROR SAVE COMPLAINT:",
                            e
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

        elif (
            st.session_state.complaint_step
            == "complaint"
        ):

            st.session_state.complaint_text = (
                clean_complaint_text(prompt)
            )


            if not st.session_state.complaint_text:

                answer = (
                    "Boleh ceritakan sedikit lebih detail "
                    "tentang kendalanya ya kak? 🙏"
                )


            else:

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
                        "ERROR SAVE COMPLAINT:",
                        e
                    )


                    answer = (
                        "Maaf kak, komplain belum berhasil "
                        "disimpan. 😔\n\n"
                        "Silakan coba lagi."
                    )


    # =====================================================
    # START NEW COMPLAINT
    # =====================================================

    elif is_complaint_message(prompt):

        # -------------------------------------------------
        # Jika customer sudah dikenal
        # -------------------------------------------------

        if (
            st.session_state.customer_name
            and
            st.session_state.customer_whatsapp
        ):

            # ---------------------------------------------
            # Simpan komplain langsung
            # ---------------------------------------------

            st.session_state.complaint_text = (
                clean_complaint_text(prompt)
            )


            if st.session_state.complaint_text:

                try:

                    complaint_id = save_current_complaint()


                    answer = (
                        f"Baik kak "
                        f"{st.session_state.customer_name}, "
                        "saya bantu catat komplainnya. 🙏\n\n"
                        "Komplain kakak sudah berhasil saya catat "
                        f"dengan nomor laporan **#{complaint_id}**.\n\n"
                        "Komplain akan disampaikan kepada Admin "
                        "Kays Kitchen untuk ditindaklanjuti.\n\n"
                        "Admin akan menghubungi kakak melalui "
                        "WhatsApp yang sudah diberikan."
                    )


                    reset_complaint_process()


                except Exception as e:

                    print(
                        "ERROR SAVE KNOWN CUSTOMER:",
                        e
                    )


                    answer = (
                        "Maaf kak, komplain belum berhasil "
                        "disimpan. 😔"
                    )


            else:

                st.session_state.complaint_active = True

                st.session_state.complaint_step = (
                    "complaint"
                )


                answer = (
                    "Baik kak, saya bantu catat komplainnya. 🙏\n\n"
                    "Boleh ceritakan detail kendalanya?"
                )


        # -------------------------------------------------
        # Customer belum dikenal
        # -------------------------------------------------

        else:

            st.session_state.complaint_active = True

            st.session_state.complaint_step = "name"


            # ---------------------------------------------
            # Simpan complaint yang sudah diberikan
            # ---------------------------------------------

            complaint = clean_complaint_text(
                prompt
            )


            if complaint:

                st.session_state.complaint_text = (
                    complaint
                )


            # ---------------------------------------------
            # Coba ambil nama + WA jika langsung diberikan
            # ---------------------------------------------

            detected_name = extract_customer_name(
                prompt
            )


            detected_phone = extract_phone_number(
                prompt
            )


            if detected_name:

                st.session_state.customer_name = (
                    detected_name
                )


            if detected_phone:

                st.session_state.customer_whatsapp = (
                    detected_phone
                )


            # ---------------------------------------------
            # Semua lengkap
            # ---------------------------------------------

            if (
                st.session_state.customer_name
                and
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
                        "ERROR SAVE COMPLETE:",
                        e
                    )


                    answer = (
                        "Maaf kak, komplain belum berhasil "
                        "disimpan. 😔"
                    )


            # ---------------------------------------------
            # Nama sudah ada
            # ---------------------------------------------

            elif st.session_state.customer_name:

                if st.session_state.customer_whatsapp:

                    st.session_state.complaint_step = (
                        "complaint"
                    )


                    answer = (
                        f"Baik kak "
                        f"{st.session_state.customer_name}. 🙏\n\n"
                        "Boleh ceritakan detail kendalanya?"
                    )


                else:

                    st.session_state.complaint_step = (
                        "whatsapp"
                    )


                    answer = (
                        f"Baik kak "
                        f"{st.session_state.customer_name}. 😊\n\n"
                        "Boleh saya minta nomor WhatsApp kakak "
                        "yang bisa dihubungi Admin?"
                    )


            # ---------------------------------------------
            # Nama belum ada
            # ---------------------------------------------

            else:

                st.session_state.complaint_step = "name"


                answer = (
                    "Mohon maaf ya kak atas kendalanya 🙏\n\n"
                    "Saya bantu catat komplainnya agar dapat "
                    "ditindaklanjuti oleh Admin Kays Kitchen.\n\n"
                    "Boleh saya tahu nama kakak?"
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
                e
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