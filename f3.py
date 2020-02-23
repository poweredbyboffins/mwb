

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
train="select winprob,loseconc,loseprob,winconc,homeformadj/100,awayformadj/100,coalesce(pctwin,0),coalesce(pctnotwin,0) from pred_res where matchdate < '2016-01-18'"
#sql="select winprob,coalesce(pctwin,0) from traingamepred"
traindata=lq.getdata2(train)
sql="select case result when 'H' then 20 when 'A' then 10 when 'D' then 0 end from pred_res where matchdate < '2016-01-18'"
result=lq.getdata2(sql)
traindata = traindata.astype(np.float32)
sql="select winprob,loseconc,loseprob,winconc,homeformadj/100,awayformadj/100,coalesce(pctwin,0),coalesce(pctnotwin,0) from gamepred p join rescuttmp r on replace(lower(r.hometeam),' ','')=lower(p.hometeam) and replace(lower(r.awayteam),' ','')=lower(p.awayteam) and r.matchdate=p.matchdate where p.matchdate between '2016-01-19' and '2016-04-20' and winprob is not null and loseconc is not null";
predict=lq.getdata2(sql)
sql="select case r.ftr when 'H' then 20 when 'A' then 10 when 'D' then 0 end from gamepred p join rescuttmp r on replace(lower(r.hometeam),' ','')=lower(p.hometeam) and replace(lower(r.awayteam),' ','')=lower(p.awayteam) and r.matchdate=p.matchdate where p.matchdate between '2016-01-19' and '2016-04-20' and winprob is not null and loseconc is not null ";
teams=lq.getdata2(sql)



# Fit regression model
clf = RandomForestClassifier(n_estimators=10,random_state=1)

clf.fit(traindata, result.ravel())
#clf.predict(predict)
#mse = mean_squared_error(y_test, clf.predict(X_test))
#print (y_test)
#print (clf.predict(X_test))
#print("MSE: %.4f" % mse)



###############################################################################
# Plot training deviance

# compute test set deviance
x=0
y=0
for i, y_pred in enumerate(clf.predict(predict)):
     if (teams[i]==y_pred):
         x=x+1
     else:
         y=y+1
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
