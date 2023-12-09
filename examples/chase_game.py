# This is an example game built to show a simple use of tphysics
# This example makes use of some advanced concepts in terms of using
# Screen Width and Screen Height as markers, to stop the player, enemy
# or pickup from going off of the screen.
# For a simpler example, see chase_game_simple.py

from tphysics import *
from random import randint

game = Game("Chase Game")
window_width, window_height = game.get_window_size()

player = Rectangle(0, 0, 30, 30, "yellow")
game.add_shape(player)
player_speed = 5

enemy = Rectangle(
    randint(int(-window_width/2) + 30, int(window_width/2) - 30),
    randint(int(-window_height/2) + 30, int(window_height/2) - 30),
    20,
    20,
    "red"
)
game.add_shape(enemy)
enemy_speed = 4

pickup = Circle(
    randint(int(-window_width/2) + 30, int(window_width/2) - 30),
    randint(int(-window_height/2) + 30, int(window_height/2) - 30),
    5,
    "purple"
)
game.add_shape(pickup)

score = 0
high_score = 0

while True:

    if game.ispressed("Left"):
        player.x -= player_speed
    if game.ispressed("Right"):
        player.x += player_speed
    if game.ispressed("Down"):
        player.y -= player_speed
    if game.ispressed("Up"):
        player.y += player_speed

    if player.x > int(window_width/2) - player.width:
        player.x = int(window_width/2) - player.width
    if player.x < -int(window_width/2) + player.width:
        player.x = -int(window_width/2) + player.width
    if player.y > int(window_height/2) - player.height:
        player.y = int(window_height/2) - player.height
    if player.y < -int(window_height/2) + player.height:
        player.y = -int(window_height/2) + player.height

    if enemy.x < player.x:
        enemy.x += enemy_speed
    elif enemy.x > player.x:
        enemy.x -= enemy_speed
    if enemy.y < player.y:
        enemy.y += enemy_speed
    elif enemy.y > player.y:
        enemy.y -= enemy_speed

    if player.collide(enemy):
        score = 0
        player.x = 0
        player.y = 0
        enemy.x = randint(int(-window_width/2) + 30, int(window_width/2) - 30)
        enemy.y = randint(int(-window_height/2) + 30, int(window_height/2) - 30)
        pickup.x = randint(int(-window_width/2) + 30, int(window_width/2) - 30)
        pickup.y = randint(int(-window_height/2) + 30, int(window_height/2) - 30)

    if player.collide(pickup):
        score += 1
        pickup.x = randint(int(-window_width/2) + 30, int(window_width/2) - 30)
        pickup.y = randint(int(-window_height/2) + 30, int(window_height/2) - 30)

    if score > high_score:
        high_score = score

    game.write(-window_width/2 + 30, window_height/2 - 50, f"Score: {score}", "black", 28)
    game.write(-window_width/2 + 30, window_height/2 - 80, f"High Score: {high_score}", "black", 28)

    game.update()