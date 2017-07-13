#Imports
from functools import partial

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
