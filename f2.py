

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
import lineq6 as lq

###############################################################################
# Load data
#boston = datasets.load_boston()
sql="select winprob,loseconc,homeformadj/100,awayformadj/100,coalesce(pctwin,0),coalesce(pctnotwin,0) from pred_res"
#sql="select winprob,coalesce(pctwin,0) from traingamepred"
X=lq.getdata2(sql)
sql="select case result when 'H' then 20 when 'A' then 10 when 'D' then 0 end from pred_res"
y=lq.getdata2(sql)
#X, y = shuffle(boston.data, boston.target, random_state=13)
X = X.astype(np.float32)
offset = int(X.shape[0] * 0.9)
print (offset)
X_train, y_train = X[:offset], y[:offset]
X_test, y_test = X[offset:], y[offset:]

###############################################################################
# Fit regression model
params = {'n_estimators': 2000, 'max_depth': 16, 
          'learning_rate': 0.0001, 'loss': 'ls', }
#params = {'learning_rate':0.005, 'n_estimators':1500,'max_depth':9, 'min_samples_split':1200, 'min_samples_leaf':60, 'subsample':0.85, 'warm_start':True} 
#clf = ensemble.GradientBoostingRegressor(**params)
clf = RandomForestClassifier(n_estimators=10)

clf.fit(X_train, y_train)
mse = mean_squared_error(y_test, clf.predict(X_test))
#print (y_test)
#print (clf.predict(X_test))
print("MSE: %.4f" % mse)

###############################################################################
# Plot training deviance

# compute test set deviance
test_score = np.zeros((params['n_estimators'],), dtype=np.float64)
x=0
y=0
for i, y_pred in enumerate(clf.predict(X_test)):
    #test_score[i] = clf.loss_(y_test, y_pred)
    if (y_pred==y_test[i].astype(int)):
        x=x+1 
    else:
        y=y+1
print (x+y)
print (x/(x+y)*100)
"""
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title('Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, clf.train_score_, 'b-',
         label='Training Set Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',
         label='Test Set Deviance')
plt.legend(loc='upper right')
plt.xlabel('Boosting Iterations')
plt.ylabel('Deviance')

###############################################################################
# Plot feature importance
feature_importance = clf.feature_importances_
# make importances relative to max importance
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + .5
plt.subplot(1, 2, 2)
plt.barh(pos, feature_importance[sorted_idx], align='center')
#plt.yticks(pos, boston.feature_names[sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.show()
"""
