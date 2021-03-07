from downloader import pd, ad, mvd
import os

def cls():
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      _ = os.system('cls')

cls()
while True:
    print('dlSpotify by gbrlalmd')
    opt = input('1 - Playlist Downloader\n2 - Album Downloader\n3 - Music Video Downloader (EXPERIMENTAL)\n')
    if opt == '1':
        pd()
        break
    elif opt == '2':
        ad()
        break
    elif opt == '3':
        mvd()
        break
    else:
        print('Invalid command! Try again.')
input('Press ENTER to exit.')