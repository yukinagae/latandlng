#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# 現在位置(緯度,経度)と目的地位置(緯度,経度)を与えると 2点間の直線距離と目的位置の方位角(北=0)を出力させるプログラム
#

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

# setting (GRS80)
a = 6378137 # 長軸半径 (赤道半径)
# f = 1/298.257223563 # 扁平率
f = 1/298.257222101 # 扁平率
# b = (1 - f) * a # 短軸半径 (極半径)
b = 6356752.31414036 # いちいち計算するのが勿体無いので計算しておく

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
        return 0, 0

    φ1 = lat1 # 出発点の緯度
    L1 = lng1 # 出発点の経度
    φ2 = lat2 # 到着点の緯度
    L2 = lng2 # 到着点の経度
    U1 = atan((1 - f) * tan(radians(φ1))) # 出発点の更成緯度 (補助球上の緯度)
    U2 = atan((1 - f) * tan(radians(φ2))) # 到着点の更成緯度 (補助球上の緯度)
    L = radians(L2 - L1) # 2点間の経度差
    # Inverse problem
    loss = 10 ** -12
    λ = L
    for n in range(0, 2000): # iterations
        sinσ = sqrt((cos(U2) * sin(λ)) ** 2 + (cos(U1) * sin(U2) - sin(U1) * cos(U2) * cos(λ)) ** 2)
        if sinσ == 0:
            return 0, 0
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
    s = b * A * (σ - Δσ) # 2点間の距離
    α1 = degrees(atan2(cos(U2) * sin(λ), cos(U1) * sin(U2) - sin(U1) * cos(U2) * cos(λ))) # 出発点の方位角
    if α1 < 0:
        α1 = α1 + 360
    return s, α1

#
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
    return s, α1

#
# 距離が近い場合、平面として距離と方角の近似を計算する
#
# @profile
def short_distance(lat1, lng1, lat2, lng2):
    phi1 = radians(lat1)
    L1 = radians(lng1)
    phi2 = radians(lat2)
    L2 = radians(lng2)
    phi = phi2 - phi1
    L = L2 - L1
    s = a * sqrt((L) ** 2 + (phi) ** 2)
    alpha1 = degrees(atan2(a * phi, a * L))
    if 0 < alpha1 <= 90:
        alpha1 = 90 - alpha1
    elif -179 < alpha1 <= 0:
        alpha1 = -alpha1 + 90
    elif 90 < alpha1 < 180:
        alpha1 = 360 - (90 - alpha1)
    return s, alpha1

#
# 精度の差異を出力
#
# 仮にVincenty's formulaeを正として、差異を出力する
#
def difference(lat1, lng1, lat2, lng2):
    print("#######################################################")
    print("lat1:{} lng1:{} lat2:{} lng2:{}".format(lat1, lng1, lat2, lng2))
    print("#######################################################")
    v_distance, v_direction = vincenty(lat1, lng1, lat2, lng2)
    print("[vincenty] distance: {}".format(v_distance))
    print("[vincenty] direction: {}".format(v_direction))
    s_distance, s_direction = simple(lat1, lng1, lat2, lng2)
    print("[simple] distance: {}".format(s_distance))
    print("[simple] direction: {}".format(s_direction))
    print("[simple distance diff: {}]".format(abs(v_distance - s_distance)))
    print("[simple direction diff: {}]".format(abs(v_direction - s_direction)))
    sh_distance, sh_direction = short_distance(lat1, lng1, lat2, lng2)
    print("[short] distance: {}".format(sh_distance))
    print("[short] direction: {}".format(sh_direction))
    print("[short distance diff: {}]".format(abs(v_distance - sh_distance)))
    print("[short direction diff: {}]".format(abs(v_direction - sh_direction)))
    print("#######################################################")

# main
if __name__ == '__main__':
    import timeit
    # performance
    print("#######################################################")
    print("performance")
    print("#######################################################")
    print("[vincenty]")
    print(timeit.timeit("vincenty(36, 150, 44, 141)",       number=100000, setup="from __main__ import vincenty")) # 1.8238524299813434
    print("[simple]")
    print(timeit.timeit("simple(36, 150, 44, 141)",         number=100000, setup="from __main__ import simple")) # 0.15921848092693835
    print("[short distance]")
    print(timeit.timeit("short_distance(36, 150, 44, 141)", number=100000, setup="from __main__ import short_distance")) # 0.14479246700648218
    # 各計算方法による距離と方角の差異
    difference(0, 0, 89, 00)
    difference(0, 0, -89, 00)
    difference(0, 0, 1, 179)
    difference(35.41, 139.41, 34.3, 118.14)
    difference(35.41, 139.41, 33.25, 70.35)
    difference(35.41, 139.41, 33.52, 151.12)
