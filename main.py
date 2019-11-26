from datetime import datetime

import pickledb
import spotipy
import spotipy.util as util

from keys import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, USERNAME

db = pickledb.load('tmp.db', False)

scope = 'user-library-read playlist-modify-private playlist-read-private'
token = util.prompt_for_user_token(USERNAME, scope, client_id=SPOTIPY_CLIENT_ID,
                                   client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri='https://github.com/djmango')

def get_all_playlists(poffset=0):
    playlistRequest = sp.current_user_playlists(limit=50, offset=poffset)
    playlists = []

    while not len(playlistRequest['items']) == 0:
        # get the next 50
        playlistRequest = sp.current_user_playlists(limit=50, offset=poffset)
        # for song saved
        for playlist in playlistRequest['items']:

            playlistName = playlist['name']
            playlists.append(playlistName)
            print('got playlist: ' + playlistName)

        if len(playlistRequest['items']) < 50:
            return playlists
        else:
            poffset += 50
    
# make sure we auth'd
if token:  
    sp = spotipy.Spotify(auth=token)

    # get all playlists
    playlists = get_all_playlists()
    print(playlists)

    # get all saved
    offset = 0
    saved = sp.current_user_saved_tracks(limit=50, offset=offset)
    
    # repeat until we've gone through all the saved
    while not len(saved['items']) == 0:
        # get the next 50
        saved = sp.current_user_saved_tracks(limit=50, offset=offset)

        # for song saved
        for item in saved['items']:
            date = item['added_at']
            
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
            date_string = date.strftime('%B `%y')
            # date_string example: November `19


            track = item['track']
            print(track['name'] + ' - ' + track['artists'][0]['name'])
            # now we have to check if the playlist exists
            offset = 0
            sp.current_user_playlists(limit=50, offset=offset)

        # check if weve gone through all the songs
        if len(saved['items']) < 50:
            saved['items'] = []
        else:
            offset += 50

else:
    print("Can't get token for", USERNAME)

db.dump()
