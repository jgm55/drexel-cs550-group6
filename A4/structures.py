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
import copy

####  CONSTANTS   ################

# the variable name used to store a proc's return value
returnSymbol = 'return'

tabstop = '  ' # 2 spaces

# built-in symbols
PFP = '__PFP__'
RA = '__RA__'
SP = '__SP__'
FP = '__FP__'
BUF1 = '__BUF1__'
BUF2 = '__BUF2__'
RETURN = 'return'


######### Helper classes ############

class SymbolTable:
    def __init__(self):
        self.table = {}

    def add(self, key, value, comment):
        if key not in self.table:
            self.table[key] = (len(self.table) + 1, value, comment)
        else:
            raise Exception('Duplicate symbol ' + str(key))

    def setValue(self, key, value):
        self.table[key] = (self.table[key][0], value, self.table[key][2])

    def getAddr(self, key):
        return self.table[key][0]

    def getOffset(self, key):
        return self.table[key][0] - 1

    def size(self):
        return len(self.table)

    def dump(self):
        table = ""
        allocations = {}
        for k, v in self.table.iteritems():
            allocations[int(v[0])] = (v[1], v[2])
        for addr, v in sorted(allocations.iteritems()):
            table += str(addr) + "  " + str(v[0]) + " ; " + str(v[1])
            table += "\n"
        return table


class CompilerFunction:

    # class-wide link count (static)
    labelcount = 0

    def __init__(self, name):
        # map symbols to values during translation
        self.name = name
        self.param = {}
        self.var = {}
        self.temp = {}
        self.ret = {RETURN: 0}
        self.support = {PFP: 0, RA: 0}

        # map symbols to a tuple of (FP-offset, value) during linking
        self.table = SymbolTable()

        # code string built using addCode()
        self.code = ''

    @classmethod
    def makeLabel(cls):
        cls.labelcount += 1
        return 'L' + str(cls.labelcount)

    def addParam(self, key, order):
        if key not in self.param:
            self.param[key] = order
        return key

    def addVariable(self, key, value):
        if key not in self.var and key not in self.param and key not in self.ret:
            self.var[key] = value
        return key

    def addTemp(self, value=0):
        key = 'Temp_' + str(len(self.temp))
        self.temp[key] = value
        return key

    def addCode(self, code):
        self.code += code + '\n'

    def addCodeLabel(self, label):
        self.code += label + ": "

    def setCode(self, code):
        self.code = code

    def linkTable(self):
        offset = 0
        self.table = SymbolTable()
        offset = self.linkOrderedMap(self.param, self.table, offset)
        offset = self.linkMap(self.var, self.table, offset)
        offset = self.linkMap(self.temp, self.table, offset)
        offset = self.linkMap(self.ret, self.table, offset)
        offset = self.linkMap(self.support, self.table, offset)
        return offset

    def linkMap(self, map, table, offset):
        for key, value in sorted(map.iteritems()):
            self.table.add(key, value, key)
            offset += 1
        return offset

    def linkOrderedMap(self, map, table, offset):
        ordered = {}
        for key, value in map.iteritems():
            ordered[value] = key
        for order, key in sorted(ordered.iteritems()):
            self.table.add(key, 0, key)
            offset += 1
        return offset

    def stackSize(self):
        return self.table.size()

    def __str__(self):
        return self.code


class CompilerProgram:

    def __init__(self):
        self.mainKey = '__main__'
        self.functions = {}
        self.const = {}
        self.table = SymbolTable()
        self.bootcode = ''
        self.code = ''

    def dumpSymbolTable(self):
        return self.table.dump()

    def dumpActivationRecords(self):
        out = ''
        for key, func in sorted(self.functions.iteritems()):
            out += key + ':\n'
            out += func.table.dump()
        return out

    def addConst(self, value):
        # fun-fact: this implementation is auto-optimizing on constants
        key = self.constKey(value)
        if key not in self.const:
            self.const[key] = value
        return key

    def constKey(self, value):
        return 'Const_' + str(value)

    def addFunction(self, key):
        self.functions[key] = CompilerFunction(key)
        return self.functions[key]

    def addMainFunction(self):
        self.functions[self.mainKey] = CompilerFunction(self.mainKey)
        return self.functions[self.mainKey]

    def addBootCode(self, code):
        self.bootcode += code + '\n'

    def getFunction(self, key):
        return self.functions[key]

    def symbolic(self):
        self.code = ''
        self.code += self.bootcode
        for key, func in sorted(self.functions.iteritems()):
            self.code += str(func)

    def optimize(self):
        #optimized cases:
        #lda a lda a #drop second
        #sta a sta a #drop second
        #lda a sta a #drop second
        #sta a lda a #drop second

        # loop over each function and optimize code
        for key, func in self.functions.iteritems():
            optimizedCode = ''
            lines = str(func).split('\n')
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

                optimizedCode += focus + '\n'
            optimizedCode += lines[0]
            func.setCode(optimizedCode)

    def link(self):
        # create global symbol table (FP, SP, FPB)
        self.table = SymbolTable()
        self.table.add(SP, 0, 'Stack Pointer (SP)')
        self.table.add(FP, 0, 'Frame Pointer (FP)')
        self.table.add(BUF1, 0, 'Scratch buffer 1 (BUF1)')
        self.table.add(BUF2, 0, 'Scratch buffer 2 (BUF2)')

        # create activation records for each function
        # keep track of the maximum offset in each function
        maxoffset = 0
        for fkey, func in sorted(self.functions.iteritems()):
            maxoffset = max(func.linkTable(), maxoffset)

        # in order to do pointer arithmetic, we need to have a
        # constant for each possible offset into a function
        for i in range(maxoffset + 1):
            self.addConst(i)

        # we also need a constant for each movement of FP/SP
        for key, func in self.functions.iteritems():
            self.addConst(func.stackSize())

        # add constants to global symbol table
        for key, val in sorted(self.const.iteritems()):
            self.table.add(key, val, key)

        # get some static addresses for convenience
        aSP = str(self.table.getAddr(SP))
        aFP = str(self.table.getAddr(FP))
        aBUF1 = str(self.table.getAddr(BUF1))
        aBUF2 = str(self.table.getAddr(BUF2))

        # initialize FP and SP with correct values in memory
        initFP = self.table.size() + 1
        initSP = initFP + self.functions[self.mainKey].table.getOffset(RA)
        self.table.setValue(FP, initFP)
        self.table.setValue(SP, initSP)

        # bootstrap code to call main and then halt the program
        code = 'CAL ' + self.mainKey + '\n'
        code += 'HLT' + '\n'

        # first pass:
        # - lay out global code listing
        # - link constants globally
        # - transform non-const LD/ST to reference call stack
        # - transform CAL instructions
        for key, func in sorted(self.functions.iteritems()):
            lines = str(func).split('\n')
            for l in lines:
                if l:
                    tok = l.split(' ')
                    # skip labels for now
                    while tok[0][-1] == ':':
                        code += tok[0] + ' '
                        tok = tok[1:]
                    if tok[0] != 'CAL' and tok[1] in self.table.table:
                        # Link global constants and special registers
                        tok[1] = str(self.table.getAddr(tok[1]))
                        code += ' '.join(tok) + '\n'
                    elif tok[0] == 'LDA':
                        # convert LDA to load from offset from FP
                        code += 'LDA ' + aFP + '\n'
                        code += 'ADD ' + str(self.table.getAddr(self.constKey(func.table.getOffset(tok[1])))) + '\n'
                        code += 'STA ' + aBUF1 + '\n'
                        code += 'LDI ' + aBUF1 + '\n'
                    elif tok[0] == 'STA':
                        # convert STA to load from offset from FP
                        code += 'STA ' + aBUF2 + '\n'  # store AC in temp buffer
                        code += 'LDA ' + aFP + '\n'  # load current frame pointer
                        code += 'ADD ' + str(self.table.getAddr(self.constKey(func.table.getOffset(tok[1])))) + '\n'
                        code += 'STA ' + aBUF1 + '\n'  # store destination address
                        code += 'LDA ' + aBUF2 + '\n'  # reload AC from temp
                        code += 'STI ' + aBUF1 + '\n'  # store value indirectly in destination
                    elif tok[0] == 'JMI':
                        # convert JMI to load from offset from FP
                        code += 'LDA ' + aFP + '\n'
                        code += 'ADD ' + str(self.table.getAddr(self.constKey(func.table.getOffset(tok[1])))) + '\n'
                        code += 'STA ' + aBUF1 + '\n'
                        code += 'LDI ' + aBUF1 + '\n'
                        code += 'STA ' + aBUF1 + '\n'
                        code += 'JMI ' + aBUF1 + '\n'
                    elif tok[0] in ['ADD', 'SUB', 'MUL']:
                        # convert ADD/SUB/MUL to use offset from FP
                        code += 'STA ' + aBUF2 + '\n'  # store AC in temp buffer
                        code += 'LDA ' + aFP + '\n'  # load current frame pointer
                        code += 'ADD ' + str(self.table.getAddr(self.constKey(func.table.getOffset(tok[1])))) + '\n'
                        code += 'STA ' + aBUF1 + '\n'  # store target address
                        code += 'LDI ' + aBUF1 + '\n'  # load target
                        code += tok[0] + ' ' + aBUF2 + '\n'  # compute with temp
                    elif tok[0] == 'CAL':
                        # symbolic CAL is 'CAL func return arg1 ... argN'
                        fname = tok[1]
                        callfunc = self.functions[fname]
                        retsym = tok[2]
                        args = []
                        for arg in tok[3:]:
                            args.append(arg)

                        print 'call ' + fname + ', stacksize=' + str(callfunc.stackSize())
                        # Initiate call
                        # 1. Create activation record
                            # 1. Update FP and SP

                        # update FP (FP = SP + 1)
                        code += 'LDA ' + aFP + '\n'
                        code += 'STA ' + aBUF2 + '\n'  # save the old FP temporarily
                        code += 'LDA ' + aSP + '\n'
                        code += 'ADD ' + str(self.table.getAddr(self.constKey(1))) + '\n'
                        code += 'STA ' + aFP + '\n'

                        # update SP (SP = FP + addr(RA))
                        code += 'ADD ' + str(self.table.getAddr(self.constKey(callfunc.table.getOffset(RA)))) + '\n'
                        code += 'STA ' + aSP + '\n'

                        # store previous FP in activation record
                        code += 'LDA ' + aFP + '\n'
                        code += 'ADD ' + str(self.table.getAddr(self.constKey(callfunc.table.getOffset(PFP)))) + '\n'
                        code += 'STA ' + aBUF1 + '\n'
                        code += 'LDA ' + aBUF2 + '\n'  # the old FP we saved above
                        code += 'STI ' + aBUF1 + '\n'

                        # write args to activation record
                        argcount = 0
                        for arg in args:
                            if arg in self.table.table:
                                code += 'LDA ' + str(self.table.getAddr(arg)) + '\n'
                                code += 'STA ' + aBUF1 + '\n'  # value of global argument
                            else:
                                code += 'LDA ' + aFP + '\n'
                                code += 'ADD ' + str(self.table.getAddr(self.constKey(callfunc.table.getOffset(PFP)))) + '\n'
                                code += 'STA ' + aBUF1 + '\n'
                                code += 'LDI ' + aBUF1 + '\n'  # prev fp
                                code += 'ADD ' + str(self.table.getAddr(self.constKey(func.table.getOffset(arg)))) + '\n'
                                code += 'STA ' + aBUF1 + '\n'  # addr of local argument
                                code += 'LDI ' + aBUF1 + '\n'  # load value of argument
                                code += 'STA ' + aBUF1 + '\n'  # value of local argument

                            # arg value now in BUF1

                            # to get parameter address, assume ordering of parameters
                            # parameters start at FP
                            code += 'LDA ' + aFP + '\n'
                            code += 'ADD ' + str(self.table.getAddr(self.constKey(argcount))) + '\n'
                            code += 'STA ' + aBUF2 + '\n'  # destination
                            code += 'LDA ' + aBUF1 + '\n'  # load value of argument
                            code += 'STI ' + aBUF2 + '\n'  # store to destination
                            argcount += 1

                        # use CAL to jump to procedure (stores return address (RA) for us)
                        code += 'CAL ' + fname + '\n'

                        # (call has returned)
                        # retrieve return value from activation record
                        code += 'LDA ' + aFP + '\n'
                        code += 'ADD ' + str(self.table.getAddr(self.constKey(callfunc.table.getOffset(RETURN)))) + '\n'
                        code += 'STA ' + aBUF1 + '\n'  # addr of return value
                        code += 'LDA ' + aFP + '\n'
                        code += 'ADD ' + str(self.table.getAddr(self.constKey(callfunc.table.getOffset(PFP)))) + '\n'
                        code += 'STA ' + aBUF2 + '\n'  # previous FP addr
                        code += 'LDI ' + aBUF2 + '\n'  # previous FP
                        code += 'ADD ' + str(self.table.getAddr(self.constKey(func.table.getOffset(retsym)))) + '\n'
                        code += 'STA ' + aBUF2 + '\n'  # return symbol addr
                        code += 'LDI ' + aBUF1 + '\n'  # load return value
                        code += 'STI ' + aBUF2 + '\n'  # store in return symbol

                        # Reset FP (FP = prefFP)
                        code += 'LDA ' + aFP + '\n'
                        code += 'ADD ' + str(self.table.getAddr(self.constKey(callfunc.table.getOffset(PFP)))) + '\n'
                        code += 'STA ' + aBUF1 + '\n'
                        code += 'LDI ' + aBUF1 + '\n'  # prev fp
                        code += 'STA ' + aFP + '\n'

                        # Reset SP (SP = FP + addr(RA))
                        code += 'ADD ' + str(self.table.getAddr(self.constKey(func.table.getOffset(RA)))) + '\n'
                        code += 'STA ' + aSP + '\n'

                    else:
                        code += ' '.join(tok) + '\n'

        # second pass:
        # - count line numbers
        # - map and remove labels
        labels = {}
        lineNumber = 0
        lines = code.split('\n')
        code = ''
        for l in lines:
            if l:
                tok = l.split(' ')
                lineNumber += 1
                # handle any number of labels on the same line
                while tok[0][-1] == ':':
                    labels[tok[0][:-1]] = lineNumber
                    tok = tok[1:]

                code += ' '.join(tok) + '\n'

        # third pass:
        # - link jump labels
        lines = code.split('\n')
        code = ''
        for l in lines:
            if l:
                tok = l.split(' ')
                if tok[0] in ['JMP', 'JMZ', 'JMN', 'CAL']:
                    #replace L_ with line number
                    tok[1] = str(labels[tok[1]])
                code += ' '.join(tok) + '\n'

        # store result
        self.code = code

    def __str__(self):
        return self.code


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

    def translate(self, f, ft):
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

    def translate(self, f, ft):
        key = str(self.name)
        f.addVariable(key, 0)
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
    def translate(self, f, ft):
        temp = f.addTemp()
        lhs = self.lhs.translate(f, ft)
        rhs = self.rhs.translate(f, ft)
        f.addCode("LDA " + lhs)
        f.addCode("MUL " + rhs)
        f.addCode("STA " + temp)
        return temp


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
    def translate(self, f, ft):
        temp = f.addTemp()
        lhs = self.lhs.translate(f, ft)
        rhs = self.rhs.translate(f, ft)
        f.addCode("LDA " + lhs)
        f.addCode("ADD " + rhs)
        f.addCode("STA " + temp)
        return temp


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
    def translate(self, f, ft):
        temp = f.addTemp()
        lhs = self.lhs.translate(f, ft)
        rhs = self.rhs.translate(f, ft)
        f.addCode("LDA " + lhs)
        f.addCode("SUB " + rhs)
        f.addCode("STA " + temp)
        return temp


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

    def translate(self, f, ft):
        rtemp = f.addTemp()
        instr = 'CAL ' + self.name + ' ' + rtemp
        for arg in self.argList:
            instr += ' ' + arg.translate(f, ft)
        f.addCode(instr)
        return rtemp


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

    def translate(self, f, ft):
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

    def translate(self, f, ft):
        f.addVariable(self.name, 0)
        f.addCode('LDA ' + self.rhs.translate(f, ft))
        f.addCode('STA ' + self.name)


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

    def translate(self, f, ft):
        newFunction = ft.addFunction(self.name)
        self.proc.translate(newFunction, ft)


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

    def translate(self, f, ft):
        falseLabel = CompilerFunction.makeLabel()
        continueLabel = CompilerFunction.makeLabel()
        f.addCode("LDA " + self.cond.translate(f, ft))
        f.addCode("JMN " + falseLabel)
        f.addCode("JMZ " + falseLabel)
        self.tBody.translate(f, ft)
        f.addCode("JMP " + continueLabel)
        f.addCodeLabel(falseLabel)
        self.fBody.translate(f, ft)
        f.addCodeLabel(continueLabel)


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

    def translate(self, f, ft):
        loopLink = CompilerFunction.makeLabel()
        continueLink = CompilerFunction.makeLabel()
        f.addCodeLabel(loopLink)
        f.addCode("LDA " + self.cond.translate(f, ft))
        f.addCode("JMN " + continueLink)
        f.addCode("JMZ " + continueLink)
        self.body.translate(f, ft)
        f.addCode("JMP " + loopLink)
        f.addCodeLabel(continueLink)

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

    def translate(self, f, ft):
        for s in self.sl:
            s.translate(f, ft)


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

    def translate(self, f, ft):
        # add symbols for parameters
        count = 0
        for param in self.parList:
            f.addParam(param, count)
            count += 1

        # store a label for the start of the procedure
        f.addCodeLabel(f.name)

        # translate the function body
        self.body.translate(f, ft)

        # jump to calling location using support register
        f.addCode('JMI ' + RA)


class Program:
    def __init__(self, stmtList):
        self.stmtList = stmtList
        self.nameTable = {}
        self.funcTable = {}
        self.prog = CompilerProgram()

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
        self.prog = CompilerProgram()
        main = self.prog.addMainFunction()
        proc = Proc([], self.stmtList)
        proc.translate(main, self.prog)
        self.prog.symbolic()

    def compile(self, opt=False):
        '''calls translate, optionally calls optimize, and then calls link'''
        self.translate()
        print 'Symbolic: \n', str(self.prog), '\n\n\n\n'
        self.printToFile('symbolic.out', str(self.prog))

        if opt:
            newProg = copy.deepcopy(self.prog)
            newProg.optimize()
            newProg.link()
            print 'optimizedCode: \n', str(newProg), '\n\n'
            self.printToFile('linkedOptimized.out', str(newProg))

        self.prog.link()
        print 'linkedCode: \n', str(self.prog), '\n\n'
        self.printToFile('linkedNonOpt.out', str(self.prog))

        symbols = self.prog.dumpSymbolTable()
        print 'symbolTable: \n', symbols
        self.printToFile('symbolTable.out', symbols)

        ar = self.prog.dumpActivationRecords()
        print 'activationRecords: \n', ar
        self.printToFile('activationRecords.out', ar)

    def printToFile(self, fileName, toOut):
        fout = open(fileName, 'w')
        for l in toOut:
            fout.write(l)
        fout.close()
