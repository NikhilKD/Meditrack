import numpy as np 
from keras.layers import *
from keras.models import * 
from keras.applications.vgg16 import preprocess_input
from keras.utils import load_img, img_to_array

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
