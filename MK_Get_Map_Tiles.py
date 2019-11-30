## This scrip uses maps from the Finnish Transport Agency (Open Data)
## Disclaimer: Ei navigointiin
## Karttojen Lähde: Liikennevirasto. Ei navigointikäyttöön. Ei täytä virallisen merikartan vaatimuksia.
## https://www.liikennevirasto.fi/avoindata/kayttoehdot/avoimen-tietokannan-lisenssi#.WyqO3aczZ3h

## Python code by Mikko Horsmanheimo (c)

## WARNING !!!!
## This has been a one off project and NONE OF THE CHARTS have been verified to be correct.
## To my understanding the geocoding is correct but this has not been verified for any of the charts. Do not use for navigation.

## VAROITUS !!!!
## Tama on ollut yksittainen projekti EIKA AINUTTAKAAN KARTTAA ole tarkistettu/varmistettu.
## Ymmartaakseni karttojen geokoodaus (kiinnitys koordinaatistoon) on oikein, mutta touta ei ole mitenkaan tarkistettu. EI NAVIGOINTIIN.

##The purpose of this is to retrieve a range of small map tiles  and combine the tiles into one large bitmap
##Also create the kap configuration/header file for the group of tiles
##And finally add a line in the batch file to run imgkap to create the KAP file(s)


## This scrip will generate bitmap (PNG) file(s) and the corresponding configuration (txt) file(s) that is needed for geocoding the image.
## Geocoding will be done with the command: "imgkap chartname.png chartname.txt"
## You will also need the utility program imgkap.exe to run the above command.

## You will also need a csv-configuration file containing the parameters needed for the map(s)
## The csv should contain a header row(s) containing: mapScale;fileName;x_min;x_max;y_min;y_max;zoomLevel
## the rows in the csv contain the name of the map datum, scale, the map filename and the tile limits for the map.
## The configuration csv file will need to be given as a parameter when starting the script
## Example: python MK_Get_Map_Tiles.py MK_A_data.csv


import math
import pandas
import time
import sys
from urllib import request
from PIL import Image


##http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

def MakeKapHeaderSingleTile(name_extension, xtile, ytile, zoom):
  NW_lat, NW_lon = num2deg(xtile, ytile, zoom)
  SE_lat, SE_lon = num2deg(xtile+1, ytile+1, zoom)
  NE_lat = NW_lat
  NE_lon = SE_lon
  SW_lat = SE_lat
  SW_lon = NW_lon
  ##Palautetaan kulmien koordinaatit
  name_extension = "WMTS_"+str(zoom)+"_"+str(xtile)+"_"+str(ytile)
  WriteKapHeader(scale, name_extension, 256, 256, zoom, NW_lat, NW_lon, NE_lat, NE_lon, SE_lat, SE_lon, SW_lat, SW_lon)

def MakeKapHeaderForGroupOfTiles(scale, name_extension, x_size, y_size, xmin, xmax, ymax, ymin, zoom):
  NW_lat, NW_lon = num2deg(xmin, ymin, zoom)
  SE_lat, SE_lon = num2deg(xmax+1, ymax+1, zoom)
  NE_lat = NW_lat
  NE_lon = SE_lon
  SW_lat = SE_lat
  SW_lon = NW_lon
  ##Palautetaan kulmien koordinaatit
  WriteKapHeader(scale, name_extension, x_size, y_size, zoom, NW_lat, NW_lon, NE_lat, NE_lon, SE_lat, SE_lon, SW_lat, SW_lon)

def AppendBatForImkapConversion(group, map):
# This will create a file called makekap.bat which can be run to perform the imgkap.exe conversion to KAP format
# (this can be usefull, if there are a lot of maps in the configuration csv) 
  with open("makekap.BAT", "a") as bat_file:
    print("magick "+map+".png -remap palette.png "+map+"_c128.png", file=bat_file)
    print("imgkap "+map+"_c128.png "+map+".txt", file=bat_file)
    print("copy "+map+"_c128.kap 128_Colors", file=bat_file)
  
  
def WriteKapHeader(scale, name_extension, x_size, y_size, zoom, NW_lat, NW_lon, NE_lat, NE_lon, SE_lat, SE_lon, SW_lat, SW_lon):
  with open(name_extension+".txt", "w") as text_file:
    print("VER/2.0", file=text_file)
    print("CED/SE=1,RE=1,ED=05/11/2017", file=text_file)
    print("BSB/NA= "+name_extension, file=text_file)
    print("    NU="+name_extension+",RA="+str(x_size)+","+str(y_size)+",DU=254", file=text_file)
    print("KNP/SC="+str(scale)+",GD=WGS 84,PR=MERCATOR, PP=0.0", file=text_file)
    print("    PI=UNKNOWN,SP=UNKNOWN,SK=0.0,TA=90", file=text_file)
    print("    UN=METERS,SD=UNKNOWN,DX=0,DY=0", file=text_file)
    print("REF/1,0,0,"+str(NW_lat)+","+str(NW_lon)+"", file=text_file)
    print("REF/2,"+str(x_size)+",0,"+str(NE_lat)+","+str(NE_lon)+"", file=text_file)
    print("REF/3,"+str(x_size)+","+str(y_size)+","+str(SE_lat)+","+str(SE_lon)+"", file=text_file)
    print("REF/4,0,"+str(y_size)+","+str(SW_lat)+","+str(SW_lon)+"", file=text_file)
    print("PLY/1,"+str(NW_lat)+","+str(NW_lon)+"", file=text_file)
    print("PLY/2,"+str(NE_lat)+","+str(NE_lon)+"", file=text_file)
    print("PLY/3,"+str(SE_lat)+","+str(SE_lon)+"", file=text_file)
    print("PLY/4,"+str(SW_lat)+","+str(SW_lon)+"", file=text_file)
    print("DTM/0.00,0.00", file=text_file)
    print("OST/1", file=text_file)
    print("IFM/6", file=text_file)

def GetTile(mapData, xtile, ytile, zoom):
  retryAttemptsRemaining = 15
  while retryAttemptsRemaining > 0:
    try:
    ##Get one tile from wmts and save bitmap as WMTS_zoom_x_y.png
      request.urlretrieve("https://julkinen.liikennevirasto.fi/rasteripalvelu/service/wmts?request=GetTile&version=1.0.0&service=wmts&layer="+mapData+"&TILEMATRIXSET=WGS84_Pseudo-Mercator&TileMatrix=WGS84_Pseudo-Mercator:"+str(zoom)+"&tilerow="+str(ytile)+"&tilecol="+str(xtile)+"&format=image/png&style=default","WMTS_"+str(zoom)+"_"+str(xtile)+"_"+str(ytile)+".png")
      #time.sleep(0.1)
    except request.URLError as e:
      print('Html-hakuvirhe:', e.reason ,' (uusi yritys)')
      retryAttemptsRemaining = retryAttemptsRemaining - 1
      time.sleep(1.0)
      if retryAttemptsRemaining <= 0:
        print("Hakuvirhe, lopetetaan...")
        exit()
      continue
    
    else:
      break




  ##  request.urlretrieve("https://julkinen.liikennevirasto.fi/rasteripalvelu/service/wmts?request=GetTile&version=1.0.0&service=wmts&layer=liikennevirasto:Merikarttasarja%20A%20public&TILEMATRIXSET=WGS84_Pseudo-Mercator&TileMatrix=WGS84_Pseudo-Mercator:"+str(zoom)+"&tilerow="+str(ytile)+"&tilecol="+str(xtile)+"&format=image/png&style=default","WMTS_"+str(zoom)+"_"+str(xtile)+"_"+str(ytile)+".png")


def RetrieveRangeOfTiles(mapData, scale, name_extension, xmin, xmax, ymin, ymax, zoom):
  NoumberOfTiles = ((xmax+1-xmin)*(ymax+1-ymin))
  x_size = str(256*(xmax+1-xmin))
  y_size = str(256*(ymax+1-ymin))
  MakeKapHeaderForGroupOfTiles(scale, name_extension, x_size, y_size, xmin, xmax, ymax, ymin, zoom)
  for x in range(xmin,xmax+1):
    for y in range(ymin,ymax+1):
      NoumberOfTiles -=1
      print(name_extension+" xtile: "+str(x)+", ytile: "+str(y)+" Remaining: "+str(NoumberOfTiles))
      GetTile(mapData, x, y, zoom)
      #MakeKapHeaderSingleTile(name_extension, x, y, zoom)
      #AppendBatConversion(x, y, zoom)
  merge_images(zoom, xmin, xmax, ymin, ymax, name_extension)
  print("Next run command: imgkap "+name_extension+".png "+name_extension+".txt" )
  

def merge_images( zoom, xmin, xmax, ymin, ymax, output_file) :
    TILESIZE = 256
    out = Image.new( 'RGB', ((xmax-xmin+1) * TILESIZE, (ymax-ymin+1) * TILESIZE) ) 

    imx = 0;
    for x in range(xmin, xmax+1) :
        imy = 0
        for y in range(ymin, ymax+1) :
            tile = Image.open( "WMTS_"+"%s_%s_%s.png" % (zoom, x, y) )
            out.paste( tile, (imx, imy) )
            imy += TILESIZE
        imx += TILESIZE
    out.save( output_file+".png")
    ##out.save( output_file+"%s_%s_%s.png" % (zoom, x, y))


	  
def main() :	  
# count the arguments
    if (len(sys.argv) - 1) != 1:
        print("Anna parametriksi tiedostonimi")
        exit()
    else:
        gridData = pandas.read_csv(sys.argv[1], na_filter='', dtype=str, sep=';', comment='#')
        print(gridData)
        for index, row in gridData.iterrows():
            RetrieveRangeOfTiles(row['mapData'], int(row['mapScale']), row['fileName'], int(row['x_min']), int(row['x_max']), int(row['y_min']), int(row['y_max']), int(row['zoomLevel']))
            AppendBatForImkapConversion(sys.argv[1], row['fileName'])




####################################################
main()
####################################################


## 

#Kartta: MK_A_604
#RetrieveRangeOfTiles("MK_A_604", 18902, 18918, 9405, 9435, 15)

#Kartta: MK_A_605
#RetrieveRangeOfTiles("MK_A_605", 18876, 18912, 9420, 9445, 15)

#Kartta: MK_A_606
#RetrieveRangeOfTiles("MK_A_606", 18874, 18902, 9438, 9463, 15)

#Kartta: MK_A_607
#RetrieveRangeOfTiles("MK_A_607", 18855, 18881, 9419, 9454, 15)

#Kartta: MK_A_608
#RetrieveRangeOfTiles("MK_A_608", 18844, 18878, 9450, 9476, 15)

#Kartta: MK_A_609
#RetrieveRangeOfTiles("MK_A_609", 18830, 18865, 9410, 9435, 15)

#Kartta: MK_A_610
#RetrieveRangeOfTiles("MK_A_610", 18827, 18862, 9432, 9457, 15)

#Kartta: MK_A_611
#RetrieveRangeOfTiles("MK_A_611", 18807, 18833, 9425, 9460, 15)

#Kartta: MK_A_612
#RetrieveRangeOfTiles("MK_A_612", 18813, 18848, 9453, 9479, 15)

#Kartta: MK_A_613
#RetrieveRangeOfTiles("MK_A_613", 18786, 18812, 9426, 9460, 15)

#Kartta: MK_A_614
#RetrieveRangeOfTiles("MK_A_614", 18794, 18820, 9451, 9485, 15)

#Kartta: MK_A_615
#RetrieveRangeOfTiles("MK_A_615", 18764, 18790, 9432, 9466, 15)

#Kartta: MK_A_616
#RetrieveRangeOfTiles("MK_A_616", 18772, 18798, 9454, 9489, 15)

#Kartta: MK_A_617
#RetrieveRangeOfTiles("MK_A_617", 18742, 18767, 9426, 9460, 15)

#Karttalehti 618
#RetrieveRangeOfTiles("MK_A_618", 18750, 18775, 9457, 9491, 15)

#Karttalehti 619
#RetrieveRangeOfTiles("MK_A_619", 18726, 18751, 9440, 9473, 15)

#Karttalehti 620
#RetrieveRangeOfTiles("MK_A_620", 18724, 18758, 9468, 9492, 15)

#Karttalehti 621
#RetrieveRangeOfTiles("MK_A_621", 18708, 18733, 9466, 9500, 15)

#Karttalehti 622
#RetrieveRangeOfTiles("MK_A_622", 18706, 18730, 9445, 9479, 15)

#Karttalehti 623
#RetrieveRangeOfTiles("MK_A_623", 18685, 18710, 9466, 9500, 15)

#Karttalehti 624
#RetrieveRangeOfTiles("MK_A_624", 18684, 18718, 9495, 9520, 15)

#Karttalehti 625
#RetrieveRangeOfTiles("MK_A_625", 18663, 18688, 9468, 9502, 15)

#Karttalehti 626
#RetrieveRangeOfTiles("MK_A_626", 18642, 18667, 9477, 9511, 15)

#Karttalehti 627
#RetrieveRangeOfTiles("MK_A_627", 18625, 18649, 9481, 9515, 15)

#Karttalehti 628
#RetrieveRangeOfTiles("MK_A_628", 18623, 18658, 9507, 9532, 15)





