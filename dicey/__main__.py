from lark import exceptions
from . import roller
import sys

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
