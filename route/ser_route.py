from flask import Flask, render_template, url_for, request, redirect, Blueprint
from matplotlib.pyplot import specgram
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from collections import Counter
import os
import tensorflow as tf
import numpy as np
import json
import requests
import librosa
import librosa.display
import pickle
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import glob 
import IPython.display as ipd  # To play sound in the notebook
import sys
import warnings

ser_route = Blueprint('ser_route',__name__)
#tesorflow server
MODEL_URI='http://3.34.44.190:8501/v1/models/saved_model:predict'

EMOTION_LIST = {'happy':1, 'neutral':2, 'sad':3, 'angry':4}
sentence_num = 0
sentence_emo = []
#모델 전처리 및 rest api결과 받아옴
def get_prediction(wav_path):
    newData, newSR = librosa.load(wav_path
                              ,duration=2.5
                              ,sr=44100
                              ,offset=0.5)

    newSR = np.array(newSR)
    mfccs = np.mean(librosa.feature.mfcc(y=newData, sr=newSR, n_mfcc=13),axis=0)
    newdf = pd.DataFrame(data=mfccs).T

    newdf= np.expand_dims(newdf,axis=2)
    
    data = json.dumps({'instances':newdf.tolist()})

    
    response = requests.post(MODEL_URI, data=data)
    

    filename = filename = 'ser_files/labels'
    infile = open(filename,'rb')
    lb = pickle.load(infile)
    infile.close()
    print(response.content)
    predictions = np.array(json.loads(str(response.content, 'utf-8'))['predictions'])
    
    final = predictions.argmax(axis=1)
    
    # Get the final predicted label
    final = final.astype(int).flatten()
    
    final = (lb.inverse_transform((final)))
    
    return final[0]


@ser_route.route('/predict', methods=['POST'])
def predict():
    index =  str(int(request.form['index']) + 1)
    result = get_prediction(index)
    return result