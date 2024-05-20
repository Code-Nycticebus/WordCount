#!/bin/python3

import sys
from timeit import timeit
from subprocess import DEVNULL, run
from os import stat
from dataclasses import dataclass

FILE = "t8.shakespeare.txt" if len(sys.argv) < 2 else sys.argv[1]
NUMBER = 1
SORTED_BY = "run"


@dataclass
class Executable:
    language: str
    cmd: str


@dataclass
class Stats:
    language: str
    run: float
    compile: float
    size: float


def time_command(args: list[str], number=1) -> float:
    return timeit(lambda: run(args, stdout=DEVNULL, stderr=DEVNULL), number=number)


def compile_file(exe: Executable) -> Stats:
    output_file = f"bin/{exe.language}"

    compile_time = time_command(exe.cmd.split())
    run_time = time_command([output_file, FILE], number=NUMBER)
    run(["strip", output_file])

    return Stats(
        language=exe.language,
        run=run_time,
        compile=compile_time,
        size=stat(output_file).st_size / 1000,
    )


def main() -> None:
    run(["mkdir", "-p", "bin"])
    with open("bin/.gitignore", "w") as f:
        f.write("*")

    executable: list[Executable] = [
        Executable("c", "gcc src/c/main.c -O3 -flto -o bin/c"),
        Executable("cpp", "g++ src/cpp/main.cpp -O3 -flto -o bin/cpp"),
        Executable("rust", "rustc src/rust/main.rs -C opt-level=3"),
    ]

    times: list[Stats] = [compile_file(exe) for exe in executable]

    print(f"+==========+===========+==========+===========+")
    print(f"| language |   size    |   run    |  compile  |")
    print(f"+==========+===========+==========+===========+")
    for stat in sorted(times, key=lambda t: t.__dict__[SORTED_BY]):
        print(
            f"| {stat.language:<8} | {stat.size: 6.0f} kb | {stat.run*1000:5.0f} ms | {stat.compile*1000:6.0f} ms |"
        )
        print(f"+----------+-----------+----------+-----------+")


if __name__ == "__main__":
    main()
