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
        
        SPOTIPY_CLIENT_ID=client_id
        SPOTIPY_CLIENT_SECRET=client_secret 
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, 
                                                                                    client_secret=SPOTIPY_CLIENT_SECRET))
        
        return spotify

    def get_song_info(self, playlist_ids):
        '''Returns the information of each song in one or more given Spotify playlists'''
        
        playlists = []
        track_ids = []
        songs = []
        artists = []
        dates = []
        count = 0
        
        # Get songs in each playlist
        for playlist_id in playlist_ids:
            playlists.append(self.spotify.playlist_items(playlist_id))
        
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
            track_info.append(self.spotify.audio_features(track_ids[i*100:i*100+100]))
        
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
        data.dropna(inplace=True)
        
        return data

def graph_year_data(data, year):
    '''Graph distribution of features for songs in a given year'''
    
    data_year = data.loc[data['year'] == year]
    features = ['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    
    fig, axs = plt.subplots(5, 2, tight_layout=True, figsize=(18,20))
    count = 0 
    for i in range(5):
        for j in range(2):
            N, bins, patches = axs[i, j].hist(data_year[features[count]], bins=10)
            axs[i, j].set_title(features[count].capitalize(), fontdict={'fontsize':22})
            count += 1

            section = N / N.max()
            
            norm = colors.Normalize(section.min(), section.max())

            for thisfrac, thispatch in zip(section, patches):
                color = plt.cm.viridis(norm(thisfrac))
                thispatch.set_facecolor(color)