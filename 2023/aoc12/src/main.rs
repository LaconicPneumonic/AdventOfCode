use std::io::{BufRead, BufReader};

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

        for start in valid_starting_indexes {
            let mut assigned_anything = false;
            let mut fail_terminal_check = true;

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

                    dp[rule_index][record_index] +=
                        dp[rule_index - 1][start - rules[rule_index - 1] - 1];

                    // println!("{} {}", dp[rule_index][record_index], record_index);
                } else if record[record_index] == '#'
                    || (record_index != 0 && record[record_index - 1] == '#')
                {
                    break;
                }
            }

            if !assigned_anything || fail_terminal_check {
                dp[rule_index - 1][start - rules[rule_index - 1] - 1] = 0;
            }
        }
    }

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

    return dp[dp.len() - 1].iter().sum();
}
fn super_fast(
    record: &Vec<char>,
    record_index: usize,
    rules: &Vec<usize>,
    cnt_calls: &mut usize,
    rule_index: usize,
    depth: usize,
) -> usize {
    if rule_index == rules.len() {
        // -1 on the record index since we skipped over the last char in our recursive step
        let not_valid =
            record_index < record.len() && record[record_index - 1..].iter().any(|v| *v == '#');

        return if not_valid { 0 } else { 1 };
    }

    let mut count = 0;

    let max_ending_point = record.len() - rules[rule_index..].iter().sum::<usize>() - rules.len()
        + (rule_index + 1)
        + 1;

    for index in record_index..max_ending_point {
        let rule_end = index + rules[rule_index];

        if record[index..rule_end]
            .iter()
            .all(|c| *c == '#' || *c == '?')
            && (rule_end == record.len() || record[rule_end] != '#')
            && (index == 0 || record[index - 1] != '#')
        {
            count += super_fast(
                record,
                rule_end + 1,
                rules,
                cnt_calls,
                rule_index + 1,
                depth + 1,
            );
        } else if record[index] == '#' || (index != 0 && record[index - 1] == '#') {
            break;
        }
    }

    return count;
}

fn can_place(
    record: &Vec<char>,
    rules: &Vec<usize>,
    record_index: usize,
    rule_index: usize,
) -> bool {
    // println!("{} {}", record_index, rule_index);

    let can_place_group = (record_index + rules[rule_index]) <= record.len()
        && record[record_index..record_index + rules[rule_index]]
            .iter()
            .all(|c| *c == '#' || *c == '?');

    let final_char_is_terminal = record_index + rules[rule_index] >= record.len()
        || record[record_index + rules[rule_index]] == '.'
        || record[record_index + rules[rule_index]] == '?';

    let prefix_char_is_terminal =
        record_index == 0 || record[record_index - 1] == '.' || record[record_index - 1] == '?';

    let last_rule_rest_valid = rule_index < rules.len() - 1
        || record
            .iter()
            .skip(record_index + rules[rule_index])
            .all(|c| *c == '.' || *c == '?');

    let ret = can_place_group
        && final_char_is_terminal
        && prefix_char_is_terminal
        && last_rule_rest_valid;

    return ret;
}

#[allow(dead_code)]
fn fast_count(record: &Vec<char>, rules: &Vec<usize>) -> usize {
    let mut state: Vec<Vec<_>> = (0..rules.len())
        .map(|_| (0..record.len()).map(|_| 0).collect())
        .collect();

    for r in 0..rules.len() {
        let min_starting_point = rules[..r].iter().sum::<usize>() + r;

        // let min_starting_point = 0;

        // let max_ending_point = record
        //     .len()
        //     .checked_sub(rules[r..].iter().sum::<usize>() + rules.len() - r)
        //     .unwrap_or(record.len());

        let mut first_success = false;

        for c in min_starting_point..record.len() {
            if record[c] == '.' {
                continue;
            }

            let ok = can_place(record, rules, c, r);
            let terminal_check = r < rules.len() - 1
                || record
                    .iter()
                    .skip(c + rules[r])
                    .all(|v| *v == '.' || *v == '?');

            let valid_position = terminal_check && ok;
            // state[r][c] += if valid_position { 1 } else { 0 };

            if min_starting_point == 9 {
                // println!(
                //     "{:?} {:?} {:?}",
                //     record[c],
                //     record[c..c + 1 + rules[r]].iter().collect::<String>(),
                //     rules[r]
                // );
            }

            if valid_position {
                first_success = true;
                // fill in the future rules
                if r == 0 || c == 0 {
                    state[r][c] = 1;
                } else {
                    // println!("{:?} {:?} {:?}", c, rules, rules[r - 1]);

                    for record_index in 0..(c.checked_sub(rules[r - 1]).unwrap_or(0)) {
                        state[r][c] += state[r - 1][record_index];
                    }
                }
            } else if record[c] == '#' && first_success {
                break;
            }
        }
        println!("{:>2} {:?}", min_starting_point, state[r]);
    }

    // state.iter().for_each(|r| println!("{:?}", r));

    return state[state.len() - 1].iter().sum();
}

fn main() {
    let lines = load_text_file_lines("input.txt");

    let answer_1: usize = lines
        .iter()
        .map(|l| {
            let (raw_line, raw_rules) = l.split_once(" ").unwrap();

            let line_vec = raw_line.chars().collect::<Vec<char>>();
            let parsed_rules = raw_rules
                .split(",")
                .map(|s| s.parse::<usize>().unwrap())
                .collect::<Vec<usize>>();

            let ret = super_fast_dp(&line_vec.clone(), &parsed_rules);

            return ret;
        })
        .sum();

    println!("answer_1: {}", answer_1);

    let answer_multiplier = 5;

    let answer_2: usize = lines
        .iter()
        .map(|l| {
            let (raw_line, raw_rules) = l.split_once(" ").unwrap();

            let mut line_vec = (0..answer_multiplier)
                .map(|_| raw_line.chars().chain(['?'].into_iter()))
                .flatten()
                .collect::<Vec<char>>();

            line_vec.pop();

            let parsed_rules = (0..answer_multiplier)
                .map(|_| raw_rules.split(",").map(|s| s.parse::<usize>().unwrap()))
                .flatten()
                .collect::<Vec<usize>>();

            let ret = super_fast_dp(&line_vec, &parsed_rules);

            return ret;
        })
        .sum();

    println!("answer_2: {}", answer_2);
}
