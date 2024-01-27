from PIL import Image
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


if __name__ == "__main__":
	app = Ursina()

	# Load the image
	img = Image.open('AlanTuring.jpg')
	pixels = img.load()

	# Get the size of the image
	width, height = img.size

	# Create a 3D structure of colored cubes
	for y in range(height):
		for x in range(width):
			r, g, b = pixels[x, y]
			color = rgb(r, g, b)  # Use the rgb function to create a color
			cube = Entity(model='cube', color=color, scale=(1, 1, 1), position=(x - width / 2, 0, y - height / 2))
			cube.collider = BoxCollider(cube)
	# Create pivotable camera
	origin = Entity()
	camera.parent = origin
	camera.z = -100

	#rotate camera on drag
	def update():
		origin.rotation_y += (
			mouse.velocity[0]
			
			#only rotate if right mouse button is being held
			* mouse.right * 200
			)
		
		origin.rotation_x -= (
			mouse.velocity[1]
			* mouse.right * 200
			)

	app.run()
	

	

	
