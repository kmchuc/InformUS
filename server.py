import requests
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

r = requests.get('https://www.googleapis.com/civicinfo/v2/voterinfo?address=990%20Jackson%20Street%20San%20Francisco%2C%20CA%2094133&key=AIzaSyCALOx3a43D4qa6l_2R9YJPAPF43A4NnjA')

voting_info = r.json()

polling_locations = voting_info['pollingLocations']

first_result = polling_locations[0]

for polling_address in first_result['address']:
    print fir