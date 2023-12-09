use std::collections::HashMap;
use std::io::BufRead;

fn iterate_string(s: String) -> i32 {
    let mut first_number: i32 = 0;
    let mut last_number: i32 = 0;
    for c in s.chars() {
        // if char is an integer
        if c.is_digit(10) {
            // convert char to integer

            if first_number == 0 {
                first_number = c.to_digit(10).unwrap() as i32;
            }

            last_number = c.to_digit(10).unwrap() as i32;
        }
    }

    return 10 * first_number + last_number;
}

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

fn main() {
    println!("{}", std::env::current_dir().unwrap().display());
    let lines: Vec<String> = load_text_file_lines("./input.txt");

    let sum_ints: i32 = lines
        .iter()
        .map(|line| iterate_string(line.to_string()))
        .sum();

    println!("problem 1 {}", sum_ints);

    let digit_map: HashMap<&str, i32> = HashMap::from([
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
        ("6", 6),
        ("7", 7),
        ("8", 8),
        ("9", 9),
        ("one", 1),
        ("two", 2),
        ("three", 3),
        ("four", 4),
        ("five", 5),
        ("six", 6),
        ("seven", 7),
        ("eight", 8),
        ("nine", 9),
    ]);

    let reverse_digit_map = digit_map
        .iter()
        .map(|(key, val)| (key.chars().rev().collect::<String>(), *val))
        .collect::<HashMap<_, _>>();

    let sum_ints_processed: i32 = lines
        .iter()
        .map(|line| {
            let line = line.to_string();
            let reversed_line = line.chars().rev().collect::<String>();

            let first_digit = digit_map
                .iter()
                .map(|(key, val)| (key, val, line.find(key)))
                .min_by_key(|v| v.2.unwrap_or(std::usize::MAX))
                .unwrap()
                .1;

            let second_digit = reverse_digit_map
                .iter()
                .map(|(key, val)| (key, val, reversed_line.find(key)))
                .min_by_key(|v| v.2.unwrap_or(std::usize::MAX))
                .unwrap()
                .1;

            return 10 * first_digit + second_digit;
        })
        .sum();

    println!("problem 2 {}", sum_ints_processed);
}
