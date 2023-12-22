use std::io::BufRead;

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: std::io::BufReader<std::fs::File> = std::io::BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

fn solve_race(race_time_int: usize, best_distance_int: usize) -> (usize, usize) {
    let race_time = race_time_int as f64;
    let best_distance = best_distance_int as f64;

    let plus_solution =
        (-1.0 * race_time + (race_time.powf(2.0) - 4.0 * best_distance).sqrt()) / -2.0;

    let minus_solution =
        (-1.0 * race_time - (race_time.powf(2.0) - 4.0 * best_distance).sqrt()) / -2.0;

    return (
        (plus_solution + 1.0).floor() as usize,
        (minus_solution - 1.0).ceil() as usize,
    );
}

fn main() {
    let lines: Vec<String> = load_text_file_lines("./input.txt");

    let time_line = lines[0]
        .strip_prefix("Time:")
        .unwrap()
        .split_whitespace()
        .map(|s| s.parse::<usize>().unwrap());

    let distance_line = lines[1]
        .strip_prefix("Distance:")
        .unwrap()
        .split_whitespace()
        .map(|s| s.parse::<usize>().unwrap());

    let answer_one = time_line
        .zip(distance_line)
        .map(|(race_time, best_distance)| solve_race(race_time, best_distance))
        .map(|(min, max)| max - min + 1)
        .reduce(|acc, v| acc * v);

    println!("answer one: {:?}", answer_one.unwrap());

    let long_race_time = lines[0]
        .strip_prefix("Time:")
        .unwrap()
        .split_whitespace()
        .collect::<String>()
        .parse::<usize>()
        .unwrap();

    let long_race_distance = lines[1]
        .strip_prefix("Distance: ")
        .unwrap()
        .split_whitespace()
        .collect::<String>()
        .parse::<usize>()
        .unwrap();

    let (lower_bound, upper_bound) = solve_race(long_race_time, long_race_distance);
    println!("answer two: {:?}", upper_bound - lower_bound + 1);
}
