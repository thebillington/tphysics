from tphysics import *
from random import randint

# Create game object
game = Game("Aim Training", "white", fullscreen=True)

# Get screen size
screen_width, screen_height = game.get_window_size()

# Create a circle target in the bounds of the screen
target = Circle(
    randint(-int(screen_width/2) + 100, int(screen_width/2) - 100),
    randint(-int(screen_height/2) + 100, int(screen_height/2) - 100),
    10,
    "red"
)
game.add_shape(target)

# Track the score and make it a global variable
global score
score = 0

# Track the high score
high_score = 0

# Track the number of targets left in the game
global targets_remaining
targets_remaining = 30 

# Create a click handler
def click(x,y):
   
   # Check if the click collides with the target
   if Point(x,y).collide(target):
        
        # Take one from number of remaining targets
        global targets_remaining
        targets_remaining -= 1
      
        # Calculate the value based on the radius of the target
        target_value = 150 - target.radius
    
        # Fetch the score variable and add the correct amount
        global score
        score += target_value

        # Check if we still have targets left
        if targets_remaining > 0:

            # Generate a new location for the target and reset radius
            target.x = randint(-int(screen_width/2) + 100, int(screen_width/2) - 100)
            target.y = randint(-int(screen_height/2) + 100, int(screen_height/2) - 100)
            target.radius = 10

        # If we don't have any targets left
        else:

            # Remove the target from the game
            game.remove_shape(target)

# Add the click handler to the game
game.addclick(click)

# Game loop
while True:

    # Check if we need to increase the size of the target
    if target.radius < 100:
      target.radius += 1

    # Check if high score needs updating
    if score > high_score:
        high_score = score

    # Show the score
    game.write(
       -int(screen_width/2) + 20,
       int(screen_height/2) - 30,
       f"Score: {score}",
       "black",
       20
    )

    # Show the high score
    game.write(
       -int(screen_width/2) + 20,
       int(screen_height/2) - 60,
       f"High Score: {high_score}",
       "black",
       20
    )

    # Check if game has finished
    if targets_remaining == 0:
    
        # Write end screen text
        game.write(-200, 0, f"Your score: {score} - Press 'r' to play again", "black", 30)

        # Check for r press
        if game.ispressed("r"):

            # Set score to 0
            score = 0

            # Reset number of targets
            targets_remaining = 30

            # Generate a new location for the target and reset radius
            target.x = randint(-int(screen_width/2) + 100, int(screen_width/2) - 100)
            target.y = randint(-int(screen_height/2) + 100, int(screen_height/2) - 100)
            target.radius = 10

            # Add target back to game
            game.add_shape(target)

    # Render the next frame
    game.update()
