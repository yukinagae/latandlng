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
# TODO 緯度、経度が180を超えた場合の考慮が抜けている。（その場合には、マイナスにして計算する必要がある）
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
# 方位角は北：:0度、東：90度、南：180度、西270度で表示。
# 方位角=90-atan2(sin(x2-x1),cos(y1)tan(y2)-sin(y1)cos(x2-x1))
# @profile
# TODO 緯度、経度が180を超えた場合の考慮が抜けている。（その場合には、マイナスにして計算する必要がある）
def get_simple_direction(lat1, lng1, lat2, lng2):
    # 角度をradianに変換
    lat1 = lat1 * math.pi / 180
    lng1 = lng1 * math.pi / 180
    lat2 = lat2 * math.pi / 180
    lng2 = lng2 * math.pi / 180
    atan = math.atan2(math.sin(lng2 - lng1), math.cos(lat1) * math.tan(lat2) - math.sin(lat1) * math.cos(lng2 - lng1))
    result = atan * 180 / math.pi # radianから角度に戻す
    if result >= 0:
        return result
    else:
        return 360 + result

#
# 地球を楕円体として計算した場合
#
# see: http://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/bl2stf.html
# see: http://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/algorithm/bl2st/bl2st.htm
#
# 楕円体	GRS80
# 出発点	緯度	北緯 36°00′00.0000″
# 経度	東経 150°00′00.0000″
# 到着点	緯度	北緯 44°00′00.0000″
# 経度	東経 141°00′00.0000″

# 測地線長	1,173,117.651(m)
# 方位角	出発点→到着点	321°57′20.46″
# 到着点→出発点	136°08′57.93″

#
# TODO 地球を楕円体として距離を求める
#
def get_accurate_distance(lat1, lng1, lat2, lng2):
    pass

def get_ll(l):
    if l > 180:
        return l - 360
    elif l < -180:
        return l + 360
    else:
        return l

def get_delta(phi1, phi2, ll):
    if ll >= 0:
        return phi2 - phi1
    else:
        return phi1 - phi2

def get_u1(phi1, phi2, ll, f):
    if ll >= 0:
        return math.atan((1 - f) * math.tan(phi1))
    else:
        return math.atan((1 - f) * math.tan(phi2))

def get_u2(phi1, phi2, ll, f):
    if ll >= 0:
        return math.atan((1 - f) * math.tan(phi2))
    else:
        return math.atan((1 - f) * math.tan(phi1))


#
# TODO 地球を楕円体として方角を求める
#
def get_acurate_direction(lat1, lng1, lat2, lng2):
    phi1 = lat1
    L1 = lng1
    phi2 = lat2
    L2 = lng2
    a = 6378137 # 長半径
    f = 1/298.257222101 # 扁平率
    l = L2 - L1
    ll = get_ll(l)
    L = math.fabs(ll)
    LL = 180 - L
    delta = get_delta(phi1, phi2, ll)
    sigma = phi1 + phi2
    u1 = get_u1(phi1, phi2, ll, f)
    u2= get_u1(phi1, phi2, ll, f)
    sigmasigma = u1 + u2
    deltadelta = u2 - u1
    Z = math.cos(sigmasigma/2)
    ZZ = math.sin(sigmasigma/2)
    E = math.sin(deltadelta/2)
    EE = math.cos(deltadelta/2)
    x = math.sin(u1) * math.sin(u2)
    y = math.cos(u1) * math.cos(u2)
    c = y * math.cos(L) + x
    e = (f * (2 - f)) / math.pow((1 - f), 2)
    # zone 1
    theta = L * (1 + f * y)
    print theta
    for n in range(0, 100):
        g = math.sqrt(math.pow(E, 2) * math.pow(math.cos(theta/2), 2) + math.pow(Z, 2) * math.pow(math.sin(theta/2), 2))
        h = math.sqrt(math.pow(EE, 2) * math.pow(math.cos(theta/2), 2) + math.pow(ZZ, 2) * math.pow(math.sin(theta/2), 2))
        o = 2 * math.atan(g/h)
        J = 2 * g * h
        K = math.pow(h, 2) - math.pow(g, 2)
        r = y * math.sin(theta) / J
        R = 1 - math.pow(y, 2)
        S = R * K - 2 * x
        SS = S + x
        D = 1 / 4 * f * (1 + f) - 3 / 16 * math.pow(f, 2) * R
        E1 = (1 - D * R) * f * y * (o + D * J * (S + D * K * ((2 * math.pow(S, 2) - math.pow(R, 2)))))
        F = theta - L - E1
        G = f * math.pow(y, 2) * (1 - 2 * D * R) + f * SS * (o / J) * (1 - D * R + 1/2 * f * math.pow(y, 2))
        print G
        theta = theta - F / (1 - G)
    print theta


# main
if __name__ == '__main__':
    import timeit
    # print(timeit.timeit("get_simple_distance(36, 150, 44, 141)", number=100, setup="from __main__ import get_simple_distance"))
    # print(timeit.timeit("get_simple_direction(36, 150, 44, 141)", number=100, setup="from __main__ import get_simple_direction"))
    # distance = get_simple_distance(36, 150, 44, 141)
    direction = get_acurate_direction(36, 150, 44, 141)
    # print "distance: {}".format(distance)   # distance: 1174.15250957
    print "direction: {}".format(direction) # direction: 322.066953861
