use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let games: Vec<(char, char)> = fs::read_to_string("02/input.txt")
        .expect("File not found")
        .lines()
        .map(|line| {
            let mut chars = line.chars();
            let c1: char = chars.next().unwrap();
            let c2: char = chars.nth(1).unwrap();

            (c1, c2)
        })
        .collect();

    println!("part1: {}", part1(&games));
    println!("part2: {}", part2(&games));

    println!("time: {:?}", start.elapsed());
}

fn part1(games: &[(char, char)]) -> i32 {
    let diff = b'X' - b'A';
    let offset = b'W';

    let mut score: i32 = 0;
    for &(opp, you) in games {
        if opp as u8 + diff as u8 == you as u8 {
            score += 3;
        } else if opp == 'A' && you == 'Y' || opp == 'B' && you == 'Z' || opp == 'C' && you == 'X' {
            score += 6;
        }
        score += (you as u8 - offset as u8) as i32;
    }
    score
}

fn part2(games: &[(char, char)]) -> i32 {
    let mut score: i32 = 0;
    for &(opp, you) in games {
        if you == 'X' {
            // loss
            if opp == 'A' {
                score += 3;
            } else if opp == 'B' {
                score += 1;
            } else {
                score += 2;
            }
        } else if you == 'Y' {
            // draw
            score += (3 + (opp as u8 - b'A' + 1)) as i32;
        } else {
            // win
            score += 6;
            if opp == 'A' {
                score += 2;
            } else if opp == 'B' {
                score += 3;
            } else {
                score += 1;
            }
        }
    }
    score
}
