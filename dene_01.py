import numpy as np


recete = [(11,     0.), (10,   990.), (21,  1584.), (20,  2574.), (31,  3168.),
 (30,  4158.), (41,  4752.), (40,  5742.), (51,  6336.), (50,  7326.),
 (11,  7920.), (61,  7920.), (60,  8910.), (71,  9504.), (10,  9900.),
 (21, 10494.), (70, 10494.), (81, 11088.), (20, 11484.), (31, 12078.),
 (80, 12078.), (30, 13068.), (41, 13662.), (40, 14652.), (51, 15246.),
 (50, 16236.), (61, 16830.), (60, 17820.), (71, 18414.), (70, 19404.),
 (81, 19998.), (80, 20988.)]

pl_list = [20988.0, 21582.0, 22176.0, 22770.0, 23364.0, 23958.0, 24552.0, 25146.0]

kafa_sozluk = {10: 0, 11: 0, 20: 1, 21: 1, 30: 2, 31: 2, 40: 3, 41: 3, 50: 4, 51: 4,
               60: 5, 61: 5, 70: 6, 71: 6, 80: 7, 81: 7}


def get_length(recete):
    mesafe = []
    head_map = []
    for any in recete:
        mesafe.append(any[1])
        head_map.append(any[0])
    return mesafe, head_map
mesafe, head_map = get_length(recete)


def hesap_yeni_hedef(mesafe, head_map, pl_list):

    for i in range(1):
        sonuc = []
        for j in range(len(mesafe)):
            print(mesafe[j],  pl_list[kafa_sozluk[head_map[j]]])
            sonuc.append(mesafe[j] + pl_list[kafa_sozluk[head_map[j]]])
    print(sonuc)


hesap_yeni_hedef(mesafe, head_map, pl_list)
