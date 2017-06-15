#Imports
from shapes import *

#Create a class to hold a verlet version of the circle
class VerletCircle(Circle):

    #Define init for the circle
    def __init__(self, x, y, radius, xspeed, yspeed):
		
        #Crete our derivative shape
		super(VerletCircle, self).__init__(x, y, radius)
		#Set the radious
		self.radius = radius
		
		#Store the previous position values
		self.prevx = self.x - xspeed
		self.prevy = self.y - yspeed
        
    #Create a function to set the speed
    def setspeed(self, xspeed, yspeed):
		
		#Update the previous position to match the speed
        self.prevx = self.x - xspeed
        self.prevy = self.y - yspeed
        
    #Create a function to set the speed
    def setxspeed(self, xspeed):
		
		#Update the previous position to match the speed
        self.prevx = self.x - xspeed
        
    #Create a function to set the speed
    def setyspeed(self, yspeed):
		
		#Update the previous position to match the speed
        self.prevy = self.y - yspeed
        
    #Create a function to get the x speed
    def getxspeed(self):
		
		#Return the x speed
        return self.x - self.prevx
        
    #Create a function to get the speed
    def getyspeed(self):
		
		#Return the y speed
        return self.y - self.prevy
    
    #Create a function to bounce on the x
    def bouncex(self, elasticity):
		
		#Bounce on the x axis
		tempx = self.prevx
		self.prevx = self.x
		self.x = self.x + ((tempx - self.prevx) * elasticity)
    
    #Create a function to bounce on the y
    def bouncey(self, elasticity, friction):
	
		#Bounce on the y axis
		tempy = self.prevy
		self.prevy = self.y
		self.y = self.y + ((tempy - self.y) / (1/ elasticity))
		self.x = self.x + ((self.prevx - self.x) * friction)
	
	#Create a function to update the position
    def update(self):
		
		#Store the current position
		tempx = self.x
		tempy = self.y
		
		#Update the position
		self.x = self.x + (self.x - self.prevx)
		self.y = self.y + (self.y - self.prevy)
		
		#Store the previous position
		self.prevx = tempx
		self.prevy = tempy
		
		#Check whether the ball has come to an effective stop
		if abs(self.x - self.prevx) < 0.01:
			self.prevx = self.x
		if abs(self.y - self.prevy) < 0.01:
			self.prevy = self.y
