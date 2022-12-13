use std::cmp::Ordering;
use std::collections::VecDeque;
use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("13/input.txt").expect("File not found");

    println!("part1: {}", part1(&data));
    println!("part2: {}", part2(&data));

    println!("time: {:?}", start.elapsed());
}

fn compare(line1: &[char], line2: &[char]) -> Ordering {
    let mut q1: VecDeque<char> = line1.iter().copied().collect();
    let mut q2: VecDeque<char> = line2.iter().copied().collect();

    while !q1.is_empty() {
        // as long as they're identical, but NOT a number, move on
        while q1[0] == q2[0] && !q1[0].is_ascii_digit() {
            q1.pop_front();
            q2.pop_front();
        }

        // q1's list ran out
        if q1[0] == ']' {
            return Ordering::Less;
        }

        // q2's list ran out
        if q2[0] == ']' {
            return Ordering::Greater;
        }

        // q1 is a list, q2 isn't
        if q1[0] == '[' {
            let mut i = 0;
            while q2[i].is_ascii_digit() {
                i += 1;
            }
            q2.insert(i, ']');
            q2.insert(0, '[');
        } else if q2[0] == '[' {
            // q2 is a list, q1 isn't
            let mut i = 0;
            while q1[i].is_ascii_digit() {
                i += 1;
            }
            q1.insert(i, ']');
            q1.insert(0, '[');
        } else {
            // both are numbers
            let mut n1 = 0;
            while q1[0].is_ascii_digit() {
                let c = (q1.pop_front().unwrap() as u8 - b'0') as i32;
                n1 = n1 * 10 + c;
            }

            let mut n2 = 0;
            while q2[0].is_ascii_digit() {
                let c = (q2.pop_front().unwrap() as u8 - b'0') as i32;
                n2 = n2 * 10 + c;
            }

            // if both numbers are the same, just continue
            if n1 != n2 {
                if n1 < n2 {
                    return Ordering::Less;
                } else {
                    return Ordering::Greater;
                }
            }
        }
    }
    // lists are assumed to be distinct by order
    Ordering::Equal
}

fn part1(data: &str) -> usize {
    data.split("\n\n")
        .enumerate()
        .map(|(i, batch)| {
            let mut splits = batch.split('\n');
            let line1: Vec<char> = splits.next().unwrap().chars().collect();
            let line2: Vec<char> = splits.next().unwrap().chars().collect();

            if compare(&line1, &line2) == Ordering::Less {
                i + 1
            } else {
                0
            }
        })
        .sum()
}

fn part2(data: &str) -> usize {
    let mut packets: Vec<Vec<char>> = format!("{}\n[[2]]\n[[6]]", data)
        .split('\n')
        .filter(|l| !l.is_empty())
        .map(|l| l.chars().collect::<Vec<char>>())
        .collect();

    packets.sort_by(|l1, l2| compare(l1, l2));

    let two = packets
        .iter()
        .position(|l| l.iter().collect::<String>() == "[[2]]")
        .unwrap();

    let six = packets
        .iter()
        .position(|l| l.iter().collect::<String>() == "[[6]]")
        .unwrap();

    (two + 1) * (six + 1)
}
