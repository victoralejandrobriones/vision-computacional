import Tkinter
import Image, ImageTk
from sys import argv

file = argv[1]

im = Image.open(file).convert("RGB")
original = im
(x,y) = im.size

def b_and_w():
    for i in range(x):
        for j in range(y):
            (r,g,b)=original.getpixel((i, j))
            mini = max((r,g,b))
            if(mini<127):
                mini = 0
            else:
                mini = 255
            im.putpixel((i,j), (mini,mini,mini))

def grayscale():
    for i in range(x):
        for j in range(y):
            (r,g,b)=original.getpixel((i, j))
            mini = max((r,g,b))
            im.putpixel((i,j), (mini,mini,mini))

def blur():
    for i in range(x):
        for j in range(y):
            prom = []
            k=0
            (r,g,b)=original.getpixel((i, j))
            if(i-1>=0):
                (rn,gn,bn)=original.getpixel((i-1, j))
                prom.append(max((rn,gn,bn)))
                k+=1
            if(i+1<x):
                (rs,gs,bs)=original.getpixel((i+1, j))
                prom.append(max((rs,gs,bs)))
                k+=1
            if(j+1<y):
                (re,ge,be)=original.getpixel((i, j+1))
                prom.append(max((re,ge,be)))
                k+=1
            if(j-1>=0):
                (ro,go,bo)=original.getpixel((i, j-1))
                prom.append(max((re,ge,be)))
                k+=1
            promedio = 0;
            for valor in prom:
                promedio+=valor
            promedio=promedio/k
            im.putpixel((i,j), (promedio,promedio,promedio))
            
if(argv[2]=="BW"):
    b_and_w()
if(argv[2]=="G"):
    grayscale()
if(argv[2]=="B"):
    numero=0
    while numero!=int(argv[3]):
        blur()
        numero+=1
ventana = Tkinter.Tk()
im2 = ImageTk.PhotoImage(im)
Tkinter.Label(ventana, image=im2).pack()

ventana.mainloop()
