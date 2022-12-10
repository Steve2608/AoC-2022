use std::fs;
use std::time::Instant;

fn main() {
    let start = Instant::now();

    let data: String = fs::read_to_string("10/input.txt").expect("File not found");
    let instructions: Vec<&str> = data.split('\n').collect();

    println!("part1: {}", part1(&instructions));
    println!("part2:\n{}", part2(&instructions, 40));

    println!("time: {:?}", start.elapsed());
}

fn part1(instructions: &[&str]) -> i32 {
    fn sig_stren(i: i32, x: i32, signal: &mut i32) {
        if (i - 20) % 40 == 0 {
            *signal += i * x;
        }
    }

    let mut i = 1;
    let mut x = 1;
    let mut signal = 0;
    for &instr in instructions {
        if instr == "noop" {
            i += 1;
        } else {
            i += 1;
            sig_stren(i, x, &mut signal);
            let n = instr.split(' ').last().unwrap().parse::<i32>().unwrap();
            i += 1;
            x += n;
        }
        sig_stren(i, x, &mut signal);
    }
    signal
}

fn part2(instructions: &[&str], crt_width: usize) -> String {
    fn shift_i(i: &mut i32, crt_width: usize) {
        *i = (*i + 1) % (crt_width as i32);
    }

    fn append_buffer(i: i32, sprite: i32, result: &mut String) {
        if sprite - 1 <= i && i <= sprite + 1  {
            result.push('#');
        } else {
            result.push('.');
        }
    }

    let mut i = 0;
    let mut sprite = 1;
    let mut result: String = "".to_string();
    for &instr in instructions {
        append_buffer(i, sprite, &mut result);

        if instr == "noop" {
            shift_i(&mut i, crt_width);
        } else {
            shift_i(&mut i, crt_width);
            append_buffer(i, sprite, &mut result);

            let n = instr.split(' ').last().unwrap().parse::<i32>().unwrap();
            shift_i(&mut i, crt_width);
            sprite += n;
        }
    }
    // not even mad
    for i in (crt_width..6*crt_width).step_by(crt_width).rev() {
        result.insert(i, '\n');
    }
    result
}
