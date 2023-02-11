import numpy as np 
# import pandas as pd
# import matplotlib.pyplot as plt
# import tensorflow as tf
# print(tf.__version__)
# from keras import Sequential
from keras.layers import *
from keras.models import * 
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
# from keras.preprocessing.image import ImageDataGenerator
# from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from keras.utils import load_img, img_to_array
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

# ..................................................
diabetes_dataset = pd.read_csv('diabetes.csv')
diabetes_dataset.groupby('Outcome').mean()
X = diabetes_dataset.drop(columns = 'Outcome', axis=1)
Y = diabetes_dataset['Outcome']
scaler = StandardScaler()
scaler.fit(X)
# standardized_data = scaler.transform(X)
# X = standardized_data
# Y = diabetes_dataset['Outcome']
# X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, stratify=Y, random_state=2)
# classifier = svm.SVC(kernel='linear')
# classifier.fit(X_train, Y_train)
# X_train_prediction = classifier.predict(X_train)
# training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
# print('Accuracy score of the training data : ', training_data_accuracy)
# X_test_prediction = classifier.predict(X_test)
# test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
# print('Accuracy score of the test data : ', test_data_accuracy)
# input_data = (1,100,72,19,173,25.8,0.587,18)

# # changing the input_data to numpy array
# input_data_as_numpy_array = np.asarray(input_data)

# # reshape the array as we are predicting for one instance
# input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

# # standardize the input data
# std_data = scaler.transform(input_data_reshaped)
# print(std_data)

# prediction = classifier.predict(std_data)
# print(prediction)

# if (prediction[0] == 0):
#     print('The person is not diabetic')
# else:
#     print('The person is diabetic')

# import pickle
# pickle.dump(classifier,open('diabetes_model.pkl','wb'))
scaler = StandardScaler()
scaler.fit(X)
loaded_m=pickle.load(open('diabetes_model.pkl','rb'))
input_data = (1,100,72,19,173,25.8,0.587,18)

# changing the input_data to numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the array as we are predicting for one instance
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

# # standardize the input data
std_data = scaler.transform(input_data_reshaped)
# print(std_data)

prediction = loaded_m.predict(input_data_reshaped)
# print(prediction)

if (prediction[0] == 0):
    print('The person is not diabetic')
else:
    print('The person is diabetic')

#--------------------------------
# import os
# for dirname, _, filenames in os.walk('/kaggle/input'):
#     for filename in filenames:
#         print(os.path.join(dirname, filename))

# train_path= 'dataset/archive (6)/train'
# test_path='dataset/archive (6)/val'
# train_datagen = image.ImageDataGenerator(
#     rotation_range=15,
#     shear_range=0.2,
#     zoom_range=0.2,
#     horizontal_flip=True,
#     fill_mode='nearest',
#     width_shift_range=0.1,
#     height_shift_range=0.1
# )
# val_datagen= image.ImageDataGenerator(    rotation_range=15,
#     shear_range=0.2,
#     zoom_range=0.2,
#     horizontal_flip=True,
#     fill_mode='nearest',
#     width_shift_range=0.1,
#     height_shift_range=0.1)

# train_generator = train_datagen.flow_from_directory(
#     train_path,
#     target_size = (224,224),
#     batch_size = 4,
#     class_mode = 'binary')
# validation_generator = val_datagen.flow_from_directory(
#     test_path,
#     target_size = (224,224),
#     batch_size = 4,
#     shuffle=True,
#     class_mode = 'binary')

# base_model = tf.keras.applications.EfficientNetB3(weights='imagenet', input_shape=(224,224,3), include_top=False)

# for layer in base_model.layers:
#     layer.trainable=False
# model = Sequential()
# model.add(base_model)
# model.add(GaussianNoise(0.25))
# model.add(GlobalAveragePooling2D())
# model.add(Dense(512,activation='relu'))
# model.add(BatchNormalization())
# model.add(GaussianNoise(0.25))
# model.add(Dropout(0.25))
# model.add(Dense(1, activation='sigmoid'))
# model.summary()

# model.compile(loss='binary_crossentropy',
#             optimizer='adam',
#             metrics=['accuracy','Precision','Recall','AUC'])

# lrp=ReduceLROnPlateau(monitor="val_loss", factor=0.1, patience=2)
# filepath='best_model.h5'
# checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
# call=[checkpoint,lrp]
# history = model.fit(
#     train_generator,
#     epochs=10,
#     validation_data=validation_generator,
#     steps_per_epoch= 50,
#     callbacks=call
#     )

# model.evaluate(train_generator)
# model.evaluate(validation_generator)


# ypred = model.predict(imaga)
# print(ypred)
# a=ypred[0]
# if a<0.5:
#     op="Fracture"   
# else:
#     op="Normal"
# # plt.imshow(img)
# print("THE UPLOADED X-RAY IMAGE IS: "+str(op))
# model.save("model.h5")

# def bone_fracture():
#     loaded_model=load_model("best_model.h5")
#     img = load_img('image123.jpg',target_size=(224,224))
#     imag = img_to_array(img)
#     imaga = np.expand_dims(imag,axis=0) 
#     res=loaded_model.predict(imaga)
#     a=res[0]
#     if a<0.5:
#         op="Fracture"   
#     else:
#         op="Normal"
#     return "THE UPLOADED X-RAY IMAGE IS: "+str(op)

# def lung_disease():
#     loaded_model=load_model("lungpred.h5",compile=False)
#     img=load_img('lung_disease.jpg',target_size=(224,224))
#     x=img_to_array(img)
#     x=np.expand_dims(x,axis=0)
#     img_data=preprocess_input(x)
#     classes=loaded_model.predict(img_data)
#     if classes[0][0]==0.0 and classes[0][1]==1.0:
#         return "The person has pneumonia"
#     elif classes[0][0]==1.0 and classes[0][1]==0.0:
#         return "The person is normal"
#     else:
#         return "ille"

# loaded_model=load_model("lungpred.h5",compile=False)
# img=load_img('lung_disease.jpg',target_size=(224,224))
# x=img_to_array(img)
# x=np.expand_dims(x,axis=0)
# img_data=preprocess_input(x)
# classes=loaded_model.predict(img_data)
# if round(classes[0][1])==1.0:
#     print("The person has pneumonia")
# elif round(classes[0][0])==1.0:
#     print("The person is normal")
# else:
#     print("The person")
# print(classes)

# img = load_img('image123.jpg',target_size=(224,224))
# print(type(img))
# imag = img_to_array(img)
# imaga = np.expand_dims(imag,axis=0) 
# loaded_m=load_model("model.h5")
# r=loaded_m.predict(imaga)
# b=r[0]
# if b<0.5:
#     op="Fracture"   
# else:
#     op="Normal"
# print("THE UPLOADED X-RAY IMAGE IS: "+str(op))


#Diabetes:----------------------------------------------------------------
# loaded_model=pickle.load(open('diabetes_model2.pkl','rb'))
# p=1
# g=89
# bp=66
# st=23
# insulin=94
# bmi=28.1
# dpf=0.167
# age=21
# input_data = (p,g,bp,st,insulin,bmi,dpf,age)
# input_data_as_numpy_array = np.asarray(input_data)
# input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
# res=loaded_model.predict(input_data_reshaped)
# if (res == 0):
#     print('The person is not diabetic')
# else:
#     print('The person is diabetic')
# print(res)
