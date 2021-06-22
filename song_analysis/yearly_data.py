import matplotlib.pyplot as plt
from matplotlib import colors

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