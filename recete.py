
from PyQt5.QtWidgets import QWidget,QListWidget,QApplication,QPushButton,QLineEdit,QGridLayout,QDialog
import sys

import pickle
from pyModbusTCP import utils


class recete_list(QDialog):
    def __init__(self,color="Renk"):
        super(recete_list, self).__init__()
        self.color=color
        self.color="Renk 1"
        self.list_w=QListWidget(self)
        self.btn_ekle=QPushButton("ekle",self)
        self.btn_sil=QPushButton("sil",self)
        self.txt_bas=QLineEdit(self)
        self.txt_son=QLineEdit(self)

        self.btn_ekle.clicked.connect(self.ekle)
        self.btn_sil.clicked.connect(self.sil)
        self.initUi()

        #recete oluşturma
        self.desen=color_list(self.color)


    def initUi(self):
        self.resize(260,400)
        lay_o_1=QGridLayout()
        lay_o_1.addWidget(self.txt_bas,0,0)
        lay_o_1.addWidget(self.txt_son, 0, 1)
        lay_o_1.addWidget(self.list_w, 1, 0)
        lay_o_1.addWidget(self.btn_ekle, 2, 0)
        lay_o_1.addWidget(self.btn_sil, 2, 1)
        self.setLayout(lay_o_1)

    def ekle(self):
        bas=self.txt_bas.text()
        bit=self.txt_son.text()
        self.desen.ekle(self.color,bas,bit)
        self.gun_liste()

    def sil(self):
        pass

    def gun_liste(self):
        self.list_w.clear()
        rec=self.desen.recete()
        for i in range(len(rec)):
            txt=str(rec[i])
            print(txt)
            self.list_w.addItem(txt)
            print(rec[i])



class color_list(object):
    def __init__(self,color):
        self.my_dict={}
        self._id=0
        self._bas=0
        self._bit=0
        self._color=color
        self.my_dict_r={}
    def setDict(self,sdict):
        self.my_dict=sdict
        self._id=len(self.my_dict)

    def ekle(self,color,bas,bit):
        self.my_dict[self._id]=[color,bas,bit]
        self._id+=1


    def kaldir(self, id):
        if len(self.my_dict)>=1:
            self._id -= 1
        self.my_dict.pop(id)

        a=0
        i=0
        c=len(self.my_dict)
        for i in range(len(self.my_dict)+1):
            try:
                self.my_dict_r[a]=self.my_dict[i]
                a+=1
            except KeyError:
                pass
        i=0
        a=0
        self.my_dict.clear()
        for i in range(len(self.my_dict_r)+1):
           try:
               self.my_dict[a]=self.my_dict_r[i]
               a+=1
           except KeyError:
                pass
        # print("my_dic_r ",self.my_dict_r)
        self.my_dict_r.clear()


    def yazdir(self):
        pass
        # print("mydict  ",self.my_dict)

    def recete(self):
        return self.my_dict



class dosyakayit(object):
    # def __init__(self,mydict):
    #     self.mydict=mydict

    def kayit(self,mydict,dosya):
        _mydict=mydict
        _dosya=str(dosya)+".txt"
        with open(_dosya,'wb') as fh:
            pickle.dump(_mydict, fh)

    def oku(self,dosya):
        _dosya=dosya
        with open(_dosya,'rb') as fh:
            oku_dict=pickle.load(fh)
            return oku_dict


mydict = {0: ['renk1', 0, 500], 1: ['renk2', 50, 80], 2: ['renk3', 80, 120], 3: ['renk4', 120, 180],
          4: ['renk5', 180, 220], 5: ['renk6', 220, 350],
          6: ['renk1', 500, 900], 7: ['renk2', 90, 110], 8: ['renk3', 134, 560], 9: ['renk4', 455, 567],
          10: ['renk5', 230, 420], 11: ['renk6', 304, 405], 11: ['renk1', 1000, 1200]}

my_recete_dict = {0: ['Renk 1', '100.00', '250.4'], 1: ['Renk 2', '250.04', '500.00'],
                  2: ['Renk 3', '500.00', '650.05'], 3: ['Renk 4', '650.05', '700'],
                  4: ['Renk 1', '0.00', '50.00'], 5: ['Renk 2', '50', '200']}



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
    f = recete_list()
    f.show()

    try:
        sys.exit(app.exec_())
    except:
        pass



