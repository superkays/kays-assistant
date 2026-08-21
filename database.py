import sqlite3


def create_database():

    connection = sqlite3.connect("orders.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            sambal_matah INTEGER,
            sambal_bawang INTEGER,
            total_porsi INTEGER,
            total_harga INTEGER,
            status TEXT
        )
    """)

    connection.commit()
    connection.close()

def save_order(
    customer_name,
    sambal_matah,
    sambal_bawang,
    total_porsi,
    total_harga,
    status="Pending"
):

    connection = sqlite3.connect("orders.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO orders (
            customer_name,
            sambal_matah,
            sambal_bawang,
            total_porsi,
            total_harga,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        customer_name,
        sambal_matah,
        sambal_bawang,
        total_porsi,
        total_harga,
        status
    ))

    connection.commit()
    connection.close()
    
if __name__ == "__main__":
    create_database()
    print("Database berhasil dibuat.")