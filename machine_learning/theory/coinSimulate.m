function [results] = coinSimulate(n)
  results = zeros(n,3);
  for i=1:n
      coinArray = sum(randi([0 1],10,1000))./10;
      results(i,1) = coinArray(1,1);
      results(i,2) = coinArray(1,randi([1,1000]));
      results(i,3) = min(coinArray);
  end
  
%   figure
%   hist(results(:,1));
%   xlabel('fraction of heads');
%   ylabel('#occurence');
%   title('first coin');
%   
%   figure
%   hist(results(:,2));
%   xlabel('fraction of heads');
%   ylabel('#occurence');
%   title('random coin');
%   
%   figure
%   hist(results(:,3));
%   xlabel('fraction of heads');
%   ylabel('#occurence');
%   title('min coin');
  
end

