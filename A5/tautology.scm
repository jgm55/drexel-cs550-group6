;;;;boolean constants are predeclared

;;;;may need to do variables
;;;(load "C:\\Users\\Joe Muoio\\Documents\\GitHub\\drexel-cs550-group6\\A5\\tautology.scm")

; Tautology example: ()

(define (tautology-prover expression env)
	(get-permutations expression (dedupe (find-vars expression)) env))
	
	
(define (get-permutations expression vars env)
	(display vars)
	(cond((null? vars) (eval expression env))
		(else ;;
			(eval (list 'define (car vars) '#t)env)
			(and 	
				(get-permutations expression(cdr vars) env)
				(eq?(eval (list 'set! (car vars) '#f)env)'ok)
				(get-permutations expression(cdr vars) env))
			)))
				

;; finds all the variables in hte expresion
(define (find-vars expression)
	(if (null? expression)
		'()
		(if (reserved-word?(car expression))
			(find-vars (cdr expression))
			(if (list? (car expression))
				(append (find-vars (car expression)) (find-vars (cdr expression)))
				(cons (car expression) (find-vars (cdr expression)))))))
			
(define (reserved-word? word) 
	(cond ((eq? word 'and) '#t)
		((eq? word 'or) '#t)
		((eq? word 'implies) '#t)
		((eq? word 'equiv) '#t)
		((eq? word 'not) '#t)
		(else '#f)))

(define (not exp env)
	(false? (eval(cadr exp) env)))

(define (implies exp env)
	(let ((exp1 (cadr exp))
		(exp2 (caddr exp)))
		(if (true? (eval exp1 env))
			(true? (eval exp2 env))
			'#t)))
			
		
(define (equiv exp env)
	(let ((exp1 (cadr exp))
		(exp2 (caddr exp)))
		(and (eval (list 'implies exp1 exp2 ) env) 
			(eval (list 'implies exp2 exp1) env))))

(define (and->split exp env)
  (and-clauses (get-clauses exp) env))
  
(define (and-clauses clauses env)
  (if (null? clauses)
      '#f                          ; no clauses
      (let ((first (eval (car clauses) env))
            (rest (cdr clauses)))
            (if (null? rest)
                first
				(and first (and-clauses rest env))))))

(define (or->split exp env)
  (or-clauses (get-clauses exp) env))  
		
(define (or-clauses clauses env)
  (if (null? clauses)
      '#f                          ; no clauses
      (let ((first (eval (car clauses) env))
            (rest (cdr clauses)))
            (if (null? rest)
                first
				(or first (or-clauses rest env))))))	

(define (get-clauses exp) (cdr exp))

;;;;    Everything below here is SICP Code or based on it (eg eval)   ;;;;				
				
(define apply-in-underlying-scheme apply)

(define (eval exp env)
  (cond ((self-evaluating? exp) exp)
		((variable? exp) (eval(lookup-variable-value exp env) env))
		((assignment? exp) (eval-assignment exp env))
		((definition? exp) (eval-definition exp env))
        ((not? exp) (eval(not exp env) env))
		((implies? exp) (eval (implies exp env) env))
		((equiv? exp) (eval (equiv exp env) env))
		((and? exp) (eval (and->split exp env) env))
		((or? exp) (eval (or->split exp env) env))

        (else
         (error "Unknown expression type -- EVAL" exp))))

(define (apply procedure arguments)
  (cond ((primitive-procedure? procedure)
         (apply-primitive-procedure procedure arguments))
        ((compound-procedure? procedure)
         (eval-sequence
           (procedure-body procedure)
           (extend-environment
             (procedure-parameters procedure)
             arguments
             (procedure-environment procedure))))
        (else
         (error
          "Unknown procedure type -- APPLY" procedure))))

(define (self-evaluating? exp)
  (cond ((boolean? exp) true)
        (else false)))
(define (variable? exp)(symbol? exp))

(define (assignment? exp)
  (tagged-list? exp 'set!))
	  
(define (not? exp) (tagged-list? exp 'not))

(define (implies? exp) (tagged-list? exp 'implies))

(define (equiv? exp) (tagged-list? exp 'equiv))

(define (and? exp) (tagged-list? exp 'and))

(define (or? exp) (tagged-list? exp 'or))

(define (definition? exp)
  (tagged-list? exp 'define))

(define (tagged-list? exp tag)
  (if (pair? exp)
      (eq? (car exp) tag)
      false))		  
		  
		  
(define (true? x)
  (eq? x true))

(define (false? x)
  (eq? x false))

(define (lookup-variable-value var env)
  (define (env-loop env)
    (define (scan vars vals)
      (cond ((null? vars)
             (env-loop (enclosing-environment env)))
            ((eq? var (car vars))
             (car vals))
            (else (scan (cdr vars) (cdr vals)))))
    (if (eq? env the-empty-environment)
        (error "Unbound variable" var)
        (let ((frame (first-frame env)))
          (scan (frame-variables frame)
                (frame-values frame)))))
  (env-loop env))

(define (make-procedure parameters body env)
  (list 'procedure parameters body env))

(define (compound-procedure? p)
  (tagged-list? p 'procedure))


(define (procedure-parameters p) (cadr p))
(define (procedure-body p) (caddr p))
(define (procedure-environment p) (cadddr p))


(define (enclosing-environment env) (cdr env))

(define (first-frame env) (car env))

;;;;;;;;;;;;;; Taken from stack overflow ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define (dedupe e)
  (if (null? e) '()
      (cons (car e) (dedupe (filter (lambda (x) (false? (equal? x (car e)))) 
                                    (cdr e))))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define the-empty-environment '())

(define (make-frame variables values)
  (cons variables values))

(define (frame-variables frame) (car frame))
(define (frame-values frame) (cdr frame))

(define (add-binding-to-frame! var val frame)
  (set-car! frame (cons var (car frame)))
  (set-cdr! frame (cons val (cdr frame))))

(define (extend-environment vars vals base-env)
  (if (= (length vars) (length vals))
      (cons (make-frame vars vals) base-env)
      (if (< (length vars) (length vals))
          (error "Too many arguments supplied" vars vals)
          (error "Too few arguments supplied" vars vals))))

		  
		  
(define (eval-definition exp env)
  (define-variable! (definition-variable exp)
                    (eval (definition-value exp) env)
                    env)
  'ok)
(define (definition-variable exp)
  (if (symbol? (cadr exp))
      (cadr exp)
      (caadr exp)))
	  
(define (definition-value exp)(display (caddr exp))
  (if (symbol? (cadr exp))
      (caddr exp)
      (make-lambda (cdadr exp)
                   (cddr exp))))
;;;;;;;;;;;;;;;;;;;;

(define (define-variable! var val env)
  (let ((frame (first-frame env)))
    (define (scan vars vals)
      (cond ((null? vars)
             (add-binding-to-frame! var val frame))
            ((eq? var (car vars))
             (set-car! vals val))
            (else (scan (cdr vars) (cdr vals)))))
    (scan (frame-variables frame)
          (frame-values frame))))

(define (eval-assignment exp env)
  (set-variable-value! (assignment-variable exp)
                       (eval (assignment-value exp) env)
                       env)
  'ok)

(define (set-variable-value! var val env)
  (define (env-loop env)
    (define (scan vars vals)
      (cond ((null? vars)
             (env-loop (enclosing-environment env)))
            ((eq? var (car vars))
             (set-car! vals val))
            (else (scan (cdr vars) (cdr vals)))))
    (if (eq? env the-empty-environment)
        (error "Unbound variable -- SET!" var)
        (let ((frame (first-frame env)))
          (scan (frame-variables frame)
                (frame-values frame)))))
  (env-loop env))
 
(define (assignment-variable exp) (cadr exp))

(define (assignment-value exp) (caddr exp))

;;;;;;;;;

(define (setup-environment)
  (let ((initial-env
         (extend-environment (primitive-procedure-names)
                             (primitive-procedure-objects)
                             the-empty-environment)))
    (define-variable! 'true true initial-env)
    (define-variable! 'false false initial-env)
    initial-env))

(define (primitive-procedure? proc)
  (tagged-list? proc 'primitive))

(define (primitive-implementation proc) (cadr proc))

(define primitive-procedures
  (list (list 'null? null?)
        ))

(define (primitive-procedure-names)
  (map car
       primitive-procedures))

(define (primitive-procedure-objects)
  (map (lambda (proc) (list 'primitive (cadr proc)))
       primitive-procedures))

(define (apply-primitive-procedure proc args)
  (apply-in-underlying-scheme
   (primitive-implementation proc) args))


(define input-prompt ";;; Tautology input:")
(define output-prompt ";;; Tautology output:")

(define (driver-loop)
  (prompt-for-input input-prompt)
  (let ((input (read)))
    (let ((output (tautology-prover input the-global-environment)))
      (announce-output output-prompt)
      (user-print output)))
  (driver-loop))

(define (prompt-for-input string)
  (newline) (newline) (display string) (newline))

(define (announce-output string)
  (newline) (display string) (newline))

(define (user-print object)
  (if (compound-procedure? object)
      (display (list 'compound-procedure
                     (procedure-parameters object)
                     (procedure-body object)
                     '<procedure-env>))
      (display object)))

	  
(define the-global-environment (setup-environment))
(driver-loop)


'METACIRCULAR-EVALUATOR-LOADED




