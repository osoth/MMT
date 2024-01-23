import numpy as np

import matplotlib.pyplot as plt
import cv2 as cv2
import time
import math
######################
# 
#  Das programm soll später in den haupt script importiert werden und die dct2 funktion aufgerufen werden
#  um dann die dct matrix zu erstellen, welche für die komprimierung bearbeitet werden kann.
#
#  die matrix heißt Trans und wird dann wieder verwendet um ein Bild zu geben. Dieses ausgebene bilde werden
#  dann auf ein Objekt projezuiert damit man es sehen kann. Durch eine Update funktion wird dieses bilde
#  dann immer ausgetauscht mit dem entsprechenden angepassten komprimerungskoeffizienten
#
#################################


def patterns():
    #DCT matrix
    N=8 # matrix shape: 8*8
    DCT=np.zeros((N,N),np.float32)
    for m in range(N):
        for n in range(N):
            if m==0:
                DCT[m][n]=math.sqrt(1/N)
            else:
                DCT[m][n]=math.sqrt(2/N)*math.cos((2*n+1)*math.pi*m/(2*N))

# DCT basis image
    basis=np.zeros((N*N,N*N), np.float32)
    for m in range(N):
        for n in range(N):
            pos_m=m*N
            pos_n=n*N
            DCT_v=DCT[m,:].reshape(-1,1)
            DCT_T_h=DCT.T[:,n].reshape(-1,N)
            basis[pos_m:pos_m+N,pos_n:pos_n+N]=np.matmul(DCT_v,DCT_T_h)

# Center values
    basis+=np.absolute(np.amin(basis))
    scale=np.around(1/np.amax(basis),decimals=3)
    for m in range(basis.shape[0]):
        for n in range(basis.shape[1]):
            basis[m][n]=np.around(basis[m][n]*scale,decimals=3)
    cv2.imwrite('Bilder/DCT/Base.jpg',basis)

    plt.figure(figsize=(4,4))
    plt.gray()
    plt.axis('off')
    plt.title('DCT Basis Image')
    plt.imshow(basis,vmin=0)
    plt.savefig(fname='Bilder/DCT/Base.jpg',dpi='figure')

# hier wird die dct matrix übergeben und ein wert der dann die kompriemierung bestimmt. muss noch gemacht werden
def koeffizientenAnpassung(matrix, komprimierungsIndex):
    code = range(0,64)  #bis 11 eingetragen
    # per hand eintragen :/
    item = [(7,7),(6,7),(7,6),(7,5),(6,6),(5,7),(4,7),(5,6),(6,5),(7,4),(7,3),(6,4),(5,5),(4,6),(3,7),(2,7),(3,6),(4,5),(5,4),(6,3),(7,2),(7,1),(6,2),(5,3),(4,4),(3,5),(2,6),(1,7),(0,7),(1,6),(2,5),(3,4),(4,3),(5,2),(6,1),(7,0),(6,0),(5,1),(4,2),(3,3),(2,4),(1,5),(0,6),(0,5),(1,4),(2,3),(3,2),(4,1),(5,0),(4,0),(3,1),(2,2),(1,3),(0,4),(0,3),(1,2),(2,1),(3,0),(2,0),(1,1),(0,2),(0,1),(1,0),(0,0)]
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
    back0 = np.zeros((h,w), np.float32)
    for row in range(blocksV):
            for col in range(blocksH):
                currentblock = matrix[row*B:(row+1)*B,col*B:(col+1)*B]
            # diese schleife um alle notwendigen matrix einträge im block auf null zu setzten
                for i in range(0,komprimierungsIndex):
                # die Variable i wählt aus dem dictZipped das feld und die Zweite [0] 
                        # wählen den eintrag in der liste
                        currentblock[dictZipped[i][0],dictZipped[i][1]] = 0 
                        matrix[row*B:(row+1)*B,col*B:(col+1)*B] = currentblock
                        back0[row*B:(row+1)*B,col*B:(col+1)*B]=currentblock
                        #print("index:"+str(dictZipped[i][0])+str(dictZipped[i][1])+ "  " +str(currentblock[dictZipped[i][0],dictZipped[i][1]])) #for debugging purpise

    cv2.imwrite('Bilder/Pattern/Pattern'+ str(komprimierungsIndex)+'.jpg', back0)
    return matrix
    
# Generiert die Pattern von der Standard dct
def Dct2(fn3):
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
    cv2.imwrite('Transformed.jpg', img1)
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
    patterns()
    end_time = time.perf_counter()
    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
    #for i in range(0,14):
    #    for x,y in enumerate(range(0,i)):
    #        print(str(x) + " : " + str(y-i) + " --> " + str(i))


