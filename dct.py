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


# brechnet die dct matrix des bildes. muss nur einmalig ausgeführt werden damit
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

# hier wird die dct matrix übergeben und ein wert der dann die kompriemierung bestimmt. muss noch gemacht werden
def koeffizientenAnpassung(matrix, komprimierung):

    pass

# nimmt die dct matrix und verwandelt sie in ein bild zurück das dann auf einen entity projeziert wird
def Idct2(Trans):
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
    cv2.imwrite('BackTransformed.jpg', back0)


if __name__ == "__main__":
    import sys
    
    start_time = time.perf_counter()
    Trans = dct2('Hamburger.jpg')
    print(Trans)
    Idct2(Trans)
    time.thread_time_ns
    end_time = time.perf_counter()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
