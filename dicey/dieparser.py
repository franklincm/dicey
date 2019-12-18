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

        for i in range(self.transformer.repeats - 1):
            self.transformer.__init__()
            self.parser.parse(text)
            self.transformer._eval()
            self.intermediate_expr.append(self.transformer.intermediate_expr)
            self.results.append(self.transformer.value.get())

    def __str__(self):
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
