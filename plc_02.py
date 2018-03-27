import numpy as np

recete_dict = (
    {0: [0, 100], 1: [800, 1000]},
    {0: [100, 200], 1: [1000, 1100]},
    {0: [200, 300], 1: [1100, 1200]},
    {0: [300, 400], 1: [1200, 1300]},
    {0: [400, 500], 1: [1300, 1400]},
    {0: [500, 600], 1: [1400, 1500]},
    {0: [600, 700], 1: [1500, 1600]},
    {0: [700, 800], 1: [1600, 1700]})



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


def find_pl(s_liste_renk):
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
    return pl


def init_pl(pl, list_offset, skala):
    list_pl = []
    for i in range(8):
        list_pl.append(pl + list_offset[i] * skala)
    return list_pl


kafa_sozluk = {10: 0, 11: 0, 20: 1, 21: 1, 30: 2, 31: 2, 40: 3, 41: 3, 50: 4, 51: 4,
               60: 5, 61: 5, 70: 6, 71: 6, 80: 7, 81: 7}


def hedef_hesap(mesafe, kafa, pl, tur,  offset_list, skala):
    sonuc = mesafe * skala + pl * tur * skala + offset_list[kafa] * skala
    return sonuc



liste_renk = recete_dict_to_renk(recete_dict)

print(recete_skala(liste_renk, off_set, skala))

# pattern length bulunuyor
# pl = find_pl(skaled_recete)
# pattern length listesi başlangış
# list_pl = init_pl(pl, off_set, skala)
# print(list_pl)

index = 0
hsc = 0
kafa_sozluk = {10: 0, 11: 0, 20: 1, 21: 1, 30: 2, 31: 2, 40: 3, 41: 3, 50: 4, 51: 4,
               60: 5, 61: 5, 70: 6, 71: 6, 80: 7, 81: 7}


def hsc_run(recete):
    renk_0, renk_1, renk_2, renk_03, renk_4, renk_5, renk_6, renk_7 = recete
    hsc = 0
    p_sayac = [0, 0, 0, 0, 0, 0, 0, 0]
    while hsc < 1:  # 00000:



        hsc += 1

    print(hsc)
    print(recete)

