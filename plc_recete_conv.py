import numpy as np
from pyModbusTCP import utils

recete_dict = (
    {0: [0, 100], 1: [800, 1000]},
    {0: [100, 200], 1: [1000, 1100]},
    {0: [200, 300], 1: [1100, 1200]},
    {0: [300, 400], 1: [1200, 1300]},
    {0: [400, 500], 1: [1300, 1400]},
    {0: [500, 600], 1: [1400, 1500]},
    {0: [600, 700], 1: [1500, 1600]},
    {0: [700, 800], 1: [1600, 1700]})

#

skala = 9.9
off_set = [0, 60, 120, 180, 240, 300, 360, 420]


def recete_dict_to_renk(dict_recete):
    """
    dict olarak verile receti alacak ve dizi döndürecek
    :param dict_recete:
    :return: renk_1, renk_2
    """
    sonuc = []
    for any_dict in recete_dict:
        temp_list = []
        for any_list in any_dict.values():
            for val in any_list:
                temp_list.append(val)
        sonuc.append(temp_list)
    return sonuc


def recete_skala(list_renk, list_offset, skala):
    """
    reçeteyi dizi olarak alıyor np.array yapıyor
    ve skala ve offset ile çarpıp np.array olrak sonuç döndürür
    :param list_renk:
    :param list_offset:
    :param skala:
    :return:
    """
    a = np.array(list_renk)
    sonuc = []
    i = 0
    for any_list in a:
        b = any_list * skala + list_offset[i] * skala
        c = b.tolist()
        sonuc.append(c)
        i += 1
    return sonuc


def recete_ikili_sirala(s_liste_renk):
    """
    recete değerlerine x0 stop ve x1 start olarak ekleyip mesafeye
    göre sıralama yapıyor
    sonuç formatı (x0, mesafe) yada (x1, mesafe olarak çıkıyor)
    :param s_liste_renk:
    :return:
    """
    i1 = 11
    i0 = 10
    temp   = []
    temp_1 = []
    temp_2 = []
    temp_3 = []
    temp_4 = []
    for any_list in s_liste_renk:
        c = 0
        for any in any_list:
            if c % 2 == 0:
                temp.append((i1, any))
                c += 1
            else:
                temp.append((i0, any))
                c += 1
        i1 += 10
        i0 += 10
    for any in temp:
        if any[0] in (10, 11, 20, 21):
            temp_1.append(any)
        if any[0] in (30, 31, 40, 41):
            temp_2.append(any)
        if any[0] in (50, 51, 60, 61):
            temp_3.append(any)
        if any[0] in (70, 71, 80, 81):
            temp_4.append(any)

    dtype = [('start', int), ('mesafe', float)]
    temp_np_arr_1 = np.array(temp_1, dtype=dtype)
    temp_np_arr_2 = np.array(temp_2, dtype=dtype)
    temp_np_arr_3 = np.array(temp_3, dtype=dtype)
    temp_np_arr_4 = np.array(temp_4, dtype=dtype)
    sonuc_1 = np.sort(temp_np_arr_1, order='mesafe')
    sonuc_2 = np.sort(temp_np_arr_2, order='mesafe')
    sonuc_3 = np.sort(temp_np_arr_3, order='mesafe')
    sonuc_4 = np.sort(temp_np_arr_4, order='mesafe')
    return sonuc_1, sonuc_2, sonuc_3, sonuc_4


def make_key_arr(ikili_dizi):
    """
    bu fonksiyon ikili dizileri alır ve plc için dizilein başlangıç ve sonu bulur
    yalnız bu float dizi int yapıldıktan sonra mı olmalı ??
    :param ikili_dizi:
    :return:
    """
    key_arr = []
    start = 0
    for any_list in ikili_dizi:
        key_arr.append(start)
        stop = start + len(any_list) - 1
        key_arr.append(stop)
        start = stop + 1
    return key_arr


class MakePlcArr():
    def __init__(self, dict_recete, list_offset, skala):
        self.dict_recete = dict_recete
        self.list_offset = list_offset
        self.skala = skala

    def convert_plc_arr(self):
        list_recete = self.recete_dict_to_list_renk(self.dict_recete)
        # print(list_recete)
        list_skaled_recete = self.recete_skala(list_recete, self.list_offset, self.skala)
        # print(list_skaled_recete)
        list_sorted_recete=self.recete_ikili_sirala(list_skaled_recete)
        # print(list_sorted_recete)
        key_arr = self.make_key_arr(list_sorted_recete)
        cylinder_arr, recete_plc_float = self.make_cylinder_recete(list_sorted_recete)
        print(key_arr)
        print(cylinder_arr)
        print(recete_plc_float)
        plc_arr_int = self.make_float_to_16_int_arr(recete_plc_float)
        print(plc_arr_int)
        return cylinder_arr, key_arr, plc_arr_int
    def recete_dict_to_list_renk(self, dict_recete):
        """
        dict olarak verile receti alacak ve dizi döndürecek
        :param dict_recete:
        :return: renk_1, renk_2
        """
        sonuc = []
        for any_dict in recete_dict:
            temp_list = []
            for any_list in any_dict.values():
                for val in any_list:
                    temp_list.append(val)
            sonuc.append(temp_list)
        return sonuc

    def recete_skala(self, list_renk, list_offset, skala):
        """
        reçeteyi dizi olarak alıyor np.array yapıyor
        ve skala ve offset ile çarpıp np.array olrak sonuç döndürür
        :param list_renk:
        :param list_offset:
        :param skala:
        :return:
        """
        a = np.array(list_renk)
        sonuc = []
        i = 0
        for any_list in a:
            b = any_list * skala + list_offset[i] * skala
            c = b.tolist()
            sonuc.append(c)
            i += 1
        return sonuc

    def recete_ikili_sirala(self, skaled_recete):
        """
        recete değerlerine x0 stop ve x1 start olarak ekleyip mesafeye
        göre sıralama yapıyor
        sonuç formatı (x0, mesafe) yada (x1, mesafe olarak çıkıyor)
        :param s_liste_renk:
        :return:
        """
        i1 = 11
        i0 = 10
        temp = []
        temp_1 = []
        temp_2 = []
        temp_3 = []
        temp_4 = []
        for any_list in skaled_recete:
            c = 0
            for any in any_list:
                if c % 2 == 0:
                    temp.append((i1, any))
                    c += 1
                else:
                    temp.append((i0, any))
                    c += 1
            i1 += 10
            i0 += 10
        for any in temp:
            if any[0] in (10, 11, 20, 21):
                temp_1.append(any)
            if any[0] in (30, 31, 40, 41):
                temp_2.append(any)
            if any[0] in (50, 51, 60, 61):
                temp_3.append(any)
            if any[0] in (70, 71, 80, 81):
                temp_4.append(any)

        dtype = [('start', int), ('mesafe', float)]
        temp_np_arr_1 = np.array(temp_1, dtype=dtype)
        temp_np_arr_2 = np.array(temp_2, dtype=dtype)
        temp_np_arr_3 = np.array(temp_3, dtype=dtype)
        temp_np_arr_4 = np.array(temp_4, dtype=dtype)
        sonuc_1 = np.sort(temp_np_arr_1, order='mesafe')
        sonuc_2 = np.sort(temp_np_arr_2, order='mesafe')
        sonuc_3 = np.sort(temp_np_arr_3, order='mesafe')
        sonuc_4 = np.sort(temp_np_arr_4, order='mesafe')
        return [sonuc_1, sonuc_2, sonuc_3, sonuc_4]

    def make_cylinder_recete(self, sorted_recete):
        cylinder_arr = []
        recete_pcl_float = []
        for any_list in sorted_recete:
            for any_item in any_list:
                cylinder_arr.append(any_item[0])
                recete_pcl_float.append(any_item[1])
        return cylinder_arr, recete_pcl_float

    def make_key_arr(self, sorted_recete):
        """
        bu fonksiyon ikili dizileri alır ve plc için dizilein başlangıç ve sonu bulur
        yalnız bu float dizi int yapıldıktan sonra mı olmalı ??
        :param ikili_dizi:
        :return:
        """
        key_arr = []
        start = 0
        for any_list in sorted_recete:
            key_arr.append(start)
            stop = start + len(any_list) - 1
            key_arr.append(stop)
            start = stop + 1
        return key_arr

    def make_float_to_16_int_arr(self, float_list):
        """
        float diziyi alıp int 16 şeklinde geri döndürür
        :param float_list:
        :return: list int16
        """
        s_dizi = []
        for a in float_list:
            c = utils.encode_ieee(a)
            x0, y0 = self.int32_to_int16(c)
            s_dizi.append(x0)
            s_dizi.append(y0)
        return s_dizi

    def int32_to_int16(self, n):
        """
        int32 yıl int 16 ya döndürür
        :param n: int32
        :return: list int16
        """
        mask = (1 << 16) - 1
        return [(n >> k) & mask for k in range(0, 32, 16)]


plc_arr = MakePlcArr(recete_dict, off_set, skala)
slindir_arr, key_arr, plc_arr_int = plc_arr.convert_plc_arr()

def find_pl(s_liste_renk, skala):
    """
    skalalanmış listeyi alır ve maks uzunluğu
    geri döndürür
    :param s_liste_renk:
    :return: pattern_length pl
    """
    pl = 0
    for any_list in s_liste_renk:
        temp_max_l = max(any_list)
        if temp_max_l > pl:
            pl = temp_max_l
    print("pattern length ", pl)
    return pl * skala

class BASKI():
    kafa_sozluk = {10: "sil 1 of", 11: "sil 1 on", 20: "sil 2 of", 21: "sil 2 on", 30: "sil 3 of", 31: "sil 3 on", 40: "sil 4 of", 41: "sil 4 on",
                   50: "sil 5 of", 51: "sil 5 on", 60: "sil 6 of", 61: "sil 6 on", 70: "sil 7 of", 71: "sil 7 on", 80: "sil 8 of", 81: "sil 8 on"}

    def __init__(self, recete, pl):
        self.recete = recete
        self.index = 0
        self.recete_sonu = len(recete)
        self.pl = pl

    def bas(self, hsc):
        if self.index >= self.recete_sonu:
            self.index = 0
        if hsc == self.recete[self.index][1]:
            self.sil_kont()
            eski_hedef = self.recete[self.index][1]
            yeni_hedef = self.recete[self.index][1] + self.pl
            self.recete[self.index][1] = yeni_hedef
            self.index += 1
            fw_ind = 0
            for i in range(self.index, self.recete_sonu):
                if eski_hedef == self.recete[i][1]:
                    yeni_hedef = self.recete[self.index][1] + self.pl
                    self.recete[i][1] = yeni_hedef
                    fw_ind += 1
            if fw_ind != 0:
                self.index = self.index + fw_ind

    def sil_kont(self):
        print(self.kafa_sozluk[self.recete[self.index][0]])

    def get_recete(self):
        return self.recete


# liste_renk = recete_dict_to_renk(recete_dict)
# skaled_recete = recete_skala(liste_renk, off_set, skala)
#
# sorted_recete, sorted_recete_1, sorted_recete_2, sorted_recete_3 = recete_ikili_sirala(skaled_recete)
# # recete_sonu = len(sorted_recete)
# print(sorted_recete)
# # pattern length bulunuyor
# pl = find_pl(liste_renk, skala)
# print("pl : ", pl)
# # pattern length listesi başlangış
#
# print("key_arr = ", make_key_arr(recete_ikili_sirala(skaled_recete)))

# index = 0
# index_1 = 0
# hsc = 0
# kafa_sozluk = {10: 0, 11: 0, 20: 1, 21: 1, 30: 2, 31: 2, 40: 3, 41: 3, 50: 4, 51: 4,
#                60: 5, 61: 5, 70: 6, 71: 6, 80: 7, 81: 7}
#
# kafa_0_1 = BASKI(sorted_recete, pl)
# kafa_2_3 = BASKI(sorted_recete_1, pl)
# kafa_4_5 = BASKI(sorted_recete_2, pl)
# kafa_6_7 = BASKI(sorted_recete_3, pl)
#
# while hsc < 8090:  # 00000:
#     kafa_0_1.bas(hsc)
#     kafa_2_3.bas(hsc)
#     kafa_4_5.bas(hsc)
#     kafa_6_7.bas(hsc)
#     hsc += 1
#
#
# print(kafa_0_1.get_recete())
# print(kafa_2_3.get_recete())
# print(kafa_4_5.get_recete())
# print(kafa_6_7.get_recete())

