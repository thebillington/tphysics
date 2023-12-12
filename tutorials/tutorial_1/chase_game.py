from tphysics import Game, Rectangle, Circle
from random import randint

# Create a new game window
game = Game("Chase Game", "black")

# Create the player game object in the middle of the screen
player = Rectangle(0, 0, 20, 20, "light blue")
game.add_shape(player)

# Create a coin with a random position between -250 and 250 on x and y
coin = Circle(randint(-250,250), randint(-250,250), 5, "yellow")
game.add_shape(coin)

# Create enemy with a random position
enemy = Circle(randint(-250,250), randint(-250,250), 10, "red")
game.add_shape(enemy)

# Set the initial score to zero
score = 0

# Set the player and enemy speed
player_speed = 2
enemy_speed = 1

# Game loop which will contain all of our logic
while True:

    # Check key presses
    if game.ispressed("Right"):
        player.x += player_speed
    if game.ispressed("Left"):
        player.x -= player_speed
    if game.ispressed("Up"):
        player.y += player_speed
    if game.ispressed("Down"):
        player.y -= player_speed

    # Enemy movement checks
    if enemy.x < player.x:
        enemy.x += enemy_speed
    if enemy.x > player.x:
        enemy.x -= enemy_speed
    if enemy.y < player.y:
        enemy.y += enemy_speed
    if enemy.y > player.y:
        enemy.y -= enemy_speed

    # Check if the player has collected the coin
    if player.collide(coin):

        # If so, add to score and generate new coin position
        score += 1
        coin.x = randint(-250, 250)
        coin.y = randint(-250, 250)

        # Check if the score is divisible by 5
        if score % 5 == 0:

            # If so, increase player and enemy speed
            player_speed += 1
            enemy_speed += 1

    # Check if the enemy has hit the player
    if enemy.collide(player):

        # Reset the player position and score
        score = 0
        player.x = 0
        player.y = 0

        # Generate new coin and enemy positions
        coin.x = randint(-250,250)
        coin.y = randint(-250,250)
        enemy.x = randint(-250,250)
        enemy.y = randint(-250,250)

        # Reset player and enemy speed
        player_speed = 2
        enemy_speed = 1

    # Show the score
    game.write(-300, 300, f"Score: {score}", "white", 20)

    # Each time the game loop runs, at the end, render a new frame
    game.update()
