; CS550 Group 6
; Tom Houman (A7 Leader)
; Ryan Daugherty
; Joe Muoio
; CS550 Spring 2013
; Assignment 7
;
; q3.scm
; Assignment 7, question 3
; SICP exercise 4.68
; Simple Query Language implementation of the reverse of a list

;;; Load the support functions
(load "q3_support.scm")

;;; Initialize the database
(initialize-data-base microshaft-data-base)

;;; Start the query loop
(query-driver-loop)

;;; The rules (solution for Exercise 4.68)
;;; There are implemented in q3_support.scm
(rule (append-to-form () ?y ?y))
(rule (append-to-form (?u . ?v) ?y (?u . ?z))
      (append-to-form ?v ?y ?z))

(rule (reverse () ()))
(rule (reverse ?x ?y) 
      (and (append-to-form (?u) ?v ?x) 
           (append-to-form ?rv (?u) ?y) 
           (reverse ?v ?rv)))

))

;;; Reverse query that works
(reverse ?x (1 2 3))

;;; Reverse causing infinite loop
;;; Not sure how to remedy this situation
;;; The problem may be a limitation in the query language
(reverse (1 2 3) ?x)

