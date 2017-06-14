# tphysics 

tphysics is a cross platform physics engine with Turtle integration built for educational purposes.
It has been written as a pet project as I wanted to create a game engine for personal use that did not require use of any external libraries.

If you are wanting a fully fledged game engine with sprite integration then I suggest checking out other engines that may be more fit for purpose.
If you are looking for a simple library that implements basic physics collision detection with an Object Oriented approach then tphysics is the one for you.

Please feel free to read through the code as it is thoroughly commented with aims to providing a suitable library for people interested in learning the basics of Game Engineering.

### Supported versions:
* Python 2.7.13

## Contents

### [Installation](#install)

### [Getting Started](#getting-started)

* [Creating a game object](#create-a-new-game-object)
* [Creating shapes](#drawing-shapes)
* [Drawing the game window](#updating-the-game-window)
* [Checking for collisions](#collision-detection)
* [Colour](#colour-and-fill)

## Installation

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

Depending on your permission, you may need to run this as root:

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
g.add_shape("player", player)
g.add_shape("obstacle", obstacle)
```

Please note: When adding shapes each needs a unique key identifier. Although this doesn't currently do anything functionally, it helps ensure that shapes are not duplicated.
In future iterations this will allow for shapes to be deleted without requiring clean up.

#### Updating the game window

In order to draw your shapes at their correct location, create a game loop that calls the **update** function:

```python
#Game loop
while True:
	#Update the game
	g.update()
```

#### Collision detection

There is currently thorought collision detection support for circles and rectangles. Shape rotation as of the current time is unsupported.

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
