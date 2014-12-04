% predict and compute errors using decision stump
%   alpha: alpha value associated witht the learner
%   stp: decision stump
%   i: number of weak hypotheses
%   X: data matrix
%   y: labels

function [err] = boostPred(alpha,weakLearners,i,X,y, weight)
    % number of examples
    N = size(X,1);
    % N by i matrix to store predictions
    m = zeros(N,i);
    % each column corresponds to predictions 
    % using k rounds
    for k = 1:i
        m(:,k) = alpha(k).*weakLearners{k}.predict(X);
    end
    % compute current hypothesis
    m = sum(m,2);
    % label +1/-1 based on sign
    label = sign(m);
    % compute error
    err_label = logical(label ~= y);
    err = sum(err_label)./N;
end

