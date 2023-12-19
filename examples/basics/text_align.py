from tphysics import Game

# Create a game object
game = Game("Score Game", "red")

# Game Loop
while True:

	# Write aligned text using write(x, y, text, colour, size, align)
	game.write(0, 100, "Left align", "black", 20)
	game.write(0, 50, "Center align", "black", 20, align="center")
	game.write(0, 0, "Right align", "black", 20, align="right")

	# Update the game
	game.update()