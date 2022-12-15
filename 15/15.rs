use std::cmp::min;
use std::collections::HashSet;
use std::fs;
use std::time::Instant;

type Coord = i32;
type TCoord = (Coord, Coord);

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("15/input.txt").expect("File not found");
    let coordinates: Vec<(TCoord, TCoord)> = data
        .lines()
        .map(|line| {
            let parts: Vec<&str> = line.split('=').collect();

            let s1: Coord = parts[1]
                .split(',')
                .next()
                .unwrap()
                .parse::<Coord>()
                .unwrap();
            let s2: Coord = parts[2]
                .split(':')
                .next()
                .unwrap()
                .parse::<Coord>()
                .unwrap();
            let b1: Coord = parts[3]
                .split(',')
                .next()
                .unwrap()
                .parse::<Coord>()
                .unwrap();
            let b2: Coord = parts[4].parse::<Coord>().unwrap();
            ((s1, s2), (b1, b2))
        })
        .collect();

    println!("part1: {}", part1(&coordinates, 2_000_000));
    println!("part2: {}", part2(&coordinates, 0, 4_000_000));

    println!("time: {:?}", start.elapsed());
}

fn manhatten(a: TCoord, b: TCoord) -> Coord {
    (a.0 - b.0).abs() + (a.1 - b.1).abs()
}

fn deltoids(data: &[(TCoord, TCoord)]) -> Vec<(Coord, Coord, Coord)> {
    let mut deltoids: Vec<(Coord, Coord, Coord)> = vec![];
    for &(s, b) in data {
        let d: Coord = manhatten(s, b);
        deltoids.push((s.1 - d, s.1 + d, s.0));
    }

    deltoids
}

fn ranges(delts: &[(Coord, Coord, Coord)], target_y: Coord) -> Vec<TCoord> {
    // [start, end] in target_y
    let mut ranges: Vec<TCoord> = vec![];
    for &(dl, dr, x) in delts {
        if dl <= target_y && target_y <= dr {
            let span: Coord = min(target_y - dl, dr - target_y);
            ranges.push((x - span, x + span));
        }
    }
    ranges
}

fn part1(data: &[(TCoord, TCoord)], target_y: Coord) -> Coord {
    fn simplify_ranges(ranges: &mut [TCoord]) -> Vec<TCoord> {
        ranges.sort();
        let (mut start, mut end) = ranges[0];
        let mut rngs: Vec<TCoord> = vec![];
        for &(s, e) in ranges.iter().skip(1) {
            if (start <= s && s <= end && end <= e) || (end + 1 == s) {
                end = e;
            } else if !(start <= s && e <= end) {
                rngs.push((start, end));
                // found new range
                (start, end) = (s, e);
            }
        }
        if rngs.is_empty() || rngs[rngs.len() - 1] != (start, end) {
            rngs.push((start, end));
        }
        rngs
    }

    let mut sensors: HashSet<TCoord> = HashSet::new();
    let mut beacons: HashSet<TCoord> = HashSet::new();
    for &(s, b) in data {
        sensors.insert(s);
        beacons.insert(b);
    }

    let delts: Vec<(Coord, Coord, Coord)> = deltoids(data);
    let mut rngs: Vec<TCoord> = ranges(&delts, target_y);

    let r: Vec<TCoord> = simplify_ranges(&mut rngs);
    let mut n: Coord = r.iter().map(|&(a, b)| b - a + 1).sum();

    for &(sx, _) in sensors.iter().filter(|&&(_, sy)| sy == target_y) {
        for &(min_, max_) in r.iter() {
            if min_ <= sx && sx <= max_ {
                n -= 1;
            }
        }
    }

    for &(bx, _) in beacons.iter().filter(|&&(_, sy)| sy == target_y) {
        for &(min_, max_) in r.iter() {
            if min_ <= bx && bx <= max_ {
                n -= 1;
            }
        }
    }

    n
}

fn part2(data: &[(TCoord, TCoord)], min_y: Coord, max_y: Coord) -> i64 {
    fn simplify_ranges(ranges: &mut [TCoord]) -> Coord {
        ranges.sort();
        let (a1, mut a2) = ranges[0];
        for &(b1, b2) in ranges.iter().skip(1) {
            if (a1 <= b1 && b1 <= a2 && a2 <= b2) || (a2 + 1 == b1) {
                a2 = b2;
            } else if !(a1 <= b1 && b2 <= a2) {
                // assuming there's only a single free space, the NEXT x-coordinate has to be it
                // so we take the lower range's max and +1 to it
                return a2 + 1;
            }
        }
        -1
    }

    let delts: Vec<(Coord, Coord, Coord)> = deltoids(data);
    for target_y in min_y..=max_y {
        let mut rngs: Vec<TCoord> = ranges(&delts, target_y);
        let x: Coord = simplify_ranges(&mut rngs);
        if x != -1 {
            return (x as i64) * 40_000_000 + (target_y as i64);
        }
    }
    -1
}
