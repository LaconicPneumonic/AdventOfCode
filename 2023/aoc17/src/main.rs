use std::{
    cmp::Ordering,
    collections::{BinaryHeap, HashMap, HashSet},
    io::{BufRead, BufReader},
};

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: BufReader<std::fs::File> = BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

type Point = (isize, isize);

#[derive(Clone, Eq, PartialEq, Debug, Hash)]
struct Pose {
    point: Point,
    direction: u8,
    len_no_turn: u8,
}

#[derive(Clone, Eq, PartialEq, Debug, Hash, Copy)]
struct State {
    point: Point,
    direction: u8,
    len_no_turn: u8,
    heat_loss: usize,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        // Notice that the we flip the ordering on costs.
        // In case of a tie we compare positions - this step is necessary
        // to make implementations of `PartialEq` and `Ord` consistent.
        other.heat_loss.cmp(&self.heat_loss)
    }
}

// `PartialOrd` needs to be implemented as well.
impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl State {
    fn to_pose(&self) -> Pose {
        Pose {
            point: self.point,
            direction: self.direction,
            len_no_turn: self.len_no_turn,
        }
    }
}

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

fn shortest_path(
    graph: &HashMap<Point, String>,
    start: &Point,
    end: &Point,
) -> Option<(usize, Vec<Pose>)> {
    let valid_starting_nodes = [
        State {
            point: *start,
            direction: 0,
            len_no_turn: 0,
            heat_loss: 0,
        },
        State {
            point: *start,
            direction: 1,
            len_no_turn: 0,
            heat_loss: 0,
        },
    ];

    let mut dist: HashMap<Pose, usize> = HashMap::new();

    let mut prev: HashMap<Pose, Pose> = HashMap::new();
    let mut heap: BinaryHeap<State> = BinaryHeap::from(valid_starting_nodes.clone());

    valid_starting_nodes.iter().for_each(|p| {
        dist.insert(
            Pose {
                point: p.point,
                direction: p.direction,
                len_no_turn: p.len_no_turn,
            },
            0,
        );
    });

    while let Some(node) = heap.pop() {
        if node.point == *end {
            let mut path = vec![];

            let mut curr = node.to_pose();
            while let Some(p) = prev.get(&curr) {
                path.push(curr);
                curr = p.clone();
            }

            path.push(curr);

            path.reverse();

            return Some((node.heat_loss, path));
        }

        if node.heat_loss > dist[&node.to_pose()] {
            continue;
        }

        let valid_neighbors = [0, 1, 3]
            .into_iter()
            .map(|d| {
                let next_direction = (node.direction + d) as u8 % 4;

                let next_point = (
                    node.point.0 + DIRECTIONS[next_direction as usize].0,
                    node.point.1 + DIRECTIONS[next_direction as usize].1,
                );

                let next_len_no_turn = if next_direction == node.direction {
                    node.len_no_turn + 1
                } else {
                    1
                };

                Pose {
                    point: next_point,
                    direction: next_direction,
                    len_no_turn: next_len_no_turn,
                }
            })
            .filter(|s| s.len_no_turn < 4)
            .filter(|s| graph.contains_key(&s.point));

        for neighbor in valid_neighbors {
            let next = State {
                point: neighbor.point,
                direction: neighbor.direction,
                len_no_turn: neighbor.len_no_turn,
                heat_loss: graph
                    .get(&neighbor.point)
                    .unwrap()
                    .parse::<usize>()
                    .unwrap()
                    + node.heat_loss,
            };

            if next.heat_loss < *dist.get(&next.to_pose()).unwrap_or(&usize::MAX) {
                heap.push(next);
                dist.insert(next.to_pose(), next.heat_loss);
                prev.insert(next.to_pose(), node.to_pose());
            }
        }
    }

    // Goal not reachable
    None
}

fn shortest_ultra_path(
    graph: &HashMap<Point, String>,
    start: &Point,
    end: &Point,
) -> Option<(usize, Vec<Pose>)> {
    let valid_starting_nodes = [
        State {
            point: *start,
            direction: 0,
            len_no_turn: 0,
            heat_loss: 0,
        },
        State {
            point: *start,
            direction: 1,
            len_no_turn: 0,
            heat_loss: 0,
        },
    ];

    let mut dist: HashMap<Pose, usize> = HashMap::new();

    let mut prev: HashMap<Pose, Pose> = HashMap::new();
    let mut heap: BinaryHeap<State> = BinaryHeap::from(valid_starting_nodes.clone());

    valid_starting_nodes.iter().for_each(|p| {
        dist.insert(
            Pose {
                point: p.point,
                direction: p.direction,
                len_no_turn: p.len_no_turn,
            },
            0,
        );
    });

    while let Some(node) = heap.pop() {
        if node.point == *end {
            let mut path = vec![];

            let mut curr = node.to_pose();
            while let Some(p) = prev.get(&curr) {
                path.push(curr);
                curr = p.clone();
            }

            path.push(curr);

            path.reverse();

            return Some((node.heat_loss, path));
        }

        if node.heat_loss > dist[&node.to_pose()] {
            continue;
        }

        let valid_neighbors = if node.len_no_turn < 4 {
            let next_direction = node.direction;

            let next_point = (
                node.point.0 + DIRECTIONS[next_direction as usize].0,
                node.point.1 + DIRECTIONS[next_direction as usize].1,
            );

            let next_len_no_turn = node.len_no_turn + 1;

            [Pose {
                point: next_point,
                direction: next_direction,
                len_no_turn: next_len_no_turn,
            }]
            .into_iter()
            .collect::<Vec<_>>()
        } else {
            [0, 1, 3]
                .into_iter()
                .map(|d| {
                    let next_direction = (node.direction + d) as u8 % 4;

                    let next_point = (
                        node.point.0 + DIRECTIONS[next_direction as usize].0,
                        node.point.1 + DIRECTIONS[next_direction as usize].1,
                    );

                    let next_len_no_turn = if next_direction == node.direction {
                        node.len_no_turn + 1
                    } else {
                        1
                    };

                    Pose {
                        point: next_point,
                        direction: next_direction,
                        len_no_turn: next_len_no_turn,
                    }
                })
                .collect::<Vec<_>>()
        }
        .into_iter()
        .filter(|s| s.len_no_turn < 11)
        .filter(|s| graph.contains_key(&s.point));

        for neighbor in valid_neighbors {
            let next = State {
                point: neighbor.point,
                direction: neighbor.direction,
                len_no_turn: neighbor.len_no_turn,
                heat_loss: graph
                    .get(&neighbor.point)
                    .unwrap()
                    .parse::<usize>()
                    .unwrap()
                    + node.heat_loss,
            };

            if next.heat_loss < *dist.get(&next.to_pose()).unwrap_or(&usize::MAX) {
                heap.push(next);
                dist.insert(next.to_pose(), next.heat_loss);
                prev.insert(next.to_pose(), node.to_pose());
            }
        }
    }

    // Goal not reachable
    None
}

fn main() {
    /**
     * Navigate through a multi layer graph where the original heat loss grid is expanded
     * into multiple layers determined by the constraints placed on the number of steps in each
     * direction. Part one and two place different constraints, but can still be reduced to the
     * shortest path problem in each graph. Solved with Djikstra's algorithm.
     */
    let lines = load_text_file_lines("./input.txt");

    let graph = parse_graph(&lines);

    let ret = shortest_path(
        &graph,
        &(0, 0),
        &(lines.len() as isize - 1, lines[0].len() as isize - 1),
    );

    let (best_heat_loss, path) = ret.unwrap();

    println!("Best heat loss: {:?}", best_heat_loss);

    for p in path {
        println!("{:?}", p);
    }

    let ret_two = shortest_ultra_path(
        &graph,
        &(0, 0),
        &(lines.len() as isize - 1, lines[0].len() as isize - 1),
    );

    let (best_heat_loss_two, path_two) = ret_two.unwrap();

    println!("Best ultra heat loss: {:?}", best_heat_loss_two);

    for p in path_two {
        println!("{:?}", p);
    }
}
