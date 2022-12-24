use std::cmp::{max, min};
use std::collections::{HashSet, VecDeque};
use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: Vec<(i32, (i32, i32, i32, i32, i32, i32))> = fs::read_to_string("19/input.txt")
        .expect("File not found")
        .lines()
        .map(|line| {
            let parts: Vec<String> = line
                .replace(":", "")
                .split(' ')
                .map(|s| s.to_owned())
                .collect();

            return (
                parts[1].parse::<i32>().unwrap(),
                (
                    parts[6].parse::<i32>().unwrap(),
                    parts[12].parse::<i32>().unwrap(),
                    parts[18].parse::<i32>().unwrap(),
                    parts[21].parse::<i32>().unwrap(),
                    parts[27].parse::<i32>().unwrap(),
                    parts[30].parse::<i32>().unwrap(),
                ),
            );
        })
        .collect();

    println!("part1: {}", part1(&data, 24));
    println!("part2: {}", part2(&data, 32));
    println!("time: {:?}", start.elapsed());
}

fn solve(
    cost_o: i32,
    cost_c: i32,
    cost_ob_o: i32,
    cost_ob_c: i32,
    cost_g_o: i32,
    cost_g_ob: i32,
    time: i32,
) -> i32 {
    let max_cost_ore = *vec![cost_o, cost_c, cost_ob_o, cost_g_o]
        .iter()
        .max()
        .unwrap();
    let mut fringe: VecDeque<((i32, i32, i32, i32), (i32, i32, i32, i32), i32)> =
        VecDeque::from(vec![((0, 0, 0, 0), (1, 0, 0, 0), time)]);
    let mut visited: HashSet<((i32, i32, i32, i32), (i32, i32, i32, i32))> = HashSet::new();
    let mut best_geodes = 0;

    while !fringe.is_empty() {
        let ((mut o, mut c, mut ob, g), (bot_o, bot_c, bot_ob, bot_g), mut t) =
            fringe.pop_front().unwrap();
        
        // reduce search-depth by one
        // no matter what action is taken by at time==1 it does not change the number of geodes in time==0
        if t == 1 {
            best_geodes = max(g + bot_g, best_geodes);
            continue;
        }

        // throw away surplus resources that cannot be spent in time
        o = min(o, t * max_cost_ore - bot_o * (t - 1));
        c = min(c, t * cost_ob_c - bot_c * (t - 1));
        ob = min(ob, t * cost_g_ob - bot_ob * (t - 1));

        let state = ((o, c, ob, g), (bot_o, bot_c, bot_ob, bot_g));
        if visited.contains(&state) {
            continue;
        }
        visited.insert(state);

        t -= 1;
        // do nothing
        fringe.push_back((
            (o + bot_o, c + bot_c, ob + bot_ob, g + bot_g),
            (bot_o, bot_c, bot_ob, bot_g),
            t,
        ));

        // buy ore, clay, obsidian, geode bot but never beyond a point where it cannot be spent
        if o >= cost_o && bot_o < max_cost_ore {
            fringe.push_back((
                (o + bot_o - cost_o, c + bot_c, ob + bot_ob, g + bot_g),
                (bot_o + 1, bot_c, bot_ob, bot_g),
                t,
            ));
        }
        if o >= cost_c && bot_c < cost_ob_c {
            fringe.push_back((
                (o + bot_o - cost_c, c + bot_c, ob + bot_ob, g + bot_g),
                (bot_o, bot_c + 1, bot_ob, bot_g),
                t,
            ));
        }

        if o >= cost_ob_o && c >= cost_ob_c && bot_ob < cost_g_ob {
            fringe.push_back((
                (
                    o + bot_o - cost_ob_o,
                    c + bot_c - cost_ob_c,
                    ob + bot_ob,
                    g + bot_g,
                ),
                (bot_o, bot_c, bot_ob + 1, bot_g),
                t,
            ));
        }

        if o >= cost_g_o && ob >= cost_g_ob {
            fringe.push_back((
                (
                    o + bot_o - cost_g_o,
                    c + bot_c,
                    ob + bot_ob - cost_g_ob,
                    g + bot_g,
                ),
                (bot_o, bot_c, bot_ob, bot_g + 1),
                t,
            ));
        }
    }

    best_geodes
}

fn part1(blueprints: &[(i32, (i32, i32, i32, i32, i32, i32))], time: i32) -> i32 {
    blueprints
        .iter()
        .map(
            |&(id, (cost_o, cost_c, cost_ob_o, cost_ob_c, cost_g_o, cost_g_ob))| {
                solve(
                    cost_o, cost_c, cost_ob_o, cost_ob_c, cost_g_o, cost_g_ob, time,
                ) * id
            },
        )
        .sum()
}

fn part2(blueprints: &[(i32, (i32, i32, i32, i32, i32, i32))], time: i32) -> i32 {
    blueprints
        .iter()
        .take(3)
        .map(
            |&(_, (cost_o, cost_c, cost_ob_o, cost_ob_c, cost_g_o, cost_g_ob))| {
                solve(
                    cost_o, cost_c, cost_ob_o, cost_ob_c, cost_g_o, cost_g_ob, time,
                )
            },
        )
        .product()
}
