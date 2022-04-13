#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.


import logging
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

from spotipy.oauth2 import SpotifyClientCredentials
from tokens import SpotifyCID as SCID, SpotifyCS as SCS, spotify_user as SU

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

scope = [
        'user-read-currently-playing',
        'streaming',
        'user-read-playback-state',
        'user-modify-playback-state'
        ]
RDURI = 'http://localhost:6969/'
username = SU

token = util.prompt_for_user_token(username, scope, client_id=SCID, client_secret=SCS, redirect_uri=RDURI)

spotify = spotipy.Spotify(auth=token)

def get_currently_playing():
    current_track = spotify.current_user_playing_track()

    try:
        for track in current_track:
            #print(track)
            track = current_track['item']
            artist = track['artists'][0]['name']
            now_playing = track['name']
        return ("{} by {}".format(now_playing,artist))
    except:
        return 1

def play_next():
    spotify.next_track(device_id=None)

def play_previous():
    spotify.previous_track(device_id=None)
######
def play_pause():
    spotify.pause_playback(device_id=None)

def set_volume(vol):
    spotify.volume(volume_percent=vol, device_id=None)

def set_shuffle(setshuf):
    spotify.shuffle(state=setshuf, device_id=None)

def play_play():
    spotify.start_playback(device_id=None, context_uri=None, uris=None, offset=None, position_ms=None)
	
def refresh_token():
    global spotify
"""
    cached_token = spotify.get_cached_token()
    refreshed_token = cached_token['refresh_token']
    new_token = spotify.refresh_access_token(refreshed_token)
    # also we need to specifically pass `auth=new_token['access_token']`
    spotify = spotipy.Spotify(auth=new_token['access_token'])
    return new_token
"""		
#print(spotify.devices())
#print(spotify.me())
#print(spotify.currently_playing(market=None, additional_types=None))
