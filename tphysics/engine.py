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

        #Create a dictionary of shapes
        self.shapes = {}
        
        self.window.exitonclick()

    #Define a function to add a shape
    def add_shape(key, shape):

        #Check if the shape already exists
        if key in shapes.keys():
            raise KeyError("Shape already exists.")

        #Add the shape
        shapes[key] = shape
    
    #Create a function to iterate over each of the shapes and draw them on screen
    def update(self):

        #For each of the shapes in the dictionary, draw them
        for s in shapes.items():
            print(s[1].type)
