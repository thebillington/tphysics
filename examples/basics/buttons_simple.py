from tphysics import Game, Button, Rectangle

# Instantiate a game object
game = Game("test", "blue")

# Create a player rectangle and add to the game
player = Rectangle(0, 100, 20, 20, "orange")
game.add_shape(player)

# Create 2 buttons with different labels, positions and colours
button_a = Button(-100, 0, 150, 20, "A Button", button_colour="green", text_colour="white", padding=12)
button_b = Button(100, 0, 150, 20, "B Button", button_colour="red", text_colour="black", padding=12)

# Add buttons to the game∂
game.add_button(button_a)
game.add_button(button_b)

# Define a click handler function
def click(x,y):

    # Check for A Button press and if so, move player left
    if button_a.check_click(x,y):
        player.x -= 10
    
    # Check for B Button press and if so, move player left
    if button_b.check_click(x,y):
        player.x += 10

# Add click handler to the game as a higher order function
game.addclick(click)

# Game loop
while True:

    # Render the next frame of the game (no logic as all logic is in click handler)
    game.update()