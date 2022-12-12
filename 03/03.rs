use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("03/input.txt").expect("File not found");

    let rucksacks: Vec<&str> = data.lines().collect();

    println!("part1: {}", part1(&rucksacks));
    println!("part2: {}", part2(&rucksacks));

    println!("time: {:?}", start.elapsed());
}

fn char_to_score(chr: u8) -> u8 {
    if chr <= b'Z' {
        27 + (chr - b'A')
    } else {
        1 + (chr - b'a')
    }
}

fn part1(rucksacks: &[&str]) -> usize {
    let mut score: usize = 0;
    for line in rucksacks {
        let len = line.len() / 2;
        let left = &line[0..len];
        let right = &line[len..];

        for c in left.chars() {
            if right.contains(c) {
                score += char_to_score(c as u8) as usize;
                break;
            }
        }
    }
    score
}

fn part2(rucksacks: &[&str]) -> usize {
    let mut score: usize = 0;
    for lines in rucksacks.chunks(3) {
        'outer: for c in lines[0].chars() {
            if lines[1].contains(c) && lines[2].contains(c) {
                score += char_to_score(c as u8) as usize;
                break 'outer;
            }
        }
    }
    score
}
