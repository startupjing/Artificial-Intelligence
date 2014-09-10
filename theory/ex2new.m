function [] = ex2new(expNum,dim,times)
    
results = zeros(times,3);

for i=1:times
    results(i,1) = i;
    w_star = rand(dim,1);
    w_star(1,1) = 0;
    
    x = -1 + 2.*rand(dim,expNum);
    y = sign(transpose(w_star)*x);
    
    results(i,2) = pla(x,y,w_star);
    
    x_norm = zeros(1,expNum);
    
    for j=1:expNum
        x_norm(1,j) = norm(x(:,j));
    end
    
    r = max(x_norm).^2;
    
    p = (min(y.*(transpose(w_star)*x))).^2;
    
    w_norm = (norm(w_star)).^2;
    
    results(i,3) = (r.*w_norm)./p;
    
end


figure
scatter(results(:,2),results(:,3),'blue');
xlabel('actual #iterations');
ylabel('error bound');
title('actual iterations vs. error bound');

figure
scatter(log(results(:,2)),log(results(:,3)),'blue');
xlabel('log(actual #iterations)');
ylabel('log(error bound)');
title('log(actual iterations) vs. log(error bound)');

figure
scatter(results(:,2),results(:,3)-results(:,2),'blue');
xlabel('actual #iterations');
ylabel('difference(actual #iterations - error bound)');
title('distribution of difference');

figure
scatter(results(:,2),log(results(:,3)-results(:,2)),'blue');
xlabel('actual #iteraions');
ylabel('log-difference(log(actual #iterations - error bound))');
title('distribution of log(difference)');


% 
% figure
% scatter(results(:,1),log(results(:,3)),'blue');
% xlabel('trial');
% ylabel('log(value of bound)');
% title('distribution of bound across trials');

% figure
% hist(results(:,2));
% xlabel('#iterations');
% ylabel('#occurence');
% title('iteraions experiement');
% 
% 
% figure
% hist(results(:,3));
% xlabel('#error');
% ylabel('#occurence');
% title('error bound');



% figure;
% trial = results(:,1);
% scatter(trial,results(:,2),'blue','fill');
% xlabel('trial');
% ylabel('iterations');
% title('number of iterations');

% figure;
% trial = results(:,1);
% scatter(trial,results(:,3),'green','fill');
% xlabel('trial');
% ylabel('error bound');
% title('number of errors');


end

