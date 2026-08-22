import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

from ai_order import parse_order
from process_order import process_order
from database import create_database


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

# Pastikan database dan tabel orders tersedia
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
    api_key = os.getenv("OPENAI_API_KEY")


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

- Cara order: WhatsApp
- Nomor WhatsApp: 085882101190
- Delivery: Bisa
- Area delivery: Sekitar Bandar Lampung
- Pembayaran: Transfer / QRIS


KEBIJAKAN:

- Pembatalan dapat dilakukan sebelum produk dikirim.
- Refund diberikan jika makanan rusak atau tumpah.
- Komplain melalui chatbot dan nanti akan disampaikan kepada Owner..


PROMO:

- Pembelian di atas 20 pcs mendapatkan potongan harga.
- Nominal potongan harga belum ditentukan.
"""


# =========================================================
# AI INSTRUCTIONS
# =========================================================

instructions = f"""
Kamu adalah AI Customer Service Kays Kitchen,
bernama Mika.

Kays Kitchen adalah UMKM yang menjual ricebowl ayam popcorn.

Tugas kamu adalah membantu customer dengan ramah,
singkat, natural, dan jelas.

Jawab hanya pertanyaan yang ditanyakan oleh customer.

Jangan memberikan informasi tambahan yang tidak diperlukan.

Jika customer menawarkan atau menanyakan sesuatu yang
tidak ada di Knowledge Base, jangan mengarang jawaban.

Jika informasi tidak tersedia, katakan bahwa informasi
tersebut belum tersedia.

Jika customer membutuhkan informasi lebih lanjut di luar
Knowledge Base, arahkan customer untuk menghubungi WhatsApp
Kays Kitchen di:

085882101190

ATURAN WHATSAPP:

- Hanya berikan nomor WhatsApp jika customer meminta nomor.
- Berikan nomor WhatsApp jika pertanyaan customer tidak
  dapat dijawab berdasarkan Knowledge Base.
- Jika kamu menawarkan nomor WhatsApp dan customer menjawab
  "mau", "iya", "boleh", atau maksud yang sama,
  segera berikan nomor WhatsApp.

ATURAN PERCAKAPAN:

- Panggil customer dengan sebutan kak.
- Jika percakapan sudah berjalan, jangan memperkenalkan diri
  sebagai Mika lagi.
- Jangan mengulang salam jika tidak diperlukan.
- Jika customer bercanda, kamu boleh membalas dengan ringan.
- Tetap sopan dan ramah.
- Jangan membuat harga, menu, promo, jam buka, atau kebijakan
  yang tidak ada di Knowledge Base.

Knowledge Base:

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
# ORDER DETECTION
# =========================================================

def is_order_message(text):

    text = text.lower()

    kata_pesan = [

        "mau",
        "pesan",
        "pesen",
        "order",
        "ambil",
        "beli",
        "pesanan"

    ]

    kata_menu = [

        "sambal matah",
        "sambal bawang",
        "matah",
        "bawang",
        "ricebowl"

    ]

    ada_kata_pesan = any(
        kata in text
        for kata in kata_pesan
    )

    ada_kata_menu = any(
        kata in text
        for kata in kata_menu
    )

    ada_angka = any(
        char.isdigit()
        for char in text
    )

    return (
        ada_kata_pesan
        and
        ada_kata_menu
        and
        ada_angka
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


    # =====================================================
    # ORDER
    # =====================================================

    if is_order_message(prompt):

        try:

            # =============================================
            # PARSE ORDER
            # =============================================

            order_data = parse_order(
                client,
                prompt
            )


            sambal_matah = int(
                order_data["sambal_matah"]
            )


            sambal_bawang = int(
                order_data["sambal_bawang"]
            )


            # =============================================
            # CUSTOMER NAME
            # =============================================

            customer_name = "Customer"


            # =============================================
            # PROCESS ORDER
            # =============================================

            process_order(

                customer_name,

                sambal_matah,

                sambal_bawang

            )


            # =============================================
            # CALCULATE TOTAL
            # =============================================

            total_porsi = (
                sambal_matah
                +
                sambal_bawang
            )


            total_harga = (
                total_porsi
                *
                18000
            )


            # =============================================
            # FORMAT PRICE
            # =============================================

            harga_format = (
                f"Rp {total_harga:,}"
                .replace(",", ".")
            )


            # =============================================
            # RESPONSE
            # =============================================

            answer = f"""
            🎉 **Pesanan berhasil diproses!**

            👤 **Customer**
            {customer_name}

            🌶️ **Detail Pesanan**

            Sambal Matah : {sambal_matah} porsi  
            Sambal Bawang : {sambal_bawang} porsi  

            🍚 **Total Porsi**
            {total_porsi} porsi

            💰 **Total Harga**
            **{harga_format}**

            Terima kasih sudah memesan di **Kays Kitchen**! ❤️
            """


        except Exception as e:

            answer = (
                "Maaf, pesanan belum berhasil "
                "diproses. 😔"
            )

            print(
                "ERROR ORDER:",
                e
            )


    # =====================================================
    # CUSTOMER SERVICE
    # =====================================================

    else:

        try:

            # =============================================
            # KIRIM HISTORY CHAT KE AI
            # =============================================

            chat_history = []

            for message in st.session_state.messages:

                chat_history.append({

                    "role": message["role"],

                    "content": message["content"]

                })


            # =============================================
            # AI RESPONSE
            # =============================================

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
                "Maaf, Mika sedang mengalami "
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