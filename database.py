from supabase import create_client, Client
import streamlit as st
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import base64
import json


load_dotenv()


# =========================================================
# SUPABASE CONFIGURATION
# =========================================================

def get_secret(name):

    # -----------------------------------------------------
    # PRIORITAS 1: STREAMLIT SECRETS
    # -----------------------------------------------------

    try:

        value = st.secrets[name]

        if value:

            return value

    except Exception:

        pass


    # -----------------------------------------------------
    # PRIORITAS 2: ENVIRONMENT VARIABLE
    # -----------------------------------------------------

    value = os.getenv(name)

    if value:

        return value


    return None


# =========================================================
# SUPABASE URL
# =========================================================

SUPABASE_URL = get_secret(
    "SUPABASE_URL"
)


# =========================================================
# PUBLIC / PUBLISHABLE KEY
# =========================================================

SUPABASE_KEY = get_secret(
    "SUPABASE_KEY"
)


# =========================================================
# SERVICE ROLE KEY
# =========================================================

SUPABASE_SERVICE_ROLE_KEY = get_secret(
    "SUPABASE_SERVICE_ROLE_KEY"
)


# =========================================================
# VALIDATION
# =========================================================

if not SUPABASE_URL:

    raise RuntimeError(
        "SUPABASE_URL belum ditemukan."
    )


if not SUPABASE_KEY:

    raise RuntimeError(
        "SUPABASE_KEY belum ditemukan."
    )


# =========================================================
# PUBLIC CLIENT
# =========================================================

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# ADMIN CLIENT
# =========================================================

admin_supabase = None


if SUPABASE_SERVICE_ROLE_KEY:

    admin_supabase = create_client(
        SUPABASE_URL,
        SUPABASE_SERVICE_ROLE_KEY
    )


# =========================================================
# DIAGNOSTIC
# =========================================================

def decode_key_info(key):

    """
    Membaca informasi NON-RAHASIA dari JWT.

    Tidak mencetak key.

    Digunakan hanya untuk mengetahui role
    dari key yang sedang digunakan.
    """

    if not key:

        return {
            "format": "tidak ada",
            "role": None
        }


    # -----------------------------------------------------
    # Key baru Supabase biasanya bukan JWT
    # -----------------------------------------------------

    if not key.startswith("eyJ"):

        return {
            "format": "publishable / non-JWT",
            "role": None
        }


    try:

        parts = key.split(".")

        if len(parts) != 3:

            return {
                "format": "JWT tidak valid",
                "role": None
            }


        payload = parts[1]

        # Tambahkan padding jika diperlukan

        payload += "=" * (
            4 - len(payload) % 4
        )


        decoded = base64.urlsafe_b64decode(
            payload
        )


        data = json.loads(
            decoded.decode("utf-8")
        )


        return {
            "format": "JWT",
            "role": data.get("role"),
            "ref": data.get("ref"),
            "iss": data.get("iss")
        }


    except Exception:

        return {
            "format": "JWT tetapi gagal dibaca",
            "role": None
        }


# =========================================================
# CONNECTION DIAGNOSTIC
# =========================================================

def test_supabase_connection():

    print("")
    print("====================================")
    print("SUPABASE CONNECTION DIAGNOSTIC")
    print("====================================")


    # -----------------------------------------------------
    # URL
    # -----------------------------------------------------

    try:

        parsed_url = urlparse(
            SUPABASE_URL
        )

        print(
            "SUPABASE URL TERBACA : YES"
        )

        print(
            "SUPABASE HOST        :",
            parsed_url.netloc
        )

    except Exception:

        print(
            "SUPABASE URL TERBACA : FORMAT TIDAK VALID"
        )


    # -----------------------------------------------------
    # PUBLIC KEY
    # -----------------------------------------------------

    print(
        "SUPABASE KEY TERBACA :",
        "YES" if SUPABASE_KEY else "NO"
    )


    public_key_info = decode_key_info(
        SUPABASE_KEY
    )


    print(
        "PUBLIC KEY FORMAT    :",
        public_key_info.get("format")
    )


    if public_key_info.get("role"):

        print(
            "PUBLIC KEY ROLE      :",
            public_key_info.get("role")
        )


    if public_key_info.get("ref"):

        print(
            "PUBLIC KEY PROJECT   :",
            public_key_info.get("ref")
        )


    # -----------------------------------------------------
    # SERVICE ROLE
    # -----------------------------------------------------

    print(
        "SERVICE ROLE TERBACA :",
        "YES"
        if SUPABASE_SERVICE_ROLE_KEY
        else "NO"
    )


    service_key_info = decode_key_info(
        SUPABASE_SERVICE_ROLE_KEY
    )


    print(
        "SERVICE KEY FORMAT   :",
        service_key_info.get("format")
    )


    if service_key_info.get("role"):

        print(
            "SERVICE KEY ROLE     :",
            service_key_info.get("role")
        )


    if service_key_info.get("ref"):

        print(
            "SERVICE KEY PROJECT  :",
            service_key_info.get("ref")
        )


    print(
        "===================================="
    )


# =========================================================
# CREATE DATABASE
# =========================================================

def create_database():

    # Supabase sudah memiliki database.
    # Fungsi ini dipertahankan agar app.py lama
    # tetap kompatibel.

    return True


# =========================================================
# SAVE COMPLAINT
# =========================================================

def save_complaint(
    customer_name,
    customer_whatsapp,
    complaint_text,
    status="Pending"
):

    try:

        response = (
            supabase
            .table("complaints")
            .insert({

                "customer_name":
                    customer_name,

                "customer_whatsapp":
                    customer_whatsapp,

                "complaint_text":
                    complaint_text,

                "status":
                    status

            })
            .execute()
        )


        # =================================================
        # CEK HASIL INSERT
        # =================================================

        if not response.data:

            raise RuntimeError(
                "Supabase tidak mengembalikan data laporan."
            )


        # response.data adalah LIST

        complaint_id = response.data[0]["id"]


        # =================================================
        # LOG
        # =================================================

        print(
            "===================================="
        )

        print(
            "COMPLAINT BERHASIL DISIMPAN"
        )

        print(
            "ID:",
            complaint_id
        )

        print(
            "NAMA:",
            customer_name
        )

        print(
            "WHATSAPP:",
            customer_whatsapp
        )

        print(
            "COMPLAINT:",
            complaint_text
        )

        print(
            "===================================="
        )


        return complaint_id


    except Exception as e:

        print(
            "===================================="
        )

        print(
            "ERROR SUPABASE INSERT"
        )

        print(
            "TYPE:",
            type(e).__name__
        )

        print(
            "DETAIL:",
            str(e)
        )

        print(
            "===================================="
        )

        raise


# =========================================================
# GET ALL COMPLAINTS
# =========================================================

def get_complaints():

    if admin_supabase is None:

        raise RuntimeError(
            "SUPABASE_SERVICE_ROLE_KEY "
            "belum dikonfigurasi."
        )


    try:

        response = (
            admin_supabase
            .table("complaints")
            .select(
                "id, created_at, customer_name, "
                "customer_whatsapp, complaint_text, status"
            )
            .order(
                "id",
                desc=True
            )
            .execute()
        )


        complaints = []


        for row in response.data:

            complaints.append((

                row.get("id"),

                row.get("created_at"),

                row.get("customer_name"),

                row.get("customer_whatsapp"),

                row.get("complaint_text"),

                row.get("status")

            ))


        return complaints


    except Exception as e:

        print(
            "===================================="
        )

        print(
            "ERROR GET COMPLAINTS"
        )

        print(
            "TYPE:",
            type(e).__name__
        )

        print(
            "DETAIL:",
            str(e)
        )

        print(
            "===================================="
        )

        raise


# =========================================================
# UPDATE COMPLAINT STATUS
# =========================================================

def update_complaint_status(
    complaint_id,
    new_status
):

    if admin_supabase is None:

        raise RuntimeError(
            "SUPABASE_SERVICE_ROLE_KEY "
            "belum dikonfigurasi."
        )


    try:

        response = (
            admin_supabase
            .table("complaints")
            .update({

                "status":
                    new_status

            })
            .eq(
                "id",
                complaint_id
            )
            .execute()
        )


        return response.data


    except Exception as e:

        print(
            "===================================="
        )

        print(
            "ERROR UPDATE COMPLAINT"
        )

        print(
            "TYPE:",
            type(e).__name__
        )

        print(
            "DETAIL:",
            str(e)
        )

        print(
            "===================================="
        )

        raise


# =========================================================
# TEST PUBLIC INSERT
# =========================================================

def test_public_insert():

    print("")
    print("====================================")
    print("TEST PUBLIC INSERT")
    print("====================================")

    try:

        response = (
            supabase
            .table("complaints")
            .insert({
                "customer_name": "TEST USER",
                "customer_whatsapp": "080000000000",
                "complaint_text": "TEST RLS PUBLIC INSERT",
                "status": "Pending"
            })
            .execute()
        )

        print("PUBLIC INSERT BERHASIL")
        print("DATA:", response.data)

        return True

    except Exception as e:

        print("PUBLIC INSERT GAGAL")
        print("TYPE:", type(e).__name__)
        print("DETAIL:", str(e))

        return False

# =========================================================
# TEST PUBLIC INSERT VIA POSTGREST
# =========================================================

def test_public_insert_postgrest():

    import requests

    print("")
    print("====================================")
    print("TEST DIRECT POSTGREST")
    print("====================================")

    url = (
        SUPABASE_URL
        + "/rest/v1/complaints"
    )

    headers = {

        "apikey": SUPABASE_KEY,

        "Authorization":
            f"Bearer {SUPABASE_KEY}",

        "Content-Type":
            "application/json",

        "Prefer":
            "return=representation"

    }

    payload = {

        "customer_name":
            "TEST DIRECT AUTH",

        "customer_whatsapp":
            "080000000009",

        "complaint_text":
            "TEST DIRECT AUTH HEADER",

        "status":
            "Pending"

    }

    try:

        response = requests.post(

            url,

            headers=headers,

            json=payload,

            timeout=15

        )

        print(
            "HTTP STATUS:",
            response.status_code
        )

        print(
            "RESPONSE:",
            response.text
        )

    except Exception as e:

        print(
            "DIRECT POSTGREST GAGAL"
        )

        print(
            "TYPE:",
            type(e).__name__
        )

        print(
            "DETAIL:",
            str(e)
        )


# =========================================================
# TEST SECRET INSERT
# =========================================================

def test_secret_insert():

    print("")
    print("====================================")
    print("TEST SECRET INSERT")
    print("====================================")

    if admin_supabase is None:

        print("SECRET INSERT GAGAL")
        print("SUPABASE_SERVICE_ROLE_KEY tidak tersedia.")

        return False

    try:

        response = (
            admin_supabase
            .table("complaints")
            .insert({
                "customer_name": "TEST SECRET",
                "customer_whatsapp": "080000000002",
                "complaint_text": "TEST SECRET INSERT",
                "status": "Pending"
            })
            .execute()
        )

        print("SECRET INSERT BERHASIL")
        print("DATA:", response.data)

        return True

    except Exception as e:

        print("SECRET INSERT GAGAL")
        print("TYPE:", type(e).__name__)
        print("DETAIL:", str(e))

        return False

def test_key_identity():

    print("")
    print("====================================")
    print("TEST KEY IDENTITY")
    print("====================================")

    print(
        "SUPABASE KEY PREFIX:",
        SUPABASE_KEY[:20]
        if SUPABASE_KEY
        else "NONE"
    )

    print(
        "SUPABASE KEY LENGTH:",
        len(SUPABASE_KEY)
        if SUPABASE_KEY
        else 0
    )

    print(
        "SERVICE KEY PREFIX:",
        SUPABASE_SERVICE_ROLE_KEY[:20]
        if SUPABASE_SERVICE_ROLE_KEY
        else "NONE"
    )

    print(
        "SERVICE KEY LENGTH:",
        len(SUPABASE_SERVICE_ROLE_KEY)
        if SUPABASE_SERVICE_ROLE_KEY
        else 0
    )

    print(
        "SUPABASE URL:",
        SUPABASE_URL
    )

    print("====================================")


def test_legacy_anon_insert():

    import requests

    print("")
    print("====================================")
    print("TEST LEGACY ANON KEY")
    print("====================================")

    legacy_key = os.getenv(
        "SUPABASE_LEGACY_ANON_KEY"
    )

    if not legacy_key:

        print(
            "LEGACY ANON KEY TIDAK DITEMUKAN"
        )

        return

    url = (
        SUPABASE_URL
        + "/rest/v1/complaints"
    )

    headers = {

        "apikey": legacy_key,

        "Authorization":
            f"Bearer {legacy_key}",

        "Content-Type":
            "application/json",

        "Prefer":
            "return=representation"
    }

    payload = {

        "customer_name":
            "TEST LEGACY ANON",

        "customer_whatsapp":
            "080000000006",

        "complaint_text":
            "TEST LEGACY ANON KEY",

        "status":
            "Pending"
    }

    try:

        response = requests.post(

            url,

            headers=headers,

            json=payload,

            timeout=15
        )

        print(
            "HTTP STATUS:",
            response.status_code
        )

        print(
            "RESPONSE:",
            response.text
        )

    except Exception as e:

        print(
            "LEGACY ANON GAGAL"
        )

        print(
            "TYPE:",
            type(e).__name__
        )

        print(
            "DETAIL:",
            str(e)
        )

# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print(
        "Supabase database module aktif."
    )

    test_supabase_connection()

    test_public_insert()

    test_public_insert_postgrest()

    test_legacy_anon_insert()

    print("")
    print("====================================")
    print("TEST SAVE_COMPLAINT")
    print("====================================")

    try:

        result = save_complaint(
            "TEST SAVE FUNCTION",
            "080000000010",
            "TEST DARI FUNGSI SAVE_COMPLAINT"
        )

        print(
            "SAVE_COMPLAINT BERHASIL"
        )

        print(
            "ID:",
            result
        )

    except Exception as e:

        print(
            "SAVE_COMPLAINT GAGAL"
        )

        print(
            "TYPE:",
            type(e).__name__
        )

        print(
            "DETAIL:",
            str(e)
        )