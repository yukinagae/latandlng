#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import cos
from math import sin
from math import tan
from math import atan2
from math import sqrt
from math import radians
from math import degrees

a = 6378137 # 長軸半径 (赤道半径)

def short_distance(lat1, lng1, lat2, lng2):
    phi1 = radians(lat1)
    L1 = radians(lng1)
    phi2 = radians(lat2)
    L2 = radians(lng2)
    phi = phi2 - phi1
    L = L2 - L1
    s = a * sqrt((L) ** 2 + (phi) ** 2)
    alpha1 = degrees(atan2(a * phi, a * L))
    print("distance: {}".format(s))
    print("direction: {}".format(alpha1))

if __name__ == '__main__':
    short_distance(0, 0, 10, -10)

# i.e.
# 315 (135)  0 (90)      45 (45)
# 270 (180)              90 (0)
# 225 (-135) 180 (-90)  135 (-45)
