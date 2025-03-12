# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:58:53 2023

@author: fvfentanes
"""
#Tensor Flow First Model
############Dependencies############
import tensorflow as tf
import numpy as np
import logging
import matplotlib.pyplot as plt
logger=tf.get_logger()
logger.setLevel(logging.ERROR)
############DATA FOR TRAINING ############
celsius_q=np.array([-40,-10,0,8,15,22,38],dtype=float)
fahrenheit_a=np.array([-40,14,32,46,59,72,100],dtype=float)
############ MODEL ############
lo=tf.keras.layers.Dense(units=1, input_shape=[1])#Units numer of neurons in the layer & Shape input to this layer, in this case is a single variable
#We just define the layer 
#Assemble layers  into the model
model=tf.keras.Sequential([lo])
############ COMPILE THE MODEL ############
model.compile(loss="mean_squared_error", optimizer=tf.keras.optimizers.Adam(0.1))
"Esto lo usaremos durante el entranamiento, calcularemos la perdida en cada punto y la iremos mejorando con el optimizador"
############ TRAINING ############
history=model.fit(celsius_q,fahrenheit_a,epocsh=500,verbose=False)
print("Finishing training")
plt.xlabel('Epoch Number')
plt.ylabel("Loss Magnitude")
plt.plot(history.history['loss'])
abs()