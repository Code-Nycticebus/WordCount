use std::collections::HashMap;
use std::env;
use std::fs::read_to_string;

fn main() {
    let filename: String = env::args().nth(1).unwrap_or(file!().to_string());
    let content = read_to_string(filename).unwrap();

    let mut map: HashMap<&str, usize> = HashMap::new();
    let mut words: Vec<(&str, usize)> = vec![];

    for word in content.split_whitespace() {
        let idx = map.entry(word).or_insert(0);
        if *idx == 0 {
            words.push((word, 1));
            *idx = words.len();
        } else {
            words[*idx - 1].1 += 1;
        }
    }

    words.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());

    for (i, word) in words.iter().enumerate().take(3) {
        println!("{}: {}: {}", i + 1, word.0, word.1);
    }
}
