#!/usr/bin/python
#
# CS550 Group 6
# Ryan Daugherty
# Tom Houman
# Joe Muoio
# CS550 Spring 2013
# Assignment 2
#
# structures.py
# Classes to represent underlying data structures for the grammar
# Modified from code provided by Kurt Schmidt

from types import *
import copy
import sys

####  CONSTANTS   ################

# the variable name used to store a proc's return value
returnSymbol = 'return'

tabstop = '  '  # 2 spaces

######   CLASSES   ##################


class Expr:
    '''Virtual base class for expressions in the language'''

    def __init__(self):
        raise NotImplementedError(
            'Expr: pure virtual base class.  Do not instantiate')

    def eval(self, nt):
        '''Given an environment and a function table, evaluates the expression,
        returns the value of the expression (an int in this grammar)'''

        raise NotImplementedError(
            'Expr.eval: virtual method.  Must be overridden.')

    def isList(self):
        return False

    def isInt(self):
        return False

    def display(self, nt, depth=0):
        'For debugging.'
        raise NotImplementedError(
            'Expr.display: virtual method.  Must be overridden.')


class Ident(Expr):
    '''Stores the symbol'''

    def __init__(self, name):
        self.name = name
    def isInt(self):
        return True
    def eval(self, nt):	
        return nt[self.name]

    def display(self, nt, depth=0):
        print "%s%s" % (tabstop * depth, self.name)


class Times(Expr):
    '''expression for binary multiplication'''
    def __init__(self, lhs, rhs):
        if (lhs.isInt() or type(lhs) is IntType) and (rhs.isInt() or type(rhs) is IntType):
            self.lhs = lhs
            self.rhs = rhs
        else:
            raise Exception("Operation can only apply to integers")

    def eval(self, nt):
        return self.lhs.eval(nt) * self.rhs.eval(nt)
    def isInt(self):
        return True
    def display(self, nt, depth=0):
        print "%sMULT" % (tabstop * depth)
        self.lhs.display(nt, depth + 1)
        self.rhs.display(nt, depth + 1)



class Plus(Expr):
    '''expression for binary addition'''

    def __init__(self, lhs, rhs):
        #print lhs, " ",rhs," ",type(lhs)," ",type(rhs)
        if (lhs.isInt() or type(lhs) is IntType) and (rhs.isInt() or type(rhs) is IntType):
            self.lhs = lhs
            self.rhs = rhs
        else:
            raise Exception("Operation can only apply to integers")
    def eval(self, nt):
        return self.lhs.eval(nt) + self.rhs.eval(nt)
    def isInt(self):
        return True
    def display(self, nt, depth=0):
        print "%sADD" % (tabstop * depth)
        self.lhs.display(nt, depth + 1)
        self.rhs.display(nt, depth + 1)



class Minus(Expr):
    '''expression for binary subtraction'''

    def __init__(self, lhs, rhs):
        #print lhs, " ",rhs," ",type(lhs)," ",type(rhs)
        if (lhs.isInt() or type(lhs) is IntType) and (rhs.isInt() or type(rhs) is IntType):
            self.lhs = lhs
            self.rhs = rhs
        else:
            raise Exception("Operation can only apply to integers")

    def eval(self, nt):
        return self.lhs.eval(nt) - self.rhs.eval(nt)
    def isInt(self):
        return True
    def display(self, nt, depth=0):
        print "%sSUB" % (tabstop * depth)
        self.lhs.display(nt, depth + 1)
        self.rhs.display(nt, depth + 1)

class InlineFunCall(Expr):
    '''stores a function call:
      - its name, and arguments'''

    def __init__(self, func, argList):
        self.func = func
        self.argList = argList

    def eval(self, nt):
        self.func.eval(nt)
        return self.func.apply(nt, self.argList)

    def display(self, nt, depth=0):
        print "%sFunction Call: %s, args:" % (tabstop * depth, self.name)
        for e in self.argList:
            e.display(nt, depth + 1)
	
class FunCall(Expr):
    '''stores a function call:
      - its name, and arguments'''

    def __init__(self, name, argList, classIns=None):
        self.name = name
        self.argList = argList
        self.classIns = classIns

    def eval(self, nt):
        if self.classIns is None:
            return nt[self.name].apply(nt, self.argList)
        else:
            print self.classIns, " classIns"
            print nt, "nt"
            #print 'other nt:',nt[self.classIns].nt
            print 'vars: ',vars(nt[self.classIns])
            return nt[self.classIns].nt[self.name].apply(nt, self.argList,True)

    def display(self, nt, depth=0):
        if self.classIns is None:
            print "%sFunction Call: %s, args:" % (tabstop * depth, self.name)
            for e in self.argList:
                e.display(nt, depth + 1)
        else:
            print "%sFunction Call: %s in %s (instance of %s), args:" % (tabstop * depth, self.name, nt[self.classIns].className)
            for e in self.argList:
                e.display(nt, depth + 1)        


#-------------------------------------------------------

class Stmt:
    '''Virtual base class for statements in the language'''

    def __init__(self):
        raise NotImplementedError(
            'Stmt: pure virtual base class.  Do not instantiate')

    def eval(self, nt):
        '''Given an environment and a function table, evaluates the expression,
        returns the value of the expression (an int in this grammar)'''

        raise NotImplementedError(
            'Stmt.eval: virtual method.  Must be overridden.')

    def display(self, nt, depth=0):
        'For debugging.'
        raise NotImplementedError(
            'Stmt.display: virtual method.  Must be overridden.')


class AssignStmt(Stmt):
    '''adds/modifies symbol in the current context'''

    def __init__(self, name, rhs):
        '''stores the symbol for the l-val, and the expressions which is the
        rhs'''
        self.name = name
        self.rhs = rhs

    def eval(self, nt):
        nt[self.name] = self.rhs.eval(nt)

    def display(self, nt, depth=0):
        print "%sAssign: %s :=" % (tabstop * depth, self.name)
        self.rhs.display(nt, depth + 1)


class DefineStmt(Stmt):
    '''Binds a proc object to a name'''

    def __init__(self, name, proc):
        self.name = name
        self.proc = proc

    def eval(self, nt):
        nt[self.name] = self.proc

    def display(self, nt, depth=0):
        print "%sDEFINE %s :" % (tabstop * depth, self.name)
        self.proc.display(nt, depth + 1)


class IfStmt(Stmt):
    def __init__(self, cond, tBody, fBody):
        '''expects:
        cond - expression (integer)
        tBody - StmtList
        fBody - StmtList'''

        self.cond = cond
        self.tBody = tBody
        self.fBody = fBody

    def eval(self, nt):
        if self.cond.eval(nt) > 0:
            self.tBody.eval(nt)
        else:
            self.fBody.eval(nt)

    def display(self, nt, depth=0):
        print "%sIF" % (tabstop * depth)
        self.cond.display(nt, depth + 1)
        print "%sTHEN" % (tabstop * depth)
        self.tBody.display(nt, depth + 1)
        print "%sELSE" % (tabstop * depth)
        self.fBody.display(nt, depth + 1)


class WhileStmt(Stmt):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def eval(self, nt):
        while self.cond.eval(nt) > 0:
            self.body.eval(nt)

    def display(self, nt, depth=0):
        print "%sWHILE" % (tabstop * depth)
        self.cond.display(nt, depth + 1)
        print "%sDO" % (tabstop * depth)
        self.body.display(nt, depth + 1)

#-------------------------------------------------------

class StmtList:
    '''builds/stores a list of Stmts'''

    def __init__(self):
        self.sl = []

    def insert(self, stmt):
        self.sl.insert(0, stmt)

    def eval(self, nt):
        for s in self.sl:
            s.eval(nt)

    def display(self, nt, depth=0):
        print "%sSTMT LIST" % (tabstop * depth)
        for s in self.sl:
            s.display(nt, depth + 1)


class StaticProc:
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
        try:
            paramList.remove('')
        except ValueError:
            pass
        self.parList = paramList
        self.body = body
        self.surrounding_nt = None
        
    def eval(self, nt):
        self.surrounding_nt = nt
        return self
        
    def apply(self, nt, args, classMethod = False):
        newContext = copy.copy(self.surrounding_nt)
        # sanity check, # of args
        if len(args) is not len(self.parList):
            print "Param count does not match:"
            sys.exit(1)
			
        # bind parameters in new name table, note that we are evaluating the arguments from the calling functions nametable
        for i in range(len(args)):	
            newContext[self.parList[i]] = args[i].eval(nt)
			
        # evaluate the function body using the new name table and the old (only)
        # function table.  Note that the proc's return value is stored as
        # 'return in its nametable
        
        self.body.eval(newContext)
        
        if classMethod:
            for key in self.surrounding_nt:
                self.surrounding_nt[key] = newContext[key]
        
        if newContext.has_key(returnSymbol):
            return newContext[returnSymbol]
        else:
            print "Error:  no return value"
            sys.exit(2)
           

    def display(self, nt, depth=0):
        print "%sPROC %s :" % (tabstop * depth, str(self.parList))
        self.body.display(nt, depth + 1)

class DynamicProc:
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
        try:
            paramList.remove('')
        except ValueError:
            pass
        self.parList = paramList
        self.body = body
        
    def eval(self, nt):
        return self
        
    def apply(self, nt, args):
        newContext = copy.copy(nt)
        # sanity check, # of args
        if len(args) is not len(self.parList):
            print "Param count does not match:"
            sys.exit(1)

        # bind parameters in new name table (the only things there right now)
        for i in range(len(args)):
            newContext[self.parList[i]] = args[i].eval(nt)

        # evaluate the function body using the new name table and the old (only)
        # function table.  Note that the proc's return value is stored as
        # 'return in its nametable

        self.body.eval(newContext)
        if newContext.has_key(returnSymbol):
            return newContext[returnSymbol]
        else:
            print "Error:  no return value"
            sys.exit(2)

    def display(self, nt, depth=0):
        print "%sPROC %s :" % (tabstop * depth, str(self.parList))
        self.body.display(nt, depth + 1) 

        
class classLookup:
    def __init__(self, ident, var):
        self.name = ident
        self.var = var
        
    def eval(self, nt):
        return nt[self.name].nt[self.var].eval(nt[self.name].nt)   
        
        
class classInstance:
    def __init__(self, parList, args, localnt, nt, className, stmtList):
        self.className = className
        self.args = args
        self.nt = localnt
        
        # sanity check, # of args
        if len(args) is not len(parList):
            print "Param count does not match:"
            sys.exit(1)

        # bind parameters in new name table (the only things there right now)
        for i in range(len(self.args)):
            self.nt[parList[i]] = self.args[i].eval(nt)
        print "before",self.nt    
        stmtList.eval(self.nt)
        print "after",self.nt  
        
class classDef:
    def __init__(self, ident, paramList, stmtList):
        self.name = ident
        try:
            paramList.remove('')
        except ValueError:
            pass
        self.parameters = paramList
        self.stmtList = stmtList
        self.surrounding_nt = None
        
    def eval(self, nt):
        nt[self.name] = self
        self.surrounding_nt = nt
        return self
        
    def apply(self, nt, args):
        newClassInst = classInstance(self.parameters, args, self.getNt(), nt, self.name, self.stmtList)
        return newClassInst
        
    def getNt(self):
        return copy.copy(self.surrounding_nt)
    
class Program:
    def __init__(self, stmtList):
        self.stmtList = stmtList
		# the global nt and ft
        self.nameTable = {}

    def eval(self):
        self.stmtList.eval(self.nameTable)

    def dump(self):
        print "Dump of Symbol Table"
        print "Name Table"
        for k in self.nameTable:
            print "  %s -> %s " % ( str(k), str(self.nameTable[k]) )
    

    def display(self, depth=0):
        #print "%sPROGRAM :" % (tabstop*depth)
        self.stmtList.display(self.nameTable)

