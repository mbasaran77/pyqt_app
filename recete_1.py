


from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout, QWidget,QListWidget,QApplication,QPushButton,QLineEdit,QGridLayout,QDialog,QToolButton
import sys

import pickle
from pyModbusTCP import utils
mydict = {0: [100, 0], 1: [60, 1], 2: [20, 0], 3: [160, 1]}



den_list=[(0,10),(20,30),(50,85)]

class pop_up(QDialog):
    def __init__(self):
        super(pop_up, self).__init__()
        self.dolu_bos=0

        self.txt_1=QLineEdit()
        self.tool_b=QPushButton("Boş",self)
        self.btn_kayit=QPushButton("kayıt",self)
        self.btn_iptal=QPushButton("iptal",self)
        self.initUi()

        self.tool_b.clicked.connect(self.bos_dolu_sec)

    def initUi(self):
        lay_h_0=QHBoxLayout()
        lay_h_0.addWidget(self.txt_1)
        lay_h_0.addWidget(self.tool_b)

        lay_h_1=QHBoxLayout()
        lay_h_1.addWidget(self.btn_kayit)
        lay_h_1.addWidget(self.btn_iptal)

        lay_v_0=QVBoxLayout()
        lay_v_0.addItem(lay_h_0)
        lay_v_0.addItem(lay_h_1)
        self.setLayout(lay_v_0)

    def bos_dolu_sec(self):
        if self.dolu_bos==0:
            self.dolu_bos=1
            self.tool_b.setText("Dolu")
            return
        if self.dolu_bos == 1:
            self.dolu_bos = 0
            self.tool_b.setText("Boş")

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
        uzun=self.txt_bas.text()
        dolu_bos=self.txt_son.text()
        print("index",self.list_w_click_item()[0])
        self.desen.ekle(uzun,dolu_bos,self.list_w_click_item()[0])
        self.gun_liste()
    def list_w_click_item(self):
        index=self.list_w.currentRow()
        item=self.list_w.currentItem()
        print(index,item.text())
        return (index,item.text())


    def edit(self):
        f=pop_up()
        f.exec_()

        index, txt = self.list_w_click_item()
        self.desen.desen_uzat(index)
        #index,text=self.list_w_click_item()
        # self.desen.desen_kontrol()
        # print(index)
        self.gun_liste()


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
            uzun,dolu_bos=rec[i]
            txt= '{:<4}'.format(str(i))+ '{:<6}'.format(str(uzun)) +'{:<4}'.format(("dolu" if dolu_bos==1 else "bos"))
            self.list_w.addItem(txt)



class color_list():
        def __init__(self):
            self.my_dict = {}
            self.id = 0
            self.my_dict_r = {}

        def setDict(self, sdict):
            self.my_dict = sdict
            self.id = len(self.my_dict)

        def ekle(self,uzun, dolu_bos,list_id=0):
            #max_l=self.desen_kontrol()
            if list_id==0:
                self.my_dict[self.id] = [uzun, dolu_bos]
                self.id += 1
            else:
                self.desen_uzat(list_id)
                self.my_dict[list_id]=[uzun, dolu_bos]
                self.id=len(self.my_dict)


        def desen_uzat(self,list_id):
            d_key=self.my_dict.keys()
            d_len=len(self.my_dict)
            dict_r={}
            for i in range(d_len):
                dict_r[i]=self.my_dict[i]
            print(len(self.my_dict))
            if list_id in d_key:
                for i in range(list_id,d_len):
                    dict_r[i+1]=self.my_dict[i]
            print(dict_r,"len",len(dict_r))
            self.my_dict=dict_r

        def sil(self, id):
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



