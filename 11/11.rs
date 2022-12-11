use std::fs;
use std::time::Instant;

#[derive(Debug, Copy, Clone)]
enum Operation {
    Square(),
    Multiply(usize),
    Add(usize),
}

fn main() {
    let start = Instant::now();

    let monkeys = parse_monkeys(fs::read_to_string("11/input.txt").expect("File not found"));

    let p1 = part1(&monkeys, 20, 3);
    println!("part1: {}", p1);

    let p2 = part2(&monkeys, 10_000);
    println!("part2: {}", p2);

    println!("time: {:?}", start.elapsed());
}

fn parse_monkeys(data: String) -> Vec<(Vec<usize>, Operation, usize, usize, usize)> {
    let monkeys: Vec<(Vec<usize>, Operation, usize, usize, usize)> = data
        .split("\n\n")
        .map(|chunk| {
            /*
            Monkey 1:
                Starting items: 66, 50, 90, 53, 88, 85
                Operation: new = old + 3
                Test: divisible by 2
                    If true: throw to monkey 5
                    If false: throw to monkey 4
            */
            let lines: Vec<&str> = chunk.lines().map(|line| line.trim()).collect();
            let starting_items: Vec<usize> = lines[1]["Starting items: ".len()..lines[1].len()]
                .split(", ")
                .map(|num| num.parse::<usize>().unwrap())
                .collect();

            let operation_str: &str = lines[2].split("old ").nth(1).unwrap();
            let op: char = operation_str[0..1].chars().next().unwrap();
            let operand: &str = &operation_str[2..operation_str.len()];

            let operation = match operand {
                "old" => Operation::Square(),
                _ => {
                    let i = operand.parse::<usize>().unwrap();
                    if op == '+' {
                        Operation::Add(i)
                    } else {
                        Operation::Multiply(i)
                    }
                }
            };

            let div_by: Vec<&str> = lines[3].split(' ').collect();
            let if_true: Vec<&str> = lines[4].split(' ').collect();
            let if_false: Vec<&str> = lines[5].split(' ').collect();

            (
                starting_items,
                operation,
                div_by[div_by.len() - 1].parse::<usize>().unwrap(),
                if_true[if_true.len() - 1].parse::<usize>().unwrap(),
                if_false[if_false.len() - 1].parse::<usize>().unwrap(),
            )
        })
        .collect();

    monkeys
}

fn part1(
    monkeys: &[(Vec<usize>, Operation, usize, usize, usize)],
    rounds: usize,
    worry_decay: usize
) -> usize {
    fn step(
        monkeys: &[(Vec<usize>, Operation, usize, usize, usize)],
        src: &mut [Vec<usize>],
        dst: &mut [Vec<usize>],
        tmp: &mut [Vec<usize>],
        inspec: &mut [usize],
        worry_decay: usize
    ) -> bool {
        let mut has_tmp = false;
        for (i, monkey) in src.iter().enumerate() {
            inspec[i] += monkey.len();

            let m = &monkeys[i];
            for item in monkey.iter() {
                let worry = match m.1 {
                    Operation::Square() => item * item,
                    Operation::Add(n) => item + n,
                    Operation::Multiply(n) => item * n,
                } / worry_decay;

                let target = match worry % m.2 {
                    0 => m.3,
                    _ => m.4,
                };

                if target < i {
                    dst[target].push(worry);
                } else {
                    tmp[target].push(worry);
                    has_tmp = true;
                }
            }
        }
        has_tmp
    }

    let mut dst: Vec<Vec<usize>> = vec![vec![]; monkeys.len()];
    let mut tmp: Vec<Vec<usize>> = vec![vec![]; monkeys.len()];
    let mut src: Vec<Vec<usize>> = monkeys.iter().map(|m| m.0.clone()).collect();
    let mut inspec: Vec<usize> = vec![0; monkeys.len()];

    for _ in 0..rounds {
        let mut has_tmp = step(monkeys, &mut src, &mut dst, &mut tmp, &mut inspec, worry_decay);

        while has_tmp {
            src = tmp;
            tmp = vec![vec![]; monkeys.len()];
            has_tmp = step(monkeys, &mut src, &mut dst, &mut tmp, &mut inspec, worry_decay);
        }
        src = dst;
        tmp = vec![vec![]; monkeys.len()];
        dst = vec![vec![]; monkeys.len()];
    }

    inspec.sort_by(|a, b| b.cmp(a));
    (inspec[0] as usize) * (inspec[1] as usize)
}

fn get_lcm(monkeys: &[(Vec<usize>, Operation, usize, usize, usize)]) -> usize {
    let mut lcm = monkeys
        .iter()
        .map(|m| m.2)
        .reduce(|accum: usize, item: usize| accum * item)
        .unwrap();
    
    monkeys.iter().map(|m| m.2).for_each(|mult| {
        if (lcm / mult) % mult == 0 {
            lcm /= mult;
        }
    });

    lcm
}

fn part2(
    monkeys: &[(Vec<usize>, Operation, usize, usize, usize)],
    rounds: usize
) -> usize {
    fn step(
        monkeys: &[(Vec<usize>, Operation, usize, usize, usize)],
        src: &mut [Vec<usize>],
        dst: &mut [Vec<usize>],
        tmp: &mut [Vec<usize>],
        inspec: &mut [usize],
        lcm: usize
    ) -> bool {
        let mut has_tmp = false;
        for (i, monkey) in src.iter().enumerate() {
            inspec[i] += monkey.len();

            let m = &monkeys[i];
            for item in monkey.iter() {
                let worry = match m.1 {
                    Operation::Square() => item * item,
                    Operation::Add(n) => item + n,
                    Operation::Multiply(n) => item * n,
                } % lcm;

                let target = match worry % m.2 {
                    0 => m.3,
                    _ => m.4,
                };

                if target < i {
                    dst[target].push(worry);
                } else {
                    tmp[target].push(worry);
                    has_tmp = true;
                }
            }
        }
        has_tmp
    }

    let mut dst: Vec<Vec<usize>> = vec![vec![]; monkeys.len()];
    let mut tmp: Vec<Vec<usize>> = vec![vec![]; monkeys.len()];
    let mut src: Vec<Vec<usize>> = monkeys.iter().map(|m| m.0.clone()).collect();
    let mut inspec: Vec<usize> = vec![0; monkeys.len()];
    let lcm = get_lcm(monkeys);

    for _ in 0..rounds {
        let mut has_tmp = step(monkeys, &mut src, &mut dst, &mut tmp, &mut inspec, lcm);

        while has_tmp {
            src = tmp;
            tmp = vec![vec![]; monkeys.len()];
            has_tmp = step(monkeys, &mut src, &mut dst, &mut tmp, &mut inspec, lcm);
        }
        src = dst;
        tmp = vec![vec![]; monkeys.len()];
        dst = vec![vec![]; monkeys.len()];
    }

    inspec.sort_by(|a, b| b.cmp(a));
    (inspec[0] as usize) * (inspec[1] as usize)
}
