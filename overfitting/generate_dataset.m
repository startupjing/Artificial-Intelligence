function [ train_set, test_set ] = generate_dataset( Q_f, N_train, N_test, sigma )
%GENERATE_DATASET Generate training and test sets for the Legendre
%polynomials example
%   Inputs:
%       Q_f: order of the hypothesis
%       N_train: number of training examples
%       N_test: number of test examples
%       sigma: standard deviation of the stochastic noise
%   Outputs:
%       train_set and test_set are both 2-column matrices in which each row
%       represents an (x,y) pair

% uniform distribution of x in [-1,1]
% get x-input for train and test set
train_x = rand(N_train,1).*2 - 1;
test_x = rand(N_test,1).*2 - 1;

% normalize factor
factor = 0;
for q = 0:Q_f
    factor = factor + 1./(2.*q+1);
end
factor = sqrt(factor);

% generate coefficients a_q by standard normal distribution
aq = normrnd(0,1,1,Q_f+1);
train_aq = repmat(aq, N_train, 1);
test_aq = repmat(aq, N_test, 1);

% compute legendre polynomials
train_leg = computeLegPoly(train_x, Q_f);
test_leg = computeLegPoly(test_x, Q_f);

% linear combination to get f(x)
train_f = sum(train_leg.*train_aq,2);
test_f = sum(test_leg.*test_aq,2);

% normalize f
train_f = factor.*train_f;
test_f = factor.*test_f;

% generate noise using standard normal distribution
train_noise = sigma.*normrnd(0,1,N_train,1);
test_noise = sigma.*normrnd(0,1,N_test,1);

% compute output y
train_y = train_f + train_noise;
test_y = test_f + test_noise;

% build date set
train_set = [train_x train_y];
test_set = [test_x test_y];


end

