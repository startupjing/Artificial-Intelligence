% decision stump class

classdef decisionStump  
    properties
        threshold;   % threshold to split on feature
        error;       % classification error
        pred_less;   % predictions <
        pred_more;   % predictions >=
        dim;         % dimension
        gain;    % information gain
    end
    
    methods
        % constructor        
        function stp = decisionStump(x,y,d,weight,gain,threshold)
            stp.threshold = threshold;
            stp.gain = gain;
            stp.dim = d;
            % assign labels based on weighted sum
            idx_more = logical(x >= threshold);
            idx1 = logical(y(idx_more) == 1);
            sum1 = sum(weight(idx1));
            sum2 = sum(weight(idx_more)) - sum1;
            stp.pred_more = sign(sum1 - sum2);
            stp.pred_less = -stp.pred_more;
        end
        
        % use stp to predict on X
        function label = predict(stp,X)
            % number of examples
            N = size(X,1);
            % column vector of corresponding feature
            dim_x = X(:, stp.dim);
            idx = logical(dim_x >= stp.threshold);
            label = zeros(N,1);
            % assign corresponding labels
            label(idx) = stp.pred_more;
            label(~idx) = stp.pred_less;
        end    
    end
    
end

