import Tkinter 
import Image, ImageTk
from sys import argv

file = argv[1]

im = Image.open(file).convert("RGB")
(x,y) = im.size

for i in range(x):
    for j in range(y):
        (r,g,b)=im.getpixel((i, j))
        mini = min((r,g,b))
        im.putpixel((i,j), (mini,mini,mini))
ventana = Tkinter.Tk()
im2 = ImageTk.PhotoImage(im)

Tkinter.Label(ventana, image=im2).pack()

ventana.mainloop()
