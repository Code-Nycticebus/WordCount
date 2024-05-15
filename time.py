#!/bin/python3
from timeit import timeit
from subprocess import DEVNULL, run
from pathlib import Path


FILE = "t8.shakespeare.txt"


times: list[tuple[Path, float]] = [
    (exe, timeit(lambda: run([exe, FILE], stdout=DEVNULL), number=1))
    for exe in Path("bin").glob("*")
]

for exe, time in sorted(times, key=lambda t: t[1]):
    print(f"'{exe}':\t{time*1000:4.0f}ms")
