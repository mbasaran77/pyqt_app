

from PyQt5.QtWidgets import QDialog,QApplication
#from PyQt5.QtCore import QObject
from functools import partial
import sys
import keypadN


class keypadForm(QDialog,keypadN.Ui_Dialog):
    def __init__(self,f_obj):
        super(keypadForm, self).__init__()
        self.f_obj=f_obj
        self.setupUi(self)

        self.btn_list=[self.pushButton,self.pushButton_2,self.pushButton_3,self.pushButton_4,
                       self.pushButton_5,self.pushButton_6,self.pushButton_7,self.pushButton_8,
                       self.pushButton_9,self.pushButton_10,self.pushButton_11]
        self.girilenDeger=''
        self.onay=False
        self.my_tuple=(self.girilenDeger,self.onay)
        for obj in self.btn_list:
            #self.cmd=partial()
            obj.clicked.connect(self.degerGirise)

        self.pushButton_14.clicked.connect(self.onayDeger)
        self.pushButton_12.clicked.connect(self.close)
        self.pushButton_13.clicked.connect(self.degerSil)
        self.pushButton_15.clicked.connect(self.temizle)

    def degerGirise(self):
        sender=self.sender() #burada Qobject.sender() medtodu çağırılıyor sender=QObject.sender(self) ile aynı
        if sender.text()=='.' and '.' in self.girilenDeger:
            return
        self.girilenDeger+=sender.text()
        self.lineEdit.setText(self.girilenDeger)

        print(sender.text())
        print(self.girilenDeger)

    def onayDeger(self):
        if not (self.girilenDeger=='' or self.girilenDeger==None):
            self.onay=True
            self.my_tuple=(self.girilenDeger,self.onay)
            self.f_obj.setText(self.girilenDeger)
            self.close()

    def degerSil(self):
        kardiz=self.girilenDeger
        if len(kardiz)!=0:
            a=len(kardiz)-1
            self.girilenDeger=kardiz[:a]
            self.lineEdit.setText(self.girilenDeger)

    def temizle(self):
        self.girilenDeger=''
        self.lineEdit.setText('')

    def degerAl(self):
        return self.my_tuple


if __name__ == '__main__':
    app=QApplication(sys.argv)
    # hata yakalama için ilave edildi
    sys._excepthook = sys.excepthook


    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print("program hatalar", exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook

    f=keypadForm()
    f.show()
    sys.exit(app.exec_())