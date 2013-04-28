#!/usr/bin/python
#
#	A python implementation of the mini language, with user-defined
#	functions
#
# Ryan Daugherty
# Tom Houman
# Joe Muoio
#
# Modified from code provided by Kurt Schmidt

import sys
#import list_implementation
from structures import *
from  list_structures import *
#import list_functions
#from list_functions import *

######   LEXER   ###############################

from ply import lex

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
	'IDENT',
	'CONS',
	'CDR',
	'CAR',
	'NULLP',
	'INTP',
	'LISTP'
)

	# These are all caught in the IDENT rule, typed there.
reserved = {
		'while' : 'WHILE',
		'do'		: 'DO',
		'od'		: 'OD',
		'if'		: 'IF',
		'then'	: 'THEN',
		'else'	: 'ELSE',
		'fi'		: 'FI',
		'car' : 'CAR',
		'cdr' : 'CDR',
		'nullp' : 'NULLP',
		'cons' : 'CONS',
		'intp' : 'INTP',
		'listp': 'LISTP'
		}

# Now, this section.  We have a mapping, REs to token types (please note
# the t_ prefix).  They simply return the type.

	# t_ignore is special, and does just what it says.  Spaces and tabs
t_ignore = ' \t'

	# These are the simple maps
t_PLUS		= r'\+'
t_MINUS   = r'-'
t_TIMES		= r'\*'
t_LPAREN	= r'\('
t_RPAREN	= r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_CONCAT = r'\|\|'
t_ASSIGNOP = r':='
t_SEMICOLON = r';'
t_COMMA		= r','

def t_IDENT( t ):
	#r'[a-zA-Z_][a-zA-Z_0-9]*'
	r'[a-z]+'
	t.type = reserved.get( t.value, 'IDENT' )    # Check for reserved words
	return t

def t_NUMBER( t ) :
	r'[0-9]+'

		# t.value holds the string that matched.  Dynamic typing - no unions
	t.value = int( t.value )
	return t

	# These are standard little ditties:
def t_newline( t ):
  r'\n+'
  t.lexer.lineno += len( t.value )

  # Error handling rule
def t_error( t ):
  print "Illegal character '%s' on line %d" % ( t.value[0], t.lexer.lineno )
  return t
  #t.lexer.skip( 1 )

lex.lex()

#-----   LEXER (end)   -------------------------------


######   YACC   #####################################

import ply.yacc as yacc

	# create a function for each production (note the prefix)
	# The rule is given in the doc string

def p_program( p ) :
	'program : stmt_list'
	P = Program( p[1] )
	#P.display()
	print 'Running Program'
	P.eval()
	P.dump()
	print P.translate()

def p_stmt_list( p ) :
	'''stmt_list : stmt SEMICOLON stmt_list
       | stmt'''
	
	if len( p ) == 2 :  # single stmt => new list
		p[0] = StmtList()
		p[0].insert( p[1] )
	else :  # we have a stmtList, keep adding to front
		p[3].insert( p[1] )
		p[0] = p[3]

def p_stmt( p ) :
	'''stmt : assign_stmt
				| while_stmt
				| if_stmt'''
	p[0] = p[1]

def p_add( p ) :
	'expr : expr PLUS term'
	p[0] = Plus( p[1], p[3] )

def p_sub( p ) :
	'expr : expr MINUS term'
	p[0] = Minus( p[1], p[3] )

def p_expr_list( p ) :
  '''expr_list : expr COMMA expr_list
              | expr'''
  if len( p ) == 2 :  # single expr => new list
    p[0] = [ p[1] ]
  else :  # we have a expr_list, keep adding to front
    p[3].insert( 0, p[1] )
    p[0] = p[3]

def p_expr_term( p ) :
	'expr : term'
	p[0] = p[1]

def p_mult( p ) :
	'''term : term TIMES fact'''
	p[0] = Times( p[1], p[3] )

def p_term_fact( p ) :
	'term : fact'
	p[0] = p[1]

def p_fact_expr( p ) :
	'fact : LPAREN expr RPAREN'
	p[0] = p[2]

def p_fact_NUM( p ) :
	'fact : NUMBER'
	p[0] = Number( p[1] )

def p_fact_IDENT( p ) :
	'fact : d_ident'
	p[0] = p[1]

def p_fact_funcall( p ) :
	'fact : func_call'
	p[0] = p[1]

def p_assn( p ) :
	'assign_stmt : IDENT ASSIGNOP expr'
	p[0] = AssignStmt( p[1], p[3] )

def p_while( p ) :
	'while_stmt : WHILE expr DO stmt_list OD'
	p[0] = WhileStmt( p[2], p[4] )

def p_if( p ) :
	'if_stmt : IF expr THEN stmt_list ELSE stmt_list FI'
	p[0] = IfStmt( p[2], p[4], p[6] )

def p_func_call( p ) :
  'func_call : IDENT LPAREN expr_list RPAREN'
  p[0] = FunCall( p[1], p[3] )

# Error rule for syntax errors
def p_error( p ):
	print "Syntax error in input!", str( p )
	sys.exit( 2 )
	
########################### was in list implementation #############################3
def p_def_ident( p ):
	'd_ident : IDENT'
	p[0]=Ident(p[1])
def p_concat( p ) :
	'expr : expr CONCAT list'
	p[0] = Concat( p[1], p[3] )
	
def p_concat_id( p ) :
	'expr : expr CONCAT d_ident'
	p[0] = Concat( p[1], p[3] )

def p_list( p ) :
	'list : LSQUARE sequence RSQUARE'
	p[0] = List(p[2])
	#print "to [seq]",p[0]

def p_empty_list( p ) :
	'list : LSQUARE RSQUARE'
	p[0] = List([])
	#print "to empty", p[0]

def p_sequence( p ):
	'sequence : list_element COMMA sequence'
	p[0] = [p[1]] + p[3]
	#print "to list , seq", p[0]

def p_sequence_list_element( p ):
	'sequence : list_element'
	p[0] = [p[1]]
	#print "tolistElem", p[0]

def p_list_element_element( p ):
	'list_element : expr'
	p[0] = p[1]
	#print "toexpr", p[0]
'''
def p_element_list( p ):
	'list_element : list'
	p[0] = p[1]
	#print " tolist", p[0]
	'''
def p_expr_to_list( p ):
	'expr : list'
	p[0] = p[1]

def p_func_call_cons( p ):
	'func_call : CONS LPAREN expr COMMA expr RPAREN'
	p[0] = Cons(p[3],p[5])

def p_func_call_car( p ):
	'func_call : CAR LPAREN expr RPAREN'
	p[0] = Car(p[3])

def p_func_call_cdr( p ):
	'func_call : CDR LPAREN expr RPAREN'
	p[0] = Cdr(p[3])

def p_func_call_nullp( p ):
	'func_call : NULLP LPAREN expr RPAREN'
	p[0] = Nullp(p[3])

def p_func_call_intp( p ):
	'func_call : INTP LPAREN expr RPAREN'
	p[0] = Nullp(p[3])

def p_func_call_listp( p ):
	'func_call : LISTP LPAREN expr RPAREN' # was list_elem
	p[0] = Listp(p[3])

 ##############################################

	# now, build the parser
yacc.yacc()


######   MAIN   #################################

def test_scanner( arg=sys.argv ) :

	data = ' 1+2 1-2 3*4 x blah y := 5 '

	lex.input( data )

	# attempt to get that first token
	tok = lex.token()
	while tok :
		print tok
		tok = lex.token()

def test_parser( arg=sys.argv ) :

	print "Please enter the program,  terminate with CTRL+D on a new line"

	data = ""
	
	data += sys.stdin.read()

	yacc.parse( data )


if __name__ == '__main__' :
	test_parser()

