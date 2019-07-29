class DieRollResult:
    def __init__(self, die_expr="", roll_expr="", mod_expr="", total=0):

        self.die_expr = die_expr
        self.roll_expr = roll_expr
        self.mod_expr = mod_expr
        self.total = total

    def __str__(self):
        return self.result_v()

    def result(self):
        """
        print result -> int
        """
        return "{0}".format(self.total)

    def result_v(self):
        """
        print verbose result -> '1d20 + 2d4 + 1 = 16'
        """
        return "{0}{1} = {2}".format(self.die_expr, self.mod_expr, self.total)

    def result_vv(self):
        """
        print very verbose result -> '1d20 + 2d4 + 1 = 10 + 3 + 2 + 1 = 16'
        """
        return "{0}{1} = {2}{3} = {4}".format(
            self.die_expr,
            self.mod_expr,
            self.roll_expr,
            self.mod_expr,
            self.total,
        )
