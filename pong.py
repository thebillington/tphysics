#Imports
from tphysics import Circle, Rectangle, Game
from random import randint

#Create a new game
g = Game("Empty Game", 600, 600, "light blue")

# Create a paddle for player one
paddleOne = Rectangle(-250, 0, 30, 100)
paddleOne.fill_colour = "green"
g.add_shape(paddleOne)

# Create a paddle for player two
paddleTwo = Rectangle(250, 0, 30, 100)
paddleTwo.fill_colour = "red"
g.add_shape(paddleTwo)

# Create the ball
ball = Circle(0, 0, 20)
ball.fill_colour = "yellow"
g.add_shape(ball)

# Store the x and y speed of the ball
ballSpeedX = 2
ballSpeedY = randint(-3, 3)

#Game loop
while True:

    # Move the ball
    ball.x += ballSpeedX
    ball.y += ballSpeedY

    # Check if the ball is going off the top of the screen
    if ball.y > 200 or ball.y < -200:
        ballSpeedY *= -1

    # Check if the ball collides with a paddle
    if ball.collide(paddleOne) or ball.collide(paddleTwo):
        ballSpeedX *= -1

    # Check if the ball goes off the left or right of the screen
    if ball.x > 300 or ball.x < -300:
        ball.x = 0
        ball.y = 0
        ballSpeedY = randint(-3, 3)

    # Check key presses
    if g.ispressed("w"):
        paddleOne.y += 1
    if g.ispressed("s"):
        paddleOne.y -= 1
    if g.ispressed("Up"):
        paddleTwo.y += 1
    if g.ispressed("Down"):
        paddleTwo.y -= 1

    # Update the game
    g.update()
