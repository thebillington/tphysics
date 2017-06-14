#Imports
from tphysics import Game, Rectangle, Circle

#Create the game window
g = Game("Pong Game", 600, 600, "grey")

#Create a list of walls
walls = [Rectangle(-290, 0, 20, 600), Rectangle(290, 0, 20, 600), Rectangle(0, 290, 600, 20), Rectangle(0, -290, 600, 20)]

#Set the walls fill colour to black and add them to the game
for i in range(len(walls)):
	
	#Set the colour
	walls[i].fill_colour = "black"
	
	#Add the wall to the game
	g.add_shape("wall{}".format(i), walls[i])
	
#Create the centre line
centre = Rectangle(0, 0, 5, 600)
#Set the centre square colour
centre.fill_colour = "black"

#Create the players
p1 = Rectangle(-250, 0, 30, 100)
p2 = Rectangle(250, 0, 30, 100)
#Set the player colours
p1.fill_colour = "red"
p2.fill_colour = "green"

#Create the ball
ball = Circle(0, 0, 5)
#Set the ball colour
ball.fill_colour = "white"

#Add the shapes
g.add_shape("player1", p1)
g.add_shape("player2", p2)
g.add_shape("centre", centre)
g.add_shape("ball", ball)

#Game loop
while True:
	#Update the game
	g.update()
