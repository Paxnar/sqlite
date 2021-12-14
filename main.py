import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.update_result)
        self.pushButton_2.clicked.connect(self.addS)
        self.pushButton_3.clicked.connect(self.editS)
        self.modified = {}
        self.titles = None

    def addS(self):
        self.form = Addedit('add')
        self.form.show()

    def editS(self):
        self.form = Addedit('edit')
        self.form.show()

    def update_result(self):
        try:
            cur = self.con.cursor()
            # Получили результат запроса, который ввели в текстовое поле
            result = cur.execute("SELECT * FROM coffe").fetchall()
            # Заполнили размеры таблицы
            self.tableWidget.setRowCount(len(result))
            # Если запись не нашлась, то не будем ничего делать
            if not result:
                self.statusBar().showMessage('Ничего не нашлось')
                return
            self.tableWidget.setColumnCount(len(result[0]))
            self.titles = [description[0] for description in cur.description]
            # Заполнили таблицу полученными элементами
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}
        except BaseException as be:
            print(be)

    def item_changed(self, item):
        pass

    def save_results(self):
        pass


class Addedit(QMainWindow):
    def __init__(self, what):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        if what == 'add':
            self.pushButton.setEnabled(True)
            self.pushButton.clicked.connect(self.add_results)
        else:
            self.spinBox_2.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_2.clicked.connect(self.save_results)

    def add_results(self):
        cur = self.con.cursor()
        lisedit = [self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text()]
        if '' in lisedit:
            self.label_8.setText('поле пусто')
            return
        else:
            self.label_8.setText('')
        if self.radioButton.isChecked():
            checker = 'молотый'
        elif self.radioButton_2.isChecked():
            checker = 'в зёрнах'
        cur.execute("""INSERT INTO coffe(название_сорта, степень_обжарки, молотый_в_зернах, описание_вкуса,
                                                              цена, объем_упаковки) VALUES(?, ?, ?, ?, ?, ?)""",\
                    (lisedit[0], lisedit[1], checker, lisedit[2], self.spinBox.value(), self.spinBox_3.value()))
        self.con.commit()
        self.close()

    def save_results(self):
        cur = self.con.cursor()
        ids = cur.execute("SELECT ID FROM coffe").fetchall()
        lis = []
        for i in ids:
            lis.append(i[0])
        if self.spinBox_2.value() not in lis:
            self.label_8.setText('неправильный ID')
            return
        else:
            self.label_8.setText('')
        lisedit = [self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text()]
        if '' in lisedit:
            self.label_8.setText('поле пусто')
            return
        else:
            self.label_8.setText('')
        if self.radioButton.isChecked():
            checker = 'молотый'
        elif self.radioButton_2.isChecked():
            checker = 'в зёрнах'

        que = """UPDATE coffe
                                  SET название_сорта = ?, степень_обжарки = ?, молотый_в_зернах = ?, описание_вкуса = ?,
                                  цена = ?, объем_упаковки = ?              
                                  WHERE ID = ?"""
        cur.execute(que, (lisedit[0], lisedit[1], checker, lisedit[2], self.spinBox.value(), self.spinBox_3.value(),
                          self.spinBox_2.value()))
        self.con.commit()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())