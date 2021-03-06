import os
import base64 as bsf

def dec(x):
    x = x.encode('ascii')
    x = bsf.b64decode(x)
    x = x.decode('ascii')
    return(x)

def auth():
    os.environ['SPOTIPY_CLIENT_ID'] = dec('ZWFiZWU2ODExMzY1NDQ4YWI4YTZiMzViMDAxYzI0ZDM=')
    os.environ['SPOTIPY_CLIENT_SECRET'] = dec('NGNjNjE0OWQ1YWJjNDE1NmIwNzMxYTY3YWM3OTQzM2U=')
