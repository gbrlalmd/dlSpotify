from downloader import pd, ad
import os

def cls():
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      _ = os.system('cls')

cls()
while True:
    print('Spotify Downloader by gbrlalmd')
    opt = input('1 - Playlist Downloader\n2 - Album Downloader\n3 - Single Track Downloader\n')
    if opt == '1':
        pd()
        break
    elif opt == '2':
        ad()
        break
    elif opt == '3':
        print('Not implemented yet :(')
        break
    else:
        print('Invalid command! Try again.')