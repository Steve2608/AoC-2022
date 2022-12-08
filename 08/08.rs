use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("08/input.txt").expect("File not found");
    let grid: Vec<Vec<u8>> = data.split("\n")
        .map(|line| {
            line.as_bytes().iter().map(|num| num - b'0').collect()
        })
        .collect();
    
    println!("part1: {}", part1(&grid));
    println!("part2: {}", part2(&grid));

    println!("time: {:?}", start.elapsed());
}

fn part1(grid: &Vec<Vec<u8>>) -> usize {
    // no double counting on corners
    let mut i = grid.len()*2 + grid[0].len()*2 - 4;
    for x in 1..grid.len() - 1 {
        let row = &grid[x];

        for y in 1..&row.len() - 1 {
            let tree = &row[y];

            if row[y+1..row.len()].iter().all(|t| tree > t) || row[0..y].iter().rev().all(|t| tree > t) {
                i += 1;
            } else {
                // construction of col-vec is expensive, so we check for rows only first
                let col = grid.iter()
                    .map(|s| &s[y])
                    .collect::<Vec<_>>();

                if col[x+1..col.len()].iter().all(|t| tree > t) || col[0..x].iter().rev().all(|t| tree > t) {
                    i += 1;
                }
            }
        }
    }
    return i
}

fn part2(grid: &Vec<Vec<u8>>) -> usize {
    let mut scenic_score = 0;
    for x in 1..grid.len() - 1 {
        let row = &grid[x];

        for y in 1..&row.len() - 1 {
            let tree = &row[y];

            let mut score_up = 1;
            for i in (1..x).rev() {
                if tree <= &grid[i][y] { break; }
                score_up += 1;
            }

            let mut score_left = 1;
            for i in (1..y).rev() {
                if tree <= &grid[x][i] { break; }
                score_left += 1;
            }

            let mut score_down = 1;
            for i in x+1..grid.len() - 1 {
                if tree <= &grid[i][y] { break; } 
                score_down += 1;
            }

            let mut score_right = 1;
            for i in y+1..grid[x].len() - 1 {
                if tree <= &grid[x][i] { break; }
                score_right += 1;
            }

            let s = score_up * score_left * score_down * score_right;
            if s > scenic_score {
                scenic_score = s;
            }
        }
    }
    return scenic_score
}
