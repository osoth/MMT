from ursina import *
from ursina.prefabs.slider import Slider
import cv2
import dct

app = Ursina()

# Create a new scene
scene = Entity()
i = 0
img = cv2.imread('rickastley.jpg', 0)
cv2.imwrite('Bilder/original.jpg', img)
# Create a new plane
parent_plane = Entity()
plane = Entity(position=(0, 0, 0), parent=parent_plane, model='plane', texture='Bilder/BackTransformed1.jpg')
plane2 = Entity(position=(0, 0, 5), parent=parent_plane, model='plane', texture='Bilder/original.jpg')
plane2.rotation_x = +90
plane2.rotation_y = +180
# Center the plane in the middle of the scene
plane.x = 0
plane.y = 0
plane.z = 0
plane.rotation_z = +180
plane.rotation_x = +90
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


EditorCamera(position=(0, 0, 15), rotation=(0, 0, 180))
app.run()
