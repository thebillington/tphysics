#Imports
from tphysics import Rectangle, Game
from Tkinter import TclError

#Create a new game
g = Game("Platformer", 600, 600, "grey")

#Create the player
player = Rectangle(0, -250, 20, 20)
g.add_shape(player)

#Create the ground
ground = Rectangle(0, -290, 600, 20)
ground.fill_colour = "blue"
g.add_shape(ground)

#Fields
gravity = 0.5
fallspeed = -10
jumpspeed = 12
global xspeed
xspeed = 0
global yspeed
yspeed = 0
global jumping
jumping = False

#Create platforms
platforms = []
platforms.append(Rectangle(-100, -200, 50, 10))
platforms.append(Rectangle(-150, 50, 50, 10))
platforms.append(Rectangle(200, 0, 50, 10))
platforms.append(Rectangle(-200, 200, 50, 10))
platforms.append(Rectangle(0, -50, 50, 10))
for p in platforms:
	p.fill_colour = "white"
	g.add_shape(p)

#Handle jumps
def jump():
	global jumping
	global yspeed
	#If not jumping, jump
	if not jumping:
		yspeed = jumpspeed
		jumping = True
		
#Handle left and right key presses
def left():
	global xspeed
	if xspeed > -5:
		xspeed -= 1
def right():
	global xspeed
	if xspeed < 5:
		xspeed += 1
def stop():
	global xspeed
	xspeed = 0
	
#Function to resolve platform collisions
def platform(p):
	while p.collide(player):
		player.y += 0.1
		
#Add key listeners
g.addkeypress(jump, "space")
g.addkeypress(left, "Left")
g.addkeypress(right, "Right")
g.addkeypress(stop, "Down")

#Game loop
while True:
	
	#Move the player
	player.x += xspeed
	player.y += yspeed
	
	#Gravity
	if yspeed > fallspeed:
		yspeed -= gravity
	
	#If the player collided with the ground
	if player.collide(ground):
		jumping = False
		platform(ground)
		
	#Check each of the platforms for collisions
	for p in platforms:
		if p.collide(player):
			jumping = False
			platform(p)
			
	#Check collisions with platforms
	
	#Check for game exit
	try:
		g.update()
	except TclError:
		print("Program exited successfully.")
		break
