#!/usr/bin/env python
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

DEVICE_ID="98bb0735e28656bac098d927d410c3138a4b5bca"
CLIENT_ID="624eed6c66314802b1a2eda4c251889e"
CLIENT_SECRET="77dc781d293d4b52ac43c475c9912be2"

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
            
            # DONT include the quotation marks around the card's ID value, just paste the number
            if (id==1047326530359):
                
                # playing a song: Hazy Shade of Winter - Bangles
                sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:7EmsauPLjAy9XMNELaHBZa'])
                sleep(2)

            elif (id==291058495942):
                
                # playing a song: Disorder - Joy Division
                sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:5fbQCQt91LsVgXusFS0CCD'])
                sleep(2)
                 
            elif (id=='RFID-CARDVALUE-2'):
                
                # playing an album
                sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:0JGOiO34nwfUdDrD612dOp')
                sleep(2)
                
            # continue adding as many "elifs" for songs/albums that you want to play

    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()