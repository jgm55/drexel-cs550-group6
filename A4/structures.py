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

import sys

####  CONSTANTS   ################

# the variable name used to store a proc's return value
returnSymbol = 'return'

tabstop = '  ' # 2 spaces

#####  Globals    #################

code = '' # the compiled code


######### Helper classes ############

class SymbolTable:

    # class-wide link count (static)
    linkcount = 0

    def __init__(self):
        # maps a symbolic key to a tuple containing (memory address, value, label)
        self.table = {}

        # current local variable count (including temporary)
        self.localcount = 1

        # current local temporary count
        self.tempcount = 1
        pass

    @classmethod
    def makeLink(cls):
        cls.linkcount += 1
        return 'L' + str(cls.linkcount)

    def dump(self):
        table = ""
        allocations = [0] * self.localcount
        for k, v in self.table.iteritems():
            allocations[int(v[0])] = k
        for i in range(1, self.localcount):
            k = allocations[i]
            v = self.table[k]
            table += str(v[0]) + "  " + str(v[1]) + " ; "
            table += str(v[2]) + ' ' + k
            table += "\n"
        return table

    def getAddress(self, key):
        try:
            address = self.table[key][0]
        except:
            address = self.table[self.add(key, 0, 'variable')][0]
        return address

    def getValue(self, key):
        try:
            val = self.table[key][1]
        except:
            val = self.table[self.add(key, 0, 'variable')][1]
        return val

    def add(self, key, value, t):
        # adds the value at the location of key
        # key is the symbol in the program that was parsed
        # value is the numerical value of the thing being stored
        # returns the symbol table address.

        if key not in self.table:
            self.table[key] = (str(self.localcount), value, t)
            self.localcount += 1
        if t == 'label':
            temp = self.table[key][0]
            self.table[key] = (temp, value, t)
        return key

    def addTemp(self, value=0):
        # adds the value at the location of "temporary_#"
        # value is the numerical value of the key
        # returns the symbol table address.

        key = "Temp_" + str(self.tempcount)
        self.table[key] = (str(self.localcount), value, 'temporary')
        self.localcount += 1
        self.tempcount += 1
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

    def translate(self, st, ft):
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

    def translate(self, st, ft):
        key = str(self.name)
        st.add(key, 0, 'variable')
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
    def translate(self, st, ft):
        global code

        keyl = self.lhs.translate(st, ft)
        keyr = self.rhs.translate(st, ft)
        keyt = st.addTemp()

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
    def translate(self, st, ft):
        global code

        keyl = self.lhs.translate(st, ft)
        keyr = self.rhs.translate(st, ft)
        keyt = st.addTemp()

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
    def translate(self, st, ft):
        global code

        keyl = self.lhs.translate(st, ft)
        keyr = self.rhs.translate(st, ft)
        keyt = st.addTemp()

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

    def translate(self, st, ft):
        raise NotImplementedError('FunCall.translate: TODO')


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

    def translate(self, st, ft, depth=0):
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

    def translate(self, st, ft):
        #print "%sAssign: %s :=" % (tabstop*depth, self.name)
        global code
        keyResult = self.rhs.translate(st, ft)
        code += 'LDA ' + keyResult + "\n"
        code += 'STA ' + str(self.name) + "\n"


class DefineStmt(Stmt):
    '''Binds a proc object to a name'''

    def __init__(self, name, proc):
        self.name = name
        self.proc = proc

    def eval(self, nt, ft):
        ft[self.name] = self.proc

    def display(self, nt, ft, depth=0):
        print "%sDEFINE %s :" % (tabstop * depth, self.name)
        self.proc.display(nt, ft, depth + 1)

    def translate(self, st, ft):
        raise NotImplementedError('DefineStmt.translate: TODO')


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

    def translate(self, st, ft):
        keyC = self.cond.translate(st, ft)
        global code

        elseLink = SymbolTable.makeLink()
        continueLink = SymbolTable.makeLink()

        code += "LDA " + keyC + "\n"
        code += "JMN " + elseLink + '\n'
        code += "JMZ " + elseLink + '\n'

        #call code for true
        self.tBody.translate(st, ft)
        code += "JMP " + continueLink + '\n'

        code += elseLink + ': '

        #call code for false
        self.fBody.translate(st, ft)

        #go to rest of code
        code += continueLink + ': '


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

    def translate(self, st, ft):
        global code

        loopLink = SymbolTable.makeLink()
        continueLink = SymbolTable.makeLink()

        code += loopLink + ': '

        #calls condition
        keyC = self.cond.translate(st, ft)

        code += "LDA " + keyC + "\n"
        code += "JMN " + continueLink + '\n'
        code += "JMZ " + continueLink + '\n'

        #call code for body
        self.body.translate(st, ft)

        code += "JMP " + loopLink + '\n'
        code += continueLink + ': '

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

    def translate(self, st, ft):
        for s in self.sl:
            s.translate(st, ft)


class Proc:
    '''stores a procedure (formal params, and the body)

    Note that, while each function gets its own environment, we decided not to
    allow side-effects, so, no access to any outer contexts.  Thus, nesting
    functions is legal, but no different than defining them all in the global
    environment.  Further, all calls are handled the same way, regardless of
    the calling environment (after the actual args are evaluated); the proc
    doesn't need/want/get an outside environment.'''

    def __init__(self, paramList, body):
        '''expects a list of formal parameters (variables, as strings), and a
        StmtList'''

        self.parList = paramList
        self.body = body

    def apply(self, nt, ft, args):
        newContext = {}

        # sanity check, # of args
        if len(args) is not len(self.parList):
            print "Param count does not match:"
            sys.exit(1)

        # bind parameters in new name table (the only things there right now)
        # use zip, bastard
        for i in range(len(args)):
            print "self.parList[i]:", self.parList[i]
            print "args[i].eval( nt, ft )", args[i].eval(nt, ft)
            newContext[self.parList[i]] = args[i].eval(nt, ft)

        # evaluate the function body using the new name table and the old (only)
        # function table.  Note that the proc's return value is stored as
        # 'return in its nametable

        self.body.eval(newContext, ft)
        if newContext.has_key(returnSymbol):
            return newContext[returnSymbol]
        else:
            print "Error:  no return value"
            sys.exit(2)

    def display(self, nt, ft, depth=0):
        print "%sPROC %s :" % (tabstop * depth, str(self.parList))
        self.body.display(nt, ft, depth + 1)

    def translate(self, st, ft):
        raise NotImplementedError('Proc.translate: TODO')


class Program:
    def __init__(self, stmtList):
        self.stmtList = stmtList
        self.nameTable = {}
        self.funcTable = {}
        self.symbolTable = SymbolTable()

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
        self.stmtList.translate(self.symbolTable, self.funcTable)
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
                self.symbolTable.add(tok[0][0:-1], lineNumber, 'label')
                tok = tok[1:]
            if tok[0] == "HLT":
                pass
            elif tok[0][0] == 'J':
                #replace L_ with line number on second pass
                pass

            else:
                tok[1] = self.symbolTable.getAddress(tok[1])

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
                tok[1] = str(self.symbolTable.getValue(tok[1]))

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

        symTable = self.symbolTable.dump()
        print 'symbolTable: \n', symTable
        self.printToFile('symbolTable.out', symTable)

    def printToFile(self, fileName, toOut):
        fout = open(fileName, 'w')
        for l in toOut:
            fout.write(l)
        fout.close()
