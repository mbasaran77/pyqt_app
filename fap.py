

from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QApplication,QLineEdit,QDialog
from PyQt5.QtGui import  QDoubleValidator,QValidator,QIntValidator
from PyQt5.Qt import *

import keypad_Mdl
import sys

__name__ ='__main__'

class Form(QDialog):

    def __init__(self):
        super(Form, self).__init__()


        btn=QPushButton("deneme",self)
        btn.move(50,60)
        self.lbl=QLabel("mehmet    ",self)
        btn.clicked.connect(self.deneme)
        self.lbl.move(50,90)

        self.txtBox=QLineEdit(self)
        self.txtBox.move(50,5)
        self.txtBox.installEventFilter(self)


        self.floatValidator=QDoubleValidator(0.00,1000.00,2)
        self.floatValidator.setNotation(QDoubleValidator.StandardNotation)
        self.txtBox.setValidator(self.floatValidator)

        self.intValidator=QIntValidator(0,1000)


        self.txtBox_1=QLineEdit(self)
        self.txtBox_1.move(50,30)
        self.txtBox_1.installEventFilter(self)


        self.txtBox_2=QLineEdit(self)
        self.txtBox_2.move(50,110)
        self.txtBox_2.setValidator(self.intValidator)
        self.txtBox_2.textChanged.connect(self.degerKontrol)

        self.dgBool=False

    def eventFilter(self, QObject, QEvent):
        if QEvent.type()==QEvent.FocusIn and self.dgBool==False:
            print(QObject)
            print(QEvent)
            self.dgBool=True
            self.showKeyP(QObject)
        return False

    def focusOutEvent(self, QFocusEvent):
        print(QFocusEvent)
        pass



    def deneme(self):
        self.txtBox_2.setText("15000")
        self.lbl.setText("ne haber")

    def showKeyP(self,obj):
        f=keypad_Mdl.keypadForm(obj)
        f.exec_()
        self.dgBool=False
        print(self.dgBool)

    def degerKontrol(self):
        print("deger kontrol")
        ch=checkIsFloat(self.txtBox_2.text(),self.intValidator)
        a=ch.checkText()
        print("sonuç :",a)

class  checkIsFloat():
    def __init__(self,text,validator):
        self.text=text
        self.validator=validator


    def checkText(self):
        text=self.text
        state = self.validator.validate(self.text, 0)[0]
        if "," in text:
            return (False,"virgül yerine nokta kullanılmalı")
        elif state ==QValidator.Intermediate:
            return (False,"girilen desen boyu belirlenen aralıkta değil")
        else:
            return (True,"başarılı")

if __name__ == '__main__':
    app=QApplication(sys.argv)

    sys._excepthook = sys.excepthook
    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook
    form=Form()
    form.show()
    try:
        sys.exit(app.exec_())
    except:
        pass
        # print("Exiting")

