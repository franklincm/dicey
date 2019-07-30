# Dicey
version 1.0.2

A python package for evaluating dice rolls.

## Description
Dicey parses strings of dice rolls of the form:
```
'1d20 + 2 + 2d4 - 1d8 + 1'
```
Dicey then rolls the specified dice, and computes the total.

Results can be displayed a few different ways:

- just the total, e.g. '20'
- the original expression and the total, e.g. '1d20 + 2 = 17'
- the original expression, the intermediate dice rolls, and the total, e.g. '1d20 + 2 = (15) + 2 = 17'

## Installation
pip install dicey

## Usage
### Command Line
```
Usage:
  dicey
  dicey [-v | -vv] <expression>

Options:
  -h --help  show this screen.
  -v         print expression with total
  -vv        print expression, intermediate results, and total
```

### As a python package
```python
from dicey import roller

d = roller.DieRoller()
d.roll('1d20 + 1d4 + 2')

result = d.result
str(result)        # >>> "13"
str(result.v())    # >>> "1d20 + 1d4 + 2 = 13"
print(result.vv()) # >>> "1d20 + 1d4 + 2 = (7) + (4) + 2 = 13

d.reroll()
result = d.result
print(result)      # >>> "23"
print(result.v())  # >>> "1d20 + 1d4 + 2 = 23"
print(result.vv()) # >>> "1d20 + 1d4 + 2 = (19) + (2) = 23"
```
