use std::{
    collections::{HashMap, HashSet, VecDeque},
    io::{BufRead, BufReader},
};

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: BufReader<std::fs::File> = BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

type Point = (isize, isize);

fn parse_graph(lines: &Vec<String>) -> (Point, HashMap<Point, Vec<Point>>, HashMap<Point, char>) {
    let mut start = (0, 0);

    let mut graph: HashMap<Point, Vec<Point>> = HashMap::new();
    let mut point_to_val: HashMap<Point, char> = HashMap::new();

    for (row, line) in lines.iter().enumerate() {
        for (col, c) in line.chars().enumerate() {
            let row = row as isize;
            let col: isize = col as isize;
            let neighbors = match c {
                '|' => vec![(row - 1, col), (row + 1, col)],
                '-' => vec![(row, col - 1), (row, col + 1)],
                'L' => vec![(row - 1, col), (row, col + 1)],
                'J' => vec![(row - 1, col), (row, col - 1)],
                '7' => vec![(row + 1, col), (row, col - 1)],
                'F' => vec![(row + 1, col), (row, col + 1)],
                _ => vec![],
            };

            if c == 'S' {
                start = (row, col);
            } else {
                graph.insert((row, col), neighbors);
            }

            point_to_val.insert((row, col), c);
        }
    }

    // find everything that points to start

    let mut start_neighbors = graph
        .iter()
        .filter(|(_, neighbors)| neighbors.contains(&start))
        .map(|(point, _)| *point)
        .collect::<Vec<_>>();

    start_neighbors.sort_by_key(|n| n.0);
    start_neighbors.sort_by_key(|n| n.1);

    let start_neighbor_str = start_neighbors
        .iter()
        .flat_map(|p| vec![p.0 - start.0, p.1 - start.1])
        .map(|v| v.to_string())
        .collect::<Vec<_>>()
        .join("");

    let start_str = match start_neighbor_str.as_str() {
        "-1010" => '|',
        "0-101" => '-',
        "-1001" => 'L',
        "-100-1" => 'J',
        "0-110" => '7',
        "0110" => 'F',
        _ => panic!("unknown start: {:?}", start_neighbor_str),
    };

    graph.insert(start, start_neighbors);

    point_to_val.insert(start, start_str);

    return (start, graph, point_to_val);
}

fn breadth_first_search(start: Point, graph: HashMap<Point, Vec<Point>>) -> HashMap<Point, usize> {
    let mut stack = VecDeque::from([(0, start)]);

    let mut seen: HashSet<Point> = HashSet::from([start]);

    let mut max = 0;

    let mut ret: HashMap<Point, usize> = HashMap::new();

    while stack.len() != 0 {
        let (dist, curr) = stack.pop_front().unwrap();

        // println!("{:?} {:?}", dist, curr);

        ret.insert(curr, dist);

        max = dist.max(max);

        let neighbors = graph.get(&curr).unwrap();

        for n in neighbors.iter() {
            if !seen.contains(n) {
                seen.insert(n.clone());
                stack.push_back((dist + 1, n.clone()));
            }
        }
    }

    return ret;
}

fn main() {
    let lines = load_text_file_lines("input.txt");

    let (start, graph, point_to_val) = parse_graph(&lines);

    let answer_1 = breadth_first_search(start, graph.clone());

    println!("answer_1: {:?}", answer_1.values().max().unwrap());

    let non_loop_points = graph.keys().filter(|p| !answer_1.contains_key(p));

    let loop_points_by_row: HashMap<isize, Vec<&Point>> = answer_1.keys().map(|p| (p.0, p)).fold(
        HashMap::new(),
        |mut acc: HashMap<_, _>, (row, p)| {
            acc.entry(row).or_insert(Vec::new()).push(p);

            acc
        },
    );

    let answer_two = non_loop_points
        .filter(|p1| {
            loop_points_by_row
                .get(&p1.0)
                .unwrap_or(&Vec::new())
                .iter()
                .filter(|v| v.1 > p1.1)
                .map(|p| {
                    let graph_char = point_to_val.get(p).unwrap();
                    // assign arbitrary direction to loop when using ray casting algorithm
                    // F and 7 are determined to go clockwise and - does not count towards boundary counting
                    if vec!['F', '-', '7'].contains(graph_char) {
                        0
                    } else {
                        1
                    }
                })
                .sum::<isize>()
                % 2
                == 1
        })
        .collect::<Vec<_>>();

    println!("answer_two: {:?}", answer_two.len());
}
