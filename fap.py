

from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QApplication,QLineEdit,QDialog
from PyQt5.QtGui import  QFocusEvent
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import *
import keypad_Mdl
import sys

__name__ ='__main__'

class Form(QDialog):

    def __init__(self):
        super(Form, self).__init__()

        btn=QPushButton("deneme",self)
        btn.move(50,50)
        self.lbl=QLabel("mehmet    ",self)
        btn.clicked.connect(self.deneme)
        self.lbl.move(50,80)

        self.txtBox=QLineEdit(self)
        self.txtBox.installEventFilter(self)
        self.dgBool=False

    def eventFilter(self, QObject, QEvent):
        if QEvent.type()==QEvent.FocusIn and self.dgBool==False:
            print(QObject)
            print(QEvent)
            self.dgBool=True
            self.showKeyP()
        return False
            #if QEvent=

    def deneme(self):
        self.lbl.setText("ne haber")

    def showKeyP(self):
        f=keypad_Mdl.keypadForm()
        f.exec_()
        self.dgBool=False
        a=f.degerAl()
        if a[1]==True:
            self.txtBox.setText(a[0])

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

