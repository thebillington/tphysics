#Import math
import math

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

#Create our rectangle class
class Rectangle(Shape):

    #Define our initialize function
    def __init__(self, x, y, width, height):

        #Create our derivative shape
        super(Rectangle, self).__init__(x, y, Shape.RECT)
        self.width = width
        self.height = height

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
        
        return("Collision not implemented")

#Create my circle class
class Circle(Shape):

    #Define init for my circle
    def __init__(self, x, y, radius):
        
        #Create our derivative shape
        super(Circle, self).__init__(x, y, Shape.CIRCLE)
        #Set the radious
        self.radius = radius
        
        #Set the default fill colour
        self.fill_colour = "yellow"

    def collide(self, s):

        #If the s is a circle
        if s.type == Shape.CIRCLE:
            return self.pythagoras(s) < self.radius + s.radius
		#Otherwise
        if s.type == Shape.RECT:
            return s.collide(self) 
