
from PyQt5.QtWidgets import QWidget,QListWidget,QApplication,QPushButton,QLineEdit,QGridLayout,QDialog
import sys

import pickle
from pyModbusTCP import utils
mydict = {0: [0, 50], 1: [60, 80], 2: [120, 150], 3: [160, 200]}



den_list=[(0,10),(20,30),(50,85)]


class recete_list(QDialog):
    def __init__(self,color="Renk"):
        super(recete_list, self).__init__()
        self.color=color
        self.color="Renk 1"
        self.list_w_index=0
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
        self.desen.ekle(bas,bit)
        self.gun_liste()

    def list_w_click_item(self):
        index=self.list_w.currentRow()
        a=self.desen.my_dict[index]
        self.txt_bas.setText(str(a[0]))
        self.txt_son.setText(str(a[1]))
        self.list_w_index=index


    def edit(self):
        max_l=self.desen.desen_kontrol()

        self.desen.duzenle(self.list_w_index, self.txt_bas.text(),self.txt_son.text())
        self.gun_liste()


    def sil(self):
        index=self.list_w_index
        self.desen.kaldir(index)
        self.gun_liste()

    def gun_liste(self):
        self.desen.desen_sirala()
        self.list_w.clear()
        rec=self.desen.recete()
        print("---------------------------------------")
        print(rec)


        for i in range(len(rec)):
            bas, son = rec[i]
            txt = 'satır {:<4}'.format(str(i)) + '{:<6}'.format(str(bas)) + '{:<4}'.format(str(son))
            self.list_w.addItem(txt)


class color_list():
        def __init__(self):
            self.my_dict = {}
            self.id = 0
            self.my_dict_r = {}

        def setDict(self, sdict):
            self.my_dict = sdict
            self.id = len(self.my_dict)

        def ekle(self, bas, bit):
            max_l=self.desen_kontrol()
            if max_l==0 or int(bas)>=max_l:
                self.my_dict[self.id] = [bas, bit]
                self.id += 1
            elif int(bit)<max_l:
                self.desen_uzat(bas,bit)
                self.my_dict[self.id] = [bas, bit]
                self.id += 1

        def desen_uzat(self,bas,bit,index=None):
            fark=int(bit)-int(bas)
            if index==None: #index yoksa uzatma işlemi direk ekle için geçerli
                for a in self.my_dict:
                    bas_r, son_r = self.my_dict[a]
                    if int(bas_r)>=int(bas):
                        x,y=(int(bas_r)+fark),((int(son_r)+fark))
                        self.my_dict[a]=[x,y]
            else: #index varsa uzatma veya kısatma işlemi
                b_r,s_r=self.my_dict[index]
                fark=fark-(s_r-b_r)
                if fark>0:
                    for a in range(index,len(self.my_dict)):
                        bas_r, son_r = self.my_dict[a]
                        x, y = (int(bas_r) + fark), ((int(son_r) + fark))
                        self.my_dict[a] = [x, y]
                elif fark<0: #fark eksiyse kısaltma gerekli demektir
                    for a in range(index,len(self.my_dict)):
                        bas_r, son_r = self.my_dict[a]
                        x, y = (int(bas_r) + fark), ((int(son_r) + fark))
                        self.my_dict[a] = [x, y]
        def desen_kisalt(self):
            pass

        def desen_sirala(self):
            list_sort=[]
            for a in self.my_dict:
                bas,son=self.my_dict[a]
                list_sort.append([int(bas),int(son)])
            list_sort.sort()
            for i in range(len(list_sort)):
                self.my_dict[i]=list_sort[i]

            print("sıralı liste ",list_sort)

                #burada siralama yapılacak
        def duzenle(self,index,bas,son):
            bas_r,son_r=self.my_dict[index]
            self.desen_uzat(bas, son, index)
            self.my_dict[index] = [bas, son]

            # if int(son)>int(son_r):
            #     self.desen_uzat(bas,son,index)
            #     self.my_dict[index]=[bas,son]
            # else:
            #     self.my_dict[index] = [bas, son]

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
                    bas,son=self.my_dict[a]
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



