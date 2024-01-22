from ursina import *
from ursina.prefabs.slider import Slider
import dct

app = Ursina()

# Create a new scene
scene = Entity()
i = 0

# Create a new plane
parent_plane = Entity()
plane = Entity(parent=parent_plane, model='plane', texture='Bilder/BackTransformed1.jpg')

# Center the plane in the middle of the scene
plane.x = 0
plane.y = 0
plane.z = 0
plane.rotation_z = 0
plane.rotation_x = +90
plane.rotation_y = +160
Trans = dct.dct2('rickastley.jpg')

# Create a slider
slider = Slider(min=0, max=64, default_value=0, dynamic=True, position=(-0.25, -0.45))


def update():
	global i
	global Trans
	i = int(slider.value)
	Trans = dct.koeffizientenAnpassung(Trans, i)
	dct.Idct2(Trans, i)
	plane.texture = load_texture('Bilder/BackTransformed' + str(i) + '.jpg')
	invoke(setattr, plane, 'y', plane.y, delay=.25)

EditorCamera()
app.run()
