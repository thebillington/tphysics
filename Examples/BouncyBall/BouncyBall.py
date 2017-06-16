#Imports
from tphysics import VerletCircle, Rectangle, Point, Game
from Tkinter import TclError

#Create the game
g = Game("Bouncy Ball", 600, 600, "grey")

#Create the walls
walls = [Rectangle(-290, 0, 20, 600), Rectangle(290, 0, 20, 600), Rectangle(0, 290, 600, 20), Rectangle(0, -290, 600, 20)]

#Add the walls to the game
for w in walls:
	g.add_shape(w)
	
#Create a bouncy ball
ball = VerletCircle(0, 0, 50, 10, 5)
g.add_shape(ball)

#Set the physics constants
elasticity = 0.8
friction = 0.2
gravity = 0.6
max_fall = 10

#Create a boolean to store whether the ball was clicked
global clicked
clicked = False

#Create a boolean to store whether the game is running
global running
running = True

#Functions to handle mouse clicks
def click(x, y):
	
	#Get the globals
	global clicked
	global running
	#Check whether the click collides with the ball
	if ball.collide(Point(x,y)) and not clicked:
		#Set clicked to true
		clicked = True
		running = False
	elif clicked:
		#Set the current position of the ball to the mouse x and y
		ball.x = x
		ball.y = y
		clicked = False
		running = True
		
#Add click listeners to the game
g.addclick(click)

#Game loop
while True:
	
	#If the game is running
	if running:
	
		#Update the ball
		ball.update()
		
		#Implement gravity
		if ball.getyspeed() > -max_fall:
			#Change the y speed
			ball.setyspeed(ball.getyspeed() - gravity)
		
		#If the ball hits a side wall
		for i in range(2):
			if ball.collide(walls[i]) != 0:
				#Bounce on the x
				ball.bouncex(elasticity)
		
		#If the ball hits a vertical wall
		for i in range(2,4):
			if ball.collide(walls[i]):
				#Bounce on the y
				ball.bouncey(elasticity, friction)
	
	#If the window hasn't been closed update the game
	try:
		g.update()
	except TclError:
		print("Program closed successfully.")
		break
