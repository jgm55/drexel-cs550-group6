#!/usr/bin/python
#
# CS550 Group 6
# Ryan Daugherty
# Tom Houman
# Joe Muoio
# CS550 Spring 2013
# Assignment 2
#
# A python implementation of the mini language, with user-defined functions
# Modified from code provided by Kurt Schmidt

import sys
from structures import *
from list_structures import *

######   LEXER   ###############################

from ply import lex

scope_mode = None


tokens = (
    'PLUS',
    'MINUS',
    'TIMES',
    'LPAREN',
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    'CONCAT',
    'SEMICOLON',
    'COMMA',
    'NUMBER',
    'ASSIGNOP',
    'WHILE',
    'DO',
    'OD',
    'IF',
    'THEN',
    'ELSE',
    'FI',
    'PROC',
    'END',
    'IDENT',
    'CONS',
    'CDR',
    'CAR',
    'NULLP',
    'INTP',
    'LISTP',
    'DOT',
    'COLON',
    'CLASSWORD'#not sure if necessay
)

# These are all caught in the IDENT rule, typed there.
reserved = {
    'while': 'WHILE',
    'do': 'DO',
    'od': 'OD',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    'proc': 'PROC',
    'end': 'END',
    'car': 'CAR',
    'cdr': 'CDR',
    'nullp': 'NULLP',
    'cons': 'CONS',
    'intp': 'INTP',
    'listp': 'LISTP',
    'class': 'CLASSWORD'
}

# Now, this section.  We have a mapping, REs to token types (please note
# the t_ prefix).  They simply return the type.

# t_ignore is special, and does just what it says.  Spaces and tabs
t_ignore = ' \t'

# These are the simple maps
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_CONCAT = r'\|\|'
t_ASSIGNOP = r':='
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'.'
t_COLON = r':'


def t_IDENT(t):
    #r'[a-zA-Z_][a-zA-Z_0-9]*'
    r'[a-z]+'
    t.type = reserved.get(t.value, 'IDENT')    # Check for reserved words
    return t


def t_NUMBER(t):
    r'[0-9]+'

    # t.value holds the string that matched.  Dynamic typing - no unions
    t.value = int(t.value)
    return t

# These are standard little ditties:
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

    # Error handling rule


def t_error(t):
    print "Illegal character '%s' on line %d" % ( t.value[0], t.lexer.lineno )
    return t
    #t.lexer.skip( 1 )


lex.lex()

#-----   LEXER (end)   -------------------------------


######   YACC   #####################################

import ply.yacc as yacc

# create a function for each production (note the prefix)
# The rule is given in the doc string

def p_program(p):
    'program : class_and_stmt_list'
    P = Program(p[1])
    #P.display()
    print 'Running Program'
    P.eval()
    P.dump()

def p_stmt_and_class_list(p):
    '''class_and_stmt_list : class SEMICOLON class_and_stmt_list
            | stmt_list
            | class'''
def p_class(p):
    '''class : class_non_inherit
        | class_inherit'''
    p[0] = p[1]
def p_class_no_inherit(p):
    'class_non_inherit : CLASSWORD d_ident LPAREN param_list RPAREN stmt_list END'
    p[0] = Class()
    
def p_class_inherit(p):
    'class_inherit : CLASSWORD d_ident LPAREN param_list RPAREN COLON d_ident stmt_list END'
    
def p_stmt_list(p):
    '''stmt_list : stmt SEMICOLON stmt_list
       | stmt'''

    if len(p) == 2:  # single stmt => new list
        p[0] = StmtList()
        p[0].insert(p[1])
    else:  # we have a stmtList, keep adding to front
        p[3].insert(p[1])
        p[0] = p[3]


def p_stmt(p):
    '''stmt : assign_stmt
                | while_stmt
                | if_stmt'''
    p[0] = p[1]


def p_add(p):
    'expr : expr PLUS term'
    p[0] = Plus(p[1], p[3])


def p_sub(p):
    'expr : expr MINUS term'
    p[0] = Minus(p[1], p[3])


def p_expr_list(p):
    '''expr_list : expr COMMA expr_list
                | expr'''
    if len(p) == 2:  # single expr => new list
        p[0] = [p[1]]
    else:  # we have a expr_list, keep adding to front
        p[3].insert(0, p[1])
        p[0] = p[3]


def p_expr_term(p):
    'expr : term'
    p[0] = p[1]

def p_expr_to_proccall(p):
    'expr : proc_call'
    p[0] = p[1]
    
def p_proc_call(p):
    'proc_call : PROC LPAREN param_list RPAREN stmt_list END'
    if scope_mode == "static":
        p[0] = StaticProc(p[3], p[5])
    elif scope_mode == "dynamic":
        p[0] = DynamicProc(p[3], p[5])
    else:
        raise Exception("Scope not set")
    

def p_mult(p):
    '''term : term TIMES fact'''
    p[0] = Times(p[1], p[3])


def p_term_fact(p):
    'term : fact'
    p[0] = p[1]


def p_fact_expr(p):
    'fact : LPAREN expr RPAREN'
    p[0] = p[2]


def p_fact_NUM(p):
    'fact : NUMBER'
    p[0] = Number(p[1])


def p_fact_IDENT(p):
    'fact : d_ident'
    p[0] = p[1]

def p_assn(p):
    'assign_stmt : IDENT ASSIGNOP expr'
    p[0] = AssignStmt(p[1], p[3])
    
def p_while(p):
    'while_stmt : WHILE expr DO stmt_list OD'
    p[0] = WhileStmt(p[2], p[4])

def p_if(p):
    'if_stmt : IF expr THEN stmt_list ELSE stmt_list FI'
    p[0] = IfStmt(p[2], p[4], p[6])

def p_param_list(p):
    '''param_list : IDENT COMMA param_list
                | IDENT'''
    if len(p) == 2:  # single param => new list
        p[0] = [p[1]]
    else:  # we have a param_list, keep adding to front
        p[3].insert(0, p[1])
        p[0] = p[3]

def p_expr_to_funcall(p):
    'expr : func_call'
    p[0] = p[1]

def p_inline_func_call(p):
    'func_call : proc_call LPAREN expr_list RPAREN'
    p[0] = InlineFunCall(p[1], p[3])
	
def p_func_call(p):
    'func_call : IDENT LPAREN expr_list RPAREN'
    p[0] = FunCall(p[1], p[3])


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!", str(p)
    sys.exit(2)


def p_def_ident(p):
    'd_ident : IDENT'
    p[0] = Ident(p[1])


def p_concat(p):
    'expr : expr CONCAT list'
    p[0] = Concat(p[1], p[3])


def p_concat_id(p):
    'expr : expr CONCAT d_ident'
    p[0] = Concat(p[1], p[3])


def p_list(p):
    'list : LSQUARE sequence RSQUARE'
    p[0] = List(p[2])


def p_empty_list(p):
    'list : LSQUARE RSQUARE'
    p[0] = List([])


def p_sequence(p):
    'sequence : list_element COMMA sequence'
    p[0] = [p[1]] + p[3]


def p_sequence_list_element(p):
    'sequence : list_element'
    p[0] = [p[1]]


def p_list_element_element(p):
    'list_element : expr'
    p[0] = p[1]

def p_expr_to_list(p):
    'expr : list'
    p[0] = p[1]


def p_func_call_cons(p):
    'func_call : CONS LPAREN expr COMMA expr RPAREN'
    p[0] = Cons(p[3], p[5])


def p_func_call_car(p):
    'func_call : CAR LPAREN expr RPAREN'
    p[0] = Car(p[3])


def p_func_call_cdr(p):
    'func_call : CDR LPAREN expr RPAREN'
    p[0] = Cdr(p[3])


def p_func_call_nullp(p):
    'func_call : NULLP LPAREN expr RPAREN'
    p[0] = Nullp(p[3])


def p_func_call_intp(p):
    'func_call : INTP LPAREN expr RPAREN'
    p[0] = Nullp(p[3])


def p_func_call_listp(p):
    'func_call : LISTP LPAREN expr RPAREN' # was list_elem
    p[0] = Listp(p[3])

##############################################

# now, build the parser
yacc.yacc()


######   MAIN   #################################

def test_scanner(arg=sys.argv):
    data = ' 1+2 1-2 3*4 x blah y := 5 '

    lex.input(data)

    # attempt to get that first token
    tok = lex.token()
    while tok:
        print tok
        tok = lex.token()


def test_parser(args=sys.argv):

    global scope_mode
    
    if len(args) > 1:
        if args[1] == "static" or args[1] == "dynamic":
            scope_mode = args[1]
        else:
            raise Exception("Scope type not set.")
    else:
        raise Exception("Scope type not set.")
	
    print "Please enter the program,  terminate with CTRL+D on a new line"

    data = ""
    data += sys.stdin.read()
    yacc.parse(data)


if __name__ == '__main__':
    test_parser()

