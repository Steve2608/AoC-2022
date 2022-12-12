use std::collections::{HashMap, HashSet, VecDeque};
use std::fs;
use std::time::Instant;

type Coord = u8;
type Height = u16;

fn main() {
    let start = Instant::now();

    let (map, s, strt, end) = parse_input("12/input.txt");

    println!("part1: {}", part1(&map, s, end));
    println!("part2: {}", part2(&map, &strt, end));

    println!("time: {:?}", start.elapsed());
}

fn parse_input(path: &str) -> (Vec<Vec<char>>, (Coord, Coord), Vec<(Coord, Coord)>, (Coord, Coord)) {
    let map: Vec<Vec<char>> = fs::read_to_string(path)
        .expect("File not found")
        .lines()
        .map(|l| l.chars().collect())
        .collect();
    let mut end = (0, 0);
    let mut s = (0, 0);
    let mut strt = vec![(0, 0)];

    for (i, x) in map.iter().enumerate() {
        for (j, &y) in x.iter().enumerate() {
            match y {
                'E' => end = (i as Coord, j as Coord),
                'S' => s = (i as Coord, j as Coord),
                'a' => {
                    // if we're surrounded by other 'a', 'S' or something unreachable, don't even consider this start
                    // they can't even be local optima
                    if !(i > 0
                        && (height(&map, ((i - 1) as Coord, j as Coord)) == 0
                            || height(&map, ((i - 1) as Coord, j as Coord)) >= 2)
                        && i < map.len() - 1
                        && (height(&map, ((i + 1) as Coord, j as Coord)) == 0
                            || height(&map, ((i + 1) as Coord, j as Coord)) >= 2)
                        && j > 0
                        && (height(&map, (i as Coord, (j - 1) as Coord)) == 0
                            || height(&map, (i as Coord, (j - 1) as Coord)) >= 2)
                        && j < map[i].len() - 1
                        && (height(&map, (i as Coord, (j + 1) as Coord)) == 0
                            || height(&map, (i as Coord, (j + 1) as Coord)) >= 2))
                    {
                        strt.push((i as Coord, j as Coord))
                    }
                }
                _ => {}
            };
        }
    }
    (map, s, strt, end)
}

fn part1(map: &[Vec<char>], start: (Coord, Coord), end: (Coord, Coord)) -> usize {
    let mut visited: HashSet<(Coord, Coord)> = HashSet::new();
    let mut distances: HashMap<(Coord, Coord), Height> = HashMap::new();
    distances.insert(start, 0);
    // counting start as first step - will have to subtract later on
    let mut fringe: VecDeque<(Coord, Coord)> = VecDeque::from([start]);

    bfs(map, &mut visited, &mut distances, &mut fringe);

    distances[&end] as usize
}

fn height(map: &[Vec<char>], idx: (Coord, Coord)) -> usize {
    let c: char = map[idx.0 as usize][idx.1 as usize];

    match c {
        'S' => 0,
        'E' => 26,
        _ => (c as Coord - b'a') as usize,
    }
}

fn bfs(
    map: &[Vec<char>],
    visited: &mut HashSet<(Coord, Coord)>,
    distances: &mut HashMap<(Coord, Coord), Height>,
    fringe: &mut VecDeque<(Coord, Coord)>,
) {
    while !fringe.is_empty() {
        let curr = fringe.pop_front().unwrap();
        if visited.contains(&curr) {
            continue;
        }
        visited.insert(curr);

        let dist = *distances.get(&curr).unwrap();

        // process all neighbours
        if curr.1 > 0 {
            let left = (curr.0, curr.1 - 1);
            if height(map, left) <= height(map, curr) + 1
                && !visited.contains(&left)
            {
                fringe.push_back(left);
                distances.insert(left, dist + 1);
            }
        }

        if (curr.1 as usize) < map[curr.0 as usize].len() - 1 {
            let right = (curr.0, curr.1 + 1);
            if height(map, right) <= height(map, curr) + 1
                && !visited.contains(&right)
            {
                fringe.push_back(right);
                distances.insert(right, dist + 1);
            }
        }

        if curr.0 > 0 {
            let up = (curr.0 - 1, curr.1);
            if height(map, up) <= height(map, curr) + 1
                && !visited.contains(&up)
            {
                fringe.push_back(up);
                distances.insert(up, dist + 1);
            }
        }

        if (curr.0 as usize) < map.len() - 1 {
            let down = (curr.0 + 1, curr.1);
            if height(map, down) <= height(map, curr) + 1
                && !visited.contains(&down)
            {
                fringe.push_back(down);
                distances.insert(down, dist + 1);
            }
        }
    }
}

fn part2(map: &[Vec<char>], strt: &[(Coord, Coord)], end: (Coord, Coord)) -> usize {
    let mut min_dist: Height = Height::MAX;

    for &start in strt {
        let mut visited: HashSet<(Coord, Coord)> = HashSet::new();
        let mut distances: HashMap<(Coord, Coord), Height> = HashMap::new();
        distances.insert(start, 0);
        // counting start as first step - will have to subtract later on
        let mut fringe: VecDeque<(Coord, Coord)> = VecDeque::from([start]);

        bfs(map, &mut visited, &mut distances, &mut fringe);

        if *distances.get(&end).unwrap_or(&Height::MAX) < min_dist {
            min_dist = distances[&end];
        }
    }
    min_dist as usize
}
