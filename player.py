#!/usr/bin/env python
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

DEVICE_ID="98bb0735e28656bac098d927d410c3138a4b5bca"
CLIENT_ID="624eed6c66314802b1a2eda4c251889e"
CLIENT_SECRET="77dc781d293d4b52ac43c475c9912be2"

SongListFile = 'SongList.txt'
SongList = []

# Read the file containing the list of songs to play
def load_song_list():
    with open(SongListFile, "r") as f:
        for line in f:
            SongList.append([x for x in line.replace("\n", "").split(",")])
    f.close()

# Find the song assocated with the scanned RFID
# If RFID is associated with a track, send command to play a track
# If RFID is associated with an album, send command to play an album
def find_song(rfid):
    found_track = 0
    
    for item in SongList:
        if item[0] == rfid:
            if item[2] == 'Track':
                sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:' + item[1]])
                sleep(2)
                found_track = 1
                break

            elif item[2] == 'Album':
                sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:' + item[1])
                sleep(2)
                found_track = 1
                break

# If RFID tag is not found, play this track (R.E.M. - It's the End of the World as We Know It)
    if found_track == 0:
        sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:2oSpQ7QtIKTNFfA08Cy0ku'])
        sleep(2)            

# load the song list from the text file
load_song_list()

while True:
    try:
        reader=SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri="http://localhost:8080",
                                                       scope="user-read-playback-state,user-modify-playback-state"))
        
        # create an infinite while loop that will always be waiting for a new scan
        while True:
            print("Waiting for record scan...")
            id= reader.read()[0]
            print("Card Value is:",id)
            sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
            
            # find the song using the scanned RFID tag
            find_song(str(id))

    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()