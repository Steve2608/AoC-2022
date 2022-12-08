use std::fs;
use std::collections::HashMap;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let sizes: HashMap<String, usize> = file_system("07/input.txt");

    let p1: usize = sizes.values().filter(|size| **size <= 100_000).sum();
    println!("part1: {}", p1);

    let free_size: usize = sizes["/"] - (70_000_000 - 30_000_000);
    let p2: usize = *sizes.values().filter(|size| **size >= free_size).min().unwrap();
    println!("part2: {}", p2);

    println!("time: {:?}", start.elapsed());
}

fn file_system(path: &str) -> HashMap<String, usize> {
    let data: String = fs::read_to_string(path).expect("File not found");
    let mut sizes: HashMap<String, usize> = HashMap::new();
    let mut cwd: Vec<String> = vec!["".to_string()];

    for line in data.split("\n") {
        let parts: Vec<&str> = line.split(" ").collect();
        match parts[0..2] {
            ["$", "cd"] => {
                match parts[2] {
                    "/" => {
                        cwd = vec!["/".to_string()];
                    },
                    ".." => {
                        cwd.pop();
                    },
                    _ => {
                        cwd.push(parts[2].to_string());
                    }
                }
            },
            [_, _] => {
                let num = parts[0].parse::<usize>();
                match num {
                    Ok(val) => {
                        let mut dir = "/".to_string();
                        *sizes.entry(dir.to_string()).or_insert(0) += val;

                        // update size in cwd and all parents
                        for part in cwd.iter().skip(1) {
                            dir.push_str(part);
                            dir.push_str("/");
                            *sizes.entry(dir.to_string()).or_insert(0) += val;
                        }
                    },
                    _ => {}
                }
            },
            _ => {}
        }
    }
    return sizes
}
