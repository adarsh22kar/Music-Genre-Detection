import os
import json
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import argparse
import librosa
import numpy as np
from pydub import AudioSegment
from tensorflow.keras.models import load_model

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['mp3', 'wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'therandomstring'

genres = {
    'Metal': 0, 'Disco': 1, 'Classical': 2, 'Hiphop': 3, 'Jazz': 4, 
    'Country': 5, 'Pop': 6, 'Blues': 7, 'Reggae': 8, 'Rock': 9
}

@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    
    destination="/".join([target, filename])
    # destination2="/".join([target, filename])
   
    file.save(destination)
    
    session['uploadFilePath']=destination
    response="File Uploaded!"
    # getGenre(filename)
    return getGenre(filename)

def majority_voting(scores, dict_genres):
    preds = np.argmax(scores, axis = 1)
    values, counts = np.unique(preds, return_counts=True)
    counts = np.round(counts/np.sum(counts), 2)
    votes = {k:v for k, v in zip(values, counts)}
    votes = {k: v for k, v in sorted(votes.items(), key=lambda item: item[1], reverse=True)}
    return [(get_genres(x, dict_genres), prob) for x, prob in votes.items()]


def get_genres(key, dict_genres):
    labels = []
    tmp_genre = {v:k for k,v in dict_genres.items()}
    return tmp_genre[key]

def splitsongs(X, overlap = 0.5):
    temp_X = []
    xshape = X.shape[0]
    chunk = 33000
    offset = int(chunk*(1.-overlap))
    spsong = [X[i:i+chunk] for i in range(0, xshape - chunk + offset, offset)]
    for s in spsong:
        if s.shape[0] != chunk:
            continue
        temp_X.append(s)
    return np.array(temp_X)


def to_melspectrogram(songs, n_fft=1024, hop_length=256):
    melspec = lambda x: librosa.feature.melspectrogram(x, n_fft=n_fft,
        hop_length=hop_length, n_mels=128)[:,:,np.newaxis]
    tsongs = map(melspec, songs)
    return np.array(list(tsongs))
  

def make_dataset_dl(model,song,typeModel):
    signal, sr = librosa.load(song, sr=None)
    signals = splitsongs(signal)
    specs = to_melspectrogram(signals)
    return specs
    

def run(model,song,typeModel):
    if typeModel == "dl":       
        X = make_dataset_dl(model,song,typeModel)
        model = load_model(model)
        preds = model.predict(X)
        votes = majority_voting(preds, genres)
        # print("{} is a {} song".format(song, votes[0][0]))
        # print("most likely genres are: {}".format(votes[:3]))
        return json.dumps(votes[:3])

def main(model,song,typeModel):
    if typeModel not in ["dl"]:
        raise ValueError("Invalid type for the application. You should use dl or ml.")
    ans=run(model,song,typeModel)
    return ans

def getGenre(filename):
    model='./models/custom_cnn_2d.h5'
    song='./uploads/test_docs/{}'.format(filename)
    typeModel='dl'
    return main(model,song,typeModel)
    

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

CORS(app, expose_headers='Authorization')