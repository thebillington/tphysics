from tphysics import Game, Rectangle, Circle
from random import randint

# Create a new game object
game = Game("Apple Catch", "light blue")

# Create a player rectangle
player = Rectangle(0, -200, 60, 30, "brown")
game.add_shape(player)

# Create a circle for the apple
apple = Circle( randint(-250,250), 300, 10, "red")
game.add_shape(apple)

# Set initial score to zero
score = 0

# Initialise the player and apple speeds
player_speed = 2
apple_speed = 3

# Game loop
while True:

    # Move the player in response to key presses
    if game.ispressed("Right"):
        player.x += player_speed
    if game.ispressed("Left"):
        player.x -= player_speed

    # Make the apple fall on every frame
    apple.y -= apple_speed

    # Check if the player has caught the apple
    if player.collide(apple):

        # Generate a new apple position
        apple.x = randint(-250,250)
        apple.y = 300

        # Increase the score and speed
        score += 1
        player_speed += 1
        apple_speed += 1

    # Check if the apple has fallen off the bottom of the screen
    if apple.y < -350:
        
        # Generate a new apple position
        apple.x = randint(-250,250)
        apple.y = 300
        
        # Reset the score and speeds
        score = 0
        player_speed = 2
        apple_speed = 3

    # Show the score in game
    game.write(-250, 250, f"Score: {score}", "black", 20)

    # Render the next frame
    game.update()
