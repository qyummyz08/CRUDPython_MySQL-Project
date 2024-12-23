from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
import database.pelanggan as pell
import database.jenis_pakaian as jenpak

console = Console()

def ambil_satu_data(id_pesanan, curr):
    statement = "SELECT * FROM pesanan WHERE id_pesanan = %s;"
    curr.execute(statement, (id_pesanan,))

    hasil = curr.fetchone()
    return hasil

def tambah_pesanan(conn, curr):
    pell.lihat_daftar_pelanggan(curr)
    id_pelanggan = input("\nmasukkan id pelanggan yg akan melaundry : ")
    
    pelanggan = pell.ambil_satu_data(id_pelanggan, curr)

    if pelanggan:
        jenis_pakaian = jenpak.lihat_daftar_jenis_pakaian(curr)
        print(f"{pelanggan[1]} akan melakukan laundry")
        data_pakaian_dilaundry = []
        tambah = True
        while tambah:
            id_pakaian = input(f"pilih id pakaian yg akan di laundry : ")
            jumlah = int(input(f"jumlah pakaian : "))

            data_pakaian = jenpak.ambil_satu_data(id_pakaian, curr)

            if not data_pakaian:
                print("maaf sepertinya anda memasukkan id jenis yg salah, harap di coba lagi")
                continue

            subtotal = int(data_pakaian[2]) * jumlah
           
            for data in data_pakaian_dilaundry:
                if data[0] == id_pakaian:
                    data[1] += jumlah
                    data[2] += subtotal
                    break
            else:
                data_pakaian_dilaundry.append([id_pakaian, jumlah, subtotal])

            tanya = input("apakah ingin menambah jenis pakaian yg lain(y/n) ? ")
            if tanya == "n":
                tambah = False
        
        # print(data_pakaian_dilaundry)
        total_subtotal = sum(data[2] for data in data_pakaian_dilaundry)
        statement = "INSERT INTO `pesanan`(`id_pelanggan`, `total_harga`) VALUES(%s, %s);"

        curr.execute(statement, (id_pelanggan, total_subtotal))
        conn.commit()

        curr.execute("SELECT LAST_INSERT_ID();")
        id_pesanan = curr.fetchone()[0]

        query_detail = "INSERT INTO detail_pesanan (id_pesanan, id_jenis, jumlah, sub_total) VALUES (%s, %s, %s, %s)"
        data_detail = []

        for data in data_pakaian_dilaundry:
            data_detail.append((id_pesanan, *data))
        
        curr.executemany(query_detail, data_detail)
        conn.commit()
        
        print(f"Pesanan selesai ditambahkan")
        print("\n\n")
    else:
        print(f"Maaf, sepertinya id yg anda inputkan salah ({id_pelanggan})")

def lihat_daftar_pesanan(curr):
    query = """
    SELECT 
        pesanan.id_pesanan,
        pesanan.tanggal_pesanan,
        pesanan.total_harga,
        pesanan.status,
        pelanggan.nama AS nama_pelanggan
    FROM 
        pesanan
    INNER JOIN 
        pelanggan
    ON 
        pesanan.id_pelanggan = pelanggan.id_pelanggan;
    """

    # Eksekusi query
    curr.execute(query)

    # Ambil hasilnya
    results = curr.fetchall()

    # Tampilkan hasil dalam tabel menggunakan rich
    console = Console()
    table = Table(title="Daftar Pesanan dengan Nama Pelanggan")

    # Tambahkan header tabel
    table.add_column("ID Pesanan", justify="right", style="cyan", no_wrap=True)
    table.add_column("Tanggal Pesanan", justify="center", style="magenta")
    table.add_column("Total Harga", justify="right", style="green")
    table.add_column("Status", justify="center", style="yellow")
    table.add_column("Nama Pelanggan", justify="left", style="blue")

    # Tambahkan data ke tabel
    for row in results:
        table.add_row(str(row[0]), str(row[1]), f"{row[2]:,.2f}", row[3], row[4])

    # Cetak tabel
    console.print(table)
    print("\n\n")


def ubah_status_pesanan(conn, curr):
    print("Daftar status pesanan Saat Ini:")

    lihat_daftar_pesanan(curr)

    id_pesanan = input("\nMasukkan ID pesanan yang ingin diubah statusnya: ")

    data_valid = ambil_satu_data(id_pesanan, curr)

    if data_valid:
        valid_status = ['Diproses', 'Selesai', 'Diambil']
        console.print(f"Status yang tersedia: {', '.join(valid_status)}")
        status_baru = input(f"Masukkan status baru ({data_valid[4]}): ")

        if status_baru not in valid_status:
            console.print("[red]Status tidak valid. Pilih dari status yang tersedia.[/red]")
            return

        # Update status di database
        update_query = "UPDATE pesanan SET status = %s WHERE id_pesanan = %s;"
        curr.execute(update_query, (status_baru, id_pesanan))
        conn.commit()

        console.print(f"[green]Status pesanan dengan ID {id_pesanan} berhasil diubah menjadi '{status_baru}'.[/green]")
        print("\n\n")
    else:
        print(f"Maaf, sepertinya id yg anda inputkan salah ({id_pesanan})")

def batalkan_pesanan(conn, curr):
    print("Daftar status pesanan Saat Ini:")

    lihat_daftar_pesanan(curr)

    id_pesanan = input("\nMasukkan ID pesanan yang ingin dibatalkan : ")

    data_valid = ambil_satu_data(id_pesanan, curr)

    if data_valid:
        confirm = input(f"Apakah Anda yakin ingin membatalkan pesanan dengan ID {id_pesanan}? (y/n): ").lower()
        if confirm != 'y':
            console.print("[yellow]Pembatalan pesanan dibatalkan.[/yellow]")
            return
        
        # Hapus dari tabel detail_pesanan
        delete_detail_query = "DELETE FROM detail_pesanan WHERE id_pesanan = %s;"
        curr.execute(delete_detail_query, (id_pesanan,))

        # Hapus dari tabel pesanan
        delete_pesanan_query = "DELETE FROM pesanan WHERE id_pesanan = %s;"
        curr.execute(delete_pesanan_query, (id_pesanan,))

        # Commit perubahan
        conn.commit()
        console.print(f"[green]Pesanan dengan ID {id_pesanan} dan semua detailnya berhasil dibatalkan.[/green]")
        print("\n\n")
    else:
        print(f"Maaf, sepertinya id yg anda inputkan salah ({id_pesanan})")

def lihat_riwayat_transaksi(curr):
    query = """
    SELECT 
        pesanan.id_pesanan,
        pesanan.tanggal_pesanan,
        pesanan.total_harga,
        pesanan.status,
        pelanggan.nama AS nama_pelanggan
    FROM 
        pesanan
    INNER JOIN 
        pelanggan
    ON 
        pesanan.id_pelanggan = pelanggan.id_pelanggan
    WHERE 
        pesanan.status = 'Diambil';
    """

    # Eksekusi query
    curr.execute(query)

    # Ambil hasilnya
    results = curr.fetchall()

    console = Console()
    table = Table(title="Daftar Pesanan dengan Nama Pelanggan")

    if not results:
        console.print("[yellow]Tidak ada riwayat transaksi dengan status 'Diambil'.[/yellow]")
        return

    # Tambahkan header tabel
    table.add_column("ID Pesanan", justify="right", style="cyan", no_wrap=True)
    table.add_column("Tanggal Pesanan", justify="center", style="magenta")
    table.add_column("Total Harga", justify="right", style="green")
    table.add_column("Status", justify="center", style="yellow")
    table.add_column("Nama Pelanggan", justify="left", style="blue")

    # Tambahkan data ke tabel
    for row in results:
        table.add_row(str(row[0]), str(row[1]), f"{row[2]:,.2f}", row[3], row[4])

    # Cetak tabel
    console.print(table)
    print("\n\n")

def cari_riwayat_berdasarkan_nama_dan_id(curr):
    console = Console()

    lihat_riwayat_transaksi(curr)

    # Meminta input untuk pencarian berdasarkan nama pelanggan atau ID pesanan
    pencarian = input("Masukkan ID Pesanan atau Nama Pelanggan untuk pencarian: ").strip()

    # Cek apakah input berupa angka (ID Pesanan)
    if pencarian.isdigit():
        query = """
        SELECT 
            pesanan.id_pesanan,
            pelanggan.nama AS nama_pelanggan,
            pesanan.tanggal_pesanan,
            pesanan.total_harga
        FROM 
            pesanan
        INNER JOIN 
            pelanggan
        ON 
            pesanan.id_pelanggan = pelanggan.id_pelanggan
        WHERE 
            pesanan.id_pesanan = %s
            AND pesanan.status = 'Diambil';
        """
        parameter = (int(pencarian),)
    else:
        query = """
        SELECT 
            pesanan.id_pesanan,
            pelanggan.nama AS nama_pelanggan,
            pesanan.tanggal_pesanan,
            pesanan.total_harga
        FROM 
            pesanan
        INNER JOIN 
            pelanggan
        ON 
            pesanan.id_pelanggan = pelanggan.id_pelanggan
        WHERE 
            pelanggan.nama LIKE %s
            AND pesanan.status = 'Diambil';
        """
        parameter = (f"%{pencarian}%",)

    
    curr.execute(query, parameter)
    results = curr.fetchall()

    # Jika tidak ada data ditemukan, tampilkan pesan
    if not results:
        console.print("[yellow]Tidak ada riwayat transaksi yang ditemukan.[/yellow]")
        return
    
    # Buat tabel untuk menampilkan data
    table = Table(title="Riwayat Transaksi Berdasarkan Nama Pelanggan atau ID Pesanan")
    table.add_column("ID Pesanan", justify="right", style="cyan")
    table.add_column("Nama Pelanggan", justify="left", style="blue")
    table.add_column("Tanggal Pesanan", justify="center", style="magenta")
    table.add_column("Total Harga", justify="right", style="green")
    # Tambahkan data ke tabel
    for row in results:
        table.add_row(str(row[0]), row[1], str(row[2]), f"{row[3]:,.2f}")
    # Cetak tabel
    console.print(table)
    print("\n\n")

def cetak_struk_transaksi(curr):
    console = Console()

    lihat_riwayat_transaksi(curr)

    # Meminta input ID Pesanan untuk mencetak struk
    id_pesanan = input("Masukkan ID Pesanan untuk mencetak struk: ").strip()

    # Query untuk mendapatkan detail transaksi dan pakaian
    query = """
    SELECT 
        pesanan.id_pesanan,
        pelanggan.nama AS nama_pelanggan,
        pesanan.tanggal_pesanan,
        pesanan.total_harga,
        jenis_pakaian.jenis_pakaian,
        detail_pesanan.jumlah,
        detail_pesanan.sub_total
    FROM 
        pesanan
    INNER JOIN 
        pelanggan ON pesanan.id_pelanggan = pelanggan.id_pelanggan
    INNER JOIN 
        detail_pesanan ON pesanan.id_pesanan = detail_pesanan.id_pesanan
    INNER JOIN 
        jenis_pakaian ON detail_pesanan.id_jenis = jenis_pakaian.id_jenis
    WHERE 
        pesanan.id_pesanan = %s
        AND pesanan.status = 'Diambil';
    """
    
    curr.execute(query, (id_pesanan,))
    results = curr.fetchall()

    # Jika tidak ada data, tampilkan pesan
    if not results:
        console.print(f"[yellow]Tidak ada data untuk ID Pesanan {id_pesanan}.[/yellow]")
        return
    # Menampilkan header struk
    header = Panel(
        Align.center(
            Text(f"Struk Transaksi\nID Pesanan: {id_pesanan}", justify="center", style="bold cyan"),
            vertical="middle"
        ),
        style="cyan",
        border_style="bold white",
    )
    console.print(header)

    # Membuat tabel untuk detail pesanan
    table = Table(title="Detail Pesanan")
    table.add_column("Jenis Pakaian", justify="left", style="cyan")
    table.add_column("Jumlah", justify="right", style="magenta")
    table.add_column("Subtotal", justify="right", style="green")

    total_harga = 0

    # Tambahkan detail pesanan ke tabel
    for row in results:
        table.add_row(row[4], str(row[5]), f"{row[6]:,.2f}")
        total_harga += row[6]  # Mengakumulasi subtotal

    # Menampilkan informasi pelanggan dan total harga
    pelanggan_info = Panel(
        Align.left(
            f"Nama Pelanggan: {results[0][1]}\nTanggal Pesanan: {results[0][2]}\nTotal Harga: {total_harga:,.2f}",
            vertical="middle"
        ),
        style="magenta",
        border_style="bold white",
    )
    console.print(pelanggan_info)

    # Menampilkan tabel
    console.print(table)

    # Pesan terima kasih
    footer = Panel(
        Align.center(
            Text("Terima kasih telah menggunakan layanan kami!", justify="center", style="bold green"),
            vertical="middle"
        ),
        style="green",
        border_style="bold white",
    )
    console.print(footer)

# Contoh penggunaan (gunakan koneksi database Anda)
# conn = ...
# curr = conn.cursor()
# cetak_struk_transaksi(curr))