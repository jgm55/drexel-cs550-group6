#!/usr/bin/python
#
# Ryan Daugherty
# Tom Houman
# Joe Muoio


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

    def cons(self, car, cdr):
        """Allocate a free block and return the element.
           Performs garbage collection no available blocks.
           If none available after GC, throws an error"""
        if self.avail.isptr and self.avail.val >= 0:
            avail = self.avail
            self.avail = self.cells[avail.val].cdr
        else:
            # Garbage collection
            # Loop over all context and mark accessible lists
            #for ctx in self.ctx:
            #    for name, val in ctx:
            #        if isinstance(val, ListElt):
            #            self.mark(val)
            #print "GC Mark Result:"
            print "GC Not implemented. Memory:"
            print str(self)
            print "Context:"
            print self.ctx
            raise Exception("Garbage collect not implemented")

        self.cells[avail.val].update(car, cdr)
        return avail

    def mark(self, elt):
        if elt.isnull():
            return

        if elt.isptr:
            self.mark(self.cells[elt.val].car)
            self.cells[elt.val].cdr.mark = True
            self.mark(self.cells[elt.val].cdr)

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

