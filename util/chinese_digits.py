# -*- coding: utf-8 -*-


chs_arabic_map = {0: u'零', 1: u'一', 2: u'二', 3: u'三', 4: u'四', 5: u'五', 6: u'六', 7: u'七', 8: u'八', 9: u'九',
                  10: u'十'}


# do the number exchange above one hundred.
def get_chinese(arab):
    if arab > 10:
        mod = arab % 10
        int_num = arab / 10
        return chs_arabic_map.get(int_num) + chs_arabic_map.get(10) + chs_arabic_map.get(mod)

    return chs_arabic_map.get(arab)
