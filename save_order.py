import sqlite3


# Data pesanan
customer_name = "Budi"
sambal_matah = 3
sambal_bawang = 2
total_porsi = 5
total_harga = 90000
status = "Pending"


# Hubungkan ke database
connection = sqlite3.connect("orders.db")

cursor = connection.cursor()


# Simpan pesanan
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


# Simpan perubahan
connection.commit()

connection.close()


print("Pesanan berhasil disimpan.")