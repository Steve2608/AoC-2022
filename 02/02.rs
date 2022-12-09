use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("02/input.txt").expect("File not found");

    let games: Vec<&str> = data.split('\n').collect();

    println!("part1: {}", part1(&games));
    println!("part2: {}", part2(&games));

    println!("time: {:?}", start.elapsed());
}

fn part1(games: &[&str]) -> i32 {
    let diff = b'X' - b'A';
    let offset = b'W';

    let mut score: i32 = 0;
    for line in games {
        let chars = line.as_bytes();
        let opp = chars[0];
        let you = chars[2];

        if opp + diff == you {
            score += 3;
        } else if opp == b'A' && you == b'Y'
            || opp == b'B' && you == b'Z'
            || opp == b'C' && you == b'X'
        {
            score += 6;
        }
        score += (you - offset) as i32;
    }

    score
}

fn part2(games: &[&str]) -> i32 {
    let mut score: i32 = 0;
    for line in games {
        let chars = line.as_bytes();
        let opp = chars[0];
        let you = chars[2];

        if you == b'X' {
            // loss
            if opp == b'A' {
                score += 3;
            } else if opp == b'B' {
                score += 1;
            } else {
                score += 2;
            }
        } else if you == b'Y' {
            // draw
            score += (3 + (opp - b'A' + 1)) as i32;
        } else {
            // win
            score += 6;
            if opp == b'A' {
                score += 2;
            } else if opp == b'B' {
                score += 3;
            } else {
                score += 1;
            }
        }
    }

    score
}
