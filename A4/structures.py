#!/usr/bin/python
#
# Classes to represent underlying data structures for the grammar
#
# CS550 Group 6
# Tom Houman (A4 Leader)
# Ryan Daugherty
# Joe Muoio
# CS550 Spring 2013
# Assignment 4
#
# Modified from code provided by Kurt Schmidt

####  CONSTANTS   ################

# the variable name used to store a proc's return value
returnSymbol = 'return'

tabstop = '  ' # 2 spaces

#####  Globals    #################

symbolCounter = 1
temporaryCounter = 1
linkerCounter = 1

symbolTable = {} # maps a symbolic key to a tuple containing (memory address, value, label)

code = '' # the compiled code


#########	Helper functions	############

def dumpSymbolTable():
    global symbolTable
    global symbolCounter
    table = ""
    allocations = [0] * symbolCounter
    for k, v in symbolTable.iteritems():
        allocations[int(v[0])] = k
    for i in range(1, symbolCounter):
        k = allocations[i]
        v = symbolTable[k]
        table += str(v[0]) + "  " + str(v[1]) + " ; "
        table += str(v[2]) + ' ' + k
        table += "\n"
    return table


def getAddressFromSymbolTable(key):
    try:
        address = symbolTable[key][0]
    except:
        address = symbolTable[addToSymbolTable(key, 0, 'variable')][0]

    return address


def getValueFromSymbolTable(key):
    try:
        val = symbolTable[key][1]
    except:
        val = symbolTable[addToSymbolTable(key, 0, 'variable')][1]

    return val


def addToSymbolTable(key, value, t):
    # adds the value at the location of key
    # key is the symbol in the program that was parsed
    # value is the numerical value of the thing being stored
    # returns the symbol table address.
    global symbolTable
    global symbolCounter

    if key not in symbolTable:
        symbolTable[key] = (str(symbolCounter), value, t )
        symbolCounter += 1
    if t == 'label':
        temp = symbolTable[key][0]
        symbolTable[key] = ( temp, value, t )
    return key


def addTempToSymbolTable(value=0):
    # adds the value at the location of "temporary_#"
    # value is the numerical value of the key
    # returns the symbol table address.
    global symbolTable
    global symbolCounter
    global temporaryCounter

    key = "Temp_" + str(temporaryCounter)
    symbolTable[key] = ( str(symbolCounter), value, 'temporary' )
    symbolCounter += 1
    temporaryCounter += 1

    return key

######   CLASSES   ##################

class Expr:
    '''Virtual base class for expressions in the language'''

    def __init__(self):
        raise NotImplementedError(
            'Expr: pure virtual base class.  Do not instantiate')

    def eval(self, nt, ft):
        '''Given an environment and a function table, evaluates the expression,
        returns the value of the expression (an int in this grammar)'''

        raise NotImplementedError(
            'Expr.eval: virtual method.  Must be overridden.')

    def isList(self):
        return False

    def isInt(self):
        return False

    def display(self, nt, ft, depth=0):
        'For debugging.'
        raise NotImplementedError(
            'Expr.display: virtual method.  Must be overridden.')

    def translate(self, nt, ft):
        'For debugging.'
        raise NotImplementedError(
            'Expr.translate: virtual method.  Must be overridden.')


class Ident(Expr):
    '''Stores the symbol'''

    def __init__(self, name):
        self.name = name

    def eval(self, nt, ft):
        return nt[self.name]

    def display(self, nt, ft, depth=0):
        print "%s%s" % (tabstop * depth, self.name)

    def translate(self, nt, ft):
        key = str(self.name)
        addToSymbolTable(key, 0, 'variable')
        #we use 0 since it will get its real value when it is assigned.

        return key


class Times(Expr):
    '''expression for binary multiplication'''

    def __init__(self, lhs, rhs):
        '''lhs, rhs are Expr's, the operands'''

        if lhs.isList() or rhs.isList():
            raise Exception("Operation cannot apply to lists")
        self.lhs = lhs
        self.rhs = rhs

    def eval(self, nt, ft):
        return self.lhs.eval(nt, ft) * self.rhs.eval(nt, ft)

    def display(self, nt, ft, depth=0):
        print "%sMULT" % (tabstop * depth)
        self.lhs.display(nt, ft, depth + 1)
        self.rhs.display(nt, ft, depth + 1)

    #print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))
    def translate(self, nt, ft):
        global code

        keyl = self.lhs.translate(nt, ft)
        keyr = self.rhs.translate(nt, ft)
        keyt = addTempToSymbolTable()

        code += "LDA " + keyl + "\n"
        code += "MUL " + keyr + "\n"

        code += "STA " + keyt + "\n"

        return keyt


class Plus(Expr):
    '''expression for binary addition'''

    def __init__(self, lhs, rhs):
        if lhs.isList() or rhs.isList():
            raise Exception("Operation cannot apply to lists")
        self.lhs = lhs
        self.rhs = rhs

    def eval(self, nt, ft):
        return self.lhs.eval(nt, ft) + self.rhs.eval(nt, ft)

    def display(self, nt, ft, depth=0):
        print "%sADD" % (tabstop * depth)
        self.lhs.display(nt, ft, depth + 1)
        self.rhs.display(nt, ft, depth + 1)

    #print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))
    def translate(self, nt, ft):
        global code

        keyl = self.lhs.translate(nt, ft)
        keyr = self.rhs.translate(nt, ft)
        keyt = addTempToSymbolTable()

        code += "LDA " + keyl + "\n"
        code += "ADD " + keyr + "\n"

        code += "STA " + keyt + "\n"

        return keyt


class Minus(Expr):
    '''expression for binary subtraction'''

    def __init__(self, lhs, rhs):
        if lhs.isList() or rhs.isList():
            raise Exception("Operation cannot apply to lists")
        self.lhs = lhs
        self.rhs = rhs

    def eval(self, nt, ft):
        return self.lhs.eval(nt, ft) - self.rhs.eval(nt, ft)

    def display(self, nt, ft, depth=0):
        print "%sSUB" % (tabstop * depth)
        self.lhs.display(nt, ft, depth + 1)
        self.rhs.display(nt, ft, depth + 1)

    #print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))
    def translate(self, nt, ft):
        global code

        keyl = self.lhs.translate(nt, ft)
        keyr = self.rhs.translate(nt, ft)
        keyt = addTempToSymbolTable()

        code += "LDA " + keyl + "\n"
        code += "SUB " + keyr + "\n"

        code += "STA " + keyt + "\n"

        return keyt


class FunCall(Expr):
    '''stores a function call:
      - its name, and arguments'''

    def __init__(self, name, argList):
        self.name = name
        self.argList = argList

    def eval(self, nt, ft):
        return ft[self.name].apply(nt, ft, self.argList)

    def display(self, nt, ft, depth=0):
        print "%sFunction Call: %s, args:" % (tabstop * depth, self.name)
        for e in self.argList:
            e.display(nt, ft, depth + 1)


#-------------------------------------------------------

class Stmt:
    '''Virtual base class for statements in the language'''

    def __init__(self):
        raise NotImplementedError(
            'Stmt: pure virtual base class.  Do not instantiate')

    def eval(self, nt, ft):
        '''Given an environment and a function table, evaluates the expression,
        returns the value of the expression (an int in this grammar)'''

        raise NotImplementedError(
            'Stmt.eval: virtual method.  Must be overridden.')

    def display(self, nt, ft, depth=0):
        'For debugging.'
        raise NotImplementedError(
            'Stmt.display: virtual method.  Must be overridden.')

    def translate(self, nt, ft, depth=0):
        raise NotImplementedError(
            'Stmt.translate: virtual method.  Must be overridden.')


class AssignStmt(Stmt):
    '''adds/modifies symbol in the current context'''

    def __init__(self, name, rhs):
        '''stores the symbol for the l-val, and the expressions which is the
        rhs'''
        self.name = name
        self.rhs = rhs

    def eval(self, nt, ft):
        nt[self.name] = self.rhs.eval(nt, ft)

    def display(self, nt, ft, depth=0):
        print "%sAssign: %s :=" % (tabstop * depth, self.name)
        self.rhs.display(nt, ft, depth + 1)

    def translate(self, nt, ft):
        #print "%sAssign: %s :=" % (tabstop*depth, self.name)
        global code
        keyResult = self.rhs.translate(nt, ft)
        code += 'LDA ' + keyResult + "\n"
        code += 'STA ' + str(self.name) + "\n"


class IfStmt(Stmt):
    def __init__(self, cond, tBody, fBody):
        '''expects:
        cond - expression (integer)
        tBody - StmtList
        fBody - StmtList'''

        self.cond = cond
        self.tBody = tBody
        self.fBody = fBody

    def eval(self, nt, ft):
        if self.cond.eval(nt, ft) > 0:
            self.tBody.eval(nt, ft)
        else:
            self.fBody.eval(nt, ft)

    def display(self, nt, ft, depth=0):
        print "%sIF" % (tabstop * depth)
        self.cond.display(nt, ft, depth + 1)
        print "%sTHEN" % (tabstop * depth)
        self.tBody.display(nt, ft, depth + 1)
        print "%sELSE" % (tabstop * depth)
        self.fBody.display(nt, ft, depth + 1)

    def translate(self, nt, ft):
        keyC = self.cond.translate(nt, ft)
        global linkerCounter
        global code

        code += "LDA " + keyC + "\n"
        code += "JMN " + 'L' + str(linkerCounter) + '\n'
        code += "JMZ " + 'L' + str(linkerCounter) + '\n'
        linkerCounter += 1

        #call code for true
        self.tBody.translate(nt, ft)
        code += "JMP " + 'L' + str(linkerCounter) + '\n'

        code += 'L' + str(linkerCounter - 1) + ': '
        linkerCounter += 1

        #call code for false
        self.fBody.translate(nt, ft)

        #go to rest of code
        code += 'L' + str(linkerCounter - 1) + ': '


class WhileStmt(Stmt):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def eval(self, nt, ft):
        while self.cond.eval(nt, ft) > 0:
            self.body.eval(nt, ft)

    def display(self, nt, ft, depth=0):
        print "%sWHILE" % (tabstop * depth)
        self.cond.display(nt, ft, depth + 1)
        print "%sDO" % (tabstop * depth)
        self.body.display(nt, ft, depth + 1)

    def translate(self, nt, ft):
        global linkerCounter
        global code

        code += 'L' + str(linkerCounter) + ': '
        linkerCounter += 1

        #calls condition
        keyC = self.cond.translate(nt, ft)

        code += "LDA " + keyC + "\n"
        code += "JMN " + 'L' + str(linkerCounter) + '\n'
        code += "JMZ " + 'L' + str(linkerCounter) + '\n'
        linkerCounter += 1

        #call code for body
        self.body.translate(nt, ft)

        code += "JMP " + 'L' + str(linkerCounter - 2) + '\n'

        code += 'L' + str(linkerCounter - 1) + ': '

#-------------------------------------------------------

class StmtList:
    '''builds/stores a list of Stmts'''

    def __init__(self):
        self.sl = []

    def insert(self, stmt):
        self.sl.insert(0, stmt)

    def eval(self, nt, ft):
        for s in self.sl:
            s.eval(nt, ft)

    def display(self, nt, ft, depth=0):
        print "%sSTMT LIST" % (tabstop * depth)
        for s in self.sl:
            s.display(nt, ft, depth + 1)

    def translate(self, nt, ft):
        for s in self.sl:
            s.translate(nt, ft)


class Program:
    def __init__(self, stmtList):
        self.stmtList = stmtList
        self.nameTable = {}
        self.funcTable = {}

    def eval(self):
        self.stmtList.eval(self.nameTable, self.funcTable)

    def dump(self):
        print "Dump of Symbol Table"
        print "Name Table"
        for k in self.nameTable:
            print "  %s -> %s " % ( str(k), str(self.nameTable[k]) )
        print "Function Table"
        for k in self.funcTable:
            print "  %s" % str(k)
        print ""

    def display(self, depth=0):
        #print "%sPROGRAM :" % (tabstop*depth)
        self.stmtList.display(self.nameTable, self.funcTable)

    def translate(self):
        self.stmtList.translate(self.nameTable, self.funcTable)
        global code
        code += 'HLT'
        return code

    def optimize(self, code):
        #optimized cases:
        #lda a lda a #drop second
        #sta a sta a #drop second
        #lda a sta a #drop second
        #sta a lda a #drop second

        tokenizedCode = ''
        lines = code.split('\n')
        print lines, '\n\n'
        while len(lines) > 1:

            focus = lines.pop(0)
            focusSplit = focus
            tokens = focusSplit.split(' ')

            if tokens[0][-1] == ':':
                tokens = tokens[1:]
            if tokens[0] == "LDA" or tokens[0] == "STA":
                comp = lines[0]
                comp_tokens = comp.split(' ')
                #if comp_tokens[0][-1] == ':':
                #	comp_tokens = comp_tokens[1:]
                if (comp_tokens[0] == "LDA" or comp_tokens[0] == "STA") and tokens[1] == comp_tokens[1]:
                    lines[0] = focus
                    continue

            tokenizedCode += focus + '\n'

        tokenizedCode += lines[0]

        return tokenizedCode

    def link(self, code):
        lineNumber = 0
        tokenizedCode = ''
        lines = code.split('\n')
        for l in lines:
            tok = l.split(' ')
            lineNumber += 1
            if tok[0][-1] == ':':
                addToSymbolTable(tok[0][0:-1], lineNumber, 'label')
                tok = tok[1:]
            if tok[0] == "HLT":
                pass
            elif tok[0][0] == 'J':
                #replace L_ with line number on second pass
                pass

            else:
                tok[1] = getAddressFromSymbolTable(tok[1])

            tokenizedCode += ' '.join(tok)
            tokenizedCode += '\n'

        tokenizedCode = tokenizedCode[0:-1]
        #second pass to replace jump links
        lines = tokenizedCode.split('\n')
        tokenizedCode = ''
        for l in lines:
            tok = l.split(' ')
            if tok[0][0] == 'J':
                #replace L_ with line number
                tok[1] = str(getValueFromSymbolTable(tok[1]))

            tokenizedCode += ' '.join(tok)
            tokenizedCode += '\n'

        return tokenizedCode[0:-1]

    def compile(self, opt=False):
        '''calls translate, optionally calls optimize, and then calls link'''
        global code
        code = ''

        symbCode = self.translate()
        print 'Symbolic: \n', symbCode, '\n\n\n\n'
        self.printToFile('symbolic.out', symbCode)

        if opt:
            optimizedCode = self.optimize(symbCode)
            linkedCode = self.link(optimizedCode)
            print 'optimizedCode: \n', linkedCode, '\n\n'
            self.printToFile('linkedOptimized.out', linkedCode)

        linkedCode = self.link(symbCode)
        print 'linkedCode: \n', linkedCode, '\n\n'
        self.printToFile('linkedNonOpt.out', linkedCode)

        symTable = dumpSymbolTable()
        print 'symbolTable: \n', symTable
        self.printToFile('symbolTable.out', symTable)

    def printToFile(self, fileName, toOut):
        fout = open(fileName, 'w')
        for l in toOut:
            fout.write(l)
        fout.close()
