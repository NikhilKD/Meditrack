import numpy as np 
# import pandas as pd
# import matplotlib.pyplot as plt
# import tensorflow as tf
# print(tf.__version__)
# from keras import Sequential
from keras.layers import *
from keras.models import * 
# from keras.preprocessing import image
# from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from keras.utils import load_img, img_to_array

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
loaded_model=load_model("best_model.h5")
def ans():
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