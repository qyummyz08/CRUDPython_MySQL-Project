from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def ambil_satu_data(id, curr):
    statement = "SELECT * FROM pelanggan WHERE id_pelanggan = %s;"
    curr.execute(statement, (id,))

    hasil = curr.fetchone()
    return hasil

def tambah_pelanggan(conn, curr):
    nama_pelanggan = input("masukkan nama pelanggan : ")
    alamat_pelanggan = input("masukkan alamat pelanggan : ")
    nomor_tlp_pelanggan = input("masukkan nomor telepon pelanggan : ")

    data_to_insert = (nama_pelanggan, alamat_pelanggan, nomor_tlp_pelanggan)

    statement = """
    INSERT INTO `pelanggan`(`nama`,`alamat`,`no_telepon`) VALUES(%s, %s, %s);
    """
    curr.execute(statement, data_to_insert)
    conn.commit()
    print("pelanggan baru berhasil di tambahkan")
    print("\n\n")

def lihat_daftar_pelanggan(curr):
    statement = "SELECT * FROM pelanggan;"
    curr.execute(statement)

    hasil_pelanggan = curr.fetchall()
    
    table = Table(title="Daftar Pelanggan")
    table.add_column("ID Pelanggan", style="cyan", justify="right")
    table.add_column("Nama", style="green")
    table.add_column("Alamat", style="magenta")
    table.add_column("No Telepon", style="yellow")
    table.add_column("Tanggal Bergabung", style="blue")

    for pelanggan in hasil_pelanggan:
        table.add_row(
            str(pelanggan[0]),  
            pelanggan[1],       
            pelanggan[2] or "-",
            pelanggan[3] or "-",
            str(pelanggan[4])
        )

    console = Console()
    console.print(table)
    print("\n\n")

def perbarui_data_pelanggan(conn, curr):
    print("Daftar Pelanggan Saat Ini:")

    lihat_daftar_pelanggan(curr)

    id_pelanggan = input("\nMasukkan ID pelanggan yang ingin diupdate: ")

    data_valid = ambil_satu_data(id_pelanggan, curr)

    if data_valid:
        print("Masukkan data baru (tekan Enter jika tidak ingin mengubah):")
        nama_baru = input(f"Nama baru ({data_valid[1]}): ").strip()
        alamat_baru = input(f"Alamat baru ({data_valid[2]}): ").strip()
        no_telepon_baru = input(f"No Telepon baru ({data_valid[3]}): ").strip()

        update_query = "UPDATE pelanggan SET "
        update_fields = []
        params = []

        if nama_baru:
            update_fields.append("nama = %s")
            params.append(nama_baru)
        if alamat_baru:
            update_fields.append("alamat = %s")
            params.append(alamat_baru)
        if no_telepon_baru:
            update_fields.append("no_telepon = %s")
            params.append(no_telepon_baru)

        if not update_fields:
            print("Tidak ada perubahan yang dilakukan.")
            return
    
        update_query += ", ".join(update_fields) + " WHERE id_pelanggan = %s"
        params.append(id_pelanggan)
    
        curr.execute(update_query, params)
        conn.commit()

        print(f"Data pelanggan dengan ID {id_pelanggan} berhasil diupdate.")
        print("\nDaftar Pelanggan Setelah Update:")
        lihat_daftar_pelanggan(curr)
        print("\n\n")
    else:
        print(f"Maaf, sepertinya id yg anda inputkan salah ({id_pelanggan})")

def hapus_pelanggan(conn, curr):
    print("Daftar Pelanggan Saat Ini:")

    lihat_daftar_pelanggan(curr)

    id_pelanggan = input("\nMasukkan ID pelanggan yang ingin diupdate: ")

    data_valid = ambil_satu_data(id_pelanggan, curr)

    if data_valid:
        konfirmasi = input(f"Apakah Anda yakin ingin menghapus pelanggan dengan ID {id_pelanggan}? (y/n): ").lower()
        if konfirmasi != 'y':
            print("Penghapusan dibatalkan.")
            return

        delete_query = "DELETE FROM pelanggan WHERE id_pelanggan = %s"
        curr.execute(delete_query, (id_pelanggan,))
        conn.commit()

        if curr.rowcount > 0:
            print(f"Pelanggan dengan ID {id_pelanggan} berhasil dihapus.")
        else:
            print(f"Tidak ditemukan pelanggan dengan ID {id_pelanggan}.")

        print("\nDaftar Pelanggan Setelah Penghapusan:")
        lihat_daftar_pelanggan(curr)
        print("\n\n")
    else:
        print(f"Maaf, sepertinya id yg anda inputkan salah ({id_pelanggan})")