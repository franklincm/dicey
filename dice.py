from lark import Lark
import random

roll_grammar = '''
    start: expr

    expr: token+

    token: op* (die|mod)

    die: numdie "d" max

    !op: "-"|"+"

    numdie: INT
    max: INT
    mod: INT

    %import common.INT
    %import common.WS
    %ignore WS
'''


class DieRoller:

    def __init__(self):
        self.parser = Lark(roll_grammar, parser='lalr')
        self.grammar = roll_grammar
        self.roll_expr = ''
        self.die_expr = ''
        self.mod_expr = ''
        self.total = 0

        self.prev_roll_expr = ''
        self.prev_roll_verbose = ''

    def eval_string(self, expr):
        self.roll_expr = expr
        self.prev_roll_expr = expr
        self.parse_tree = self.parser.parse(expr)

        (self.die_expr, self.roll_expr,
         self.mod_expr, self.total) = self.process_tree(
             self.parse_tree)

    def reroll(self):
        self.parser.parse(self.prev_roll_expr)

        (self.die_expr, self.roll_expr,
         self.mod_expr, self.total) = self.process_tree(
             self.parse_tree)

    def process_tree(self, t):

        positive = True
        total = 0
        die_expr = ''
        roll_expr = ''
        mod_expr = ''

        for node in t.find_data('token'):
            ntype = node.children[0].data

            if ntype == 'die':
                die, roll, result = self._process_die(node.children[0])
                roll_expr += '{0}'.format(roll)
                die_expr += '{0}'.format(die)
                total += result
            else:
                ttype = node.children[1].data
                positive = node.children[0].children[0] == '+'

                if ttype == 'mod':
                    value = int(node.children[1].children[0])
                    if positive:
                        mod_expr += ' + {0}'.format(value)
                        total += value
                    else:
                        mod_expr += ' - {0}'.format(value)
                        total -= value
                else:
                    die, roll, result = self._process_die(node.children[1])
                    if positive:
                        roll_expr += ' + {0}'.format(roll)
                        die_expr += ' + {0}'.format(die)
                        total += result
                    else:
                        roll_expr += ' - ({0})'.format(roll)
                        die_expr += ' - {0}'.format(die)
                        total -= result

        return (die_expr, roll_expr, mod_expr, total)

    def _process_die(self, t):
        numdie = int(t.children[0].children[0])
        maxdie = int(t.children[1].children[0])

        die_expr = '{0}d{1}'.format(numdie, maxdie)
        roll_expr = ''
        total = 0
        for die in range(numdie):
            roll = random.randint(1, maxdie)
            roll_expr += '({0}) '.format(roll)
            total += roll
        roll_expr = roll_expr.replace(') (', ') + (')
        roll_expr = roll_expr[:-1]

        return (die_expr, roll_expr, total)


if __name__ == '__main__':
    d = DieRoller()
    d.eval_string('1d4 + 2d8 - 1')
    print(d.roll_expr)
    print(d.die_expr)
    print(d.mod_expr)
    print(d.total)
    print()
    d.reroll()
    print(d.roll_expr)
    print(d.die_expr)
    print(d.mod_expr)
    print(d.total)
