#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# 現在位置(緯度,経度)と目的地位置(緯度,経度)を与えると 2点間の直線距離と目的位置の方位角(北=0)を出力させるプログラム
#
# TODO • 出力するまでの時間を測る
# TODO • 計算方法を変えて精度や処理時間の違いを出力する

import math

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
# @profile
def get_simple_distance(lat1, lng1, lat2, lng2):
    # 地球の半径を赤道半径と仮定する
    r = 6378.137
    # 角度をradianに変換
    lat1 = lat1 * math.pi / 180
    lng1 = lng1 * math.pi / 180
    lat2 = lat2 * math.pi / 180
    lng2 = lng2 * math.pi / 180
    return r * math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lng2 - lng1))

# 2点の(緯度, 経度)から方角を計算する(北=0)
#
# 方位角は北：:0度、東：90度、南：180度、西-90度で表示。
# 方位角=90-atan2(sin(x2-x1),cos(y1)tan(y2)-sin(y1)cos(x2-x1))
# @profile
def get_simple_direction(lat1, lng1, lat2, lng2):
    # 角度をradianに変換
    lat1 = lat1 * math.pi / 180
    lng1 = lng1 * math.pi / 180
    lat2 = lat2 * math.pi / 180
    lng2 = lng2 * math.pi / 180
    atan = math.atan2(math.sin(lng2 - lng1), math.cos(lat1) * math.tan(lat2) - math.sin(lat1) * math.cos(lng2 - lng1))
    return atan * 180 / math.pi # radianから角度に戻す

import timeit

# timeit.timeit('get_distance(36, 150, 44, 141)', number=10)

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("get_simple_distance(36, 150, 44, 141)", number=100, setup="from __main__ import get_simple_distance"))
    print(timeit.timeit("get_simple_direction(36, 150, 44, 141)", number=100, setup="from __main__ import get_simple_direction"))
    distance = get_simple_distance(36, 150, 44, 141)
    direction = get_simple_direction(36, 150, 44, 141)
    print "distance: {}".format(distance)
    print "direction: {}".format(direction)
