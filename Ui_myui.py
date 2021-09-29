import sys
import requests
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 140, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(50, 90, 113, 20))
        self.lineEdit.setObjectName("lineEdit")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 50, 150, 12))
        self.label.setObjectName("label")

        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(50, 150, 500, 200))
        self.label1.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "搜書小達人"))
        self.pushButton.setText(_translate("MainWindow", "我搜"))
        self.label.setText(_translate("MainWindow", "請輸入欲搜尋的書名"))
        self.label1.setText(_translate("MainWindow", ""))
        self.pushButton.clicked.connect(self.mysearch)
    def mysearch(self):
        s=self.lineEdit.text()
        B = Books()
        result1 = B.search(s)

        E = Eslite()
        result = E.search(s)

        K = Kingstone()
        result2 = K.search(s)

        self.label1.setText("博客來\n" + result[0] + "\n" + result[1] + "\n" + result[2]+"\n"+"誠品\n" + result1[0] + "\n" + result1[1] + "\n" + result1[2]+"\n"+"金石堂\n" + result2[0] + "\n" + result2[1] + "\n" + result2[2])
        

class Eslite:
    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        self.url = "http://www.eslite.com/Search_BW.aspx?query="

    def search(self, name):
        if " " in name:
            name = name.strip().replace(" ", "+")
        r = requests.get(self.url+name, headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")
        target = soup.find(class_="box_list")
        target = target.find("table")
        anchor = target.find(class_="name")
        anchor = anchor.find_all("a")[1]
        price = target.find_all(class_="price_sale")
        string = ""
        if len(price) > 2:
            string += price[0].text.replace(",", "").strip() + " " + price[2].text
        else:
            string += price[1].text
        return [anchor["title"], string, anchor["href"]]

class Kingstone:
    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        self.url = "https://www.kingstone.com.tw/new/search/search?q="

    def search(self, name):
        if " " in name:
            name = name.strip().replace(" ", "+")
        r = requests.get(self.url+name, headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")
        target = soup.find(class_="division1 clearfix")
        anchor = target.find(class_="pdnamebox").a
        price = target.find(class_="buymixbox")
        price = price.find_all("span")
        string = ""
        if len(price) > 2:
            string += price[0].text + price[1].text
        else:
            string += price[0].text
        return [anchor.text, string, "https://www.kingstone.com.tw" + anchor["href"]]

class Books:
    def __init__(self):
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        self.url = "https://search.books.com.tw/search/query/key/"

    def search(self, name):
        r = requests.get(self.url+name.strip(),  headers=self.headers)
        soup = BeautifulSoup(r.text, "lxml")
        target = soup.find(class_="item")   
        anchor = target.find(attrs={"rel": "mid_name"})
        price = target.find(class_="price")
        price = price.find_all("strong")
        string = ""
        for ele in price:
            string += ele.text + " "
        return [anchor["title"], string.strip(), "https:" + anchor["href"]]

if __name__ == "__main__":
   want = "狼與辛香料 20"
   app = QtWidgets.QApplication(sys.argv)
   MainWindow = QtWidgets.QMainWindow()
   ui = Ui_MainWindow()
   ui.setupUi(MainWindow)
   MainWindow.show()
   sys.exit(app.exec_())