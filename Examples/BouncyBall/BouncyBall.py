#Imports
from tphysics import VerletCircle, Rectangle, Game
from Tkinter import TclError

#Create the game
g = Game("Bouncy Ball", 600, 600, "grey")

#Create the walls
walls = [Rectangle(-290, 0, 20, 600), Rectangle(290, 0, 20, 600), Rectangle(0, 290, 600, 20), Rectangle(0, -290, 600, 20)]

#Add the walls to the game
for w in walls:
	g.add_shape(w)
	
#Create a bouncy ball
ball = VerletCircle(0, 0, 10, 10, 50)
g.add_shape(ball)

#Set the physics constants
elasticity = 1
friction = 0
gravity = 0.2
max_fall = 10
	
#Game loop
while True:
	
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
