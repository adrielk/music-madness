# -*- coding: utf-8 -*-
"""
MP3 Player
Created on Fri Jan  3 16:25:41 2020

@author: thead
"""
"""to Do"""
#biased randomization(DONE,but room for improvement)
"""
    Algo:
        all start iwth bias of 1
        When played, bias is 0.
        Randomization is done by sum of all indices (length of songlist)
        keep summing along list until sum > randomized value. Ending index is chosen song
        
        bias of previously played songs (bias<1) are increment by 0.1(or whatever value)
    
"""
#Add a back button...! (DONE)
#Database: allow users to create their own playlists in desired order (using SQLite or something?)
#use regex to neaten up titles...
#automated classification of songs
#liked songs + ML!
#automated removal of non-music parts of video
#stream music to server so I can listen to it on my phone!

#FUTURE IDEA: Scraping youtube to find random MP3 music videos. downloading from youtube and onto music selection! (need a database for this?)
    #start with MP3 video converter (takes in list of youtube links)
import pygame
import tkinter as tkr
import threading
import os #allows us to read and print out stuff in a folder
import random
import time

"""Playlist Register"""
#chdir = change directory
os.chdir(r"C:\Users\thead\Desktop\MusicPlayer\Songs")#changes your current directory!
songList = os.listdir()
songListDict = {i:1 for i in songList}
#print(os.getcwd()) this is file path

"""Pygame Inits"""
pygame.init()
pygame.mixer.init()
"""Variables"""
threadAlive = True
isPaused = False
isLooped = False
isShuffled = False
isOrdered = False
songsHistory = []
songsForward = []
#for bias randomization
biasInc = 0.05
#customization
primaryColor = "SpringGreen2"
accentColor = "grey17"
#stat records
songsPlayed = []
startTime = time.time()
#songEnd event set up
SONG_END = pygame.USEREVENT+1

#Action events and functions

def CheckSongEndedThread(name):
    while True:
        if threadAlive:
            for event in pygame.event.get():
                if event.type == 25:
                    SongEnded()
        else:
            break

def SongEnded():
    #history for purposes of back functionality
    if not playList.get(tkr.ACTIVE) in songsHistory:
        songsHistory.append(playList.get(tkr.ACTIVE))
        
    if isLooped == True:
        Play()
        print("Looped")
    elif isShuffled == True:
        print("Shuffled")
        PickRandomSong()
        Play()
    elif isOrdered == True:
        PickNextSong()
        Play()
        print("Ordered")
    else:
        print("DONE")
    print("SONG ENDED")
        
def ResetToggleControls(beingToggled):
    global isLooped, isShuffled, isOrdered
    
    isLooped = False if beingToggled != "LoopedTog" else isLooped
    isShuffled = False if beingToggled != "ShuffledTog" else isShuffled
    isOrdered = False if beingToggled != "OrderedTog" else isOrdered

    if isLooped == False:    
        loopVar.set("Loop")
    if isShuffled == False:
        shuffledTxt.set("Shuffle")
    if isOrdered == False:
        orderTxt.set("Order")

def ToggleLooped():
    ResetToggleControls("LoopedTog")
    global isLooped
    if isLooped == False:
        isLooped = True
        loopVar.set("UnLoop")

    else:
        isLooped = False
        loopVar.set("Loop")

def ToggleShuffled():
    ResetToggleControls("ShuffledTog")
    global isShuffled
    if isShuffled ==False:
        isShuffled = True
        shuffledTxt.set("UnShuffle")
    else:
        isShuffled = False
        shuffledTxt.set("Shuffle")
    
def ToggleOrdered():
    ResetToggleControls("OrderedTog")
    global isOrdered
    if isOrdered == False:
        isOrdered = True
        orderTxt.set("UnOrder")
    else:
        isOrdered =False
        orderTxt.set("Order")
    
def UpdateVolume(vol):
    convertedVol = float(int(vol)/100)
    pygame.mixer.music.set_volume(convertedVol)

def UpdateTitle():
    var.set(playList.get(tkr.ACTIVE)[0:playList.get(tkr.ACTIVE).index(".mp3")])

def Pause():
    global isPaused
    if isPaused == False:
        isPaused = True
        pauseTxt.set("Unpause")
        pygame.mixer.music.pause()
    else:
        isPaused = False
        pauseTxt.set("Pause")
        pygame.mixer.music.unpause()  
        
def Play():
    queuedSong = playList.get(tkr.ACTIVE)
    if not queuedSong in songsPlayed:
        songsPlayed.append(queuedSong)
    
    UpdateTitle()
    pygame.mixer.music.set_endevent(SONG_END)
    pygame.mixer.music.load(queuedSong)
    pygame.mixer.music.play()
    print(queuedSong)
    
#incrementing bias increases chances for a song being chosen
def IncrementBias():
    global songListDict
    global biasInc
    for k in songListDict.keys():
        #if songListDict[k]<1:
        songListDict[k] += biasInc

def PickRandomSong():
    itemSum = 0
    randSongIndex = 0
    totalBias = 0
    
    IncrementBias()#This increments bias of songs in songListDict. Thus, allowing songs with <1 bias to recover their chance of being chosen
    currentSong = playList.get(tkr.ACTIVE)
    songListDict[currentSong] = 0
    for i in songListDict.values():
        totalBias+=i
    
    randSongNum = random.uniform(0,len(songList))
    
    for i in songListDict.values():
        itemSum+=i
        if itemSum > randSongNum:
            break
        randSongIndex +=1
#    print(itemSum)
    print(randSongIndex)
#    print(totalBias)
    playList.activate(randSongIndex)
   # playList.activate(random.randint(0,len(songList)))
   
def PlayForwardSong():
    #if no more forward, then it just stops song to trigger next song
    if len(songsForward)>0:
        forSong = songsForward.pop()
        
        songsHistory.append(playList.get(tkr.ACTIVE))
        
        playList.activate(songList.index(forSong))
        Play()
    else:
        ExitPlayer()
    print("From Forward Song FUNCTION: Song forward stack: ",songsForward)
    print("Song history:", songsHistory)
        
        
def PlayPreviousSong():
    if len(songsHistory)>0:
        prevSong = songsHistory.pop()
        
        songsForward.append(playList.get(tkr.ACTIVE))
        
        playList.activate(songList.index(prevSong))
        Play()
    print("From Previous Song FUNCTION: Song history:", songsHistory)
    print("Song forward stack: ",songsForward)

    

def PickNextSong():
    playList.activate((songList.index(playList.get(tkr.ACTIVE))+1)%len(songList))

def ExitPlayer():
    pygame.mixer.music.stop()    

def OnExit():#stops all processes when window is closed
    global threadAlive
    global startTime
    timeElapsed = time.time()-startTime
    
    print("Length: %d" %(len(songsPlayed)),"; Songs Played: ",songsPlayed)
    print("Listening time: %.2f seconds or %.2f minutes" %(timeElapsed, timeElapsed/60))
    
    ExitPlayer()
    player.destroy()
    threadAlive = False
            
            
"""Basic set up"""
player = tkr.Tk()
player.title("Adriel's Music Player")
player.geometry("800x430")

"""Creating buttons"""

#Text Varaibles
loopVar = tkr.StringVar()
loopVar.set("Loop")
pauseTxt = tkr.StringVar()
pauseTxt.set("Pause")
shuffledTxt = tkr.StringVar()
shuffledTxt.set("Shuffle")
orderTxt = tkr.StringVar()
orderTxt.set("Order")


stopControlFrame = tkr.Frame(player,width=5,height = 2)
playB = tkr.Button(player,width=5,height = 2, text = "Play", command = Play,activebackground = "SpringGreen3",font = ("Helvetica",15),background = primaryColor)
stopB = tkr.Button(stopControlFrame,height = 1 ,text = "Stop", command = ExitPlayer, activebackground = "red",font = ("Helvetica",15),background = primaryColor)
pauseB = tkr.Button(stopControlFrame,height = 1 ,textvariable = pauseTxt, command = Pause,font = ("Helvetica",15),background = primaryColor)
"""Frame for loop, shuffle, or sequential control options"""
controlFrame = tkr.Frame(player)

backB = tkr.Button(controlFrame,height =1, text = "Back",command = PlayPreviousSong ,font = ("Helvetica",15),background = accentColor, fg = primaryColor)
loopB = tkr.Button(controlFrame,height = 1,textvariable = loopVar, command = ToggleLooped,font = ("Helvetica",15),background = primaryColor)
shuffleB = tkr.Button(controlFrame,height = 1,textvariable = shuffledTxt, command = ToggleShuffled,font = ("Helvetica",15),background = primaryColor)
seqB = tkr.Button(controlFrame, height = 1,textvariable = orderTxt, command = ToggleOrdered,font = ("Helvetica",15),background = primaryColor)
forB = tkr.Button(controlFrame,height =1, text = "Forward",command = PlayForwardSong ,font = ("Helvetica",15),background = accentColor, fg = primaryColor)

"""Volume control"""
volScale = tkr.Scale(player,from_ = 0, to_= 100,
                     orient = tkr.HORIZONTAL,resolution = 1, command = UpdateVolume,troughcolor = primaryColor, background = accentColor, fg = "white")
volScale.set(50)
UpdateVolume(volScale.get())

"""PlayList"""
playList = tkr.Listbox(player, highlightcolor = "blue",selectmode = tkr.SINGLE,font = ("Helvetica",11),background = accentColor,fg = "white")#restricts to only ONE selections
for pos in range(0,len(songList)):
    playList.insert(pos,songList[pos])
    
"""Title"""
#by using text variable, can be changed without recreating title!
var = tkr.StringVar()
songtitle = tkr.Label(player, height = 1, textvariable= var,font = ("Helvetica",20),background = accentColor, fg= "white")

#place widgets: order matters!
songtitle.pack(fill = "x")
playB.pack(fill = "x")
stopControlFrame.pack(fill = "x")
pauseB.pack(side ="left", fill = "both",expand = "YES")
stopB.pack(side ="left", fill = "both",expand = "YES")    
controlFrame.pack(fill = "x")

#control butotns
backB.pack(side = "left", fill = "both", expand = "YES")
loopB.pack(side ="left", fill = "both",expand = "YES")
shuffleB.pack(side = "left", fill = "both", expand = "YES")
seqB.pack(side = "left", fill = "both", expand = "YES")
forB.pack(side = "left", fill = "both", expand = "YES")
volScale.pack(fill = "x")
playList.pack(fill = "x")

"""Music player event handling"""
#Threading setup:
eventThread = threading.Thread(target = CheckSongEndedThread, args=(1,))
eventThread.start()

#Activate:
player.protocol("WM_DELETE_WINDOW", OnExit)
player.mainloop()
player.attributes("-topmost", True)

































