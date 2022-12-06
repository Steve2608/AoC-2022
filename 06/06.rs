use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("06/input.txt").expect("File not found");

    println!("part1: {}", solve(&data, 4));    
    println!("part1: {}", solve(&data, 14));    

    println!("time: {:?}", start.elapsed());
}

fn solve(data: &String, n_distinct: usize) -> i32 {
    let bytes = data.as_bytes();
    'outer: for i in n_distinct..bytes.len() {
        // for-loop go brrrrr
        for j in i - n_distinct..i {
            for k in i - n_distinct..i {
                if j != k && bytes[j] == bytes[k] {
                    continue 'outer;
                }
            }
        }
        return i as i32;
    }
    return -1;
}
