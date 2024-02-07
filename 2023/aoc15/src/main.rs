use std::{
    collections::HashMap,
    io::{BufRead, BufReader},
};

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: BufReader<std::fs::File> = BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

fn hash_string(instr: &str) -> usize {
    return instr
        .chars()
        .map(|v| v as usize)
        .fold(0, |agg, curr_val| ((agg + curr_val) * 17) % 256);
}

fn main() {
    let lines = load_text_file_lines("./input.txt");

    let code = lines.first().unwrap().split(",").collect::<Vec<_>>();

    let answer_1 = code.iter().map(|l| hash_string(l)).sum::<usize>();

    let mut prev_map: HashMap<String, String> = HashMap::new();
    let mut next_map: HashMap<String, String> = HashMap::new();
    let mut values: HashMap<String, usize> = HashMap::new();

    let mut box_to_head: HashMap<usize, String> = HashMap::new();
    let mut box_to_tail: HashMap<usize, String> = HashMap::new();

    for i in 0..256 {
        box_to_head.insert(i, format!("B{}H", i));
        box_to_tail.insert(i, format!("B{}T", i));

        next_map.insert(format!("B{}H", i), format!("B{}T", i));
        prev_map.insert(format!("B{}T", i), format!("B{}H", i));
    }

    for line in code.iter() {
        let split_code = line.split_once("=");

        if split_code.is_some() {
            let (key, value) = split_code
                .map(|(a, b)| (a.to_string(), b.parse::<usize>().unwrap()))
                .unwrap();

            let hash = hash_string(key.as_str());

            // println!("{} {} {}", key, value, hash);

            let exists = prev_map.contains_key(&key) || next_map.contains_key(&key);

            if !exists {
                let psuedo_tail = box_to_tail.get(&hash).unwrap();
                let tail = prev_map.get(psuedo_tail).unwrap();

                next_map.insert(tail.clone(), key.clone());
                prev_map.insert(key.clone(), tail.clone());

                next_map.insert(key.clone(), psuedo_tail.clone());
                prev_map.insert(psuedo_tail.clone(), key.clone());
            }

            values.insert(key.clone(), value);
        } else {
            let subtract_key = line.strip_suffix('-').unwrap().to_string();

            let exists =
                prev_map.contains_key(&subtract_key) || next_map.contains_key(&subtract_key);

            if exists {
                let before_key = prev_map.get(&subtract_key).unwrap().clone();
                let after_key = next_map.get(&subtract_key).unwrap().clone();
                next_map.insert(before_key.clone(), after_key.clone());
                prev_map.insert(after_key.clone(), before_key.clone());
                prev_map.remove(&subtract_key);
                next_map.remove(&subtract_key);
            }
        }
    }

    println!("answer_1 {}", answer_1);

    let mut answer_2 = 0;

    for box_id in box_to_head.keys() {
        print!("Box {}: ", box_id);

        let mut curr = box_to_head.get(&box_id).unwrap().clone();
        let mut idx = 1;
        let mut total = 0;

        loop {
            print!("[{} {:?}] ", curr, values.get(&curr).unwrap_or(&0));

            if values.contains_key(&curr) {
                total += (box_id + 1) * idx * values.get(&curr).unwrap();
                idx += 1;
            }

            if !next_map.contains_key(&curr) {
                break;
            }

            curr = next_map.get(&curr).unwrap().clone();
        }

        answer_2 += total;

        println!(" total={}", total);
    }

    println!("answer_2 {}", answer_2);
}
