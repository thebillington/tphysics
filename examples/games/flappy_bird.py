from tphysics import Game, Rectangle, Circle
from random import randint

# Instantiate a tphysics game object and store in game variable
game = Game("Flappy Bird", "light blue")

# Instantiate a circle for the player and add it to the game
player = Circle(-300, 0, 20, "yellow")
game.add_shape(player)

# Set the initial player speed and max speed
player_speed = 0
max_speed = -10

# Generate a top pipe at a random y position
top_pipe = Rectangle(300, randint(200,750) , 20, 800, "green")
game.add_shape(top_pipe)

# Generate the bottom pipe, setting position to leave a gap of 150 between this and top pipe
bottom_pipe = Rectangle(300, top_pipe.y - 950 , 20, 800, "green")
game.add_shape(bottom_pipe)

# Set score to zero
score = 0

# Game loop
while True:

    # If the player is not at max velocity, increase the speed
    if player_speed > max_speed:
        player_speed -= 0.3

    # If the space key is pressed, set upward velocity of 6
    if game.ispressed("space") and player_speed < -2:
        player_speed = 6
    
    # Move the player by its speed
    player.y += player_speed
    
    # Move the pipes to the left
    top_pipe.x -= 2
    bottom_pipe.x -= 2

    # Check for a collision with either pipe or player falling off bottom
    if player.collide(top_pipe) or player.collide(bottom_pipe) or player.y < -400:

        # Reset the player position, speed and score
        player.y = 0
        player_speed = 0
        score = 0
        
        # Generate a new position for the pipes
        top_pipe.x = 450
        bottom_pipe.x = 450
        top_pipe.y = randint(200,600)
        bottom_pipe.y = top_pipe.y - 950
        
    # Check if the pipes have gone off the left of the screen
    if top_pipe.x < -450:

        # If they have, increase the score
        score += 1
        
        # Generate a new position for the pipes
        top_pipe.x = 450
        bottom_pipe.x = 450
        top_pipe.y = randint(200,600)
        bottom_pipe.y = top_pipe.y - 950

    # Show the score in the top left corner at (-300,300)
    game.write(-300, 300, f"Score: {score}", "black", 20)
    
    # Render the next frame
    game.update()
