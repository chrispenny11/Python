# Initialize
import os
import sys
import json
import pandas as pd
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError as JSONDE
import urllib.request as req # For saving album art image from URL
import numpy as np
import PIL
from PIL import Image, ImageFilter # Allows python to interact with saved album art jpeg.
import colour # For conversion of RGB color scale to CIE xy chromaticity (see: https://en.wikipedia.org/wiki/CIE_1931_color_space)
import matplotlib # For plotting RGB histograms
from matplotlib import pyplot as pypl


# Define function for obtaining colors to pass to Philips Hue API Wrapper (phue package)
def get_artwork_colors():
    
# Define scope
    scope = 'current_user_playing_track user-read-private user-read-playback-state user-modify-playback-state'

# Obtain Spotify Token (username, client_id, and client_secret will vary per user - for additional information see Spotify API documentation.)
    try:
        token = util.prompt_for_user_token("Chris Penny", client_id='dd41386aabca41aa8dd7ba2f947782b3',client_secret='4bf7eefcbf7241298d92b9f5ad6fe3f0',redirect_uri='http://google.com/')
# Error Case - Remove token cache and replace
    except (AttributeError, JSONDE):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token("Chris Penny", client_id='dd41386aabca41aa8dd7ba2f947782b3',client_secret='4bf7eefcbf7241298d92b9f5ad6fe3f0',redirect_uri='http://google.com/')

# Generate spotipy object using Spotify Token
    spot_obj = spotipy.Spotify(auth=token)

# Call spotipy attribute for the currently playing track
    track = spot_obj.current_user_playing_track()
    #print(list(track)) # For Debug

# NOTE: While the current_user_playing_track() attribute results in a dictionary, the album art image URL is not assigned to a key and must be extracted by parsing.
    items = track['item']
    
# Convert dictionary object to string and parse the album art image URL.
    string_items = str(items)
    image_loc = string_items.find('images')
    image_loc_end = string_items.find('width', image_loc)
    image_url = string_items[image_loc+34:image_loc_end-4]

# Use the urllib library to save the image as a temporary file in a sub-directory.
    req.urlretrieve(image_url, "Temporary Image Directory/temp_artwork.jpg")
    #print(image_url) # For Debug

    album_art_test = Image.open("Temporary Image Directory/temp_artwork.jpg").convert("L")
    album_art = Image.open("Temporary Image Directory/temp_artwork.jpg")
    print(album_art.mode)

    histogram = album_art.histogram()
#    print(rgb_data)

# Convert image to a numpy array.
    rgb_tuples = np.asarray(album_art)
#    print(rgb_tuples)
#    print(type(rgb_tuples.shape))


# Stack with Numpy
    for i in range(0, 639):
        if i==0:
            np_stack = rgb_tuples[i]
        if i > 0:
            np_stack = np.vstack((np_stack, rgb_tuples[i]))

    print(np.shape(np_stack))

    pd_rgb_stack = pd.DataFrame(np_stack, columns = ['r', 'g', 'b'])
#    print(pd_rgb_stack['r'])
    pd_rgb_stack['rgb'] = (pd_rgb_stack['r'].astype(str)) + '_' + (pd_rgb_stack['g'].astype(str)) + '_' + (pd_rgb_stack['b'].astype(str))
    pd_rgb_stack['check_sum'] = pd_rgb_stack[['r', 'b', 'g']].sum(axis=1)

#   Sort by Value Counts to find modal values and return in order of frequency
    pd_rgb_sorted = pd_rgb_stack['rgb'].value_counts().to_frame()
    pd_rgb_sorted.astype(int)
    print(pd_rgb_sorted.iloc[0])
    print(pd_rgb_sorted)
    print(pd_rgb_stack['rgb'].head())
    print(pd_rgb_stack['check_sum'].head(20))
    check_sum_mean = pd_rgb_stack['check_sum'].mean()
    print(check_sum_mean)
#    r_select = pd_rgb_sorted['r'].values[0]
#    r_select = pd_rgb_sorted.loc[1, 'r']
    print(pd_rgb_stack['r'])
#    print(r_select)

#Guiding Idea: Take the highest frequency rgb combination that is a sufficient distance from the max value.

# Initialize Values for While Loop
    rgb_temp_std = 0
    rgb_temp_sum = 0
    i = -1

    #and (rgb_temp_sum < 50)
# Implement While Loop to Ensure Color is not black/white/greyscale (in which all rgb values are approximately the same)
    while (rgb_temp_std < 10):
        i = i + 1
        temp = pd_rgb_sorted.index[i]
        parse_1 = temp.find('_')
        parse_2 = temp.find('_', parse_1+1)
        rgb_temp = pd.DataFrame({'r':[temp[0:parse_1]], 'g':[temp[parse_1+1: parse_2]], 'b':[temp[parse_2+1:]]}).astype(int)
        rgb_temp_std = np.std(rgb_temp, 1)[0]
        rgb_temp_sum = rgb_temp['r'] + rgb_temp['g'] + rgb_temp['b']

    rgb_select = rgb_temp
    print(rgb_temp)

    pd_rgb_stack['r_select'] = rgb_select['r'][0]
    pd_rgb_stack['g_select'] = rgb_select['g'][0]
    pd_rgb_stack['b_select'] = rgb_select['b'][0]

#    pd_rgb_stack['dist_score'] = pd_rgb_stack['r'] - r_select
    pd_rgb_stack['dist_score'] = np.sqrt(np.square(pd_rgb_stack['r'] - pd_rgb_stack['r_select']) + np.square(pd_rgb_stack['g'] - pd_rgb_stack['g_select']) + np.square(pd_rgb_stack['b'] - pd_rgb_stack['b_select']))
    print(pd_rgb_stack['dist_score'].head(20))
    dist_score_sorted = pd_rgb_stack['dist_score'].value_counts().to_frame()
    dist_score_std = np.std(pd_rgb_stack['dist_score'])
    print(dist_score_std)

# Recreate Sorted List On DF including distance score -- Merge/Join?
    pd_rgb_sorted = pd_rgb_stack['rgb'].value_counts().to_frame()
    pd_rgb_sorted.astype(int)

# Reset Initial Values for Second While Loop
    rgb_temp_std = 0
    rgb_temp_sum = 0
    j = -1

# Perform left join on pd_rgb_stack to get distance scores in same dataframe
    pd_rgb_merged = pd_rgb_stack.join(pd_rgb_sorted, on = 'rgb', how = 'left', rsuffix = '_count')

# Second While Loop    
##    while (rgb_temp_std < 10):
##        j = j + 1
##        temp = pd_rgb_sorted.index[j]
##        parse_1 = temp.find('_')
##        parse_2 = temp.find('_', parse_1+1)
##        rgb_temp = pd.DataFrame({'r':[temp[0:parse_1]], 'g':[temp[parse_1+1: parse_2]], 'b':[temp[parse_2+1:]]}).astype(int)
##        rgb_temp_std = np.std(rgb_temp, 1)[0]
##        rgb_temp_sum = rgb_temp['r'] + rgb_temp['g'] + rgb_temp['b']

# Generate Histograms and Plot
            
    histogram_test = album_art_test.histogram()
    #print(histogram_test)
    r_hist = histogram[1:256]
    r_hist_max = r_hist.index(max(r_hist))
    g_hist = histogram[257:512]
    g_hist_max = g_hist.index(max(g_hist))
    b_hist = histogram[513:768]
    b_hist_max = b_hist.index(max(b_hist))
    rgb_max = [r_hist_max, g_hist_max, b_hist_max]
    print(rgb_max)

    # Generate Histogram Plot with RGB channels
    fig, histo = pypl.subplots()
    histo.plot(r_hist, 'r')
    histo.plot(g_hist, 'g')
    histo.plot(b_hist, 'b')
    histo.plot(histogram_test, 'black')
    pypl.show()

    # Assuming sRGB encoded colour values.
    RGB = np.array([r_hist_max, g_hist_max, b_hist_max])

    # Conversion to tristimulus values.
    XYZ = colour.sRGB_to_XYZ(RGB / 256)

    # Conversion to chromaticity coordinates.
    xy = colour.XYZ_to_xy(XYZ)
    print(xy)
    return(xy)

get_artwork_colors()
