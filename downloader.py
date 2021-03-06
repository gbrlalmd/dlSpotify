import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_dl import YoutubeDL
import auth
import os
import urllib.request

auth.auth()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())


YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '',
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def cls():
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      _ = os.system('cls')

def dl(artist, track, fdir, req, tn):
    if req==1:
        YDL_OPTIONS['outtmpl'] = '{0}/{1} - {2}.%(ext)s'.format(fdir,artist,track)
    elif req==2:
        YDL_OPTIONS['outtmpl'] = '{0}/{1}. {2}.%(ext)s'.format(fdir,str(tn).zfill(2),track)
    query = '{0} - {1} audio'.format(artist,track)
    with YoutubeDL(YDL_OPTIONS) as ydl:
        ydl.extract_info(f'ytsearch:{query}', download=True)['entries'][0]

def batchdl(tracks, fdir, req):
    failedtracks = []
    count = 0
    fail = 0
    tn = 0
    for n in tracks:
        try:
            artist, track = n.split('!@!', 1)
            print('Downloading {0} - {1}'.format(artist,track))
            tn += 1
            dl(artist, track, fdir, req, tn)
            print('Download complete!')
            count += 1
        except:
            fail += 1
            failedtracks.append(n)
            print('Download failed!')
    return count, fail, failedtracks


def retry(failedtracks, fail, fdir):
    while True:
        ret = input('{} tracks failed to download. Retry downloading these tracks? Y/N\n'.format(fail))
        if ret.upper() == 'Y':
            count, fail, failedtracks = batchdl(failedtracks, fdir)
            print('More {} tracks downloaded.'.format(count))
            print('{} tracks failed again :('.format(fail))
            break
        elif ret.upper() == 'N':
            break
        elif ret.upper() != 'N' and ret.upper() != 'Y':
            print('Invalid command! Try again.')

def pd():
    cls()
    puri = input('Enter the Spotify Playlist URL or URI: ')
    exists = False
    try:
        sp.playlist(puri)
        exists = True
    except:
        print('Playlist does not exist.')
    if exists:
        playlistname = sp.playlist(puri)['name']
        tracks = sp.playlist_items(puri)['items']
        tracklist = []
        cdir = os.getcwd()
        fdir = os.path.join(cdir, r'{}'.format(playlistname))
        if not os.path.exists(fdir):
            os.makedirs(fdir)
        for n in tracks:
            artist = n['track']['artists'][0]['name']
            track = n['track']['name']
            search = '{0}!@!{1}'.format(artist, track)
            tracklist.append(search)
        count, fail, failedtracks = batchdl(tracklist,fdir, 1)
        print('{0} tracks downloaded from playlist "{1}"!'.format(count, playlistname))
        if fail > 0:
            retry(failedtracks, fail, fdir)

def ad():
    cls()
    auri = input('Enter the Spotify Album URL or URI: ')
    exists = False
    try:
        album = sp.album(auri)
        exists = True
    except:
        print('Album not found!')
    if exists:
        albumname = album['name']
        albumartist = album['artists'][0]['name']
        year = album['release_date'][0:4]
        cover = album['images'][0]['url']
        tracks = album['tracks']['items']
        tcount = 0
        tracklist = []
        cdir = os.getcwd()
        fdir = os.path.join(cdir, r'{0} - {1} ({2})'.format(albumartist,albumname,year))
        if not os.path.exists(fdir):
            os.makedirs(fdir)
        for n in tracks:
            tcount += 1
            artist = n['artists'][0]['name']
            track = n['name']
            search = '{0}!@!{1}'.format(artist, track)
            tracklist.append(search)
        count, fail, failedtracks = batchdl(tracklist,fdir, 2)
        urllib.request.urlretrieve(cover, '{}/folder.jpg'.format(fdir))
        print('{0} of {1} tracks from "{2} - {3}" downloaded!'.format(count,tcount,albumartist,albumname))
        if fail>0:
            retry(failedtracks, fail, fdir)