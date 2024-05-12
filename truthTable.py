from boolparser import parseStmt, getInputs, evalStmtOO, evalStmtLR, generateParseTable, printFormatParseTable

def getBoolInput(query):
    return 1 if input(query).strip().lower() in "yes" else 0

if __name__ == "__main__":
    debug = False
    makeTable = True
    evalMode = 0
    if not getBoolInput("Autoconfig? "):
        debug = getBoolInput("Debug? ")
        makeTable = getBoolInput("Generate truth table? ")
        evalMode = int(getBoolInput("Use left to right evaluation? "))
    else:
        print("Defaults: \n\
    debug: False\n\
    makeTable: True\n\
    evalMode: Order of operations\n")
    mainStatement = parseStmt(input("Boolean Statement > "))
    inputs = getInputs(mainStatement)
    evalStmt = [evalStmtOO, evalStmtLR][int(evalMode)]

    print("Parsed statement: ", mainStatement)
    print("Detected inputs: ", [key for key in inputs])
    if not makeTable:
        for i in inputs:
            inputs[i] = bool(input("{i} > ".format(i=i)).replace("0", "").replace("True", ""))
        print("Inputs: ", inputs)
    if not makeTable:
        print("Output:", evalStmt(mainStatement, inputs))
    if makeTable:
        parseTable = generateParseTable(mainStatement, evalStmt)
        printFormatParseTable(parseTable, inputs)
