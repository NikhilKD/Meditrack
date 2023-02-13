import numpy as np 
from keras.layers import *
from keras.models import * 
from keras.applications.vgg16 import preprocess_input
from keras.utils import load_img, img_to_array
import pickle
import numpy as np
import pandas as pd

def bone_fracture():
    loaded_model=load_model("best_model.h5")
    img = load_img('image123.jpg',target_size=(224,224))
    imag = img_to_array(img)
    imaga = np.expand_dims(imag,axis=0) 
    res=loaded_model.predict(imaga)
    a=res[0]
    if a<0.5:
        op="Fracture"   
    else:
        op="Normal"
    return "THE UPLOADED X-RAY IMAGE IS: "+str(op)


def lung_disease():
    loaded_model=load_model("lungpred.h5",compile=False)
    img=load_img('lung_disease.jpg',target_size=(224,224))
    x=img_to_array(img)
    x=np.expand_dims(x,axis=0)
    img_data=preprocess_input(x)
    classes=loaded_model.predict(img_data)
    print(classes)
    if classes[0][0]==0.0 and classes[0][1]==1.0:
        return "The person has pneumonia"
    elif classes[0][0]==1.0 and classes[0][1]==0.0:
        return "The person is normal"
    return "ille"
# ..................................................
# diabetes_dataset = pd.read_csv('diabetes.csv')
# diabetes_dataset.groupby('Outcome').mean()
# X = diabetes_dataset.drop(columns = 'Outcome', axis=1)
# Y = diabetes_dataset['Outcome']
# scaler = StandardScaler()
# scaler.fit(X)

import pickle

#Diabetes:----------------------------------------------------------------
def diabetes_predict(p,g,bp,st,insulin,bmi,dpf,age):
    load_m1=pickle.load(open("modelnaivebayes.pkl","rb"))
    load_m2=pickle.load(open("modelrandomforest.pkl","rb"))
    y_pred = load_m1.predict([[p,g,bp,st,insulin,bmi,dpf,age]])
    y_pre= load_m2.predict([[p,g,bp,st,insulin,bmi,dpf,age]])
    print(y_pred)
    print(y_pre)
    if y_pred==1 and y_pre==1:
        print("Diabetic")
    else:
        print("Non Diabetic")

#Insurance----------
def insurance_pre(a,g,b,c,s,r):
    loaded_model=pickle.load(open('modelregress.pkl','rb'))
    input_data = (a,g,b,c,s,r)
    # age=int
    # gender=0 for male 1 for female  
    # bmi=float
    # children=int
    # smoker=0 for yes 1 for no
    # 'region':{'southeast':0,'southwest':1,'northeast':2,'northwest':3}
    # changing input_data to a numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    res=loaded_model.predict(input_data_reshaped)
    inr = res[0] * 82.52
    print(res[0])
    return f'The insurance cost is Rs {str(round(inr,2))} approx'
    