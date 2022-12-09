use std::collections::HashSet;
use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("09/input.txt").expect("File not found");
    let instr: Vec<(&str, usize)> = data
        .split("\n")
        .map(|line| {
            let parts: Vec<&str> = line.split(" ").collect();

            let direction: &str = parts[0];
            let n = parts[1].parse::<usize>().unwrap();

            return (direction, n);
        })
        .collect();

    println!("part1: {}", part1(&instr));
    println!("part2: {}", part2(&instr, 9));

    println!("time: {:?}", start.elapsed());
}

fn part1(instructions: &Vec<(&str, usize)>) -> usize {
    let mut visited: HashSet<(i16, i16)> = HashSet::new();

    let mut head = (0, 0);
    let mut tail = (0, 0);
    visited.insert(tail);

    for &(direction, amount) in instructions.iter() {
        for _ in 0..amount {
            match direction {
                "U" => head.1 += 1,
                "D" => head.1 -= 1,
                "L" => head.0 -= 1,
                "R" => head.0 += 1,
                _ => unreachable!()
            }

            // drag tail behind
            let diff_x = head.0 - tail.0;
            let diff_y = head.1 - tail.1;
        
            if diff_x.abs() > 1 || diff_y.abs() > 1 {
                tail.0 += diff_x.signum();
                tail.1 += diff_y.signum();
            }
            visited.insert(tail);
        }
    }
    return visited.len();
}

fn part2(instructions: &Vec<(&str, usize)>, n_knots: usize) -> usize {
    let mut visited: HashSet<(i16, i16)> = HashSet::new();

    let mut knots: Vec<(i16, i16)> = vec![(0, 0); n_knots + 1];
    visited.insert(knots[n_knots]);

    for &(direction, amount) in instructions.iter() {
        for _ in 0..amount {
            match direction {
                "U" => knots[0].1 += 1,
                "D" => knots[0].1 -= 1,
                "L" => knots[0].0 -= 1,
                "R" => knots[0].0 += 1,
                _ => unreachable!()
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
            visited.insert(knots[n_knots]);
        }
    }
    return visited.len();
}
