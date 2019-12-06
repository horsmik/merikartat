from  tkinter import *
from urllib.request import urlopen
import io
import base64
import os.path
from os import path
from urllib import request
import threading
from concurrent.futures import ThreadPoolExecutor
import multiprocessing


## Tama on kaikkea muuta kuin kaunis ohjelma :)
## iteratiivisesti leikin tkinter kirjastolla ja softan kehittaminen pysahtyi,
## kun sain alkuperaisen toiminnalisen tavoitteen jotenkin toimimaan

## Kaytannossa talle voi antaa parametrina karttasarjan tiilinumeron ja sita kautta yrittaa loytaa
## aineiston kulmatiilia tms. Liikuminen nuolinappaimilla.

## Esim:
## python find_tile.py A 15 18657 9496

## Paikkaa voi myos etsia vaikka talla: https://openlayers.org/en/latest/examples/canvas-tiles.html

def close(event):
    master.withdraw() # if you want to bring it back
    sys.exit() # if you want to exit the entire thing

def leftKey(event):
    global C_data
    C_Data[2] = C_Data[2]-1
    haeTiilet(*C_Data)
    updateGridPictures(C_Data[1], C_Data[2], C_Data[3])

def rightKey(event):
    global C_Data
    C_Data[2] = C_Data[2]+1
    haeTiilet(*C_Data)
    updateGridPictures(C_Data[1], C_Data[2], C_Data[3])
    
def upKey(event):
    global C_Data
    C_Data[3] = C_Data[3]-1
    haeTiilet(*C_Data)
    updateGridPictures(C_Data[1], C_Data[2], C_Data[3])


def downKey(event):
    global C_Data
    C_Data[3] = C_Data[3]+1
    haeTiilet(*C_Data)
    updateGridPictures(C_Data[1], C_Data[2], C_Data[3])


def urlTiili(mapData, zoom, x_tiili, y_tiili):
    image_url="https://julkinen.vayla.fi/rasteripalvelu/service/wmts?request=GetTile&version=1.0.0&service=wmts&layer="+str(mapData)+"&TILEMATRIXSET=WGS84_Pseudo-Mercator&TileMatrix=WGS84_Pseudo-Mercator:"+str(zoom)+"&tilerow="+str(y_tiili)+"&tilecol="+str(x_tiili)+"&format=image/png&style=default"
    #print(image_url)
    return (image_url)

def start_point():
  if (len(sys.argv)) != 5:
    print("Anna parametrit A/B/C/D/RK/YK250/SK  zoom x_tiili y_tiili")
    print("Esimerkiksi:")
    print("python find_tile.py A 15 18657 9496")
    print("...avaa A-karttasarjan Harmajan majakan kohdalta")
    print("Mistä sitten voit liikkua eri suuntiin nuolinäppäimillä")
    exit()

  kartta = sys.argv[1]
  zoom = int(sys.argv[2])
  x_tiili = int(sys.argv[3])
  y_tiili = int(sys.argv[4])

  if kartta == "A":
    #print("A")
    mapData = "liikennevirasto:Merikarttasarja%20A%20public"
  elif kartta == "B":
    #print("B")
    mapData = "liikennevirasto:Merikarttasarja%20B"
  if kartta == "C":
    #print("C")
    mapData = "liikennevirasto:Merikarttasarja%20C%20public"
  elif kartta == "D":
    #print("D")
    mapData = "liikennevirasto:Merikarttasarja%20D"
  elif kartta == "RK":
    #print("RK")
    mapData = "liikennevirasto:Rannikkokartat%20public"
  elif kartta == "YK250":
    #print("YK250")
    mapData = "liikennevirasto:Yleiskartat%20250k%20public"
  elif kartta=="SK":
    mapData="liikennevirasto:Satamakartat"
  return[mapData, zoom, x_tiili, y_tiili]
  #return from StartPoint()

def download_group_of_tiles(listOfTiles):
    #images = client.get_album_images(album_id)
    #print("Lahdetaan hakemaan puuttuvia karttoja")
    with ThreadPoolExecutor(max_workers=9) as executor:
        executor.map(Download_Tile, listOfTiles)
    #print("Valmista...")

def Download_Tile(link):
  retryAttemptsRemaining = 15
  #Poimitaan tiilien mumerot ja zoom-taso http-kutsusta
  filename_x = link.split('tilecol=')[1].split('&')[0]
  filename_y = link.split('tilerow=')[1].split('&')[0]
  filename_z = link.split('WGS84_Pseudo-Mercator:')[1].split('&')[0]
  #print("WMTS_"+filename_z+"_"+filename_x+"_"+filename_y+".png")
  while retryAttemptsRemaining > 0:
    try:
      ##Get one tile from wmts and save bitmap as WMTS_zoom_x_y.png
      request.urlretrieve(link, "WMTS_"+filename_z+"_"+filename_x+"_"+filename_y+".png")
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


 
def haeTiilet(mapData, zoom, x_tiili, y_tiili):  
    #print('WMTS_'+str(zoom)+'_'+str(x_tiili)+'_'+str(y_tiili)+'.png')
    listOfTiles=[]
    if path.exists('WMTS_'+str(zoom)+'_'+str(x_tiili)+'_'+str(y_tiili)+'.png') == False:
        #print("Center: file not found, need to get from api"+str(x_tiili)+" "+str(y_tiili))
        listOfTiles.append(urlTiili(mapData, zoom, x_tiili, y_tiili))
    if  path.exists('WMTS_'+str(zoom)+'_'+str(x_tiili)+'_'+str(y_tiili-1)+'.png') == False:
        #print("N: file not found, need to get from api"+str(x_tiili)+" "+str(y_tiili-1))
        listOfTiles.append(urlTiili(mapData, zoom, x_tiili, y_tiili-1))
    if  path.exists('WMTS_'+str(zoom)+'_'+str(x_tiili+1)+'_'+str(y_tiili-1)+'.png') == False:
        #print("NE: file not found, need to get from api"+str(x_tiili+1)+" "+str(y_tiili-1))
        listOfTiles.append(urlTiili(mapData, zoom, x_tiili+1, y_tiili-1))
    if  path.exists('WMTS_'+str(zoom)+'_'+str(x_tiili+1)+'_'+str(y_tiili)+'.png') == False:
        #print("E: file not found, need to get from api"+str(x_tiili+1)+" "+str(y_tiili))
        listOfTiles.append(urlTiili(mapData, zoom, x_tiili+1, y_tiili))
    if  path.exists('WMTS_'+str(zoom)+'_'+str(x_tiili+1)+'_'+str(y_tiili+1)+'.png') == False:
        #print("SE: file not found, need to get from api"+str(x_tiili+1)+" "+str(y_tiili+1))
        listOfTiles.append(urlTiili(mapData, zoom, x_tiili+1, y_tiili+1))
    if  path.exists('WMTS_'+str(zoom)+'_'+str(x_tiili)+'_'+str(y_tiili+1)+'.png') == False:
        #print("S: file not found, need to get from api"+str(x_tiili)+" "+str(y_tiili+1))
        listOfTiles.append(urlTiili(mapData, zoom, x_tiili, y_tiili+1))
    if  path.exists('WMTS_'+str(zoom)+'_'+str(x_tiili-1)+'_'+str(y_tiili+1)+'.png') == False:
        #print("SW: file not found, need to get from api"+str(x_tiili-1)+" "+str(y_tiili+1))
        listOfTiles.append(urlTiili(mapData, zoom, x_tiili-1, y_tiili+1))
    if  path.exists('WMTS_'+str(zoom)+'_'+str(x_tiili-1)+'_'+str(y_tiili)+'.png') == False:
        #print("W: file not found, need to get from api"+str(x_tiili-1)+" "+str(y_tiili))
        listOfTiles.append(urlTiili(mapData, zoom, x_tiili-1, y_tiili))
    if  path.exists('WMTS_'+str(zoom)+'_'+str(x_tiili-1)+'_'+str(y_tiili-1)+'.png') == False:
        #print("NW: file not found, need to get from api"+str(x_tiili-1)+" "+str(y_tiili-1))
        listOfTiles.append(urlTiili(mapData, zoom, x_tiili-1, y_tiili-1))
#    print("Lista urleista")
#    print(listOfTiles)
#    print(len(listOfTiles))
    if len(listOfTiles) > 0:
        download_group_of_tiles(listOfTiles)
        


def updateGridPictures(zoom, x_tiili, y_tiili):
#    adding image (remember image should be PNG and not JPG) 
#    print("updateGrid-aliohjelma")
    #img_C.configure(file = r"WMTS_"+str(zoom)+"_"+str(x_tiili-1)+"_"+str(y_tiili-1)+".png")
    img_NW = PhotoImage(file = r"WMTS_"+str(zoom)+"_"+str(x_tiili-1)+"_"+str(y_tiili-1)+".png") 
    img_N = PhotoImage(file = r"WMTS_"+str(zoom)+"_"+str(x_tiili)+"_"+str(y_tiili-1)+".png") 
    img_NE = PhotoImage(file = r"WMTS_"+str(zoom)+"_"+str(x_tiili+1)+"_"+str(y_tiili-1)+".png") 
    img_W = PhotoImage(file = r"WMTS_"+str(zoom)+"_"+str(x_tiili-1)+"_"+str(y_tiili)+".png") 
    img_C = PhotoImage(file = r"WMTS_"+str(zoom)+"_"+str(x_tiili)+"_"+str(y_tiili)+".png") 
    img_E = PhotoImage(file = r"WMTS_"+str(zoom)+"_"+str(x_tiili+1)+"_"+str(y_tiili)+".png") 
    img_SW = PhotoImage(file = r"WMTS_"+str(zoom)+"_"+str(x_tiili-1)+"_"+str(y_tiili+1)+".png") 
    img_S = PhotoImage(file = r"WMTS_"+str(zoom)+"_"+str(x_tiili)+"_"+str(y_tiili+1)+".png") 
    img_SE = PhotoImage(file = r"WMTS_"+str(zoom)+"_"+str(x_tiili+1)+"_"+str(y_tiili+1)+".png") 
      
    # setting image with the help of label 
    Label(master, image = img_NW, text = "x:"+str(x_tiili-1)+" y:"+str(y_tiili-1), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 0, column = 0)
    Label(master, image = img_N, text = "x:"+str(x_tiili)+" y:"+str(y_tiili-1), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 0, column = 1)
    Label(master, image = img_NE, text = "x:"+str(x_tiili+1)+" y:"+str(y_tiili-1), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 0, column = 2)
    Label(master, image = img_W, text = "x:"+str(x_tiili-1)+" y:"+str(y_tiili), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 1, column = 0)
    Label(master, image = img_C, text = "x:"+str(x_tiili)+" y:"+str(y_tiili), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 1, column = 1)
    Label(master, image = img_E, text = "x:"+str(x_tiili+1)+" y:"+str(y_tiili), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 1, column = 2)
    Label(master, image = img_SW, text = "x:"+str(x_tiili-1)+" y:"+str(y_tiili+1), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 2, column = 0)
    Label(master, image = img_S, text = "x:"+str(x_tiili)+" y:"+str(y_tiili+1), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 2, column = 1)
    Label(master, image = img_SE, text = "x:"+str(x_tiili+1)+" y:"+str(y_tiili+1), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 2, column = 2)
    grid()


C_Data = start_point()


haeTiilet(*C_Data)



master = Tk()
master.title("Use arrow keys to move. <Esc> or <q> to exit.") 

middleTileUrl = urlTiili(*start_point())

#print(C_Data[2]) #X_TILE 18000 left right
#print(C_Data[3]) #Y_TILE 9500 up down



# adding image 
img_NW = PhotoImage(file = r"WMTS_"+str(C_Data[1])+"_"+str(C_Data[2]-1)+"_"+str(C_Data[3]-1)+".png") 
img_N = PhotoImage(file = r"WMTS_"+str(C_Data[1])+"_"+str(C_Data[2])+"_"+str(C_Data[3]-1)+".png") 
img_NE = PhotoImage(file = r"WMTS_"+str(C_Data[1])+"_"+str(C_Data[2]+1)+"_"+str(C_Data[3]-1)+".png") 
img_W = PhotoImage(file = r"WMTS_"+str(C_Data[1])+"_"+str(C_Data[2]-1)+"_"+str(C_Data[3])+".png") 
img_C = PhotoImage(file = r"WMTS_"+str(C_Data[1])+"_"+str(C_Data[2])+"_"+str(C_Data[3])+".png") 
img_E = PhotoImage(file = r"WMTS_"+str(C_Data[1])+"_"+str(C_Data[2]+1)+"_"+str(C_Data[3])+".png") 
img_SW = PhotoImage(file = r"WMTS_"+str(C_Data[1])+"_"+str(C_Data[2]-1)+"_"+str(C_Data[3]+1)+".png") 
img_S = PhotoImage(file = r"WMTS_"+str(C_Data[1])+"_"+str(C_Data[2])+"_"+str(C_Data[3]+1)+".png") 
img_SE = PhotoImage(file = r"WMTS_"+str(C_Data[1])+"_"+str(C_Data[2]+1)+"_"+str(C_Data[3]+1)+".png") 
 
 

# setting image with the help of label 
Label(master, image = img_NW, text = "x:"+str(C_Data[2]-1)+" y:"+str(C_Data[3]-1), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 0, column = 0)
Label(master, image = img_N, text = "x:"+str(C_Data[2])+" y:"+str(C_Data[3]-1), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 0, column = 1)
Label(master, image = img_NE, text = "x:"+str(C_Data[2]+1)+" y:"+str(C_Data[3]-1), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 0, column = 2)
Label(master, image = img_W, text = "x:"+str(C_Data[2]-1)+" y:"+str(C_Data[3]), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 1, column = 0)
Label(master, image = img_C, text = "x:"+str(C_Data[2])+" y:"+str(C_Data[3]), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 1, column = 1)
Label(master, image = img_E, text = "x:"+str(C_Data[2]+1)+" y:"+str(C_Data[3]), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 1, column = 2)
Label(master, image = img_SW, text = "x:"+str(C_Data[2]-1)+" y:"+str(C_Data[3]+1), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 2, column = 0)
Label(master, image = img_S, text = "x:"+str(C_Data[2])+" y:"+str(C_Data[3]+1), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 2, column = 1)
Label(master, image = img_SE, text = "x:"+str(C_Data[2]+1)+" y:"+str(C_Data[3]+1), font=('Helvetica 24 bold'), fg="red", compound = "center", bg="black").grid(row = 2, column = 2)
  
  
# infinite loop which can be terminated  
# by keyboard or mouse interrupt 

master.bind('<Left>', leftKey)
master.bind('<Right>', rightKey)
master.bind('<Up>', upKey)
master.bind('<Down>', downKey)
master.bind('<Escape>', close)
master.bind('q', close)

mainloop() 