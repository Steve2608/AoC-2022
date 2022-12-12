use std::fs;
use std::time::Instant;

type Range = u8;

fn main() {
    let start = Instant::now();

    let ranges: Vec<Range> = fs::read_to_string("04/input.txt")
        .expect("File not found")
        .lines()
        .flat_map(|line| {
            line.split(',')
                .flat_map(|tuple| tuple.split('-').map(|num| num.parse::<Range>().unwrap()))
        })
        .collect();

    println!("part1: {}", part1(&ranges));
    println!("part2: {}", part2(&ranges));

    println!("time: {:?}", start.elapsed());
}

fn part1(ranges: &[Range]) -> usize {
    let mut count = 0;
    for r in ranges.chunks(4) {
        // r[0] - r[1], r[2] - r[3]
        if (r[0] <= r[2] && r[3] <= r[1]) || (r[2] <= r[0] && r[1] <= r[3]) {
            count += 1;
        }
    }
    count
}

fn part2(ranges: &[Range]) -> usize {
    let mut count = 0;
    for r in ranges.chunks(4) {
        // r[0] - r[1], r[2] - r[3]
        if (r[0] <= r[2] && r[2] <= r[1]) || (r[2] <= r[0] && r[0] <= r[3]) {
            count += 1;
        }
    }
    count
}
