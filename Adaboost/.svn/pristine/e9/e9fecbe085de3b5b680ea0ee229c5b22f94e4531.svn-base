% compute entropy of binary variable
%  p: probability of variable=+1

function [val] = computeB(q)
   if q>0 && q<1
       p = 1-q;
       val = q.*log2(q) + p.*log2(p);
       val = -val;
   else
       val = 0;
end

