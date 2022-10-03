import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog , QApplication , QWidget,QStackedWidget,QTabWidget,QVBoxLayout,QLabel,QTableWidget
import sqlite3





class WelcomeScreen(QDialog):

    
    def __init__(self ) :
        super(WelcomeScreen,self).__init__()
        loadUi("welcomescreen.ui",self)
        
        self.textSifre.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btnGiris.clicked.connect(self.loginfunction)
        self.btnKayitOl.clicked.connect(self.gotocreate)


    def gotocreate(self):
        kayıtol = createscreen()
        widget.addWidget(kayıtol)
        widget.setCurrentIndex(widget.currentIndex()+1)




    def loginfunction(self):
        user = self.textEposta.text()
        password = self.textSifre.text()



        if len(user)==0 or len(password)==0:
            self.lbl.setText("Lütfen giriş yapınız")
        
        else:
            conn = sqlite3.connect("KayıtlıKullanıcı.db")
            cur = conn.cursor()
            query = 'SELECT Şifre from Kullanıcı Where Email =\''+user+"\'"
            cur.execute(query)
            result_pass = cur.fetchone()[0]
            
            if result_pass == password :

                print('Başarılı giriş')
                mainwindow = mainwindowscreen()
                widget.addWidget(mainwindow)
                widget.setCurrentIndex(widget.currentIndex()+1)
                
                    
            else:
                self.lbl.setText("E-mail yada şifre yanlış")  


class createscreen(QDialog):
    def __init__(self ) :
        super(createscreen,self).__init__()
        loadUi("KayıtOl.ui",self)
        self.textSifre.setEchoMode(QtWidgets.QLineEdit.Password)
        self.textSifreTkr.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btnKayt.clicked.connect(self.gotowelcome)

    def gotowelcome(self):

        user = self.textad.text()
        lastname = self.textsoyad.text()
        password = self.textSifre.text()
        confirmpassword = self.textSifreTkr.text()
        e_mail = self.textemail.text()


        if len(user)==0 or len(lastname)==0 or len(password)==0 or len(confirmpassword)==0 or len(e_mail)==0:

            self.error.setText("Eksik Bilgi")
        
        elif password!=confirmpassword:
            self.error.setText("Şifreler aynı değil")
           
        else:
            
            conn1 = sqlite3.connect("KayıtlıKullanıcı.db")
            cur1 = conn1.cursor()
            
            user_info=[user,lastname,e_mail,password]
            query1 ='INSERT INTO Kullanıcı (Ad,Soyad,Email,Şifre) VALUES (?,?,?,?)'
            cur1.execute(query1,user_info)


            conn1.commit()
            conn1.close()

            
            win2 = WelcomeScreen()
            widget.addWidget(win2)
            widget.setCurrentIndex(widget.currentIndex()+1)



class mainwindowscreen(QDialog):
    def __init__(self) :
        super(mainwindowscreen,self).__init__()
        loadUi("MainWindow.ui",self)
        
        self.tableWidget.setColumnWidth(0,150)
        self.tableWidget.setColumnWidth(1,150)
        self.tableWidget.setColumnWidth(0,150)
        self.tableWidget.setHorizontalHeaderLabels(["Ad","Fiyat","Stok"])
        self.loaddata()
        self.btnAl.clicked.connect(self.btnal)
        self.btncikis.clicked.connect(self.exit)
        self.btnekle.clicked.connect(self.gotorn)
   
    def exit(self):
        log = WelcomeScreen()
        widget.addWidget(log)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotorn(self):
        win5 = ekle()
        widget.addWidget(win5)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def btnal(self):
        urunad = self.txturun.text()
        kactane = self.txtkac.text()
        con = sqlite3.connect("KayıtlıKullanıcı.db")
        cur = con.cursor()
        query1 = 'SELECT ad from Products '
        cur.execute(query1)
        
        result_urun = cur.fetchone()[0]
        print(result_urun)
        
        query = 'SELECT stok from Products Where ad =\''+urunad+"\'"
        cur2 = con.cursor()
        cur2.execute(query)
        result_stok = cur2.fetchone()[0]
        
       
        if result_urun==urunad or result_stok>kactane:
            print("başarılı")
            query2 = 'SELECT fiyat from Products Where ad =\''+urunad+"\'"
            cur3 =con.cursor()
            cur3.execute(query2)
            rsltfiyat = cur3.fetchone()[0]
            self.lblsonuc.setText("Ürün adı : " +urunad +"\n"+"adet : " + kactane +"\n"+"fiyat : "+rsltfiyat+"\n"+"Sipaşiş verildi.")
            rslt = int(result_stok) - int(kactane)
            reslt = str(rslt)
            sqlquery = 'UPDATE Products SET stok = \'' +reslt +"\'"'Where ad = \''+urunad+"\'"
            cur4 =con.cursor()
            cur4.execute(sqlquery)

            con.commit()
            con.close()

        else : 
            print("yanlış ürün ")

    def loaddata(self):

        conn = sqlite3.connect("KayıtlıKullanıcı.db")
        cur = conn.cursor()
        query = 'SELECT * FROM Products LIMIT 15'

        self.tableWidget.setRowCount(15)
        tablerow = 0

        for row in cur.execute(query):
            self.tableWidget.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[2]))
            tablerow+=1

    

class ekle(QDialog):
    def __init__(self ) :
        super(ekle,self).__init__()
        loadUi("Ekle.ui",self)
        
        self.btngeri.clicked.connect(self.gotogeri)
        self.btnexit.clicked.connect(self.gotoexit)
        self.btnonayla.clicked.connect(self.onayla)

    def gotogeri(self):
        mm = mainwindowscreen()
        widget.addWidget(mm)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoexit(self):
        win6 = ekle()
        widget.addWidget(win6)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.close()
        
    def onayla(self):

        rnad=self.txtad.text()
        rnfiyat=self.txtfiyat.text()
        rnstok=self.txtstok.text()

        con = sqlite3.connect("KayıtlıKullanıcı.db")
        cur = con.cursor()
        products_info=[rnad,rnfiyat,rnstok]
        query ='INSERT INTO Products (ad,fiyat,stok) VALUES (?,?,?)'
        cur.execute(query,products_info)
        con.commit()
        con.close()






app = QApplication(sys.argv)




win = WelcomeScreen()

widget = QStackedWidget()
widget.addWidget(win)
widget.setFixedHeight(581)
widget.setFixedWidth(701)
widget.setWindowIcon(QIcon("logo.png"))
widget.setWindowTitle("Bayi Ürün Satış")
widget.show()

    
try:
    sys.exit(app.exec_())
except:
    print("exiting.")