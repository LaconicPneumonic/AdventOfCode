use std::io::BufRead;

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: std::io::BufReader<std::fs::File> = std::io::BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

fn predict_next_num(numbers: Vec<isize>) -> isize {
    let mut data: Vec<Vec<isize>> = Vec::new();

    data.push(numbers);

    let mut index = 0;

    loop {
        let diffs = (1..data[index].len())
            .map(|i| data[index][i] - data[index][i - 1])
            .collect::<Vec<_>>();

        data.push(diffs.clone());
        index += 1;

        if diffs.iter().all(|d| *d == 0) {
            break;
        }
    }

    for i in (1..index + 1).rev() {
        let new_val = data[i].iter().last().unwrap().clone();
        let next_val = data[i - 1].iter().last().unwrap().clone();
        data[i - 1].push(new_val + next_val);
    }

    return data[0].iter().last().unwrap().clone();
}

fn predict_prev_num(numbers: Vec<isize>) -> isize {
    let mut data: Vec<Vec<isize>> = Vec::new();

    data.push(numbers);

    let mut index = 0;

    loop {
        let diffs = (1..data[index].len())
            .map(|i| data[index][i] - data[index][i - 1])
            .collect::<Vec<_>>();

        data.push(diffs.clone());
        index += 1;

        if diffs.iter().all(|d| *d == 0) {
            break;
        }
    }

    let mut prev_val = 0;

    for i in (1..index + 1).rev() {
        let new_val = data[i - 1][0].clone();
        prev_val = new_val - prev_val;
    }

    return prev_val;
}

fn main() {
    let lines = load_text_file_lines("input.txt");

    let line_vecs = lines
        .iter()
        .map(|line| {
            line.split(" ")
                .map(|val| val.parse::<isize>().unwrap())
                .collect()
        })
        .collect::<Vec<Vec<isize>>>();

    let answer_one: isize = line_vecs
        .iter()
        .map(|line| predict_next_num(line.clone()))
        .sum();

    println!("answer1 = {:?}", answer_one);

    let answer_two: isize = line_vecs
        .iter()
        .map(|line| predict_prev_num(line.clone()))
        .sum();

    println!("answer2 = {:?}", answer_two);
}
