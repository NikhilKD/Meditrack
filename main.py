import numpy as np 
from keras.layers import *
from keras.models import * 
from keras.applications.vgg16 import preprocess_input
from keras.utils import load_img, img_to_array
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

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
diabetes_dataset = pd.read_csv('diabetes.csv')
diabetes_dataset.groupby('Outcome').mean()
X = diabetes_dataset.drop(columns = 'Outcome', axis=1)
Y = diabetes_dataset['Outcome']
scaler = StandardScaler()
scaler.fit(X)

import pickle
# pickle.dump(classifier,open('diabetes_model.pkl','wb'))
# scaler = StandardScaler()
# scaler.fit(X)
# loaded_m=pickle.load(open('diabetes_model.pkl','rb'))
# input_data = (1,100,72,19,173,25.8,0.587,18)

# # changing the input_data to numpy array
# input_data_as_numpy_array = np.asarray(input_data)

# # reshape the array as we are predicting for one instance
# input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

# # # standardize the input data
# std_data = scaler.transform(input_data_reshaped)
# # print(std_data)

# prediction = loaded_m.predict(input_data_reshaped)
# # print(prediction)

# if (prediction[0] == 0):
#     print('The person is not diabetic')
# else:
#     print('The person is diabetic')

#Diabetes:----------------------------------------------------------------
def diabetes_predict(p,g,bp,st,insulin,bmi,dpf,age):
    loaded_model=pickle.load(open('diabetes_model.pkl','rb'))
    print(type(p))
    print(type(g))
    print(type(bp))
    print(type(st))
    print(type(insulin))
    print(type(bmi))
    print(type(dpf))
    print(type(age))
    input_data = (p,g,bp,st,insulin,bmi,dpf,age)
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    # standardize the input data
    std_data = scaler.transform(input_data_reshaped)
    # # print(std_data)
    res=loaded_model.predict(std_data)
    if (res == 0):
        return 'The person is not diabetic'
    else:
        return 'The person is diabetic'
# print(res)
