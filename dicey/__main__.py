"""
Usage:
  dicey
  dicey <expression>

Options:
  -h --help  show this screen.
"""

import sys
from lark import exceptions
from dicey.dieparser import DieParser


def loop():
    d = DieParser()

    while True:
        try:
            expr = input("roll: ")
            d.parse(expr)
            print(d)
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


def main():
    from docopt import docopt

    arguments = docopt(__doc__)

    if arguments["<expression>"]:
        d = DieParser()
        d.parse(arguments["<expression>"])
        print(d)

    else:
        loop()


if __name__ == "__main__":
    main()
