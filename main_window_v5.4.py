import sys
from PyQt5.QtWidgets import QLabel, QWidget, QCheckBox, QPushButton, QApplication, QScrollArea, QFrame, QLineEdit, QMainWindow, QAction, QMenu, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from Mypymongo import Mydb
from re import compile
import os
from Finder_Books import Books
from Finder_Eslite import Eslite
from Finder_Kingstone import Kingstone
from Finder_Library import Library
import urllib.request

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = Mydb()
        self.L = Library()
        self.B = Books()
        self.E = Eslite()
        self.K = Kingstone()
        self.initUI()
        
    def initUI(self):  
        self.widget = QWidget()
        menubar = self.menuBar()
        self.setFixedSize(1600, 900)


        self.islogin = False
        self.issignup = False
        self.issignin = False

        page = menubar.addMenu('Page')
        settings = menubar.addMenu('Settings')

        back_to_home = QAction('Home', self)
        back_to_home.setStatusTip('Back to home')
        back_to_home.triggered.connect(self.home)
        my_history = QAction('History', self)
        my_history.setStatusTip('My History')
        my_history.triggered.connect(self.show_History)
        my_account = QMenu('My Account', self)
        my_account_edit = QAction('Edit', self)
        my_account.addAction(my_account_edit)
        my_account_logout = QAction('Log Out', self)
        my_account.addAction(my_account_logout)
        my_account_logout.triggered.connect(self.logout)

        language = QMenu('Language', self)
        language_en = QAction('English', self)
        language.addAction(language_en)
        language_ch = QAction('Chinese', self)
        language.addAction(language_ch)
        
        page.addAction(back_to_home)
        page.addAction(my_history)
        settings.addMenu(my_account)
        settings.addMenu(language)

        self.main_frame = QFrame(self.widget)

###########################################################

        self.left_frame = QFrame(self.main_frame)
        self.left_frame.setGeometry(0, 0, 800, 900)
        self.right_frame = QFrame(self.main_frame)
        self.right_frame.setGeometry(800, 0, 800, 900)
        
        self.logo_label = QLabel(self.left_frame)
        self.pixmap = QPixmap('logo.jpg')
        self.logo_label.setPixmap(self.pixmap)
        self.logo_label.setGeometry(0, 0, 800, 900)

        self.sign_in_btn = QPushButton('Sign In', self.right_frame)
        self.sign_in_btn.setGeometry(266, 200, 266, 50)
        self.sign_in_btn.clicked.connect(self.sign_in)
        self.sign_up_btn = QPushButton('Sign Up', self.right_frame)
        self.sign_up_btn.setGeometry(266, 650, 266, 50)
        self.sign_up_btn.clicked.connect(self.sign_up)

#############################################################

        self.sign_in_frame = QFrame(self.main_frame)
        self.sign_in_frame.setGeometry(800, 0, 800, 900)

        self.font = QFont()
        self.font.setPointSize(15)
        self.store_name_font = QFont()
        self.store_name_font.setPointSize(30)

        self.account_label = QLabel('Account', self.sign_in_frame)
        self.account_label.setFont(self.font)
        self.account_edit = QLineEdit(self.sign_in_frame)
        self.account_label.setGeometry(40, 190, 150, 40)
        self.account_edit.setGeometry(190, 190, 490, 40)

        self.password_label = QLabel('Password', self.sign_in_frame)
        self.password_label.setFont(self.font)
        self.password_edit = QLineEdit(self.sign_in_frame)
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_label.setGeometry(40, 375, 150, 40)
        self.password_edit.setGeometry(190, 375, 490, 40)

        self.save_login = QCheckBox('save login', self.sign_in_frame)
        self.save_login.setGeometry(408, 570, 150, 40)
        self.save_login.setFont(self.font)
        # self.save_login.stateChanged.connect(self.save_check)

        self.forget = QPushButton('forget', self.sign_in_frame)
        self.forget.setGeometry(525, 570, 150, 40)
        self.forget.clicked.connect(self.forget_account)

        self.in_submit_button = QPushButton('Submit', self.sign_in_frame)
        self.in_submit_button.setGeometry(525, 750, 150, 40)
        self.in_submit_button.clicked.connect(self.signin_submit)

        self.backbtn = QPushButton('Back', self.sign_in_frame)
        self.backbtn.setGeometry(40, 750, 150, 40)
        self.backbtn.clicked.connect(self.main)
        
######################################################################

        self.forget_frame = QFrame(self.main_frame)
        self.forget_frame.setGeometry(800, 0, 800, 900)

        self.forget_account_label = QLabel('Account', self.forget_frame)
        self.forget_account_label.setFont(self.font)
        self.forget_account_edit = QLineEdit(self.forget_frame)
        self.forget_account_label.setGeometry(40, 190, 190, 40)
        self.forget_account_edit.setGeometry(190, 190, 490, 40)

        self.forget_email_label = QLabel('Enter your email', self.forget_frame)
        self.forget_email_label.setFont(self.font)
        self.forget_email_edit = QLineEdit(self.forget_frame)
        self.forget_email_label.setGeometry(13, 375, 175, 40)
        self.forget_email_edit.setGeometry(190, 375, 490, 40)

        self.forget_submit_button = QPushButton('Submit', self.forget_frame)
        self.forget_submit_button.setGeometry(420, 600, 120, 30)
        # self.forget_submit_button.clicked.connect()

        self.forget_back_button = QPushButton('Back', self.forget_frame)
        self.forget_back_button.setGeometry(40, 750, 150, 40)
        self.forget_back_button.clicked.connect(self.sign_in)

######################################################################

        self.sign_up_frame = QFrame(self.main_frame)
        self.sign_up_frame.setGeometry(800, 0, 800, 900)

        self.set_account_label = QLabel('Account', self.sign_up_frame)
        self.set_account_label.setFont(self.font)
        self.set_account_edit = QLineEdit(self.sign_up_frame)
        self.set_account_label.setGeometry(0, 190, 190, 40)
        self.set_account_edit.setGeometry(225, 190, 490, 40)

        self.set_nickname_label = QLabel('Nickname', self.sign_up_frame)
        self.set_nickname_label.setFont(self.font)
        self.set_nickname_edit = QLineEdit(self.sign_up_frame)
        self.set_nickname_label.setGeometry(0, 250, 190, 40)
        self.set_nickname_edit.setGeometry(225, 250, 490, 40)

        self.set_email_label = QLabel('Email', self.sign_up_frame)
        self.set_email_label.setFont(self.font)
        self.set_email_edit = QLineEdit(self.sign_up_frame)
        self.set_email_label.setGeometry(0, 313, 190, 40)
        self.set_email_edit.setGeometry(225, 313, 490, 40)

        self.set_password_label = QLabel('Password', self.sign_up_frame)
        self.set_password_label.setFont(self.font)
        self.set_password_edit = QLineEdit(self.sign_up_frame)
        self.set_password_edit.setEchoMode(QLineEdit.Password)
        self.set_password_label.setGeometry(0, 375, 190, 40)
        self.set_password_edit.setGeometry(225, 375, 490, 40)

        self.set_confirm_password_label = QLabel('Comfirm Password', self.sign_up_frame)
        self.set_confirm_password_label.setFont(self.font)
        self.set_confirm_password_edit = QLineEdit(self.sign_up_frame)
        self.set_confirm_password_edit.setEchoMode(QLineEdit.Password)
        self.set_confirm_password_label.setGeometry(0, 440, 190, 40)
        self.set_confirm_password_edit.setGeometry(225, 440, 490, 40)

        self.up_submit_button = QPushButton('Submit', self.sign_up_frame)
        self.up_submit_button.setGeometry(560, 750, 150, 40)
        self.up_submit_button.clicked.connect(self.signup_submit)

        self.backbtn = QPushButton('Back', self.sign_up_frame)
        self.backbtn.setGeometry(0, 750, 150, 40)
        self.backbtn.clicked.connect(self.main)
        
############################################################################

        self.main_search_frame = QFrame(self.main_frame)
        self.main_search_frame.setGeometry(0, 0, 1600, 900)

        self.select_store = 0

        self.booktitle_label = QLabel('Book Title', self.main_search_frame)
        self.booktitle_label.setFont(self.font)
        self.booktitle_label.setGeometry(30, 40, 100, 40)
        self.search_edit = QLineEdit(self.main_search_frame)
        self.search_edit.setGeometry(220, 40, 1100, 40)
        self.search_btn = QPushButton('Search', self.main_search_frame)
        self.search_btn.setGeometry(1375, 40, 190, 40)
        self.search_btn.clicked.connect(self.store_check)

        self.choose = QLabel('BookStore', self.main_search_frame)
        self.choose.setFont(self.font)
        self.choose.setGeometry(30, 100, 100, 40)
        self.check_store1 = QCheckBox('NPTU Library', self.main_search_frame)
        self.check_store1.setGeometry(220, 100, 190, 40)
        self.check_store1.setFont(self.font)
        self.check_store2 = QCheckBox('Books', self.main_search_frame)
        self.check_store2.setGeometry(540, 100, 190, 40)
        self.check_store2.setFont(self.font)
        self.check_store3 = QCheckBox('Eslite', self.main_search_frame)
        self.check_store3.setGeometry(860, 100, 190, 40)
        self.check_store3.setFont(self.font)
        self.check_store4 = QCheckBox('Kingstone', self.main_search_frame)
        self.check_store4.setGeometry(1180, 100, 190, 40)
        self.check_store4.setFont(self.font)

        self.check_store1.stateChanged.connect(self.check_store)
        self.check_store2.stateChanged.connect(self.check_store)
        self.check_store3.stateChanged.connect(self.check_store)
        self.check_store4.stateChanged.connect(self.check_store)

        self.top_hot_frame = QFrame(self.main_search_frame)
        self.top_hot_frame.setGeometry(30, 150, 1540, 720)
        self.top_hot_lab = QLabel('this is top hop', self.top_hot_frame)
        self.top_hot_lab.setGeometry(0, 0, 1540, 720)
        self.top_hot_lab.setOpenExternalLinks(True)

######################################################################

        self.search_result_frame = QFrame(self.main_search_frame)
        self.search_result_frame.setGeometry(30, 150, 1540, 720)
        
######################################################################

        self.history_frame = QFrame(self.main_search_frame)
        self.history_frame.setGeometry(30, 150, 1540, 720)
        
        self.history_lab1 = QLabel("",self.history_frame)
        self.history_lab1.setGeometry(10, 10, 1000, 50)
        self.history_lab1.setFont(self.store_name_font)
        self.history_lab2 = QLabel("",self.history_frame)
        self.history_lab2.setGeometry(10, 60, 1000, 50)
        self.history_lab2.setFont(self.store_name_font)
        self.history_lab3 = QLabel("",self.history_frame)
        self.history_lab3.setGeometry(10, 110, 1000, 50)
        self.history_lab3.setFont(self.store_name_font)
        self.history_lab4 = QLabel("",self.history_frame)
        self.history_lab4.setGeometry(10, 160, 1000, 50)
        self.history_lab4.setFont(self.store_name_font)
        self.history_lab5 = QLabel("",self.history_frame)
        self.history_lab5.setGeometry(10, 210, 1000, 50)
        self.history_lab5.setFont(self.store_name_font)

        self.history_btn1 = QPushButton("search",self.history_frame)
        self.history_btn1.setGeometry(1010, 10, 100, 50)
        self.history_btn1.clicked.connect(lambda: self.history_search(0))
        self.history_btn2 = QPushButton("search",self.history_frame)
        self.history_btn2.setGeometry(1010, 60, 100, 50)
        self.history_btn2.clicked.connect(lambda: self.history_search(1))
        self.history_btn3 = QPushButton("search",self.history_frame)
        self.history_btn3.setGeometry(1010, 110, 100, 50)
        self.history_btn3.clicked.connect(lambda: self.history_search(2))
        self.history_btn4 = QPushButton("search",self.history_frame)
        self.history_btn4.setGeometry(1010, 160, 100, 50)
        self.history_btn4.clicked.connect(lambda: self.history_search(3))
        self.history_btn5 = QPushButton("search",self.history_frame)
        self.history_btn5.setGeometry(1010, 210, 100, 50)
        self.history_btn5.clicked.connect(lambda: self.history_search(4))


######################################################################
        self.main()
        #self.main_search()

        self.main_frame.show()
        self.setCentralWidget(self.widget)

        self.setGeometry(0, 0, 1600, 900)
        self.setWindowTitle('search system')
        self.show()

    def main(self):
        self.all_hide()
        self.right_frame.show()
        self.left_frame.show()

    def all_hide(self):
        self.account_edit.setText('')
        self.forget_account_edit.setText('')
        self.forget_email_edit.setText('')
        self.password_edit.setText('')
        self.search_edit.setText('')
        self.set_account_edit.setText('')
        self.set_confirm_password_edit.setText('')
        self.set_email_edit.setText('')
        self.set_nickname_edit.setText('')
        self.set_password_edit.setText('')

        self.main_search_frame.hide()
        self.right_frame.hide()
        self.left_frame.hide()
        self.sign_in_frame.hide()
        self.sign_up_frame.hide()
        self.search_result_frame.hide()
        self.top_hot_frame.hide()
        self.forget_frame.hide()
        self.history_frame.hide()

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Enter: 
            if self.islogin:
                self.store_check()
            if self.issignup:
                self.signup_submit()
            if self.issignin:
                self.signin_submit()

    def sign_in(self):
        self.issignin = True
        self.islogin = False
        self.issignup = False

        self.all_hide()
        self.left_frame.show()
        self.sign_in_frame.show()
        if os.path.isfile("account.csv"):
            fp = open("account.csv")
            temp = fp.readline().split(",")
            self.account_edit.setText(temp[0])
            self.password_edit.setText(temp[1])
            self.save_login.setChecked(True)

    def sign_up(self):
        self.issignup = True
        self.islogin = False
        self.issignin = False

        self.all_hide()
        self.left_frame.show()
        self.sign_up_frame.show()

    def signin_submit(self):

        username = self.account_edit.text().strip()
        password = self.password_edit.text().strip()
        result = self.client.find({"username": username})
        if len(result) == 0 or result[0]["password"] != password:
            QMessageBox.warning(self, '確認', 'wrong account or password', QMessageBox.Yes, )
        else:
            if self.save_login.isChecked():
                fp = open("account.csv", "w")
                fp.write(f"{username},{password}")
                fp.close()
            else:
                if os.path.isfile("account.csv"):
                    os.remove("account.csv")
            self.client.this = self.client.find({"username": username})[0]      ####
            self.main_search()


    def signup_submit(self):

        username = self.set_account_edit.text().strip()
        nickname = self.set_nickname_edit.text().strip()
        email = self.set_email_edit.text().strip()
        password = self.set_password_edit.text().strip()
        confirm = self.set_confirm_password_edit.text().strip()
        error_message = ""
        check = 0
        for i in password:
            if not ('A' <= i <= 'Z' or 'a' <= i <= 'z' or '0' <= i <= '9'):
                check += 1
        error_message = error_message + "Plz enter your account name\n" if not username else error_message
        error_message = error_message + "Plz enter your nickname\n" if not nickname else error_message
        error_message = error_message + "Plz enter your email\n" if not email else error_message
        error_message = error_message + "Plz enter your password\n" if not password else error_message
        error_message = error_message + "Plz enter your confirm password\n" if not confirm else error_message
        error_message = error_message + "This account has been used.\n" if len(self.client.find({"username": username})) > 0 else error_message
        error_message = error_message + "This email is malformed.\n" if not compile(r"[^@]+@[^@]+\.[^@]+").match(email) else error_message
        error_message = error_message + "This email has been used.\n" if len(self.client.find({"email": email})) > 0 else error_message
        error_message = error_message + "Your password less than 8 words.\n" if len(password) < 8 else error_message
        error_message = error_message + "Your password more tha 16 words.\n" if len(password) > 16 else error_message
        error_message = error_message + "Your password has wrong words.\n" if check else error_message
        error_message = error_message + "Confirm password is not correct.\n" if password != confirm else error_message

        if error_message:
            QMessageBox.warning(self, '確認', error_message, QMessageBox.Yes, )
        else:
            self.client.insert({"_id": self.client.id + 1, "username": username, "password": password, "nickname": nickname, "email": email}, many=False)
            self.client.update({"_id": 0}, {"id_count": self.client.id + 1})
            self.sign_in()
            
    def forget_account(self):
        self.all_hide()
        self.left_frame.show()
        self.forget_frame.show()

    def main_search(self):
        self.islogin = True
        self.issignin = False
        self.issignup = False
        
        self.all_hide()
        self.main_search_frame.show()
        self.top_hot_frame.show()
        #self.show_TopHot()

    def store_check(self):
        if not self.select_store:
            self.reply = QMessageBox.warning(self,
                    '確認', 
                    '你必須至少選一間', 
                        QMessageBox.Yes, 
                        )
        else:
            self.search()

    def check_store(self, state):   # 勾選店家總數
        if state == Qt.Checked:
            self.select_store += 1
        else:
            self.select_store -= 1

    def show_L(self, store, i, num):

        self.topFiller = QWidget(self.search_result_frame)
        self.topFiller.setMinimumSize(1500, len(self.result_list[i]) * 650 / num)
        self.search_scroll = QScrollArea(self.search_result_frame)
        self.search_scroll.setWidget(self.topFiller)

        self.store_name_label = QLabel('Library',self.topFiller)
        self.store_name_label.setGeometry(20, 0, 200, 40)
        self.store_name_label.setFont(self.store_name_font)
        if num == 4:
            self.search_scroll.setGeometry(0, 0, 770, 360)
            num = 2
        else:
            self.search_scroll.setGeometry(1540 / num * i, 0, 1540 / num, 720)
        
        for n, book in enumerate(store):
            self.result_pic_label = QLabel(self.topFiller)
            if n == 0:
                self.result_pic_label.setGeometry(0, 50, 600 / num, 600 / num)
            else:
                self.result_pic_label.setGeometry(0, self.max_h  + 10, 600 / num, 600 / num)
            if book[1] != None:
                data = urllib.request.urlopen(book[1]).read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.result_pic_label.setPixmap(pixmap.scaled(600 / num, 600 / num, Qt.KeepAspectRatio, Qt.FastTransformation))
                self.result_booktitle_label = QLabel(book[0], self.topFiller)
            if n == 0:
                self.result_booktitle_label.setGeometry(500 / num + 20, 50, 1000, 20)
            else:
                self.result_booktitle_label.setGeometry(500 / num + 20, self.max_h  + 10, 1000, 20)
            
            self.result_booktitle_label.setFont(self.font)

            self.result_url_label = QLabel(f'<a href="{book[2]}">More</a>', self.topFiller)
            self.result_url_label.setOpenExternalLinks(True)
            if n == 0:
                self.result_url_label.setGeometry(500 / num + 20, 80, 1000, 20)
            else:
                self.result_url_label.setGeometry(500 / num + 20, self.max_h + 40, 1000, 20)

            self.result_url_label.setFont(self.font)

            self.result_booktype_label = QLabel(book[3], self.topFiller)
            if n == 0:
                self.result_booktype_label.setGeometry(500 / num + 20, 110, 1000, 20)
            else:
                self.result_booktype_label.setGeometry(500 / num + 20, self.max_h  + 70, 1000, 20)
            self.result_booktype_label.setFont(self.font)

            for i,v in enumerate(book[4]):
                if i <= 2:
                    string = ", ".join(v)
                    self.result_price_label = QLabel(string, self.topFiller)
                    if n == 0:
                        self.result_price_label.setGeometry(500 / num + 20, 140 + i * 20, 1000, 20)
                    else:
                        self.result_price_label.setGeometry(500 / num + 20, self.max_h + 100 + i * 20, 1000, 20)
                    self.result_price_label.setFont(self.font)
                elif i == 3:
                    self.result_price_label = QLabel(".\n.\n.\n.", self.topFiller)
                    if n == 0:
                        self.result_price_label.setGeometry(500 / num + 20+200, 140 + i * 20, 1000, 80)
                    else:
                        self.result_price_label.setGeometry(500 / num + 20+200, self.max_h + 100 + 4 * 20, 1000, 80)
                    self.result_price_label.setFont(self.font)
                    break

            self.max_h = self.result_pic_label.y()+self.result_pic_label.height()

    def show_B(self, store, i, num):     # data = [ [name, img, url, type, price], [], [] ]
        self.topFiller = QWidget(self.search_result_frame)
        self.topFiller.setMinimumSize(1500, len(self.result_list[i]) * 650 / num)
        self.search_scroll = QScrollArea(self.search_result_frame)
        self.search_scroll.setWidget(self.topFiller)

        self.max_h = 0

        if num == 4:
            self.search_scroll.setGeometry(770, 0, 770, 360)
            num = 2
        else:
            self.search_scroll.setGeometry(1540 / num * i, 0, 1540 / num, 720)

        self.store_name_label = QLabel('Books',self.topFiller)
        self.store_name_label.setGeometry(20, 0, 200, 40)
        self.store_name_label.setFont(self.store_name_font)
        for n, book in enumerate(store):
            self.result_pic_label = QLabel(self.topFiller)
            if n == 0:
                self.result_pic_label.setGeometry(0, 50, 600 / num, 600 / num)
            else:
                self.result_pic_label.setGeometry(0, self.max_h  + 10, 600 / num, 600 / num)
            data = urllib.request.urlopen(book[1]).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.result_pic_label.setPixmap(pixmap.scaled(600 / num, 600 / num, Qt.KeepAspectRatio, Qt.FastTransformation))
            self.result_booktitle_label = QLabel(book[0], self.topFiller)
            if n == 0:
                self.result_booktitle_label.setGeometry(500 / num + 20, 50, 1000, 20)
            else:
                self.result_booktitle_label.setGeometry(500 / num + 20, self.max_h  + 10, 1000, 20)
            
            self.result_booktitle_label.setFont(self.font)

            self.result_url_label = QLabel(f'<a href="{book[2]}">More</a>', self.topFiller)
            self.result_url_label.setOpenExternalLinks(True)
            if n == 0:
                self.result_url_label.setGeometry(500 / num + 20, 80, 1000, 20)
            else:
                self.result_url_label.setGeometry(500 / num + 20, self.max_h + 40, 1000, 20)

            self.result_url_label.setFont(self.font)

            self.result_booktype_label = QLabel(book[3], self.topFiller)
            if n == 0:
                self.result_booktype_label.setGeometry(500 / num + 20, 110, 1000, 20)
            else:
                self.result_booktype_label.setGeometry(500 / num + 20, self.max_h  + 70, 1000, 20)
            self.result_booktype_label.setFont(self.font)

            self.result_price_label = QLabel(book[4], self.topFiller)
            if n == 0:
                self.result_price_label.setGeometry(500 / num + 20, 140, 1000, 20)
            else:
                self.result_price_label.setGeometry(500 / num + 20, self.max_h  + 100, 1000, 20)
            self.result_price_label.setFont(self.font)

            self.max_h = self.result_pic_label.y()+self.result_pic_label.height()

    def show_E(self, store, i, num):
        self.topFiller = QWidget(self.search_result_frame)
        self.topFiller.setMinimumSize(1500, len(self.result_list[i]) * 650 / num)
        self.search_scroll = QScrollArea(self.search_result_frame)
        self.search_scroll.setWidget(self.topFiller)

        self.max_h = 0

        if num == 4:
            self.search_scroll.setGeometry(0, 360, 770, 360)
            num = 2
        else:
            self.search_scroll.setGeometry(1540 / num * i, 0, 1540 / num, 720)

        self.store_name_label = QLabel('Eslite',self.topFiller)
        self.store_name_label.setGeometry(20, 0, 200, 40)
        self.store_name_label.setFont(self.store_name_font)
        for n, book in enumerate(store):
            self.result_pic_label = QLabel(self.topFiller)
            if n == 0:
                self.result_pic_label.setGeometry(0, 50, 600 / num, 600 / num)
            else:
                self.result_pic_label.setGeometry(0, self.max_h + 10, 600 / num, 600 / num)
            data = urllib.request.urlopen(book[1]).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.result_pic_label.setPixmap(pixmap.scaled(600 / num, 600 / num, Qt.KeepAspectRatio, Qt.FastTransformation))
            self.result_booktitle_label = QLabel(book[0], self.topFiller)
            if n == 0:
                self.result_booktitle_label.setGeometry(500 / num + 20, 50, 1000, 20)
            else:
                self.result_booktitle_label.setGeometry(500 / num + 20, self.max_h  + 10, 1000, 20)
            self.result_booktitle_label.setFont(self.font)

            self.result_url_label = QLabel(f'<a href="{book[2]}">More</a>', self.topFiller)
            self.result_url_label.setOpenExternalLinks(True)
            if n == 0:
                self.result_url_label.setGeometry(500 / num + 20, 80, 1000, 20)
            else:
                self.result_url_label.setGeometry(500 / num + 20, self.max_h  + 40, 1000, 20)

            self.result_url_label.setFont(self.font)

            self.result_booktype_label = QLabel(book[3], self.topFiller)
            if n == 0:
                self.result_booktype_label.setGeometry(500 / num + 20, 110, 1000, 20)
            else:
                self.result_booktype_label.setGeometry(500 / num + 20, self.max_h  + 70, 1000, 20)
            self.result_booktype_label.setFont(self.font)

            self.result_price_label = QLabel(book[4], self.topFiller)
            if n == 0:
                self.result_price_label.setGeometry(500 / num + 20, 140, 1000, 20)
            else:
                self.result_price_label.setGeometry(500 / num + 20, self.max_h  + 100, 1000, 20)
            self.result_price_label.setFont(self.font)

            self.max_h = self.result_pic_label.y()+self.result_pic_label.height()

    def show_K(self, store, i, num):
        self.topFiller = QWidget(self.search_result_frame)
        self.topFiller.setMinimumSize(1500, len(self.result_list[i]) * 650 / num)
        self.search_scroll = QScrollArea(self.search_result_frame)
        self.search_scroll.setWidget(self.topFiller)

        self.max_h = 0

        if num == 4:
            self.search_scroll.setGeometry(770, 360, 770, 360)
            num = 2
        else:
            self.search_scroll.setGeometry(1540 / num * i, 0, 1540 / num, 720)

        self.store_name_label = QLabel('Kingstone',self.topFiller)
        self.store_name_label.setGeometry(20, 0, 200, 40)
        self.store_name_label.setFont(self.store_name_font)
        for n, book in enumerate(store):
            self.result_pic_label = QLabel(self.topFiller)
            if n == 0:
                self.result_pic_label.setGeometry(0, 50, 600 / num, 600 / num)
            else:
                self.result_pic_label.setGeometry(0, self.max_h  + 10, 600 / num, 600 / num)
            data = urllib.request.urlopen(book[1]).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.result_pic_label.setPixmap(pixmap.scaled(600 / num, 600 / num, Qt.KeepAspectRatio, Qt.FastTransformation))
            self.result_booktitle_label = QLabel(book[0], self.topFiller)
            if n == 0:
                self.result_booktitle_label.setGeometry(500 / num + 100, 50, 1000, 20)
            else:
                self.result_booktitle_label.setGeometry(500 / num + 100, self.max_h  + 10, 1000, 20)
            self.result_booktitle_label.setFont(self.font)

            self.result_url_label = QLabel(f'<a href="{book[2]}">More</a>', self.topFiller)
            self.result_url_label.setOpenExternalLinks(True)
            if n == 0:
                self.result_url_label.setGeometry(500 / num + 100, 80, 1000, 20)
            else:
                self.result_url_label.setGeometry(500 / num + 100, self.max_h  + 40, 1000, 20)

            self.result_url_label.setFont(self.font)

            self.result_booktype_label = QLabel(book[3], self.topFiller)
            if n == 0:
                self.result_booktype_label.setGeometry(500 / num + 100, 110, 1000, 20)
            else:
                self.result_booktype_label.setGeometry(500 / num + 100, self.max_h  + 70, 1000, 20)
            self.result_booktype_label.setFont(self.font)

            self.result_price_label = QLabel(book[4], self.topFiller)
            if n == 0:
                self.result_price_label.setGeometry(500 / num + 100, 140, 1000, 20)
            else:
                self.result_price_label.setGeometry(500 / num + 100, self.max_h  + 100, 1000, 20)
            self.result_price_label.setFont(self.font)

            self.max_h = self.result_pic_label.y()+self.result_pic_label.height()

    def clear(self, MyResourceFrame):
        for i in range(len(MyResourceFrame.children())):
            MyResourceFrame.children()[i].deleteLater()
            
    def search(self):
        search_text = self.search_edit.text().strip()

        self.all_hide()
        self.main_search_frame.show()
        self.book_store = []
        self.result_list = []

        self.clear(self.search_result_frame)

        if self.check_store1.isChecked():
            self.book_store.append("L")
            self.result_list.append(self.L.search(search_text))

        if self.check_store2.isChecked():
            self.book_store.append("B")
            self.result_list.append(self.B.search(search_text))

        if self.check_store3.isChecked():
            self.book_store.append("E")
            self.result_list.append(self.E.search(search_text))

        if self.check_store4.isChecked():
            self.book_store.append("K")
            self.result_list.append(self.K.search(search_text))

        search_store = "".join(self.book_store)
        self.client.append_history([search_text, search_store])
            
        for i, ele in enumerate(self.book_store):
            if ele == "L":
                self.show_L(self.result_list[i], i, self.select_store)

            if ele == "B":
                self.show_B(self.result_list[i], i, self.select_store)

            if ele == "E":
                self.show_E(self.result_list[i], i, self.select_store)

            if ele == "K":
                self.show_K(self.result_list[i], i, self.select_store)

        self.search_result_frame.show()

    def home(self):
        if self.islogin:
            self.main_search()
        else:
            self.reply = QMessageBox.warning(self,
                    '確認', 
                    '搞毛阿～你還沒登入呢?', 
                        QMessageBox.Yes, 
                        )

    def logout(self):
        if not self.islogin:
            self.reply = QMessageBox.warning(self,
                    '確認', 
                    '你還沒登入就要登出?', 
                        QMessageBox.Yes, 
                        )
        else:
            self.islogin = False
            self.main()

    def show_TopHot(self):
        string = ""
        B = self.B.top_hot()
        E = self.E.top_hot()
        K = self.K.top_hot()
        string += "<h3>Books</h3>"
        for x in B:
            string += f"<a href={x[1]}>{x[0]}</a><br>"
        string += "<h3>Eslite</h3>"
        for x in E:
            string += f"<a href={x[1]}>{x[0]}</a><br>"
        string += "<h3>Kingstone</h3>"
        for x in K:
            string += f"<a href={x[1]}>{x[0]}</a><br>"
        self.top_hot_font = QFont()
        self.top_hot_font.setPointSize(20)
        self.top_hot_lab.setFont(self.top_hot_font)
        self.top_hot_lab.setText(string)

    def show_History(self):
        self.history = self.client.show_history()
        self.all_hide()
        if len(self.history) >= 1:
            self.history_lab1.setText(str(self.history[0][0]+self.history[0][1]))
        if len(self.history) >= 2:
            self.history_lab2.setText(str(self.history[1][0]+self.history[1][1]))
        if len(self.history) >= 3:
            self.history_lab3.setText(str(self.history[2][0]+self.history[2][1]))
        if len(self.history) >= 4:
            self.history_lab4.setText(str(self.history[3][0]+self.history[3][1]))
        if len(self.history) >= 5:
            self.history_lab5.setText(str(self.history[4][0]+self.history[4][1]))

        self.main_search_frame.show()
        self.history_frame.show()
    
    def all_uncheck(self):
        self.check_store1.setChecked(False)
        self.check_store2.setChecked(False)
        self.check_store3.setChecked(False)
        self.check_store4.setChecked(False)

    def history_search(self, index):
        self.all_uncheck()
        self.search_edit.setText(self.history[index][0])
        for ele in self.history[index][1]:
            if ele == "L":
                self.check_store1.setChecked(True)
            if ele == "B":
                self.check_store2.setChecked(True)
            if ele == "E":
                self.check_store3.setChecked(True)
            if ele == "K":
                self.check_store4.setChecked(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
