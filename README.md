# Dice Strings

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
```python
python -m dicey
```

```python
from dicey import roller

d = roller.DieRoller()
result = d.roll('1d20 + 1d4 + 2')

print(result.result())
print(result.result_v())
print(result.result_vv())

d.reroll()
result = d.result
print(result.result())
print(result.result_v())
print(result.result_vv())
```
