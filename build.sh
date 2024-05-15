#!/bin/bash
mkdir -p bin

set -xe

gcc -o bin/c -O3 c/main.c
g++ -o bin/cpp -O3 cpp/main.cpp
rustc -o bin/rust -C opt-level=3 rust/main.rs
