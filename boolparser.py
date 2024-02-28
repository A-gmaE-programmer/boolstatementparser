debug = 0

# Boolean lists of operations ordered by their precedence
operation_order = \
[
        [ "AND" , "NAND" ],
        [ "OR", "NOR" ],
        [ "XOR", "XNOR" ],
]

# Dictionary that maps operations to their functions
operations = \
{
        "NOT" : lambda a   : not a, # only symbolic, does not do anything
        "AND" : lambda a, b: a and b,
        "NAND": lambda a, b: not (a and b),
        "OR"  : lambda a, b: a or b,
        "NOR" : lambda a, b: not (a or b),
        "XOR" : lambda a, b: (a and not b) or (not a and b),
        "XNOR": lambda a, b: (a and b) or (not a and not b),
}

def parseStmt(string):
    return string.strip().replace("(", "( ").replace(")", " )").split()

def getInputs(statement):
    inputs = {}
    for elm in statement:
        if elm not in operations and elm not in "()":
            inputs[elm] = False
    return inputs

def evalPreprocess(statement, inputs, recursiveEvaluator):
    if debug == 1:
        print("Evaluating:", statement)
    # Statement after all operations in brackets have been processed
    linearStmt = []
    sCache = []
    sDepth = 0
    # Recursively process statements in brackets
    for elm in statement:
        if (elm == '('):
            sCache.append(elm)
            sDepth += 1
        elif (elm == ')'):
            sDepth += -1
            sCache.append(elm)
            if sDepth == 0:
                linearStmt.append(recursiveEvaluator(sCache[1:-1], inputs))
                sCache = []
        else:
            if sDepth == 0:
                linearStmt.append(elm)
            else:
                sCache.append(elm)

    if sDepth != 0:
        print("Error: unclosed bracket")
        raise SyntaxError

    # Replace all inputs with their actual values
    length = len(linearStmt)
    for i in range(length):
        try:
            linearStmt[i] = inputs[linearStmt[i]]
        except KeyError:
            pass
    # Find all inverted values (NOT) and invert them
    cleanStmt = []
    invert = False
    for elm in linearStmt:
        if elm == "NOT":
            invert = not invert
        elif invert:
            cleanStmt.append(not elm)
            invert = False
        else:
            cleanStmt.append(elm)

    return cleanStmt

# Old left to right interpreter
def evalStmtLR(statement, inputs):
    # Preprocess
    cleanStmt = evalPreprocess(statement, inputs, evalStmtLR)

    # Interpret the statement left to right
    lastop = "AND"
    result = True
    for elm in cleanStmt:
        if isinstance(elm, bool):
            result = operations[lastop](result, elm)
        else:
            if elm in operations:
                lastop = elm
            else:
                print("Error: Variable unaccounted for: {}".format(elm))
                raise ValueError
    return result

def evalStmtOO(statement, inputs):
    # Preprocess
    cleanStmt = evalPreprocess(statement, inputs, evalStmtOO)

    for operation_stage in operation_order:
        newStmt = ["NOOP"]
        for elm in cleanStmt:
            if newStmt[-1] in operation_stage:
                operation = newStmt.pop()
                newStmt.append(operations[operation](newStmt.pop(), elm))
            else:
                newStmt.append(elm)
        cleanStmt = newStmt[1:]

    return cleanStmt[0]

def generateParseTable(statement, evaluator):
    inputs = [key for key in getInputs(statement)]
    length = len(inputs)
    possiblities = 2 ** length
    parseTable = []
    for i in range(possiblities):
        rawInputs = list(map(lambda x: bool(int(x)), list(format(i, f"0{length}b"))))
        inputDict = dict(zip(inputs, rawInputs))
        output = evaluator(statement, inputDict)
        parseTable.append(rawInputs + [output])
    return parseTable

def printFormatParseTable(parseTable, inputs):
    keys = [key for key in inputs] + ["O"]
    widths = []
    width = 1
    for i in keys:
        width += len(i) + 3
        widths.append(len(i)-1)
    print("+{}+".format("+".join(map(lambda x: "-"*(3+x), widths))))
    print("| {} |".format(" | ".join(keys)))
    print("+{}+".format("+".join(map(lambda x: "-"*(3+x), widths))))
    # Print Data
    for row in parseTable:
        string = "| "
        for i in range(len(row)):
            string += "1" if row[i] else "0"
            string += " "*widths[i]
            string += " | "
        print(string[:-1])

    print("+{}+".format("+".join(map(lambda x: "-"*(3+x), widths))))

if __name__ == "__main__":
    statement = parseStmt(input("> "))
    inputs = getInputs(statement)
    # for i in inputs:
        # inputs[i] = bool(input("{} > ".format(i)))

    print(inputs)
    printFormatParseTable(generateParseTable(statement, evalStmtLR), inputs)
    # print(evalStmtOO(statement, inputs))
