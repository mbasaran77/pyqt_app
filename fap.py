

from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QApplication,QLineEdit,QDialog
from PyQt5.QtGui import  QDoubleValidator
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


        self.floatValidator=QDoubleValidator(0.00,10000.00,2)
        self.floatValidator.setNotation(QDoubleValidator.StandardNotation)
        self.txtBox.setValidator(self.floatValidator)


        self.txtBox_1=QLineEdit(self)
        self.txtBox_1.move(50,30)
        self.txtBox_1.installEventFilter(self)

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
        self.lbl.setText("ne haber")

    def showKeyP(self,obj):
        f=keypad_Mdl.keypadForm(obj)
        f.exec_()
        self.dgBool=False
        print(self.dgBool)

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

