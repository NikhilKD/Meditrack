import numpy as np 
import pickle

#Diabetes:----------------------------------------------------------------
def diabetes_predict(p,g,bp,st,insulin,bmi,dpf,age):
    load_m1=pickle.load(open("pred_models/modelnaivebayes.pkl","rb"))
    load_m2=pickle.load(open("pred_models/modelrandomforest.pkl","rb"))
    y_pred = load_m1.predict([[p,g,bp,st,insulin,bmi,dpf,age]])
    y_pre= load_m2.predict([[p,g,bp,st,insulin,bmi,dpf,age]])
    print(y_pred)
    print(y_pre)
    if y_pred==1 and y_pre==1:
        return "Diabetic"
    else:
        return "Non Diabetic"

#Insurance-------------------------------------------------------
def insurance_pre(a,g,b,c,s,r):
    loaded_model=pickle.load(open('pred_models/modelregress.pkl','rb'))
    input_data = (a,g,b,c,s,r)
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    res=loaded_model.predict(input_data_reshaped)
    inr = res[0] * 82.52
    inr=inr/10
    print(res[0])
    return f'The insurance cost is Rs {str(round(inr,2))} approx'

#heart disease-----------------------------------------------------------
def heart_prediction(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,old,slope,ca,thal):

    inputdata=(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,old,slope,ca,thal)

    inputdata_asnumpyarray=np.asarray(inputdata) #changing the input for the numpy array

    inputdata_reshape=inputdata_asnumpyarray.reshape(1,-1)

    filename='pred_models/heartdis_pred_model'

    loadedmodel=pickle.load(open(filename,'rb'))

    cred=loadedmodel.predict(inputdata_reshape)
    if(cred[0]==0):
        return 'Healthy heart'
    else:
        return 'Heart Disease'