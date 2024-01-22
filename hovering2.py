from ursina import *
from ursina.prefabs.slider import Slider
import cv2
import dct

i = 0
plane_visible = True
plane2_visible = True


def update():
	global i
	i = int(slider.value)
	plane.texture = load_texture('Bilder/BackTransformed' + str(i) + '.jpg')
	invoke(setattr, plane, 'y', plane.y, delay=.25)


def input(key):
	if held_keys['escape']:  # if ESC is pressed
		options_menu.enabled = not options_menu.enabled


def toggle_plane():
	global plane_visible
	plane.visible = not plane.visible
	plane_visible = not plane_visible
	plane_button.text = 'Toggle Plane (Currently: ' + ('Visible' if plane_visible else 'Hidden') + ')'


def toggle_plane2():
	global plane2_visible
	plane2.visible = not plane2.visible
	plane2_visible = not plane2_visible
	plane2_button.text = 'Toggle Plane2 (Currently: ' + ('Visible' if plane2_visible else 'Hidden') + ')'


if __name__ == "__main__":
	app = Ursina()

	# Create a new scene
	scene = Entity()
	start_screen = Text(text='Press ESC to open the options menu\nUse mouse or touchpad to pivot around', color=color.white, origin=(0, 0), background=True)
	invoke(destroy, start_screen, delay=6)
	img = cv2.imread('rickastley.jpg', 0)
	cv2.imwrite('Bilder/original.jpg', img)
	# Create a new plane
	parent_plane = Entity()
	plane = Entity(position=(0, 0, 0), parent=parent_plane, model='plane', texture='Transformed.jpg')
	plane2 = Entity(position=(0, 0, 1), parent=parent_plane, model='plane', texture='Bilder/original.jpg')
	plane2.rotation_x = +90
	plane2.rotation_y = +180
	# Center the plane in the middle of the scene
	plane.x = 0
	plane.y = 0
	plane.z = 0
	plane.rotation_z = +180
	plane.rotation_x = +90
	Trans = dct.Dct2('rickastley.jpg')
	for k in range(0, 64):
		Trans1 = dct.koeffizientenAnpassung(Trans, k)
		dct.Idct2(Trans1, k)

	# Create a slider
	slider = Slider(min=0, max=64, default_value=0, dynamic=True, position=(-0.25, -0.45))

	# Create options menu
	options_menu = Entity(parent=camera.ui, enabled=False)
	plane_button = Button(position=(-0.5, -0.3), parent=options_menu, text='Toggle Plane (Currently: Visible)', on_click=toggle_plane)
	plane2_button = Button(position=(-0.5, 0), parent=options_menu, text='Toggle Plane2 (Currently: Visible)', on_click=toggle_plane2)

	# Create start screen

	EditorCamera(position=(2.5, 0, 15), rotation=(0, 10, 180))
	app.run()