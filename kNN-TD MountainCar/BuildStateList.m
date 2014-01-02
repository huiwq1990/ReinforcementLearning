function [ states ] = BuildStateList
%BuildStateList builds a state list from a state matrix

% state definition

x = linspace(-1.5,0.5,   21);
xp= linspace(-0.07,0.07, 21);

states = setprod(x,xp); %carestian product of dimension lists


