import numpy as np 
from keras.layers import *
from keras.models import * 
from keras.applications.vgg16 import preprocess_input
from keras.utils import load_img, img_to_array
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences

from keys import google
import time
import googlemaps # pip install googlemaps
import pandas as pd # pip install pandas

def bone_fracture():
    loaded_model=load_model("pred_models/best_model.h5")
    img = load_img('image123.jpg',target_size=(224,224))
    imag = img_to_array(img)
    imaga = np.expand_dims(imag,axis=0) 
    res=loaded_model.predict(imaga)
    a=res[0]
    if a<0.5:
        op="Fracture"   
    else:
        op="Normal"
    return str(op)


def lung_disease():
    check='lung_disease.jpg'
    model=load_model("pred_models/Pneumonia.h5")
    img=load_img(check, target_size=(150, 150), grayscale=True)
    img=np.array(img)/255
    img=img.reshape(-1,150,150,1)
    isPneumonic=model.predict(img)[0]
    imgClass='Pneumonic' if isPneumonic<0.5 else 'Normal'
    return imgClass

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

#Depression----------------------------------------------------------------------------------------
def predict_sentiment1(text):
    max_vocab = 20000000
    tokenizer = Tokenizer(num_words=max_vocab)
    data = pd.read_csv('csv_file/data1.csv')
    a=data.text.values
    tokenizer.fit_on_texts(a)
    load=load_model('pred_models/tweetanalysis.h5',compile=False)
    text_seq = tokenizer.texts_to_sequences(text)
    text_pad = pad_sequences(text_seq, maxlen=942)
    predicted_sentiment = load.predict(text_pad).round()
    if predicted_sentiment == 1.0:
        return 'depressed'
    else:
        return 'normal'
    
def mental_health(text):
    count=0
    for i in text:
        if predict_sentiment1(i)=='depressed':
            count+=1
    if count>=2:
        return 'Depressed'
    else:
        return "Normal"

def miles_to_meters(miles):
    try:
        return miles * 1_609.344
    except:
        return 0
        

def get_doctors(location,doctor):
    API_KEY = google['API_KEY']
    map_client = googlemaps.Client(API_KEY)

    address = location
    geocode = map_client.geocode(address=address)
    (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))


    search_string = doctor
    distance = miles_to_meters(2)
    business_list = []

    response = map_client.places_nearby(
        location=(lat, lng),
        keyword=search_string,
        radius=distance
    )   

    business_list.extend(response.get('results'))
    return business_list