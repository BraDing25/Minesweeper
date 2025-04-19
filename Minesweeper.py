import os
import pygame as pg
import random
import tkinter as tk
from tkinter import ttk
import numpy as np

os.environ['SDL_VIDEO_CENTERED'] = '1'
#---------------------------------- Gamemode Selection Popup ----------------------------------------------------
def startUp():
    #Setting up the window to be prompted
    gamemode = tk.Tk()
    gamemode.title("Gamemode")
    gamemode.minsize(600,200)
    gamemode.resizable(False,False)
    #Variables to link with Radiobuttons
    ss = tk.IntVar()
    sd = tk.IntVar()
    ss.set(1)
    sd.set(1)
    #First region of window that asks for board size
    frameA = ttk.Frame()
    ttk.Label(frameA,width=50,text="").grid(column=0,row=0,columnspan=3)
    ttk.Label(frameA,text="Select Board Size",justify="center").grid(column=0,row=0,columnspan=3)

    tk.Radiobutton(frameA, text = "Small", variable = ss, value = 1).grid(column=0,row=1)
    tk.Radiobutton(frameA, text = "Medium", variable = ss, value = 2).grid(column=1,row=1)
    tk.Radiobutton(frameA, text = "Large", variable = ss, value = 3).grid(column=2,row=1)
    #Second region of window that asks for game difficulty
    frameB = ttk.Frame()
    ttk.Label(frameB,width=50,text="").grid(column=0,row=0,columnspan=3)
    ttk.Label(frameB,text="Select Difficulty",justify="center").grid(column=0,row=0,columnspan=3)

    tk.Radiobutton(frameB, text = "Easy", variable = sd, value = 1).grid(column=0,row=1)
    tk.Radiobutton(frameB, text = "Medium", variable = sd, value = 2).grid(column=1,row=1)
    tk.Radiobutton(frameB, text = "Hard", variable = sd, value = 3).grid(column=2,row=1)
    #Function that closes window and assigns values based on input
    def close():
        global size
        global dif

        size = 0
        dif = 0

        match ss.get():
            case 1:
                size = 10
            case 2:
                size = 20
            case 3:
                size = 25

        match sd.get():
            case 1:
                dif = 15
            case 2:
                dif = 25
            case 3:
                dif = 35

        gamemode.destroy()
    #Last region of window with button to close
    frameC = ttk.Frame()
    tk.Button(frameC,text="Done",bg="red",fg="white",command=close,width=15).pack()
    #Places the frames
    frameA.grid(column=0,row=0,padx=5,pady=50,sticky='n')
    frameB.grid(column=1,row=0,padx=5,pady=50,sticky='n')
    frameC.grid(column=0,row=1,columnspan=2,sticky='n')

    gamemode.eval('tk::PlaceWindow . center')

    gamemode.mainloop()

#-------------------------------------- Sprite Object Classes ----------------------------------------------------------
pg.init()
unitsTexture = pg.image.load(os.path.dirname(os.path.abspath(__file__))+"\minesweeper.png") #base .png with all textures
#Default Box object
class Box:
    def __init__(self):
        self.visible = False
        self.number = 0
        self.flag = False
        self.pos = pg.Vector2(0,0)
        
        handle_surface = unitsTexture.copy()
        self.defRect = pg.Rect(0,32,16,16) #Default texture as empty space
        handle_surface.set_clip(self.defRect)
        self.image = unitsTexture.subsurface(handle_surface.get_clip()).copy()
#Default Bomb object
class Bomb:
    def __init__(self):
        self.visible = False
        self.flag = False
        self.pos = pg.Vector2(0,0)
        self.number = 9999

        handle_surface = unitsTexture.copy()
        self.defRect = pg.Rect(32,32,16,16) #Default texture as bomb
        handle_surface.set_clip(self.defRect)
        self.image = unitsTexture.subsurface(handle_surface.get_clip()).copy()
       
#------------------------------------------- Game Function -------------------------------------------------------------

class Game():
    def __init__(self):
        #Set up game window
        worldsize = pg.math.Vector2(800,800)
        self.worldsize = worldsize
        self.window = pg.display.set_mode(worldsize)
        self.cellSize = pg.math.Vector2((800/size),(800/size))

        icon = pg.image.load(os.path.dirname(os.path.abspath(__file__))+"\icon.png")
        pg.display.set_caption("Minesweeper")
        pg.display.set_icon(icon)
        #Empty object array to store data
        self.sprites = np.zeros(shape=(size,size),dtype=np.object_)
        #Variables to count total state of all cells
        self.bombCount = 0
        self.boxCount = 0
        self.openCount = 0
        self.closedCount = 0
        #Randomly creates and places either boxes or objects based on game difficulty
        for i in range(0,size):
            for j in range(0,size):
                n = random.randint(0,100)
                if n <= dif:
                    bomb = Bomb()
                    self.sprites[i][j] = bomb
                    self.bombCount += 1
                    placePoint = pg.math.Vector2(self.cellSize.x*i,self.cellSize.y*j)
                    bomb.pos = placePoint
                    sprite = pg.transform.scale(bomb.image,self.cellSize)
                    self.window.blit(sprite,placePoint)
                else:
                    box = Box()
                    self.sprites[i][j] = box
                    self.boxCount += 1
                    placePoint = pg.math.Vector2(self.cellSize.x*i,self.cellSize.y*j)
                    box.pos = placePoint
                    sprite = pg.transform.scale(box.image,self.cellSize)
                    self.window.blit(sprite,placePoint)
        #Goes over every cell to determine how many bombs surround each box
        for i in range(0,size):
            for j in range(0,size):
                if isinstance(self.sprites[i][j], Bomb) == True:
                    pass
                else:
                    n = 0
                    bound = len(self.sprites) - 1
                    if ((i-1)>=0 and (j-1)>=0 and (i-1)<=bound and (j-1)<=bound):
                        if isinstance(self.sprites[i-1][j-1],Bomb) == True:
                            n += 1
                    if ((j-1)>=0 and (j-1)<=bound):
                        if isinstance(self.sprites[i][j-1],Bomb)==True:
                            n += 1
                    if ((i+1)>=0 and (j-1)>=0 and (i+1)<=bound and (j-1)<=bound):
                        if isinstance(self.sprites[i+1][j-1],Bomb)==True:
                            n += 1
                    if ((i-1)>=0 and (i-1)<=bound):
                        if isinstance(self.sprites[i-1][j],Bomb)==True:
                            n += 1
                    if ((i+1)>=0 and (i+1)<=bound):
                        if isinstance(self.sprites[i+1][j],Bomb)==True:
                            n += 1
                    if ((i-1)>=0 and (j+1)>=0 and (i-1)<=bound and (j+1)<=bound):
                        if isinstance(self.sprites[i-1][j+1],Bomb)==True:
                            n += 1
                    if ((j+1)>=0 and (j+1)<=bound):
                        if isinstance(self.sprites[i][j+1],Bomb)==True:
                            n += 1
                    if ((i+1)>=0 and (j+1)>=0 and (i+1)<=bound and (j+1)<=bound):
                        if isinstance(self.sprites[i+1][j+1],Bomb)==True:
                            n += 1
                    #Changes default box image to match number of surrounding bombs
                    match n:
                        case 0:
                            pass
                        case 1:
                            self.sprites[i][j].defRect = pg.Rect(0,0,16,16)
                            self.sprites[i][j].number = n
                        case 2:
                            self.sprites[i][j].defRect = pg.Rect(16,0,16,16)
                            self.sprites[i][j].number = n
                        case 3:
                            self.sprites[i][j].defRect = pg.Rect(32,0,16,16)
                            self.sprites[i][j].number = n
                        case 4:
                            self.sprites[i][j].defRect = pg.Rect(48,0,16,16)
                            self.sprites[i][j].number = n
                        case 5:
                            self.sprites[i][j].defRect = pg.Rect(0,16,16,16)
                            self.sprites[i][j].number = n
                        case 6:
                            self.sprites[i][j].defRect = pg.Rect(16,16,16,16)
                            self.sprites[i][j].number = n
                        case 7:
                            self.sprites[i][j].defRect = pg.Rect(32,16,16,16)
                            self.sprites[i][j].number = n
                        case 8:
                            self.sprites[i][j].defRect = pg.Rect(48,16,16,16)
                            self.sprites[i][j].number = n

        self.clock = pg.time.Clock()
        self.state = "active"
        self.cursorPos = pg.Vector2(0,0)
        self.click = [False,False,False]
        self.running = True
    #Checks if input should quit game otherwise get mouse position and inputs
    def processInput(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                break
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    break
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.cursorPos = pg.mouse.get_pos()
                self.click = pg.mouse.get_pressed()
    #Updates state of objects based on inputs
    def update(self):
        if self.state == "active":    
            #Checks if all boxes are opened and no bombs are revealed
            if (self.closedCount == 0 and self.openCount == self.boxCount):
                self.state = "win"
            
            c = 0
            for i in range(0,size):
                for j in range(0,size):
                    obj = self.sprites[i][j]
                    #Counts total number of opened boxes
                    if obj.visible == True:
                        c += 1
                    if c > self.openCount:
                        self.openCount = c
                    #If a box has no bombs arround it, it openes all surrounding boxes
                    if (obj.number == 0 and obj.visible == True):
                        bound = len(self.sprites) - 1
                        if ((i-1)>=0 and (j-1)>=0 and (i-1)<=bound and (j-1)<=bound):
                            if isinstance(self.sprites[i-1][j-1],Box):
                                self.sprites[i-1][j-1].visible = True
                        if ((j-1)>=0 and (j-1)<=bound):
                            if isinstance(self.sprites[i][j-1],Box):
                                self.sprites[i][j-1].visible = True
                        if ((i+1)>=0 and (j-1)>=0 and (i+1)<=bound and (j-1)<=bound):
                            if isinstance(self.sprites[i+1][j-1],Box):
                                self.sprites[i+1][j-1].visible = True
                        if ((i-1)>=0 and (i-1)<=bound):
                            if isinstance(self.sprites[i-1][j],Box):
                                self.sprites[i-1][j].visible = True
                        if ((i+1)>=0 and (i+1)<=bound):
                            if isinstance(self.sprites[i+1][j],Box):
                                self.sprites[i+1][j].visible = True
                        if ((i-1)>=0 and (j+1)>=0 and (i-1)<=bound and (j+1)<=bound):
                            if isinstance(self.sprites[i-1][j+1],Box):
                                self.sprites[i-1][j+1].visible = True
                        if ((j+1)>=0 and (j+1)<=bound):
                            if isinstance(self.sprites[i][j+1],Box):
                                self.sprites[i][j+1].visible = True
                        if ((i+1)>=0 and (j+1)>=0 and (i+1)<=bound and (j+1)<=bound):
                            if isinstance(self.sprites[i+1][j+1],Box):
                                self.sprites[i+1][j+1].visible = True
                    #If the cursor is over a cell, do an action based on click
                    cell = [obj.pos[0],obj.pos[1],obj.pos[0]+self.cellSize[0]-1,obj.pos[1]+self.cellSize[0]-1]
                    if (cell[0] <= self.cursorPos[0] <= cell[2]) and (cell[1] <= self.cursorPos[1] <= cell[3]):
                        if self.click[0] == True: #Left click opens cell
                            obj.visible = True
                            if isinstance(obj, Bomb):
                                self.state = "lose"
                                self.closedCount +=1
                        if self.click[2] == True: #Right click flags cell
                            obj.flag = True
                        self.click = [False, False, False]

    def render(self):  
        for i in range(0,size):
            for j in range(0,size):
                obj = self.sprites[i][j]
                #If cell is flagged and not visible, update to flag texture
                if (obj.flag == True and obj.visible == False):
                    handle_surface = unitsTexture.copy()
                    areaRect = pg.Rect(48,32,16,16)
                    handle_surface.set_clip(areaRect)
                    obj.image = unitsTexture.subsurface(handle_surface.get_clip()).copy()
                        
                    placePoint = pg.math.Vector2(self.cellSize.x*i,self.cellSize.y*j)
                    sprite = pg.transform.scale(obj.image,self.cellSize)
                    self.window.blit(sprite,placePoint)
                #If cell is visible, update to default texture
                if obj.visible == True:
                    handle_surface = unitsTexture.copy()
                    areaRect = obj.defRect
                    handle_surface.set_clip(areaRect)
                    obj.image = unitsTexture.subsurface(handle_surface.get_clip()).copy()
                    
                    placePoint = pg.math.Vector2(self.cellSize.x*i,self.cellSize.y*j)
                    sprite = pg.transform.scale(obj.image,self.cellSize)
                    self.window.blit(sprite,placePoint)
                #If cell is not visible and not flagged, update to closed texture
                elif obj.flag == False:
                    handle_surface = unitsTexture.copy()
                    areaRect = pg.Rect(16,32,16,16)
                    handle_surface.set_clip(areaRect)
                    obj.image = unitsTexture.subsurface(handle_surface.get_clip()).copy()

                    placePoint = pg.math.Vector2(self.cellSize.x*i,self.cellSize.y*j)
                    sprite = pg.transform.scale(obj.image,self.cellSize)
                    self.window.blit(sprite,placePoint)
        #Show "Win" screen if win
        if self.state == "win":
            pg.draw.rect(self.window, (50,200,50), (300,300,200,100))
            myText = pg.font.SysFont("Calibri",45).render("YOU WIN!",False,(255,255,255))
            self.window.blit(myText,(310,330))
            pg.display.update()
            return
        #Show "Lose" screen if lose
        elif self.state == "lose":
            pg.draw.rect(self.window, (255,0,0), (300,300,200,100))
            myText = pg.font.SysFont("Calibri",45).render("YOU LOSE",False,(255,255,255))
            self.window.blit(myText,(310,330))
            pg.display.update()
            return

        pg.display.update() 

    def run(self):    
        while self.running:
            self.processInput()
            self.update()
            self.render()        
            self.clock.tick(60)

#---------- Run Game ----------------
startUp()

game = Game()
game.run()
