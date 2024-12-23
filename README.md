# Toko Laundry CRUD Application in Python

Selamat datang di By Laundry, sebuah sistem manajemen laundry berbasis Python yang dilengkapi dengan antarmuka terminal interaktif dan dukungan database MySQL. Proyek ini dirancang untuk memudahkan pengelolaan data pelanggan, pakaian, pesanan, dan riwayat transaksi dalam bisnis laundry.

## 📋 Fitur Utama
- Data Pelanggan: Menambahkan, melihat, memperbarui, dan menghapus data pelanggan.
- Jenis Pakaian: Mengelola daftar jenis pakaian beserta harga layanan.
- Pesanan Laundry: Membuat, melihat, memperbarui status, dan menghapus pesanan.
- Riwayat Transaksi: Melihat dan mencari riwayat transaksi serta mencetak struk.

## 🔧 Prasyarat
Sebelum menjalankan proyek ini, pastikan Anda memiliki:
- Python 3.10 atau versi lebih baru.
- MySQL Server.
- dan Library paket Python: **mysql-connector-python**, **rich**, **pyfiget**

## 🚀 Cara Menjalankan
1. Clone repositori ini:
   ```bash
   git clone https://github.com/username/by-laundry.git
   cd by-laundry
2. Pastikan Python dan MySQL telah terinstal di perangkat Anda.
3. Instal dependensi Python:
   ```bash
   pip install mysql-connector-python rich pyfiglet
4. Konfigurasikan koneksi database di file Database.py. Pastikan host, user, dan password sesuai dengan konfigurasi MySQL Anda.
5. Jalankan file **Database.py** untuk membuat database dan tabel:
   ```bash
   python Database.py
6. Jalankan aplikasi:
   ```bash
   python main.py

## 📆 Contoh Data Awal:
Jenis pakaian dan harga layanan yang sudah tersedia di database:
- Kemeja: Rp10.000
- Celana Panjang: Rp12.000
- Jaket: Rp15.000
- Hoodie: Rp15.000
- Selimut: Rp25.000 ... (dan lainnya)

## 💡 Penggunaan:
1. Jalankan aplikasi dengan **python main.py.**
2. Pilih menu interaktif untuk:
   - Menambah pelanggan
   - Membuat pesanan
   - Melihat atau mengedit data
