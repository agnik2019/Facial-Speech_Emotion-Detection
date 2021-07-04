import librosa
import numpy as np
import pandas as pd

from tensorflow import keras
model = keras.models.load_model('model2_70ep')

class_to_label = {0 :'male_angry', 
                  1 : 'male_disgust', 
                  2:'male_fear', 
                  3 :'male_happy',
                  4:'male_neutral', 
                  5:'male_sad', 
                  6:'male_surprise',
                  7:'female_angry',
                  8:'female_disgust',
                  9: 'female_fear',
                  10: 'female_happy',
                  11: 'female_neutral' ,
                  12:'female_sad',
                   13:'female_surprise'}

def predictSpeech(filepath):
    X, sample_rate = librosa.load(filepath
                              ,res_type='kaiser_fast'
                              ,duration=3
                              ,sr=44100
                              ,offset=0.5)

    sample_rate = np.array(sample_rate)
    mfcc_test = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40),axis=0)
    mfcc_test = pd.DataFrame(data=mfcc_test).T
    mfcc_test= np.expand_dims(mfcc_test, axis=2)
    pred_test = model.predict(mfcc_test, 
                         batch_size=16, 
                         verbose=0)
    result = pred_test.argmax(axis=1)
    result = result.astype(int).flatten()
    result[0]
    return class_to_label[result[0]]