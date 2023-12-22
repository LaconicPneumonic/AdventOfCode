use std::{cmp::Ordering, io::BufRead};

fn load_text_file_lines(filename: &str) -> Vec<String> {
    let file = std::fs::File::open(filename).unwrap();
    let reader: std::io::BufReader<std::fs::File> = std::io::BufReader::new(file);
    return reader.lines().map(|line| line.unwrap()).collect();
}

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy, PartialOrd, Ord)]
enum Card {
    Ace,
    King,
    Queen,
    Jack,
    Ten,
    Nine,
    Eight,
    Seven,
    Six,
    Five,
    Four,
    Three,
    Two,
    One,
    Joker,
}

impl Card {
    fn from_char(c: char) -> Card {
        match c {
            '1' => Card::One,
            '2' => Card::Two,
            '3' => Card::Three,
            '4' => Card::Four,
            '5' => Card::Five,
            '6' => Card::Six,
            '7' => Card::Seven,
            '8' => Card::Eight,
            '9' => Card::Nine,
            'T' => Card::Ten,
            'J' => Card::Jack,
            'Q' => Card::Queen,
            'K' => Card::King,
            'A' => Card::Ace,
            _ => panic!("invalid card char"),
        }
    }
}

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy, PartialOrd, Ord)]
enum HandType {
    FiveOfAKind,
    FourOfAKind,
    FullHouse,
    ThreeOfAKind,
    TwoPair,
    OnePair,
    HighCard,
}

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
struct Hand([Card; 5]);

impl Hand {
    fn compare(left: Hand, right: Hand) -> Ordering {
        let left_type = HandType::from_cards(left);
        let right_type = HandType::from_cards(right);

        if left_type != right_type {
            return left_type.cmp(&right_type);
        };

        let first_none_equal = left.0.iter().zip(right.0.iter()).find(|(l, r)| l != r);

        if first_none_equal.is_none() {
            return Ordering::Equal;
        }

        let (left_card, right_card) = first_none_equal.unwrap();

        return left_card.cmp(right_card);
    }

    fn compare_v2(left: Hand, right: Hand) -> Ordering {
        let left_type = HandType::from_cards_v2(left);
        let right_type = HandType::from_cards_v2(right);

        if left_type != right_type {
            return left_type.cmp(&right_type);
        };

        let first_none_equal = left.0.iter().zip(right.0.iter()).find(|(l, r)| l != r);

        if first_none_equal.is_none() {
            return Ordering::Equal;
        }

        let (mut left_card, mut right_card) = first_none_equal.unwrap();

        if left_card == &Card::Jack {
            left_card = &Card::Joker;
        }

        if right_card == &Card::Jack {
            right_card = &Card::Joker;
        }

        return left_card.cmp(right_card);
    }
}

impl HandType {
    fn from_cards(cards: Hand) -> HandType {
        let mut card_counts: std::collections::HashMap<Card, u8> = std::collections::HashMap::new();

        for card in cards.0 {
            let count = card_counts.entry(card).or_insert(0);
            *count += 1;
        }

        let mut counts: Vec<_> = card_counts.values().map(|v| *v).collect();
        counts.sort();

        match counts.as_slice() {
            [1, 1, 1, 2] => HandType::OnePair,
            [1, 2, 2] => HandType::TwoPair,
            [1, 1, 3] => HandType::ThreeOfAKind,
            [1, 4] => HandType::FourOfAKind,
            [5] => HandType::FiveOfAKind,
            [2, 3] => HandType::FullHouse,
            [1, 1, 1, 1, 1] => HandType::HighCard,
            _ => panic!("invalid card counts"),
        }
    }

    fn from_cards_v2(cards: Hand) -> HandType {
        let mut card_counts: std::collections::HashMap<Card, u8> = std::collections::HashMap::new();

        for card in cards.0 {
            let count = card_counts.entry(card).or_insert(0);
            *count += 1;
        }

        let optional_joker = card_counts.remove(&Card::Jack);

        if optional_joker.is_some() && optional_joker.unwrap() < 5 {
            let max_entry = card_counts.iter().max_by_key(|v| v.1).unwrap();

            let count = card_counts.entry(*max_entry.0).or_insert(0);

            *count += optional_joker.unwrap();
        } else if optional_joker.is_some() && optional_joker.unwrap() == 5 {
            return HandType::FiveOfAKind;
        }

        let mut counts: Vec<_> = card_counts.values().map(|v| *v).collect();
        counts.sort();

        // println!("{:?} {:?}", cards, counts);

        match counts.as_slice() {
            [1, 1, 1, 2] => HandType::OnePair,
            [1, 2, 2] => HandType::TwoPair,
            [1, 1, 3] => HandType::ThreeOfAKind,
            [1, 4] => HandType::FourOfAKind,
            [5] => HandType::FiveOfAKind,
            [2, 3] => HandType::FullHouse,
            [1, 1, 1, 1, 1] => HandType::HighCard,
            _ => panic!("invalid card counts"),
        }
    }
}

fn main() {
    let lines: Vec<String> = load_text_file_lines("./input.txt");

    let mut parsed_lines = lines
        .iter()
        .map(|l| {
            let hand_points = l.split(" ").collect::<Vec<_>>();

            let hand = hand_points[0]
                .chars()
                .map(|c| Card::from_char(c))
                .collect::<Vec<_>>();

            let hand_array: Hand = Hand([hand[0], hand[1], hand[2], hand[3], hand[4]]);

            return (hand_array, hand_points[1].parse::<usize>().unwrap());
        })
        .collect::<Vec<_>>();

    parsed_lines.sort_by(|a, b| Hand::compare(a.0.clone(), b.0.clone()));

    parsed_lines.reverse();

    let answer_one: usize = parsed_lines
        .iter()
        .enumerate()
        .map(|(index, (_, points))| {
            let multiplier = index + 1;
            return multiplier * points;
        })
        .sum();
    println!("answer one: {:?}", answer_one);

    parsed_lines.sort_by(|a, b| Hand::compare_v2(a.0.clone(), b.0.clone()));
    parsed_lines.reverse();

    let answer_two: usize = parsed_lines
        .iter()
        .enumerate()
        .map(|(index, (_, points))| {
            let multiplier = index + 1;
            return multiplier * points;
        })
        .sum();

    println!("answer two: {:?}", answer_two);
}
