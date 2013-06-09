% CS550 Group 6
% Tom Houman (A7 Leader)
% Ryan Daugherty
% Joe Muoio
% CS550 Spring 2013
% Assignment 7
%
% q3.pl
% Assignment 7, question 3
% SICP exercise 4.68
% Prolog implementation of the reverse of a list
% Note: This implementation uses an accumulating parameter

% Example usage:
% ['q3.pl'].
% reverse([1,2,3],[],A).
% Result: A = [3,2,1]

% Base case
reverse([],X,X).

% Here is where the magic happens
reverse([X|Y],Z,A) :- reverse(Y,[X|Z],A).

