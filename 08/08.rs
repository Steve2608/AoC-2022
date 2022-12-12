use std::cmp::max;
use std::fs;
use std::time::Instant;

type Height = u8;

fn main() {
    let start = Instant::now();

    let grid: Vec<Vec<Height>> = fs::read_to_string("08/input.txt")
        .expect("File not found")
        .lines()
        .map(|line| line.as_bytes().iter().map(|num| num - b'0').collect())
        .collect();

    println!("part1: {}", part1(&grid));
    println!("part2: {}", part2(&grid));

    println!("time: {:?}", start.elapsed());
}

fn part1(grid: &[Vec<Height>]) -> usize {
    // no double counting on corners
    let mut n_visible = grid.len() * 2 + grid[0].len() * 2 - 4;

    for x in 1..grid.len() - 1 {
        let row = &grid[x];

        for y in 1..grid[x].len() - 1 {
            let tree = grid[x][y];

            if row[y + 1..grid[x].len()].iter().all(|t| tree > *t)
                || row[0..y].iter().rev().all(|t| tree > *t)
                || grid[x + 1..grid.len()].iter().all(|t| tree > t[y])
                || grid[0..x].iter().rev().all(|t| tree > t[y])
            {
                n_visible += 1;
            }
        }
    }
    n_visible
}

fn part2(grid: &[Vec<Height>]) -> usize {
    let mut scenic_score = 0;
    for (x, row) in grid.iter().enumerate() {
        for (y, &tree) in row.iter().enumerate() {
            let mut score_up = 1;
            for i in (1..x).rev() {
                if tree <= grid[i][y] {
                    break;
                }
                score_up += 1;
            }

            let mut score_left = 1;
            for i in (1..y).rev() {
                if tree <= grid[x][i] {
                    break;
                }
                score_left += 1;
            }

            let mut score_down = 1;
            for i in x + 1..grid.len() - 1 {
                if tree <= grid[i][y] {
                    break;
                }
                score_down += 1;
            }

            let mut score_right = 1;
            for i in y + 1..grid[x].len() - 1 {
                if tree <= grid[x][i] {
                    break;
                }
                score_right += 1;
            }

            scenic_score = max(
                scenic_score,
                score_up * score_left * score_down * score_right,
            );
        }
    }
    scenic_score
}
