from ursina import *
from ursina.prefabs.slider import Slider
import cv2
import dct

i = 0
plane_visible = True
plane2_visible = True
plane3_visible = True



def update():
	global i
	i = int(slider.value)
	plane.texture = load_texture('Bilder/BackTransformed' + str(i) + '.jpg')
	invoke(setattr, plane, 'y', plane.y, delay=.25)
	plane3.texture = load_texture('Bilder/Pattern/Pattern'+str(i)+'.jpg')
	invoke(setattr, plane, 'y', plane3.y, delay=.25)


	# camera navigation
	origin.rotation_y += (
		mouse.velocity[0]
		
		#only rotate if right mouse button is being held
		* mouse.right * -200
		)	
	origin.rotation_x -= (
		mouse.velocity[1]
		* mouse.right * -200
		)


def input(key):
	if held_keys['escape']:  # if ESC is pressed
		options_menu.enabled = not options_menu.enabled
	#wir brauchen eine Aufräum funktion aber q ist doof und escape ist belegt
	if key == 'q':
		for d in range(0,65):
			os.remove('Bilder/BackTransformed'+str(d)+'.jpg')
			os.remove('Bilder/Pattern/Pattern'+str(d)+'.jpg')
			print('Bilder/Pattern/Pattern'+str(d)+'.jpg removed')
		quit()


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

def toggle_plane3():
	global plane3_visible
	plane3.visible = not plane3.visible
	plane3_visible = not plane3_visible
	plane3_button.text = 'Toggle Plane3 (Currently: ' + ('Visible' if plane3_visible else 'Hidden') + ')'

def popup(text):
	global popupText
	popupText.text = text
	popupText.background = True
	popupText.visible = True


if __name__ == "__main__":
	import os
	app = Ursina()
	Trans = dct.Dct2('rickastley.jpg')
	for k in range(0, 64):
		Trans1 = dct.koeffizientenAnpassung(Trans, k)
		dct.Idct2(Trans1, k)
	# Create a new scene
	scene = Entity()
	start_screen = Text(text='Press ESC to open the options menu\nUse mouse or touchpad to pivot around', color=color.white, origin=(0, 0), background=True)
	invoke(destroy, start_screen, delay=6)
	# Create a new plane
	parent_plane = Entity()
	plane = Entity(position=(0, 0, 3), parent=parent_plane, model='plane', texture='Bilder/BackTransformed0.jpg')
	plane2 = Entity(position=(0, 0, 2), parent=parent_plane, model='plane', texture='Bilder/BackTransformed0.jpg')
	plane3 = Entity(position=(0, 0, 1), parent=parent_plane, model='plane', texture='Bilder/Pattern/Pattern0.jpg')
	plane4 = Entity(position=(0, 0, 4), parent=parent_plane, model='plane', texture='Bilder/DCT/Base.jpg')
	plane2.rotation_x = +90
	plane2.rotation_y = +180
	# Center the plane in the middle of the scene
	plane.x = 0
	plane.y = 0
	plane.z = 0
	plane.rotation_z = +180
	plane.rotation_x = +90
	plane3.rotation_x = +90
	plane3.rotation_y = +180
	plane4.rotation_x = +90
	plane4.rotation_y = +180

	# Create a slider
	slider = Slider(min=0, max=65, default_value=0, dynamic=True, position=(-0.25, -0.45))

	# Create options menu
	options_menu = Entity(parent=camera.ui, enabled=False)
	plane_button = Button(position=(-0.6, 0.25), scale=(0.5, 0.2), parent=options_menu, text='Toggle Plane (Currently: Visible)', on_click=toggle_plane)
	plane2_button = Button(position=(-0.6, 0), scale=(0.5, 0.2), parent=options_menu, text='Toggle Plane2 (Currently: Visible)', on_click=toggle_plane2)
	plane3_button = Button(position=(-0.6, -0.25), scale=(0.5, 0.2), parent=options_menu, text='Toggle Plane3 (Currently: Visible)', on_click=toggle_plane3)
	#button1 = Button(text='Button 1', color=color.azure, scale=(0.1, 0.05), position=(-0.2, 0.2), on_click=on_button1_click)

	popupText = Text(text="", position=(0.3,0.4), color=color.white, background=True, visible=False, size=0.02, line_height=1.4)

	popup1 = 'Komprimiertes Bild. Insbesondere bei hoher Kompressionsrate wird die 8x8 Segmentierung durch die scharfen Kanten deutlich. Bei einem hochauflösenden Bild sind die Kanten dass, was wir als "Pixelig" wahrnehmen. '
	popup2 = "Jeder 8x8 Block des Bildes wird als Linearkombination der Quantisierungstabelle dargestellt. Die Ebene stellt dabei den Wert der Linearfaktoren graphisch dar (1 = Weiß, 0 = Schwarz). Dabei treten hohe Koeffizienten vor allem in den niedrigen Frequenzen, dass heißt in der linken oberen Ecke auf. Da lediglich die Koeffizienten ungleich 0 gespeichert werden müssen um das Bild rekonstruieren zu können, ist der Speicherbedarf des Zielbildes kleiner als beim Original. Die mögliche Kompressionsrate für ein zufriedenstellendes Resultat ist dabei vom Originalbild abhängig. Grundsätzlich lassen sich Bilder mit großen Flächen (z.B. einfarbige Wand) stärker kompremieren, als unruhige Bilder (z.B. weißes Rauschen), da weniger Linearfaktoren benötigt werden (größere Unterschiede der Koeffizienten). Über den Slider lassen sich die Koeffizienten stufenweise, von den Frequenzen absteigend, null setzen. "
	popup3 = "Originalbild als Graustufenbild. Das Bild wird in 8x8 Blöcke segmentiert, so dass die DCT angewendet werden kann. Da es sich um ein Bild handelt wird der zweidimensionale DCT-2 angewandt. "
	popup4 = "Quantisierungstabelle: Unabhängig vom Bild wendet jede DCT-2 diese Qunatisierungstabelle an. Die 8x8 Einträge bestehen aus je 8x8 Pixeln und representieren vertikale und horizontale Cosinus Schwingungen in unterschiedlichen Frequenzen. Die Einträge berechnen sich durch die Multiplikation zweier, zueinander senkrechter cos-Funktionen auf dem Intervall 0 bis Pi. Der Farbwert jedes Subpixels ist dabei der Wert der Funktion an der mittleren Position des Feldes, wobei 1 als Weiß und -1 als Schwarz interpretiert werden. Die Frequenzen nehmen von Links oben nach rechts unten zu. Der Block in der linken oberen Ecke wiederspiegelt den Gleichanteil und somit die mittlere Helligkeit des 8x8 Blocks des Bildes. Jeder 8x8 Schwarz-Weiß-Block kann als Linearkombination dieser 64 Einträge dargestellt werden. "

	# Add new line to popups after every 4 words
	def add_new_line(popup):
		popup = popup.split()
		n = 35
		newpopup = ""
		while popup:
			tmp = ""
			while len(tmp) < n:
				if not popup:
					break
				tmp += popup.pop(0) + " "
			newpopup += tmp + "\n"
		return  newpopup
	
	popup1 = add_new_line(popup1)
	popup2 = add_new_line(popup2)
	popup3 = add_new_line(popup3)
	popup4 = add_new_line(popup4)

	
	popup_button = Button(position=(0.5, 0.01, 0.5), rotation=(90,180,0), scale=(0.15, 0.15), color=color.turquoise, parent=plane, on_click=Func(popup, popup1))
	popup_button2 = Button(position=(0.5, 0.01, 0.5), rotation=(90,180,0), scale=(0.15, 0.15), color=color.turquoise, parent=plane2, on_click=Func(popup, popup3))
	popup_button3 = Button(position=(0.5, 0.01, 0.5), rotation=(90,180,0), scale=(0.15, 0.15), color=color.turquoise, parent=plane3, on_click=Func(popup, popup2))
	popup_button4 = Button(position=(0.5, 0.01, 0.5), rotation=(90,180,0), scale=(0.15, 0.15), color=color.turquoise, parent=plane4, on_click=Func(popup, popup4))

	# Create start screen
	origin = Entity()
	camera.parent = origin
	camera.z = -10
	camera.rotation_z = 180
	#EditorCamera(position=(2.5, 0, 15), rotation=(0, 10, 180))
	app.run()
