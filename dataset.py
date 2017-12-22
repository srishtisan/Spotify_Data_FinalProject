# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 14:38:48 2017

@author: srishti 
"""

import spotipy


import spotipy.util as util

from spotipy.oauth2 import SpotifyClientCredentials

import pprint
import pandas as pd

import matplotlib.pyplot as plt

import datetime as dt
from IPython.display import display, Image # Displays things nicely

# helper function to print info about dataframe

def df_info(df):
    print("Shape: ", df.shape)
    print("dtypes: ", df.dtypes.to_dict())
    print("index dtype: ", df.index.dtype)
    return pd.concat([df.head(3), df.tail(3)])



SPOTIPY_CLIENT_ID= # Located in a private txt
SPOTIPY_CLIENT_SECRET= #Located in a private txt
SPOTIPY_REDIRECT_URI= 'http://localhost:8888/callback'

scope = 'user-library-read'
username = 'srishy'

client_credentials_manager = SpotifyClientCredentials(client_id = SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

token = util.prompt_for_user_token(username, scope, client_id = SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri= SPOTIPY_REDIRECT_URI)

#%%

def identify(song_id):
    print(sp.track(song_id)['name'])
    song_results = sp.audio_features(song_id)
    pprint.pprint(song_results)
    
#%%

df1 = pd.read_excel("billboard.xlsx", sheetname = "billboard")

df2 = pd.read_excel("billboard_hits.xlsx", sheetname = "billboard_hits")


df1 = df1[['Issue Date', 'Track Name']].copy()

#%%
track_basics = pd.merge(df1, df2, how='outer', on = "Track Name", indicator = True)
track_basics

#%%
tracks = pd.read_excel("track_basics.xlsx", sheetname = "Sheet1")
tracks.head()

#%%

ids = [] 
for index, row in tracks.iterrows():
        ids.append(row['Spotify URI'])

print(ids)
 
#%%

ids_unique=set(ids)
ids_unique=list(ids_unique)
print(ids_unique)

#%%

features = []
def get_features():
    for i in range(0,len(ids_unique),50):    
        audio_features = sp.audio_features(ids_unique[i:i+50])
        for track in audio_features:
            features.append(track) 

# if necessary (though unlikely), can use this to reset the features list.           
def reset_features(features):
    features = []
    

get_features()        
print(features)


#%%

feat_frame=pd.DataFrame(features)
feat_frame.rename(columns = {'uri': 'Spotify URI'}, inplace=True)
feat_frame.head()

#%%

features_set = pd.merge(tracks, feat_frame, how='outer', on = "Spotify URI", indicator = True)
features_set.head()

#%%

from pandas import ExcelWriter

writer = ExcelWriter("full_features.xlsx")
features_set.to_excel(writer, 'Sheet1')

writer.save()

#%%

tracks = pd.read_excel("full_features.xlsx", sheet_name = "Sheet1")
tracks.head()



