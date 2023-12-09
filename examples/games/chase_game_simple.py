# This is an example game built to show a simple use of tphysics
# For a more complex example, making use of screen width and height, see chase_game.py

from tphysics import *
from random import randint

game = Game("Chase Game")
window_width, window_height = game.get_window_size()

player = Rectangle(0, 0, 20, 20, "yellow")
game.add_shape(player)
player_speed = 3

enemy = Rectangle(randint(-300, 300), randint(-300, 300), 10, 10, "red")
game.add_shape(enemy)
enemy_speed = 2

pickup = Circle(randint(-300, 300), randint(-300, 300), 5, "purple")
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

    game.update()