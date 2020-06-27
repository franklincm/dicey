from dicey.dieparser import DieParser


def test_diceless():
    d = DieParser()
    d.parse("1+2")
    result = d.results[0]
    assert result == 3


def test_const():
    d = DieParser()
    d.parse("1")
    result = d.results[0]
    assert result == 1


def test_exprs():
    exprs = [
        "2d4 + 1 - 3",
        "(2d4 + 6) + ((1d8 + 2) + 3)",
        "2d4 + 8",
        "1d6",
        "4d6 - min {6}",
        "4d6 + max {6}",
        "(((1d4)))",
        "2d4 * (1 + 3)",
        "(1d6)",
        "1d8 + (2 * 3d4 + (1d6))",
        "1d8 + (2 * 3d4 + (1d6))",
        "2d4 + 1 - (3)",
        "(2d4 *2) + 2d6 + 1 - 1d8",
        "(2d4 *2) + 2d6 + 1 - 1d8",
        "(2d4 *2) + 2d6 + 1 - 1d8",
        "(2d4 *2) + 2d6 + 1 - 1d8",
        "2d4 + 2d6 + 2d5 + 1d8",
        "2d4",
    ]

    d = DieParser()
    for expr in exprs:
        d.parse(expr)
        print(d)
