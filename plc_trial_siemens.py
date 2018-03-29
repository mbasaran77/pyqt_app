import numpy as np
from pyModbusTCP import utils
from pyModbusTCP.client import ModbusClient


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





def hazirla_dizi_to_write(d_list):
    r_list = []
    g_list = []
    i = 0
    for index in range(len(d_list)):
        g_list.append(d_list[index])
        i += 1
        if i > 119:
            i = 0
            r_list.append(g_list)
            g_list = []
        if (len(d_list) - 1) == index and i < 119:
            r_list.append(g_list)
    return r_list


def plcGonder(recete_dizi, anahtar_dizi):
    client_host = "192.168.250.3"
    client_port = 502
    c = ModbusClient()
    c.host(client_host)
    c.port(client_port)
    err_list = []
    if not c.is_open():
        if not c.open():
            text = "unable to connect to " + client_host + ":" + str(client_port)
            print(text)
            # QMessageBox.warning(self, __appname__, text)
    if c.is_open():
        # self.prgBarRec.setValue(50)
        if len(recete_dizi) > 120:
            recete = hazirla_dizi_to_write(recete_dizi)
            i = 0
            hedef_reg_taban = 2001
            for send_recete in recete:
                hedef_reg = hedef_reg_taban + (i * 120)
                a = c.write_multiple_registers(hedef_reg, send_recete)
                if a is None or a == False:
                    err_list.append(False)
                i += 1
        else:
            a = c.write_multiple_registers(0, recete_dizi)
            if a is None or a is False:
                err_list.append(False)
        # self.prgBarRec.setValue(60)
        a = c.write_multiple_registers(100, anahtar_dizi)
        if a is None or a is False:
            err_list.append(False)
        # self.prgBarRec.setValue(70)
        # a = c.write_multiple_registers(1099, ayarlar_dizi_float)
        # if a is None or a is False:
        #     err_list.append(False)
        # self.prgBarRec.setValue(80)
        # a = c.write_multiple_registers(1017, ayarlar_dizi_int)
        # if a is None or a is False:
        #     err_list.append(False)
        # # self.prgBarRec.setValue(90)
        if len(err_list) > 0:
            #QMessageBox.warning(self, __appname__, "recete göndermede hata oluştu, tekrar deneyin !")
            print("recete göndermede hata oluştu, tekrar deneyin !")



plc_arr = MakePlcArr(recete_dict, off_set, skala)
slindir_arr, key_arr, plc_arr_int = plc_arr.convert_plc_arr()

plcGonder(plc_arr_int, key_arr)

