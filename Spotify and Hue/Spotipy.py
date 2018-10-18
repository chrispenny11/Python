import sys
import spotipy
import spotipy.util as util

scope = 'user-read-currently-playing'

token = util.prompt_for_user_token("Chris Penny",scope,client_id='dd41386aabca41aa8dd7ba2f947782b3',client_secret='53ffd5dd1b6c4771826d8e0f67c63271',redirect_uri='http://locallhost.com/')

##sp = spotipy.Spotify(auth=token)
##
##results = sp.user_playlists("Chris Penny")
##for item in results['items']:
##    track = item['track']
##    print(track['name'] + ' - ' + track['artists'][0]['name'])
##
##
##birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
##spotify = spotipy.Spotify()
##
##results = spotify.artist_albums(birdy_uri, album_type='album')
##albums = results['items']
##while results['next']:
##    results = spotify.next(results)
##    albums.extend(results['items'])
##
##for album in albums:
##    print(album['name'])
