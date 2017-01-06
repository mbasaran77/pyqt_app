
from PyQt5.QtWidgets import QWidget,QListWidget,QApplication,QPushButton,QLineEdit,QGridLayout,QDialog
import sys

import pickle
from pyModbusTCP import utils
mydict = {0: ['renk 1', 0, 50], 1: ['renk 1', 60, 80], 2: ['renk 1', 120, 150], 3: ['renk 1', 160, 200]}



den_list=[(0,10),(20,30),(50,85)]


class recete_list(QDialog):
    def __init__(self,color="Renk"):
        super(recete_list, self).__init__()
        self.color=color
        self.color="Renk 1"
        self.list_w=QListWidget(self)
        self.btn_ekle=QPushButton("ekle",self)
        self.btn_sil=QPushButton("sil",self)
        self.btn_edit=QPushButton("edit",self)

        self.txt_bas=QLineEdit(self)
        self.txt_son=QLineEdit(self)

        self.btn_ekle.clicked.connect(self.ekle)
        self.btn_sil.clicked.connect(self.sil)
        self.btn_edit.clicked.connect(self.edit)
        self.list_w.itemClicked.connect(self.list_w_click_item)

        self.initUi()

        #recete oluşturma

        self.desen=color_list()
        self.desen.setDict(mydict)
        self.gun_liste()


    def initUi(self):
        self.resize(260,400)
        lay_o_1=QGridLayout()
        lay_o_1.addWidget(self.txt_bas,0,0)
        lay_o_1.addWidget(self.txt_son, 0, 1)
        lay_o_1.addWidget(self.list_w, 1, 0)
        lay_o_1.addWidget(self.btn_edit,1,1)
        lay_o_1.addWidget(self.btn_ekle, 2, 0)
        lay_o_1.addWidget(self.btn_sil, 2, 1)
        self.setLayout(lay_o_1)

    def ekle(self):
        bas=self.txt_bas.text()
        bit=self.txt_son.text()
        self.desen.ekle(self.color,bas,bit)
        self.gun_liste()
    def list_w_click_item(self):
        index=self.list_w.currentRow()
        item=self.list_w.currentItem()
        print(index,item.text())
        return (index,item.text())


    def edit(self):
        index,text=self.list_w_click_item()
        self.desen.desen_kontrol()
        print(index)


        pass

    def sil(self):
        index,text=self.list_w_click_item()
        self.desen.kaldir(index)
        self.gun_liste()

    def gun_liste(self):
        self.list_w.clear()
        rec=self.desen.recete()
        print("---------------------------------------")
        print(rec)


        for i in range(len(rec)):
            txt=str(rec[i])
            self.list_w.addItem(txt)



class color_list():
        def __init__(self):
            self.my_dict = {}
            self.id = 0
            self.my_dict_r = {}

        def setDict(self, sdict):
            self.my_dict = sdict
            self.id = len(self.my_dict)

        def ekle(self, color, bas, bit):
            max_l=self.desen_kontrol()
            if max_l==0 or int(bas)>=max_l:
                self.my_dict[self.id] = [color, bas, bit]
                self.id += 1
            elif int(bit)<max_l:
                self.desen_uzat(color,bas,bit)
                self.my_dict[self.id] = [color, bas, bit]
                self.id += 1

        def desen_uzat(self,color,bas,bit):
            fark=int(bit)-int(bas)
            for a in self.my_dict:
                renk, bas_r, son_r = self.my_dict[a]
                if int(bas_r)>=int(bas):
                    x,y=(int(bas_r)+fark),((int(son_r)+fark))
                    self.my_dict[a]=[renk,x,y]
        def desen_sirala(self):
            for a in self.my_dict:
                renk,bas,son=self.my_dict[a]
                #burada siralama yapılacak


        def kaldir(self, id):
            if len(self.my_dict) >= 1:
                self.id -= 1
            self.my_dict.pop(id)

            a = 0
            i = 0
            c = len(self.my_dict)
            for i in range(len(self.my_dict) + 1):
                try:
                    self.my_dict_r[a] = self.my_dict[i]
                    a += 1
                except KeyError:
                    pass
            i = 0
            a = 0
            self.my_dict.clear()
            for i in range(len(self.my_dict_r) + 1):
                try:
                    self.my_dict[a] = self.my_dict_r[i]
                    a += 1
                except KeyError:
                    pass
            # print("my_dic_r ",self.my_dict_r)
            self.my_dict_r.clear()

        def desen_kontrol(self):
            if len(self.my_dict)>0:
                max_l =0
                for a in range(len(self.my_dict)):
                    renk,bas,son=self.my_dict[a]
                    if max_l<=int(son):
                        max_l=int(son)
            else:
                max_l=0

            return max_l




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



