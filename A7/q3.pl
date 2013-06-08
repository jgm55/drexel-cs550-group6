% SICP exercise 4.68
% Prolog implementation of the reverse of a list

% Note: This implementation uses an accumulating parameter

% Base case
reverse([],X,X).

% Here is where the magic happens
reverse([X|Y],Z,A) :- reverse(Y,[X|Z],A).

% Example usage:
% ['q3.pl']
% reverse([1,2,3],[],A).
% Result: A = [3,2,1]
