import math
import os
import socket
import random
import re
import sqlite3
import string
import sys
import time
import qr_extractor as reader
from datetime import datetime
from io import BytesIO
from requests import post
import cv2
import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageQt
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon, QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel, QApplication, QTableWidgetItem, QFileDialog
from playsound import playsound
from func_timeout import func_timeout, FunctionTimedOut
from Designs import design_1
from Designs import design_2
from Designs import design_3
from Designs import design_5
from Designs import design_6
from Designs import design_7

token = "1694103677:AAGuFWePbKghZGsu3_wJkQJeAUSFQb-TAxI"
url = f"https://api.telegram.org/bot{token}/sendMessage"
encoder_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']


def encoder(n):
    s = ""
    for i in str(n):
        s += encoder_characters[int(i)]
    return s


def decoder(a):
    s = ""
    for i in a:
        s += str(encoder_characters.index(i))
    return int(s)


def removeColumns(db_cur, t, columns_to_junk):
    sql = "PRAGMA table_info(" + t + ")"
    record = db_cur.execute(sql).fetchall()
    cols_w_types = "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
    cols = ""
    for r in record:
        if r[1] not in columns_to_junk:
            if r[5] == 0:
                cols_w_types += r[1] + " " + r[2] + ","
            cols += r[1] + ","
    if cols_w_types[-1] == ",":
        cols_w_types = cols_w_types[:-1]
    else:
        pass

    if cols[-1] == ",":
        cols = cols[:-1]
    else:
        pass
    sql = "CREATE TABLE xfer " + cols_w_types + ")"
    db_cur.execute(sql)
    sql = "INSERT INTO xfer SELECT " + cols + " FROM " + t
    db_cur.execute(sql)
    sql = "DROP TABLE " + t
    db_cur.execute(sql)
    sql = "CREATE TABLE " + t + cols_w_types + ")"
    db_cur.execute(sql)
    sql = "INSERT INTO " + t + " SELECT " + cols + " FROM xfer"
    db_cur.execute(sql)
    sql = "DROP TABLE xfer"
    db_cur.execute(sql)


class Main_window(QMainWindow, design_1.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conn = sqlite3.connect(database, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.check_database()
        self.lineEdit.textChanged.connect(self.search)
        self.tableWidget_2.itemSelectionChanged.connect(self.class_changed_2)
        self.comboBox.currentTextChanged.connect(
            lambda x: self.class_changed(self.comboBox.currentText()))
        self.tableWidget_2.doubleClicked.connect(
            lambda x: self.open_window_3(int(self.tableWidget_2.item(self.tableWidget_2.currentRow(), 0).text())))
        self.tableWidget.doubleClicked.connect(
            lambda x: self.open_window_2(
                int(self.tableWidget.item(self.tableWidget.currentRow(), 0).text()))
        )
        self.tableWidget_5.doubleClicked.connect(
            lambda x: self.open_window_5(int(self.tableWidget_5.item(self.tableWidget_5.currentRow(), 0).text(
            )), self.tableWidget_5.horizontalHeaderItem(self.tableWidget_5.currentColumn()).text())
        )
        self.pushButton_2.clicked.connect(lambda x: self.open_window_2(0))
        self.pushButton_3.clicked.connect(lambda x: self.open_window_3(0))
        self.pushButton_5.clicked.connect(self.export_cart)
        self.pushButton_6.clicked.connect(self.del_with_button)
        self.pushButton_7.clicked.connect(self.edit_using_button)
        self.pushButton_8.clicked.connect(self.open_window_5_button)
        self.pushButton_9.clicked.connect(self.delete_date)
        self.pushButton_10.clicked.connect(self.open_window_6)
        self.checkBox.clicked.connect(self.hide_img_row)

        self.lineEdit_5.textChanged.connect(self.about_data_changed)
        self.lineEdit_6.textChanged.connect(self.about_data_changed)
        self.lineEdit_8.textChanged.connect(self.about_data_changed)
        self.format_tables()
        self.check_today()
        self.update_window()

        self.tableWidget.clicked.connect(
            lambda: self.tableWidget_2.clearSelection())
        self.tableWidget_2.clicked.connect(
            lambda: self.tableWidget.clearSelection())
        self.tableWidget_3.clicked.connect(lambda x: self.clear_sel(
            [self.tableWidget_4, self.tableWidget_5]))
        self.tableWidget_4.clicked.connect(lambda x: self.clear_sel(
            [self.tableWidget_3, self.tableWidget_5]))
        self.tableWidget_5.clicked.connect(lambda x: self.clear_sel(
            [self.tableWidget_4, self.tableWidget_3]))
        self.tableWidget_3.itemSelectionChanged.connect(lambda: self.write_attendance(
            self.tableWidget_3.item(self.tableWidget_3.currentRow(), 0)))

    def check_database(self):
        self.cur.execute(
            "create table if not exists classes(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, classcom TEXT)")
        self.cur.execute(
            "create table if not exists pupils(id INTEGER PRIMARY KEY AUTOINCREMENT, photo BLOB, class TEXT, guruh TEXT, gender TEXT, name TEXT, surname TEXT, father TEXT, mother TEXT, birthday TEXT, location TEXT, phone TEXT, passport TEXT, telegram_id TEXT, qrcode TEXT)")
        self.cur.execute(
            "create table if not exists school(province TEXT, region TEXT, school TEXT)")
        self.conn.commit()

    def check_today(self):
        today = encoder(datetime.today().toordinal())
        try:
            self.cur.execute(
                f"""ALTER TABLE pupils ADD COLUMN "{today}" TEXT""")
            self.conn.commit()
        except:
            pass

    def clear_sel(self, a):
        for i in a:
            i.clearSelection()

    def edit_using_button(self):
        if len(self.tableWidget.selectedItems()) != 0:
            self.open_window_2(int(self.tableWidget.item(
                self.tableWidget.currentRow(), 0).text()))
        elif len(self.tableWidget_2.selectedItems()) != 0:
            self.open_window_3(int(self.tableWidget_2.item(
                self.tableWidget_2.currentRow(), 0).text()))

    def export_cart(self):
        try:
            if len(self.tableWidget.selectedItems()) != 0:
                id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()

                filename = QFileDialog.getSaveFileName(
                    self, 'Qr kartani saqlash', '', "JPG (*.jpg)")[0]
                if filename != "":
                    self.cur.execute("select * from pupils where id=?", [id])
                    data = self.cur.fetchone()
                    img = ImageQt.fromqpixmap(QPixmap(":/Icons/Icons/cart.jpg"))
                    # user photo
                    if data[1] != "":
                        user = Image.open(BytesIO(data[1]))
                        new = user.resize((150, 200))
                        img.paste(new, (30, 25))
                    # qrcode
                    qr_img = qrcode.make(data[14])
                    qr_img = qr_img.resize((240, 240))
                    img.paste(qr_img, (160, 280))
                    # strings
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype(resource_path("./font.ttf"), 44)
                    # surname
                    w, h = draw.textsize(data[6], font)
                    draw.text(((560 - w) / 2, (648 - h)), data[6], font=font)
                    # name
                    w, h = draw.textsize(data[5], font)
                    draw.text(((560 - w) / 2, 678), data[5], font=font)
                    font = ImageFont.truetype(resource_path("./font.ttf"), 40)
                    # region
                    w, h = draw.textsize(self.lineEdit_5.text(), font)
                    draw.text(((380 - w) / 2 + 180, 25),
                              self.lineEdit_5.text(), font=font)
                    # school
                    w, h = draw.textsize(self.lineEdit_6.text(), font)
                    draw.text(((380 - w) / 2 + 180, 95),
                              self.lineEdit_6.text(), font=font)
                    # class
                    w, h = draw.textsize(data[2], font)
                    draw.text(((380 - w) / 2 + 180, 170), data[2], font=font)
                    img.save(filename)
        except Exception as er:
            with open("error.txt", "w+") as f:
                f.write(str(er))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Up and self.tableWidget_2.hasFocus():
            if self.tableWidget_2.currentRow() != 0:
                self.tableWidget_2.selectRow(
                    self.tableWidget_2.currentRow() - 1)
        if e.key() == Qt.Key_Down and self.tableWidget_2.hasFocus():
            if self.tableWidget_2.currentRow() != self.tableWidget_2.rowCount():
                self.tableWidget_2.selectRow(
                    self.tableWidget_2.currentRow() + 1)
        if e.key() == Qt.Key_Delete and self.tableWidget_2.hasFocus():
            self.delete_class()
        if e.key() == Qt.Key_Delete and self.tableWidget.hasFocus():
            self.delete_pupil()
        if e.key() == Qt.Key_Delete and self.tableWidget_4.hasFocus():
            self.delete_date()

    def about_data_changed(self):
        self.cur.execute("delete from school")
        province = self.lineEdit_8.text()
        region = self.lineEdit_5.text()
        school = self.lineEdit_6.text()
        self.cur.execute("insert into school(province, region, school) values(?, ?, ?)", [
            province, region, school])
        self.conn.commit()

    def delete_pupil(self):
        if self.tableWidget.rowCount() != 0:
            msg = QMessageBox()
            msg.setWindowTitle("O'quvchini o'chirish")
            msg.setText("Rostdan xam bu o'quvchini o'chirmoqchimisiz?")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            msg.buttonClicked.connect(self.delete_pupil_ok)
            msg.setDefaultButton(QMessageBox.Cancel)
            x = msg.exec_()

    def del_with_button(self):
        if len(self.tableWidget.selectedItems()) != 0:
            self.delete_pupil()
        elif len(self.tableWidget_2.selectedItems()) != 0:
            self.delete_class()

    def delete_pupil_ok(self, i):
        if i.text() == "OK":
            id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            self.cur.execute("delete from pupils where id=?", [id])
            self.conn.commit()
            self.update_window()

    def delete_class(self):
        if self.tableWidget_2.rowCount() != 0:
            msg = QMessageBox()
            msg.setWindowTitle("Sinfni o'chirish")
            msg.setText(
                "Rostdan xam bu sinfni o'chirmoqchimisiz!?\nSinf bilan uni barcha o'quvchilari xam o'chadi")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            msg.buttonClicked.connect(self.delete_class_ok)
            msg.setDefaultButton(QMessageBox.Cancel)
            x = msg.exec_()

    def delete_class_ok(self, i):
        if i.text() == "OK":
            class_name = self.tableWidget_2.item(
                self.tableWidget_2.currentRow(), 1).text()
            self.cur.execute("delete from pupils where class=?", [class_name])
            self.cur.execute("delete from classes where name=?", [class_name])
            self.conn.commit()
            self.update_window()

    def delete_date(self):
        if len(self.tableWidget_4.selectedItems()) != 0:
            msg = QMessageBox()
            msg.setWindowTitle("Sanani o'chirish")
            msg.setText("Rostdan xam bu sanani o'chirmoqchimisiz!?")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            msg.buttonClicked.connect(self.delete_date_ok)
            msg.setDefaultButton(QMessageBox.Cancel)
            x = msg.exec_()

    def delete_date_ok(self, i):
        if i.text() == "OK":
            date = self.tableWidget_4.item(
                self.tableWidget_4.currentRow(), 0).text()
            date = date.split(", ")[1].split("/")
            date = encoder(datetime(int(date[2]), int(
                date[1]), int(date[0])).toordinal())
            removeColumns(self.cur, "pupils", date)
            self.conn.commit()
            self.update_window()

    def search(self):
        if len(self.lineEdit.text()) > 2:
            class_type = self.comboBox.currentText()
            key1 = '"%' + self.lineEdit.text() + '%"'
            key2 = '"%' + self.lineEdit.text().capitalize() + '%"'
            if class_type != "Hammasi":
                self.cur.execute(
                    f"select * from pupils where (name like {key1} or name like {key2}) and class='{class_type}' order by surname")
            else:
                self.cur.execute(
                    f"select * from pupils where name like {key1} or name like {key2} order by surname")
            self.write_pupils(self.cur.fetchall())
        else:
            if self.comboBox.currentText() == "Hammasi":
                self.cur.execute("select * from pupils order by surname")
                self.write_pupils(self.cur.fetchall())
            else:
                self.cur.execute(
                    f"select * from pupils where class='{self.comboBox.currentText()}' order by surname")
                self.write_pupils(self.cur.fetchall())

    def format_tables(self):
        # 1
        self.tableWidget_2.setColumnHidden(0, True)
        self.tableWidget_2.setColumnWidth(1, 160)
        self.tableWidget_2.setColumnWidth(2, 250)
        self.tableWidget_2.setColumnWidth(3, 150)
        self.tableWidget_2.setColumnWidth(4, 120)
        self.tableWidget_2.setColumnWidth(5, 120)
        # 2
        self.tableWidget.setColumnHidden(0, True)
        self.tableWidget.setColumnWidth(1, 60)
        self.tableWidget.setColumnWidth(2, 50)
        self.tableWidget.setColumnWidth(3, 118)
        self.tableWidget.setColumnWidth(4, 118)
        self.tableWidget.setColumnWidth(5, 118)
        self.tableWidget.setColumnWidth(6, 120)
        self.tableWidget.setColumnWidth(7, 60)
        self.tableWidget.setColumnWidth(8, 110)
        self.tableWidget.setColumnWidth(9, 130)
        self.tableWidget.setColumnWidth(10, 116)
        self.tableWidget.setColumnWidth(11, 100)
        self.tableWidget.setColumnWidth(12, 150)
        # 3
        self.tableWidget_3.setColumnWidth(0, 150)
        # 4
        self.tableWidget_4.setColumnWidth(0, 210)
        self.tableWidget_4.setColumnWidth(1, 180)
        self.tableWidget_4.setColumnWidth(2, 180)
        self.tableWidget_4.setColumnWidth(3, 180)

    def class_changed(self, name):
        if name == "Hammasi":
            self.cur.execute("select * from pupils order by name")
            a = self.cur.fetchall()
            self.write_pupils(a)
        else:
            self.cur.execute(
                "select * from pupils where class=? order by name", [name])
            a = self.cur.fetchall()
            self.write_pupils(a)

    def class_changed_2(self):
        try:
            name = self.tableWidget_2.item(
                self.tableWidget_2.currentRow(), 1).text()
            self.comboBox.setCurrentText(name)
        except:
            pass

    def open_window_2(self, id):
        if self.tableWidget_2.rowCount() != 0:
            self.setDisabled(True)
            self.w2 = Window_2(id)
            self.w2.show()

    def open_window_3(self, id):
        self.setDisabled(True)
        self.w3 = Window_3(id)
        self.w3.show()

    def open_window_5_button(self):
        if len(self.tableWidget_5.selectedItems()) != 0:
            self.open_window_5(int(self.tableWidget_5.item(self.tableWidget_5.currentRow(), 0).text(
            )), self.tableWidget_5.horizontalHeaderItem(self.tableWidget_5.currentColumn()).text())

    def open_window_5(self, id, date):
        if date != "Ism Familiya":
            self.setDisabled(True)
            self.w5 = Window_5(id, date)
            self.w5.show()

    def open_window_6(self):
        if self.lineEdit_8.text() != "" and self.lineEdit_6.text() != "" and self.lineEdit_5.text() != "":
            self.setDisabled(True)
            self.w6 = Window_6()
            self.w6.show()
        else:
            QMessageBox.about(self, "Xatolik", "Maktab xaqidagi ma'lumotlar yetarli emas!")
            self.tabWidget.setCurrentIndex(0)
            self.lineEdit_8.setFocus()

    def hide_img_row(self):
        if self.checkBox.isChecked():
            self.tableWidget.setColumnHidden(1, False)
            self.tableWidget.verticalHeader().setDefaultSectionSize(80)
        else:
            self.tableWidget.setColumnHidden(1, True)
            self.tableWidget.verticalHeader().setDefaultSectionSize(30)

    def write_pupils(self, a):
        self.tableWidget.setRowCount(0)
        for row in range(0, len(a)):
            b = self.tableWidget.rowCount()
            self.tableWidget.insertRow(b)
            self.tableWidget.setItem(b, 0, QTableWidgetItem(str(a[b][0])))
            if a[b][1] != "":
                item = self.get_image(a[b][1])
                self.tableWidget.setCellWidget(b, 1, item)
            self.tableWidget.setItem(b, 2, QTableWidgetItem(a[b][3]))
            self.tableWidget.setItem(b, 3, QTableWidgetItem(a[b][5]))
            self.tableWidget.setItem(b, 4, QTableWidgetItem(a[b][6]))
            self.tableWidget.setItem(b, 5, QTableWidgetItem(a[b][7]))
            self.tableWidget.setItem(b, 6, QTableWidgetItem(a[b][8]))
            self.tableWidget.setItem(b, 7, QTableWidgetItem(a[b][4]))
            self.tableWidget.setItem(b, 8, QTableWidgetItem(a[b][9]))
            self.tableWidget.setItem(b, 9, QTableWidgetItem(a[b][11]))
            self.tableWidget.setItem(b, 10, QTableWidgetItem(a[b][12]))
            self.tableWidget.setItem(b, 11, QTableWidgetItem(a[b][13]))
            self.tableWidget.setItem(b, 12, QTableWidgetItem(a[b][10]))

    # write pupils' attendance
    def write_attendance(self, key):
        if key in [None, "Hammasi"]:
            key = "Hammasi"
        else:
            key = key.text()
        descs = self.conn.execute("select * from pupils")
        names = [desc[0] for desc in descs.description][15:]
        names2 = []
        week_days = ["Dush", "Sesh", "Chor", "Pay", "Jum", "Shan", "Yak"]
        for i in names:
            names2.append(week_days[datetime.fromordinal(decoder(i)).weekday(
            )] + ", " + datetime.fromordinal(decoder(i)).strftime("%d/%m/%Y"))
        self.tableWidget_4.setRowCount(len(names))
        names2.insert(0, "Ism Familiya")
        names2.insert(0, "id")
        self.tableWidget_5.setColumnCount(len(names2))
        self.tableWidget_5.setHorizontalHeaderLabels(names2)
        self.tableWidget_5.horizontalHeaderItem(len(names2)-1).setForeground(QColor(0, 139, 242))
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Times New Roman")
        self.tableWidget_5.horizontalHeader().setFont(font)
        self.tableWidget_5.setColumnHidden(0, True)
        self.tableWidget_5.setColumnWidth(1, 220)

        if key == "Hammasi":
            self.cur.execute("""select id, name, surname from pupils""")
        else:
            self.cur.execute(
                f"""select id, name, surname from pupils where class='{key}'""")
        pupils = self.cur.fetchall()
        self.tableWidget_5.setRowCount(0)
        for i in range(len(pupils)):
            self.tableWidget_5.insertRow(i)
            self.tableWidget_5.setItem(
                i, 0, QTableWidgetItem(str(pupils[i][0])))
            self.tableWidget_5.setItem(i, 1, QTableWidgetItem(
                pupils[i][2] + " " + pupils[i][1]))

        def get_count(a):
            c, l = 0, 0
            for i in a:
                if not (i[0] in ["", None]):
                    if len(i[0].split(", ")) == 2:
                        c += 1
                        l += 1
                    elif len(i[0].split(", ")) == 1:
                        c += 1
            if c == 0:
                k = (f"0/{len(a)} 0%", "0/0, 100%", f"0/{len(a)} 0%")
            else:
                k = (f"{c}/{len(a)}, {int(c / len(a) * 100)}%", f"{l}/{c}, {int(l / c * 100)}%",
                     f"{c - l}/{len(a)}, {int((c - l) / len(a) * 100)}%")

            return k

        names2.pop(0)
        names2.pop(0)

        for i in range(len(names)):
            if key == "Hammasi":
                self.cur.execute(f"""select "{names[i]}" from pupils""")
            else:
                self.cur.execute(
                    f"""select "{names[i]}" from pupils where class='{key}'""")
            data = self.cur.fetchall()
            for k in range(len(data)):
                self.tableWidget_5.setItem(
                    k, i + 2, QTableWidgetItem(data[k][0]))
            status = get_count(data)
            self.tableWidget_4.setItem(i, 0, QTableWidgetItem(names2[i]))
            self.tableWidget_4.setItem(i, 1, QTableWidgetItem(status[0]))
            self.tableWidget_4.setItem(i, 2, QTableWidgetItem(status[1]))
            self.tableWidget_4.setItem(i, 3, QTableWidgetItem(status[2]))
        self.tableWidget_4.item(len(names)-1,0).setForeground(QColor(0, 139, 242))

    def update_window(self):
        # total pupils groupbox
        self.cur.execute("""select * from pupils where gender="O'g'il" """)
        self.lineEdit_3.setText(str(len(self.cur.fetchall())))
        self.cur.execute("""select * from pupils where gender="Qiz" """)
        self.lineEdit_4.setText(str(len(self.cur.fetchall())))
        self.cur.execute("""select * from pupils""")
        self.lineEdit_2.setText(str(len(self.cur.fetchall())))
        self.cur.execute("""select * from classes""")
        self.lineEdit_7.setText(str(len(self.cur.fetchall())))
        # table of classes
        self.tableWidget_2.setRowCount(0)
        self.cur.execute("select * from classes order by name")
        a = self.cur.fetchall()
        for row in range(0, len(a)):
            b = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(b)
            self.tableWidget_2.setItem(b, 0, QTableWidgetItem(str(a[b][0])))
            self.tableWidget_2.setItem(b, 1, QTableWidgetItem(a[b][1]))
            self.tableWidget_2.setItem(b, 2, QTableWidgetItem(a[b][2]))
            self.cur.execute(
                """select id from pupils where class=? and gender='Qiz' """, [a[b][1]])
            girls = len(self.cur.fetchall())
            self.cur.execute(
                """select id from pupils where class=? and gender="O'g'il" """, [a[b][1]])
            boys = len(self.cur.fetchall())
            self.tableWidget_2.setItem(
                b, 3, QTableWidgetItem(str(girls + boys)))
            self.tableWidget_2.setItem(b, 4, QTableWidgetItem(str(boys)))
            self.tableWidget_2.setItem(b, 5, QTableWidgetItem(str(girls)))
        # classes combobox
        self.comboBox.clear()
        for i in a:
            self.comboBox.addItem(i[1])
        self.comboBox.addItem("Hammasi")
        self.comboBox.setCurrentText("Hammasi")
        # about school
        self.cur.execute("select * from school")
        a = self.cur.fetchone()
        if not (a == None):
            if not (a[0] == None):
                self.lineEdit_8.setText(a[0])
            if not (a[1] == None):
                self.lineEdit_5.setText(a[1])
            if not (a[2] == None):
                self.lineEdit_6.setText(a[2])
        # classes
        self.tableWidget_3.setRowCount(0)
        a = self.cur.execute("""select * from classes""").fetchall()
        for row in range(0, len(a)):
            b = self.tableWidget_3.insertRow(row)
            self.tableWidget_3.setItem(
                row, 0, QTableWidgetItem(str(a[row][1])))
            self.tableWidget_3.setItem(
                row, 1, QTableWidgetItem(str(a[row][2])))
        self.tableWidget_3.insertRow(len(a))
        self.tableWidget_3.setItem(len(a), 0, QTableWidgetItem("Hammasi"))
        self.write_attendance("Hammasi")

    def get_image(self, image):
        imageLabel = QLabel()
        imageLabel.setText("")
        imageLabel.setScaledContents(True)
        pixmap = QPixmap()
        pixmap.loadFromData(image, 'jpg')
        imageLabel.setPixmap(pixmap)
        return imageLabel


# add pupil
class Window_2(QMainWindow, design_2.Ui_MainWindow):
    def __init__(self, id):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, False)
        self.id = id
        self.photo = ""
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()

        self.format_window()
        if self.id != 0:
            self.write_data()
        else:
            self.old_photo = ""
        self.pushButton_3.clicked.connect(self.set_UserPhoto)
        self.pushButton.clicked.connect(self.finish)
        self.pushButton_2.clicked.connect(self.Close)
        self.pushButton_5.clicked.connect(self.save_user_photo)

    def write_data(self):
        self.cur.execute("select * from pupils where id=?", [self.id])
        # photo
        user = self.cur.fetchone()
        photo = QPixmap()
        if user[1] != "":
            self.old_photo = user[1]
            photo.loadFromData(user[1])
            self.label_9.setPixmap(photo)
        else:
            self.old_photo = ""
        # combobox
        self.comboBox.setCurrentText(user[2])
        self.comboBox_2.setCurrentText(user[3])
        self.comboBox_3.setCurrentText(user[4])
        # date
        if user[9] != "":
            time = datetime.strptime(user[9], "%d/%m/%Y")
            self.dateEdit.setDate(time)
        # texts
        self.lineEdit.setText(user[5])
        self.lineEdit_2.setText(user[6])
        self.lineEdit_3.setText(user[7])
        self.lineEdit_4.setText(user[8])
        self.lineEdit_5.setText(user[11])
        self.lineEdit_6.setText(user[10])
        self.lineEdit_7.setText(user[12])
        self.lineEdit_8.setText(user[13])

    def save_user_photo(self):
        if self.old_photo != "":
            save_path = QFileDialog.getSaveFileName(
                self, 'Rasmni saqlash', '', "Image (*.jpg)"
            )[0]
            if save_path != "":
                with open(save_path, 'wb') as file:
                    file.write(self.old_photo)


    def convertToBinaryData(self, filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def gen_qrcode(self, length):
        strs = string.ascii_letters
        num = string.digits
        res = "".join(random.choice(strs + num) for _ in range(length))
        return res

    def finish(self):
        if "" in [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_5.text(),
                  self.lineEdit_6.text()]:
            pass
        else:
            if self.id != 0:
                if self.photo != "":
                    self.old_photo = self.convertToBinaryData(self.photo)
                if self.dateEdit.date() == datetime.now():
                    birthday = ""
                else:
                    birthday = self.dateEdit.text()
                self.cur.execute("""update pupils set photo=?, class=?, guruh=?, gender=?, name=?, surname=?, 
                father=?, mother=?, birthday=?, location=?, phone=?, passport=?, telegram_id=? where id=?""",
                                 (self.old_photo, self.comboBox.currentText(), self.comboBox_2.currentText(),
                                  self.comboBox_3.currentText(), self.lineEdit.text(), self.lineEdit_2.text(),
                                  self.lineEdit_3.text(), self.lineEdit_4.text(), birthday, self.lineEdit_6.text(),
                                  self.lineEdit_5.text(), self.lineEdit_7.text(), self.lineEdit_8.text(), self.id))
                self.conn.commit()
                self.Close()
                w1.update_window()
            else:
                # user_photo
                if self.photo != "":
                    img = self.convertToBinaryData(self.photo)
                else:
                    img = ""
                # make qrcode
                self.cur.execute("select qrcode from pupils")
                qrcodes = self.cur.fetchall()
                while True:
                    qrcode = self.gen_qrcode(6)
                    if qrcode not in qrcodes:
                        break
                # passport date
                if self.dateEdit.date() == datetime.now():
                    birthday = ""
                else:
                    birthday = self.dateEdit.text()
                self.cur.execute(
                    """insert into pupils(photo, class, guruh, gender, name, surname, father, mother, birthday, location, 
                    phone, passport, telegram_id, qrcode) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (img, self.comboBox.currentText(), self.comboBox_2.currentText(), self.comboBox_3.currentText(),
                     self.lineEdit.text(), self.lineEdit_2.text(
                    ), self.lineEdit_3.text(), self.lineEdit_4.text(),
                     birthday,
                     self.lineEdit_6.text(), self.lineEdit_5.text(), self.lineEdit_7.text(), self.lineEdit_8.text(),
                     qrcode))
                self.conn.commit()
                self.Close()
                w1.update_window()

    def format_window(self):
        self.lineEdit.setFocus()
        self.cur.execute("select name from classes order by name")
        classes = self.cur.fetchall()
        for i in classes:
            self.comboBox.addItem(i[0])
        curr = datetime.now()
        self.dateEdit.setDate(curr)

    def set_UserPhoto(self):
        self.photo = QFileDialog.getOpenFileName(
            self, 'Rasmni yuklash', '', "Image (*.jpg)")[0]
        if self.photo != "":
            pic = QPixmap(self.photo)
            self.label_9.setPixmap(pic)

    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key_Escape:
            self.Close()

    def closeEvent(self, e):
        self.Close()

    def Close(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.close()
        w1.setDisabled(False)


# add class
class Window_3(QMainWindow, design_3.Ui_MainWindow):
    def __init__(self, id):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, False)
        self.id = int(id)
        self.pushButton_2.clicked.connect(self.Close)
        self.pushButton.clicked.connect(self.finish)
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        if self.id != 0:
            self.write_data(id)

    def write_data(self, id):
        self.cur.execute("select * from classes where id=?", [id])
        data = self.cur.fetchone()
        if data is not None:
            self.lineEdit.setText(data[1])
            self.lineEdit_2.setText(data[2])

    def keyPressEvent(self, e):
        k = e.key()
        if k == Qt.Key_Escape:
            self.Close()
        elif k == Qt.Key_Up and self.lineEdit_2.hasFocus():
            self.lineEdit.setFocus()
        elif k in [Qt.Key_Down, Qt.Key_Enter, Qt.Key_Return] and self.lineEdit.hasFocus():
            self.lineEdit_2.setFocus()
        elif k in [Qt.Key_Enter, Qt.Key_Return] and self.lineEdit_2.hasFocus():
            self.finish()

    def finish(self):
        if "" in [self.lineEdit.text(), self.lineEdit_2.text()]:
            pass
        else:
            if self.id == 0:
                self.cur.execute("select * from classes where name=? or classcom=?",
                                 [self.lineEdit.text(), self.lineEdit_2.text()])
                if self.cur.fetchone() is None:
                    self.cur.execute("insert into classes(name, classcom) values(?, ?)",
                                     [self.lineEdit.text(), self.lineEdit_2.text()])
                    self.conn.commit()
                else:
                    self.lineEdit.setFocus()
            else:
                self.cur.execute(
                    "select name from classes where id=?", [self.id])
                class_name = self.cur.fetchone()[0]
                self.cur.execute("update pupils set class=? where class=?", [
                    self.lineEdit.text(), class_name])
                self.cur.execute("update classes set name=?, classcom=? where id=?",
                                 [self.lineEdit.text(), self.lineEdit_2.text(), self.id])
                self.conn.commit()
            self.conn.close()
            self.Close()
            w1.update_window()

    def closeEvent(self, e):
        self.Close()

    def Close(self):
        w1.setDisabled(False)
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.close()


# change time
class Window_5(QMainWindow, design_5.Ui_MainWindow):
    def __init__(self, id, date):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, False)
        self.id = id
        date = date.split(", ")[1].split("/")
        self.date = encoder(
            datetime(int(date[2]), int(date[1]), int(date[0])).toordinal())
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        self.write_data()
        self.pushButton_3.clicked.connect(
            lambda x: self.timeEdit.setDateTime(datetime.now()))
        self.pushButton_4.clicked.connect(
            lambda x: self.timeEdit_2.setDateTime(datetime.now()))
        self.pushButton_7.clicked.connect(
            lambda x: self.timeEdit.setDateTime(datetime.strptime("0:00", "%H:%M")))
        self.pushButton_6.clicked.connect(
            lambda x: self.timeEdit_2.setDateTime(datetime.strptime("0:00", "%H:%M")))
        self.pushButton_5.clicked.connect(self.Close)
        self.pushButton_8.clicked.connect(self.Finish)

    def Finish(self):
        t1 = self.timeEdit.text()
        t2 = self.timeEdit_2.text()
        if t1 == "0:00" and t2 != "0:00":
            return 0
        elif t1 != "0:00" and t2 == "0:00":
            res_date = t1
        elif t1 != "0:00" and t2 != "0:00":
            res_date = t1 + ", " + t2
        else:
            res_date = None
        self.cur.execute(f"""update pupils set "{self.date}"=? where id=?""", [
            res_date, self.id])
        self.conn.commit()
        self.conn.close()
        self.Close()

    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key_Escape:
            self.Close()
        elif key in [Qt.Key_Return, Qt.Key_Enter]:
            self.Finish()

    def closeEvent(self, e):
        self.Close()

    def Close(self):
        self.close()
        w1.setDisabled(False)
        w1.update_window()

    def write_data(self):
        self.cur.execute(
            f"""select "{self.date}" from pupils where id={self.id}""")
        k = self.cur.fetchone()[0]
        if k in [None, ""]:
            times = []
        else:
            times = k.split(", ")
        if len(times) == 2:
            self.timeEdit.setDateTime(datetime.strptime(times[0], "%H:%M"))
            self.timeEdit_2.setDateTime(datetime.strptime(times[1], "%H:%M"))
        elif len(times) == 1:
            self.timeEdit.setDateTime(datetime.strptime(times[0], "%H:%M"))


# Camera
class Window_6(QMainWindow, design_6.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.volume = True
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, False)
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.run_camera)
        self.ip_cam_visible()
        self.comboBox.currentIndexChanged.connect(self.ip_cam_visible)
        self.write_dates()
        self.pushButton_2.clicked.connect(self.stop_cam)
        self.pushButton_3.clicked.connect(self.change_volume)

    def Close(self):
        w1.setDisabled(False)
        self.stop_cam()
        self.close()

    def change_volume(self):
        self.volume_on = QIcon()
        self.volume_on.addPixmap(
            QPixmap(":/Icons/Icons/volume_on.png"), QIcon.Normal, QIcon.On)
        self.volume_off = QIcon()
        self.volume_off.addPixmap(
            QPixmap(":/Icons/Icons/volume_off.png"), QIcon.Normal, QIcon.On)
        if self.volume:
            self.volume = False
            self.pushButton_3.setIcon(self.volume_off)
        else:
            self.volume = True
            self.pushButton_3.setIcon(self.volume_on)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.Close()

    def closeEvent(self, e):
        self.Close()

    def write_dates(self):
        week_days = ["Dush", "Sesh", "Chor", "Pay", "Jum", "Shan", "Yak"]
        today_date = week_days[datetime.today().weekday(
        )] + ", " + datetime.today().strftime("%d/%m/%Y")
        self.lineEdit_2.setText(today_date)

    def ip_cam_visible(self):
        if self.comboBox.currentText() == "IP Webcam":
            c = True
        else:
            c = False
        self.label_3.setVisible(c)
        self.lineEdit.setVisible(c)

    def run_camera(self):
        if self.comboBox.currentText() == "Kompyuter":
            camera = 0
        else:
            if self.lineEdit.text() == "":
                self.lineEdit.setFocus()
                return 0
            else:
                try:
                    Image.open(urlopen(self.lineEdit.text() + "/shot.jpg"))
                except:
                    return 0
                camera = self.lineEdit.text() + "/video"
        self.th1 = self.MyCam(camera)
        self.th1.start()
        self.comboBox.setDisabled(True)
        self.lineEdit.setDisabled(True)
        self.lineEdit_2.setDisabled(True)
        self.comboBox_2.setDisabled(True)
        self.pushButton.setDisabled(True)

    def stop_cam(self):
        if not (self.pushButton.isEnabled()):
            self.comboBox.setDisabled(False)
            self.lineEdit.setDisabled(False)
            self.lineEdit_2.setDisabled(False)
            self.comboBox_2.setDisabled(False)
            self.pushButton.setDisabled(False)
            try:
                if self.th1.cap.isOpened():
                    self.th1.cap.release()
                if self.th1.isRunning():
                    self.th1.terminate()
            except:
                pass
            self.label.setPixmap(QPixmap(":/Icons/Icons/transparent.png"))
            w1.update_window()

    class MyCam(QThread):
        def __init__(self, cam):
            super().__init__()
            self.last_time = time.perf_counter()
            self.cam = cam
            self.con = sqlite3.connect(database, check_same_thread=False)
            self.cur = self.con.cursor()

        def check_qrcode(self, qrcode):
            check = self.cur.execute(
                f"select id from pupils where qrcode = '{qrcode}'").fetchone()
            if check is None:
                return 0
            else:
                return check[0]

        def notify(self, code):
            if time.perf_counter() - self.last_time > 1:
                if code == 1:
                    if w1.w6.checkBox.isChecked():
                        my_th = send_to_parents(self.id)
                        my_th.start()
                    if w1.w6.volume:
                        try:
                            playsound("./correct.wav")
                        except:
                            pass
                self.last_time = time.perf_counter()

        def write_time(self, date, action, id):
            self.cur.execute(f"select {date} from pupils where id={id}")
            k = self.cur.fetchone()[0]
            if k in [None, ""]:
                times = []
            else:
                times = k.split(", ")
            cur_time = datetime.now().strftime("%H:%M")
            if len(times) == 2:
                return 0
            elif len(times) == 1:
                if action == "Keldi":
                    return 0
                else:
                    times.append(cur_time)
            elif len(times) == 0:
                if action == "Keldi":
                    times.append(cur_time)
                else:
                    return 0
            self.cur.execute(f"""update pupils set "{date}"=? where id=?""", [
                ", ".join(times), id])
            self.con.commit()
            return 1

        def set_user_photo(self):
            self.cur.execute("select * from pupils where id=?", [self.id])
            photo_usr = self.cur.fetchone()
            if len(photo_usr) != 0:
                if photo_usr[1] != "":
                    pm = QPixmap()
                    pm.loadFromData(photo_usr[1])
                    w1.w6.label_6.setPixmap(pm)

        def run(self):
            qrCodeDetector = cv2.QRCodeDetector()
            self.cap = cv2.VideoCapture(self.cam)
            while True:
                try:
                    success, image = self.cap.read()
                    if success:
                        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        height, width, channel = img.shape
                        step1 = channel * width
                        try:
                            if reader.extract(image):
                                barcode, points, _ = func_timeout(1, qrCodeDetector.detectAndDecode, args=(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),))
                            else:
                                barcode = None
                        except FunctionTimedOut:
                            barcode = None
                        if not ((barcode is None) or (barcode == "")):
                            myData = barcode
                            self.id = self.check_qrcode(myData)
                            if self.id != 0:
                                color = (0, 255, 65)
                                color_text = (0, 0, 255)
                                self.infor = self.write_time(
                                    encoder(datetime.today().toordinal()), w1.w6.comboBox_2.currentText(), self.id)
                                if self.infor == 0:
                                    color_text = (255, 0, 0)
                                    text = "Xatolik"
                                else:
                                    text = "Tasdiqlandi"
                            else:
                                color = (240, 0, 0)
                                color_text = (255, 85, 255)
                                text = "Mavjud emas"

                            # qr shape
                            pts = points[0]
                            polygon = [(pts[0][0], pts[0][1]), (pts[1][0], pts[1][1]),
                                       (pts[2][0], pts[2][1]), (pts[3][0], pts[3][1])]
                            pts = np.array([polygon], np.int32)
                            cv2.polylines(img, [pts], True, color, 3)

                            pts2 = polygon[0]
                            cv2.putText(img, text, (int(pts2[0]), int(pts2[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.8, color_text, 2)
                        qim = QImage(img.data, width, height,
                                     step1, QImage.Format_RGB888)
                        w1.w6.label.setPixmap(QPixmap.fromImage(qim))
                        if hasattr(self, 'infor'):
                            self.set_user_photo()
                            self.notify(self.infor)
                            del self.infor
                except Exception as er:
                    print(er)


class send_to_parents(QThread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self):
        c = True
        cur.execute(f"select * from pupils where id={self.id}")
        data = cur.fetchone()
        cur.execute("select * from school")
        school = cur.fetchone()
        if w1.w6.comboBox_2.currentText() == "Keldi":
            action = "↙️Keldi"
        else:
            action = "↗️Ketdi"
        date = f"🕔 Vaqt:  <code>{w1.w6.lineEdit_2.text()} " + datetime.now().strftime("%H:%M") + \
               "</code>"
        text = date + "\n------------------------------------------------------\n"
        text += f"<b>🔔 Xarakat</b>:  <cod e>{action}</code>\n  <b>🏫 Maktab:</b>  {school[2]}\n<b>  Ism:</b>  {data[5]}\n<b>  Familiya:</b>  {data[6]}\n<b>  Sinf:</b>  {data[2]}"
        while c:
            try:
                data_ = {"chat_id": data[13],
                         "text": text,
                         "parse_mode": "HTML"}
                post(url, data=data_)
                c = False
            except Exception as er:
                with open("logs.txt", "w+") as f:
                    f.write(str(er))


def get_mac():
    return socket.gethostname()


def on_to_2(num, n):
    satr = ""
    while num != 0:
        satr = str(num % 2) + satr
        num = (num // 2)
    while len(satr) < n:
        satr = '0' + satr
    return satr


def enycrypt(matn):
    p = 241
    g = 51
    x = 98
    k = 12
    b01 = ""
    for c in matn:
        b01 += str(on_to_2(ord(c), 8))

    int(math.log(p, 2))
    while len(b01) % (int(math.log(p, 2))) != 0:
        b01 = '0' + b01

    y = (g ** x) % p
    a = (g ** k) % p
    shifr = chr(a)
    for i in range(0, len(b01), 7):
        b_i_son = int(b01[i:i + 7], 2)
        natija = (y ** k * b_i_son) % p
        shifr += chr(natija)
    return shifr


def funk_10_to_2(num, n):
    satr = ""
    while num != 0:
        satr = str(num % 2) + satr
        num = (num // 2)
    while len(satr) < n:
        satr = '0' + satr
    return satr


def decrypt(shifr):
    p = 241
    x = 98
    a = ord(shifr[0])
    a_1 = (a ** (p - 2)) % p
    a_1 = (a_1 ** x) % p
    b01 = ""
    for i in range(1, len(shifr)):
        b01 += funk_10_to_2((ord(shifr[i]) * a_1) % p, int(math.log(p, 2)))
    ortiqcha_soni = len(b01) % 8
    b01 = b01[ortiqcha_soni: len(b01)]
    matn = ""
    for i in range(0, len(b01), 8):
        matn += chr(int(b01[i:i + 8], 2))
    return matn


def encode_password(text):
    s = datetime.today().toordinal()+20
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) + s - 65) % 26 + 65)
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)

    return result


# activation
class Window_7(QMainWindow, design_7.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, False)
        self.lineEdit.setText(encode_password(get_mac()).upper())
        self.pushButton_2.clicked.connect(lambda x: self.close())
        self.pushButton.clicked.connect(self.check_password)
        self.pushButton_4.clicked.connect(lambda x: QApplication.clipboard().setText(self.lineEdit.text()))

    def check_password(self):
        if self.lineEdit_2.text() == encode_password(self.lineEdit.text()):
            f = open("license.bin", "wb")
            f.write(enycrypt(get_mac()).encode("utf8"))
            f.close()
            self.close()
            global w1
            w1 = Main_window()
            w1.showMaximized()
            QMessageBox.about(self, "SControl activation", "Dastur muvofaqqiyatli aktivlashtirildi!")
        else:
            QMessageBox.about(self, "Xatolik", "Parol xato kiritildi, iltimos qayta kiriting!")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    try:
        if not (os.path.exists(os.getenv("APPDATA") + "\SControl")):
            os.mkdir(os.getenv("APPDATA") + "\SControl")
        database = os.getenv("APPDATA") + "\SControl\data.db"
        app = QApplication(sys.argv)
        con = sqlite3.connect(database, check_same_thread=False)
        cur = con.cursor()
        if os.path.exists("license.bin"):
            f = open("license.bin", "rb")
            if enycrypt(get_mac()) == f.read().decode("utf8"):
                w1 = Main_window()
                w1.showMaximized()
            else:
                w7 = Window_7()
                w7.show()
            f.close()
        else:
            w7 = Window_7()
            w7.show()
            open("license.bin", "wb")
        sys.exit(app.exec_())
    except Exception as er:
        with open("logs.txt", "w+") as f:
            f.write(str(er))