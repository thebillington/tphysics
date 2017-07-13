#Imports
from tphysics import Game, Rectangle, Circle
from random import randint
from tkinter import TclError

#Create the game window
g = Game("Pong Game", 600, 600, "grey")

#Create a list of walls
walls = [Rectangle(-290, 0, 20, 600), Rectangle(290, 0, 20, 600), Rectangle(0, 290, 600, 20), Rectangle(0, -290, 600, 20)]

#Set the walls fill colour to black and add them to the game
for w in walls:
	#Set the colour
	w.fill_colour = "black"
	#Add the wall to the game
	g.add_shape(w)
	
#Create the centre line
centre = Rectangle(0, 0, 5, 600)
#Set the centre square colour
centre.fill_colour = "black"

#Create variable to hold whether game is running
global running
running = False

#Create the players
p1 = Rectangle(-250, 0, 30, 100)
p2 = Rectangle(250, 0, 30, 100)
#Set the player colours
p1.fill_colour = "red"
p2.fill_colour = "green"

#Create the ball
ball = Circle(0, 0, 10)
#Set the ball colour
ball.fill_colour = "white"

#Add the shapes
g.add_shape(p1)
g.add_shape(p2)
g.add_shape(centre)
g.add_shape(ball)

#Set the paddle speed
paddle_speed = 20

#Create functions to deal with key presses
def w():
	p1.y += paddle_speed
	while p1.collide(walls[2]):
		p1.y -= 1
def s():
	p1.y -= paddle_speed
	while p1.collide(walls[3]):
		p1.y += 1
def up():
	p2.y += paddle_speed
	while p2.collide(walls[2]):
		p2.y -= 1
def down():
	p2.y -= paddle_speed
	while p2.collide(walls[3]):
		p2.y += 1
def space():
	global running
	running = not running
	
#Create a function to reset the game
def reset():
	p1.y = 0
	p2.y = 0
	ball.x = 0
	ball.y = 0
	speed = [3, randint(-2, 2)]
	
#Add the functions to key listeners
g.addkeypress(w, "w")
g.addkeypress(s, "s")
g.addkeypress(up, "Up")
g.addkeypress(down, "Down")
g.addkeypress(space, "space")

#Set the speed of the ball
speed = [3, randint(-2, 2)]
xdirection = 1

#Game loop
while True:
	
	#If the game is running
	if running:
		
		#Change the balls position
		ball.x += speed[0] * xdirection
		ball.y += speed[1]
		
		#If the ball collides with a top wall
		for i in range(2):
			if walls[i].collide(ball):
				running = False
				reset()
		for i in range(2, 4):
			if walls[i].collide(ball):
				speed[1] = -speed[1]
				
		#If the ball hits the top of a paddle
		if p1.collide(ball) == 1 or p2.collide(ball) == 1:
			speed[0] += 1
			xdirection = -xdirection
				
		#If the ball hits the top of a paddle
		if p1.collide(ball) == 2 or p2.collide(ball) == 2:
			speed[0] += 1
			xdirection = -xdirection
			
		#If the ball hits the bottom of a paddle
		if p1.collide(ball) == 3 or p2.collide(ball) == 3:
			speed[0] += 1
			speed[1] = -speed[1]
			
		#If the ball hits the corner of a paddle
		if p1.collide(ball) == 4 or p2.collide(ball) == 4:
			speed[0] += 1
			xdirection = -xdirection
			speed[1] = -speed[1]
	
	#If the window hasn't been closed update the game
	try:
		g.update()
	except TclError:
		print("Program closed successfully.")
		break
