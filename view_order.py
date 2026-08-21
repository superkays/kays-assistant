import sqlite3

connection = sqlite3.connect("orders.db")

cursor = connection.cursor()

cursor.execute("""
    SELECT
        id,
        customer_name,
        sambal_matah,
        sambal_bawang,
        total_porsi,
        total_harga,
        status
    FROM orders
""")

orders = cursor.fetchall()

connection.close()

print("DAFTAR PESANAN")
print("=" * 60)

for order in orders:
    print("ID            :", order[0])
    print("Customer      :", order[1])
    print("Sambal Matah  :", order[2])
    print("Sambal Bawang :", order[3])
    print("Total Porsi   :", order[4])
    print("Total Harga   : Rp", order[5])
    print("Status        :", order[6])
    print("-" * 60)