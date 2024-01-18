use std::{
    fmt,
    io::{BufRead, BufReader},
};

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: BufReader<std::fs::File> = BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

struct ValleyMap {
    rows: usize,
    cols: usize,
    row_data: Vec<usize>,
    column_data: Vec<usize>,
}

impl fmt::Display for ValleyMap {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "ValleyMap: {} {} [\n{}\n] [\n{}\n]",
            self.rows,
            self.cols,
            self.row_data
                .iter()
                .map(|v| format!("{:020b}", v))
                .collect::<Vec<_>>()
                .join(",\n"),
            self.column_data
                .iter()
                .map(|v| format!("{:020b}", v))
                .collect::<Vec<_>>()
                .join(",\n"),
        )
    }
}

fn find_palindrome_helper(
    data: &Vec<usize>,
    bound: usize,
    smudge_fix: bool,
) -> Vec<(usize, usize)> {
    let odd_center = (0..data.len() - 1).map(|v| (v, v + 1));

    let ret = odd_center
        .map(|(l, r)| {
            let mut left = l;
            let mut right = r;

            let mut is_palindrome = false;

            let mut smudge_fixed = false;

            // println!("left: {} right: {}", left, right);
            loop {
                if data[left] != data[right] {
                    if smudge_fix {
                        let diff = data[right] ^ data[left];
                        if diff != 0 && (diff & (diff - 1)) == 0 {
                            if smudge_fixed {
                                left += 1;
                                right -= 1;
                                break;
                            }

                            smudge_fixed = true;
                        } else {
                            left += 1;
                            right -= 1;
                            break;
                        }
                    } else {
                        left += 1;
                        right -= 1;
                        break;
                    }
                }

                is_palindrome = true;

                if left == 0 || right == bound {
                    break;
                }

                left -= 1;
                right += 1;
            }

            if is_palindrome && (left == 0 || right == bound) {
                // println!("great success");
                return Some((left, right));
            } else {
                return None;
            }
        })
        .filter(|v| v.is_some())
        .map(|v| v.unwrap_or((0, 0)))
        .collect::<Vec<_>>();
    // .filter(|(l, r)| *l == 0 || *r == bound)
    // .nth(0)
    // .unwrap_or((0, 0));

    if ret.len() > 1 {
        // println!("ret: {:?}", ret);
    }

    return if ret.len() > 0 { ret } else { vec![(0, 0)] };
}

// returns center of largest palindrome
fn find_palindrome(v: &ValleyMap, smudge_fix: bool) -> usize {
    let mut rows_max = find_palindrome_helper(&v.row_data, v.rows - 1, false)[0];

    let mut col_max = find_palindrome_helper(&v.column_data, v.cols - 1, false)[0];

    if smudge_fix {
        let smudged_row_options: Vec<(usize, usize)> =
            find_palindrome_helper(&v.row_data, v.rows - 1, true);

        let smudged_col_options = find_palindrome_helper(&v.column_data, v.cols - 1, true);

        println!("map: {}", v);
        println!("rows_max: {:?} col_max: {:?}", rows_max, col_max);
        println!("smudged_row_options: {:?}", smudged_row_options);
        println!("smudged_col_options: {:?}", smudged_col_options);

        rows_max = *smudged_row_options
            .iter()
            .filter(|v| **v != rows_max)
            .nth(0)
            .unwrap_or(&(0, 0));

        col_max = *smudged_col_options
            .iter()
            .filter(|v| **v != col_max)
            .nth(0)
            .unwrap_or(&col_max);
    }

    println!("row_max: {:?} col_max: {:?}", rows_max, col_max);

    if (rows_max.0 == 0 || rows_max.1 == v.rows - 1) && rows_max.1 - rows_max.0 >= 1 {
        return 100 * (((1 + rows_max.1 - rows_max.0) / 2) + rows_max.0);
    }

    return ((1 + col_max.1 - col_max.0) / 2) + col_max.0;
}

fn main() {
    let lines = load_text_file_lines("input.txt");

    let valley_maps = lines
        .iter()
        .fold(vec![vec![]], |mut agg: Vec<Vec<&String>>, line| {
            if line == "" {
                agg.push(vec![]);
            } else {
                agg.last_mut().unwrap().push(line);
            }

            agg
        })
        .iter()
        .map(|rows| {
            let num_rows = rows.len();
            let num_cols = rows[0].len();

            let row_data = rows
                .iter()
                .map(|r| {
                    r.chars().enumerate().fold(0, |mut agg, (i, c)| {
                        if c == '#' {
                            agg |= 1 << num_cols - i - 1;
                        }

                        agg
                    })
                })
                .collect::<Vec<_>>();

            let mut column_data = vec![0; num_cols];

            row_data.iter().enumerate().for_each(|(row_num, row)| {
                column_data.iter_mut().enumerate().for_each(|(col_num, v)| {
                    let mask = 1 << (num_cols - col_num - 1);

                    let extracted_bit = (row & mask) >> (num_cols - col_num - 1);

                    *v |= extracted_bit << num_rows - row_num - 1;
                })
            });

            ValleyMap {
                rows: num_rows,
                cols: num_cols,
                row_data,
                column_data,
            }
        })
        .collect::<Vec<_>>();

    let answer_1 = valley_maps
        .iter()
        .map(|v| {
            let val = find_palindrome(&v, false);

            // println!("{} {}", v, val);
            return val;
        })
        .sum::<usize>();

    println!("answer_1: {}", answer_1);
    println!("_____________________________________________________");

    let answer_2 = valley_maps
        .iter()
        .map(|v| {
            let val = find_palindrome(&v, true);

            // println!("{} {}", v, val);
            return val;
        })
        .sum::<usize>();

    println!("answer_2: {}", answer_2);
}
