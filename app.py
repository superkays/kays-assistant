import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

from ai_order import parse_order
from process_order import process_order

# ==========================================
# CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Kays Assistant",
    page_icon="🍗"
)

# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("API key tidak ditemukan.")
    st.stop()

client = OpenAI(api_key=api_key)

# ==========================================
# KNOWLEDGE BASE
# ==========================================

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
- Komplain melalui WhatsApp.

PROMO:
- Pembelian di atas 20 pcs mendapatkan potongan harga.
- Nominal potongan harga belum ditentukan.
"""

# ==========================================
# AI INSTRUCTIONS
# ==========================================

instructions = f"""
Kamu adalah AI Customer Service Kays Kitchen, bernama Mika.

Kays Kitchen adalah UMKM yang menjual ricebowl
ayam popcorn.

jawab hanya pertanyaan yang ditanyakan oleh customer, dan bersikap ramahlah.

Kalau kamu menawarkan nomer Whatsapp dan customer bilang "mau", artinya dia mau nomer whatsapp, segera kirim.

Hanya bagikan nomer whatsapp Admin bila customer meminta,
atau bila ada pertanyaan yang tidak bisa kamu jawab kerena tidak ada didalam knowladge base.

Gunakan Knowledge Base berikut sebagai sumber informasi:

{knowledge_base}

ATURAN PENTING:

1. Jawab berdasarkan Knowledge Base.
2. Jangan mengarang informasi.
3. Jangan membuat harga, promo, menu, atau kebijakan
   yang tidak tersedia.
4. Jika informasi tidak tersedia, katakan bahwa
   informasi tersebut belum tersedia.
5. Jika customer membutuhkan informasi lebih lanjut diluar knowlade,
   arahkan customer untuk menghubungi WhatsApp
   Kays Kitchen di 085882101190.
6. Jawab dengan ramah, singkat, dan jelas. Tertawa bila jawaban customer terlihat bercanda.
7. Jangan memberikan informasi tambahan yang tidak
   diperlukan oleh customer.
8. Hanya berikan nomer whatsapp bila customer meminta, atau ada
   informasi yang tidak bisa kamu jawab.
9. Jangan pernah memperkenalkan diri lagi jika riwayat percakapan (chat history) sudah dimulai atau lebih dari satu pesan.
"""

# ==========================================
# DETEKSI PESANAN
# ==========================================

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

    ada_kata_pesan = any(kata in text for kata in kata_pesan)
    ada_kata_menu = any(kata in text for kata in kata_menu)

    # Cek apakah ada angka
    ada_angka = any(char.isdigit() for char in text)

    return ada_kata_pesan and ada_kata_menu and ada_angka

# ==========================================
# PAGE
# ==========================================

st.title("🍗 Kays Kitchen")
st.caption("Kays Customer Service")

# ==========================================
# CHAT MEMORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================
# USER INPUT
# ==========================================

prompt = st.chat_input("Tulis pertanyaan kamu...")

if prompt:

    # ======================================
    # SIMPAN PESAN CUSTOMER
    # ======================================

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # ======================================
    # TAMPILKAN PESAN CUSTOMER
    # ======================================

    with st.chat_message("user"):
        st.write(prompt)

    # ======================================
    # CEK APAKAH CUSTOMER MEMBUAT PESANAN
    # ======================================

    if is_order_message(prompt):

        try:

            # ==================================
            # PARSE PESANAN DENGAN AI
            # ==================================

            order_data = parse_order(client, prompt)

            sambal_matah = order_data["sambal_matah"]
            sambal_bawang = order_data["sambal_bawang"]

            # ==================================
            # PROSES PESANAN
            # ==================================

            customer_name = "Customer"

            process_order(
                customer_name,
                sambal_matah,
                sambal_bawang
            )

            # ==================================
            # HITUNG TOTAL
            # ==================================

            total_porsi = sambal_matah + sambal_bawang
            total_harga = total_porsi * 18000

            answer = f"""
Pesanan berhasil diproses. 🎉

Customer : {customer_name}
Sambal Matah : {sambal_matah}
Sambal Bawang : {sambal_bawang}
Total Porsi : {total_porsi}
Total Harga : Rp {total_harga:,}
""".replace(",", ".")

        except Exception as e:

            answer = f"Maaf, pesanan belum berhasil diproses. 😔"

            print("ERROR ORDER:", e)

    # ======================================
    # BUKAN PESANAN → CUSTOMER SERVICE
    # ======================================

    else:

        response = client.responses.create(
            model="gpt-5-mini",
            instructions=instructions,
            input=prompt
        )

        answer = response.output_text

    # ======================================
    # TAMPILKAN JAWABAN AI
    # ======================================

    with st.chat_message("assistant"):
        st.write(answer)

    # ======================================
    # SIMPAN JAWABAN AI
    # ======================================

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })