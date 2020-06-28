import os
from pathlib import Path
import lark
from dicey.dietransformer import DieTransformer


class DieParser:
    def __init__(self):
        self.grammar = open(
            os.path.join(Path(__file__).parent, "dicey.lark")
        ).read()
        self.last_exp = ""
        self.intermediate_expr = []
        self.results = []
        self.hits = []
        self.transformer = DieTransformer()
        self.parser = lark.Lark(
            self.grammar,
            parser="lalr",
            transformer=self.transformer,
            propagate_positions=False,
        )

    def parse(self, text):
        self.__init__()
        self.parser.parse(text)
        self.transformer._eval()
        self.last_exp = self.transformer.string
        self.intermediate_expr.append(self.transformer.intermediate_expr)
        self.results.append(self.transformer.value.get())
        self.parse_relop()

        if self.transformer.diminishing:
            self.diminish_start = self.transformer.diminish_start
            self.diminish_sides = self.transformer.diminish_sides
            for i in range(self.diminish_start - 1, 0, -1):
                text = text.replace(
                    ("%dd%d" % (i + 1, self.diminish_sides)),
                    ("%dd%d" % (i, self.diminish_sides)),
                )
                self.transformer.__init__()
                self.parser.parse(text)
                self.transformer._eval()
                self.intermediate_expr.append(
                    self.transformer.intermediate_expr
                )
                self.results.append(self.transformer.value.get())
                self.parse_relop()

        for i in range(self.transformer.repeats - 1):
            self.transformer.__init__()
            self.parser.parse(text)
            self.transformer._eval()
            self.intermediate_expr.append(self.transformer.intermediate_expr)
            self.results.append(self.transformer.value.get())
            self.parse_relop()

    def parse_relop(self):
        if self.transformer.has_relexp:
            for i in range(len(self.transformer.relops)):
                val = self.transformer.relvals[i]

                if self.transformer.relops[i] == "<":
                    self.hits.append(
                        len(
                            [
                                x
                                for x in self.transformer.intermediate_vals
                                if x < val
                            ]
                        )
                    )

                if self.transformer.relops[i] == ">":
                    self.hits.append(
                        len(
                            [
                                x
                                for x in self.transformer.intermediate_vals
                                if x > val
                            ]
                        )
                    )

                if self.transformer.relops[i] == ">=":
                    self.hits.append(
                        len(
                            [
                                x
                                for x in self.transformer.intermediate_vals
                                if x >= val
                            ]
                        )
                    )

                if self.transformer.relops[i] == "<=":
                    self.hits.append(
                        len(
                            [
                                x
                                for x in self.transformer.intermediate_vals
                                if x <= val
                            ]
                        )
                    )

                if self.transformer.relops[i] == "=":
                    self.hits.append(
                        len(
                            [
                                x
                                for x in self.transformer.intermediate_vals
                                if x == val
                            ]
                        )
                    )

    def _ellipsis_expr(self, s, n):
        """
        str: s, string to insert ellipsis into
        int: n, max length of resulting string
        """

        c = s
        while len(c) > n:
            c = "{}{}".format(c[:-7], " ... ]")
            # c = c[:-1]
            while c[-1].isdigit():
                c = c[:-1]

        return c

    def _print_relexp(self):
        # relational operators present
        num_relops = len(self.transformer.relops)

        # total output width, this should be passable from
        # somewhere later
        width = 80

        # calc field width for intermediate expression
        expr_width = (
            min(width - 7 - (num_relops * 6), len(self.intermediate_expr[0]))
            + 2
        )

        # print headers
        s = ("{:<7}{:<%d}" % expr_width).format("Pool", "Roll")

        # print specified conditions
        for relexp in self.transformer.relexps:
            s += "{:^6}".format(relexp)
        s += "\n"

        # print rule
        for i in range(expr_width + 7 + (num_relops * 6)):
            s += "-"
        s += "\n"

        # if multiline output
        if len(self.results) > 1:

            for i in range(len(self.intermediate_expr)):
                if self.transformer.diminishing:
                    s += "{:<7}".format(
                        "%dd%d"
                        % (self.diminish_start - i, self.diminish_sides)
                    )
                else:
                    s += "{:<7}".format(self.last_exp)
                s += ("{:<%d}" % expr_width).format(
                    self._ellipsis_expr(self.intermediate_expr[i], expr_width)
                )

                for k in range(num_relops):
                    s += "{:^6}".format(
                        ("[%s]") % self.hits[num_relops * i + k]
                    )
                s += "\n"

        # single line output (not including headers)
        else:
            s += ("{:<7}{:<%d}" % expr_width).format(
                self.last_exp,
                self._ellipsis_expr(self.intermediate_expr[0], expr_width),
            )

            for index, val in enumerate(self.hits):
                s += "{:^6}".format(("[%s]" % (val)))

        return s

    def _print_expr(self):
        s = ""
        if len(self.results) > 1:
            s += "{} = ".format(self.last_exp)
            s += "\n{}".format(
                "-"
                * (
                    len(self.intermediate_expr[0])
                    + 3
                    + len(str(max(self.results)))
                )
            )
            for i in range(self.transformer.repeats):
                s += "\n{} = {}".format(
                    self.intermediate_expr[i], self.results[i]
                )
        else:

            s += "{} = ".format(self.last_exp)
            s += "{} = {}".format(self.intermediate_expr[0], self.results[0])

        return s

    def __str__(self):
        if self.transformer.has_relexp:
            return self._print_relexp()
        return self._print_expr()
