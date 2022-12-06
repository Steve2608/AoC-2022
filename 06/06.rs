use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("06/input.txt").expect("File not found");

    let p1 = solve(&data, 4, 0);
    println!("part1: {}", p1);    
    println!("part1: {}", solve(&data, 14, (p1 - 4) as usize));    

    println!("time: {:?}", start.elapsed());
}

fn solve(data: &String, n_distinct: usize, offset: usize) -> i32 {
    let bytes = data.as_bytes();
    'outer: for i in (offset + n_distinct)..bytes.len() {
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
