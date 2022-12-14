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
    fn dfs(grid: &mut Vec<Vec<char>>, n_sand: &mut usize, ud: usize, lr: usize) -> bool {
        // falling off the map
        if ud == grid.len() - 1 && grid[ud][lr] != '#' {
            return false;
        }
        if grid[ud][lr] != '.' {
            return true;
        }

        // early stopping
        if !dfs(grid, n_sand, ud + 1, lr)
            || !dfs(grid, n_sand, ud + 1, lr - 1)
            || !dfs(grid, n_sand, ud + 1, lr + 1)
        {
            return false;
        }

        grid[ud][lr] = 'O';
        *n_sand += 1;
        return true;
    }
    let (mut grid, spawn) = init_grid(data);
    let mut n_sand = 0;
    dfs(&mut grid, &mut n_sand, spawn.0, spawn.1);
    n_sand
}

fn part2(data: &[Vec<TCoord>]) -> usize {
    fn dfs(grid: &mut Vec<Vec<char>>, n_sand: &mut usize, ud: usize, lr: usize) {
        if ud >= grid.len() - 1 || grid[ud][lr] != '.' {
            return;
        }
    
        dfs(grid, n_sand, ud + 1, lr);
        dfs(grid, n_sand, ud + 1, lr - 1);
        dfs(grid, n_sand, ud + 1, lr + 1);
    
        grid[ud][lr] = 'O';
        *n_sand += 1;
    }
    let (mut grid, mut spawn) = init_grid(data);
    // one row at the bottom
    grid.push(vec!['.'; grid[0].len()]);

    let offset_left = grid.len() - spawn.1;
    let left_buf = vec!['.'; offset_left];
    let offset_right = grid.len() - (grid[0].len() - spawn.1);
    let right_buf = vec!['.'; offset_right];
    for row in &mut grid {
        row.splice(0..0, left_buf.clone());
        row.extend(&right_buf);
    }
    spawn.1 = grid.len();

    // bottomless pit now has a bottom
    grid.push(vec!['#'; grid[0].len()]);

    let mut n_sand = 0;
    dfs(&mut grid, &mut n_sand, spawn.0, spawn.1);
    n_sand
}


