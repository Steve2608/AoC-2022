use std::fs;
use std::time::Instant;

type Cal = u32;

fn main() {
    let start = Instant::now();

    let mut calories: Vec<Cal> = fs::read_to_string("01/input.txt")
        .expect("File not found")
        .split("\n\n")
        .map(|elf| elf.lines().map(|num| num.parse::<Cal>().unwrap()).sum())
        .collect();

    calories.sort_by(|a, b| b.cmp(a));
    calories.truncate(3);

    println!("part1: {}", calories[0]);
    println!("part2: {}", calories.iter().sum::<Cal>());

    println!("time: {:?}", start.elapsed());
}
