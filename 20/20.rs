use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: Vec<i64> = fs::read_to_string("20/input.txt")
        .expect("File not found")
        .lines()
        .map(|num| num.parse::<i64>().unwrap())
        .collect();

    println!("part1: {}", solve(&data, 0, 1));
    println!("part2: {}", solve(&data, 811589153, 10));
    println!("time: {:?}", start.elapsed());
}

fn solve(data: &[i64], encryption_key: i64, n_mixing: usize) -> i64 {
    let mut i_zero = data.iter().position(|&x| x == 0).unwrap();
    let numbers: Vec<(usize, i64)> = if encryption_key != 0 {
        data.iter()
            .map(|&x| x * encryption_key)
            .enumerate()
            .collect()
    } else {
        data.iter().copied().enumerate().collect()
    };

    let mut ring: Vec<(usize, i64)> = numbers.clone();
    let n: i64 = numbers.len() as i64;
    for _ in 0..n_mixing {
        for key_num in numbers.iter() {
            let mut i: i64 = ring.iter().position(|entry| entry == key_num).unwrap() as i64;
            i += ring.remove(i as usize).1;

            if !(-n <= i && i < n) {
                i %= n - 1;
            }
            if -n <= i && i < 0 {
                i += n - 1;
            }

            ring.insert(i as usize, *key_num);
        }
    }

    i_zero = ring.iter().position(|&elem| elem == (i_zero, 0)).unwrap();
    (1000..=3000)
        .step_by(1000)
        .map(|i| ring[(i_zero + i) % ring.len()].1)
        .sum()
}
