#Imports
from turtle import Turtle

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
