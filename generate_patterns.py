import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image


# Definieren Sie eine Funktion für die 2D-DCT
def dct2(a):
	return dct(dct(a.T, norm='ortho').T, norm='ortho')


# Definieren Sie eine Funktion für die 2D-iDCT
def idct2(a):
	return idct(idct(a.T, norm='ortho').T, norm='ortho')


if __name__ == "__main__":
	# Erstellen Sie eine 32x32-Matrix
	N = 32
	x = np.zeros((N, N))

	# Erzeugen Sie alle 1024 Grundmuster
	for u in range(N):
		for v in range(N):
			x[u, v] = 1
			pattern = idct2(x)
			if np.ptp(pattern) != 0:  # Überprüfen Sie, ob das Muster konstant ist
				pattern = (pattern - np.min(pattern)) / np.ptp(pattern)  # Normalisieren Sie das Muster auf den Bereich [0, 1]
			img = Image.fromarray(np.uint8(pattern * 255))  # Konvertieren Sie das Muster in ein Bild
			img.save(f'pattern_{u}_{v}.png')  # Speichern Sie das Bild
			x[u, v] = 0  # Setzen Sie den Wert zurück auf 0 für das nächste Muster
