from dotenv import load_dotenv
import os
import json
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("API key tidak ditemukan.")
    exit()

client = OpenAI(api_key=api_key)

question = """
Saya mau pesan 3 Kays Ricebowl Sambal Matah
dan 2 Kays Ricebowl Sambal Bawang.
"""

instructions = """
Kamu adalah sistem yang bertugas membaca pesanan Kays Kitchen.

Ambil jumlah masing-masing varian dari kalimat customer.

Produk yang tersedia:
- Kays Ricebowl Sambal Matah
- Kays Ricebowl Sambal Bawang

Kembalikan hasil HANYA dalam format JSON berikut:

{
    "sambal_matah": 0,
    "sambal_bawang": 0
}

Jangan tambahkan penjelasan lain.
"""

response = client.responses.create(
    model="gpt-5-mini",
    instructions=instructions,
    input=question
)

result = response.output_text

print("Pesanan customer:")
print(question)

print("\nData dari AI:")
print(result)

order = json.loads(result)

sambal_matah = order["sambal_matah"]
sambal_bawang = order["sambal_bawang"]

menu = {
    "sambal_matah": {
        "nama": "Kays Ricebowl Sambal Matah",
        "harga": 18000
    },
    "sambal_bawang": {
        "nama": "Kays Ricebowl Sambal Bawang",
        "harga": 18000
    }
}

sambal_matah = order["sambal_matah"]
sambal_bawang = order["sambal_bawang"]

harga_matah = menu["sambal_matah"]["harga"]
harga_bawang = menu["sambal_bawang"]["harga"]

total_matah = sambal_matah * harga_matah
total_bawang = sambal_bawang * harga_bawang

total_porsi = sambal_matah + sambal_bawang
total_harga = total_matah + total_bawang

print("\nHasil perhitungan:")
print("Sambal Matah:", sambal_matah)
print("Sambal Bawang:", sambal_bawang)
print("Total porsi:", total_porsi)
print("Total harga: Rp", total_harga)

print("\nRingkasan Pesanan:")
print("-----------------------------")

if sambal_matah > 0:
    print(
        f"{sambal_matah}x Kays Ricebowl Sambal Matah "
        f"= Rp {total_matah:,}"
    )

if sambal_bawang > 0:
    print(
        f"{sambal_bawang}x Kays Ricebowl Sambal Bawang "
        f"= Rp {total_bawang:,}"
    )

print("-----------------------------")
print(f"Total porsi : {total_porsi}")
print(f"Total harga : Rp {total_harga:,}")