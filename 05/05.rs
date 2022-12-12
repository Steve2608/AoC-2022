use std::fs;
use std::time::Instant;

static N_STACKS: usize = 9;
static N_INSTR_PARTS: usize = 3;

type Instr = u8;

fn main() {
    let start = Instant::now();

    let (data, instructions): (Vec<String>, Vec<Instr>) = parse_input();

    println!("part1: {}", part1(&data, &instructions));
    println!("part1: {}", part2(&data, &instructions));

    println!("time: {:?}", start.elapsed());
}

fn parse_input() -> (Vec<String>, Vec<Instr>) {
    let content: String = fs::read_to_string("05/input.txt").expect("File not found");

    let parts: Vec<&str> = content.split("\n\n").collect();
    let initial: &str = parts[0];
    let instr: &str = parts[1];

    let mut data: Vec<String> = vec![String::new(); N_STACKS];
    let mut lines: Vec<&str> = initial.lines().collect();
    // remove numbered line
    lines.pop();
    for line in lines {
        for i in 0..N_STACKS {
            let c: char = line.as_bytes()[1 + i * 4] as char;
            if c != ' ' {
                data[i] = format!("{}{}", c, data[i]);
            }
        }
    }

    let instructions: Vec<Instr> = instr
        .lines()
        .flat_map(|line| {
            let parts: Vec<&str> = line.split(' ').collect();
            // only take the numbers
            [parts[1], parts[3], parts[5]]
        })
        .map(|num| num.parse::<Instr>().unwrap())
        .collect();

    (data, instructions)
}

fn part1(data: &[String], instructions: &[Instr]) -> String {
    let mut containers = data.to_vec();

    for instr in instructions.chunks(N_INSTR_PARTS) {
        let cnt = instr[0];
        let src = (instr[1] - 1) as usize;
        let dst = (instr[2] - 1) as usize;

        for _ in 1..=cnt {
            let c: char = containers[src].pop().unwrap();
            containers[dst] = format!("{}{}", containers[dst], c);
        }
    }

    containers
        .iter()
        .map(|c| c.chars().last().unwrap())
        .collect::<Vec<char>>()
        .into_iter()
        .collect()
}

fn part2(data: &[String], instructions: &[Instr]) -> String {
    let mut containers = data.to_vec();

    for instr in instructions.chunks(N_INSTR_PARTS) {
        let cnt = instr[0] as usize;
        let src = (instr[1] - 1) as usize;
        let dst = (instr[2] - 1) as usize;

        let mut buf: Vec<char> = vec!['\0'; cnt];
        for i in 0..cnt {
            let c: char = containers[src].pop().unwrap();
            buf[cnt - 1 - i] = c;
        }
        containers[dst] = format!("{}{}", containers[dst], buf.into_iter().collect::<String>());
    }

    containers
        .iter()
        .map(|c| c.chars().last().unwrap())
        .collect::<Vec<char>>()
        .into_iter()
        .collect()
}
