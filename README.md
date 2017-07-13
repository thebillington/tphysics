# tphysics 

tphysics is a cross platform physics engine with Turtle integration built for educational purposes.
It has been written as a pet project as I wanted to create a game engine for personal use that did not require use of any external libraries.

If you are wanting a fully fledged game engine with sprite integration then I suggest checking out other engines that may be more fit for purpose.
If you are looking for a simple library that implements basic physics collision detection with an Object Oriented approach then tphysics is the one for you.

Please feel free to read through the code as it is thoroughly commented with aims to providing a suitable library for people interested in learning the basics of Game Engineering.

### Supported versions:
* Python 3+

## Contents

### [Installation](#install)

### [Examples](#tphysics-examples)

### [Getting Started](#getting-started)

* [Creating a game object](#create-a-new-game-object)
* [Creating shapes](#drawing-shapes)
* [Drawing the game window](#updating-the-game-window)
* [Checking for collisions](#collision-detection)
* [Colour](#colour-and-fill)
* [Key presses](#detecting-key-presses)
* [Mouse clicks](#detecting-mouse-clicks)

### [Verlet](#verlet-physics)

* [Verlet objects](#verlet-objects)
* [Verlet with mouse clicks](#verlet-with-mouse-clicks)

## Install

tphysics is not currently registered as a package with the PyPi Package Manager, therefore install requires cloning of this repository onto your computer and install with **pip**.

To get started using pip read the documentation [here](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip).

#### Step One

Clone this repository onto your local file system, either using a Git manager or through terminal with the following command:

```
git clone https://github.com/thebillington/tphysics
```

#### Step Two

Once you have the repository downloaded locally, navigate to the root folder of the project in your terminal window or command prompt. The root folder is the one that holds **setup.py**.

#### Step Three

Now you are ready to run the pip install command install tphysics as a python package:
```
pip install .
```

Depending on your permissions, you may need to run this as root:

```
sudo pip install .
```

And if you already have an earlier version of tphysics installed you may have to use the **upgrade** flag:


```
sudo pip install . --upgrade
```

#### Step Four

The last step is to check that the package has installed correctly. Create a new python file and **import tphysics**:

```python
import tphysics
```

If you get an **ImportError** then you have not installed the package correctly. Go back and ensure you have successfully installed using pip.

## tphysics Examples

To see what you can do with tphysics, check out the following examples:

* [Bouncy Ball](https://github.com/thebillington/tphysics/tree/master/Examples/BouncyBall) - An example that implements verlet integration to create a real physics simulator for a bouncing ball.

* [Pong](https://github.com/thebillington/tphysics/tree/master/Examples/Pong) - A super simple pong game that implements basic collision detection and physics.

* [Platformer](https://github.com/thebillington/tphysics/tree/master/Examples/Pong) - A very simple platforming game with basic gravity implemented and platform collision detection.

## Getting started

Getting started with tphysics is easy. First, select which **classes** you are going to need and import them.
The following example will make use of the circle, square and game classes.

#### Create a new game object

First, create a new game object with the desired title, width, height and colour:

```python
#Imports
from tphysics import Game, Rectangle, Circle

#Create a new game object and store it in a variable
g = Game("Basic Game", 600, 600, "grey")
```

#### Drawing shapes

Once you have created a game it is extremely simple to draw shapes. Simply create a new shape, store it in a variable and add it to the game:

```python
#Create a player Rectangle(x, y, width, height)
player = Rectangle(-100, 100, 20, 50)

#Create an obstacle Circle(x, y, radius)
obstacle = Circle(100, 100, 50)

#Add the shapes to the game
g.add_shape(player)
g.add_shape(obstacle)
```

Shapes will be drawn in the order they are added.

#### Updating the game window

In order to draw your shapes at their correct location, create a game loop that calls the **update** function:

```python
#Game loop
while True:
	#Update the game
	g.update()
```

#### Collision detection

There is currently thorough collision detection support for circles and rectangles. Shape rotation as of the current time is unsupported.

In order to check collision between two shapes you must use the collide function:

```python
player.collide(obstacle)
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
Simply create a function that you want to handle the key press and pass this to your game object along with the name of the key you want to detect:

```python
#Create a function to handle the up key press
def up():
	#Move the player up
	player.y += 1
	
#Pass the function to the game object
g.addkeypress(up, "Up")
```

You can also check whether a specific key is pressed using the **ispressed** function on your game object. Currently only the alphanumeric, space and arrow keys are currently supported:

```python
#Check whether a specific key is being pressed
if g.ispressed("Left"):
	#Change the x speed
	xspeed = -5
```

For a full list of available key names, check out the [TK documentation](https://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm).

#### Detecting mouse clicks

Mouse click detection is handled in a very similar way to key presses.
Simply create a function that you want to handle your click and pass it in to the click listener:

```python
#Create a function to handle the click
def click(x, y):
	print("Mouse clicked at location ({},{})".format(x, y))

#Add the click listener
g.addclick(click)
```

By default the addclick function sets clicks to the left mouse button. You can specify a left or right click using 1 or 2 respectively:

```python
#Left click listener
g.addclick(click, 1)

#Right click listener
g.addclick(click, 2)
```

## Verlet Physics

#### Verlet Objects

So far there is one Verlet Object implemented which is a version of the Circle object called **VerletCircle**.
This object has a very (and I mean very) simple implementation of verlet integration to allow for physics updates.

To use the VerletCircle, import it and create an object:

```python
from tphysics import VerletCircle

#Create a VerletCircle(x, y, radius, xspeed, yspeed) with an initial x speed of 2
vc = VerletCircle(0, 0, 10, 2, 0)
```

To update the position of the circle, call the update function within your game loop:

```python
#Game loop
while True:

	#Update the position of the verlet circle
	vc.update()
```

If the speed of the circle falls below 0.01 on the x or y axis it will come to a stop. This will be implemented as a threshold in future updates.

To set the speed of the circle use the **setspeed** function. This can be done on both axes separately:

```python
vc.setspeed(5, 5)
vc.setxspeed(5)
vc.setyspeed(5)
```

You can also get the speed on either axis:

```python
vc.getxspeed()
vc.getyspeed()
```

And you can get the object to bounce on the x or y axis. When you get the ball to bounce, you need to also provide:

* Elasticity (for both the x and y axis bounce)
* Friction (for just the y axis bounce)

To have no loss of energy in your physics system, simply set your elasticity to **1** and your friction to **0**:

```python
#Set physics constants
e = 1
f = 0

#Bounce on the x axis
vc.bouncex(e)
vc.bouncey(e, f)
```

I am currently deciding on the best way to integrate verlet integration effectively so expect this API to change in future updates.

#### Verlet with mouse clicks

It is extremely easy to combine key clicks with verlet integration to set the speed of an object:

```python
#Create a boolean to store whether the ball was clicked
global clicked
clicked = False

#Functions to handle mouse clicks
def click(x, y):
	
	#Get the global
	global clicked
	
	#Check whether the click collides with the ball
	if ball.collide(Point(x,y)) and not clicked:
		#Set clicked to true
		clicked = True
	elif clicked:
		#Set the current position of the ball to the mouse x and y
		ball.x = x
		ball.y = y
		clicked = False
		
#Add click listeners to the game
g.addclick(click)
```

To see this method in action, check out the [BouncyBall](https://github.com/thebillington/tphysics/tree/master/Examples/BouncyBall) example.
