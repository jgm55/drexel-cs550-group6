; CS550 Group 6
; Tom Houman (A7 Leader)
; Ryan Daugherty
; Joe Muoio
; CS550 Spring 2013
; Assignment 7
;
; q4.scm
; Assignment 7, question 4
; SICP exercise 4.75
; Special form for query language: unique

;;; Load the support functions
(load "q4_support.scm")

;;; Initialize the database
(initialize-data-base microshaft-data-base)

;;; Start the query loop
(query-driver-loop)

;;; Test query
(and (supervisor ?employee ?super) (unique (supervisor ?someone ?super)))

;;; solution for Exercise 4.75 (also in q4_support.scm)
(define (uniquely-asserted operands frame-stream)
  (stream-flatmap
    (lambda (frame)
      (let ((stream (qeval (negated-query operands)
                           (singleton-stream frame))))
           (if (and (not (stream-null? stream))
                    (stream-null? (stream-cdr stream)))
               stream
               the-empty-stream)))
    frame-stream))

; Put to add the 4.75 solution (in initialize-data-base)
(put 'unique 'qeval uniquely-asserted) 
 
