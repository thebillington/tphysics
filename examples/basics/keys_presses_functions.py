from tphysics import Game, Circle

# Create a game object
game = Game("Higher Order Keys Example", "light blue")

# Create a player
player = Circle(0, 0, 10, "orange")
game.add_shape(player)

#Create a function to handle the up key press
def up():
	#Move the player up
	player.y += 1
	
#Pass the function to the game object
game.addkeypress(up, "Up")

# Game loop
while True:

	# Update the game
	game.update()