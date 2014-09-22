function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta

temp1 = 0;
temp2 = 0;
n = size(X,2);

for i = 1:m
    h = sigmoid(X(i,:)*theta);
    temp1 = temp1 - y(i)*log(h)-(1-y(i))*log(1-h);
end

for i = 2:n
   temp2 = temp2 + theta(i)*theta(i);
end

J = temp1/m + lambda*temp2/(2*m);

temp3 = 0;
for i = 1:m
    h = sigmoid(X(i,:)*theta);
    temp3 = temp3 + h - y(i);
end
grad(1) = temp3/m;

for i = 2:n
    temp4 = 0;
    for j = 1:m
        h = sigmoid(X(j,:)*theta);
        temp4 = temp4 + (h-y(j))*X(j,i);
    end
    grad(i) = temp4/m + lambda*theta(i)/m;
end



% =============================================================

end
