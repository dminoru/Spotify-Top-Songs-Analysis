import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import MinMaxScaler
 
class Making_DF:    
    def __init__(self, client_id, client_secret):
        '''Handle client credentials flow'''
        
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, 
                                                                                    client_secret=client_secret))
        
    def get_song_info(self, spotify, playlist_ids):
        '''Returns the information of each song in one or more given Spotify playlists'''
        
        playlists = []
        track_ids = []
        songs = []
        artists = []
        dates = []
        count = 0
        
        # Get songs in each playlist
        for playlist_id in playlist_ids:
            playlists.append(spotify.playlist_items(playlist_id))
        
        # Get information for each song
        for playlist in playlists:
            for i in range(len(playlist['items'])):
                track_ids.append(playlist['items'][i]['track']['id'])
                songs.append(playlist['items'][i]['track']['name'])
                artists.append(playlist['items'][i]['track']['album']['artists'][0]['name'])
                dates.append(2019-count)
            count += 1
        
        # Get audio features of each track
        track_info = []
        for i in range(len(track_ids)//100):
            track_info.append(spotify.audio_features(track_ids[i*100:i*100+100]))
        
        # Create final list of tracks with all of the information
        final_list = []
        for sublist in track_info:
            for item in sublist:
                if item:
                    final_list.append(item)
                else:
                    final_list.append({})
        
        return final_list, songs, dates, artists
                    
    def create_dataframe(self, final_list, songs, dates, artists):
        '''Creates a dataframe using the track information'''
        
        data = pd.DataFrame.from_dict(final_list)
        data['track_name'] = pd.Series(songs)
        data['year'] = pd.Series(dates)
        data['artist'] = pd.Series(artists)
        return data

    def preprocessing_data(self, data):
        '''Normalize the features to all be between 0 to 1 and create final dataframe'''
        
        features = ['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
        x = data[features] 
        scaler = MinMaxScaler()
        x_scaled = scaler.fit_transform(x)
        data[features] = x_scaled
        data = data[['track_name', 'artist', 'year', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']]
        data = data.dropna()
        
        return data
    
    def run_function(self, playlist_ids):
        final_list, songs, dates, artists = self.get_song_info(self.spotify, playlist_ids)
        data = self.create_dataframe(final_list, songs, dates, artists)
        data = self.preprocessing_data(data)
        return data
                
