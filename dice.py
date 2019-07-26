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


def process_tree(t, verbose=False):

    positive = True
    total = 0
    die_expr = ''
    roll_expr = ''
    mod_expr = ''

    for node in parse_tree.find_data('token'):
        ntype = node.children[0].data

        if ntype == 'die':
            die, roll, result = _process_die(node.children[0])
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
                die, roll, result = _process_die(node.children[1])
                if positive:
                    roll_expr += ' + {0}'.format(roll)
                    die_expr += ' + {0}'.format(die)
                    total += result
                else:
                    roll_expr += ' - ({0})'.format(roll)
                    die_expr += ' - {0}'.format(die)
                    total -= result

    if verbose:
        print("%s = %s%s = %s" % (die_expr, roll_expr, mod_expr, total))
    else:
        print("%s%s = %s" % (die_expr, mod_expr, total))


def _process_die(t):
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
    parser = Lark(roll_grammar, parser='lalr')
    parse_tree = parser.parse('10d20 + 1 + 2d4 - 6')
    process_tree(parse_tree, True)
