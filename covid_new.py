import numpy as np
import pandas as pd
import warnings
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
#from sklearn.neighbors import KNeighborsClassifier
import pickle
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split

names=["cough","fever","sore_throat","shortness_of_breath","head_ache","age_60_and_above","abroad","contact_with_covid_object","contact_with_covid_patient","corona_result"]
dataframe = pd.read_csv('fs_data.csv', names=names)
# X_train = pd.read_csv('X_train.csv')
# y_train =  pd.read_csv('y_train.csv')
array = dataframe.values
X = array[1:,0:9]
y = array[1:,-1]

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3,random_state=42)


rfc = RandomForestClassifier()
rfc.fit(X_train, y_train)

pickle.dump(rfc,open('model.pkl','wb'))
model = pickle.load(open('model.pkl','rb'))