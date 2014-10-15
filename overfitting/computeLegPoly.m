function [ z ] = computeLegPoly( x, Q )
%COMPUTELEGPOLY Return the Qth order Legendre polynomial of x
%   Inputs:
%       x: vector (or scalar) of reals in [-1, 1]
%       Q: order of the Legendre polynomial to compute
%   Output:
%       z: matrix where each column is the Legendre polynomials of order 0 
%          to Q, evaluated at the corresponding x value in the input


% initialize output matrix
% assuming given x is column vector
row = size(x,1);
col = Q + 1;
z = zeros(row,col);

% simple case
if Q == 0
    z = ones(row,1);
elseif Q == 1
    z = [ones(row,1) x];
else
    % base case
    z(:,1) = ones(row,1);
    z(:,2) = x;
    
    % computer higher order of polynomial using previous two terms
    for i = 3:Q+1
        z(:,i) = (2-1./(i-1)).*(z(:,2).*z(:,i-1)) - (1-1./(i-1)).*z(:,i-2);
    end

end

