#!/usr/bin/python
#
# Parts of the implementation relevant to list processing
#
# Ryan Daugherty
# Tom Houman
# Joe Muoio

######   LEXER	    ###############################
import sys

import ply.yacc as yacc
from ply import lex

tokens = (
	'COMMA',
	'LSQUARE',
	'RSQUARE',
	'NUMBER',
)

t_ignore = ' \t'

	# These are the simple maps

t_COMMA     = r','
t_LSQUARE	= r'\['
t_RSQUARE	= r'\]'


def t_NUMBER( t ) :
	r'[0-9]+'

		# t.value holds the string that matched.  Dynamic typing - no unions
	t.value = int( t.value )
	return t

def t_newline( t ):
	r'\n+'
	t.lexer.lineno += len( t.value )
	
# Error handling rule
def t_error( t ):
	print "Illegal character '%s' on line %d" % ( t.value[0], t.lexer.lineno )
	return t
	#t.lexer.skip( 1 )

  # Here is where we build the lexer, after defining it (above)
lex.lex()

######   LEXER (end)   ###############################


######   YACC   #####################################

import ply.yacc as yacc

def p_list( p ) :
	'list : LSQUARE sequence RSQUARE'
	p[0] = p[2]
	#print "to [seq]",p[0]
def p_empty_list( p ) :
	'list : LSQUARE RSQUARE'
	p[0] = []	
	#print "to empty", p[0]
def p_sequence( p ):
	'sequence : list_element COMMA sequence'
	p[0] = [p[1]] + p[3]
	#print "to list , seq", p[0]
def p_sequence_list_element( p ):
	'sequence : list_element'
	p[0] = [p[1]]
	#print "tolistElem", p[0]
'''
def p_list_element( p ):
	'list_element : list'
	p[0] = p[1]'''

def p_list_element_expr( p ):
	'list_element : expr'
	#???
	p[0] = p[1]
	#print "toexpr", p[0]
def p_expr_number( p ):
	'expr : NUMBER'
	p[0] = p[1]
	#print "tonumber", p[0]
def p_expr_list( p ):
	'expr : list'
	p[0] = p[1]
	#print " tolist", p[0]
yacc.yacc()

if __name__ == '__main__' :

	userIn = sys.stdin.readlines()
		
	input = ''.join( ''.join(userIn).split());
	
	result = yacc.parse( input )
	print result
	
	print ""

	
	
	