import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DATABASE_NAME = "complaints.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    return connection


# =========================================================
# CREATE / MIGRATE DATABASE
# =========================================================

def create_database():

    connection = get_connection()

    cursor = connection.cursor()


    # =====================================================
    # CEK APAKAH TABEL COMPLAINTS SUDAH ADA
    # =====================================================

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = 'complaints'
    """)

    table_exists = cursor.fetchone()


    # =====================================================
    # JIKA BELUM ADA
    # =====================================================

    if not table_exists:

        cursor.execute("""
            CREATE TABLE complaints (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                created_at TEXT,

                customer_name TEXT,

                customer_whatsapp TEXT,

                complaint_text TEXT,

                status TEXT DEFAULT 'Pending'

            )
        """)

        connection.commit()

        connection.close()

        return


    # =====================================================
    # CEK STRUKTUR TABEL LAMA
    # =====================================================

    cursor.execute("""
        PRAGMA table_info(complaints)
    """)

    columns = cursor.fetchall()


    existing_columns = [

        column[1]

        for column in columns

    ]


    # =====================================================
    # CEK APAKAH DATABASE MASIH MENGGUNAKAN
    # KOLOM "whatsapp" LAMA
    # =====================================================

    old_whatsapp_exists = (
        "whatsapp"
        in existing_columns
    )


    customer_whatsapp_exists = (
        "customer_whatsapp"
        in existing_columns
    )


    # =====================================================
    # MIGRATION DATABASE LAMA
    # =====================================================

    if old_whatsapp_exists:

        print(
            "Database lama terdeteksi."
        )

        print(
            "Memulai migration..."
        )


        # -------------------------------------------------
        # Rename tabel lama
        # -------------------------------------------------

        cursor.execute("""
            ALTER TABLE complaints
            RENAME TO complaints_old
        """)


        # -------------------------------------------------
        # Buat tabel baru
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE complaints (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                created_at TEXT,

                customer_name TEXT,

                customer_whatsapp TEXT,

                complaint_text TEXT,

                status TEXT DEFAULT 'Pending'

            )
        """)


        # -------------------------------------------------
        # Ambil data dari tabel lama
        # -------------------------------------------------

        cursor.execute("""
            SELECT

                id,
                created_at,
                customer_name,
                whatsapp,
                complaint_text,
                status

            FROM complaints_old
        """)


        old_complaints = cursor.fetchall()


        # -------------------------------------------------
        # Pindahkan data lama
        # -------------------------------------------------

        for complaint in old_complaints:

            (
                complaint_id,
                created_at,
                customer_name,
                whatsapp,
                complaint_text,
                status

            ) = complaint


            cursor.execute("""
                INSERT INTO complaints (

                    id,
                    created_at,
                    customer_name,
                    customer_whatsapp,
                    complaint_text,
                    status

                )

                VALUES (?, ?, ?, ?, ?, ?)
            """, (

                complaint_id,
                created_at,
                customer_name,
                whatsapp,
                complaint_text,
                status or "Pending"

            ))


        # -------------------------------------------------
        # Hapus tabel lama
        # -------------------------------------------------

        cursor.execute("""
            DROP TABLE complaints_old
        """)


        connection.commit()


        print(
            "Migration database berhasil."
        )


    # =====================================================
    # JIKA SUDAH MENGGUNAKAN STRUKTUR BARU
    # =====================================================

    else:

        # -------------------------------------------------
        # Pastikan semua kolom tersedia
        # -------------------------------------------------

        required_columns = {

            "created_at":
                "TEXT",

            "customer_name":
                "TEXT",

            "customer_whatsapp":
                "TEXT",

            "complaint_text":
                "TEXT",

            "status":
                "TEXT DEFAULT 'Pending'"

        }


        for column_name, column_type in required_columns.items():

            if column_name not in existing_columns:

                cursor.execute(
                    f"""
                    ALTER TABLE complaints
                    ADD COLUMN {column_name}
                    {column_type}
                    """
                )


        connection.commit()


    connection.close()


# =========================================================
# SAVE COMPLAINT
# =========================================================

def save_complaint(
    customer_name,
    customer_whatsapp,
    complaint_text,
    status="Pending"
):

    # Pastikan database sudah benar
    create_database()


    connection = None


    try:

        connection = get_connection()

        cursor = connection.cursor()


        # -------------------------------------------------
        # WAKTU INDONESIA GMT+7
        # -------------------------------------------------

        created_at = datetime.now(
            ZoneInfo("Asia/Jakarta")
        ).strftime(
            "%d/%m/%Y %H:%M:%S"
        )


        # -------------------------------------------------
        # SIMPAN COMPLAINT
        # -------------------------------------------------

        cursor.execute("""
            INSERT INTO complaints (

                created_at,
                customer_name,
                customer_whatsapp,
                complaint_text,
                status

            )

            VALUES (?, ?, ?, ?, ?)
        """, (

            created_at,
            customer_name,
            customer_whatsapp,
            complaint_text,
            status

        ))


        # -------------------------------------------------
        # AMBIL ID
        # -------------------------------------------------

        complaint_id = cursor.lastrowid


        # -------------------------------------------------
        # COMMIT
        # -------------------------------------------------

        connection.commit()


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

        if connection:

            connection.rollback()


        print(
            "===================================="
        )

        print(
            "ERROR SAVE COMPLAINT"
        )

        print(
            type(e).__name__
        )

        print(
            str(e)
        )

        print(
            "===================================="
        )


        raise


    finally:

        if connection:

            connection.close()


# =========================================================
# GET ALL COMPLAINTS
# =========================================================

def get_complaints():

    create_database()


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""
        SELECT

            id,
            created_at,
            customer_name,
            customer_whatsapp,
            complaint_text,
            status

        FROM complaints

        ORDER BY id DESC
    """)


    complaints = cursor.fetchall()


    connection.close()


    return complaints


# =========================================================
# UPDATE COMPLAINT STATUS
# =========================================================

def update_complaint_status(
    complaint_id,
    new_status
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""
        UPDATE complaints

        SET status = ?

        WHERE id = ?
    """, (

        new_status,
        complaint_id

    ))


    connection.commit()

    connection.close()


# =========================================================
# TEST DATABASE
# =========================================================

if __name__ == "__main__":

    create_database()

    print(
        "Database complaint berhasil dibuat / dimigrasikan."
    )