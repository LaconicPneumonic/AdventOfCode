use std::{collections::HashMap, io::BufRead};

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: std::io::BufReader<std::fs::File> = std::io::BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

fn game_one(
    directions: &Vec<char>,
    mapping: HashMap<&str, (&str, &str)>,
    first_node: &str,
    last_node: &str,
) -> i32 {
    let mut index = 0;
    let mut counter = 0;

    let mut curr_node = first_node;

    while curr_node != last_node {
        let direction = directions[index];

        let next_node = match direction {
            'L' => mapping.get(curr_node).unwrap().0,
            'R' => mapping.get(curr_node).unwrap().1,
            _ => panic!("unknown direction: {:?}", direction),
        };

        index = (index + 1) % directions.len();

        curr_node = next_node;
        counter += 1;
    }
    counter
}

fn sub_game_two(
    directions: &Vec<char>,
    mapping: HashMap<&str, (&str, &str)>,
    first_node: &str,
) -> usize {
    let mut index = 0;
    let mut counter = 0;

    let mut curr_node = first_node;

    while curr_node.chars().last().unwrap() != 'Z' {
        let direction = directions[index];

        let next_node = match direction {
            'L' => mapping.get(curr_node).unwrap().0,
            'R' => mapping.get(curr_node).unwrap().1,
            _ => panic!("unknown direction: {:?}", direction),
        };

        index = (index + 1) % directions.len();

        curr_node = next_node;
        counter += 1;
    }
    counter
}

fn greatest_common_divisor(a: usize, b: usize) -> usize {
    let mut a = a;
    let mut b = b;

    while b != 0 {
        let temp = b;
        b = a % b;
        a = temp;
    }

    a
}

fn main() {
    let lines = load_text_file_lines("input.txt");

    let directions = &lines[0].chars().collect::<Vec<_>>();

    let mapping = lines[2..]
        .iter()
        .map(|l| {
            let line_vec = l.trim().split(" = ").collect::<Vec<_>>();

            let node = line_vec[0].trim();

            let neigbors_it = line_vec[1].trim().split(", ");
            let neighbors_left = neigbors_it
                .clone()
                .nth(0)
                .unwrap()
                .strip_prefix("(")
                .unwrap();
            let neighbors_right = neigbors_it
                .clone()
                .nth(1)
                .unwrap()
                .strip_suffix(")")
                .unwrap();

            return (node, (neighbors_left, neighbors_right));
        })
        .collect::<HashMap<_, _>>();

    let answer_one = game_one(directions, mapping.clone(), "AAA", "ZZZ");

    println!("answer_one: {:?}", answer_one);

    let answer_two = mapping
        .clone()
        .into_keys()
        .filter(|n| n.chars().last().unwrap() == 'A')
        .map(|v| sub_game_two(directions, mapping.clone(), v))
        .collect::<Vec<_>>();

    let gcd = answer_two
        .iter()
        .cloned()
        .reduce(|agg, cur| greatest_common_divisor(agg, cur))
        .unwrap();

    // lowest common multiple = (a * b) / gcd(a, b)
    let answer_two = answer_two
        .iter()
        .cloned()
        .map(|v| v / gcd)
        .reduce(|agg, cur| agg * cur)
        .unwrap()
        * gcd;

    println!("answer_two: {:?}", answer_two);
}
