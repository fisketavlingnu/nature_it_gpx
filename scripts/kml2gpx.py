#!/usr/bin/env python3
import os,sys
import argparse
#import xml
#from xml.dom import minidom
#import xml.etree.ElementTree as ET  
#from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
import subprocess
import gpxpy
import gpxpy.gpx



parser = argparse.ArgumentParser(description='skapa en effektiv gpx fil från länsstyrelsens generade KML fil')

parser.add_argument('-file',help='File to read', required=True)
parser.add_argument('-output',help='Name of output file', required=True)
args = parser.parse_args()
filedata=open(args.file,"r")
coordinates=""
db={}
name=""    
for line in filedata:
    # Record name
    line=line.strip()
    if (line.find("SimpleData name=\"JAKTOMR") or line.find("coordinates")):
        if "SimpleData name=\"JAKTOMR" in line:
            tmp=list(line.split(">"))
            tmp.pop()
            tmp.remove(tmp[0])
            for t in tmp:
                name=list(t.split("<"))
                name.pop()
                name=name.pop()
                db[name]="#"
                #print("Name="+name)
        elif "coordinate" in line:
            line=line.replace("<coordinates>",'')
#            line=line.replace("0.0</coordinates>",'')
            line=line.replace("</coordinates>",'')
            line=line.replace("0.0 ",'')
            db[name]=line
            #print("DBG:"+line)

gpx = gpxpy.gpx.GPX()
for n in db:
    gpx_track = gpxpy.gpx.GPXTrack(name=n)
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
    


#print('Created GPX:', gpx.to_xml())




 
