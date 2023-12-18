use std::io::BufRead;

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: std::io::BufReader<std::fs::File> = std::io::BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

fn main() {
    let lines: Vec<String> = load_text_file_lines("./input.txt");

    let prefix_length = lines[0].split(":").nth(0).unwrap().len() + 1;

    let game_state = lines.iter().map(|l| {
        let left_right: Vec<Vec<usize>> = l[prefix_length..]
            .split("|")
            .map(|v| v.trim())
            .map(|v| {
                v.split_whitespace()
                    .map(|n| n.parse::<usize>().unwrap())
                    .collect()
            })
            .collect();

        (
            left_right.get(0).unwrap().clone(),
            left_right.get(1).unwrap().clone(),
        )
    });

    // println!(
    //     "{:?}",
    //     game_state
    //         .clone()
    //         .collect::<Vec<(Vec<usize>, Vec<usize>)>>()
    // );

    let answer_1: usize = game_state
        .clone()
        .map(|(winning_numbers, card_numbers)| {
            let line_answer = winning_numbers.iter().fold(1, |agg, next| {
                if card_numbers.iter().any(|c| c == next) {
                    agg * 2
                } else {
                    agg
                }
            }) / 2;

            // println!("{} {:?} {:?}", line_answer, winning_numbers, card_numbers);
            return line_answer;
        })
        .sum();

    print!("Answer 1: {}\n", answer_1);

    let mut copy_count: Vec<usize> = vec![1; lines.len()];

    let answer_2: usize = game_state
        .clone()
        .enumerate()
        .map(|(game_num, (winning_numbers, card_numbers))| {
            let total_wins = winning_numbers
                .iter()
                .filter(|&next| card_numbers.iter().any(|c| c == next))
                .count();

            // println!(
            //     "{} {} {:?} {:?}",
            //     game_num, total_wins, winning_numbers, card_numbers
            // );

            for i in (game_num + 1)..(game_num + total_wins + 1) {
                copy_count[i] += copy_count[game_num];
            }

            // println!("{:?}", copy_count);

            return copy_count[game_num];
        })
        .sum();

    // println!("{:?}", copy_count);
    print!("Answer 2: {}\n", answer_2);
}
