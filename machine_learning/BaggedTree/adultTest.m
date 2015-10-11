% Reference: Fitensemble, Fitctree, TreeBagger in Matlab documentation
% Script to load and preprocess data
% Choose between single decision tree model (with/without pruning)
% and bagged ensemble model
% Report error estimate and related plots

fprintf('loading data...\n');
% open file adult.data and adult.test
fid = fopen('adult.data');
fid2 = fopen('adult.test');
% set variable names
attr = {'age' 'workclass' 'fnlwgt' 'education' 'educationnum'...
    'maritalstatus' 'occupation' 'relationship' 'race'...
    'sex' 'capitalgain' 'capitalloss'...
    'hoursperweek' 'nativecountry','income'};
% predictor names
pred_attr = setdiff(attr,{'income'});
% categorical predictor names
categ_attr = {'workclass','education','maritalstatus','occupation','relationship',...
               'race','sex','nativecountry'};
% replace missing values
fid = strrep(fid,'?','');
fid2 = strrep(fid2,'?','');
% load data using "," as delimiter and consider missing value as empty
data = textscan(fid,'%f%s%f%s%f%s%s%s%s%s%f%f%f%s%s',...
      'Delimiter',',','TreatAsEmpty','');
data2 = textscan(fid2,'%f%s%f%s%f%s%s%s%s%s%f%f%f%s%s',...
      'Delimiter',',','TreatAsEmpty','');
% create table for data
data = table(data{:},'VariableNames',attr);
data2 = table(data2{:},'VariableNames',attr);
% close file
fclose(fid);
fclose(fid2);
% create predictor matrix
X = classreg.regr.modelutils.predictormatrix(data,'ResponseVar',size(data,2));
partTable = data(1:floor(end*3/4),:);
valTable = data(floor(end*3/4)+1:end,:);
partX = classreg.regr.modelutils.predictormatrix(partTable,'ResponseVar',size(partTable,2));
valX = classreg.regr.modelutils.predictormatrix(valTable,'ResponseVar',size(valTable,2));
testX = classreg.regr.modelutils.predictormatrix(data2,'ResponseVar',size(data2,2));
% create reponse vector 
Y = nominal(data.income);
partY = nominal(partTable.income);
valY = nominal(valTable.income);
testY = nominal(data2.income);
fprintf('Finish processing data...\n');


% experiment with pruning
fprintf('First experiment with single decision tree...\n\n');
fprintf('Experimenting pruning levels...\n');
ct = fitctree(partX,partY,'CrossVal','Off','PredictorNames',pred_attr,'CategoricalPredictors',categ_attr,'Prune','Off');
ct2 = fitctree(X,Y,'CrossVal','Off','PredictorNames',pred_attr,'CategoricalPredictors',categ_attr,'Prune','Off');
% tree without pruning
fprintf('No pruning case: \n');
fprintf('Validation error is %.4f: \n', loss(ct,valX,valY));
fprintf('With pruning(automatically set to optimal pruning sequence): \n');
% prune the tree
ctPrune = prune(ct);
ctPrune2 = prune(ct2);
% plot validation error vs. pruneLevel
figure 
pruneLoss = loss(ctPrune,valX,valY,'Subtrees','all');
plot(pruneLoss);
title('Validation error vs. pruneLevel');
xlabel('prunning level');
ylabel('validation error');

fprintf('Validation error(using proper pruneLevel) is %.4f\n', min(pruneLoss));
fprintf('Choose decision tree with pruning\n');
fprintf('Test error(using proper pruneLevel) is %.4f\n', min(loss(ctPrune2,testX,testY,'Subtrees','all')));


% TreeBagger
% first inspect how OOB error changes with numBag
% turn OOBVarImp on for inspecting feature importance
% in the next step
bag = TreeBagger(200,X,Y,'OOBVarImp','On','PredictorNames',pred_attr,'CategoricalPredictors',categ_attr);
figure
oobErr1 = oobError(bag);
plot(oobErr1);
title('OOB error vs. numBag');
xlabel('Number of grown trees');
ylabel('OOB classification error');
% report OOB error
fprintf('OOB classification error with numBag 200 is: %.4f\n', oobErr1(200));


% make plot to estimate feature importance
figure
bar(bag.OOBPermutedVarDeltaError);
title('Feature importance');
xlabel('Feature Index');
ylabel('Out-of-Bag Feature Importance');
idxvar = find(bag.OOBPermutedVarDeltaError>2);
fprintf('Selected import features are: \n');
impFeatures = attr(idxvar)
% learn a new treebagger with larger numBag on important features
bagFeature = TreeBagger(400,X(:,idxvar),Y,'OOBVarImp','off','OOBPred','on','PredictorNames',attr(idxvar),'CategoricalPredictors',impFeatures(2:3));
% plot OOB error vs. numBag after selecting important features
figure
oobErr2 = oobError(bagFeature);
plot(oobErr2);
title('OOB error vs. numBag(selected features)');
xlabel('Number of grown tree');
ylabel('OOB classification error');
% plot test error vs. numBag
figure
err2 = error(bagFeature,testX(:,idxvar),testY);
plot(err2);
title('Test error vs. numBag(selected features)');
xlabel('Number of grown trees');
ylabel('Test classification error');
% report OOB error and test error
fprintf('After selecting important features, OOB classification error with numBag 200 is: %.4f', oobErr2(400));
fprintf('After selecting important features, \ntest classification error with numBag 200 is: %.4f\n', err2(400));


                    