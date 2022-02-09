import os
import numpy as np
import matplotlib.pyplot as plt
import imageio as imgio


# Check whether images folder already exists or not
# the images are used to generate an animated gif with imageio
filePath = "./images" # file path for images
isExist = os.path.exists(filePath) # boolean variable to see if folder exists
if not isExist:
    # Create a new directory because it does not exist 
    os.makedirs(filePath)
    print("Generated images directory!")
else:
    # clear all previously generated images to avoid mixing
    for f in os.listdir(filePath):
        os.remove(os.path.join(filePath, f))
    print("Successfully removed previous images!")


dim=30
days=0 # initialize days to 0
earth=np.zeros((dim, dim),dtype=int) #creating an empty earth 
#Initally poulate earth 
earth[7:12,7:15]=1
newEarth=np.zeros((dim, dim),dtype=int) #creating an empty earth 
life=[]
for day in range(11):
    plt.savefig("./images/earth_day_"+str(day)+".png")
    plt.matshow(earth)
    newEarth=np.zeros((dim,dim),dtype=int) #creating
    for x in range(1,dim-1):
        for y in range(1,dim-1):
            alive=earth[x,y]==1
            neighborhood=earth[x-1:x+2,y-1:y+2]
            neighbors=neighborhood.sum()-earth[x,y]
            #Rule of life 
            #If cell has 0 or 1 neighbors
            if alive and neighbors<2:
                newEarth[x,y]=0 # die of lonliness
            #If cell has 2 or 3 neighbors,   
            if alive and (neighbors==2 or neighbors==3):
                newEarth[x,y]=1 # survive
            #If cells has 4 or more neighbors 
            if alive and neighbors>=4:
                newEarth[x,y]=0 # die of overcrowding
            #If cell has 3 neighbors 
            if not alive and neighbors==3: 
                newEarth[x,y]=1 # come back to life
                
    if np.alltrue(earth==newEarth): # checks if life didn't change change in a generation
        break
    earth=newEarth
    life.append(earth.sum())
    days = days + 1 # increment days by 1 after each generation
    
# Build GIF from generated images
with imgio.get_writer(('earth.gif'), mode='I', duration=0.1) as writer:
    for filename in os.listdir(filePath):
        if filename == "earth_day_0.png": # first image is always a blank image which causes a bug
            continue # skip first file
        image = imgio.imread(filePath+"/"+filename)
        writer.append_data(image)
    print("Gif successfully generated at " + os.path.abspath("./"))