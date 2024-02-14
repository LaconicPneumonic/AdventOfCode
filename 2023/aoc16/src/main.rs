use std::{
    collections::{HashMap, HashSet},
    io::{BufRead, BufReader},
};

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: BufReader<std::fs::File> = BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

type Point = (isize, isize);
type Pose = (Point, u8);

static DIRECTIONS: [(isize, isize); 4] = [(0, 1), (1, 0), (0, -1), (-1, 0)];

fn parse_graph(lines: &Vec<String>) -> HashMap<Point, String> {
    let mut graph: HashMap<Point, String> = HashMap::new();

    for (row, line) in lines.iter().enumerate() {
        for (col, c) in line.chars().enumerate() {
            let row = row as isize;
            let col: isize = col as isize;
            graph.insert((row, col), c.to_string());
        }
    }

    return graph;
}

fn simulate_light(graph: &HashMap<Point, String>, pose: &Pose) -> (HashSet<Point>, HashSet<Pose>) {
    let mut curr_poses = HashSet::from([pose.clone()]);

    let mut visited: HashSet<Pose> = HashSet::new();
    let mut energized: HashSet<Point> = HashSet::new();

    loop {
        let val = curr_poses
            .iter()
            .map(|curr| {
                let mut ret: Vec<Pose> = Vec::new();

                let (curr_point, direction) = curr.clone();

                let next_point = (
                    curr_point.0 + DIRECTIONS[direction as usize].0,
                    curr_point.1 + DIRECTIONS[direction as usize].1,
                );

                if !graph.contains_key(&next_point) {
                    // println!("exited");
                    return ret;
                }

                energized.insert(next_point);

                if visited.contains(&(next_point, direction)) {
                    // println!("exited");
                    return ret;
                }

                visited.insert((next_point, direction));

                let node_type = graph.get(&next_point).unwrap();

                //  [(0, 1), (1, 0), (0, -1), (-1, 0)];
                match node_type.as_str() {
                    "." => ret.push((next_point, (direction))),
                    "|" => {
                        if direction % 2 == 1 {
                            ret.push((next_point, (direction)));
                        } else {
                            ret.push((next_point, 1));
                            ret.push((next_point, 3));
                        }
                    }
                    "-" => {
                        if direction % 2 == 0 {
                            ret.push((next_point, (direction)));
                        } else {
                            ret.push((next_point, 0));
                            ret.push((next_point, 2));
                        }
                    }
                    "\\" => {
                        let new_direction = match direction {
                            0 => 1,
                            1 => 0,
                            2 => 3,
                            3 => 2,
                            _ => panic!("invalid direction"),
                        };

                        ret.push((next_point, new_direction));
                    }
                    "/" => {
                        let new_direction = match direction {
                            0 => 3,
                            1 => 2,
                            2 => 1,
                            3 => 0,
                            _ => panic!("invalid direction"),
                        };

                        ret.push((next_point, new_direction));
                    }
                    _ => {
                        panic!("invalid node type");
                    }
                }

                return ret;
            })
            .flatten()
            .collect::<HashSet<_>>();

        curr_poses = val;

        if curr_poses.len() == 0 {
            break;
        }
    }

    return (energized, visited);
}

fn main() {
    let lines = load_text_file_lines("./input.txt");

    let graph = parse_graph(&lines);

    let (energized, visited) = simulate_light(&graph, &((0, -1), 0));

    // print_visited(&lines, visited);

    let answer_1 = energized.len();

    let rows = lines.len();
    let cols = lines[0].len();

    println!("answer one: {:?}", answer_1);

    let starting_points = (0..cols)
        .flat_map(|c: usize| [((-1, c as isize), 1u8), ((rows as isize, c as isize), 3u8)])
        .chain((0..rows).flat_map(|r| {
            [
                ((r as isize, -1 as isize), 0),
                ((r as isize, cols as isize), 2),
            ]
        }));

    let (pose, (energized_2, visited_2)) = starting_points
        .map(|pose| (pose, simulate_light(&graph, &pose)))
        .max_by_key(|v| v.1 .0.len())
        .unwrap();

    // print_visited(&lines, visited_2);

    println!("answer two: {:?} {:?}", pose, energized_2.len());
}

fn print_visited(lines: &Vec<String>, visited_2: HashSet<((isize, isize), u8)>) {
    for (row, line) in lines.iter().enumerate() {
        let new_line = line
            .chars()
            .enumerate()
            .map(|(col, c)| {
                let row = row as isize;
                let col: isize = col as isize;

                let valid = [0u8, 1, 2, 3]
                    .iter()
                    .filter(|direction| visited_2.contains(&((row, col), **direction)))
                    .collect::<Vec<_>>();

                if valid.len() > 1 {
                    return valid.len().to_string();
                }

                if valid.len() == 1 {
                    return [">", "v", "<", "^"]
                        .get(*valid[0] as usize)
                        .unwrap()
                        .to_string();
                }

                return c.to_string();
            })
            .collect::<Vec<_>>()
            .join("");

        println!("{}", new_line)
    }
}
