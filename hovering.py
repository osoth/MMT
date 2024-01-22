from ursina import *

app = Ursina()

# Erstellen Sie eine neue Szene
scene = Entity()

# Fügen Sie eine Ebene hinzu, die als Texturfläche dienen soll
texture = load_texture('white_cube')

# Erstellen Sie eine neue Ebene
plane = Entity(model='plane', texture=texture)

# Zentrieren Sie die Ebene in der Mitte der Szene
plane.x = 0
plane.y = 0
plane.z = 0

# Fügen Sie eine Kamera hinzu, um die Szene zu betrachten
camera = Entity(parent=scene, model='quad', scale=(1.7778, 1), color=color.gray)


# Schreiben Sie den Code, um die Ebene um ihre eigene Achse zu drehen
def update():
	pass


EditorCamera()
# Starten Sie die Anwendung
app.run()
