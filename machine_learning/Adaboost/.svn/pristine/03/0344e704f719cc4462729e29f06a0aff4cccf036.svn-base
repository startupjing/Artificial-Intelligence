function [splitVal, gain] = computeGain(x, y, weight)
% compute information gain
   N = length(x);
   gainHist = zeros(N,1);
   % compute entropy of parent
   p = sum(logical(y==1).*weight);
   temp = computeB(p);
   % try each feature value as split point
   for i = 1:N 
     idx_more = logical(x >= x(i));
     % compute entropy for left and right child
     num1 = sum(weight(idx_more));
     num2 = 1 - num1;
     p1 = sum(logical(y(idx_more) == 1).*weight(idx_more));
     p2 = sum(logical(y(~idx_more) == 1).*weight(~idx_more));
     entropy1 = computeB(p1./num1).*num1;
     entropy2 = computeB(p2./num2).*num2;
     % compute information gain
     gainHist(i) = temp - (entropy1 + entropy2);
   end
   % find max information gain and corresponding split point
   [gain,splitIdx] = max(gainHist);
   splitVal = x(splitIdx);
end

