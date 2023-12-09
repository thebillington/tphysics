from tphysics import Game, Rectangle, Circle

#Create a new game object and store it in a variable
game = Game("Basic Game", "light blue")

#Create a player Rectangle(x, y, width, height, colour)
player = Rectangle(0, 0, 20, 20, "orange")
game.add_shape(player)

# Store the direction
direction = 1

# Game loop
while True:

	# Move the player by direction
	player.x += direction

	# If player goes above x=100 or below x=-100, flip direction
	if player.x > 100 or player.x < -100:
		direction = direction = direction * -1

	# Render the next frame
	game.update()