# Ian Annase
# 4/16/18

import os
import sys
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import urllib.request as req


# Get the username from terminal
#username = sys.argv[1]
scope = 'current_user_playing_track user-read-private user-read-playback-state user-modify-playback-state'

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token("Chris Penny", client_id='dd41386aabca41aa8dd7ba2f947782b3',client_secret='4bf7eefcbf7241298d92b9f5ad6fe3f0',redirect_uri='http://google.com/')
#    token = util.prompt_for_user_token(username, scope) # add scope
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
#    token = util.prompt_for_user_token(username, scope) # add scope
    token = util.prompt_for_user_token("Chris Penny", client_id='dd41386aabca41aa8dd7ba2f947782b3',client_secret='4bf7eefcbf7241298d92b9f5ad6fe3f0',redirect_uri='http://google.com/')

# Create our spotify object with permissions
sp = spotipy.Spotify(auth=token)

# Get current device
#devices = spotifyObject.devices()
#deviceID = devices['devices'][0]['id']

##### Current track information
##track = spotifyObject.current_user_playing_track()
##artist = track['item']['artists'][0]['name']
##track = track['item']['name']
##
##if artist != "":
##    print("Currently playing " + artist + " - " + track)

# User information
user = sp.current_user()
displayName = user['display_name']
followers = user['followers']['total']
#print(user)
#print(dir(user))

#result = sp.search('Mogwai')
#print(result)

track = sp.current_user_playing_track()
#str_location = track.index('images')
print(list(track))
items = track['item']
string_items = str(items)
image_loc = string_items.find('images')
image_loc_end = string_items.find('width', image_loc)
image_url = string_items[image_loc+34:image_loc_end-4]
req.urlretrieve(image_url, "Temporary Image Directory/temp_artwork.jpg")
#print(test_item)
#print(dir(track))
#image_url = track['is playing']
#print(image_url)
