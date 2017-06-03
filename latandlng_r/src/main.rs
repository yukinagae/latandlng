//
#![allow(non_snake_case)]

fn main() {
    simple(0.0, 0.0, 89.0, 0.0);
}

fn simple(lat1: f64, lng1: f64, lat2: f64, lng2: f64) {

    let a = 6378137.0; // 長軸半径 (赤道半径)

    let phi1 = lat1.to_radians();
    let L1 = lng1.to_radians();
    let phi2 = lat2.to_radians();
    let L2 = lng2.to_radians();
    let L = L2 - L1;
    let mut alpha1 = L.sin().atan2(phi1.cos() * phi2.tan() - phi1.sin() * L.cos()).to_degrees();

    if alpha1 < 0.0 {
        alpha1 = alpha1 + 360.0
    }
    let s = a * (phi1.sin() * phi2.sin() + phi1.cos() * phi2.cos() * L.cos()).acos();
    println!("distance: {:?}", s);
    println!("direction: {:?}", alpha1);
}
