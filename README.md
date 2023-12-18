# tphysics 

tphysics is a cross platform physics engine built for educational purposes.

The entire engine is contained in a single file and uses Turtle graphics for rendering, making it an excellent candidate for use in the classroom.

The code is thoroughly commented with aims to providing a suitable library for people interested in learning the basics of Game Engineering.

### Resources

Teacher's introduction to tphysics in the classroom: https://www.youtube.com/watch?v=6z4ZEE0VqHU

How tphysics renders using Turtle graphics: https://youtu.be/QQJT1oDcXUQ

tphysics tutorials: [Watch the Playlist on YouTube](https://www.youtube.com/watch?v=QQJT1oDcXUQ&list=PLMr7li1270gySPa4xz8PVVug1z0bCTil_)

### Why tphysics

Over time I have found that students had a hard time learning games programming. They are able to be creative in blocky environments such as Scratch, which are designed specifically for learning the fundamentals of games programming, but when moving into textual languages and engines such as Unity, they find it much more difficult.

Learners aren't able to be creative as they are having to learn the complexities of an engine at the same time as a textual language. I found that they were often copying verbatim from a video tutorial and their ability to make maningful changes and improvements to final code was limited.

tphysics is designed to bridge the gap from a blocky style environment and more feature complete engines. All of the code is contained in a single file which means learners can take a look under the hood and since tphysics only uses simple rectangles and circles, learners develop an intuitive sense of abstraction, as well as a very pure understanding of collision detection.

### Supported versions:
* Python 3+

## Contents

### [Installation](#install)

### [Examples](#tphysics-examples)

### [Learn to use tphysics](#using-tphysics)

* [Creating a game object](#create-a-new-game-object)
* [Rendering the game window](#updating-the-game-window)
* [Creating shapes](#drawing-shapes)
* [Colour](#colour-and-fill)
* [Key presses](#detecting-key-presses)
* [Checking for collisions](#collision-detection)
* [Writing text](#writing-text)
* [Mouse clicks](#detecting-mouse-clicks)

## Install

### Using as a script

Using as a python script is extremely simple and can be done on almost any computer, provided the Python installation includes TKinter. This makes `tphysics` ideal for use in schools as you can just copy the code from this repository and import it directly into your code.

1. Open [tphysics.py](https://github.com/thebillington/tphysics/blob/master/tphysics.py) and `copy` the file contents.
2. Create a new python file in your IDE (likely `IDLE` if you are on school computers) and paste the contents
3. Save the file as `tphysics.py` - if you save it as anything else, it won't work!
4. Create a new file in *the same directory/folder* as your `tphysics.py` file and test with `from tphysics import *`

### Installing with PIP

> [!WARNING]  
> The following section was no longer relevant as I have updated tphysics to a single file library, to make it simple to download and use on school computers. There are plans to release tphysics officially via `PyPi` but currently, tphysics CANNOT be installed to your python installation with `pip`.

## tphysics Examples

This section is currently being fleshed out. Remember that if you want to run any examples, you must make sure you execute the script from the *same directory* as your `tphysics.py` script.

You can check out the `examples` folder for a full list of up to date examples.

## Using tphysics

Getting started with tphysics is easy. First, select which **classes** you are going to need and import them.
The following example will make use of the circle, square and game classes.

#### Create a new game object

First, create a new game object with the desired title, width, height and colour:

```python
#Imports
from tphysics import Game

#Create a new game object and store it in a variable
game = Game("Basic Game", "light blue")
```

You can make the game window full screen by using `fullscreen=True`:

```python
#Imports
from tphysics import Game

#Create a new game object and store it in a variable
game = Game("Basic Game", "light blue", fullscreen=True)
```

#### Updating the game window

In order to update any changes you make between frames, you must create a game loop that calls the **update** function. When the update function is called, it renders all of the changes that have happened since the last time you called it and creates a new *frame*:

```python
from tphysics import Game

#Create a new game object and store it in a variable
game = Game("Basic Game", "light blue")

#Game loop
while True:

	#Update the game
	game.update()
```

#### Drawing shapes

Once you have created a game it is extremely simple to draw shapes. Simply create a new shape, store it in a variable and add it to the game:

```python
from tphysics import Game, Rectangle, Circle

#Create a new game object and store it in a variable
game = Game("Basic Game", "light blue")

#Create a player Rectangle(x, y, width, height, colour)
player = Rectangle(-100, 100, 20, 50, "orange")
game.add_shape(player)

#Create an obstacle Circle(x, y, radius, colour)
obstacle = Circle(100, 100, 50, "green")
game.add_shape(obstacle)

# Game loop
while True:

	# Render the next frame
	game.update()
```

Shapes will be drawn in the order they are added.

It is easy to move shapes by accessing the `x` and `y` properties:

```python
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
		direction = direction * -1

	# Render the next frame
	game.update()
```

#### Colour and fill

Changing the colour of objects is easy and can be done by directly accessing the **fill_colour** and **line_colour** variables in your shape.
Any pre-defined colour accepted by [TKinter](https://www.tcl.tk/man/tcl8.4/TkCmd/colors.htm) is allowed. RGB values are also accepted:

```python
player.fill_colour = "blue"
obstacle.line_colour = "#00FFF7"
```

It is also easy to enable/disable the line being drawn or the shape being filled:

```python
player.fill = False
obstacle.line = False
```

Please note: With the current implementation disabling both of these will draw a shape with an outline the same colour as the fill colour.

#### Detecting key presses

Detecting key presses in tphysics is extremely simple.

The best way to check whether a specific key is pressed is by using the **ispressed** function on your game object. Currently only the alphanumeric, space and arrow keys are supported:

```python
from tphysics import Game, Rectangle

# Create game object
game = Game("Key Press Game", "light blue")

# Create player object
player = Rectangle(0, 0, 20, 20, "green")
game.add_shape(player)

# Game loop
while True:

	#Check whether a specific key is being pressed
	if game.ispressed("Right"):
		#Change the x speed
		player.x += 1

	# Update the game
	game.update()
```

You can also create a function that you want to handle the key press and pass this to your game object along with the name of the key you want to detect. This is a more advanced way of handling key presses as it requires the passing of `higher order functions`:

```python
from tphysics import Game, Circle

# Create a game object
game = Game("Higher Order Keys Example", "light blue")

# Create a player
player = Circle(0, 0, 10, "orange")
game.add_shape(player)

#Create a function to handle the up key press
def up():
	#Move the player up
	player.y += 1
	
#Pass the function to the game object
game.addkeypress(up, "Up")

# Game loop
while True:

	# Update the game
	game.update()
```

For a full list of available key names, check out the [TK documentation](https://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm).

#### Collision detection

There is currently thorough collision detection support for circles and rectangles. Shape rotation as of the current time is unsupported.

In order to check collision between two shapes you must use the collide function:

```python
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
```

The collide function will return **False** for no collision, and **True** for any collision of two same type shapes (circle-circle and rectangle-rectangle).

There is also support for circle-rectangle collision detection, which will return 0 for no collision and a non-zero value for a collision.
The non-zero values can be used to identify where on the square the centre of the circle collided as per the below chart (1 = center, 2 = alongside, 3 = above/below, 4 = corner, 0 = no collision):

```
      |       |
  4       3      4
      |       |
 _  _  _______  _  _
      |       |
  2   |   1   |  2
 _  _ |_______| _  _
 
      |       |
  4       3      4
      |       |
```

In future iterations this will be improved to identify which individual corner or side the circle collided with.

#### Writing Text

You can write text by passing your desired text into the `write` function:

```python
from tphysics import Game

# Create a game object
game = Game("Score Game", "red")

# Create a score variable
score = 0

# Game Loop
while True:

	# Write the score using write(x, y, text, colour, size)
	game.write(-100, 100, f"Score: {score}", "black", 20)

	# Add 1 to the score
	score += 1

	# Update the game
	game.update()

```

#### Detecting mouse clicks

Mouse click detection is handled in a very similar way to key presses.
Simply create a function that you want to handle your click and pass it in to the click listener:

```python
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
```

By default the addclick function sets clicks to the left mouse button. You can specify a left or right click using 1 or 2 respectively:

```python
#Left click listener
g.addclick(click, 1)

#Right click listener
g.addclick(click, 2)
```
