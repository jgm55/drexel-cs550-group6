#!/usr/bin/python
#
# CS550 Group 6
# Ryan Daugherty
# Tom Houman
# Joe Muoio
# CS550 Spring 2013
# Assignment 2
#
# list_memory.py
# Classes supporting use of dynamic memory with garbage collection


class ListElt:
    """List element is either an integer or a pointer
       to another element in memory"""
    def __init__(self, val=-1, isptr=True):
        self.val = val
        self.isptr = isptr

    def isnull(self):
        return self.isptr and self.val == -1

    def __str__(self):
        ptr = ""
        if self.isptr:
            ptr = "*"
        return str(self.val) + ptr


class ListCell:
    """Cell in a list memory.
       Has an element (car: int or pointer to another list)
       and a link to the next cell in the list (cdr).
       Also contains a bit supporting mark-and-sweep garbage collection."""
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
        self.mark = False
        pass

    def update(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __str__(self):
        mark = ""
        if self.mark:
            mark = "X"
        return str(self.car) + ", " + str(self.cdr) + " " + mark


class ListMemory:
    """Dynamic memory for lists with mark and sweep garbage collection"""
    def __init__(self, size):
        self.size = size
        self.cells = []
        self.avail = ListElt(0, True)
        self.ctx = []

        # Build fixed size memory
        for i in range(size):
            self.cells.append(ListCell(ListElt(0, False),
                                       ListElt(i+1, True)))

        # Set cdr of last cell to end of list
        self.cells[-1].cdr = ListElt(-1, True)

    def concat(self, lhs, rhs):
        if not lhs.isptr or not rhs.isptr:
            raise Exception("Concat can only operate on list pointers")
        return self.cons(self.cells[lhs.val].car, rhs)

    def cons(self, car, cdr):
        """Allocate a free block and return the element.
           Performs garbage collection no available blocks.
           If none available after GC, throws an error"""
        if self.avail.isnull():
            # Garbage collection
            # Loop over all context and mark accessible lists
            for ctx in self.ctx:
                for name, val in ctx.items():
                    if isinstance(val, ListElt):
                        self.mark(val)
            # Sweep and reclaim unmarked cells
            self.sweep()

        if not self.avail.isnull():
            avail = self.avail
            self.avail = self.cells[avail.val].cdr
            self.cells[avail.val].update(car, cdr)
            return avail
        else:
            raise Exception("List memory full " +
                            "(size=" + str(self.size) + "). ")

    def mark(self, elt):
        if elt.isnull():
            return

        if elt.isptr:
            self.cells[elt.val].mark = True
            self.mark(self.cells[elt.val].car)
            self.mark(self.cells[elt.val].cdr)

    def sweep(self):
        i = 0
        for cell in self.cells:
            if not cell.mark:
                cell.car = ListElt(0, False)
                cell.cdr = self.avail
                self.avail = ListElt(i, True)
            else:
                cell.mark = False
            i += 1

    def pushctx(self, ctx):
        """Push a new context into the global context list"""
        self.ctx.append(ctx)

    def popctx(self):
        """Pop the last context from the global context list"""
        self.ctx.pop()

    def __str__(self):
        """Print memory to screen in a nice format"""
        out = ""
        out += "Cells:\n"
        for i in range(len(self.cells)):
            out += str(i) + ": " + str(self.cells[i]) + "\n"
        out += "Available: " + str(self.avail)
        return out

    def walk(self, elt, group=True):
        """Walk through memory and print the list starting with
           the input element"""
        if elt.isnull():
            return '[]'

        out = ""
        if elt.isptr:
            if group:
                out += '['
            out += self.walk(self.cells[elt.val].car)
            if not self.cells[elt.val].cdr.isnull():
                out += ', ' + self.walk(self.cells[elt.val].cdr, False)
            if group:
                out += ']'
        else:
            out += str(elt.val)

        return out

