use std::cmp::{max, min};
use std::fs;
use std::time::Instant;

type Coord = usize;
type TCoord = (Coord, Coord);

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("14/input.txt").expect("File not found");
    let barriers: Vec<Vec<TCoord>> = data
        .lines()
        .map(|line| {
            line.split(" -> ")
                .map(|part| {
                    let coords: Vec<Coord> = part
                        .split(',')
                        .map(|num| num.parse::<Coord>().unwrap())
                        .collect();
                    (coords[0], coords[1])
                })
                .collect()
        })
        .collect();

    println!("part1: {}", part1(&barriers));
    println!("part2: {}", part2(&barriers));

    println!("time: {:?}", start.elapsed());
}

fn init_grid(data: &[Vec<TCoord>]) -> (Vec<Vec<char>>, TCoord) {
    let mut min_lr = 1000;
    let mut max_lr = 0;
    let mut max_ud = 0;
    for line in data {
        for &(lr, ud) in line {
            min_lr = min(min_lr, lr);
            max_lr = max(max_lr, lr);

            max_ud = max(max_ud, ud);
        }
    }

    let mut grid = vec![vec!['.'; max_lr - min_lr + 3]; max_ud + 1];
    let off_lr = min_lr - 1;

    for line in data {
        let (mut y, mut x) = line[0];
        for &(lr, ud) in &line[1..line.len()] {
            for row in grid.iter_mut().take(max(x, ud) + 1).skip(min(x, ud)) {
                for val in row
                    .iter_mut()
                    .take((max(y, lr) - off_lr) + 1)
                    .skip(min(y, lr) - off_lr)
                {
                    *val = '#';
                }
            }
            x = ud;
            y = lr;
        }
    }
    let spawn_ud = 0;
    let spawn_lr = 500 - off_lr;

    (grid, (spawn_ud, spawn_lr))
}

fn part1(data: &[Vec<TCoord>]) -> usize {
    let (mut grid, spawn) = init_grid(data);

    let mut n_sand = 0;
    loop {
        let mut s_ud = spawn.0;
        let mut s_lr = spawn.1;
        while s_ud + 1 < grid.len()
            && grid[s_ud + 1][s_lr - 1..=s_lr + 1]
                .iter()
                .any(|&v| v == '.')
        {
            if grid[s_ud + 1][s_lr] == '.' {
                s_ud += 1;
            } else if grid[s_ud + 1][s_lr - 1] == '.' {
                s_ud += 1;
                s_lr -= 1;
            } else {
                s_ud += 1;
                s_lr += 1;
            }
        }

        // fell off the map
        if s_ud >= grid.len() - 1 {
            break;
        } else {
            grid[s_ud][s_lr] = 'O';
            n_sand += 1;
        }
    }
    n_sand
}

fn part2(data: &[Vec<TCoord>]) -> usize {
    let (mut grid, mut spawn) = init_grid(data);
    // one row at the bottom
    grid.push(vec!['.'; grid[0].len()]);

    while grid[0].len() < grid.len() * 2 + 1{
        if spawn.1 <= grid.len() {
            // column to the left of spawn
            for row in &mut grid {
                row.insert(0, '.');
            }
            spawn.1 += 1;
        } else {
            // column to the right of spawn
            for row in &mut grid {
                row.push('.');
            }
        }
    }

    // bottomless pit now has a bottom
    grid.push(vec!['#'; grid[0].len()]);

    let mut n_sand = 0;
    loop {
        let mut s_ud = spawn.0;
        let mut s_lr = spawn.1;
        while s_ud + 2 < grid.len()
            && grid[s_ud + 1][s_lr - 1..=s_lr + 1]
                .iter()
                .any(|&v| v == '.')
        {
            if grid[s_ud + 1][s_lr] == '.' {
                s_ud += 1;
            } else if grid[s_ud + 1][s_lr - 1] == '.' {
                s_ud += 1;
                s_lr -= 1;
            } else {
                s_ud += 1;
                s_lr += 1;
            }
        }

        grid[s_ud][s_lr] = 'O';
        n_sand += 1;

        // filled up all the way to spawn
        if s_ud == spawn.0 && s_lr == spawn.1 {
            break;
        }
    }
    n_sand
}
