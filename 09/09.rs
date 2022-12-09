use std::collections::HashSet;
use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("09/input.txt").expect("File not found");
    let instr: Vec<(&str, usize)> = data
        .split('\n')
        .map(|line| {
            let parts: Vec<&str> = line.split(' ').collect();

            let direction: &str = parts[0];
            let n = parts[1].parse::<usize>().unwrap();

            (direction, n)
        })
        .collect();

    let (p1, p2) = part12(&instr, 9);
    println!("part1: {}", p1);
    println!("part2: {}", p2);

    println!("time: {:?}", start.elapsed());
}

fn part12(instructions: &[(&str, usize)], n_knots: usize) -> (usize, usize) {
    let mut visited1: HashSet<(i16, i16)> = HashSet::new();
    let mut visited2: HashSet<(i16, i16)> = HashSet::new();

    let mut knots: Vec<(i16, i16)> = vec![(0, 0); n_knots + 1];
    visited1.insert(knots[n_knots]);
    visited2.insert(knots[n_knots]);

    for &(direction, amount) in instructions.iter() {
        for _ in 0..amount {
            match direction {
                "U" => knots[0].1 += 1,
                "D" => knots[0].1 -= 1,
                "L" => knots[0].0 -= 1,
                "R" => knots[0].0 += 1,
                _ => unreachable!(),
            }

            // drag knots behind
            for i in 1..=n_knots {
                let diff_x = knots[i - 1].0 - knots[i].0;
                let diff_y = knots[i - 1].1 - knots[i].1;

                if diff_x.abs() > 1 || diff_y.abs() > 1 {
                    knots[i].0 += diff_x.signum();
                    knots[i].1 += diff_y.signum();
                }
            }
            visited1.insert(knots[1]);
            visited2.insert(knots[n_knots]);
        }
    }
    (visited1.len(), visited2.len())
}
