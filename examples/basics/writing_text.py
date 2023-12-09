from tphysics import Game

# Create a game object
game = Game("Score Game", "red")

# Create a score variable
score = 0

# Game Loop
while True:

	# Write the score using write(x, y, text, colour, size)
	game.write(-100, 100, f"Score: {score}", "black", 20)

	# Add 1 to the score
	score += 1

	# Update the game
	game.update()