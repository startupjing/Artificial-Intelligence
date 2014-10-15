%Script that runs the set of necessary experiments. This is an example that
%you can use; you should change it as appropriate to answer the question to
%your satisfaction.

Q_f = 5:5:20; % Degree of true function
N = 40:40:120; % Number of training examples
var = 0:0.5:2; % Variance of stochastic noise

expt_data_mat_median = zeros(length(Q_f),length(N), length(var));
expt_data_mat_mean = zeros(length(Q_f), length(N), length(var));

for i = 1:length(Q_f)
    for j = 1:length(N)
        for k = 1:length(var)
            temp = computeOverfitMeasure(Q_f(i),N(j),1000,var(k),500)';
            expt_data_mat_median(i,j,k) = median(temp);
            expt_data_mat_mean(i,j,k) = mean(temp);
        end
    end
    fprintf('.');
end

% make line plots using median measurement
for v=1:5
    data = expt_data_mat_median(:,:,v);
    N_40 = data(:,1);
    N_80 = data(:,2);
    N_120 = data(:,3);
    
    figure
    str = sprintf('Noise Leve %.1f', var(v));
    plot(Q_f,N_40,'-ro',Q_f,N_80,'-g^',Q_f,N_120,'-bx');
    title(str);
    xlabel('order q');
    ylabel('median');
    legend('N=40','N=80','N=120');
end

% make line plots using mean measurement
for v=1:5
    data = expt_data_mat_mean(:,:,v);
    N_40 = data(:,1);
    N_80 = data(:,2);
    N_120 = data(:,3);
    
    figure
    str = sprintf('Noise Leve %.1f', var(v));
    plot(Q_f,N_40,'-ro',Q_f,N_80,'-g^',Q_f,N_120,'-bx');
    title(str);
    xlabel('order q');
    ylabel('median');
    legend('N=40','N=80','N=120');
end
            