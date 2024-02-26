# Simple boolean statement parser and interpreter in python
To run
`python truthTable.py`

Boolean statement is parsed from left to right, prioritising statements in backets and not inversions
Supports `AND`, `NAND`, `OR`, `NOR`, `XOR`, `NOT`

TODO: implement an interpreter that supports order of operations

# Using as a library
```python
import truthTable

# operations is a dictionary that maps
# all boolean operations that take 2 inputs
# to a lambda function
truthTable.operations["AND"](True, True) # True

# extract all the inputs from a boolean statement
# statement is just a string that has been split
# inputs can be used multiple times
# A dictionary is returned with all inputs as False
statement = "A AND NOT C XOR A".split()
inputs = truthTable.initInput(statement)
# {'A': False, 'C': False}

# Evaluate a boolean statement
# takes in a dictionary of input values
statement = "A AND (B NOR C) XOR A".split()
inputs = {'A': False, 'B': True, 'C': False}
truthTable.evalStmt(statement, inputs) # False

# Generate a parse table as a 2d list of values
# Takes in boolean statement
pt = truthTable.generateParseTable(statement)

# Pretty print the parse table
truthTable.printFormatParseTable(pt, inputs)
```
