use criterion::{black_box, criterion_group, criterion_main, Criterion};

use rustc_hash::FxHashMap;
use std::{
    collections::HashMap,
    io::{BufRead, BufReader},
};

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: BufReader<std::fs::File> = BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}
fn super_fast_dp(record: &Vec<char>, rules: &Vec<usize>) -> usize {
    let mut dp: Vec<Vec<usize>> = vec![vec![0; record.len()]; rules.len()];

    for record_index in 0..record.len() - rules[0] {
        let rule_end = record_index + rules[0];

        if record[record_index..rule_end]
            .iter()
            .all(|c| *c == '#' || *c == '?')
            && (rule_end == record.len() || record[rule_end] != '#')
            && (record_index == 0 || record[record_index - 1] != '#')
        {
            dp[0][record_index] = 1;
        } else if record[record_index] == '#'
            || (record_index != 0 && record[record_index - 1] == '#')
        {
            break;
        }
    }
    // println!("");

    for rule_index in 1..rules.len() {
        let max_ending_point =
            record.len() - rules[rule_index..].iter().sum::<usize>() - rules.len()
                + (rule_index + 1)
                + 1;

        let valid_starting_indexes = dp[rule_index - 1]
            .iter()
            .enumerate()
            .filter(|(_, v)| **v != 0)
            .map(|(i, _)| i + rules[rule_index - 1] + 1)
            .collect::<Vec<_>>();

        // println!("{:?}", valid_starting_indexes);
        for start in valid_starting_indexes {
            let mut assigned_anything = false;
            let mut fail_terminal_check = true;
            // println!("{} {} {}", start, rule_index, start - rules[rule_index - 1]);

            for record_index in start..max_ending_point {
                let rule_end = record_index + rules[rule_index];

                if record[record_index..rule_end]
                    .iter()
                    .all(|c| *c == '#' || *c == '?')
                    && (rule_end == record.len() || record[rule_end] != '#')
                    && (record_index == 0 || record[record_index - 1] != '#')
                // check whether I went to the previous val
                {
                    assigned_anything = true;

                    fail_terminal_check = rule_index == rules.len() - 1
                        && rule_end < record.len()
                        && record[rule_end..].iter().any(|v| *v == '#');

                    // dp[rule_index][record_index] = dp[rule_index - 1]
                    //     [..start - rules[rule_index - 1]]
                    //     .iter()
                    //     .sum::<usize>();

                    dp[rule_index][record_index] +=
                        dp[rule_index - 1][start - rules[rule_index - 1] - 1];

                    // println!("{} {}", dp[rule_index][record_index], record_index);
                } else if record[record_index] == '#'
                    || (record_index != 0 && record[record_index - 1] == '#')
                {
                    // println!("{} {}", rule_index, record_index);
                    break;
                }
            }

            if !assigned_anything || fail_terminal_check {
                dp[rule_index - 1][start - rules[rule_index - 1] - 1] = 0;
            }
        }
    }

    // dp.iter().for_each(|r| println!("{:?}", r));
    // println!("");

    for r_start in 0..record.len() {
        if dp[rules.len() - 1][r_start] != 0 {
            let record_index = r_start + rules[rules.len() - 1];
            let not_valid =
                record_index < record.len() && record[record_index..].iter().any(|v| *v == '#');

            // println!("{}", record[record_index..].iter().collect::<String>());
            if not_valid {
                dp[rules.len() - 1][r_start] = 0;
            }
        }
    }

    // dp.iter().for_each(|r| println!("{:?}", r));

    return dp[dp.len() - 1].iter().sum();
}

fn criterion_benchmark(c: &mut Criterion) {
    let lines = load_text_file_lines("C:\\Dev\\AdventOfCode2022\\2023\\aoc12\\src\\input.txt");

    let answer_multiplier = 1;

    let (raw_line, raw_rules) = lines[0].split_once(" ").unwrap();

    let mut line_vec = (0..answer_multiplier)
        .map(|_| raw_line.chars().chain(['?'].into_iter()))
        .flatten()
        .collect::<Vec<_>>();

    line_vec.pop();

    let parsed_rules = (0..answer_multiplier)
        .map(|_| raw_rules.split(",").map(|s| s.parse::<usize>().unwrap()))
        .flatten()
        .collect::<Vec<usize>>();

    let mut cnt_calls = 0;

    c.bench_function("fib 20", |b| {
        b.iter(|| super_fast_dp(black_box(&line_vec), black_box(&parsed_rules)))
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
