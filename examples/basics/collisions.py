from tphysics import Game, Rectangle, Circle
from random import randint

# Create game object
game = Game("Collision Game", "light blue")

# Create player
player = Rectangle(0, 0, 20, 20, "green")
game.add_shape(player)

# Create obstacle at random position
obstacle = Circle(randint(-300,300), randint(-300,300), 5, "red")
game.add_shape(obstacle)

# Game loop
while True:

	# Check for key presses and move the player
    if game.ispressed("Left"):
        player.x -= 1
    if game.ispressed("Right"):
        player.x += 1
    if game.ispressed("Down"):
        player.y -= 1
    if game.ispressed("Up"):
        player.y += 1

	# Check for a collision
    if player.collide(obstacle):
		# Move the obstacle to a rand location between -300 and 300
        obstacle.x = randint(-300,300)
        obstacle.y = randint(-300,300)

	# Render the next frame
    game.update()