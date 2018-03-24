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

liste_renk = []
i = 0
for any_dict in recete_dict:
    temp_list = []
    for any_list in any_dict.values():
        for val in any_list:
            print(val)
            temp_list.append(val)
    liste_renk.append(temp_list)

print(liste_renk)
