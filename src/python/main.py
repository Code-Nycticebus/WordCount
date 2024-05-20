from typing import DefaultDict
import itertools
import sys


def main() -> None:
    file = __file__ if len(sys.argv) < 2 else sys.argv[1]

    occurences: dict[str, int] = DefaultDict(int)

    with open(file) as f:
        for line in f.readlines():
            for word in line.split():
                occurences[word] += 1

    for i, (word, count) in enumerate(
        itertools.islice(
            sorted(
                occurences.items(),
                key=lambda s: s[1],
                reverse=True,
            ),
            3,
        )
    ):
        print(i + 1, word, count)


if __name__ == "__main__":
    main()
