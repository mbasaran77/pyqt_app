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

liste_renk = recete_dict_to_renk(recete_dict)
print(liste_renk)

def recete_skala(list_renk, list_offset, skala):
    a = np.array(list_renk)
    sonuc = []
    i = 0
    for any_list in a:
        b = any_list * skala + list_offset[i] * skala
        print(b)
        c = b.tolist()
        sonuc.append(c)
        i += 1
    return sonuc
s = recete_skala(liste_renk, off_set, skala)
print(s)



def recete_sirala(s_liste_renk):
    a = np.array(s_liste_renk)
    print(a)
    b = a.flatten()
    d = b.tolist()
    e = d.sort()
    print(e)

recete_sirala(s)
