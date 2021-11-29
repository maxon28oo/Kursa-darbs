import tkinter as tk
import random
import time
from tkinter.constants import HORIZONTAL
import numpy as np


class Circle:
    def __init__(self, point, r):
        self.position = point
        self.r = r
        self.object = None

    def draw(self, canvas):
        x0 = self.position[0] - self.r
        y0 = self.position[1] - self.r
        x1 = self.position[0] + self.r
        y1 = self.position[1] + self.r
        self.object = canvas.create_oval(
            x0, y0, x1, y1, fill="red", outline="red")

    def set_target(self, point):
        self.target = point

    def move(self, x, y):
        self.position = (x, y)

    def onMe(self, x, y):
        x = self.position[0]-x
        y = self.position[1]-y
        return ((x**2+y**2) <= self.r**2)
        


class risowashka:
    def __init__(self):
        self.animspeed = 1
        self.dragging = False
        self.handeledbymouse = False
        self.app = tk.Tk()
        self.app.title("Kursa darbs")
        self.app.protocol("WM_DELETE_WINDOW", self.onClose)
        self.app.geometry("600x700")
        self.app.resizable(False, False)
        self.frame = tk.Frame(self.app)
        self.canvas = tk.Canvas(self.frame, width=600,
                                height=520, bg="#EEE3E0")
        self.canvas.grid(column=0,row=0)
        self.canvas.bind("<Button-1>", func=self.clicd)
        self.canvas.bind("<Motion>", func=self.drag)
        self.canvas.bind("<ButtonRelease-1>", func=self.rel)
        #self.frame.pack()
        self.frame.grid()
        #tk.Button(self.frame, text='Clear all', command=self.clear).pack(side=RIGHT)
        self.resbtn=tk.Button(self.frame, text='Clear all', command=self.clear)
        self.resbtn.grid(sticky="e")
        self.AnimBtn = tk.Button(self.frame, text='Stop animation',
                             command=self.ChangeAnimation)
        self.AnimBtn.grid()
        self.AnimSpeed_Text = tk.Label(self.frame,text="Animation speed")
        self.AnimSpeed_Text.grid(sticky='w')
        self.AnimSpeed_Slider = tk.Scale(self.frame,command=self.slider, from_=10, to=300, orient=HORIZONTAL)
        self.AnimSpeed_Slider.grid(sticky='w')
        self.AnimSpeed_Slider.set(100)
        self.AnimRst = tk.Button(self.frame, text='Reset speed', command=self.ResetAll)
        self.AnimRst.grid(sticky='wn')
        self.generate()
        self.animating = True
        self.anim()

    def ResetAll(self):
        self.animspeed=1
        self.AnimSpeed_Slider.set(100)
    def slider(self,smth):
        self.animspeed=int(smth)/100

    def onClose(self):
        self.animating = False
        self.app.destroy()

    def ChangeAnimation(self):
        if self.AnimBtn.cget('text') == 'Stop animation':
            self.AnimBtn.config(text='Play animation')
            self.animating = False
        else:
            self.AnimBtn.config(text='Stop animation')
            self.animating = True

    def anim(self):
        while (True):
            try:
                time.sleep(0.01)
                self.app.update()
                if (self.animating):
                    vec = np.array(self.circle.target) - \
                        np.array(self.circle.position)
                    vec = (vec/np.linalg.norm(vec))*self.animspeed
                    self.circle.position = np.array(self.circle.position)+vec
                    self.canvas.move(self.circle.object, *vec)
                    vec = np.array(self.current_traectory[2:])-np.array(self.current_traectory[:2])
                    t = (self.circle.position[0]+self.circle.position[1]-self.current_traectory[0] -self.current_traectory[1])/(vec[0]+vec[1])
                    if (t>=1):
                        self.circle.set_target(self.current_traectory[:2])
                    elif(t<=0):
                        self.circle.set_target(self.current_traectory[2:])
            except Exception as e:
                exit()

    def generate(self):
        self.current_traectory = [random.randrange(0, 600) if x % 2 == 0 else random.randrange(0, 520) for x in range(4)]
        self.circle = Circle(self.current_traectory[:2], 10)
        self.circle.set_target(self.current_traectory[2:])
        self.repaint()

    def movecircle(self, x, y):  # idial
        vec = np.array(self.current_traectory[2:])-np.array(self.current_traectory[:2])
        div = -(vec[0]**2)-(vec[1]**2)
        sim = vec[0]*x+vec[1]*y
        sim1 = vec[1]*self.current_traectory[0] - vec[0]*self.current_traectory[1]
        x = (-vec[0]*sim-vec[1]*sim1)/div
        y = (vec[0]*sim1-vec[1]*sim)/div
        t = (x+y-self.current_traectory[0] -self.current_traectory[1])/(vec[0]+vec[1])
        if (t > 0 and t < 1):
            self.circle.move(x, y)

    def drag(self, event):
        if (self.dragging):
            self.repaint()
            self.drawline(*self.startpos, event.x, event.y, "black")
        elif (self.handeledbymouse):
            self.movecircle(event.x, event.y)
            self.repaint()

    def clicd(self, event):
        if (self.circle.onMe(event.x, event.y) and self.current_traectory!=None):
            self.handeledbymouse = True
            if self.animating:
                self.ChangeAnimation()
        else:
            self.startpos = (event.x, event.y)
            self.dragging = True

    def repaint(self):
        self.canvas.delete("all")
        if (self.current_traectory != None):
            self.circle.draw(self.canvas)
            self.drawline(*self.current_traectory, "#7F7F7F")

    def rel(self, event):
        if self.dragging == True:
            self.resbtn.grid(sticky="e")
            self.AnimBtn.grid()
            self.AnimSpeed_Text.grid(sticky='w')
            self.AnimSpeed_Slider.grid(sticky='w')
            self.AnimRst.grid(sticky='wn')
            self.dragging = False
            self.current_traectory = (*self.startpos, event.x, event.y)
            self.circle.move(*self.startpos)
            self.circle.set_target((event.x, event.y))
            self.repaint()
            if not self.animating:
                self.ChangeAnimation()
        if (self.handeledbymouse):
            self.handeledbymouse = False

    def clear(self):#idial
        if (self.current_traectory!=None):
            self.canvas.delete("all")
            self.current_traectory = None
            if (self.animating):self.ChangeAnimation()
            self.AnimBtn.grid_forget()
            self.AnimSpeed_Slider.grid_forget()
            self.AnimSpeed_Text.grid_forget()
            self.resbtn.grid_forget()
            self.AnimRst.grid_forget()


    # Brezenhema metode lai uzzimētu liniju no (x0,y0) līdz (x1,y1) ar izvelēto krasu
    def drawline(self, x0, y0, x1, y1, color):
        dx, dy = abs(x1-x0), abs(y1-y0)
        xs = 1 if x1 > x0 else -1
        ys = 1 if y1 > y0 else -1
        x, y = x0, y0
        if (dx > dy):
            p = 2*dy-dx
            while (abs(x-x1) > 0):
                # Es izmantoju create_rectangle, jo idk kā normāli izmantot create_image to draw pixels:(
                self.canvas.create_rectangle(x, y, x, y, outline=color)
                if (p > 0):
                    y += ys
                    p += 2*dy-2*dx
                else:
                    p += 2*dy
                x += xs
        else:
            p = 2*dx-dy
            while (abs(y-y1) > 0):
                self.canvas.create_rectangle(x, y, x, y, outline=color)
                if (p > 0):
                    x += xs
                    p += 2*dx-2*dy
                else:
                    p += 2*dx
                y += ys


kavo = risowashka()
