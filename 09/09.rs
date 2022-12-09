use std::collections::HashSet;
use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("09/input.txt").expect("File not found");
    let instr: Vec<(&str, usize)> = data.split("\n")
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
                "U" => {
                    head = (head.0, head.1 + 1);
                },
                "D" => {
                    head = (head.0, head.1 - 1);
                },
                "L" => {
                    head = (head.0 - 1, head.1);
                },
                "R" => {
                    head = (head.0 + 1, head.1);
                },
                _ => {}
            }
            tail = drag_tail_behind(head, tail);
            visited.insert(tail);
        }
    }
    return visited.len();
}

fn drag_tail_behind(head: (i16, i16), tail: (i16, i16)) -> (i16, i16) {
    let diff_x = head.0 - tail.0;
    let diff_y = head.1 - tail.1;
    
    if diff_x.abs() <= 1 && diff_y.abs() <= 1 {
        return tail;
    }

    return (
        tail.0 + diff_x.signum(),
        tail.1 + diff_y.signum()
    );
}


fn part2(instructions: &Vec<(&str, usize)>, n_knots: usize) -> usize {
    let mut visited: HashSet<(i16, i16)> = HashSet::new();

    let mut head: (i16, i16) = (0, 0);
    let mut knots: Vec<(i16, i16)> = vec![(0, 0); n_knots];
    visited.insert(knots[n_knots - 1]);

    for &(direction, amount) in instructions.iter() {
        for _ in 0..amount {
            match direction {
                "U" => {
                    head = (head.0, head.1 + 1);
                },
                "D" => {
                    head = (head.0, head.1 - 1);
                },
                "L" => {
                    head = (head.0 - 1, head.1);
                },
                "R" => {
                    head = (head.0 + 1, head.1);
                },
                _ => {}
            }

            knots[0] = drag_tail_behind(head, knots[0]);
            for i in 1..n_knots {
                knots[i] = drag_tail_behind(knots[i - 1], knots[i]);
            }
            visited.insert(knots[n_knots - 1]);
        }
    }
    return visited.len();
}
