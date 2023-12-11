from tphysics import *
from random import randint

# Create a new game object
game = Game("Snowglobe", "dark blue")

# Get the screen width and height
screen_width, screen_height = game.get_window_size()

# Create an empty list to hold our snowflakes, and the speed of each snowflake
snowflakes = []
speeds = []

# Run the code inside the loop 300 times, to create 300 snowflakes and add each to the list
for i in range(300):

    # Generate a random horizontal position for this snowflake
    # between left and right side of screen, based on screen_width
    # Remember that an x value of 0 is in the centre of the screen
    # so we have to use half the screen width to the left and right
    x = randint(-int(screen_width/2),int(screen_width/2))

    # Starting at the top of the screen, generate a y value randomly
    # between 30 and 500, to make each snowflake start at a different height
    y = int(screen_height/2) + randint(30, 500)

    # Generate a random size for the snowflake
    size = randint(5, 10)

    # Generate a random speed and store it in the speeds list
    speeds.append(randint(2,5))
    
    # Create the snowflake circle object, add it to the game and snowflakes list
    snowflake = Circle(x,y,size,"white")
    game.add_shape(snowflake)
    snowflakes.append(snowflake)

# Game loop - this is an infinite loop which we use to update our snowflakes every frame
while True:

    # Iterate from i = 0 to the length of the snowflakes list, to access each snowflake individually
    for i in range(len(snowflakes)):

        # Change the y position of the snowflake by its speed
        snowflakes[i].y -= speeds[i]

        # Check if the snowflake has fallen off the bottom of the screen
        if snowflakes[i].y < -int(screen_height/2) - snowflakes[i].radius:

            # If it has, generate a brand new position, radius and speed
            snowflakes[i].x = randint(-int(screen_width/2),int(screen_width/2))
            snowflakes[i].y = int(screen_height/2) + randint(30, 500)
            snowflakes[i].radius = randint(5, 10)
            speeds[i] = randint(2,5)
    
    # Generate the next frame and show it
    game.update()
