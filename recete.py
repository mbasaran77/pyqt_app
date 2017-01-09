
from PyQt5.QtWidgets import QMessageBox, QSizePolicy, QSpacerItem, QWidget,QListWidget,QApplication,QPushButton,QLineEdit,QGridLayout,QDialog,QVBoxLayout
from PyQt5.QtGui import QFont, QIntValidator
import sys

import pickle
from pyModbusTCP import utils
mydict = {0: [0, 50], 1: [60, 80], 2: [120, 150], 3: [160, 200]}



den_list=[(0,10),(20,30),(50,85)]


class recete_list(QWidget):
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
        self.intValidator = QIntValidator(0, 100000)
        self.txt_bas.setValidator(self.intValidator)
        self.txt_son.setValidator(self.intValidator)
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
        self.resize(210,400)
        my_font = QFont("Times", 14, QFont.Normal)
        my_font_k = QFont("Times", 10, QFont.Normal)
        self.txt_bas.setFont(my_font)
        self.txt_bas.setMinimumSize(80,30)
        self.txt_son.setFont(my_font)
        self.txt_son.setMinimumSize(80,30)
        self.btn_ekle.setFont(my_font)
        self.btn_ekle.setMinimumSize(80,40)
        self.btn_sil.setFont(my_font)
        self.btn_sil.setMinimumSize(80,40)
        self.btn_edit.setFont(my_font)
        self.btn_edit.setMinimumSize(80,40)

        vertSpacer=QSpacerItem(10,20,QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)

        lay_o_1=QGridLayout()
        lay_v_0=QVBoxLayout()
        lay_o_1.addWidget(self.txt_bas,0,0)
        lay_o_1.addItem(vertSpacer,0,1)
        lay_o_1.addWidget(self.txt_son, 0, 2)

        lay_o_1.addWidget(self.btn_ekle, 1, 0)
        lay_o_1.addItem(vertSpacer,1,0)
        lay_o_1.addWidget(self.btn_sil, 1, 2)

        lay_v_0.addWidget(self.list_w)
        lay_v_0.addWidget(self.btn_edit)
        lay_v_0.addItem(lay_o_1)

        self.setLayout(lay_v_0)

    def ekle(self):
        if self.giris_kontrol():
            bas=int(self.txt_bas.text())
            bit=int(self.txt_son.text())
            self.desen.ekle(bas,bit)
            self.giris_temizle()
            self.gun_liste()

    def list_w_click_item(self):
        index=self.list_w.currentRow()
        a=self.desen.my_dict[index]
        self.txt_bas.setText(str(a[0]))
        self.txt_son.setText(str(a[1]))
        self.list_w_index=index

    def giris_kontrol(self):
        if self.txt_bas.text() == "" or self.txt_son.text() == "":
            QMessageBox.warning(self, "reçete giriş", "seçim veya giriş yapılmadı")
            return False
        else:
            return True
    def giris_temizle(self):
        self.txt_bas.setText("")
        self.txt_son.setText("")


    def edit(self):
        if self.giris_kontrol():
            max_l=self.desen.desen_max_uzunluk_bul()
            self.desen.duzenle(self.list_w_index, int(self.txt_bas.text()),int(self.txt_son.text()))
            self.giris_temizle()
            self.gun_liste()


    def sil(self):
        if self.giris_kontrol():
            index=self.list_w_index
            self.desen.kaldir(index)
            self.giris_temizle()
            self.gun_liste()

    def gun_liste(self):
        self.desen.desen_sirala()
        self.list_w.clear()
        rec=self.desen.recete()

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
            cak_kontrol=self.desen_cakisma_kontrol(bas,bit)
            if cak_kontrol:
                max_l=self.desen_max_uzunluk_bul()
                if max_l==0 or bas>=max_l:
                    self.my_dict[self.id] = [bas, bit]
                    self.id += 1
                elif bit<max_l:
                    self.desen_uzat(bas,bit)
                    self.my_dict[self.id] = [bas, bit]
                    self.id += 1

        def desen_uzat(self,bas,bit,index=None):
            girilen_uzun=bit-bas
            if index==None: #index yoksa uzatma işlemi direk ekle için geçerli
                for a in self.my_dict:
                    bas_r, son_r = self.my_dict[a]
                    if bas_r>=bas:
                        x,y=((bas_r+girilen_uzun),(son_r+girilen_uzun))
                        self.my_dict[a]=[x,y]
            else: #index varsa uzatma veya kısatma işlemi
                b_r,s_r=self.my_dict[index]
                desen_uzunluk=s_r-b_r
                #fark=girilen_uzun-(desen_uzunluk)
                fark=bit-(s_r)
                if fark>0:
                    for a in range(index,len(self.my_dict)):
                        bas_r, son_r = self.my_dict[a]
                        x, y = ((bas_r + fark), (son_r + fark))
                        self.my_dict[a] = [x, y]
                elif fark<0: #fark eksiyse kısaltma gerekli demektir
                    for a in range(index,len(self.my_dict)):
                        bas_r, son_r = self.my_dict[a]
                        x, y = ((bas_r + fark), (son_r + fark))
                        self.my_dict[a] = [x, y]
                elif fark==0:
                    pass

        def desen_sirala(self):
            list_sort=[]
            for a in self.my_dict:
                bas,son=self.my_dict[a]
                list_sort.append([bas,son])
            list_sort.sort()
            for i in range(len(list_sort)):
                self.my_dict[i]=list_sort[i]

        def duzenle(self,index,bas,son):
            bas_r,son_r=self.my_dict[index]
            self.desen_uzat(bas, son, index)
            self.my_dict[index] = [bas, son]

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

        def desen_cakisma_kontrol(self,bas,son):
            for i in self.my_dict:
                b,s=self.my_dict[i]
                if b<=bas and s>=son:
                    return False
            else:
                return True

        def desen_max_uzunluk_bul(self):
            if len(self.my_dict)>0:
                max_l =0
                for a in range(len(self.my_dict)):
                    bas,son=self.my_dict[a]
                    if max_l<=son:
                        max_l=son
            else:
                max_l=0

            return max_l

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



