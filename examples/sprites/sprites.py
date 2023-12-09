#Imports
from tphysics import Sprite, Game

#Create a new game
g = Game("Sprite Game", "light blue")

#Create two sprites for each of the characters
pOne = Sprite("player1.gif", g.window, -100, 0)
pTwo = Sprite("player2.gif", g.window, 100, 0)

#Add the sprites to the game
g.add_sprite(pOne)
g.add_sprite(pTwo)

#Game loop
while True:
    
    #Check for key presses
    if g.ispressed("w"):
        pOne.move(0, 1)
    if g.ispressed("s"):
        pOne.move(0, -1)
    if g.ispressed("a"):
        pOne.move(-1, 0)
    if g.ispressed("d"):
        pOne.move(1, 0)
    if g.ispressed("Up"):
        pTwo.move(0, 1)
    if g.ispressed("Down"):
        pTwo.move(0, -1)
    if g.ispressed("Left"):
        pTwo.move(-1, 0)
    if g.ispressed("Right"):
        pTwo.move(1, 0)
    
    # Render next frame
    g.update()