import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
import mysql.connector
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit

class DialogInputPengunjung(QDialog):
    def __init__(self, parent=None):
        super(DialogInputPengunjung, self).__init__(parent)
        self.setWindowTitle('Input Detail Pengunjung')

        layout = QVBoxLayout()

        self.label_nama = QLabel('Nama:')
        self.edit_nama = QLineEdit()

        self.label_alamat = QLabel('Alamat:')
        self.edit_alamat = QLineEdit()

        self.label_telepon = QLabel('Nomor Telepon:')
        self.edit_telepon = QLineEdit()

        self.label_tipe_kamar = QLabel('Tipe Kamar:')
        self.combo_tipe_kamar = QComboBox()
        self.combo_tipe_kamar.addItems(["Standar", "Superior", "Deluxe"])

        self.label_harga = QLabel('Harga:')
        self.edit_harga = QLineEdit()

        self.label_check_in = QLabel('Check-In:')
        self.date_edit_check_in = QDateEdit()

        self.label_check_out = QLabel('Check-Out:')
        self.date_edit_check_out = QDateEdit()

        self.btn_ok = QPushButton('OK')
        self.btn_cancel = QPushButton('Batal')

        layout.addWidget(self.label_nama)
        layout.addWidget(self.edit_nama)
        layout.addWidget(self.label_alamat)
        layout.addWidget(self.edit_alamat)
        layout.addWidget(self.label_telepon)
        layout.addWidget(self.edit_telepon)
        layout.addWidget(self.label_tipe_kamar)
        layout.addWidget(self.combo_tipe_kamar)
        layout.addWidget(self.label_harga)
        layout.addWidget(self.edit_harga)
        layout.addWidget(self.label_check_in)
        layout.addWidget(self.date_edit_check_in)
        layout.addWidget(self.label_check_out)
        layout.addWidget(self.date_edit_check_out)
        layout.addWidget(self.btn_ok)
        layout.addWidget(self.btn_cancel)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

        self.setLayout(layout)

    def get_input_data(self):
        nama = self.edit_nama.text()
        alamat = self.edit_alamat.text()
        telepon = self.edit_telepon.text()
        tipe_kamar = self.combo_tipe_kamar.currentText()
        harga = self.edit_harga.text()
        check_in = self.date_edit_check_in.date().toString('yyyy-MM-dd')
        check_out = self.date_edit_check_out.date().toString('yyyy-MM-dd')

        return nama, alamat, telepon, tipe_kamar, harga, check_in, check_out

class ResepsionisHotel(QWidget):
    def __init__(self):
        super().__init__()
        self.inisialisasi_db()
        self.inisialisasi_ui()

    def inisialisasi_db(self):
        try:
            # Ganti 'password' dengan kata sandi MySQL Anda
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",  # Ganti dengan kata sandi MySQL Anda
                database="resepsionis_hotel"
            )

            if self.db.is_connected():
                print("Berhasil terhubung ke database")
                self.buat_tabel()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def buat_tabel(self):
        cursor = self.db.cursor()
        try:
            # Hapus tabel 'pengunjung' jika sudah ada
            cursor.execute("DROP TABLE IF EXISTS pengunjung")

            # Buat tabel 'pengunjung'
            cursor.execute("""
                CREATE TABLE pengunjung (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nama VARCHAR(255) NOT NULL,
                    alamat VARCHAR(255) NOT NULL,
                    telepon VARCHAR(15) NOT NULL,
                    tipe_kamar VARCHAR(50) NOT NULL,
                    harga INT NOT NULL,
                    check_in DATE NOT NULL,
                    check_out DATE NOT NULL
                )
            """)
            print("Table 'pengunjung' created.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db.rollback()
        finally:
            cursor.close()

    def inisialisasi_ui(self):
        self.setWindowTitle('Resepsionis Hotel')
        self.setGeometry(200, 200, 600, 400)

        self.label = QLabel('RESEPSIONIS HOTEL', self)
        self.label.setStyleSheet('font-size: 18px; font-weight: bold;')
        self.label.setAlignment(Qt.AlignCenter)

        self.tabel = QTableWidget(self)
        self.tabel.setColumnCount(8)
        self.tabel.setHorizontalHeaderLabels(["ID", "Nama", "Alamat", "Telepon", "Tipe Kamar", "Harga", "Check-In", "Check-Out"])

        self.tombol1 = QPushButton('Masukkan Detail Pengunjung', self)
        self.tombol2 = QPushButton('Lihat Data Pengunjung', self)
        self.tombol3 = QPushButton('Check Out', self)
        self.tombol4 = QPushButton('Keluar Aplikasi', self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.tabel)
        vbox.addWidget(self.tombol1)
        vbox.addWidget(self.tombol2)
        vbox.addWidget(self.tombol3)
        vbox.addWidget(self.tombol4)

        self.setLayout(vbox)

        self.tombol1.clicked.connect(self.masukkan_detail_pengunjung)
        self.tombol2.clicked.connect(self.lihat_data_pengunjung)
        self.tombol3.clicked.connect(self.check_out)
        self.tombol4.clicked.connect(self.keluar_program)

        self.show()

    def masukkan_detail_pengunjung(self):
        dialog_input = DialogInputPengunjung(self)
        result = dialog_input.exec_()

        if result == QDialog.Accepted:
            nama, alamat, telepon, tipe_kamar, harga, check_in, check_out = dialog_input.get_input_data()

            cursor = self.db.cursor()
            try:
                # Masukkan detail pengunjung ke dalam tabel 'pengunjung'
                query = "INSERT INTO pengunjung (nama, alamat, telepon, tipe_kamar, harga, check_in, check_out) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (nama, alamat, telepon, tipe_kamar, harga, check_in, check_out)
                cursor.execute(query, values)
                self.db.commit()

                QMessageBox.information(self, 'Sukses', 'Detail pengunjung berhasil ditambahkan.')
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                self.db.rollback()
                QMessageBox.critical(self, 'Error', 'Gagal menambahkan detail pengunjung.')
            finally:
                cursor.close()

    def lihat_data_pengunjung(self):
        cursor = self.db.cursor(dictionary=True)
        self.tabel.setRowCount(0)

        try:
            # Ambil semua detail pengunjung dari tabel 'pengunjung'
            query = "SELECT * FROM pengunjung"
            cursor.execute(query)
            pengunjung = cursor.fetchall()

            if pengunjung:
                for pengunjung_item in pengunjung:
                    row_position = self.tabel.rowCount()
                    self.tabel.insertRow(row_position)
                    self.tabel.setItem(row_position, 0, QTableWidgetItem(str(pengunjung_item['id'])))
                    self.tabel.setItem(row_position, 1, QTableWidgetItem(pengunjung_item['nama']))
                    self.tabel.setItem(row_position, 2, QTableWidgetItem(pengunjung_item['alamat']))
                    self.tabel.setItem(row_position, 3, QTableWidgetItem(pengunjung_item['telepon']))
                    self.tabel.setItem(row_position, 4, QTableWidgetItem(pengunjung_item['tipe_kamar']))
                    self.tabel.setItem(row_position, 5, QTableWidgetItem(str(pengunjung_item['harga'])))
                    self.tabel.setItem(row_position, 6, QTableWidgetItem(str(pengunjung_item['check_in'])))
                    self.tabel.setItem(row_position, 7, QTableWidgetItem(str(pengunjung_item['check_out'])))
            else:
                print("Tidak ditemukan detail pengunjung.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def check_out(self):
        id_pengunjung, ok_pressed_id = self.get_text_input("Masukkan ID Pengunjung untuk Check Out:")
        if ok_pressed_id:
            cursor = self.db.cursor()
            try:
                # Hapus pengunjung berdasarkan ID
                query = "DELETE FROM pengunjung WHERE id = %s"
                cursor.execute(query, (id_pengunjung,))
                self.db.commit()

                QMessageBox.information(self, 'Sukses', 'Check Out berhasil.')
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                self.db.rollback()
                QMessageBox.critical(self, 'Error', 'Gagal melakukan Check Out.')
            finally:
                cursor.close()

    def pilih_tipe_kamar(self):
        tipe_kamar_names = ["Standar", "Superior", "Deluxe"]
        tipe_kamar, ok_pressed = QInputDialog.getItem(self, 'Pilih Tipe Kamar', 'Pilih tipe kamar:', tipe_kamar_names, 0)

        if ok_pressed:
            if tipe_kamar == "Standar":
                return tipe_kamar, 180000
            elif tipe_kamar == "Superior":
                return tipe_kamar, 250000
            elif tipe_kamar == "Deluxe":
                return tipe_kamar, 350000
        else:
            return None, None

    def get_date_input(self, prompt):
        date, ok_pressed = QInputDialog.getText(self, 'Dialog Input', prompt)
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
            return date, ok_pressed
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Format tanggal tidak valid.')
            return None, False

    def get_text_input(self, prompt):
        text, ok_pressed = QInputDialog.getText(self, 'Dialog Input', prompt)
        return text, ok_pressed

    def keluar_program(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ResepsionisHotel()
    sys.exit(app.exec_())
