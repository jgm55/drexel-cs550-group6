(define global-variable-list '())

(define (eval exp env)
  (set! global-variable-list env)
  (eval-list exp)
  global-variable-list)

(define (eval-list exp)
  (eval-seq exp))

(define (eval-seq exp)
  (if (null? exp)
    '()
	(if (pair? (car exp))
	  (begin (eval-stmt (car exp))
	    (eval-seq (cdr exp)))
	  (eval-stmt exp))))

(define (eval-stmt exp)
  (cond ((assignment? exp) (eval-definition exp))
		((if? exp) (eval-if exp))
		((while? exp) (eval-while exp))
		(else
		 (eval-exp exp))))
		
(define (eval-exp exp)
  (cond ((self-evaluating? exp) exp)
        ((variable? exp) (lookup-variable-value exp))
		((add? exp) (add exp))
		((subtract? exp) (subtract exp))
		((multiply? exp) (multiply exp))
        (else
         (error "Unknown expression type -- EVAL" exp))))
 

 ;;;;variable
 (define (lookup-variable-value var)
  (define (inner-lookup var env)
    (if (null? env)
	  (error "Unbound variable" var)
	  (if (eq? var (caar env))
	    (cadar env)
	    (inner-lookup var (cdr env)))))
  (inner-lookup var global-variable-list))
 
 
;;;;assignment  
(define (eval-definition exp)
  (define-variable! (definition-variable exp)
                    (eval-exp (definition-value exp))))
(define (definition-variable exp) (cadr exp))
(define (definition-value exp) (caddr exp))
(define (define-variable! var val)
  (define (inner-define var examine-env)
    (if (null? examine-env)
	  (list (list var val))
	  (if (eq? var (caar examine-env))
		(cons (list var val) (cdr examine-env))
	    (cons (car examine-env) (inner-define var (cdr examine-env))))))
  (set! global-variable-list (inner-define var global-variable-list)))
 
			
;;;;if
(define (eval-if exp)
  (if (> (eval-exp (if-predicate exp)) 0)
      (eval-list (if-consequent exp))
      (eval-list (if-alternative exp)))
   'ok)
(define (if-predicate exp) (cadr exp))
(define (if-consequent exp) (caddr exp))
(define (if-alternative exp)
  (if (not (null? (cdddr exp)))
      (cadddr exp)
      '#f))
		
;;;;while
(define (eval-while exp)
  (if (> (eval-exp (while-predicate exp)) 0)
      (while-action exp)
      '()))
(define (while-action exp)
  (eval-list (while-contents exp))
  (eval-while exp))  
(define (while-predicate exp) (cadr exp))
(define (while-contents exp) (caddr exp))
		
;;;;arithmetic
(define (add exp)
	(+ (eval-exp (first-operand exp)) (eval-exp (second-operand exp))))
(define (subtract exp)
	(- (eval-exp (first-operand exp)) (eval-exp (second-operand exp))))
(define (multiply exp)
	(* (eval-exp (first-operand exp)) (eval-exp (second-operand exp))))
(define (first-operand exp) (cadr exp))
(define (second-operand exp) (caddr exp))		
		
;;;;statement type
(define (self-evaluating? exp)
  (cond ((number? exp) '#t)
        ((string? exp) '#t)
        (else '#f)))
(define (variable? exp) (symbol? exp))		
(define (assignment? exp)
  (tagged-list? exp 'assign))
(define (if? exp) (tagged-list? exp 'if))
(define (while? exp) (tagged-list? exp 'while))
(define (add? exp) (tagged-list? exp '+))
(define (subtract? exp) (tagged-list? exp '-))
(define (multiply? exp) (tagged-list? exp '*))
(define (tagged-list? exp tag)
  (if (pair? exp)
      (eq? (car exp) tag)
      '#f))
	  
;;;;utility
(define the-empty-environment '())
  
  