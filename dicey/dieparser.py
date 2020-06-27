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

        for i in range(self.transformer.repeats - 1):
            self.transformer.__init__()
            self.parser.parse(text)
            self.transformer._eval()
            self.intermediate_expr.append(self.transformer.intermediate_expr)
            self.results.append(self.transformer.value.get())
            self.parse_relop()

    def parse_relop(self):
        if len(self.transformer.relops) > 0:
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

    def __str__(self):
        s = ""
        if len(self.results) > 1:
            s += "{} = ".format(self.last_exp)

            if len(self.transformer.relvals) > 0:
                s += "\n{}".format(
                    "-"
                    * (
                        len(self.intermediate_expr[0])
                        + 8
                        + len(str(max(self.hits)))
                    )
                )
                for i in range(self.transformer.repeats):
                    s += "\n{}: ".format(self.intermediate_expr[i])

                    num_relops = len(self.transformer.relops)
                    for k in range(num_relops):
                        s += "[{}]".format(self.hits[num_relops * i + k])
                        if num_relops > 1 and k < (num_relops - 1):
                            s += ", "

            else:
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
            if len(self.transformer.relvals) > 0:
                s = "{} = {}: ".format(
                    self.last_exp, self.intermediate_expr[0]
                )

                for index, val in enumerate(self.hits):
                    s += "{}".format(val)

                    # add commas, except after the last value
                    if len(self.hits) > 1 and index < (len(self.hits) - 1):
                        s += ", "

                # s += ": {} hits".format(self.hits[0])
                return s

            s += "{} = ".format(self.last_exp)
            s += "{} = {}".format(self.intermediate_expr[0], self.results[0])

        return s
