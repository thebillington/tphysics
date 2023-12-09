# IMPORTS
import math
import turtle
from turtle import Turtle
from tkinter import TclError
from time import sleep
import sys
from functools import partial

# SHAPES

#Define a class to hold opur shape
class Shape(object):
    
    #Types
    POINT = "point"
    RECT = "rectangle"
    CIRCLE = "circle"

    #Implement our init function
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        
        self.line_colour = "black"
        self.fill_colour = "red"
        self.fill = True
        self.line = True

    #Define pythagoral function
    def pythagoras(self, s):

        #Return the distance between the shapes
        return math.sqrt(math.pow(abs(self.x - s.x) , 2) + math.pow(abs(self.y - s.y) , 2))

#Create our rectangle class
class Point(Shape):

    #Define our initialize function
    def __init__(self, x, y):

        #Create our derivative shape
        super(Point, self).__init__(x, y, Shape.POINT)

    #Define pythagoral function
    def collide(self, s):

        #Circle collision
        if s.type == Shape.CIRCLE:
            
            #Check whether the distance between the shapes is larger than the radius of the circle
            return self.pythagoras(s) < s.radius
        
        #Square collision
        if s.type == Shape.RECT:
            
            #Pass to rectangle collision
            return s.collide(self)

#Create our rectangle class
class Rectangle(Shape):

    #Define our initialize function
    def __init__(self, x, y, width, height, colour = "red"):

        #Create our derivative shape
        super(Rectangle, self).__init__(x, y, Shape.RECT)
        self.width = width
        self.height = height
        self.fill_colour = colour

    #Define a function to get the corners
    def update_corners(self):

        #Fetch the x, y, width and height
        x = self.x
        y = self.y
        width = self.width
        height = self.height

        #Create our corners
        self.corners = [Point(x - width / 2, y + height / 2), Point(x - width / 2, y - height / 2), Point(x + width / 2, y + height / 2), Point(x + width / 2, y - height / 2)]
        
    #define a collice function
    def collide(self, s):

        #If s is a rectangle
        if s.type == Shape.RECT:

            #Craete our collide x variable
            col_x = abs(self.x - s.x) < (self.width / 2) + (s.width / 2)
            #Create our collide y variables
            col_y = abs(self.y - s.y) < (self.height / 2) + (s.height / 2)
            #return col_x and col_y
            return (col_x and col_y)

        #Square Circle collision
        if s.type == Shape.CIRCLE:

            #Update the corners
            self.update_corners()

            #Check if there is an overlap on the x or y
            x_overlap = abs(self.x - s.x) < self.width / 2
            y_overlap = abs(self.y - s.y) < self.height / 2

            #If they have overlapped on x and y, return true
            if x_overlap and y_overlap:
                return 1

            #If it has overlapped on just the y
            if y_overlap:
                #If the x distance has overlapped return true
                if abs(self.x - s.x) < s.radius + self.width / 2:
                    return 2

            #If it has overlapped on just the x
            if x_overlap:
                #If the y distance has overlapped return true
                if abs(self.y - s.y) < s.radius + self.height / 2:
                    return 3

            #If we have overlapped on any corner, return true
            for c in self.corners:
                if c.pythagoras(s) < s.radius:
                    return 4

            #Not collided
            return 0
        
        #If the shape is a point
        if s.type == Shape.POINT:

            #Update the corners
            self.update_corners()
            
            #Check whether the point lies inside the rectangle
            return (s.x > self.corners[1].x and s.y > self.corners[1].y) and (s.x < self.corners[2].x and s.y < self.corners[2].y)
        
        return("Collision not implemented")

#Create my circle class
class Circle(Shape):

    #Define init for my circle
    def __init__(self, x, y, radius, colour = "yellow"):
        
        #Create our derivative shape
        super(Circle, self).__init__(x, y, Shape.CIRCLE)
        #Set the radious
        self.radius = radius
        
        #Set the default fill colour
        self.fill_colour = colour

    def collide(self, s):

        #If the s is a circle
        if s.type == Shape.CIRCLE:
            return self.pythagoras(s) < self.radius + s.radius
            
        #If it's a rectangle
        if s.type == Shape.RECT:
            return s.collide(self)
 
        #If the shape is a point
        if s.type == Shape.POINT:
            return s.collide(self)
        
        return("Collision not implemented")

# ENGINE

#Create a game object to hold all of our physics
class Game(object):

    #Initialize
    def __init__(self, name, colour = "grey", sleep_time = 0.01):

        #Create a screen and set the name
        self.window = turtle.Screen()
        self.window.title(name)
        self.window.bgcolor(colour)
        self.window.setup(1.0, 1.0)

        #Create a turtle to do our drawing
        self.t = turtle.Turtle()
        
        #Hide the turtle
        self.t.hideturtle()
        
        #Disable the tracer
        self.window.tracer(0, 0)

        #Create a list of shapes
        self.shapes = []

        # Create a list of text objects
        self.text = []
        
        #Create a key listener
        self.keylistener = KeyListener(self.window)
        
        #Create an empty list of sprites
        self.sprites = []

        # Set the sleep time
        self.sleep = sleep_time

    # Function to return the width and height of the window
    def get_window_size(self):
        return (self.window.window_width(), self.window.window_height())
    
    #Define a function to add a shape
    def add_shape(self, shape):

        #Add the shape
        self.shapes.append(shape)
        
    #Define a function to add a sprite
    def add_sprite(self, sprite):
        
        #Add the sprite
        self.sprites.append(sprite)
    
    #Create a function to iterate over each of the shapes and draw them on screen
    def update(self):

        # Check for game exit
        try:

            #Clear the canvas
            self.t.clear()
            
            #For each of the shapes in the dictionary, draw them
            for s in self.shapes:
                
                #Check the type of the shape
                if s.type == Shape.RECT:
                    self.rectangle(s)
                if s.type == Shape.CIRCLE:
                    self.circle(s)

            # For each of the shapes in the list, render
            for t in self.text:
                self.render_text(t)
            
            #Update the screen
            self.window.update()

            # Wipe the text list ready for the next frame
            self.text = []

            # Sleep
            sleep(self.sleep)
        
        except TclError as e:
            print("Program exited successfully.")
            sys.exit()
    
    #Create a function to allow us to draw a rectangle
    def rectangle(self, s):
        
        #Check whether the line should be drawn
        if s.line:
            #Set the colour of the line
            self.t.color(s.line_colour)
        else:
            #Set the colour of the line to the fill colour
            self.t.color(s.fill_colour)
        
        #Move the pen to the correct position
        self.t.penup()
        self.t.goto(s.x - (s.width/2), s.y + (s.height/2))
        self.t.pendown()
        
        #If the shape should be filled
        if s.fill:
            #Start the fill
            self.t.begin_fill()
        
        #Draw the rectangle
        for i in range(2):
            self.t.forward(s.width)
            self.t.right(90)
            self.t.forward(s.height)
            self.t.right(90)
        
        #If the shape should be filled
        if s.fill:
            #Set the colour and end the fill
            self.t.color(s.fill_colour)
            self.t.end_fill()
    
    #Create a function to allow us to draw a circle
    def circle(self, s):
        
        #Check whether the line should be drawn
        if s.line:
            #Set the colour of the line
            self.t.color(s.line_colour)
        else:
            #Set the colour of the line to the fill colour
            self.t.color(s.fill_colour)
        
        #Move the pen to the correct position
        self.t.penup()
        self.t.goto(s.x, s.y - s.radius)
        self.t.pendown()
        
        #If the shape should be filled
        if s.fill:
            #Start the fill
            self.t.begin_fill()
        
        #Draw the circle
        self.t.circle(s.radius)
        
        #If the shape should be filled
        if s.fill:
            #Set the colour and end the fill
            self.t.color(s.fill_colour)
            self.t.end_fill()

    # Create a function that lets us draw text to the screen
    def render_text(self, text_object):

                # Move to the correct location
                self.t.penup()
                self.t.goto(text_object.x, text_object.y)
                self.t.pendown()

                # Set the colour
                self.t.color(text_object.colour)
                
                # Write the text
                self.t.write(text_object.text, font=("Arial", text_object.size, "normal"))

    # Function to add text to be rendered on the next frame
    def write(self, x, y, text, colour, size):

        # Add a text object to the text list
        self.text.append(
            Text(x, y, text, colour, size)
        )
        
    #Create a function to add a mouse click
    def addclick(self, f, m=1):
        
        #Add the function to the click listener
        self.window.onclick(f, m)
    
    #Create a function to add a key listener
    def addkeypress(self, f, key):
        
        #Add the key and start listening
        self.window.onkey(f, key)
        self.window.listen()
        
    #Create a function to check whether a key is currently being pressed
    def ispressed(self, k):
        
        #Return the key listener check
        return self.keylistener.isPressed(k)
    
# TEXT

# Create a class to store information about text
class Text(object):

    # Constructor
    def __init__(self, x, y, text, colour, size):
        self.x = x
        self.y = y
        self.text = text
        self.colour = colour
        self.size = size

# KEYS

#Create a key listener class
class KeyListener(object):
    
    #List of keys
    keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "space", "Up", "Down", "Left", "Right"]
    
    #Constructor
    def __init__(self, window):
        
        #Store the window
        self.window = window
        
        #Run the setup function for the dictionary
        self.setup()
        
        #Setup the key listeners
        self.createListeners()
        
    #Function to initialize the key listener
    def setup(self):
        
        #Create a dictionary to store the keys that are currently being pressed
        self.pressed = {}
        
        #For each of the keys, set them to false in the dictionary
        for k in KeyListener.keys:
            self.pressed[k] = False
    
    #Function to handle key down events
    def keyDown(self, k):
        
        #Add this key to the list of pressed keys
        self.pressed[k] = True
    
    #Function to handle key up events
    def keyUp(self, k):
        
        #Add this key to the list of pressed keys
        self.pressed[k] = False
        
    #Function to add key listeners for each key
    def createListeners(self):
        
        #For each of the keys, add a listener
        for k in KeyListener.keys:
            
            #Set the current key
            fp = partial(self.keyDown, k)
            fr = partial(self.keyUp, k)
            
            #Add the on key listeners
            self.window.onkeypress(fp, k)
            self.window.onkeyrelease(fr, k)
        
        #Start the listener
        self.window.listen()
            
    #Function to check whether a key is pressed
    def isPressed(self, k):
        
        #Return whether the key is pressed or not
        return self.pressed[k]

# SPRITES

#Create an object to hold a sprite
class Sprite(object):
    
    #Constructor
    def __init__(self, img, window, x, y):
        
        #Store the image resource
        self.img = img
        
        #Store the window
        self.window = window
        
        #Add the image to the window
        window.addshape(self.img)
        
        #Create a turtle object
        self.turtle = Turtle()
        self.turtle.penup()
        
        #Set the image for the turtle
        self.turtle.shape(self.img)
        
        #Set the x and y position of the turtle
        self.x = x
        self.y = y
        
        #Set the turtle ot visible by default
        self.visible = True
        
        #Set the initial position
        self.move(0, 0)
        
    #Function to move the turtle
    def move(self, x, y):
        
        #Change the values of the position
        self.x += x
        self.y += y
        
        #Move the sprite
        self.turtle.goto(self.x, self.y)
        
    #Functions to set the sprite visible or invisible
    def setvisibile(self):
        self.visible = True
        self.turtle.showturtle()
    def setinvisible(self):
        self.visible = False
        self.turtle.hideturtle()
