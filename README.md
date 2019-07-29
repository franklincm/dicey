# Dice Strings

A python module for evaluating dice rolls.

## Installation

## Usage
```python
import DieRoller

d = DieRoller()
result = d.roll('1d20 + 1d4 + 2')

print(result.result())
print(result.result_v())
print(result.result_vv())

d.reroll()
result = d.roll('1d20 + 1d4 + 2')
print(result.result())
print(result.result_v())
print(result.result_vv())
```

