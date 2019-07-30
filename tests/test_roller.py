from dicey.roller import DieRoller


def test_init_total():
    d = DieRoller()
    assert d.total == 0
