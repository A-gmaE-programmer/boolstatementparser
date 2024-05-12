# Simple boolean statement parser and interpreter in python
To run
`python truthTable.py`

Boolean can be evaluated from left to right or based on the order of operations
Statements in backets are prioritsed as well as NOT operations
Supports `AND`, `NAND`, `OR`, `NOR`, `XOR`, `NOT`

# Using as a library
```python
import boolparser

# operations is a dictionary that maps
# all boolean operations that take 2 inputs
# to a lambda function
boolparser.operations["AND"](True, True) # True

# brackets take highest precedence,
# After that not statements, then the following
# Ordered list of lists in order
# Operations will be evaluated in this order
operation_order = \
[
        [ "AND", "NAND" ],
        [ "OR", "NOR" ],
        [ "XOR", "XNOR" ],
]

# Parse a string into a boolean statement
statment = parseStmt("A AND NOT C XOR A")

# extract all the inputs from a boolean statement
# inputs can be used multiple times
# A dictionary is returned with all inputs as False
inputs = boolparser.getInputs(statement)
# {'A': False, 'C': False}

# Evaluate a boolean statement left to right
# takes in a dictionary of input values
statement = parseStmt("A AND (B NOR C) XOR A")
inputs = {'A': False, 'B': True, 'C': False}
boolparser.evalStmtLR(statement, inputs) # False

# Evaluate a boolean statement based on operation_order
boolparser.evalStmtOO(statement, inputs)

# Generate a parse table as a 2d list of values
# Takes in boolean statement
pt = boolparser.generateParseTable(statement)

# Pretty print the parse table
boolparser.printFormatParseTable(pt, inputs)
```
