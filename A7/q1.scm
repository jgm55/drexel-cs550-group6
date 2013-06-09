; CS550 Group 6
; Tom Houman (A7 Leader)
; Ryan Daugherty
; Joe Muoio
; CS550 Spring 2013
; Assignment 7
;
; q1.scm
; Assignment 7, question 1


;;; Load the support functions
(load "q1_support.scm")

;;; Initialize the database
(initialize-data-base microshaft-data-base)

;;; Start the query loop
(query-driver-loop)

;;; The answers to SICP exercise 4.59 are below

;;; 4.59a
;;; Run this query to get all meetings on Friday
(meeting ?x (Friday ?y))

;;; 4.59b
;;; This rule defines the meeting times for a given person
(rule (meeting-time ?person ?day-and-time)
      (and (job ?person (?department . ?rest-1))
           (or (meeting ?department ?day-and-time)
               (meeting whole-company ?day-and-time))))

;;; 4.59c
;;; Run this query to get all meetings on Wednesday for A.P.Hacker
(meeting-time (Hacker Alyssa P) (Wednesday ?time))
