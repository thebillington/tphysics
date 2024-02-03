from random import randint
from tphysics import *

# Create the game
game = Game("Scene Demo")

# Create scenes and add to the game
menu_scene = Scene("menu", "indigo")
game_scene = Scene("game", "light blue")
game.add_scene(menu_scene)
game.add_scene(game_scene)

# Switch to the menu scene
game.load_scene(menu_scene)

# Create the menu items and add them to the scene
play_button = Button(0, 50, 100, 50, "Play", button_colour="green")
menu_scene.add_button(play_button)

quit_button = Button(0, -50, 100, 50, "Quit", button_colour="red")
menu_scene.add_button(quit_button)

# Create the game scene
player = Rectangle(0, 0, 20, 20, "yellow")
game_scene.add_shape(player)
player_speed = 3

enemy = Rectangle(randint(-300, 300), randint(-300, 300), 10, 10, "red")
game_scene.add_shape(enemy)
enemy_speed = 2

pickup = Circle(randint(-300, 300), randint(-300, 300), 5, "purple")
game_scene.add_shape(pickup)

score = 0
high_score = 0

# Click handler
def click(x,y):

    # Check if the menu scene is currently active
    if game.current_scene == menu_scene:

        # Check if play button clicked
        if play_button.check_click(x,y):

            # Load the game scene
            game.load_scene(game_scene)

        # Check if quit button clicked
        if quit_button.check_click(x,y):

            # Quit
            game.quit()

# Add click handler
game.addclick(click)

# Game loop
while True:

    # Check if the game scene is loaded
    if game.current_scene == game_scene:

        if game.ispressed("Left"):
            player.x -= player_speed
        if game.ispressed("Right"):
            player.x += player_speed
        if game.ispressed("Down"):
            player.y -= player_speed
        if game.ispressed("Up"):
            player.y += player_speed

        if enemy.x < player.x:
            enemy.x += enemy_speed
        elif enemy.x > player.x:
            enemy.x -= enemy_speed
        if enemy.y < player.y:
            enemy.y += enemy_speed
        elif enemy.y > player.y:
            enemy.y -= enemy_speed

        if player.collide(enemy):
            game.load_scene(menu_scene)
            score = 0
            player.x = 0
            player.y = 0
            enemy.x = randint(-300, 300)
            enemy.y = randint(-300, 300)

        if player.collide(pickup):
            score += 1
            pickup.x = randint(-300, 300)
            pickup.y = randint(-300, 300)

        if score > high_score:
            high_score = score

        game.write(-300, 300, f"Score: {score}", "black", 20)
        game.write(-300, 270, f"High Score: {high_score}", "black", 20)

    # Game render
    game.update()
