use std::{collections::HashMap, io::BufRead};

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: std::io::BufReader<std::fs::File> = std::io::BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

#[derive(Clone, Debug)]
struct Node {
    name: String,
    id: f64,
}

#[derive(Clone, Debug)]
struct NodeRange {
    name: String,
    range: (f64, f64),
}

type Graph = HashMap<String, String>;
type GraphRange = HashMap<(String, String), (Vec<(f64, f64)>, Vec<(f64, f64)>)>;

fn find_location(graph: &Graph, graph_range: &GraphRange, seed: Node) -> Node {
    let mut curr_node = seed;

    while curr_node.name != "location" {
        let destination_type = graph.get(&curr_node.name).unwrap();

        let (source_range, destination_range) = graph_range
            .get(&(curr_node.name.clone(), destination_type.clone()))
            .unwrap();

        curr_node = source_range
            .iter()
            .zip(destination_range.iter())
            .find(|(src, _)| src.0 <= curr_node.id && curr_node.id <= src.1)
            .map(|correct_bound| {
                let (src, dest) = correct_bound;

                Node {
                    name: destination_type.clone(),
                    id: ((curr_node.id - src.0) / (src.1 - src.0)) * (dest.1 - dest.0) + dest.0,
                }
            })
            .unwrap_or(Node {
                name: destination_type.clone(),
                id: curr_node.id,
            });
    }

    return curr_node;
}

fn find_location_range(graph: &Graph, graph_range: &GraphRange, seed: NodeRange) -> Vec<NodeRange> {
    let mut curr_node_ranges = Vec::from([seed]);

    while curr_node_ranges.len() != 0 && curr_node_ranges.iter().all(|v| v.name != "location") {
        let node_type = curr_node_ranges[0].name.clone();
        let destination_type = graph.get(&node_type).unwrap();

        let (source_range, destination_range) = graph_range
            .get(&(node_type, destination_type.clone()))
            .unwrap();

        curr_node_ranges = curr_node_ranges
            .iter()
            .flat_map(|node_range| {
                let mut overlapping_sections = source_range
                    .iter()
                    .zip(destination_range.iter())
                    .filter(|(src, _)| {
                        let w = node_range.range.1 >= src.0 && src.1 >= node_range.range.0;
                        let u = src.1 >= node_range.range.0 && node_range.range.1 >= src.0;

                        w || u
                    })
                    .map(|(src, dest)| {
                        let overlapping_range = (
                            f64::max(src.0, node_range.range.0),
                            f64::min(src.1, node_range.range.1),
                        );

                        NodeRange {
                            name: destination_type.clone(),
                            range: (
                                ((overlapping_range.0 - src.0) / (src.1 - src.0))
                                    * (dest.1 - dest.0)
                                    + dest.0,
                                ((overlapping_range.1 - src.0) / (src.1 - src.0))
                                    * (dest.1 - dest.0)
                                    + dest.0,
                            ),
                        }
                    })
                    .collect::<Vec<_>>();

                let min_range = source_range
                    .iter()
                    .min_by(|a, b| a.0.partial_cmp(&b.0).unwrap())
                    .unwrap();
                let max_range = source_range
                    .iter()
                    .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
                    .unwrap();

                // assuming all ranges are continuous, so get max and min overlaps

                if node_range.range.0 < min_range.0 {
                    let overlapping_range = (
                        node_range.range.0,
                        f64::min(min_range.0, node_range.range.1),
                    );

                    let ret = NodeRange {
                        name: destination_type.clone(),
                        range: overlapping_range,
                    };

                    overlapping_sections.push(ret);
                }

                if node_range.range.1 > max_range.1 {
                    let overlapping_range = (
                        f64::max(node_range.range.0, max_range.1),
                        node_range.range.1,
                    );

                    let ret = NodeRange {
                        name: destination_type.clone(),
                        range: overlapping_range,
                    };

                    overlapping_sections.push(ret);
                }

                return overlapping_sections;
            })
            .collect::<Vec<_>>();
    }

    return curr_node_ranges;
}

fn create_graph(lines: &Vec<String>) -> (Graph, GraphRange) {
    let mut index = 2;

    let mut graph: Graph = HashMap::new();
    let mut graph_range: GraphRange = HashMap::new();

    while index < lines.len() {
        let map_line = &lines[index];

        let map_result = map_line
            .strip_suffix(" map:")
            .unwrap()
            .split("-to-")
            .map(|v| v.to_string())
            .collect::<Vec<String>>();

        let curr_map = (map_result[0].clone(), map_result[1].clone());

        index += 1;

        let mut source_range_vec: Vec<(f64, f64)> = Vec::new();
        let mut destination_range_vec: Vec<(f64, f64)> = Vec::new();

        while index < lines.len() && lines[index] != "" {
            let range_lines = lines[index]
                .split(" ")
                .map(|v| v.parse::<f64>().unwrap())
                .collect::<Vec<_>>();

            let destination_range = (range_lines[0], range_lines[0] + range_lines[2]);
            let source_range = (range_lines[1], range_lines[1] + range_lines[2]);

            source_range_vec.push(source_range);
            destination_range_vec.push(destination_range);

            index += 1;
        }

        index += 1;

        graph.insert(curr_map.0.clone(), curr_map.1.clone());

        graph_range.insert(curr_map, (source_range_vec, destination_range_vec));
    }
    (graph, graph_range)
}

fn main() {
    let lines: Vec<String> = load_text_file_lines("./input.txt");

    let seeds = lines[0]
        .strip_prefix("seeds: ")
        .unwrap_or("")
        .split(" ")
        .map(|v| v.parse::<f64>().unwrap());

    let (graph, graph_range) = create_graph(&lines);

    let answer_one = seeds
        .clone()
        .map(|seed_id| Node {
            name: "seed".to_string(),
            id: seed_id,
        })
        .map(|s| (s.clone(), find_location(&graph, &graph_range, s)))
        .map(|v| v.1.id as usize)
        .min()
        .unwrap();

    println!("answer 1 {:?}", answer_one);

    let perm_seeds = seeds.clone().collect::<Vec<_>>();

    let answer_two = (0..perm_seeds.len() / 2)
        .map(|i| NodeRange {
            name: "seed".to_string(),
            range: (perm_seeds[2 * i], perm_seeds[2 * i] + perm_seeds[2 * i + 1]),
        })
        .flat_map(|s| find_location_range(&graph, &graph_range, s));

    println!(
        "answer 2 {:?}",
        answer_two
            .min_by(|a, b| a.range.0.partial_cmp(&b.range.0).unwrap())
            .unwrap()
            .range
            .0 as usize
    );
}
