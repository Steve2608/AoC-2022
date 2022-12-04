use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let mut calories: Vec<i32> = fs::read_to_string("01/input.txt")
        .expect("File not found")
        .split("\n\n")
        .map(|elf| elf.split("\n").map(|num| num.parse::<i32>().unwrap()).sum())
        .collect();

    calories.sort_by(|a, b| b.cmp(a));
    calories.truncate(3);

    println!("part1: {}", calories[0]);
    println!("part2: {}", calories.iter().sum::<i32>());

    println!("time: {:?}", start.elapsed());
}