# Dicey
version 2.0.3

A python package for evaluating dice rolls.

## Description
Dicey parses strings of dice rolls of the form:
```
'1d20 + 2 + 2d4 - 1d8 + 1 - min {3}'
```

Where `min` (or `max`) holds the value of the highest or lowest single die rolled and `{3}` is how many times to repeat the expression. `[min|max]` and `{num}` are optional.
Dicey then rolls the specified dice, and computes the total. Valid arithmentic operators are `+ - * / ()`. Dicey will always translate individual die expressions to a randomized result
before applying arithmetic operators.

## Installation
pip install dicey

## Usage
### Command Line
```
Usage:
  dicey
  dicey <expression>

Options:
  -h --help  show this screen.
```

### As a python package
```python
from dicey.dieparser import DieParser

d = DieParser()
d.parse('1d20 + 1d4 + 2')
result = d.__str__()
print(result)

# or of course simply:
print(d)
```
