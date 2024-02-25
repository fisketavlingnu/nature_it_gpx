#!/usr/bin/env python3
import os,sys
import argparse
import xml
from xml.dom import minidom
import xml.etree.ElementTree as gfg  
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
import subprocess




parser = argparse.ArgumentParser(description='skapa en effektiv gpx fil från länsstyrelsens generade KML fil')

parser.add_argument('-file',help='File to read', required=True)
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
outdata=[]
#root = gfg.Element('gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"')
root = gfg.Element('<gpx version="1.1" creator="GDAL 2.2.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogr="http://osgeo.org/gdal" xmlns="http://www.topografix.com/GPX/1/1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">')

for n in db:
    track=gfg.Element("trk")
    name=gfg.SubElement(track,"name")
    name.text=n
    trackseq=gfg.Element("trkseq")
    root.append(track)
    track.append(trackseq)
    c=db[n]
    i=0;
    pos=list(c.split(","))
    #Remove last 0.0 to get an even list
    pos.pop()
    psize=len(pos)
#    print("DBG:"+str(psize))
    for i in range(0,psize,2):
        p=pos[i]
        p=p.strip()
        point="trkpt"
        point=point+" lon=\""+str(pos[i])+"\""+ " lat=\""+str(pos[i+1])+"\""
        i=i+2
#        print("DBG:"+str(i)+" "+point)
        trackpoint=gfg.SubElement(trackseq,point)
    outdata.append(track)
    tree = gfg.ElementTree(track)
    NewXML="tmp."+str(n)+".gpx"
    out = open(NewXML, 'wb')
    out.write(b'<?xml version="1.0"?>')
    out.write(b'<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">')
    tree.write(out, encoding = 'UTF-8', xml_declaration = False)
    #    with open ("tmp."+str(n)+".gpx", "wb") as files : 
#       tree.write(files) 

    
with open('tmp.all.gpx', 'w') as outfile:
    for n in db:
        fname="tmp."+str(n)+".gpx"
        cmd="echo <gpx> >> "+fname
        returned_value = subprocess.call(cmd, shell=True)
        dest=str(n)+".gpx"
        print("Prettyfing "+fname+" to "+dest)
        cmd="xmllint --format "+fname+ ">" +dest
        returned_value = subprocess.call(cmd, shell=True)
        
        

print("Removing temporary files")
cmd="rm -f tmp.*.gpx"
#returned_value = subprocess.call(cmd, shell=True)
