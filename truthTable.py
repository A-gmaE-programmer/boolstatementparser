debug = 1

operations = {
        "AND" : lambda a, b: a and b,
        "NAND": lambda a, b: not (a and b),
        "OR"  : lambda a, b: a or b,
        "NOR" : lambda a, b: not (a or b),
        "XOR" : lambda a, b: (a and not b) or (not a and b),
        }
def notCheck(lastelm, elm):
    (not elm) if lastelm == "NOT" else lastelm

def evalStmt(statement, inputs):
    if debug:
        print("Evaluating:", statement)

    # TODO Scan for bracketed statements and evaluate them first
    statement2 = []
    sCache = []
    sDepth = 0
    for elm in statement:
        appended = False
        if (elm[0] == '('):
            sCache.append(elm[1:] if sDepth == 0 else elm)
            appended = True
            sDepth += elm.count("(")
        if (elm[-1] == ')'):
            sDepth += -1 * elm.count(")")
            if not appended:
                sCache.append(elm[:-1] if sDepth == 0 else elm)
            else:
                # If the element has already been appended, strip off the closing bracket
                sCache[-1] = sCache[-1][:-1]
            appended = True
            if sDepth == 0:
                statement2.append(evalStmt(sCache, inputs))
        if not appended:
            if sDepth == 0:
                statement2.append(elm)
            else:
                sCache.append(elm)
    if sDepth != 0:
        print("Error: unclosed backet")
        exit(1)
    # Replace all inputs with their actual values
    length = len(statement2)
    for i in range(length):
        if statement2[i] in inputs:
            statement2[i] = inputs[statement2[i]]
    # Find all inverted values (not) and invert them
    statement3 = []
    invert = False
    for elm in statement2:
        if elm == "NOT":
            invert = not invert
        elif invert:
            statement3.append(not elm)
            invert = False
        else:
            statement3.append(elm)
    
    lastop = "AND"
    result = True
    for elm in statement3:
        if isinstance(elm, bool):
            result = operations[lastop](result, elm)
        else:
            lastop = elm
    if debug:
        print("s1:", statement2)
        print("s2:", statement3)
    return result

def initInput(statement):
    inputs = {}
    for elm in statement:
        elm = (elm.replace(")","").replace("(",""))
        if len(elm) == 1:
            inputs[elm] = False
    return inputs

def generateParseTable(mainStatement):
    inputs = [key for key in initInput(mainStatement)]
    length = len(inputs)
    possiblities = 2 ** length
    parseTable = []
    for i in range(possiblities):
        rawInputs = list(map(lambda x: bool(int(x)), list(format(i, f"0{length}b"))))
        inputDict = dict(zip(inputs, rawInputs))
        output = evalStmt(mainStatement, inputDict)
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

    return

if __name__ == "__main__":
    debug = 1 if input("Debug? ").strip().lower() in "yes" else 0
    makeTable = 1 if input("Generate truth table? ").strip().lower() in "yes" else 0
    mainStatement = input("Boolean Statement > ").strip().split()
    inputs = initInput(mainStatement)

    print("Parsed statement: ", mainStatement)
    print("Detected inputs: ", [key for key in inputs])
    if not makeTable:
        for i in inputs:
            inputs[i] = bool(input("{i} > ".format(i=i)).replace("0", ""))
        print("Inputs: ", inputs)
    if not makeTable:
        print("Output:", evalStmt(mainStatement, inputs))
    if makeTable:
        parseTable = generateParseTable(mainStatement)
        printFormatParseTable(parseTable, inputs)
