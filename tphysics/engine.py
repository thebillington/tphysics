import shapes
import turtle

#Create a game object to hold all of our physics
class Game(object):

    #Initialize
    def __init__(self, name, width, height, colour):

        #Create a screen and set the name
        self.window = turtle.Screen()
        self.window.title(name)
        self.window.screensize(width, height, colour)

        #Create a turtle to do our drawing
        self.t = turtle.Turtle()
        
        #Hide the turtle
        self.t.hideturtle()
        
        #Disable the tracer
        self.t.tracer(0, 0)

        #Create a dictionary of shapes
        self.shapes = {}
    
    #Define a function to add a shape
    def add_shape(self, key, shape):

        #Check if the shape already exists
        if key in self.shapes.keys():
            raise KeyError("A shape with that key already exists.")

        #Add the shape
        self.shapes[key] = shape
    
    #Create a function to iterate over each of the shapes and draw them on screen
    def update(self):

        #Clear the canvas
        self.t.clear()
        
        #For each of the shapes in the dictionary, draw them
        for s in self.shapes.items():
            self.rectangle(s[1])
        
        #Update the screen
        self.window.update()
    
    #Create a function to allow us to draw a rectangle
    def rectangle(self, s):
		
		#Set the colour of the line
		self.t.color('black')
		
		#Move the pen to the correct position
		self.t.penup()
		self.t.goto(s.x - (s.width/2), s.y + (s.height/2))
		self.t.pendown()
		
		#Start the fill
		self.t.begin_fill()
		
		#Draw the rectangle
		for i in range(2):
			self.t.forward(s.width)
			self.t.right(90)
			self.t.forward(s.height)
			self.t.right(90)
			
		#Set the colour and end the fill
		self.t.color('red')
		self.t.end_fill()
