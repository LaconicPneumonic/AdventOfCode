use std::{
    collections::HashSet,
    io::{BufRead, BufReader},
};

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: BufReader<std::fs::File> = BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

type Point = (isize, isize);

fn parse_graph(lines: &Vec<String>) -> HashSet<Point> {
    let mut graph: HashSet<Point> = HashSet::new();

    for (row, line) in lines.iter().enumerate() {
        for (col, c) in line.chars().enumerate() {
            let row = row as isize;
            let col: isize = col as isize;
            if c == '#' {
                graph.insert((row, col));
            }
        }
    }

    return graph;
}

fn expand_graph(
    graph: &HashSet<Point>,
    total_rows: usize,
    total_cols: usize,
    expansion_num: isize,
) -> Vec<Point> {
    let occupied_rows = graph.iter().map(|(row, _)| row).collect::<HashSet<_>>();
    let occupied_cols = graph.iter().map(|(_, col)| col).collect::<HashSet<_>>();
    let mut final_node_set: Vec<Point> = Vec::new();

    for row in 0..total_rows {
        for col in 0..total_cols {
            let row = row as isize;
            let col: isize = col as isize;
            let point_exists = graph.contains(&(row, col));
            if point_exists {
                // could be an interval tree
                let row_adder = (expansion_num - 1)
                    * (0..row).filter(|i| !occupied_rows.contains(i)).count() as isize;
                let col_adder = (expansion_num - 1)
                    * (0..col).filter(|i| !occupied_cols.contains(i)).count() as isize;
                final_node_set.push((row + row_adder, col + col_adder));
            }
        }
    }
    return final_node_set;
}

fn compute_manhattan_distance(problem_graph: &Vec<(isize, isize)>) -> isize {
    let mut answer = 0;

    for (i, p1) in problem_graph.iter().enumerate() {
        for p2 in problem_graph[i + 1..].iter() {
            answer += (p2.0 - p1.0).abs() + (p2.1 - p1.1).abs();
        }
    }
    answer
}
fn main() {
    let lines = load_text_file_lines("./input.txt");
    let graph = parse_graph(&lines);

    let problem_one_graph = expand_graph(&graph, lines.len(), lines[0].len(), 2);

    let answer_one = compute_manhattan_distance(&problem_one_graph);

    println!("answer one: {:?}", answer_one);

    let problem_two_graph = expand_graph(&graph, lines.len(), lines[0].len(), 1000000);

    let answer_two = compute_manhattan_distance(&problem_two_graph);

    println!("answer two: {:?}", answer_two);
}
