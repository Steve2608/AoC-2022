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
        // as long as they're identical, move on
        while q1[0] == q2[0] && !('0' <= q1[0] && q1[0] <= '9') {
            q1.pop_front();
            q2.pop_front();
        }
        if q1[0] == ']' || q2[0] == ',' {
            return Ordering::Less;
        } else if q1[0] == ',' || q2[0] == ']' {
            return Ordering::Greater;
        } else if q1[0] == '[' {
            let mut i = 0;
            while '0' <= q2[i] && q2[i] <= '9' {
                i += 1;
            }
            if i > 0 {
                // wrap first number
                q2.insert(i, ']');
                q2.insert(0, '[');
            }
            continue;
        } else if q2[0] == '[' {
            let mut i = 0;
            while '0' <= q1[i] && q1[i] <= '9' {
                i += 1;
            }
            if i > 0 {
                // wrap first number
                q1.insert(i, ']');
                q1.insert(0, '[');
            }
            continue;
        } else {
            let mut n1 = 0;
            while '0' <= q1[0] && q1[0] <= '9' {
                let c = (q1.pop_front().unwrap() as u8 - b'0') as i32;
                n1 *= 10;
                n1 += c;
            }
            let mut n2 = 0;
            while '0' <= q2[0] && q2[0] <= '9' {
                let c = (q2.pop_front().unwrap() as u8 - b'0') as i32;
                n2 *= 10;
                n2 += c;
            }
            if n1 != n2 {
                if n1 < n2 {
                    return Ordering::Less;
                } else {
                    return Ordering::Greater;
                }
            }
        }
    }
    panic!()
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
        .unwrap()
        + 1;
    let six = packets
        .iter()
        .position(|l| l.iter().collect::<String>() == "[[6]]")
        .unwrap()
        + 1;
    two * six
}
