class DieRollResult:
    def __init__(self, die_expr="", roll_expr="", mod_expr="", total=0):

        self.die_expr = die_expr
        self.roll_expr = roll_expr
        self.mod_expr = mod_expr
        self.total = total

    def _check_mod(self):
        if self.die_expr == "" and self.mod_expr[0:3] == " + ":
            self.mod_expr = self.mod_expr[3:]

    def __str__(self):
        return self._total()

    def _total(self):
        """
        print result -> int
        """
        self._check_mod()
        return "{0}".format(self.total)

    def v(self):
        """
        print verbose result -> '1d20 + 2d4 + 1 = 16'
        """
        self._check_mod()
        return "{0}{1} = {2}".format(self.die_expr, self.mod_expr, self.total)

    def vv(self):
        """
        print very verbose result -> '1d20 + 2d4 + 1 = 10 + 3 + 2 + 1 = 16'
        """
        self._check_mod()
        return "{0}{1} = {2}{3} = {4}".format(
            self.die_expr,
            self.mod_expr,
            self.roll_expr,
            self.mod_expr,
            self.total,
        )
