% train a decision stump using weight
%   X: data matrix
%   y: labels
%   weight: weight on each example

function [stp] = getStump(X,y,weight)
    % number of features
    dim = size(X,2);
    % information gain for each stump
    gain = zeros(dim,1);
    split = zeros(dim, 1);
    % compute each decision stump and corresponding gain
    for i = 1:dim
        [split(i), gain(i)] = computeGain(X(:,i), y, weight);
    end
    % find decision stump with maximum information gain
    [stpGain,idx] = max(gain);
    stpThreshold = split(idx);
    % construct decision stump
    stp = decisionStump(X(:,idx),y,idx, weight, stpGain, stpThreshold);  
    pred = stp.predict(X);
    % compute weighted error
    err_label = logical(pred ~= y);
    stp.error = sum(err_label.*weight)./sum(weight);
end

