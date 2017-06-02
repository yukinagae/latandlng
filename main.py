#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# 現在位置(緯度,経度)と目的地位置(緯度,経度)を与えると 2点間の直線距離と目的位置の方位角(北=0)を出力させるプログラム
#
# TODO • 出力するまでの時間を測る
# TODO • 計算方法を変えて精度や処理時間の違いを出力する

import math
from math import cos
from math import sin
from math import tan
from math import acos
from math import atan
from math import atan2
from math import fabs
from math import sqrt
from math import radians
from math import degrees

# setting
a = 6378137 # 長軸半径 (赤道半径)

# 2点の(緯度, 経度)から距離を計算する
#
# 地球を完全な球体として想定して、球面三角法で計算する
# 地点A(経度x1, 緯度y1)、地点B(経度x2, 緯度y2)
#
# see: http://tomari.org/main/java/gps5.html
# see: http://log.nissuk.info/2012/04/2.html
#
# cos d = (siny1)×(siny2) + (cosy1)×(cosy2)×cos(x1－x2)
# (緯度=lat, 経度=lng)
# 2点の(緯度, 経度)から方角を計算する(北=0)
#
# 方位角は北：:0度、東：90度、南：180度、西270度で表示。
# 方位角=90-atan2(sin(x2-x1),cos(y1)tan(y2)-sin(y1)cos(x2-x1))
# @profile
def simple(lat1, lng1, lat2, lng2):
    φ1 = radians(lat1)
    L1 = radians(lng1)
    φ2 = radians(lat2)
    L2 = radians(lng2)
    L = L2 - L1
    α1 = degrees(atan2(sin(L), cos(φ1) * tan(φ2) - sin(φ1) * cos(L)))
    if α1 < 0:
        α1 = α1 + 360
    s = a * acos(sin(φ1) * sin(φ2) + cos(φ1) * cos(φ2) * cos(L))
    print("distance: {}".format(s))
    print("direction: {}".format(α1))

#
# 地球を楕円体として距離と方角を求める (WGS84 or GRS80)
#
# see: Vincenty's formulae
#
# 北緯を正、南緯を負
# 東経を正、西経を負
# とする。
# @profile
def vincenty(lat1, lng1, lat2, lng2):

    if lat1 == lat2 and lng1 == lng2:
        print("distance: {}".format(0))
        print("direction: {}".format(0))
        return

    # f = 1/298.257223563 # 扁平率
    f = 1/298.257222101 # 扁平率
    # b = (1 - f) * a # 短軸半径 (極半径)
    b = 6356752.31414036
    φ1 = lat1 # 出発点の緯度
    L1 = lng1 # 出発点の経度
    φ2 = lat2 # 到着点の緯度
    L2 = lng2 # 到着点の経度
    U1 = atan((1 - f) * tan(radians(φ1))) # 出発点の更成緯度 (補助球上の緯度)
    U2 = atan((1 - f) * tan(radians(φ2))) # 到着点の更成緯度 (補助球上の緯度)
    L = radians(L2 - L1) # 2点間の経度差
    #λ1 # 出発点の補助球上の経度
    #λ2 # 到着点の補助球上の経度
    #α # 赤道上での方位角
    # Inverse problem
    loss = 10 ** -12
    λ = L
    for n in range(0, 2000): # iterations
        sinσ = sqrt((cos(U2) * sin(λ)) ** 2 + (cos(U1) * sin(U2) - sin(U1) * cos(U2) * cos(λ)) ** 2)
        if sinσ == 0:
            print("distance: {}".format(0))
            print("direction: {}".format(0))
            return
        cosσ = sin(U1) * sin(U2) + cos(U1) * cos(U2) * cos(λ)
        σ = atan2(sinσ, cosσ) # 補助球上の弧の長さ
        sinα = (cos(U1) * cos(U2) * sin(λ)) / sinσ
        cos2α = 1 - (sinα ** 2)
        try:
            cos_2σm_ = cosσ - (2 * sin(U1) * sin(U2)) / cos2α
        except ZeroDivisionError:
            cos_2σm_ = 0
        C = f / 16 * cos2α * (4 + f * (4 - 3 * cos2α))
        λ_prev = λ
        λ = L + (1 - C) * f * sinα * (σ + C * sinσ * (cos_2σm_ + C * cosσ * (-1 + 2 * (cos_2σm_ ** 2))))

        if abs(λ - λ_prev) < loss:
            break
    # print("iteration: {}".format(n))
    u2 = cos2α * (a ** 2 - b ** 2) / b ** 2
    A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    Δσ = B * sinσ * (cos_2σm_ + 1 / 4 * B * (cosσ * (-1 + 2 * (cos_2σm_ ** 2)) - 1 / 6 * B * cos_2σm_ * (-3 + 4 * (sinσ ** 2)) * (-3 + 4 * (cos_2σm_ ** 2))))
    s = b * A * (σ - Δσ) # ２点間の距離
    print("distance: {}".format(s))
    α1 = degrees(atan2(cos(U2) * sin(λ), cos(U1) * sin(U2) - sin(U1) * cos(U2) * cos(λ))) # 出発点の方位角
    if α1 < 0:
        α1 = α1 + 360
    print("direction: {}".format(α1))

# main
if __name__ == '__main__':
    # import timeit
    # print(timeit.timeit("simple(36, 150, 44, 141)", number=100, setup="from __main__ import simple"))
    # print(timeit.timeit("vincenty(36, 150, 44, 141)", number=100, setup="from __main__ import vincenty"))
    simple(0, 0, 1, 180)
    vincenty(0, 0, 1, 180)
    simple(35.41, 139.41, 34.3, 118.14)
    vincenty(35.41, 139.41, 34.3, 118.14)
    simple(35.41, 139.41, 33.25, 70.35)
    vincenty(35.41, 139.41, 33.25, 70.35)
    simple(35.41, 139.41, 33.52, 151.12)
    vincenty(35.41, 139.41, 33.52, 151.12)
