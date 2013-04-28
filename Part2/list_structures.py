#!/usr/bin/python
#
# Ryan Daugherty
# Tom Houman
# Joe Muoio

from structures import Expr
from list_memory import ListElt
from uuid import uuid1

tabstop = '  '  # 2 spaces


class Element(Expr):
    '''Lists and numbers inheret from this'''

    def __init__(self):
        raise NotImplementedError('Cannot have an element object')

    def eval(self, nt, ft, mem):
        raise NotImplementedError(
            'Expr.eval: virtual method.  Must be overridden.')

    def display(self, nt, ft, mem, depth=0):
        raise NotImplementedError(
            'Expr.display: virtual method.  Must be overridden.')


class List(Element):
    '''Lists of expressions'''

    def __init__(self, v=[]):
        self.contents = v

    def eval(self, nt, ft, mem):
        L = ListElt()
        tempkeys = []
        for i in reversed(self.contents):
            e = i.eval(nt, ft, mem)
            if not isinstance(e, ListElt):
                e = ListElt(e, False)
            L = mem.cons(e, L)
            # Save temporary list to name table to support GC
            tk = '___listtemp' + str(uuid1())
            tempkeys.append(tk)
            nt[tk] = L
        # Clean up temporary names
        for k in tempkeys:
            del nt[k]
        return L

    def display(self, nt, ft, mem, depth=0):
        if len(self.contents) < 1:
            print "%s*empty list*" % (tabstop * depth)
        for i in self.contents:
            if isinstance(i, List):
                i.display(nt, ft, mem, depth + 1)
            else:
                i.display(nt, ft, mem, depth)

    def isList(self):
        return True


class Number(Element):
    '''Just integers'''

    def __init__(self, v=0):
        self.value = v

    def eval(self, nt, ft, mem):
        return self.value

    def display(self, nt, ft, mem, depth=0):
        print "%s%i" % (tabstop * depth, self.value)

    def isInt():
        return True


class Car(Expr):
    '''first entry'''

    def __init__(self, v=""):
        self.label = v

    def eval(self, nt, ft, mem):
        L = self.label.eval(nt, ft, mem)

        if not isinstance(L, ListElt):
            raise Exception("Argument must be a list")
            return
        try:
            print "L0 is ", mem.cells[L.val].car
            return mem.cells[L.val].car
        except:
            raise Exception("No elements left in the list to return")
        #raise exception

    def display(self, nt, ft, mem, depth=0):
        L = self.label.eval(nt, ft, mem)
        try:
            if L.ptr:
                mem.cells[L.val].display(nt, ft, mem, depth)
        except:
            raise Exception("ERROR LISTED ABOVE") #prob doesnt need this


class Cdr(Expr):
    '''All entries but the first'''

    def __init__(self, v=""):
        self.label = v

    def eval(self, nt, ft, mem):
        ''' returns the rest of the list (minus the first element) '''
        L = self.label.eval(nt, ft, mem)
        if not isinstance(L, ListElt):
            raise Exception("Argument must be a list")
        #return
        try:
            return mem.cells[L.val].cdr
        except:
            raise Exception("There are less than two elements in the list.")

    def display(self, nt, ft, mem, depth=0):
        L = self.label.eval(nt, ft, mem)
        print "TODO Cdr display"
        #for i in range(1, len(L)):
        #    L[i].display(nt, ft, mem, depth)


class Cons(Expr):
    '''first entry'''

    def __init__(self, v_e="", v_l=""):
        self.label_e = v_e
        self.label_l = v_l

    def eval(self, nt, ft, mem):
        '''returns a new list, with element e prepended to the front of list L '''

        e = self.label_e.eval(nt, ft, mem)
        L = self.label_l.eval(nt, ft, mem)
        #print "e",e,type(e)
        #print "L",L,type(L)
        #print "L[0]",L[0],type(L[0])
        if not isinstance(L, ListElt):
            raise Exception("Second argument must be a ListElt")
            return
        E = e
        if not isinstance(e, ListElt):
            E = ListElt(e, False)
        #C = [e] + L
        return mem.cons(E, L)

    def display(self, nt, ft, mem, depth=0):
        e = self.label_e.eval(nt, ft, mem)
        L = self.label_l.eval(nt, ft, mem)
        if isinstance(e, ListElt):
            e.display()
        else:
            raise Exception("e is not a ListElt")
        if isinstance(L, ListElt):
            L.display()
        else:
            raise Exception("L is not a ListElt")


class Nullp(Expr):
    '''first entry'''

    def __init__(self, v=""):
        self.label = v

    def eval(self, nt, ft, mem):
        ''' returns 1 if L is null, 0 otherwise '''
        L = self.label.eval(nt, ft, mem)
        if not isinstance(L, ListElt):
            raise Exception("Argument must be a ListElt")
        if L.isptr and L.val == -1:
            return 1
        return 0

    def display(self, nt, ft, mem, depth=0):
        L = self.label.eval(nt, ft, mem)
        if L.isptr and L.val == -1:
            print "%s%i" % (tabstop * depth, 0)
        else:
            print "%s%i" % (tabstop * depth, 1)


class Intp(Expr):
    '''first entry'''

    def __init__(self, v=""):
        self.label = v

    def eval(self, nt, ft, mem):
        '''returns 1 if e is an integer, 0 otherwise '''

        e = self.label.eval(nt, ft, mem)
        if isinstance(e, int):
            return 1
        return 0

    def display(self, nt, ft, mem, depth=0):
        e = self.label.eval(nt, ft, mem)
        if isinstance(e, int):
            print "%s%i" % (tabstop * depth, 1)
        else:
            print "%s%i" % (tabstop * depth, 0)


class Listp(Expr):
    '''first entry'''

    def __init__(self, v=""):
        self.label = v

    def eval(self, nt, ft, mem):
        '''returns 1 if e is a list, 0 otherwise'''
        e = self.label.eval(nt, ft, mem)
        if isinstance(e, ListElt):
            return 1
        return 0

    def display(self, nt, ft, mem, depth=0):
        e = self.label.eval(nt, ft, mem)
        if isinstance(e, ListElt):
            print "%s%i" % (tabstop * depth, 1)
        else:
            print "%s%i" % (tabstop * depth, 0)
