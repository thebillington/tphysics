from tphysics import Game, Rectangle, Circle

#Create a new game object and store it in a variable
game = Game("Basic Game", "light blue")

#Create a player Rectangle(x, y, width, height, colour)
player = Rectangle(-100, 100, 20, 50, "orange")
game.add_shape(player)

#Create an obstacle Circle(x, y, radius, colour)
obstacle = Circle(100, 100, 50, "green")
game.add_shape(obstacle)

# Game loop
while True:

	# Render the next frame
	game.update()