% Script to compute test error for
% single decision tree and bagged ensemble of 200 trees
% in one-vs-five and three-vs-five digit problem

% load zip.test and zip.train
load zip.test;
ziptest = zip;
load zip.train;

fprintf('Working on the one-vs-five problem...\n\n');
% training set
subsample = zip(find(zip(:,1)==1 | zip(:,1) == 5),:);
Y = subsample(:,1);
X = subsample(:,2:257);
% test set
testsubsample = ziptest(find(ziptest(:,1)==1 | ziptest(:,1) == 5),:);
testY = testsubsample(:,1);
testX = testsubsample(:,2:257);

fprintf('Now working on part (c)\n');
% test error for a single decision tree
ct = fitctree(X,Y);
singlePred = predict(ct,testX);
singleErr = sum((singlePred==testY)<=0)./length(testY);
fprintf('The test error for a single decision tree is %.4f\n', singleErr);
% test error for an ensemble of 200 trees
numExp = length(Y);
bags = ceil(rand(numExp,1)*numExp);
currX = X(bags,:);
currY = Y(bags);
ct = fitctree(currX,currY);
ensemblePred = predict(ct,testX);
ensembleErr = sum((ensemblePred == testY)<=0)./length(testY);
fprintf('The test error for an ensemble of 200 trees is %.4f\n', ensembleErr);


fprintf('\nNow working on the three-vs-five problem...\n\n');
% training set
subsample = zip(find(zip(:,1)==3 | zip(:,1) == 5),:);
Y = subsample(:,1);
X = subsample(:,2:257);
% test set
testsubsample = ziptest(find(ziptest(:,1)==3 | ziptest(:,1) == 5),:);
testY = testsubsample(:,1);
testX = testsubsample(:,2:257);
fprintf('Now working on part (c)\n');
% test error for a single decision tree
ct = fitctree(X,Y);
singlePred = predict(ct,testX);
singleErr = sum((singlePred==testY)<=0)./length(testY);
fprintf('The test error for a single decision tree is %.4f\n', singleErr);
% test error for an ensemble of 200 trees
numExp = length(Y);
bags = ceil(rand(numExp,1)*numExp);
currX = X(bags,:);
currY = Y(bags);
ct = fitctree(currX,currY);
ensemblePred = predict(ct,testX);
ensembleErr = sum((ensemblePred == testY)<=0)./length(testY);
fprintf('The test error for an ensemble of 200 trees is %.4f\n', ensembleErr);
