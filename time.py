#!/bin/python3
import sys
from timeit import timeit
from subprocess import DEVNULL, run
from pathlib import Path


NUMBER = 10 if len(sys.argv) < 2 else int(sys.argv[1])
FILE = "t8.shakespeare.txt"


def time_executable(exe: Path) -> float:
    return timeit(lambda: run([exe, FILE], stdout=DEVNULL), number=NUMBER) / NUMBER


def main() -> None:
    times: list[tuple[Path, float]] = [
        (exe, time_executable(exe)) for exe in Path("bin").glob("*")
    ]

    for exe, time in sorted(times, key=lambda t: t[1]):
        print(f"'{exe}':\t{time*1000:4.0f}ms")


if __name__ == "__main__":
    main()
