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


def recete_sirala(s_liste_renk):
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
    dtype = [('start', int), ('mesafe', float)]
    temp_np_arr = np.array(temp, dtype=dtype)
    sonuc = np.sort(temp_np_arr, order='mesafe')
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


def hedef_guncelle(mesafe, kafa, list_pl):
    # kafa_sozluk = {10: 0, 11: 0, 20: 1, 21: 1, 30: 2, 31: 2, 40: 3, 41: 3, 50: 4, 51: 4,
    #                60: 5, 61: 5, 70: 6, 71: 6, 80: 7, 81: 7}
    print("pl : ", list_pl[kafa_sozluk[kafa]])
    hedef = mesafe + list_pl[kafa_sozluk[kafa]]
    return hedef


def get_01head(sorted_recete ):
    sonuc = []
    for any in sorted_recete:
       if any[0] in (10, 11):
           sonuc.append(any)
    return sonuc

liste_renk = recete_dict_to_renk(recete_dict)
skaled_recete = recete_skala(liste_renk, off_set, skala)
print(skaled_recete)
sorted_recete = recete_sirala(skaled_recete)
print(get_01head(sorted_recete))

# pattern length bulunuyor
pl = find_pl(skaled_recete)
# pattern length listesi başlangış
list_pl = init_pl(pl, off_set, skala)
print(list_pl)

index = 0
hsc = 0
kafa_sozluk = {10: 0, 11: 0, 20: 1, 21: 1, 30: 2, 31: 2, 40: 3, 41: 3, 50: 4, 51: 4,
               60: 5, 61: 5, 70: 6, 71: 6, 80: 7, 81: 7}


def hsc_run(recete):
    hsc = 0
    index = 0
    recete_sonu = len(recete)
    basma_count = [0, 0, 0, 0]
    while hsc < 2200000:  # 00000:
        if index >= recete_sonu:
            index = 0
            print("sıfırlandı")
        if hsc == recete[index][1]:
            print("index : ", index)
            print(recete[index][0])
            print(recete[index][1])
            eski_hedef = recete[index][1]
            yeni_hedef = hedef_guncelle(recete[index][1], recete[index][0], list_pl)
            recete[index][1] = yeni_hedef
            print(recete[index][1])
            if recete[index][0] == 11:
                basma_count[0] = basma_count[0] + 1
            elif recete[index][0] == 10:
                basma_count[1] = basma_count[1] + 1
            elif recete[index][0] == 20:
                basma_count[2] = basma_count[2] + 1
            elif recete[index][0] == 21:
                basma_count[3] = basma_count[3] + 1


            index += 1
            fw_ind = 0
            for i in range(index, recete_sonu):
                if eski_hedef == recete[i][1]:
                    print("eşitlik",eski_hedef, recete[i][1]  )
                    yeni_hedef = hedef_guncelle(recete[i][1], recete[i][0], list_pl)
                    recete[i][1] = yeni_hedef
                    fw_ind += 1
            if fw_ind != 0:
                index = index + fw_ind
        hsc += 1

    print(hsc)
    print(recete)
    print(basma_count)

hsc_run(get_01head(sorted_recete))