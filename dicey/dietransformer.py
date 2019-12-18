import random
import sys
from queue import LifoQueue

import lark


class DieTransformer(lark.Transformer):
    def __init__(self):
        self.string = ""
        self.intermediate_expr = ""
        self.value = LifoQueue()
        self.operators = LifoQueue()
        self.max = -(sys.maxsize)
        self.min = sys.maxsize
        self.repeats = 0

    def _precedence(self, op):
        if op == "+" or op == "-":
            return 1
        if op == "*" or op == "/":
            return 2
        return 0

    def _applyOp(self, a, b, op):
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            return a / b

    def _eval(self):
        while not self.operators.empty():
            op = self.operators.get()
            b = self.value.get()
            a = self.value.get()
            self.value.put(self._applyOp(a, b, op))

    def lparen(self, args):
        self.string += "("
        self.intermediate_expr += "("

        self.operators.put(args[0])

    def rparen(self, args):
        self.string += ")"
        self.intermediate_expr += ")"

        op = self.operators.get()
        while op != "(":
            b = self.value.get()
            a = self.value.get()

            if op == "+":
                self.value.put(a + b)
            elif op == "-":
                self.value.put(a - b)
            elif op == "*":
                self.value.put(a * b)
            elif op == "/":
                self.value.put(a / b)

            op = self.operators.get()

    def num(self, args):
        self.string += "{}".format(args[0])
        self.intermediate_expr += args[0]

        self.value.put(int(args[0]))

    def op(self, args):
        self.string += " {} ".format(args[0])
        self.intermediate_expr += " {} ".format(args[0])

        if not self.operators.empty():
            op = self.operators.queue[-1]
            while not self.operators.empty() and self._precedence(
                op
            ) >= self._precedence(args[0]):
                op = self.operators.get()
                b = self.value.get()
                a = self.value.get()
                self.value.put(self._applyOp(a, b, op))

        self.operators.put(args[0])

    def die(self, args):
        self.string += "{}d{}".format(args[0], args[1])

        n = int(args[0])
        m = int(args[1])
        tmp_str = ""
        total = 0
        for die in range(n):
            roll = random.randrange(1, m + 1)
            total += roll
            tmp_str += "({})".format(roll)

            if roll > self.max:
                self.max = roll

            if roll < self.min:
                self.min = roll

        tmp_str = ") + (".join(tmp_str.split(")("))
        self.intermediate_expr += "{}".format(tmp_str)
        self.value.put(total)

    def meta(self, args):
        op = args[0]
        t = args[1]

        if t == "min":
            self.op([op])
            self.value.put(self.min)
            self.intermediate_expr += "[{}]".format(self.min)
        elif t == "max":
            self.op([op])
            self.value.put(self.max)
            self.intermediate_expr += "[{}]".format(self.max)

        self.string += "{}".format(args[1])

    def repeat(self, args):
        self.repeats = int(args[0])
        self.string += " {{{0}}}".format(self.repeats)
