#!/bin/python3

from timeit import timeit
from subprocess import DEVNULL, run
from dataclasses import dataclass

SORTED_BY = "run"


@dataclass
class Executable:
    language: str
    compile: str | None
    run: str


@dataclass
class Stats:
    language: str
    run: float
    compile: float


def time_command(args: list[str], number=1) -> float:
    return timeit(lambda: run(args, stdout=DEVNULL, stderr=DEVNULL), number=number)


def compile_file(exe: Executable) -> Stats:
    compile_time = time_command(exe.compile.split()) if exe.compile else 0
    run_time = time_command(exe.run.split())

    return Stats(
        language=exe.language,
        run=run_time,
        compile=compile_time,
    )


def main() -> None:
    run(["mkdir", "-p", "bin"])
    with open("bin/.gitignore", "w") as f:
        f.write("*")

    executable: list[Executable] = [
        Executable(
            language="c",
            compile="gcc src/c/main.c -O3 -flto -o bin/c",
            run="bin/c t8.shakespeare.txt",
        ),
        Executable(
            language="cpp",
            compile="g++ src/cpp/main.cpp -O3 -flto -o bin/cpp",
            run="bin/cpp t8.shakespeare.txt",
        ),
        Executable(
            language="rust",
            compile="rustc src/rust/main.rs -C opt-level=3 -o bin/rust",
            run="bin/rust t8.shakespeare.txt",
        ),
        Executable(
            language="python3",
            compile=None,
            run="python3 src/python/main.py t8.shakespeare.txt",
        ),
    ]

    times: list[Stats] = [compile_file(exe) for exe in executable]

    output = ""

    output += "+==========+===========+===========+\n"
    output += "| language |    run    |  compile  |\n"
    output += "+==========+===========+===========+\n"

    for stat in sorted(times, key=lambda t: t.__dict__[SORTED_BY]):
        output += f"| {stat.language:<8} | {stat.run*1000:6.0f} ms | {stat.compile*1000:6.0f} ms |\n"
        output += "+----------+-----------+-----------+\n"

    print(output)

    with open("README.md", "w") as f:
        f.write("# Word Count\n")
        f.write("Word count programm, implemented in various languages.\n")
        f.write("```terminal\n")
        f.write(output)
        f.write("```\n")


if __name__ == "__main__":
    main()
