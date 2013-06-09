% CS550 Group 6
% Tom Houman (A7 Leader)
% Ryan Daugherty
% Joe Muoio
% CS550 Spring 2013
% Assignment 7
%
% mini3.pl
% Assignment 7, question 5
% Mini language interpreter
% Modified from mini3.pl provided by J. Johnson

% The following prolog rules implement the reductions for the mini language in
% section 13.2 of Kenneth Louden, Programming Languages: Principles and Practice, 2nd Ed.
% Thomson Course Technology, 2003.
% Author:  Jeremy Johnson
% Date: 3/20/2007.
%
% Program syntax:  
%         config(E,Env) | config(P,Env)
%         E ::= plus(E1,E2) | minus(E1,E2) | times(E1,E2) | Ident | Number
%         P ::= S | seq(S,P)
%         S ::= assign(I,E) | if(E,P,P) | while(E,P)
%         Env ::= [] | [Binding | Env]
%         Binding ::= value(Ident,Number)
%
% Program semantics:  
%         The execution of a program results in an Environment.
%         The resulting environment is defined by the following reduction rules.
%
% Notes:  I have chosen to have a separate predicates, reduce_exp_all, and reduce_exp,
%         for expressions.  These take a configuration with an expression and reduce it 
%         to a value.
%         The reduce_all and reduce predicates take a configuration with a statement or 
%         statement sequence and reduce it to an environment.
%         To evaluate a program P, reduce_all(config(P),[]).
% 
% Test cases:
%         reduce_exp_all(config(plus(times(2,5),minus(2,5)),[]),V).
%             V = config(7,[])
%         reduce_exp_all(config(plus(times(x,5),minus(2,y)),[value(x,2),value(y,5)]),V).
%             V = config(7,[value(x,2),value(y,5)])
%         reduce_all(config(seq(assign(x,3),assign(y,4)),[]),Env).
%             Env = [value(x,3),value(y,4)]
%         reduce(config(if(3,assign(x,3),assign(x,4)),[]),Env).
%             Env = [value(x,3)]
%         reduce(config(if(0,assign(x,3),assign(x,4)),[]),Env).
%             Env = [value(x,4)]
%         reduce_all(config(if(n,assign(i,0),assign(i,1)),[value(n,3)]),Env).
%             Env = [value(n,3),value(i,0)]
%         reduce_all(config(while(x,assign(x,minus(x,1))),[value(x,3)]),Env).
%             Env = [value(x,0)]
%         reduce_all(config(
%                       seq(assign(n,minus(0,3)),
%                       seq(if(n,assign(i,n),assign(i,minus(0,n))),
%                       seq(assign(fact,1),
%                           while(i,seq(assign(fact,times(fact,i)),assign(i,minus(i,1)))))))
%                       ,[]),Env).
%             Env = [value(n,-3),value(i,0),value(fact,6)]

% Auxiliary predicates for environments.
lookup([value(I,V)|_],I,V).
lookup([_|Es],I,V) :- lookup(Es,I,V), !.

% add predicate update(Env,value(I,V),Env1) which is true when the binding
% value(I,V) added to the environment Env produces the updated environment
% Env2.
update([],value(I,V),[value(I,V)]).
update([value(I,_)|T],value(I,V),[Env|T]) :- update([],value(I,V),[Env]), !.
update([H|T],value(I,V),[H|Env]) :- update(T,value(I,V),Env).

% reduction rules for arithmetic expressions.

% rules (7) - (9), which reduce the first operand of an expression
reduce_exp(config(plus(E,E2),Env),config(plus(E1,E2),Env)) :- 
     reduce_exp(config(E,Env),config(E1,Env)).
reduce_exp(config(minus(E,E2),Env),config(minus(E1,E2),Env)) :- 
     reduce_exp(config(E,Env),config(E1,Env)).
reduce_exp(config(times(E,E2),Env),config(times(E1,E2),Env)) :- 
     reduce_exp(config(E,Env),config(E1,Env)).

% rules (10) - (12), which reduce the second operand of an expression
reduce_exp(config(plus(V,E),Env),config(plus(V,E1),Env)) :- 
     reduce_exp(config(E,Env),config(E1,Env)).
reduce_exp(config(minus(V,E),Env),config(minus(V,E1),Env)) :- 
     reduce_exp(config(E,Env),config(E1,Env)).
reduce_exp(config(times(V,E),Env),config(times(V,E1),Env)) :- 
     reduce_exp(config(E,Env),config(E1,Env)).

% rules (3) - (5), which reduce an expression involving integers
reduce_exp(config(plus(V1,V2),Env),config(R,Env)) :- integer(V1), integer(V2), !, R is V1+V2.
reduce_exp(config(minus(V1,V2),Env),config(R,Env)) :- integer(V1), integer(V2), !, R is V1-V2.
reduce_exp(config(times(V1,V2),Env),config(R,Env)) :- integer(V1), integer(V2), !, R is V1*V2.

% rule (15), which reduces an identifier to its value.
reduce_exp(config(I,Env),config(V,Env)) :- atom(I), !, lookup(Env,I,V).

% rule (14), which applies transitive reductions.
reduce_exp_all(config(V,Env),config(V,Env)) :- integer(V), !.
reduce_exp_all(config(E,Env),config(E2,Env)) :- 
     reduce_exp(config(E,Env),config(E1,Env)), reduce_exp_all(config(E1,Env),config(E2,Env)).
reduce_value(config(E,Env),V) :- reduce_exp_all(config(E,Env),config(V,Env)).

% reduction rules for statement sequence
% rules (18) and (14) to allow transitive reductions.
reduce_all(config(seq(S,R),Env),Env1) :-
     reduce(config(S,Env),EnvA), reduce_all(config(R,EnvA),Env1), !.
reduce_all(config(S,Env1),Env2) :- reduce(config(S,Env1),Env2), !.

% rules (16) - (17) combined for assignment statements
reduce(config(assign(I,E),Env),Env1) :-
     reduce_exp_all(config(E,Env),config(V,Env)), update(Env,value(I,V),Env1).

% rules (20) - (22) for if statements
reduce(config(if(V,T,_),Env),Env1) :- integer(V), V > 0, reduce(config(T,Env),Env1).
reduce(config(if(V,_,F),Env),Env1) :- integer(V), V =< 0, reduce(config(F,Env),Env1).
reduce(config(if(E,T,F),Env),Env1) :-
     reduce_exp_all(config(E,Env),config(E1,Env)), reduce(config(if(E1,T,F),Env),Env1).

%% rules (23) - (24) for while statements
reduce(config(while(E,_),Env),Env) :-
     reduce_exp_all(config(E,Env),config(V,Env)), integer(V), V =< 0.
reduce(config(while(E,L),Env),Env1) :-
     reduce_exp_all(config(E,Env),config(V,Env)), integer(V), V > 0,
     reduce_all(config(L,Env),EnvA), reduce(config(while(E,L),EnvA),Env1).

