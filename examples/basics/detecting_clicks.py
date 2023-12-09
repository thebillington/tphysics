from tphysics import Game, Rectangle

# Create game object
game = Game("Click Game", "light blue")

# Create a player
player = Rectangle(0, 0, 20, 20, "green")
game.add_shape(player)

#Create a function to handle the click
def click(x, y):
	
	# Move player to click location
	player.x = x
	player.y = y

#Add the click listener
game.addclick(click)

# Game loop
while True:

	# Update the game
	game.update()