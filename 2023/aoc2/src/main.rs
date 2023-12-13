use std::cmp;
use std::collections::HashMap;
use std::io::BufRead;

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

fn parse_game_state(game_state: &str) -> (usize, HashMap<&str, usize>) {
    let game_pulls: Vec<&str> = game_state.split(":").collect();

    let game_id = game_pulls[0][5..].parse::<usize>().unwrap();

    let game_pulls = game_pulls[1]
        .split("; ")
        .map(|pull| {
            pull.trim()
                .split(", ")
                .map(|dice| {
                    let num_color: Vec<&str> = dice.trim().split(" ").collect();

                    return (num_color[1], num_color[0].parse::<usize>().unwrap());
                })
                .collect::<HashMap<&str, usize>>()
        })
        .reduce(|acc, pull| {
            acc.keys()
                .chain(pull.keys())
                .map(|key: &&str| {
                    let acc_val = acc.get(key).unwrap_or(&0);
                    let pull_val = pull.get(key).unwrap_or(&0);

                    return (*key, cmp::max(*acc_val, *pull_val));
                })
                .collect::<HashMap<&str, usize>>()
        });

    return (game_id, game_pulls.unwrap());
}

fn main() {
    let lines: Vec<String> = load_text_file_lines("./input.txt");

    let game_state_one: HashMap<&str, usize> =
        HashMap::from([("red", 12), ("green", 13), ("blue", 14)]);

    let answer: usize = lines
        .iter()
        .map(|line| parse_game_state(line))
        .filter(|id_state| {
            let (_, state) = id_state;
            game_state_one.iter().all(|(color, num)| {
                let state_num = state.get(color).unwrap_or(&0);
                return state_num <= num;
            })
        })
        .map(|(id, _)| id)
        .sum();

    println!("problem 1 {}", answer);

    let answer_two: usize = lines
        .iter()
        .map(|line| parse_game_state(line))
        .map(|id_state| {
            let (_, state) = id_state;
            game_state_one
                .keys()
                .map(|color| *state.get(color).unwrap_or(&0))
                .reduce(|acc, val| acc * val)
                .unwrap_or(0)
        })
        .sum();

    println!("problem 2 {}", answer_two)
}
