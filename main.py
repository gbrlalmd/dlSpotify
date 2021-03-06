import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_dl import YoutubeDL
import os
import auth

auth.auth()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
a=1
def cls():
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      _ = os.system('cls')

cls()
puri = input('Enter the Spotify Playlist URL or URI: ')
exists = False
try:
    playlist = sp.playlist(puri)
    exists = True
except:
    print('Playlist does not exist.')
if exists:
    playlistname = sp.playlist(puri)['name']
    tracks = sp.playlist_items(puri)['items']
    count = 0
    fail = 0
    failedtracks = []
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
        artist = n['track']['artists'][0]['name']
        track = n['track']['name']
        search = '{0} - {1} audio'.format(artist, track)
        try:
            print('Downloading {0} - {1}'.format(artist,track))
            with YoutubeDL(YDL_OPTIONS) as ydl:
                video = ydl.extract_info(f'ytsearch:{search}', download=True)['entries'][0]
            print('Download complete!')
            count += 1
        except:
            fail +=1
            failedtracks.append(search)
            print('Download failed!')

    cls()
    print('{0} tracks downloaded from playlist "{1}"!'.format(count,playlistname))
    if fail>0:
        while True:
            ret = input('{} tracks failed to download. Retry downloading these tracks? Y/N\n'.format(fail))
            if ret.upper() == 'Y':
                count = 0
                fail = 0
                for n in failedtracks:
                    try:
                        print('Downloading {0}'.format(n.rsplit(' ', 1)[0]))
                        with YoutubeDL(YDL_OPTIONS) as ydl:
                            video = ydl.extract_info(f'ytsearch:{n}', download=True)['entries'][0]
                        print('Download complete!')
                        count += 1
                    except:
                        fail += 1
                        print('Download failed!')
                    print('More {} tracks downloaded.'.format(count))
                    print('{} tracks failed again :('.format(fail))
                break
            elif ret.upper() == 'N':
                break
            elif ret.upper() != 'N' and ret.upper() != 'Y':
                print('Invalid command! Try again.')
