import mysql.connector
from mysql.connector import Error
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import database.pelanggan as pell
import database.jenis_pakaian as jenpak
import database.pesanan as pess
import pyfiglet

def start_menu(): 
    try:
        # Buat koneksi
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="",  
            database="by_laundry" 
        )

        curr = connection.cursor()
        console = Console()

        text = pyfiglet.figlet_format("\nWELCOME TO  BYLO\n", font="chunky")
        subtitle = "[cyan]By Londry[/cyan]"
        menu = generate_menu(["Data Pelanggan", 
                              "Data Pakaian",
                              "Pesanan Laundry", 
                              "Riwayat Transaksi", 
                              "Keluar"])

        for line in text.split("\n"):
            console.print(Align.center(f"[bold yellow]{line}[/bold yellow]", style="bold yellow on black"))
        console.print(Align.center(subtitle))
        while True:
            console.print(Panel.fit(menu,
                                title="Mainmenu", title_align="left", border_style="bright_blue", padding=(1, 4, 0, 4)))
            
            user_input = int(input("> masukkan pilihan : "))
            print("")

            match user_input:
                case 1:
                    data_pelanggan(connection, curr, console)
                case 2:
                    data_pakaian(connection, curr, console)
                case 3:
                    pesanan_laundry(connection, curr, console)
                case 4:
                    riwayat_transaksi(connection, curr, console)
                case 5:
                    exit()
                case _:
                    print("pilihan yang anda masukkan salah")

    except Error as err:
        print("Error : ", err)

def generate_menu(menu_list):
    menu = ""
    for index, item in enumerate(menu_list, start=1):
        menu += f"[[bold cyan]{index}[/bold cyan]] [magenta]{item}[/magenta]\n"
    return menu    

def data_pelanggan(conn, curr, console):
    menu = generate_menu(["Tambah Pelanggan", "Lihat Daftar Pelanggan", "Ubah Data Pelanggan", "Hapus Data Pelanggan", "Kembali", "Keluar"])
    ulang = True
    while ulang:
        console.print(Panel.fit(menu,
                                title="Data Pelanggan", title_align="left", border_style="bright_blue", padding=(1, 4, 0, 4)))
        user_input = int(input("> masukkan pilihan : "))
        print("")

        match user_input:
            case 1:
                pell.tambah_pelanggan(conn, curr)
            case 2:
                pell.lihat_daftar_pelanggan(curr)
            case 3:
                pell.perbarui_data_pelanggan(conn,curr)
            case 4:
                pell.hapus_pelanggan(conn,curr)
            case 5:
                ulang = False
            case 6:
                exit()
            case _:
                print("pilihan yang anda masukkan salah")

def data_pakaian(conn, curr, console):
    menu = generate_menu(["Tambah Jenis Pakaian", "Lihat Daftar Pakaian", "Ubah Data Jenis Pakaian", "Hapus Jenis Pakaian", "Kembali", "Keluar"])
    ulang = True
    while ulang:
        console.print(Panel.fit(menu,
                                title="Data Pakaian", title_align="left", border_style="bright_blue", padding=(1, 4, 0, 4)))
        user_input = int(input("> masukkan pilihan : "))
        print("")

        match user_input:
            case 1:
                jenpak.tambah_jenis_pakaian(conn, curr)
            case 2:
                jenpak.lihat_daftar_jenis_pakaian(curr)
            case 3:
                jenpak.perbarui_data_jenis_pakaian(conn,curr)
            case 4:
                jenpak.hapus_jenis_pakaian(conn,curr)
            case 5:
                ulang = False
            case 6:
                exit()
            case _:
                print("pilihan yang anda masukkan salah")

def pesanan_laundry(conn, curr, console):
    menu = generate_menu(["Buat Pesanan Baru", "Lihat Daftar Pesanan", "Ubah Status Pesanan", "Hapus Pesanan", "Kembali", "Keluar"])
    ulang = True
    while ulang:
        console.print(Panel.fit(menu,
                                title="Pesanan Laundry", title_align="left", border_style="bright_blue", padding=(1, 4, 0, 4)))
        user_input = int(input("> masukkan pilihan : "))
        print("")

        match user_input:
            case 1:
                pess.tambah_pesanan(conn, curr)
            case 2:
                pess.lihat_daftar_pesanan(curr)
            case 3:
                pess.ubah_status_pesanan(conn, curr)
            case 4:
                pess.batalkan_pesanan(conn, curr)
            case 5:
                ulang = False
            case 6:
                exit()
            case _:
                print("pilihan yang anda masukkan salah")

def riwayat_transaksi(conn, curr, console):
    menu = generate_menu(["Lihat Riwayat Transaksi", "Cari Transaksi Berdasarkan ID/ Nama Pelanggan", "Cetak Struk Transaksi", "Kembali", "Keluar"])
    ulang = True
    while ulang:
        console.print(Panel.fit(menu,
                                title="Riwayat Transaksi", title_align="left", border_style="bright_blue", padding=(1, 4, 0, 4)))
        user_input = int(input("> masukkan pilihan : "))
        print("")

        match user_input:
            case 1:
                pess.lihat_riwayat_transaksi(curr)
            case 2:
                pess.cari_riwayat_berdasarkan_nama_dan_id(curr)
            case 3:
                pess.cetak_struk_transaksi(curr)
            case 4:
                ulang = False
            case 5:
                exit()
            case _:
                print("pilihan yang anda masukkan salah")

if __name__ == "__main__":
    start_menu()