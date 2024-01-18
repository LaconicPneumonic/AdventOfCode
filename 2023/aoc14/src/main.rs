use core::fmt;
use std::collections::HashMap;
use std::fmt::Debug;
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader};

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: BufReader<std::fs::File> = BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct RockMap {
    rows: usize,
    cols: usize,
    rocks: HashMap<(usize, usize), char>,
}

impl fmt::Display for RockMap {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut ret = String::new();
        for row in 0..self.rows {
            for col in 0..self.cols {
                let rock = self.rocks.get(&(row, col));
                if rock.is_some() {
                    ret.push(*rock.unwrap());
                } else {
                    ret.push('.');
                }
            }
            ret.push('\n');
        }
        write!(f, "{}", ret)
    }
}

impl Hash for RockMap {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.to_string().hash(state);
    }
}
fn parse_rock_map(lines: &Vec<String>) -> RockMap {
    let mut rocks = HashMap::new();
    for (row, line) in lines.iter().enumerate() {
        for (col, c) in line.chars().enumerate() {
            if c != '.' {
                rocks.insert((row, col), c);
            }
        }
    }
    return RockMap {
        rows: lines.len(),
        cols: lines[0].len(),
        rocks: rocks,
    };
}

fn tilt_rock_map(map: &RockMap, direction: (isize, isize)) -> RockMap {
    let mut point_order = if direction.1 == 0 {
        (0..map.rows)
            .map(|row| (0..map.cols).map(move |col| (row, col)))
            .flatten()
            .collect::<Vec<_>>()
    } else {
        (0..map.cols)
            .map(|col| (0..map.rows).map(move |row| (row, col)))
            .flatten()
            .collect::<Vec<_>>()
    };

    let mut new_rocks = HashMap::new();

    if direction.1 == 1 || direction.0 == 1 {
        point_order.reverse()
    }
    for (row, col) in point_order {
        let rock_val = map.rocks.get(&(row, col));

        if rock_val.is_none() {
            continue;
        }

        if *rock_val.unwrap() == '#' {
            new_rocks.insert((row, col), '#');
            continue;
        }

        let mut curr_rock_position = (row as isize, col as isize);

        loop {
            let potential_rock_position = (
                curr_rock_position.0 as isize + direction.0,
                curr_rock_position.1 as isize + direction.1,
            );

            if potential_rock_position.0 < 0
                || potential_rock_position.0 >= map.rows as isize
                || potential_rock_position.1 < 0
                || potential_rock_position.1 >= map.cols as isize
            {
                break;
            }

            let potential_space = new_rocks.get(&(
                potential_rock_position.0 as usize,
                potential_rock_position.1 as usize,
            ));

            if potential_space.is_some() {
                break;
            }

            curr_rock_position = potential_rock_position;
        }

        new_rocks.insert(
            (curr_rock_position.0 as usize, curr_rock_position.1 as usize),
            'O',
        );
    }

    return RockMap {
        rows: map.rows,
        cols: map.cols,
        rocks: new_rocks,
    };
}

fn calculate_weight(map: &RockMap) -> usize {
    let mut weight = 0;
    for ((row, col), val) in map.rocks.iter() {
        if *val == 'O' {
            weight += map.rows - row;
        }
    }
    return weight;
}
fn main() {
    let lines = load_text_file_lines("input.txt");
    let rock_map = parse_rock_map(&lines);

    let new_rock_map = tilt_rock_map(&rock_map, (-1, 0));

    let weight = calculate_weight(&new_rock_map);
    println!("answer 1: {}", weight);

    let target_cycles = 1_000_000_000;

    let mut curr_rock_map = rock_map;

    let mut seen = HashMap::new();

    let mut weight_array = vec![];

    let mut cycle_count = 0;
    loop {
        for direction in vec![(-1, 0), (0, -1), (1, 0), (0, 1)] {
            curr_rock_map = tilt_rock_map(&curr_rock_map, direction);
        }

        if seen.contains_key(&curr_rock_map) {
            break;
        }

        seen.insert(curr_rock_map.clone(), cycle_count);
        weight_array.push(calculate_weight(&curr_rock_map));
        cycle_count += 1;
    }

    let cycle_start = seen.get(&curr_rock_map).unwrap();

    println!(
        "answer 2: {}",
        weight_array
            [cycle_start + (target_cycles - cycle_start - 1) % (weight_array.len() - cycle_start)]
    );
}
