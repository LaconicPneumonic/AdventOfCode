use std::{
    collections::{HashMap, HashSet},
    io::BufRead,
};

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let mut lines: Vec<String> = Vec::new();
    let file = std::fs::File::open(filename).unwrap();
    let reader: std::io::BufReader<std::fs::File> = std::io::BufReader::new(file);
    reader
        .lines()
        .for_each(|line: Result<String, std::io::Error>| {
            lines.push(line.unwrap());
        });
    return lines;
}

fn split_line(line: &String) -> Vec<String> {
    let mut ret: Vec<String> = Vec::new();

    let mut accum = "".to_owned();
    for c in line.chars() {
        if c.is_numeric() {
            accum.push_str(c.to_string().as_str());
        } else {
            if accum.len() > 0 {
                ret.push(accum.clone());
                accum = "".to_owned();
            }

            ret.push(c.to_string());
        }
    }

    if accum.len() > 0 {
        ret.push(accum);
    }

    return ret;
}

#[derive(Debug)]
struct Point {
    x: isize,
    y: isize,
}

fn split_line_to_position(line: &Vec<String>, row: isize) -> Vec<(String, Point, Point)> {
    let mut ret: Vec<(String, Point, Point)> = Vec::new();

    let mut left = 0;

    for c in line.iter() {
        if c.parse::<usize>().is_ok() {
            ret.push((
                c.to_string(),
                Point { x: left, y: row },
                Point {
                    x: left + c.len() as isize - 1,
                    y: row,
                },
            ));
        } else if c != "." {
            ret.push((
                c.to_string(),
                Point {
                    x: left - 1,
                    y: row - 1,
                },
                Point {
                    x: left + 1,
                    y: row + 1,
                },
            ));
        }

        left += c.len() as isize;
    }

    return ret;
}

fn main() {
    let lines: Vec<String> = load_text_file_lines("./input.txt");

    // let rows = lines.len();
    // let cols = lines[0].len();

    let items: Vec<(String, Point, Point)> = lines
        .iter()
        .map(|line| split_line(line))
        .enumerate()
        .flat_map(|(row, line)| split_line_to_position(&line, row as isize))
        .collect();

    let numeric_items = items
        .iter()
        .filter(|(c, _, _)| c.parse::<usize>().is_ok())
        .map(|(c, p1, p2)| (c.parse::<usize>().unwrap(), p1, p2));

    let symbol_items = items.iter().filter(|(c, _, _)| !c.parse::<usize>().is_ok());

    // numeric_items
    //     .clone()
    //     .for_each(|(c, p1, p2)| println!("{} {:?} {:?}", c, p1, p2));
    // symbol_items
    //     .clone()
    //     .for_each(|(c, p1, p2)| println!("{} {:?} {:?}", c, p1, p2));
    let mut accumulator = 0;

    let mut seen_nums: HashSet<String> = HashSet::new();

    let mut gear_to_nums: HashMap<String, Vec<usize>> = HashMap::new();

    for (num, a0, a1) in numeric_items.clone() {
        for (symbol, b0, b1) in symbol_items.clone() {
            let w = a1.x >= b0.x && b1.x >= a0.x;
            let u = b1.x >= a0.x && a1.x >= b0.x;
            let m = a1.y >= b0.y && b1.y >= a0.y;
            let v = b1.y >= a0.y && a1.y >= b0.y;

            // println!("{} {} {} {} {}", num, symbol, w, m, v);

            if (w || u) && (m || v) {
                let key = format!("{:?}", (num, a0, a1));
                let symbol_key = format!("{:?}", (symbol, b0, b1));
                // println!("{} {} ", num, symbol);

                if symbol == "*" {
                    gear_to_nums
                        .entry(symbol_key)
                        .or_insert(Vec::new())
                        .push(num);
                }

                if !seen_nums.contains(&key) {
                    accumulator += num;
                    seen_nums.insert(key);
                }
            }
        }
    }

    println!("problem 1 {}", accumulator);

    println!(
        "problem 2 {:?}",
        gear_to_nums
            .values()
            .filter(|v| v.len() == 2)
            .map(|v| v[0] * v[1])
            .sum::<usize>()
    );
}
