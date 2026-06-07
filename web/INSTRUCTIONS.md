# How to Use tphysics

Welcome! This is a browser-based game playground where you can write Python code and see it run instantly.

## Getting Started

1. **Write code** in the editor on the left
2. Click **Run** (or press `Ctrl+Enter`) to start your game
3. Click **Stop** to end it
4. Use **Arrow keys** and **Space** to control your game while it's running

## Your First Game

Try this! Click **Load Example** and pick **Simple Chase** to see a working game.

Or start from scratch:

```python
from tphysics import *

game = Game("My Game", "light blue")
player = Rectangle(0, 0, 40, 40, "orange")
game.add_shape(player)

while True:
    if game.ispressed("Left"):
        player.x -= 5
    if game.ispressed("Right"):
        player.x += 5
    game.update()
```

## Shapes

You can draw different shapes on screen:

| Shape | How to create it |
|-------|-----------------|
| Rectangle | `Rectangle(x, y, width, height, "colour")` |
| Circle | `Circle(x, y, radius, "colour")` |
| Point | `Point(x, y)` |

Add any shape to your game with `game.add_shape(shape)`.

## Colours

Use any of these colour names: `red`, `blue`, `green`, `yellow`, `orange`, `purple`, `pink`, `white`, `black`, `grey`, `light blue`, `dark green`, and more.

Fill a shape with a different colour inside:
```python
player = Rectangle(0, 0, 40, 40, "red")
player.fill_colour = "yellow"
```

## Moving Things

### Keyboard Controls

Check if a key is being held down:

```python
if game.ispressed("Left"):
    player.x -= 5
```

Key names: `"Left"`, `"Right"`, `"Up"`, `"Down"`, `"space"`, `"a"` through `"z"`, `"0"` through `"9"`

### Mouse Clicks

Make something happen when the player clicks:

```python
def handle_click(x, y):
    print(f"Clicked at {x}, {y}")

game.addclick(handle_click)
```

## Collision Detection

Check if two shapes overlap:

```python
if player.collide(enemy):
    print("Hit!")
```

You can also check if a point is inside a shape:

```python
if Point(x, y).collide(target):
    print("Direct hit!")
```

## Writing Text

Display score or messages on screen:

```python
game.write(x, y, "Score: 10", "black", 20)
```

The numbers are: x position, y position, your text, colour, and font size.

## Buttons

Add clickable buttons:

```python
button = Button("Start", 0, -100, 80, 40, "green")
game.add_button(button)

# Check if the button was clicked
if button.check_click(x, y):
    print("Button pressed!")
```

## Saving Your Work

- **Save** — saves to your browser (Ctrl+S)
- **Load** — opens a saved file
- **Download** — downloads as a `.py` file
- **Copy** — copies your code to clipboard

> Files saved in your browser are only available on this device.

## Tips

- Every game needs `game.update()` at the bottom of your `while True` loop
- `x` goes right, `y` goes up — (0,0) is the centre of the screen
- The screen is 800 wide and 700 tall
- Colours with spaces like `"light blue"` work fine
- Use `game.ispressed("key")` for smooth movement, not `onkeypress`