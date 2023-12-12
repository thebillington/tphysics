# Introduction

Welcome to the first tutorial in our *learning tphysics* series.

In this tutorial we will be building a simple chase game, where the player controls their character using the arrow keys whilst an enemy chases them down. The player will need to collect coins as they go, but be careful! The game gets faster over time, making it more difficult as you collect more coins.

> [!TIP]  
> This tutorial will work best if you follow each step and write the code out for yourself. Where you see a tip like this one, try to solve the problem before moving ahead! You can easily copy and paste the final code, but doing so will miss out on the point of this tutorial, which is to learn. If you just want to look at some examples, then you can head over to the [examples folder](https://github.com/thebillington/tphysics/tree/master/examples).

## Learning outcomes

By the end of this tutorial, you will know how to:

1. Create a `tphysics` game window and add shapes.
2. Use a `game loop` to update our game state.
3. Detect key presses and respond to them.
4. Check for collisions and respond to them.
5. Generate random numbers and use them as positions.
5. Keep track of a score and output it in game.

## Creating a game window and player controller

We will start by creating our game window and game loop.

```python
from tphysics import Game, Rectangle

# Create a new game window
game = Game("Chase Game", "black")

# Game loop which will contain all of our logic
while True:

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

A game loop is an infinite loop which runs forever. This means that the code inside of the loop will continue until we press the *x* button to close the game.

Currently we haven't written any logic to go inside the game loop, so the only thing we need to do is render a new frame each time the game loop runs. If you run your code, you should see that we have an empty game window.

Now let's create a rectangle for the player and add it to the game.

```python
from tphysics import Game, Rectangle

# Create a new game window
game = Game("Chase Game", "black")

# Create the player game object in the middle of the screen
player = Rectangle(0, 0, 20, 20, "light blue")
game.add_shape(player)

# Game loop which will contain all of our logic
while True:

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

If you run the code again, you should see that we have a red square in the middle of the game window.

> [!TIP]  
> Can you change the colour of the player?

To get it to move, every frame (each time the loop runs) we need to change the position of the player.

We can do this using the `player.x` and `player.y` properties.

```python
from tphysics import Game, Rectangle

# Create a new game window
game = Game("Chase Game", "black")

# Create the player game object in the middle of the screen
player = Rectangle(0, 0, 20, 20, "light blue")
game.add_shape(player)

# Game loop which will contain all of our logic
while True:

    # Move the player by adding 1 to the x and y positions
    player.x = player.x + 1
    player.y += 1

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

We can now get our player to move, but in order to move based on key presses, we have to check if a key is pressed.

We can do this using the `game.ispressed()` function. This function will return `True` if a key is pressed, or `False` if it isn't.

Let's check if the right key is pressed and if it is, increase the `x` position of the player.

```python
from tphysics import Game, Rectangle

# Create a new game window
game = Game("Chase Game", "black")

# Create the player game object in the middle of the screen
player = Rectangle(0, 0, 20, 20, "light blue")
game.add_shape(player)

# Game loop which will contain all of our logic
while True:

    # Check if the right key is pressed
    if game.ispressed("Right"):

        # Move the player x position
        player.x += 1

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

> [!TIP]  
> You will now need to add in checks for the other direction keys and move the player. If you get stuck, then you can look ahead, however it is important to try and solve the problem by yourself first!

## Creating a coin to collect

Now that we have a character with a movement controller, we need to add a coin for the player to collect.

This will increase the score and the player will get a higher score by collecting more coins.

In order to stop the coin from generating in the same position each time, we will have to generate a random number.

Let's start by importing the `randint` function from the `random` library. We will also need to import `Circle` from tphysics.

```python
from tphysics import Game, Rectangle, Circle
from random import randint

# Create a new game window
game = Game("Chase Game", "black")

# Create the player game object in the middle of the screen
player = Rectangle(0, 0, 20, 20, "light blue")
game.add_shape(player)

# Game loop which will contain all of our logic
while True:

    # Check if the right key is pressed
    if game.ispressed("Right"):

        # Move the player x position
        player.x += 1

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

Now we need to create a new Circle with a random position.

```python
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

# Game loop which will contain all of our logic
while True:

    # Check key presses
    if game.ispressed("Right"):
        player.x += 1
    if game.ispressed("Left"):
        player.x -= 1
    if game.ispressed("Up"):
        player.y += 1
    if game.ispressed("Down"):
        player.y -= 1

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

Now that we have our coin spawning in a random position, we need to check if the player has collected the coin.

We do this by using the `player.collide()` function.

Every shape has access to its own `collide` function which allows it to check if it has collided with any other shape.

```python
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

# Game loop which will contain all of our logic
while True:

    # Check key presses
    if game.ispressed("Right"):
        player.x += 1
    if game.ispressed("Left"):
        player.x -= 1
    if game.ispressed("Up"):
        player.y += 1
    if game.ispressed("Down"):
        player.y -= 1

    # Check if the player has collected the coin
    if player.collide(coin):

        # Generate a new random position for the coin
        coin.x = randint(-250, 250)
        coin.y = randint(-250, 250)

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

Whenever the `player.collide(coin)` function returns as `True`, we generate a new random position for the coin.

# Tracking the score

Now that we have a coin to collect, we can keep track of a score.

To do this, we need to create a new variable in our setup code called `score` and give it a vlue of `1`.

Whenever we collect a coin, we will then add one to the score.

```python
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

# Set the initial score to zero
score = 0

# Game loop which will contain all of our logic
while True:

    # Check key presses
    if game.ispressed("Right"):
        player.x += 1
    if game.ispressed("Left"):
        player.x -= 1
    if game.ispressed("Up"):
        player.y += 1
    if game.ispressed("Down"):
        player.y -= 1

    # Check if the player has collected the coin
    if player.collide(coin):

        # If so, add to score and generate new coin position
        score += 1
        coin.x = randint(-250, 250)
        coin.y = randint(-250, 250)

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

Once we have a score to keep track of, we can use the `game.write()` function to show it to the player.

`game.write` needs to know the position (x,y), text, colour and size of the text to write.

```python
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

# Set the initial score to zero
score = 0

# Game loop which will contain all of our logic
while True:

    # Check key presses
    if game.ispressed("Right"):
        player.x += 1
    if game.ispressed("Left"):
        player.x -= 1
    if game.ispressed("Up"):
        player.y += 1
    if game.ispressed("Down"):
        player.y -= 1

    # Check if the player has collected the coin
    if player.collide(coin):

        # If so, add to score and generate new coin position
        score += 1
        coin.x = randint(-250, 250)
        coin.y = randint(-250, 250)

    # Show the score
    game.write(-300, 300, f"Score: {score}", "white", 20)

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

Notice that we have used a formatted string in order to show the score.

`f"Score: {score}"`

By using a formatted string, we can replace `{score}` with the actual value held in the score variable.

# Creating the enemy

Now that we have a way to collect coins and track the score, it is time to add difficulty.

We can do this by adding an enemy that chases the player.

We want our enemy to generate at a random position to prevent predictability.

```python
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

# Game loop which will contain all of our logic
while True:

    # Check key presses
    if game.ispressed("Right"):
        player.x += 1
    if game.ispressed("Left"):
        player.x -= 1
    if game.ispressed("Up"):
        player.y += 1
    if game.ispressed("Down"):
        player.y -= 1

    # Check if the player has collected the coin
    if player.collide(coin):

        # If so, add to score and generate new coin position
        score += 1
        coin.x = randint(-250, 250)
        coin.y = randint(-250, 250)

    # Show the score
    game.write(-300, 300, f"Score: {score}", "white", 20)

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

In order to get the enemy to chase the player, we will need it to keep track of the player x position.

We can do this using inequality operators, also known as the `less than` and `greater than` operators.

```python
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

# Game loop which will contain all of our logic
while True:

    # Check key presses
    if game.ispressed("Right"):
        player.x += 1
    if game.ispressed("Left"):
        player.x -= 1
    if game.ispressed("Up"):
        player.y += 1
    if game.ispressed("Down"):
        player.y -= 1

    # Check if the enemy is to the left of the player
    if enemy.x < player.x:

        # Move the enemy to the right
        enemy.x += 1

    # Check if the player has collected the coin
    if player.collide(coin):

        # If so, add to score and generate new coin position
        score += 1
        coin.x = randint(-250, 250)
        coin.y = randint(-250, 250)

    # Show the score
    game.write(-300, 300, f"Score: {score}", "white", 20)

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

> [!TIP]  
> You will now need to add in checks for the enemy being to the right, above and below the player. If you get stuck, then you can look ahead, however it is important to try and solve the problem by yourself first!

# Checking for enemy collision

Once we have the enemy movement controller working, we need to check for player and enemy collisions.

We do this in the same way we checked for player and coin collisions.

When the enemy hits the player, we will want to generate a new position for the enemy and coin.

We will also set the player position back to the centre and the score to zero.

```python
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

# Game loop which will contain all of our logic
while True:

    # Check key presses
    if game.ispressed("Right"):
        player.x += 1
    if game.ispressed("Left"):
        player.x -= 1
    if game.ispressed("Up"):
        player.y += 1
    if game.ispressed("Down"):
        player.y -= 1

    # Enemy movement checks
    if enemy.x < player.x:
        enemy.x += 1
    if enemy.x > player.x:
        enemy.x -= 1
    if enemy.y < player.y:
        enemy.y += 1
    if enemy.y > player.y:
        enemy.y -= 1

    # Check if the player has collected the coin
    if player.collide(coin):

        # If so, add to score and generate new coin position
        score += 1
        coin.x = randint(-250, 250)
        coin.y = randint(-250, 250)

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

    # Show the score
    game.write(-300, 300, f"Score: {score}", "white", 20)

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

# Increasing difficulty over time

Currently the player and enemy move with the same speed.

This isn't very fun as once the enemy has caught up, it is impossible to get away.

In order to make the game more interesting, we will add `player_speed` and `enemy_speed` variables with different values.

```python
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

    # Show the score
    game.write(-300, 300, f"Score: {score}", "white", 20)

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

Now that we have variables to track the player and enemy speed, we can increase it over time.

To do so, we will use the modulus operator to check if the score is divisible by 5.

`score % 5 == 0` - this code returns `True` if the score is divisible by 5, as the modulus operator finds the remaineder of a division.

The remainder of 24 divided by 5 is 4, so we know that it isn't divisible.

The remainder of 25 divided by 5 is 0, so we know that it is divisible, as it has a remainder of zero.

If the score is divisible by 5 after the player has collected a coin, then we will increase the player and enemy speed.

```python
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

    # Show the score
    game.write(-300, 300, f"Score: {score}", "white", 20)

    # Each time the game loop runs, at the end, render a new frame
    game.update()
```

This has now increased difficulty over time, but when we lose, the speeds don't reset back down.

To do this, when the enemy hits the player, we will need to reset the player and enemy speed.

```python
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
```

I hope you have enjoyed this tutorial. If so, you can find more tutorials on YouTube in the [tphysics playlist](https://www.youtube.com/watch?v=QQJT1oDcXUQ&list=PLMr7li1270gySPa4xz8PVVug1z0bCTil_).