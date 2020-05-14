#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:13:25 2020

@author: user
"""
import folium
import pandas

def coloring(elevation):
    if elevation<500:
        return 'blue'
    elif 1500>elevation>500:
        return 'orange'
    else:
        return 'red'

map=folium.Map(location=[38.58,-99.09],zoom_start=4,tiles = "Stamen Terrain")
#this is an instance of a Map object. Defines the start point of map. Zoom factor and the look
fgv=folium.FeatureGroup(name='Volcanos')
data=pandas.read_csv('volcanoes.txt')#pandas DataFrame object
    #I will pass a whole bunch of coordinates with lots of info about volcanos    
# print(data)

"""
No we add polygons just here as we are using the fg-feature group
that is added to the map
"""
fgp=folium.FeatureGroup(name='Population')
fgp.add_child(folium.GeoJson(data=(open('world.json','r',encoding='utf-8-sig').read())))


"""
We need to get lists for coordinates
"""
html = """<h4>Volcano information:</h4>
<strong>Name: </strong>%s<br /><br />\

"""
lat=list(data['LAT'])#we get one coordinate
# print(lat)
lon=list(data['LON'])#we get the other coordinate
elev=list(data['ELEV'])#we get info for popups
name=list(data['NAME'])
tp=list(data['TYPE'])
for lt,ln,nm,tp,el in zip(lat,lon,name,tp,elev):#we iterate over two lists
    iframe = folium.IFrame(html=html  %nm+ 'Type: \n'+tp+' Elevation: '+str(el)+' meters', width=200, height=150)
# for coordinates in [[38.2,-99.1],[39,-98]]:
    fgv.add_child(folium.Marker(location=[lt,ln],popup=folium.Popup(iframe),icon=folium.Icon(color=coloring(el)))) 
#makes markers on map and displays info. needs coordinates. For multiple - loop over. Needs list of lists


map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")#Automatically generate html file with the map and markers. Fully functional
