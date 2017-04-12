from flask import Flask, redirect, url_for, request, render_template
from operator import itemgetter
import os
import csv
import math
app = Flask(__name__)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).
    Source: http://gis.stackexchange.com/a/56589/15183
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    dist = 3961 * c
    # km = 6367 * c (for kilometers)
    return dist

@app.route('/')
def enterCoords():
    return render_template('enterCoords.html')

@app.route('/coordination', methods = ['POST'])
def showCoords():

    myLati = float(request.form['lati'])
    myLongi = float(request.form['longi'])

    rawFile = open('subwayData.csv')
    rawObject = csv.reader(rawFile)
    subwayData = list(rawObject)

    withinDistance1 = []

    #Filters out a list of subways within distance
    for row in subwayData:
        distance = haversine(myLongi, myLati, float(row[2]), float(row[1]))
        if distance <= 20:
            row.append(distance)
            withinDistance1.append(row)

    #Sorts subway list by distance in ascending order
    withinDistance_sorted = sorted(withinDistance1, key=itemgetter(6))

    #Rounds distance down to 2 decimal places
    for row in withinDistance_sorted:
        row[6] = round(row[6], 2)

    return render_template('showCoords.html', withinDistance = withinDistance_sorted)

if __name__ == '__main__':
     app.debug = True
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)