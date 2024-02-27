#!/usr/bin/env python3
#------------------------------------------------------------
#   Copyright 2024 Outdoor Recreation Sverige
#   All Rights Reserved Worldwide
#
#   Licensed under the Apache License, Version 2.0 (the
#   "License"); you may not use this file except in
#   compliance with the License.  You may obtain a copy of
#   the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in
#   writing, software distributed under the License is
#   distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#   CONDITIONS OF ANY KIND, either express or implied.  See
#   the License for the specific language governing
#   permissions and limitations under the License.
#------------------------------------------------------------

import os,sys
import argparse
import subprocess
import gpxpy
import gpxpy.gpx
from datetime import date

today = date.today()

parser = argparse.ArgumentParser(description='skapa en effektiv gpx fil från länsstyrelsens generade KML fil')

parser.add_argument('-file',help='File to read', required=True)
parser.add_argument('-output',help='Name of output file', required=True)
parser.add_argument('-filter',help='Filter on name of area', required=False)
parser.add_argument('-area',help='Area', required=False)
args = parser.parse_args()

print("Processar "+args.file+"för att generera "+args.output+":")


filedata=open(args.file,"r")
coordinates=""
db={}
name=""    
for line in filedata:
    # Record name
    line=line.strip()
    if (line.find("SimpleData name=\"JAKTOMR") or line.find("coordinates")):
        if "SimpleData name=\"JAKTOMR" in line:
            no_of_polygons=0

            tmp=list(line.split(">"))
            tmp.pop()
            tmp.remove(tmp[0])
            for t in tmp:
                name=list(t.split("<"))
                name.pop()
                name=name.pop()
                db[name]="#"
        elif "coordinate" in line:
            if no_of_polygons==0:
                line=line.replace("<coordinates>",'')
                line=line.replace("</coordinates>",'')
                line=line.replace("0.0 ",'')
                db[name]=line
                no_of_polygons+=1
            else:
                if args.filter is None:
                    print("VARNING("+name+ "): har flera polygoner associerade med sig - Använder endast första polygonen.")
                elif args.filter in name:
                    print("VARNING("+name+ "): har flera polygoner associerade med sig - Använder endast första polygonen.")

gpx = gpxpy.gpx.GPX()

gpx.description="Denna fil med jaktområden används på egen risk!"
gpx.time=today
gpx.author_name="Outdoor Recreation Sverige"
gpx.author_email="info@fisketavling.nu"

for n in db:
    if (args.filter==None):
        gpx_track = gpxpy.gpx.GPXTrack(name=n,description=args.area)
        gpx.tracks.append(gpx_track)
        # Segment
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        c=db[n]
        i=0;
        pos=list(c.split(","))
        #Remove last 0.0 to get an even list
        pos.pop()
        psize=len(pos)
        for i in range(0,psize,2):
            p=pos[i]
            p=p.strip()
            lon=pos[i]
            lat=pos[i+1]
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat,lon))
    elif (args.filter in n):
        gpx_track = gpxpy.gpx.GPXTrack(name=n,description=args.area)
        gpx.tracks.append(gpx_track)
        # Segment
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        c=db[n]
        i=0;
        pos=list(c.split(","))
        #Remove last 0.0 to get an even list
        pos.pop()
        psize=len(pos)
        for i in range(0,psize,2):
            p=pos[i]
            p=p.strip()
            lon=pos[i]
            lat=pos[i+1]
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat,lon))
        
outfile=open(args.output,"w")
for line in gpx.to_xml():
    outfile.write(line)
outfile.close()

print("Skapade "+args.output)




 
