from tphysics import Game, Rectangle, Button

# Create a game object
game = Game("test", "blue")

# Create a player and add to the game
player = Rectangle(0, 0, 20, 20, "yellow")
game.add_shape(player)

# Create a pause button
pause_button = Button(300, 300, 50, 20, "Pause", button_colour="green")
game.add_button(pause_button)

# Set global variable playing to true
global playing
playing = True

def click(x,y):
    
    # Get the global variable playing and flip it
    global playing
    playing = not playing

    # Switch the colour of the button
    if playing:
        pause_button.rect.fill_colour = "green"
    else:
        pause_button.rect.fill_colour = "red"

# Add the click handler to the game
game.addclick(click)

# Game loop
while True:

    # Check if we are playing
    if playing:

        # Check key presses
        if game.ispressed("Up"):
            player.y += 1
        if game.ispressed("Down"):
            player.y -= 1
        if game.ispressed("Right"):
            player.x += 1
        if game.ispressed("Left"):
            player.x -= 1

    # If not playing
    else:

        # Show pause message
        game.write(-50, 0, "Game is Paused", "white", 20)

    # Render the next frame
    game.update()