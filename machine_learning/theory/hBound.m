function [] = hBound(n)
results = coinSimulate(n);
c1 = results(:,1);
crand = results(:,2);
cmin = results(:,3);

binrange = 0:0.1:1;

c1_count = zeros(11,2);
crand_count = zeros(11,2);
cmin_count = zeros(11,2);

c1_count(:,1) = binrange;
crand_count(:,1) = binrange;
cmin_count(:,1) = binrange;


c1_count(:,2) = histc(c1, binrange);
crand_count(:,2) = histc(crand, binrange);
cmin_count(:,2) = histc(cmin, binrange);

plotData = zeros(6,5);
row = 1;

for limit=0:0.1:0.5
    plotData(row,1) = limit;
    plotData(row,2) = 2.*exp(-20.*limit.*limit);
    
    indexc1 = find(abs(c1_count(:,1)-0.5)>limit);
    indexcrand = find(abs(crand_count(:,1)-0.5)>limit);
    indexcmin = find(abs(cmin_count(:,1)-0.5)>limit);
    
    plotData(row,3) = sum(c1_count(indexc1,2))./n;
    plotData(row,4) = sum(crand_count(indexc1,2))./n;
    plotData(row,5) = sum(cmin_count(indexc1,2))./n;
    row = row + 1;
end




limitVal = plotData(:,1);
bound = plotData(:,2);
probc1 = plotData(:,3);
probcrand = plotData(:,4);
probcmin = plotData(:,5);


figure
plot(limitVal, probc1, 'green');
hold on;
plot(limitVal, bound, 'red');
xlabel('epsilon');
ylabel('prob/bound');
title('first coin');

figure
plot(limitVal, probcrand, 'blue');
hold on;
plot(limitVal, bound, 'red');
xlabel('epsilon');
ylabel('prob/bound');
title('random coin');

figure
plot(limitVal, probcmin, 'black');
hold on;
plot(limitVal, bound, 'red');
xlabel('epsilon');
ylabel('prob/bound');
title('min coin');



    
    
    
    
    