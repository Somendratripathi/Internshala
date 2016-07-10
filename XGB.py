from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import preprocessing
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import xgboost as xgb

# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 16:57:10 2016

@author: sotripathi
https://github.com/hyperopt/hyperopt/wiki/FMin - Hyperopt documentation
"""





import pandas as pd;
import numpy as np;
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import preprocessing
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import xgboost as xgb


#import sys
# The path to XGBoost wrappers goes here
#sys.path.append('C:\\Users\\Amine\\Documents\\GitHub\\xgboost\\wrapper')
import xgboost as xgb

def score(params):
    print "Training with params : "
    print params
    num_round = int(params['n_estimators'])
    del params['n_estimators']
    dtrain = xgb.DMatrix(X_train, y_train)
    dvalid = xgb.DMatrix(X_test, y_test)
    # watchlist = [(dvalid, 'eval'), (dtrain, 'train')]
    model = xgb.train(params, dtrain, num_round)
    predictions = model.predict(dvalid)#.reshape((X_test.shape[0], 3))
    score = auc(y_test, predictions)
    print "\tScore {0}\n\n".format(score)
    return {'loss': score, 'status': STATUS_OK}

def optimize(trials):
    space = {
             'n_estimators' : hp.quniform('n_estimators', 100, 1000, 10),
             'eta' : hp.quniform('eta', 0.025, 0.5, 0.05),
             'max_depth' : hp.quniform('max_depth', 1, 13, 1),
             'min_child_weight' : hp.quniform('min_child_weight', 1, 6, 1),
             'subsample' : hp.quniform('subsample', 0.5, 1, 0.1),
             'gamma' : hp.quniform('gamma', 0.5, 1, 0.1),
             'colsample_bytree' : hp.quniform('colsample_bytree', 0.5, 1, 0.1),
             'eval_metric': 'auc',
             'objective': 'binary:logistic',
             'nthread' : 5,
             'silent' : 1,
             'alpha':hp.quniform('alpha', 0, 1, 0.1),
             'lambda':hp.quniform('lambda',0,1,0.1)
          }
    best = fmin(score, space, algo=tpe.suggest, trials=trials, max_evals=250)

    print best



X, y = trains,target
print "Splitting data into train and valid ...\n\n"
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1234)

#Trials object where the history of search will be stored
trials = Trials()

optimize(trials)

'''
{'colsample_bytree': 0.65, 'min_child_weight': 1.0, 'n_estimators': 204.0,
 'subsample': 0.9500000000000001, 'eta': 0.17500000000000002, 'max_depth': 5.0, 'gamma': 0.75}
 '''
