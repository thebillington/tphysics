from tphysics import Game, Rectangle

# Create game object
game = Game("Key Press Game", "light blue")

# Create player object
player = Rectangle(0, 0, 20, 20, "green")
game.add_shape(player)

# Game loop
while True:

	#Check whether a specific key is being pressed
	if game.ispressed("Right"):
		#Change the x speed
		player.x += 1

	# Update the game
	game.update()