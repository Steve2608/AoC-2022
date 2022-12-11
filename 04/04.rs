use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("04/input.txt").expect("File not found");

    let ranges: Vec<i32> = data
        .lines()
        .flat_map(|line| {
            line.split(',')
                .flat_map(|tuple| tuple.split('-').map(|num| num.parse::<i32>().unwrap()))
        })
        .collect();

    println!("part1: {}", part1(&ranges));
    println!("part2: {}", part2(&ranges));

    println!("time: {:?}", start.elapsed());
}

fn part1(ranges: &[i32]) -> i32 {
    let mut count = 0;
    for r in ranges.chunks(4) {
        // r[0] - r[1], r[2] - r[3]
        if (r[0] <= r[2] && r[3] <= r[1]) || (r[2] <= r[0] && r[1] <= r[3]) {
            count += 1;
        }
    }
    count
}

fn part2(ranges: &[i32]) -> i32 {
    let mut count = 0;
    for r in ranges.chunks(4) {
        // r[0] - r[1], r[2] - r[3]
        if (r[0] <= r[2] && r[2] <= r[1]) || (r[2] <= r[0] && r[0] <= r[3]) {
            count += 1;
        }
    }
    count
}
