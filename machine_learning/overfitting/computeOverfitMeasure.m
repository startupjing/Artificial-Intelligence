function [ overfit_m ] = computeOverfitMeasure( true_Q_f, N_train, N_test, var, num_expts )
%COMPUTEOVERFITMEASURE Compute how much worse H_10 is compared with H_2 in
%terms of test error. Negative number means it's better.
%   Inputs
%       true_Q_f: order of the true hypothesis
%       N_train: number of training examples
%       N_test: number of test examples
%       var: variance of the stochastic noise
%       num_expts: number of times to run the experiment
%   Output
%       overfit_m: vector of length num_expts, reporting each of the
%                  differences in error between H_10 and H_2

% initialize overfit_m
overfit_m = zeros(num_expts,1);

for i = 1:num_expts
    % generate data set
    [train_set, test_set] = generate_dataset(true_Q_f, N_train, N_test, sqrt(var));

    % extract x and y from data set
    train_x = train_set(:,1);
    test_x = test_set(:,1);
    train_y = train_set(:,2);
    test_y = test_set(:,2);

    % construct data matrix for H2
    train2_poly = computeLegPoly(train_x, 2);
    test2_poly = computeLegPoly(test_x, 2);


    % construct data matrix for H10
    train10_poly = computeLegPoly(train_x, 10);
    test10_poly = computeLegPoly(test_x, 10);


    % apply glmfit to traing example
    b2 = glmfit(train2_poly, train_y,'normal', 'constant','off');
    b10 = glmfit(train10_poly, train_y,'normal','constant','off');

    % compute E_out
    e2_out = sum((test2_poly*b2 - test_y).^2)./N_test;
    e10_out = sum((test10_poly*b10 - test_y).^2)./N_test;
    
    % compute overfit measure
    overfit_m(i,1) = e10_out - e2_out;
end

end

