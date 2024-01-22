from ursina import *
from ursina import time
import dct

app = Ursina()
# Erstellen Sie eine neue Szene
scene = Entity()
clock_1 = 0.0
i = 0

# Erstellen Sie eine neue Ebene
parent_plane = Entity()
plane = Entity(parent=parent_plane, model='plane', texture='Bilder/BackTransformed1.jpg')

# Zentrieren Sie die Ebene in der Mitte der Szene
plane.x = 0
plane.y = 0
plane.z = 0
plane.rotation_z = 0
plane.rotation_x = +90
plane.rotation_y = +160
Trans = dct.dct2('rickastley.jpg')


def input(key, Trans=Trans):
	global i
	if (key == 'space'):
		Trans = dct.koeffizientenAnpassung(Trans, 10)
		Trans = dct.Idct2(Trans, 10)
		plane.texture = load_texture('rickastley.jpg')
		invoke(setattr, plane, 'y', plane.y, delay=.25)
		i += 1
		print(i)


# Schreiben Sie den Code, um die Ebene um ihre eigene Achse zu drehen
def update():
	pass


EditorCamera()
# Starten Sie die Anwendung
app.run()
