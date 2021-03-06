import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_dl import YoutubeDL
import os
import auth

auth.auth()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def cls():
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      _ = os.system('cls')

cls()

puri = input('Enter the Spotify Playlist URL or URI: ')
playlistname = sp.playlist(puri)['name']
tracks = sp.playlist_items(puri)['items']
count = 0
cdir = os.getcwd()
fdir = os.path.join(cdir, r'{}'.format(playlistname))
if not os.path.exists(fdir):
    os.makedirs(fdir)
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '{}/%(title)s.%(ext)s'.format(fdir),
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }

for n in tracks:
    count+=1
    artist = n['track']['artists'][0]['name']
    track = n['track']['name']
    search = '{0} - {1} audio'.format(artist,track)
    print('Downloading {0} - {1}'.format(artist,track))
    with YoutubeDL(YDL_OPTIONS) as ydl:
        video = ydl.extract_info(f'ytsearch:{search}', download=True)['entries'][0]
    print('Download complete!')
cls()
print('{0} tracks downloaded from playlist "{1}"!'.format(count,playlistname))
