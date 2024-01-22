import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import cv2 as cv2
from matplotlib.colors import Normalize
import time
######################
# 
#  Das programm soll später in den haupt script importiert werden und die dct2 funktion aufgerufen werden
#  um dann die dct matrix zu erstellen, welche für die komprimierung bearbeitet werden kann.
#
#  die matrix heißt Trans und wird dann wieder verwendet um ein Bild zu geben. Dieses ausgebene bilde werden
#  dann auf ein Objekt projezuiert damit man es sehen kann. Durch eine Update funktion wird dieses bilde
#  dann immer ausgetauscht mit dem entsprechenden angepassten komprimerungskoeffizienten
#
#
#
#
#################################


# hier wird die dct matrix übergeben und ein wert der dann die kompriemierung bestimmt. muss noch gemacht werden
def koeffizientenAnpassung(matrix, komprimierungsIndex):
    code = range(0,64)  #bis 11 eingetragen
    # per hand eintragen :/
    item = [(7,7),(6,7),(7,6),(7,5),(6,6),(5,7),(4,7),(5,6),(6,5),(7,4),(7,3),(6,4),(5,5),(4,6),(3,7),(2,7),(3,6),(4,5),(5,4),(6,3),(7,2),(7,1),(6,2),(5,3),(4,4),(3,5),(2,6),(1,7),(0,7),(1,6),(2,5),(3,4),(4,3),(5,2),(6,1),(7,0),(6,0),(5,1),(4,2),(3,3),(2,4),(1,5),(0,6),(0,5),(1,4),(2,3),(3,2),(4,1),(5,0),(4,0),(3,1),(2,2),(1,3),(0,4),(0,3),(1,2),(2,1),(3,0),(2,0),(1,1),(0,2),(0,1),(1,0),(0,0)]
    print(len(item))
    zipped = zip(code,item)
    # das Dict um die Matrixen werte zu wissen, die von hinten nach vorne auf null gesetzt werden müssen
    dictZipped = dict(zipped)
    B=8 #blocksize
    h,w=np.array(matrix.shape[:2])/B * B # universell die höhe und width bekommen
    #Konversion to integer, einfach weil python dumm und automatisch float macht
    h = int(h)
    w = int(w)
    # Unterteilung der Blöcke die in der Width und Hight benötigt werden
    blocksV=int(h/B)
    blocksH=int(w/B)
    #erste schleife um die blöcke zu bekommen
    for row in range(blocksV):
            for col in range(blocksH):
                currentblock = matrix[row*B:(row+1)*B,col*B:(col+1)*B]
            # diese schleife um alle notwendigen matrix einträge im block auf null zu setzten
                for i in range(0,komprimierungsIndex):
                        # die Variable i wählt aus dem dictZipped das feld und die Zweite [0] 
                        # wählen den eintrag in der liste
                        currentblock[dictZipped[i][0],dictZipped[i][1]] = 0 
                        matrix[row*B:(row+1)*B,col*B:(col+1)*B] = currentblock
                        #print("index:"+str(dictZipped[i][0])+str(dictZipped[i][1])+ "  " +str(currentblock[dictZipped[i][0],dictZipped[i][1]])) #for debugging purpise
    return matrix
    
def dct2(fn3):
    B=8 #blocksize
    img1 = cv2.imread(fn3, 0)
    h,w=np.array(img1.shape[:2])/B * B
    h = int(h)
    w = int(w)
    img1=img1[:h,:w]
    blocksV=int(h/B)
    blocksH=int(w/B)
    vis0 = np.zeros((h,w), np.float32)
    Trans = np.zeros((h,w), np.float32)
    vis0[:h, :w] = img1
    for row in range(blocksV):
        for col in range(blocksH):
            currentblock = cv2.dct(vis0[row*B:(row+1)*B,col*B:(col+1)*B])
            Trans[row*B:(row+1)*B,col*B:(col+1)*B]=currentblock
    cv2.imwrite('Transformed.jpg', Trans)
    plt.imshow(Trans,cmap="gray")
    return Trans


# nimmt die dct matrix und verwandelt sie in ein bild zurück das dann auf einen entity projeziert wird
def Idct2(Trans, Iteration):
    B=8 #blocksize
    h,w=np.array(Trans.shape[:2])/B * B
    h = int(h)
    w = int(w)
    blocksV=int(h/B)
    blocksH=int(w/B)
    back0 = np.zeros((h,w), np.float32)
    for row in range(blocksV):
            for col in range(blocksH):
                    currentblock = cv2.idct(Trans[row*B:(row+1)*B,col*B:(col+1)*B])
                    back0[row*B:(row+1)*B,col*B:(col+1)*B]=currentblock
    cv2.imwrite('Bilder/BackTransformed'+ str(Iteration) + '.jpg', back0)


if __name__ == "__main__":
    import sys
    
    start_time = time.perf_counter()
    Trans = dct2('Hamburger.jpg')
    print(Trans)
    Trans = koeffizientenAnpassung(Trans,64)
    Idct2(Trans,1)
    time.thread_time_ns
    end_time = time.perf_counter()
    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
    #for i in range(0,14):
    #    for x,y in enumerate(range(0,i)):
    #        print(str(x) + " : " + str(y-i) + " --> " + str(i))


