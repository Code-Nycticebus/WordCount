#!/bin/bash
mkdir -p bin

OPTIMIZE=3

( 
set -xe
gcc -o bin/c -O$OPTIMIZE c/main.c -flto 
g++ -o bin/cpp -O$OPTIMIZE cpp/main.cpp -flto
rustc -o bin/rust -C opt-level=$OPTIMIZE rust/main.rs
)

strip bin/*

