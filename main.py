from PIL import Image
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


class CustomController(FirstPersonController):
	def update(self):
		super().update()

		if held_keys['space']:
			self.y += 2 * time.dt  # move up
		if held_keys['left shift']:
			self.y -= 2 * time.dt  # move down


if __name__ == "__main__":
	app = Ursina()

	# Load the image
	img = Image.open('rickastley.jpg')
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

	# Add a custom first-person controller
	player = CustomController()
	player.y = 10
	player.gravity = 0
	player.speed = 10  # increase movement speed

	app.run()
