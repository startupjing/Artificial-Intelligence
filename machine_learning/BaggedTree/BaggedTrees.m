function [ oobErr] = BaggedTrees( X, Y, numBags)
% Discussed BaggedTrees with Tong Mu
% BAGGEDTREES Returns out-of-bag classification error of an ensemble of
% numBags CART decision trees on the input dataset, and also plots the error
% as a function of the number of bags from 1 to numBags
%   Inputs:
%       X : Matrix of training data
%       Y : Vector of classes of the training examples
%       numBags : Number of trees to learn in the ensemble
%   You may use "fitctree" but do not use "TreeBagger" or any other inbuilt
%   bagging function

% number of examples
numExp = length(Y);
% generate random bags
r = rand(numExp,numBags);
bags = ceil(r*numExp);
% vote counter for each sample
voteNum = zeros(numExp,1);
% number of correct prediction for each sample
corrPred = zeros(numExp,1);
% oob error history for each bag size
errHist = zeros(1,numBags);


for i = 1:numBags
    % limit bag size to i
    currBag = bags(:,i);
    % flag uncovered examples as true
    % and set in-bag examples to false
    allExp = true(numExp,1);
    allExp(currBag) = false;
    % find index of out-of-bag examples
    allIdx = 1:numExp;
    uncoveredIdx = allIdx(allExp); 
    % increment vote counters for current uncovered examples
    voteNum(uncoveredIdx) = voteNum(uncoveredIdx) + 1;
    halfVote = voteNum/2;
    % select samples from data matrix
    currX = X(currBag,:);
    currY = Y(currBag);
    % learn a decision tree
    tree = fitctree(currX, currY);
    % get uncovered examples and their labels
    uncoveredX = X(uncoveredIdx,:);
    uncoveredY = Y(uncoveredIdx);
    % make predictions on uncovered examples
    preds = predict(tree,uncoveredX);
    % compute number of correct predictions
    countCorrectPred = (preds == uncoveredY);
    corrPred(uncoveredIdx) = corrPred(uncoveredIdx) + countCorrectPred;
    % count missiclassification
    miss = sum(corrPred <= halfVote);
    % compute oob error for current bag size
    errHist(i) = miss./numExp;
  end
  
  oobErr = errHist(numBags);
  
  % plot OOB error vs. numBag
  figure
  plot(errHist);
  title('OOB error for different numBag');
  xlabel('Number of bags');
  ylabel('OOB error');
    

end

