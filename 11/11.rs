use std::fs;
use std::time::Instant;

#[derive(Debug, Copy, Clone)]
enum Operation {
    Square(),
    Multiply(usize),
    Add(usize),
}

#[derive(Debug, Clone)]
struct Monkey {
    items: Vec<usize>,
    operation: Operation,
    divisible_by: usize,
    if_true_pass_to: usize,
    if_false_pass_to: usize,
}

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("11/input.txt").expect("File not found");
    let monkeys = parse_monkeys(data);

    let p1 = solve(monkeys.clone(), 20, 3);
    println!("part1: {}", p1);

    let p2 = solve(monkeys, 10_000, 1);
    println!("part2: {}", p2);

    println!("time: {:?}", start.elapsed());
}

fn parse_monkeys(data: String) -> Vec<Monkey> {
    let monkeys: Vec<Monkey> = data
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

            let m = Monkey {
                items: starting_items,
                operation: operation,
                divisible_by: div_by[div_by.len() - 1].parse::<usize>().unwrap(),
                if_true_pass_to: if_true[if_true.len() - 1].parse::<usize>().unwrap(),
                if_false_pass_to: if_false[if_false.len() - 1].parse::<usize>().unwrap(),
            };
            m
        })
        .collect();

    monkeys
}

fn solve(monkeys: Vec<Monkey>, rounds: usize, worry_decay: usize) -> usize {
    let mut inspection_counts: Vec<usize> = vec![0; monkeys.len()];
    let mut post_proc: Vec<Vec<usize>> = vec![vec![]; monkeys.len()];
    let mut monkey_working = monkeys;

    let lcm: usize = get_lcm(&monkey_working);

    for _ in 0..rounds {
        let mut copy: Vec<Monkey> = monkey_working.iter().map(|m| empty_monkey(m)).collect();
        for (i_monkey, monkey) in monkey_working.iter().enumerate() {
            for item in monkey.items.iter() {
                let worry: usize = get_worry(*item, monkey.operation, lcm, worry_decay);

                let target = match worry % monkey.divisible_by {
                    0 => monkey.if_true_pass_to,
                    _ => monkey.if_false_pass_to,
                };

                if target > i_monkey {
                    post_proc[target].push(worry);
                } else {
                    copy[target].items.push(worry);
                }
                inspection_counts[i_monkey] += 1;
            }
        }

        while post_proc.iter().any(|v| v.len() > 0) {
            post_proc = post_process(
                &mut copy,
                &post_proc,
                &mut inspection_counts,
                worry_decay,
                lcm,
            );
        }
        monkey_working = copy;
    }
    inspection_counts.sort_by(|a, b| b.cmp(a));
    (inspection_counts[0] as usize) * (inspection_counts[1] as usize)
}

fn post_process(
    monkeys: &mut [Monkey],
    post_proc: &[Vec<usize>],
    inspection_counts: &mut [usize],
    worry_decay: usize,
    lcm: usize,
) -> Vec<Vec<usize>> {
    let mut still_process: Vec<Vec<usize>> = vec![vec![]; monkeys.len()];
    for (i_monkey, v) in post_proc.iter().enumerate() {
        for item in v {
            let worry: usize = get_worry(*item, monkeys[i_monkey].operation, lcm, worry_decay);

            let target = match worry % monkeys[i_monkey].divisible_by {
                0 => monkeys[i_monkey].if_true_pass_to,
                _ => monkeys[i_monkey].if_false_pass_to,
            };
            if target > i_monkey {
                still_process[target].push(worry);
            } else {
                monkeys[target].items.push(worry);
            }
            inspection_counts[i_monkey] += 1;
        }
    }
    still_process
}

fn get_lcm(monkeys: &[Monkey]) -> usize {
    monkeys
        .iter()
        .map(|m| m.divisible_by)
        .reduce(|accum: usize, item: usize| match accum % item {
            0 => accum,
            _ => accum * item,
        })
        .unwrap()
}

fn empty_monkey(monkey: &Monkey) -> Monkey {
    Monkey {
        items: vec![],
        operation: monkey.operation,
        divisible_by: monkey.divisible_by,
        if_true_pass_to: monkey.if_true_pass_to,
        if_false_pass_to: monkey.if_false_pass_to,
    }
}

fn get_worry(item: usize, op: Operation, lcm: usize, worry_decay: usize) -> usize {
    let worry = match op {
        Operation::Square() => item * item,
        Operation::Add(i) => item + i,
        Operation::Multiply(i) => item * i,
    };
    (worry / worry_decay) % lcm
}
