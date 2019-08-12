import math
from urllib import request


##http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int(((lon_deg + 180.0) / 360.0) * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)+1
  return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

# Tahan alle voi laittaa kartalehden vasemman ylakulman ja oikean alakulman koordinaatit
# ohjelma laskee arvauksen vastaavasta karttatiilesta. Usein tuo menee oikein, mutta joskus voi joutua
# valitsemaan viereisen tiilen, mikali haluaa etta kulmatiili on paperisen kartan mukainen. 

#TOP LEFT
print("618")  # Tahan voi antaa karttalehden nimen
lat_degrees = 60
lat_minutes = 19.4

lon_degrees = 25
lon_minutes = 59.5

#BOTTOM RIGHT
lat_degrees2 = 60
lat_minutes2 = 8.1

lon_degrees2 = 26
lon_minutes2 = 16.2

print("TOP LEFT")
print(str(lat_degrees)+" "+str(lat_minutes)+"   "+str(lon_degrees)+" "+str(lon_minutes))
lat = lat_degrees + lat_minutes/60
print("Lat (y, row): "+str(lat))
lon = lon_degrees + lon_minutes/60
print("Lon (x, column): "+str(lon))
print(deg2num(lat, lon, 15))
print("*************")
print("BOTTOM LEFT")

print(str(lat_degrees2)+" "+str(lat_minutes2)+"   "+str(lon_degrees2)+" "+str(lon_minutes2))
lat2 = lat_degrees2 + lat_minutes2/60
print("Lat2 (y, row): "+str(lat2))
lon2 = lon_degrees2 + lon_minutes2/60
print("Lon2 (x, column): "+str(lon2))
print(deg2num(lat2, lon2, 15))

xmin, ymin = (deg2num(lat, lon, 15))
xmax, ymax = (deg2num(lat2, lon2, 15))

print("RetrieveRangeOfTiles(NIMI, "+str(xmin)+", "+str(xmax)+", "+str(ymin)+", "+str(ymax)+", 15)")
