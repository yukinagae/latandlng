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

def get_delta(φ1, φ2, ll):
    if ll >= 0:
        return φ2 - φ1
    else:
        return φ1 - φ2

def get_u1(φ1, φ2, ll, f):
    if ll >= 0:
        return math.atan((1 - f) * math.tan(φ1))
    else:
        return math.atan((1 - f) * math.tan(φ2))

def get_u2(φ1, φ2, ll, f):
    if ll >= 0:
        return math.atan((1 - f) * math.tan(φ2))
    else:
        return math.atan((1 - f) * math.tan(φ1))


#
# TODO 地球を楕円体として方角を求める
#
def get_acurate_direction(lat1, lng1, lat2, lng2):
    φ1 = lat1
    L1 = lng1
    φ2 = lat2
    L2 = lng2
    a = 6378137 # 長半径
    f = 1/298.257222101 # 扁平率
    l = L2 - L1
    ll = get_ll(l)
    L = math.fabs(ll)
    LL = 180 - L
    Δ = get_delta(φ1, φ2, ll)
    Σ = φ1 + φ2
    u1 = get_u1(φ1, φ2, ll, f)
    u2= get_u1(φ1, φ2, ll, f)
    ΣΣ = u1 + u2
    ΔΔ = u2 - u1
    ξ = math.cos(ΣΣ/2)
    ξξ = math.sin(ΣΣ/2)
    η = math.sin(ΔΔ/2)
    ηη = math.cos(ΔΔ/2)
    x = math.sin(u1) * math.sin(u2)
    y = math.cos(u1) * math.cos(u2)
    c = y * math.cos(L) + x
    ε = (f * (2 - f)) / math.pow((1 - f), 2)
    # zone 1
    θ = L * (1 + f * y)
    print(θ)
    for n in range(0, 100):
        g = math.sqrt(math.pow(η, 2) * math.pow(math.cos(θ/2), 2) + math.pow(ξ, 2) * math.pow(math.sin(θ/2), 2))
        h = math.sqrt(math.pow(ηη, 2) * math.pow(math.cos(θ/2), 2) + math.pow(ξξ, 2) * math.pow(math.sin(θ/2), 2))
        σ = 2 * math.atan(g/h)
        J = 2 * g * h
        K = math.pow(h, 2) - math.pow(g, 2)
        r = y * math.sin(θ) / J
        Γ = 1 - math.pow(y, 2)
        ζ = Γ * K - 2 * x
        ζζ = ζ + x
        D = 1 / 4 * f * (1 + f) - 3 / 16 * math.pow(f, 2) * Γ
        E = (1 - D * Γ) * f * y * (σ + D * J * (ζ + D * K * ((2 * math.pow(ζ, 2) - math.pow(Γ, 2)))))
        F = θ - L - E
        G = f * math.pow(y, 2) * (1 - 2 * D * Γ) + f * ζζ * (σ / J) * (1 - D * Γ + 1/2 * f * math.pow(y, 2))
        print(G)
        θ = θ - F / (1 - G)
    print(θ)


# main
if __name__ == '__main__':
    import timeit
    # print(timeit.timeit("get_simple_distance(36, 150, 44, 141)", number=100, setup="from __main__ import get_simple_distance"))
    # print(timeit.timeit("get_simple_direction(36, 150, 44, 141)", number=100, setup="from __main__ import get_simple_direction"))
    # distance = get_simple_distance(36, 150, 44, 141)
    direction = get_acurate_direction(36, 150, 44, 141)
    # print "distance: {}".format(distance)   # distance: 1174.15250957
    print("direction: {}".format(direction)) # direction: 322.066953861
