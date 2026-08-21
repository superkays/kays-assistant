import json


# ==========================================
# AI ORDER PARSER
# ==========================================

def parse_order(client, question):

    instructions = """
Kamu adalah AI parser pesanan Kays Kitchen.

Tugas kamu membaca pesan customer dan mengubahnya menjadi JSON.

Format JSON WAJIB:

{
    "sambal_matah": angka,
    "sambal_bawang": angka
}

Aturan:

1. sambal_matah adalah jumlah Kays Ricebowl Sambal Matah
   yang diminta customer.

2. sambal_bawang adalah jumlah Kays Ricebowl Sambal Bawang
   yang diminta customer.

3. Jika customer menyebut jumlah masing-masing varian,
   gunakan jumlah tersebut.

4. Jika suatu varian tidak disebutkan,
   gunakan angka 0.

5. Jangan membuat jumlah sendiri.

6. Jangan menghitung total porsi.

7. Jangan menghitung harga.

8. Hanya keluarkan JSON tanpa penjelasan tambahan.

Contoh:

Customer:
"Saya mau 3 sambal matah dan 2 sambal bawang."

Output:
{
    "sambal_matah": 3,
    "sambal_bawang": 2
}

Contoh:

Customer:
"Saya mau 4 sambal matah."

Output:
{
    "sambal_matah": 4,
    "sambal_bawang": 0
}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=instructions,
        input=question
    )

    ai_text = response.output_text

    # ==========================================
    # UBAH JSON MENJADI DATA PYTHON
    # ==========================================

    order_data = json.loads(ai_text)

    sambal_matah = order_data["sambal_matah"]
    sambal_bawang = order_data["sambal_bawang"]

    # ==========================================
    # VALIDASI DATA
    # ==========================================

    if not isinstance(sambal_matah, int):
        raise ValueError("Jumlah sambal matah tidak valid.")

    if not isinstance(sambal_bawang, int):
        raise ValueError("Jumlah sambal bawang tidak valid.")

    if sambal_matah < 0 or sambal_bawang < 0:
        raise ValueError("Jumlah pesanan tidak boleh negatif.")

    return {
        "sambal_matah": sambal_matah,
        "sambal_bawang": sambal_bawang
    }


# ==========================================
# TEST MANUAL
# ==========================================

if __name__ == "__main__":

    from dotenv import load_dotenv
    import os
    from openai import OpenAI

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("API key tidak ditemukan.")
        exit()

    client = OpenAI(api_key=api_key)

    question = input("Pesanan customer: ")

    result = parse_order(client, question)

    print()
    print("Data pesanan:")
    print(result)