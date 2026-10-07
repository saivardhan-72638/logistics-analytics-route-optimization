import json,joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error,mean_squared_error,accuracy_score,precision_score,recall_score,f1_score,roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
FEATURES=['freight_value','order_value','item_count','seller_count','customer_state','purchase_weekday']; NUM=FEATURES[:4]; CAT=FEATURES[4:]
def prep(): return ColumnTransformer([('num',SimpleImputer(strategy='median'),NUM),('cat',Pipeline([('imp',SimpleImputer(strategy='most_frequent')),('oh',OneHotEncoder(handle_unknown='ignore'))]),CAT)])
def train_models(d,out):
    d=d.dropna(subset=['delivery_days','late_flag']).sort_values('order_purchase_timestamp'); cut=int(len(d)*.8); tr,te=d.iloc[:cut],d.iloc[cut:]; Xtr,Xte=tr[FEATURES],te[FEATURES]
    reg=Pipeline([('prep',prep()),('model',RandomForestRegressor(n_estimators=150,random_state=42,n_jobs=-1,min_samples_leaf=2))]); reg.fit(Xtr,tr.delivery_days); rp=reg.predict(Xte)
    rm={'mae_days':round(mean_absolute_error(te.delivery_days,rp),3),'rmse_days':round(mean_squared_error(te.delivery_days,rp)**.5,3),'train_rows':len(tr),'test_rows':len(te)}; joblib.dump(reg,out/'delivery_time_regressor.joblib')
    clf=Pipeline([('prep',prep()),('model',RandomForestClassifier(n_estimators=150,random_state=42,n_jobs=-1,class_weight='balanced'))]); clf.fit(Xtr,tr.late_flag); cp=clf.predict(Xte); prob=clf.predict_proba(Xte)[:,1]
    cm={'accuracy':round(accuracy_score(te.late_flag,cp),3),'precision':round(precision_score(te.late_flag,cp,zero_division=0),3),'recall':round(recall_score(te.late_flag,cp,zero_division=0),3),'f1':round(f1_score(te.late_flag,cp,zero_division=0),3),'roc_auc':round(roc_auc_score(te.late_flag,prob),3) if te.late_flag.nunique()>1 else None}; joblib.dump(clf,out/'late_risk_classifier.joblib')
    r={'regression':rm,'classification':cm}; (out/'model_results.json').write_text(json.dumps(r,indent=2)); return r
