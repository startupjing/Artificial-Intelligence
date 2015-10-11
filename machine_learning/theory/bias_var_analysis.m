% bias-variance analysis using f(x)=sin(pi.*x) and linear hypothesis
function [biasOutput, varianceOutput, e_out] = functionTest(n)
   x = -1:0.01:1;
   d = size(x,2);
   % generate target function
   target = x.^2;
   
   % plot target function
   figure
   plot(x, target,'red');
   axis([-1 1 -0.5 1]);
   xlabel('x');
   ylabel('y');
   title('g(D) vs. f(x)');
   hold on;
   
   % every row of dataHist stores g(D) for a data set D
   dataHist = zeros(n,d);
   % repeat the experiment for n n(repeat using n random data sets)
   for i=1:n
      % generate two random points
      x1 = 2.*rand - 1;
      x2 = 2.*rand - 1;
      % create g(D) for this particular data set
      a = (sin(pi.*x2)-sin(pi.*x1))./(x2-x1);
      b = sin(pi.*x1) - a.*x1;
      y = a.*x + b;
      dataHist(i,:) = y;
      % plot g(D) for this particular data set
      plot(x,y,'blue');
      hold on;
   end
   
   % create g_bar(x)
   y_bar = mean(dataHist);
   
   % plot g_bar(x) vs. f(x)
   figure
   plot(x, target,'red');
   axis([-1 1 -0.5 1]);
   hold on;
   plot(x,y_bar,'yellow');
   xlabel('x');
   ylabel('y');
   title('g_bar vs. f(x)');
   
   % calculate var(x)
   variance = zeros(n,d);
   for j=1:n
       variance(j,:) = dataHist(j,:) - y_bar;
   end
   variance = mean(variance.^2);
   
   % calculate g_bar(x) +/- var(x)
   y_plus = y_bar + variance;
   y_minus = y_bar - variance;
   
   
   % plot g_bar(x) with f(x)
   % shaded region indicates g_bar(x) +/- var(x)
   figure
   axis([-1 1 -0.5 1]);
   plot(x, target,'red');
   hold on;
   plot(x,y_bar,'blue');
   hold on;
   X=[x,fliplr(x)];      
   Y=[y_minus,fliplr(y_plus)]; 
   fill(X,Y,'yellow');
   alpha(0.5);
   xlabel('x');
   ylabel('y');
   title('g_bar(x) vs. f(x) with variance');
   
   % calculate bias(x)
   bias = abs(y_bar - target);
   bias = bias.^2;
   
   % calculate Ex[bias(x)], Ex[var(x)] and E_out
   biasOutput = sum(bias)./d;
   varianceOutput = sum(variance)./d;
   e_out = biasOutput + varianceOutput;
   
   biasOutput
   varianceOutput
   e_out
      
end











