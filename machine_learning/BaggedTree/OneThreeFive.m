% Script to load data from zip.train, filter it into datasets with only one
% and three or three and five, and compare the performance of plain
% decision trees (cross-validated) and bagged ensembles (OOB error)

load zip.train;
fprintf('Working on the one-vs-five problem...\n\n');
subsample = zip(find(zip(:,1)==1 | zip(:,1) == 5),:);
Y = subsample(:,1);
X = subsample(:,2:257);

ct = fitctree(X,Y,'CrossVal','on');
fprintf('The cross-validation error of decision trees is %.4f\n', ct.kfoldLoss);
bee = BaggedTrees(X, Y, 200);
fprintf('The OOB error of 200 bagged decision trees is %.4f\n', bee);


fprintf('\nNow working on the three-vs-five problem...\n\n');
subsample = zip(find(zip(:,1)==3 | zip(:,1) == 5),:);
Y = subsample(:,1);
X = subsample(:,2:257);

ct = fitctree(X,Y,'CrossVal','on');
fprintf('The cross-validation error of decision trees is %.4f\n', ct.kfoldLoss);
bee = BaggedTrees(X, Y, 200);
fprintf('The OOB error of 200 bagged decision trees is %.4f\n', bee);
