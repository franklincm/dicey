# Dicey
version 2.0.7


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
print(d)
```

## Examples
A single d20:
```
1d20
```

3 d20's:
```
3d20
```

Modifiers:
```
2d20 +2 -1
```

Precedence and multiplication:
```
(2d20 + (2*3)) * 2
```

Min and Max:
```
2d20 - min + max
```

Repeats, must be an integer inside `{}` and must occur at the end of 
an expression:
```
(2d20 + (2*3)) * 2 - min {4}
```

Note: since this is just using random ranges to determine rolls,
it's possible to roll physically impossible dice:
```
1d17
```

For rolls without modifiers or additional operations, dicey can output
a simple table displaying counts meeting specified criteria. For a game
like Shadowrun, you might want to roll a number of six sided dice and
know how many rolls are a 5 or 6, how many are exactly 6 and 1, and how
many aren't a 5 or 6:
```
10d6 >=5, =6, =1, <=4
```
This will produce something like:
```
Pool   Roll                             >= 5  = 1   = 6   <= 4 
--------------------------------------------------------------------
10d6   [1, 3, 3, 3, 4, 6, 5, 5, 3, 1]   [3]   [2]   [1]   [7]  

```

Note: conditions must be comma separated. This part was hastily added
without much forethought and could use some work.
