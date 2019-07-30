"""
Usage:
  dicey
  dicey [-v | -vv] <expression>

Options:
  -h --help  show this screen.
  -v         print expression with total
  -vv        print expression, intermediate results, and total

"""

from lark import exceptions

try:
    from . import roller
except ImportError:
    import roller
import sys


def loop():
    d = roller.DieRoller()

    while True:
        try:
            expr = input("roll: ")
            d.roll(expr)
            print(d.result)
            print(d.result.v())
            print(d.result.vv())
        except exceptions.UnexpectedCharacters:
            print("invalid expression")
        except exceptions.UnexpectedToken:
            continue
        except KeyboardInterrupt:
            print()
            continue
        except EOFError:
            print()
            print("exiting")
            sys.exit(0)


if __name__ == "__main__":
    from docopt import docopt

    arguments = docopt(__doc__)

    if arguments["<expression>"]:
        d = roller.DieRoller()
        d.roll(arguments["<expression>"])

        if arguments["-v"]:
            if arguments["-v"] == 1:
                print(d.result.v())
            elif arguments["-v"] == 2:
                print(d.result.vv())
        else:
            print(d.result)

    else:
        loop()
