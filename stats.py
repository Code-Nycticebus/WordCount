#!/bin/python3
from timeit import timeit
from subprocess import DEVNULL, run
from os import stat
from dataclasses import dataclass


FILE = "t8.shakespeare.txt"
SORTED_BY = "compile_time"


@dataclass
class Executable:
    language: str
    src: str
    compiler: str
    flags: list[str]


@dataclass
class Stats:
    language: str
    run_time: float
    compile_time: float
    size: float


def time_command(args: list[str]) -> float:
    return timeit(lambda: run(args, stdout=DEVNULL), number=1)


def compile_file(exe: Executable) -> Stats:
    output_file = f"bin/{exe.language}"

    compile_time = time_command([exe.compiler, exe.src, *exe.flags, "-o", output_file])
    run_time = time_command([output_file, FILE])
    run(["strip", output_file])

    return Stats(
        language=exe.language,
        run_time=run_time,
        compile_time=compile_time,
        size=stat(output_file).st_size / 1000,
    )


def main() -> None:
    executable: list[Executable] = [
        Executable("c", "src/c/main.c", "gcc", ["-O3", "-flto"]),
        Executable("cpp", "src/cpp/main.cpp", "g++", ["-O3", "-flto"]),
        Executable("rust", "src/rust/main.rs", "rustc", ["-C", "opt-level=3"]),
    ]

    times: list[Stats] = [compile_file(exe) for exe in executable]

    print(f"+==========+==========+==========+===========+")
    print(f"| language |   size   |   run    |  compile  |")
    print(f"+==========+==========+==========+===========+")
    for stat in sorted(times, key=lambda t: t.__dict__[SORTED_BY]):
        print(
            f"| {stat.language:<8} | {stat.size: 5.0f} kb | {stat.run_time*1000:5.0f} ms | {stat.compile_time*1000:6.0f} ms |"
        )
        print(f"+----------+----------+----------+-----------+")


if __name__ == "__main__":
    main()
