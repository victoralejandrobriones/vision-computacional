import Tkinter
import Image, ImageTk, ImageDraw, ImageFont
from sys import argv
import math
import random

file = argv[1]

im = Image.open(file).convert("RGB")
grayscaleim = Image.open(file).convert("RGB")
original = im
(x,y) = im.size

def convolucion(kerneltype, theta):
    imagen = Image.open(file).convert("RGB")
    grayscale("prom")
    kernel=[[0,1,0],[1,0,1],[0,1,0]]
    if kerneltype == "PREW":
        if theta == 0:
            kernel=[[-1,1,1],[-1,-2,1],[-1,1,1]]
        if theta == 45:
            kernel=[[1,1,1],[-1,-2,1],[-1,-1,1]]
    if kerneltype == "KIR":
        if theta == 0:
            kernel=[[-3,-3,5],[-3,0,5],[-3,-3,5]]
        if theta == 45:
            kernel=[[-3,5,5],[-3,0,5],[-3,-3,-3]]
    if kerneltype == "ROBIN3":
        if theta == 0:
            kernel=[[-1,0,1],[-1,0,1],[-1,0,1]]
        if theta == 45:
            kernel=[[1,1,1],[-1,-2,1],[-1,-1,1]]
    if kerneltype == "ROBIN5":
        if theta == 0:
            kernel=[[-1,0,1],[-2,0,2],[-1,0,1]]
        if theta == 45:
            kernel=[[0,1,2],[-1,0,1],[-2,-1,0]]
    for i in range(x):
        for j in range(y):
            prom = [[0,0,0],[0,0,0],[0,0,0]]
            pixel=grayscaleim.getpixel((i, j))[0]
            prom[1][1]=grayscaleim.getpixel((i, j))[0]
            try:
                prom[0][1]=grayscaleim.getpixel((i-1, j))[0]
            except:
                prom[0][1]=grayscaleim.getpixel((i, j))[0]
            try:
                prom[0][0]=grayscaleim.getpixel((i-1 ,j-1))[0]
                prom[1][0]=grayscaleim.getpixel((i, j-1))[0]
            except:
                prom[0][0]=grayscaleim.getpixel((i, j))[0]
                prom[1][0]=grayscaleim.getpixel((i, j))[0]
            try:
                prom[2][0]=grayscaleim.getpixel((i+1, j-1))[0]
                prom[2][1]=grayscaleim.getpixel((i+1, j))[0]
            except:
                prom[2][0]=grayscaleim.getpixel((i, j))[0]
                prom[2][1]=grayscaleim.getpixel((i, j))[0]
            try:
                prom[0][2]=grayscaleim.getpixel((i-1, j+1))[0]
                prom[1][2]=grayscaleim.getpixel((i, j+1))[0]
                prom[2][2]=grayscaleim.getpixel((i+1, j+1))[0]
            except:
                prom[0][2]=grayscaleim.getpixel((i, j))[0]
                prom[1][2]=grayscaleim.getpixel((i, j))[0]
                prom[2][2]=grayscaleim.getpixel((i, j))[0]
            resultado=0
            for a in range(len(prom)):
                for b in range(len(prom[a])):
                    resultado+=(prom[a][b]*kernel[a][b])
            im.putpixel((i,j),(resultado, resultado, resultado))

def b_and_w(scale):
    grayscale("prom")
    for i in range(x):
        for j in range(y):
            pixel = im.getpixel((i,j))[0]
            if(pixel<scale):
                pixel = 0
            else:
                pixel = 255
            im.putpixel((i,j), (pixel,pixel,pixel))

def grayscale(tipo):
    for i in range(x):
        for j in range(y):
            (r,g,b)=original.getpixel((i, j))
            if tipo == "min":
                gray = min((r,g,b))
            if tipo == "max":
                gray = max((r,g,b))
            if tipo == "r":
                gray = r
            if tipo == "g":
                gray = g
            if tipo == "b":
                gray = b
            if tipo == "prom":
                gray = (r+g+b)/3
            im.putpixel((i,j), (gray,gray,gray))
    return im

def blur(maxiter, normalizado):
    grayscale("prom")
    iter = 0
    while iter < maxiter:
        print "Iteracion: ", iter+1
        for i in range(x):
            for j in range(y):
                prom = []
                k=0
                pixel=im.getpixel((i, j))[0]
                if(i-1>=0):
                    prom.append(im.getpixel((i-1, j))[0])
                    k+=1
                if(i+1<x):
                    prom.append(im.getpixel((i+1, j))[0])
                    k+=1
                if(j+1<y):
                    prom.append(im.getpixel((i, j+1))[0])
                    k+=1
                if(j-1>=0):
                    prom.append(im.getpixel((i, j-1))[0])
                    k+=1
                promedio = 0;
                for valor in prom:
                    promedio+=valor
                promedio=promedio/k
                if normalizado:
                    im.putpixel((i,j), (pixel-promedio,pixel-promedio,pixel-promedio))
                else:
                    im.putpixel((i,j), (promedio,promedio,promedio))            
        iter+=1

def normalizado(iter, umbral):
    im = grayscale("prom")
    blur(iter*1.5, False)
    lista = []
    for i in range(x):
        for j in range(y):
            lista.append(im.getpixel((i,j)))
    (minimo,bla,bla) = min(lista)
    (maximo,bla,bla) = max(lista)
    rr = maximo-minimo
    prop=256/rr
    for i in range(x):
        for j in range(y):
            (r,g,b)=im.getpixel((i,j))
            pix = int(math.floor((r-minimo)*prop))
            im.putpixel((i,j),(pix,pix,pix))
    b_and_w(umbral)
    blur(iter, True)
    im = b_and_w(umbral)
     
def color_blur(maxiter):
    iter = 0
    while iter < maxiter:
        for i in range(x):
            for j in range(y):
                promr = []
                promg = []
                promb = []
                k=0
                (r,g,b)=original.getpixel((i, j))
                if(i-1>=0):
                    (rn,gn,bn)=original.getpixel((i-1, j))
                    promr.append(rn)
                    promg.append(gn)
                    promb.append(bn)
                    k+=1
                if(i+1<x):
                    (rs,gs,bs)=original.getpixel((i+1, j))
                    promr.append(rs)
                    promg.append(gs)
                    promb.append(bs)
                    k+=1
                if(j+1<y):
                    (re,ge,be)=original.getpixel((i, j+1))
                    promr.append(re)
                    promg.append(ge)
                    promb.append(be)
                    k+=1
                if(j-1>=0):
                    (ro,go,bo)=original.getpixel((i, j-1))
                    promr.append(ro)
                    promg.append(go)
                    promb.append(bo)
                    k+=1
                promedior = 0
                promediog = 0
                promediob = 0
                for valor in promr:
                    promedior+=valor
                for valor in promg:
                    promediog+=valor
                for valor in promb:
                    promediob+=valor
                promedior=promedior/k
                promediog=promediog/k
                promediob=promediob/k
                im.putpixel((i,j), (promedior,promediog,promediob))
        iter+=1

def getcolor(color):
    for i in range(x):
        for j in range(y):
            (r,g,b)=original.getpixel((i,j))
            if(color=="r" or color=="R"):
                im.putpixel((i,j),(r,0,0))
            if(color=="g" or color =="G"):
                im.putpixel((i,j),(0,g,0))
            if(color=="b" or color == "B"):
                im.putpixel((i,j),(0,0,b))

def color_inv():
    for i in range(x):
        for j in range(y):
            (r,g,b)=original.getpixel((i,j))
            im.putpixel((i,j),(255-r,255-g,255-b))

def sal_pim(prop, sal):
    negros = 0
    blancos = 0
    for i in range(x):
        for j in range(y):
            if prop >= random.random():
                numero = random.random()
                if sal >= numero:
                    blancos+=1
                    pim = random.randint(230, 255)
                    im.putpixel((i,j),(pim,pim,pim))
                elif sal <= numero:
                    negros+=1
                    pim = random.randint(0, 30)
                    im.putpixel((i,j),(pim,pim,pim))
    time.sleep(4)

def quitar_sal_pim(negros):
    iter = 0
    for i in range(x):
        for j in range(y):
            promr = []
            promg = []
            promb = []
            k=0
            (r,g,b)=original.getpixel((i, j))
            if(i-1>=0):
                (rn,gn,bn)=original.getpixel((i-1, j))
                promr.append(rn)
                promg.append(gn)
                promb.append(bn)
                k+=1
            if(i+1<x):
                (rs,gs,bs)=original.getpixel((i+1, j))
                promr.append(rs)
                promg.append(gs)
                promb.append(bs)
                k+=1
            if(j+1<y):
                (re,ge,be)=original.getpixel((i, j+1))
                promr.append(re)
                promg.append(ge)
                promb.append(be)
                k+=1
            if(j-1>=0):
                (ro,go,bo)=original.getpixel((i, j-1))
                promr.append(ro)
                promg.append(go)
                promb.append(bo)
                k+=1
            promedior = 0
            promediog = 0
            promediob = 0
            for valor in promr:
                promedior+=valor
            for valor in promg:
                promediog+=valor
            for valor in promb:
                promediob+=valor
            promedior=promedior/k
            promediog=promediog/k
            promediob=promediob/k
            if not negros:
                if ((r) >= 230 and (g) >= 230 and (b ) >= 230):
                    iter+=1
                    im.putpixel((i,j), (promedior,promediog,promediob))
            if negros:
                if ((r) <= 30 and (g) <= 30 and (b) <= 30):
                    iter+=1
                    im.putpixel((i,j), (promedior,promediog,promediob))

def bfs(pixel, imagen, pintura):
    k=0
    (w,h)=imagen.size
    lista = []
    lista.append(pixel)
    (r,g,b)=imagen.getpixel(pixel)
    color = r #Suponiendo que la imagen esta en blanco y negro.
    for x,y in lista:
        for i in range(x, x+1):
            for j in range(y, y+1):
                if i >= 0 and j >= 0 and i < w and j < h:
                    if imagen.getpixel((i,j))==(r,g,b):
                        lista.append((i,j))
                        imagen.putpixel((i,j), pintura)
                        #im.save(str(k)+".png")
                        k+=1
                    try:
                        if imagen.getpixel((i-1,j))==(r,g,b):
                            lista.append((i-1,j))
                            imagen.putpixel((i-1,j), pintura)
                            #im.save(str(k)+".png")
                            k+=1
                    except:
                        None
                    try:
                        if imagen.getpixel((i,j-1))==(r,g,b):
                            lista.append((i,j-1))
                            imagen.putpixel((i,j-1), pintura)
                            #im.save(str(k)+".png")
                            k+=1
                    except:
                        None   
                    try:
                        if imagen.getpixel((i+1,j))==(r,g,b):
                            lista.append((i+1,j))
                            imagen.putpixel((i+1,j), pintura)
                            #im.save(str(k)+".png")
                            k+=1
                    except:
                        None
                    try:
                        if imagen.getpixel((i,j+1))==(r,g,b):
                            lista.append((i,j+1))
                            imagen.putpixel((i,j+1), pintura) 
                            #im.save(str(k)+".png")
                            k+=1
                    except:
                        None
    return lista

def objetos():
    pintura = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255),(255,127,0),(0,255,127),(127,0,255),(255,0,127),(127,255,0),(0,127,255),(255,127,127),(127,255,127),(127,127,255),(127,0,0),(127,127,0),(127,0,127),(0,127,0),(0,0,127)]
    nueva = Image.open(file).convert("RGB")
    objs = []
    centroides = []
    count = 0
    for i in range(x):
        for j in range(y):
            if nueva.getpixel((i,j)) != (255,0,0):
                objs.append(bfs((i,j), nueva, (255,0,0)))
                count+=1
    
    for obj in objs:
        xobj = []
        yobj = []
        for coord in obj:
            xobj.append(coord[0])
            yobj.append(coord[1])
        centroides.append(((sum(xobj)/len(xobj)), (sum(yobj)/len(yobj))))
    k=0
    tam=[]
    for i in objs:
        tam.append(len(i)-1)
    ind = tam.index(max(tam))
    bfs(objs[ind][0], im, (127,127,127))

    for i in objs:
        if i[0] != objs[ind][0]:
            bfs(i[0], im, pintura[k])
        k+=1
        if k == 20:
            k = 0
        print len(i)-1, "pixeles en el objeto."
    
    print sum(tam), "pixeles en la imagen."
    print count, "objetos encontrados."
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("/System/Library/Fonts/AppleGothic.ttf", 15)
    count=1
    for i in centroides:
        draw.ellipse((i[0]-5, i[1]-5, i[0]+5, i[1]+5), fill=(0,0,0))
        draw.text((i[0]+5, i[1]), str(count), (0,0,0), font=font)
        count+=1


def giro(c, h, e):
    return cmp(0, (h[0] - c[0])*(e[1] - c[1]) - (e[0] - c[0])*(h[1] - c[1]))

def jrv_mr(coords):
    hull = [min(coords)]
    i = 0
    while True:
        end = coords[0]
        for coord in coords:
            if end == hull[i] or giro(coord, hull[i], end) == -1:
                end = coord
        i+=1
        print end
        hull.append(end)
        if end == hull[0]:
            break
    print hull
    return hull

def convexhull(im):
    hulls = []
    for i in range(x):
        for j in range(y):
            if im.getpixel((i,j)) == (255, 255, 255):
                coords = bfs((i, j),im, (127,127,127))
                hulls.append(jrv_mr(coords))
    return hulls


if(argv[2]=="CH" or argv[2]=="ch"):
    im=dilation(im)
    points = convexhull(im)
    draw = ImageDraw.Draw(im)
    for point in points:
        draw.line(point, fill=255)
    im.save("CH_"+file)


if(argv[2]=="OBJ" or argv[2]=="obj"):
    objetos()
    im.save("OBJ_"+file)

if(argv[2]=="BFS" or argv[2]=="bfs"):
    if(len(argv)==5):
        bfs((int(argv[3]), int(argv[4])))
    else:
        print "Introduzca la posicion 'X' y 'Y'"

if(argv[2]=="SP" or argv[2]=="sp"):
    if(len(argv)==5):
        sal_pim(float(argv[3]), float(argv[4]))
        im.save("SP_"+file)
        quitar_sal_pim(float(True))
        quitar_sal_pim(float(False))
        im.save("QUITAR_SP_"+file)
    else:
        print "Introduzca la proporcion de la imagen, la proporcion de sal y el rango para quitar la sal y pimienta."

if(argv[2]=="CON" or argv[2]=="con"):
    if(len(argv)==5):
        convolucion(argv[3], int(argv[4]))
        im.save("CON_"+file)
    else:
        print "Introduzca el tipo de matriz (PREW, KIR, ROBIN3, ROBN5) y theta (0 o 45)"

if(argv[2]=="INV" or argv[2]=="inv"):
        color_inv()
        im.save("INV_"+file)

if(argv[2]=="GC" or argv[2]=="gc"):
    if(len(argv)==4):
        getcolor(argv[3])
        im.save("GC_"+file)
    else:
        print "Introduzca 'r', 'g' o 'b' segun el color que desee extraer."

if(argv[2]=="BW" or argv[2]=="bw"):
    if(len(argv)==4):
        b_and_w(int(argv[3]))
        im.save("BW_"+file)
    else:
        print "Introduzca la escala de blanco y negro como parametro."

if(argv[2]=="N" or argv[2]=="n"):
    if(len(argv)==5):
        normalizado(int(argv[3]), int(argv[4]))
        im.save("N_"+file)
    else:
        print "Introduzca el numero de iteraciones y el umbral."

if(argv[2]=="G" or argv[2]=="g"):
    if(len(argv)==4):
        grayscale(argv[3])
        im.save("G_"+file)
    else:
        print "Introduzca el tipo de escala de gris (min, max, r, g, b, prom)."

if(argv[2]=="B" or argv[2]=="b"):
    if(len(argv)==4):
        blur(int(argv[3]), False)
        im.save("B_"+file)
    else:
        print "Introduzca el numero de iteraciones de blur como parametro."

if(argv[2]=="CB" or argv[2]=="cb"):
    if(len(argv)==4):
        color_blur(int(argv[3]))
        im.save("CB_"+file)
    else:
        print "Introduzca el numero de iteraciones de blur como parametro."

ventana = Tkinter.Tk()
im2 = ImageTk.PhotoImage(im)
Tkinter.Label(ventana, image=im2).pack()

ventana.mainloop()
