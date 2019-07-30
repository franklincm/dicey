from dicey.roller import DieRoller


def test_init_total():
    d = DieRoller()
    assert d.total == 0


def test_diceless_expr():
    d = DieRoller()
    d.roll("1+2")
    result = d.result
    assert str(result) == "3"
    assert result.v() == "1 + 2 = 3"
    assert result.vv() == "1 + 2 = 1 + 2 = 3"
