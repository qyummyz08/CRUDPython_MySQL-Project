from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def ambil_satu_data(id, curr):
    statement = "SELECT * FROM jenis_pakaian WHERE id_jenis = %s;"
    curr.execute(statement, (id,))

    hasil = curr.fetchone()
    return hasil

def tambah_jenis_pakaian(conn, curr):
    jenis_pakaian = input("masukkan nama jenis_pakaian : ")
    harga = input("masukkan harga jenis_pakaian : ")

    data_to_insert = (jenis_pakaian, harga)

    statement = """
    INSERT INTO `jenis_pakaian`(`jenis_pakaian`,`harga`) VALUES(%s, %s);
    """
    curr.execute(statement, data_to_insert)
    conn.commit()
    print("jenis_pakaian baru berhasil di tambahkan")
    print("\n\n")

def lihat_daftar_jenis_pakaian(curr):
    statement = "SELECT * FROM jenis_pakaian;"
    curr.execute(statement)

    hasil_jenis_pakaian = curr.fetchall()
    
    table = Table(title="Daftar jenis_pakaian")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Jenis Pakaian", style="green")
    table.add_column("Harga", style="magenta")

    for jenis_pakaian in hasil_jenis_pakaian:
        table.add_row(
            str(jenis_pakaian[0]),  
            jenis_pakaian[1],       
            str(jenis_pakaian[2])
        )

    console = Console()
    console.print(table)
    print("\n\n")

def perbarui_data_jenis_pakaian(conn, curr):
    print("Daftar jenis_pakaian Saat Ini:")

    lihat_daftar_jenis_pakaian(curr)

    id_jenis = input("\nMasukkan ID jenis_pakaian yang ingin diupdate: ")

    data_valid = ambil_satu_data(id_jenis, curr)

    if data_valid:
        print("Masukkan data baru (tekan Enter jika tidak ingin mengubah):")
        jenis_pakaian_baru = input(f"Jenis pakaian baru ({data_valid[1]}): ").strip()
        harga_baru = input(f"Harga baru ({data_valid[2]}): ").strip()

        update_query = "UPDATE jenis_pakaian SET "
        update_fields = []
        params = []

        if jenis_pakaian_baru:
            update_fields.append("jenis_pakaian = %s")
            params.append(jenis_pakaian_baru)
        if harga_baru:
            update_fields.append("harga = %s")
            params.append(harga_baru)
        

        if not update_fields:
            print("Tidak ada perubahan yang dilakukan.")
            return
    
        update_query += ", ".join(update_fields) + " WHERE id_jenis = %s"
        params.append(id_jenis)
    
        curr.execute(update_query, params)
        conn.commit()

        print(f"Data jenis_pakaian dengan ID {id_jenis} berhasil diupdate.")
        print("\nDaftar jenis_pakaian Setelah Update:")
        lihat_daftar_jenis_pakaian(curr)
        print("\n\n")
    else:
        print(f"Maaf, sepertinya id yg anda inputkan salah ({id_jenis})")

def hapus_jenis_pakaian(conn, curr):
    print("Daftar jenis_pakaian Saat Ini:")

    lihat_daftar_jenis_pakaian(curr)

    id_jenis = input("\nMasukkan ID jenis_pakaian yang ingin diupdate: ")

    data_valid = ambil_satu_data(id_jenis, curr)

    if data_valid:
        konfirmasi = input(f"Apakah Anda yakin ingin menghapus jenis_pakaian dengan ID {id_jenis}? (y/n): ").lower()
        if konfirmasi != 'y':
            print("Penghapusan dibatalkan.")
            return

        delete_query = "DELETE FROM jenis_pakaian WHERE id_jenis = %s"
        curr.execute(delete_query, (id_jenis,))
        conn.commit()

        if curr.rowcount > 0:
            print(f"jenis_pakaian dengan ID {id_jenis} berhasil dihapus.")
        else:
            print(f"Tidak ditemukan jenis_pakaian dengan ID {id_jenis}.")

        print("\nDaftar jenis_pakaian Setelah Penghapusan:")
        lihat_daftar_jenis_pakaian(curr)
        print("\n\n")
    else:
        print(f"Maaf, sepertinya id yg anda inputkan salah ({id_jenis})")