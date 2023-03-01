import numpy as np 
from keras.layers import *
from keras.models import * 
from keras.utils import load_img, img_to_array
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
import pandas as pd # pip install pandas

def bone_fracture():
    loaded_model=load_model("pred_models/best_model.h5")
    img = load_img('image123.jpg',target_size=(224,224))
    imag = img_to_array(img)
    imaga = np.expand_dims(imag,axis=0) 
    res=loaded_model.predict(imaga)
    a=res[0]
    if a<0.04:
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

print(bone_fracture())
