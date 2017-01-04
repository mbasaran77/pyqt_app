


import pickle
from pyModbusTCP import utils

class color_list(object):
    def __init__(self):
        self.my_dict={}
        self._id=0
        self._bas=0
        self._bit=0
        self._color="renk1"
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
