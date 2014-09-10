function [iter] = iterationFactor()
w_star = [0; 1; -1];

% % factor one: size of training set
% iter = zeros(1,100);
% col = 1;
% for i=10:10:1000
%     x = -1 + 2.*rand(3,i);
%     y = sign(transpose(w_star)*x);
%     iter(1,col) = pla(x,y,w_star);
%     col = col + 1;
% end
% 
% size = [10:10:1000];
% scatter(size,iter,'blue','fill');
% xlabel('sample size');
% ylabel('#iterations');
% title('Factor1-Sample Size');





% 
% factor two: classification distribution
iter = zeros(1,3);

x1 = -1 + 2.*rand(3,100);
y1 = sign(transpose(w_star)*x1);
x1plus = find(y1(:)>0);
x1minus = find(y1(:)<0);
iter(1,1) = pla(x1,y1,w_star);

x2 = zeros(3,100);
x2(2,:) = 4.*rand(1,100);
x2(3,:) = 2.*rand(1,100);
y2 = sign(transpose(w_star)*x2);
x2plus = find(y2(:)>0);
x2minus = find(y2(:)<0);
iter(1,2) = pla(x2,y2,w_star);

x3 = zeros(3,100);
x3(2,:) = 6.*rand(1,100);
x3(3,:) = 2.*rand(1,100);
y3 = sign(transpose(w_star)*x3);
x3plus = find(y3(:)>0);
x3minus = find(y3(:)<0);
iter(1,3) = pla(x3,y3,w_star);

% trial = 1:3;
% bar(trial,iter);
% xlabel('trial');
% ylabel('#iterations');
% title('Factor2-Classification Distribution');
% 
% 
% figure
% scatter(x1(2,x1plus),x1(3,x1plus),'Marker','+');
% hold on;
% scatter(x1(2,x1minus),x1(3,x1minus),'Marker','o');
% 
% xlabel('x1');
% ylabel('x2');
% title('fair distribution');
% 
% figure
% scatter(x2(2,x2plus),x2(3,x2plus),'Marker','+');
% hold on;
% scatter(x2(2,x2minus),x2(3,x2minus),'Marker','o');
% xlabel('x1');
% ylabel('x2');
% title('more biased distribution');
% 
% figure
% scatter(x3(2,x3plus),x3(3,x3plus),'Marker','+');
% hold on;
% scatter(x3(2,x3minus),x3(3,x3minus),'Marker','o');
% xlabel('x1');
% ylabel('x2');
% title('most biased distribution');



end











