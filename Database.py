import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
)
    
cursor = connection.cursor()

try:
    # Buat database jika belum ada
    cursor.execute('CREATE DATABASE IF NOT EXISTS by_laundry')
    print("Database Berhasil Dibuat atau Sudah Ada")

    # Pilih database
    cursor.execute("USE by_laundry")

    # Buat tabel pelanggan jika belum ada
    cursor.execute("""
    CREATE TABLE pelanggan (
        id_pelanggan INT AUTO_INCREMENT PRIMARY KEY,
        nama VARCHAR(100) NOT NULL,
        alamat VARCHAR(255),
        no_telepon VARCHAR(15),
        tanggal_bergabung DATE DEFAULT CURRENT_DATE
    );
    """)
    print("Tabel pelanggan Berhasil Dibuat!!")

    # Buat tabel jenis_pelanggan jika belum ada
    cursor.execute("""
    CREATE TABLE jenis_pakaian (
        id_jenis INT AUTO_INCREMENT PRIMARY KEY,
        jenis_pakaian VARCHAR(50) NOT NULL,
        harga DECIMAL(10, 2) NOT NULL
    );
    """)
    print("Tabel jenis_pelanggan Berhasil Dibuat!!")

    # Buat tabel pesanan jika belum ada
    cursor.execute("""
    CREATE TABLE pesanan (
        id_pesanan INT AUTO_INCREMENT PRIMARY KEY,
        id_pelanggan INT NOT NULL,
        tanggal_pesanan DATE DEFAULT CURRENT_DATE,
        total_harga DECIMAL(10, 2) NOT NULL,
        status ENUM('Diproses', 'Selesai', 'Diambil') DEFAULT 'Diproses',
        FOREIGN KEY (id_pelanggan) REFERENCES pelanggan (id_pelanggan) ON UPDATE CASCADE
    );
    """)
    print("Tabel pesanan Berhasil Dibuat!!")

    # Buat tabel detail_pesanan jika belum ada
    cursor.execute("""
    CREATE TABLE detail_pesanan (
        id_detail INT AUTO_INCREMENT PRIMARY KEY,
        id_pesanan INT NOT NULL,
        id_jenis INT NOT NULL,
        jumlah INT NOT NULL,
        sub_total DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (id_pesanan) REFERENCES pesanan (id_pesanan) ON UPDATE CASCADE,
        FOREIGN KEY (id_jenis) REFERENCES jenis_pakaian (id_jenis) ON UPDATE CASCADE
    );
    """)
    print("Tabel detail_pesanan Berhasil Dibuat!!")

    # manambahkan data kedalam tabel jenis pakaian
    cursor.execute("""
    INSERT INTO jenis_pakaian (jenis_pakaian, harga) VALUES
    ('Kemeja', 10000),
    ('Celana Panjang', 12000),
    ('Celana Pendek', 8000),
    ('Kaos', 7000),
    ('Jaket', 15000),
    ('Sweater', 14000),
    ('Selimut', 25000),
    ('Seprai', 15000),
    ('Handuk', 8000),
    ('Mukena', 10000),
    ('Sarung', 8000),
    ('Kain Batik', 12000),
    ('Hoodie', 15000),
    ('Celana Training', 10000),
    ('Jas', 25000),
    ('Rok', 10000);
    """)
    print("Tabel detail_pesanan Berhasil Dibuat!!")
    
    connection.commit()
except Error as err:
    print("Error:", err)

finally:
    cursor.close()
    connection.close()
    print("Koneksi ditutup")



