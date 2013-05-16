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
    if kerneltype == "SOBEL":
        if theta == 0:
            kernel=[[-1,-1,-1],[2,2,2],[-1,-1,-1]]
        if theta == 90:
            kernel=[[-1,2,-1],[-1,2,-1],[-1,2,-1]]
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
    if kerneltype == "line":
        kernel=[[0,1,0],[1,-4,1],[0,1,0]]
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
            imagen.putpixel((i,j),(resultado, resultado, resultado))
    return imagen

def b_and_w(scale):
    grayscale("prom",im)
    for i in range(x):
        for j in range(y):
            pixel = im.getpixel((i,j))[0]
            if(pixel<scale):
                pixel = 0
            else:
                pixel = 255
            im.putpixel((i,j), (pixel,pixel,pixel))

def grayscale(tipo, im):
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

def puntos(imagen):
    lista = []
    for i in range(x):
        for j in range(y):
            if imagen.getpixel((i,j))!=(0,255,0) and imagen.getpixel((i,j))!=(0,0,0):
                lista.append(bfs((i,j), imagen, (0,255,0)))
    return lista

def median_blur(maxiter, normalize = False):
    imagen = Image.open(file).convert("RGB")
    imagen = grayscale("prom",imagen)
    iter = 0
    while iter < maxiter:

        for i in range(x):
            for j in range(y):
                prom = []
                k=1
                pixel=imagen.getpixel((i, j))[0]
                prom.append(im.getpixel((i, j))[0])
                try:
                    prom.append(im.getpixel((i-1, j))[0])
                    k+=1
                except:
                    pass
                try:
                    prom.append(im.getpixel((i-1 ,j-1))[0])
                    prom.append(im.getpixel((i, j-1))[0])
                    k+=2
                except:
                    pass
                try:
                    prom.append(im.getpixel((i+1, j-1))[0])
                    prom.append(im.getpixel((i+1, j))[0])
                    k+=2
                except:
                    pass
                try:
                    prom.append(im.getpixel((i-1, j+1))[0])
                    prom.append(im.getpixel((i, j+1))[0])
                    prom.append(im.getpixel((i+1, j+1))[0])
                    k+=3
                except:
                    pass
                promedio = 0;
                prom.sort()
                promedio=prom[k/2]
                if normalize:
                    imagen.putpixel((i,j), (pixel-promedio,pixel-promedio,pixel-promedio))
                else:
                    im.putpixel((i,j), (promedio,promedio,promedio))
        iter+=1
    

def blur(maxiter, normalizado = False):
    iter = 0
    while iter < maxiter:
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
                promedio = promedio/k
                if normalizado:
                    im.putpixel((i,j), (pixel-promedio,pixel-promedio,pixel-promedio))
                else:
                    im.putpixel((i,j), (promedio,promedio,promedio))            
        iter+=1

def normalizado(iter, umbral):
    global im
    im = grayscale("prom", im)
    blur(iter*1.5, True)
    lista = []
    for i in range(x):
        for j in range(y):
            lista.append(im.getpixel((i,j)))
    (minimo,bla,bla) = min(lista)
    (maximo,bla,bla) = max(lista)
    rr = maximo-minimo
    prop=maximo-minimo
    for i in range(x):
        for j in range(y):
            (r,g,b)=im.getpixel((i,j))
            pix = int(math.floor((r-minimo)*prop))
            im.putpixel((i,j),(pix,pix,pix))
    b_and_w(umbral)
    blur(iter, False)
    b_and_w(umbral)

     
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

def centros(objs):
    centroides = []
    for obj in objs:
        xobj = []
        yobj = []
        for coord in obj:
            xobj.append(coord[0])
            yobj.append(coord[1])
        centroides.append(((sum(xobj)/len(xobj)), (sum(yobj)/len(yobj))))
    return centroides

def hole_detection(n):
    imagen = Image.open(file).convert("RGB")
    imagen2 = Image.open(file).convert("RGB")
    b_and_w(n)
    color_inv()
    im.save("B_W.png")
    picosh, picosv = holes(im)
    coords = []
    for pico in picosv:
        for i in range(x):
            imagen.putpixel((i,pico),(255,0,0))
    for pico in picosh:
        for i in range(y):
            if imagen.getpixel((pico,i)) == (255,0,0):
                coords.append((pico,i))
                imagen.putpixel((pico,i),(0,255,0))
            else:
                imagen.putpixel((pico,i),(0,0,255))
    bw = Image.open("B_W.png").convert("RGB")
    newcoords = []
    for coord in coords:
        if bw.getpixel(coord) == (255,255,255):
            newcoords.append(coord)
    bw = Image.open("B_W.png").convert("RGB")
    regions = []
    for coord in newcoords:
        regions.append(bfs(coord,bw,(255,0,255)))
    centro = centros(regions)
    i = 0
    for region in regions:
        print "Agujero",i
        print "Area ocupada:",len(region)
        print "Porcentaje:","{0:.2f}".format(float(len(region))/(im.size[0]*im.size[1])*100)+"%"
        i+=1
        b = random.randint(100,140)
        for coord in region:
            imagen2.putpixel(coord, ((76, 40, b)))
    draw = ImageDraw.Draw(imagen2)
    font = ImageFont.truetype("/System/Library/Fonts/AppleGothic.ttf", 15)
    count=0
    for i in centro:
        draw.ellipse((i[0]-3, i[1]-3, i[0]+3, i[1]+3), fill=(255, 233, 0))
        draw.text((i[0]+5, i[1]), "A"+str(count), (255,255,255), font=font)
        count+=1    
    imagen2.save("Test.png")
    imagen.save("HL_"+file)
    return imagen2

def holes(image):
    matriz = []
    for i in range(x):
        fila = []
        for j in range(y):
            fila.append(image.getpixel((i,j))[0])
        matriz.append(fila)
    horizontal = []
    escalax = 0.0
    vertical = []
    escalay = 0.0
    for i in range(x):
        suma = 0
        for j in range(y):
            suma += matriz[i][j]
        horizontal.append(suma)
    escalax = float(y)/float(max(horizontal))
    for i in range(y):
        suma = 0
        for j in range(x):
            suma += matriz[j][i]
        vertical.append(suma)
    escalay = float(x)/float(max(vertical))
    pico = False
    current = 0
    picosh = []
    picosv = []
    for i in range(len(horizontal)-1):
        if horizontal[i]>horizontal[i+1] and horizontal[i]>horizontal[current]:
            current = i
            pico = True
        if horizontal[i] == 0 and pico == True:
            picosh.append(current)
            current = 0
            pico = False
    pico = False
    current = 0
    for i in range(len(vertical)-1):
        if vertical[i]>vertical[i+1] and vertical[i]>vertical[current]:
            current = i
            pico = True
        if vertical[i] == 0 and pico == True:
            picosv.append(current)
            current = 0
            pico = False
    for i in range(x):
        for j in range(int(horizontal[i]*escalax)):
            image.putpixel((i,j),(0,0,255))
    coords = []
    for i in range(y):
        for j in range(int(vertical[i]*escalay)):
            if image.getpixel((j,i))==(0,0,255):
                coords.append((j,i))
            image.putpixel((j,i),(255,0,0))
    for coord in coords:
        image.putpixel(coord,(0,255,0))
    image.save("H.png")
    return (picosh, picosv)

def dilation(image, iter):
    k=0
    while k<iter:
        for i in range(x):
            for j in range(y):
                if image.getpixel((i,j))==(255,255,255):
                    try:
                        image.putpixel((i-1,j),(255,255,255))
                    except:
                        pass
        for i in reversed(range(x)):
            for j in reversed(range(y)):
                if image.getpixel((i,j))==(255,255,255):
                    try:
                        image.putpixel((i+1,j),(255,255,255))
                    except:
                        pass
        for i in range(x):
            for j in range(y):
                if image.getpixel((i,j))==(255,255,255):
                    try:
                        image.putpixel((i,j-1),(255,255,255))
                    except:
                        pass
        for i in reversed(range(x)):
            for j in reversed(range(y)):
                if image.getpixel((i,j))==(255,255,255):
                    try:
                        image.putpixel((i,j+1),(255,255,255))
                    except:
                        pass
        k+=1
    return image

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


def objetos(nueva):
    pintura = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255),(255,127,0),(0,255,127),(127,0,255),(255,0,127),(127,255,0),(0,127,255),(255,127,127),(127,255,127),(127,127,255),(127,0,0),(127,127,0),(127,0,127),(0,127,0),(0,0,127)]
    if nueva == None:
        nueva = Image.open(file).convert("RGB")
    objs = []
    centroides = []
    count = 0
    for i in range(x):
        for j in range(y):
            if nueva.getpixel((i,j)) != (255,0,0) and nueva.getpixel((i,j)) != (255,255,255):
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

def circulos(nueva):
    pintura = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255),(255,127,0),(0,255,127),(127,0,255),(255,0,127),(127,255,0),(0,127,255),(255,127,127),(127,255,127),(127,127,255),(127,0,0),(127,127,0),(127,0,127),(0,127,0),(0,0,127)]
    if nueva == None:
        nueva = Image.open(file).convert("RGB")
    objs = []
    bordes = []
    centroides = []
    count = 0
    for i in range(x):
        for j in range(y):
            if nueva.getpixel((i,j)) != (255,0,0) and nueva.getpixel((i,j)) != (255,255,255):
                objs.append(bfs((i,j), nueva, (255,0,0)))
                count+=1
            if nueva.getpixel((i,j)) == (255,255,255):
                bordes.append(bfs((i,j), nueva, (255,0,0)))
    print "Total de bordes:",len(bordes)
    centro = []
    for borde in bordes:
        xobj = []
        yobj = []
        for coord in borde:
            xobj.append(coord[0])
            yobj.append(coord[1])
        centro.append(((sum(xobj)/len(xobj)), (sum(yobj)/len(yobj))))
    
    distancias = []
    i = 0
    for borde in bordes:
        distancia = []
        for coord in borde:
            distancia.append(math.sqrt(((coord[0]-centro[i][0])**2)+((coord[1]-centro[i][1])**2)))
        distancias.append(distancia)
        i+=1
    area = []
    nueva = Image.open(file).convert("RGB")
    for i in centro:
        area.append(bfs(i,nueva,(255,0,0)))
    nueva.save("rojos.png")
    radios = []
    for obj in area:
        radios.append(math.sqrt(len(obj)/3.1416))
    for radio in radios:
        print radio
    nueva = Image.new('RGB', (x, y), (0, 0, 0))
    draw = ImageDraw.Draw(nueva)
    for i in range(len(radios)):
        draw.ellipse((centro[i][0]-math.floor(radios[i]), centro[i][1]-math.floor(radios[i]), centro[i][0]+math.floor(radios[i]), centro[i][1]+math.floor(radios[i])), fill=(255,0,255))
    
    circleareas=[]
    nueva.save("areas.png")
    nueva = Image.open("areas.png").convert("RGB")
    for i in centro:
        circleareas.append(bfs(i,nueva,(255,0,0)))
    errores=[]
    for i in range(len(circleareas)):
        error = 0
        for j in range(len(circleareas[i])):
            if circleareas[i][j] not in area[i]:
                error+=1
        errores.append(error)
    count = 0
    circulos=[]
    for error in errores:
        print "Errores en objeto",centro[count],error
        print ((error*1.0)/(len(area[count])*1.0))*100.0
        print ((error*1.0)/(len(area[count])*1.0))*100.0 <=7.0
        if ((error*1.0)/(len(area[count])*1.0))*100.0 <=6.0:
            circulos.append(centro[count])
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
    for i in circulos:
        draw.text((i[0]+10, i[1]-15), "Circulo", (0,0,0), font=font)
    i = 0
    for distancia in distancias:
        draw.text(bordes[i][distancia.index(min(distancia))], "*", (0,0,0), font=font)
        draw.text(bordes[i][distancia.index(max(distancia))], "*", (0,0,0), font=font)
        i+=1

def elipses(nueva):
    pintura = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255),(255,127,0),(0,255,127),(127,0,255),(255,0,127),(127,255,0),(0,127,255),(255,127,127),(127,255,127),(127,127,255),(127,0,0),(127,127,0),(127,0,127),(0,127,0),(0,0,127)]
    if nueva == None:
        nueva = Image.open(file).convert("RGB")
    objs = []
    bordes = []
    centroides = []
    count = 0
    for i in range(x):
        for j in range(y):
            if nueva.getpixel((i,j)) != (255,0,0) and nueva.getpixel((i,j)) != (255,255,255):
                objs.append(bfs((i,j), nueva, (255,0,0)))
                count+=1
            if nueva.getpixel((i,j)) == (255,255,255):
                bordes.append(bfs((i,j), nueva, (255,0,0)))
    print "Total de bordes:",len(bordes)
    centro = []
    for borde in bordes:
        xobj = []
        yobj = []
        for coord in borde:
            xobj.append(coord[0])
            yobj.append(coord[1])
        centro.append(((sum(xobj)/len(xobj)), (sum(yobj)/len(yobj))))
    distancias = []
    i = 0
    for borde in bordes:
        distancia = []
        for coord in borde:
            distancia.append(math.sqrt(((coord[0]-centro[i][0])**2)+((coord[1]-centro[i][1])**2)))
        distancias.append(distancia)
        i+=1
    
    cini = []
    cfin = []

    for i in range(len(centro)):
        print min(distancias[i]), bordes[i][distancias[i].index(min(distancias[i]))],
        print max(distancias[i]), bordes[i][distancias[i].index(max(distancias[i]))],
        print centro[i]
        print bordes[i][distancias[i].index(min(distancias[i]))][0], centro[i][0]
        if bordes[i][distancias[i].index(min(distancias[i]))][0] > centro[i][0]-10 and bordes[i][distancias[i].index(min(distancias[i]))][0] < centro[i][0]+10:
            print "Horizontal"
            cini.append((centro[i][0]-max(distancias[i]), centro[i][1]-min(distancias[i])))
            cfin.append(((centro[i][0]+max(distancias[i])), (centro[i][1]+min(distancias[i]))))
        else:
            print "Vertical"
            cini.append((centro[i][0]-min(distancias[i]), centro[i][1]-max(distancias[i])))
            cfin.append(((centro[i][0]+min(distancias[i])), (centro[i][1]+max(distancias[i]))))

    area = []
    nueva = Image.open(file).convert("RGB")
    for i in range(len(centro)):
        #if i != 0:
            area.append(bfs(centro[i],nueva,(255,0,0)))
    nueva.save("rojos.png")
    nueva = Image.new('RGB', (x, y), (0, 0, 0))
    draw = ImageDraw.Draw(nueva)
    for i in range(len(centro)):
        #if i != 0:
            draw.ellipse((cini[i][0],cini[i][1], cfin[i][0], cfin[i][1]), fill=(255,0,255))

    circleareas=[]
    nueva.save("areas.png")
    nueva = Image.open("areas.png").convert("RGB")
    for i in range(len(centro)):
        #if i != 0:
            circleareas.append(bfs(centro[i],nueva,(255,0,0)))
    errores=[]
    for i in range(len(circleareas)):
        print i
        error = 0
        for j in range(len(circleareas[i])):
            if circleareas[i][j] not in area[i]:
                error+=1
        errores.append(error)
    count = 0
    circulos=[]
    diferencia = []
    for error in errores:
        if ((error*1.0)/(len(area[count])*1.0))*100.0 <=15.0:
            print "Elipse en:",centro[count]
            print "Radio menor:", min(distancias[count])
            print "Radio mayor:", max(distancias[count])
            print "Margen de error:", ((error*1.0)/(len(area[count])*1.0))*100.0
            print "\n"
            diferencia.append(max(distancias[count]) - min(distancias[count]))
            circulos.append(centro[count])
        else:
            print "NO Elipse en:",centro[count]
            print "Radio menor:", min(distancias[count])
            print "Radio mayor:", max(distancias[count])
            print "Margen de error:",((error*1.0)/(len(area[count])*1.0))*100.0
            print "\n"
        count+=1

    for obj in objs:
        xobj = []
        yobj = []
        for coord in obj:
            xobj.append(coord[0])
            yobj.append(coord[1])
        centroides.append(((sum(xobj)/len(xobj)), (sum(yobj)/len(yobj))))

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("/System/Library/Fonts/AppleGothic.ttf", 15)

    count = 0
    bfs(objs[0][0], im, (127,127,127))
    print "Area total:",im.size[0]*im.size[1]
    print ""
    for i in circulos:
        a = bfs(i, im, pintura[count])
        draw.ellipse((i[0]-5, i[1]-5, i[0]+5, i[1]+5), fill=(0,0,0))
        if diferencia[count] > 10:
            draw.text((i[0]+10, i[1]-15), "Elipse "+str(count), (0,0,0), font=font)
        else:
            draw.text((i[0]+10, i[1]-15), "Elipse "+str(count)+" (Circulo)", (0,0,0), font=font)
        print "Elipse:", count
        print "Area ocupada:",len(a)
        print "Porcentaje:","{0:.2f}".format(float(len(a))/(im.size[0]*im.size[1])*100)+" %"
        print ""
        count+=1

    #i = 0
    #for distancia in distancias:
        #draw.text(bordes[i][distancia.index(min(distancia))], "*", (255,0,255), font=font)
        #draw.text(bordes[i][distancia.index(max(distancia))], "*", (255,0,255), font=font)
        #i+=1

    #for i in range(len(cini)):
        #draw.text(cini[i], "*", (255,0,0), font=font)
        #draw.text(cfin[i], "*", (255,0,0), font=font)

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


def lines(u):
    pintura = [(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255),(255,127,0),(0,255,127),(127,0,255),(255,0,127),(127,255,0),(0,127,255),(255,127,127),(127,255,127),(127,127,255),(127,0,0),(127,127,0),(127,0,127),(0,127,0),(0,0,127)]
    nueva = Image.new("RGB", (x,y), (255,0,0))
    gradx = convolucion("SOBEL", 0)
    grady = convolucion("SOBEL", 90)
    matriz = []
    comb = {}
    ang = []
    for i in range(x):
        lista = []
        for j in range(y):
            gx = gradx.getpixel((i,j))[0]
            gy = grady.getpixel((i,j))[0]
            theta = 0.0
            """if abs(gx) + abs(gy) <= 0.0:
                theta = None
                elif gx == 0 and gy == 255:
                theta = 90"""
            try:
                if gx == 255 and gy == 0:
                    theta = math.atan(gy/gx)
                else:
                    theta = math.atan(gx/gy)
            except:
                theta = None
            if theta is not None:
                rho = abs((i) * math.cos(theta) + (j) * math.sin(theta))
                if not theta in ang:  
                    ang.append(theta)
                if i > 0 and i < x-1 and j > 0 and j < y - 1:
                    if (rho, theta) in comb:
                        comb[(rho, theta)] += 1
                    else:
                        comb[(rho, theta)] = 1
                lista.append((rho, theta))
            else:
                lista.append((None, None))
        matriz.append(lista)
    comb = sorted(comb.items(), key=lambda k: k[1], reverse = True)
    frec = {}
    n = int(math.ceil(len(comb) * u))
    rholist = []
    for i in range(n):
        (rho, theta) = comb[i][0]
        if theta not in rholist:
            rholist.append(theta)
        frec[(rho, theta)] = comb[1]
    for i in range(x):
        for j in range(y):
            if i > 0 and j > 0 and i < x and j < y:
                rho, theta = matriz[i][j]
                if (rho, theta) in frec:
                    if theta !=0:
                        nueva.putpixel((i,j),(255,255,255))
                    else:
                        nueva.putpixel((i,j),(0,0,0))
    nueva.save("diagonal.png")
    nueva = dilation(nueva,2)
    count = 0
    objs = []
    k=0
    for i in range(x):
        for j in range(y):
            if nueva.getpixel((i,j)) == (255,255,255) or nueva.getpixel((i,j)) == (0,0,0):
                objs.append(bfs((i,j), nueva, pintura[k]))
                count+=1
                k+=1
                if k == 19:
                    k = 0
    listilla = []
    for i in range(x):
        for j in range(y):
            if i > 0 and j > 0 and i < x and j < y:
                rho, theta = matriz[i][j]
                if (rho, theta) in frec:
                    if theta not in listilla:
                        listilla.append(theta)
                    im.putpixel((i,j),nueva.getpixel((i,j)))
    print len(listilla)
    nueva.save("output.png")

def distancia(p1, p2):
    x1,y1 = p1
    y2, x2 = p2
    return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2)

if(argv[2]=="LN" or argv[2]=="ln"):
    if(len(argv)==4):
        lines(float(argv[3]))
        im.save("LN_"+file)
    else:
        print "Introduzca el umbral."

if(argv[2]=="HL" or argv[2]=="hl"):
    im = hole_detection(int(argv[3]))

if(argv[2]=="CH" or argv[2]=="ch"):
    im=dilation(im, 1)
    points = convexhull(im)
    draw = ImageDraw.Draw(im)
    for point in points:
        draw.line(point, fill=255)
    im.save("CH_"+file)

if(argv[2]=="DIL" or argv[2]=="dil"):
    if (len(argv)==4):
        im=dilation(im, int(argv[3]))
        im.save("DIL_"+file)
    else:
        print "Introduzca la cantidad de iteraciones de dilatacion"

if(argv[2]=="OBJ" or argv[2]=="obj"):
    objetos(None)
    im.save("OBJ_"+file)

if(argv[2]=="CIR" or argv[2]=="cir"):
    circulos(None)
    im.save("CIR_"+file)
               
               
if(argv[2]=="ELI" or argv[2]=="eli"):
    elipses(None)
    im.save("ELI_"+file)

if(argv[2]=="BFS" or argv[2]=="bfs"):
    if(len(argv)==5):
        bfs((int(argv[3]), int(argv[4])))
    else:
        print "Introduzca la posicion 'X' y 'Y'"

if(argv[2]=="SP" or argv[2]=="sp"):
        #sal_pim(float(argv[3]), float(argv[4]))
        #im.save("SP_"+file)
        quitar_sal_pim(float(True))
        quitar_sal_pim(float(False))
        im.save("QUITAR_SP_"+file)

if(argv[2]=="CAT"):
    median_blur(1)
    normalizado(1, 254)
    im=dilation(im, 7)
    lista = []
    for i in range(x):
	for j in range(y):
	    if im.getpixel((i,j)) != (255,255,255):
		lista.append(bfs((i,j), im, (255,255,255)))
    centro = centros(lista)
    imagen = Image.open(file).convert("RGB")
    draw = ImageDraw.Draw(imagen)
    c = centros([centro])
    suma = 0
    for d in centro:
	suma += distancia(c[0],(d[1],d[0]))
    dist = 1.5*(suma/len(centro))
    for elemento in c:
        draw.rectangle((elemento[0]-dist, elemento[1]-dist,elemento[0]+dist, elemento[1]+dist), outline=(255,0,0))
    imagen.save("CAT_"+file)
    im = imagen

if(argv[2]=="CON" or argv[2]=="con"):
    if(len(argv)==5):
        im = convolucion(argv[3], int(argv[4]))
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
        blur(int(argv[3]))
        im.save("B_"+file)
    else:
        print "Introduzca el numero de iteraciones de blur como parametro."

if(argv[2]=="E" or argv[2]=="e"):
    if(len(argv)==4):
        median_blur(int(argv[3]))
        b_and_w(20)
        im = dilation(im,2)
        points = puntos(im)
        coords = []
        for lista in points:
            coords.append(max(lista))
        algo = centros([coords])
        print algo
        grados = {}
        for coord in coords:
            dx = algo[0][0] - coord[0]
            dy = algo[0][1] - coord[1]
            rads = math.atan2(-dy,dx)
            rads %= 2*math.pi
            gr = math.degrees(rads)
            grados.update({gr:coord})
        keys = grados.keys()
        keys.sort()
        lineas = []
        ln = ImageDraw.Draw(im)
        for key in keys:
            lineas.append(grados[key])
        lineas.append(grados[keys[0]])
        ln.line(lineas, fill="red")
        im.save("B_"+file)
    else:
        print "Introduzca el numero de iteraciones de blur como parametro."

if(argv[2]=="MB" or argv[2]=="mb"):
    if(len(argv)==4):
        median_blur(int(argv[3]))
        im.save("MB_"+file)
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
