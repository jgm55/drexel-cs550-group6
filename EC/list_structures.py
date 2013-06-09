#!/usr/bin/python
#
# CS550 Group 6
# Ryan Daugherty
# Tom Houman
# Joe Muoio
# CS550 Spring 2013
# Assignment 2
#
# list_structures.py
# Classes supporting parsing and interpreting of lists in mini language

from structures import Expr

tabstop = '  '  # 2 spaces


class Concat(Expr):
    '''expression for concating two lists'''

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def eval(self, nt):
        return self.lhs.eval(nt) + self.rhs.eval(nt)

    def display(self, nt,depth=0):
        print "%sCONCAT" % (tabstop * depth)
        self.lhs.display(nt, depth + 1)
        self.rhs.display(nt, depth + 1)


class Element(Expr):
    '''Lists and numbers inheret from this'''

    def __init__(self):
        raise NotImplementedError('Cannot have an element object')

    def eval(self, nt):
        raise NotImplementedError(
            'Expr.eval: virtual method.  Must be overridden.')

    def display(self, nt, depth=0):
        raise NotImplementedError(
            'Expr.display: virtual method.  Must be overridden.')


class List(Element):
    '''Lists of expressions'''

    def __init__(self, v=[]):
        self.contents = v

    def eval(self, nt):
        self.eval_contents = []
        for i in self.contents:
            self.eval_contents.append(i.eval(nt))
        return self.eval_contents

    def display(self, nt, depth=0):
        if len(self.contents) < 1:
            print "%s*empty list*" % (tabstop * depth)
        for i in self.contents:
            if isinstance(i, List):
                i.display(nt, depth + 1)
            else:
                i.display(nt, depth)

    def isList(self):
        return True


class Number(Element):
    '''Just integers'''

    def __init__(self, v=0):
        self.value = v

    def eval(self, nt):
        return self.value

    def display(self, nt, depth=0):
        print "%s%i" % (tabstop * depth, self.value)

    def isInt(self):
        return True


class Car(Expr):
    '''first entry'''

    def __init__(self, v=""):
        self.label = v

    def eval(self, nt):
        L = self.label.eval(nt)

        if not isinstance(L, list):
            raise Exception("Argument must be a list")
            return
        try:
            print "L0 is ", L[0]
            return L[0]
        except:
            raise Exception("No elements left in the list to return")
        #raise exception

    def display(self, nt, depth=0):
        L = self.label.eval(nt)
        try:
            if len(L) > 0:
                L[0].display(nt, depth)
        except:
            raise Exception("ERROR LISTED ABOVE") #prob doesnt need this


class Cdr(Expr):
    '''All entries but the first'''

    def __init__(self, v=""):
        self.label = v

    def eval(self, nt):
        ''' returns the rest of the list (minus the first element) '''
        L = self.label.eval(nt)
        if not isinstance(L, list):
            raise Exception("Argument must be a list")
        #return
        if len(L) == 1:
            return []
        try:
            return L[1:]
        except:
            raise Exception("There are less than two elements in the list.")

    def display(self, nt, depth=0):
        L = self.label.eval(nt)
        for i in range(1, len(L)):
            L[i].display(nt,depth)


class Cons(Expr):
    '''first entry'''

    def __init__(self, v_e="", v_l=""):
        self.label_e = v_e
        self.label_l = v_l

    def eval(self, nt):
        '''returns a new list, with element e prepended to the front of list L '''

        e = self.label_e.eval(nt)
        L = self.label_l.eval(nt)
        #print "e",e,type(e)
        #print "L",L,type(L)
        #print "L[0]",L[0],type(L[0])
        if not isinstance(L, list):
            raise Exception("Second argument must be a list")
            return
        C = [e] + L
        return C

    def display(self, nt,depth=0):
        e = self.label_e.eval(nt)
        L = self.label_l.eval(nt)
        if isinstance(e, list):
            for i in e:
                i.display(nt, depth + 1)
        else:
            print "%s%i" % (tabstop * depth, e)
        #e.display( nt, depth )
        for i in L:
            if isinstance(i, List):
                i.display(nt, depth + 1)
            else:
                i.display(nt, depth)


class Nullp(Expr):
    '''first entry'''

    def __init__(self, v=""):
        self.label = v

    def eval(self, nt):
        ''' returns 1 if L is null, 0 otherwise '''
        L = self.label.eval(nt)
        if not isinstance(L, list):
            raise Exception("Argument must be a list")
        if len(L) > 0:
            return 0
        return 1
    def isInt(self):
        return True
    def display(self, nt, depth=0):
        L = nt[self.label]
        if len(L) > 0:
            print "%s%i" % (tabstop * depth, 0)
        else:
            print "%s%i" % (tabstop * depth, 1)


class Intp(Expr):
    '''first entry'''

    def __init__(self, v=""):
        self.label = v

    def eval(self, nt):
        '''returns 1 if e is an integer, 0 otherwise '''

        e = self.label.eval(nt)
        if isinstance(e, int):
            return 1
        return 0
    def isInt(self):
        return True

    def display(self, nt, depth=0):
        e = self.label.eval(nt)
        if isinstance(e, int):
            print "%s%i" % (tabstop * depth, 1)
        else:
            print "%s%i" % (tabstop * depth, 0)


class Listp(Expr):
    '''first entry'''

    def __init__(self, v=""):
        self.label = v

    def eval(self, nt):
        '''returns 1 if e is a list, 0 otherwise'''
        e = self.label.eval(nt)
        if isinstance(e, list):
            return 1
        return 0
    def isInt(self):
        return True

    def display(self, nt, depth=0):
        e = self.label.eval(nt)
        if isinstance(e, list):
            print "%s%i" % (tabstop * depth, 1)
        else:
            print "%s%i" % (tabstop * depth, 0)
