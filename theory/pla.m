function [itr] = pla(x, y, w_star)
   dim = size(x,1);
   w = zeros(dim,1);
   expNum = size(x,2);
   itr = 1;
   w = w + y(1)*x(:,1);
   guess = sign(transpose(w)*x);
   compare = guess.*y;

   while 1 
       guess = sign(transpose(w)*x);
       compare = guess.*y;
       if isequal(compare,ones(1,expNum))
           break
       end
       k = find(compare(1,:)<0,1);
       w = w + y(1,k).*x(:,k);
       itr = itr + 1;
   end
   
   
   

end

