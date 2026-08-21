from database import save_order


# =========================
# HARGA PRODUK
# =========================

HARGA_RICEBOWL = 18000


# =========================
# FUNGSI PROSES PESANAN
# =========================

def process_order(customer, sambal_matah, sambal_bawang):

    # Hitung total porsi
    total_porsi = sambal_matah + sambal_bawang

    # Hitung total harga
    total_harga = total_porsi * HARGA_RICEBOWL

    # Simpan ke database
    save_order(
        customer,
        sambal_matah,
        sambal_bawang,
        total_porsi,
        total_harga
    )

    # Tampilkan hasil
    print("Pesanan berhasil diproses.")
    print()
    print("Customer      :", customer)
    print("Sambal Matah  :", sambal_matah)
    print("Sambal Bawang :", sambal_bawang)
    print("Total Porsi   :", total_porsi)
    print("Total Harga   : Rp", total_harga)


# =========================
# TEST
# =========================

if __name__ == "__main__":

    process_order(
        "Budi",
        3,
        2
    )