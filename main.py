import turtle
import json

# Create the window and game borders
# window = 600 / 480
winX = 600
winY = 480

window = turtle.Screen()
window.setworldcoordinates(0, 480, 600, 0)
window.setup(winX + 200, winY + 240)
window.bgcolor('black')
window.title('Puzzle Dungeon Py')
borders = turtle.Turtle()
borders.penup()
borders.color('white')
borders.hideturtle()
borders.speed(0)
borders.setpos(0, 0)
borders.pendown()

borders.forward(winX)
borders.left(90)
borders.forward(winY)
borders.left(90)
borders.forward(winX)
borders.left(90)
borders.forward(winY)

borders.penup()
borders.setpos(0, 0)
for cell in range(10):
    borders.setpos(borders.xcor() + 60, 0)
    borders.pendown()
    borders.sety(winY)
    borders.penup()

for cell in range(8):
    borders.setpos(0, borders.ycor() - 60)
    borders.pendown()
    borders.setx(winX)
    borders.penup()

# Local reference to turtles
items = []

# Create the player
player = turtle.Turtle()
player.penup()
player.speed(0)
player.hideturtle()
player.color('white')
player.shape('turtle')
player.turtlesize(1.5)
player.penup()
moving = False


def checkCollisions(item, dir, canPush):
    futurePos = getFuturePos(item, dir)
    print('future position' + str(futurePos))

    willCollide = False

    for i in range(len(items)):
        itemX = items[i]['item'].xcor()
        itemY = items[i]['item'].ycor()
        if itemX == futurePos['x'] and itemY == futurePos['y']:
            if items[i]['type'] == 'W':
                willCollide = True
            if items[i]['type'] == 'G' or items[i]['type'] == 'B' or items[i]['type'] == 'R':
                if not canPush:
                    willCollide = True
                if canPush and checkCollisions(items[i]['item'], dir, False):
                    willCollide = True

        # Detect crashing into bounding walls
        if futurePos['x'] < 30 or futurePos['x'] > winX:
            willCollide = True
        if futurePos['y'] < 30 or futurePos['y'] > winY:
            willCollide = True

    return willCollide


def checkMovables(item, dir):
    futurePos = getFuturePos(item, dir)
    print('future position' + str(futurePos))

    for i in range(len(items)):
        print('Returned was' + str(items[i]))
        itemX = items[i]['item'].xcor()
        itemY = items[i]['item'].ycor()
        if itemX == futurePos['x'] and itemY == futurePos['y']:
            print('GOING TO CRASH!!!!')

            if items[i]['type'] == 'W':
                global moving
                moving = True
            if items[i]['type'] == 'G':
                if not checkCollisions(items[i]['item'], dir, False):
                    lerpItem(items[i]['item'], dir)
            if items[i]['type'] == 'B':
                for j in range(len(items)):
                    if items[j]['type'] == 'B':
                        if not checkCollisions(items[j]['item'], dir, False):
                            lerpItem(items[j]['item'], dir)
            if items[i]['type'] == 'R':
                if not checkCollisions(items[i]['item'], dir, False):
                    lerpItem(items[i]['item'], dir)
                for j in range(len(items)):
                    if items[j]['type'] == 'R' and items[j]['item'] != items[i]['item']:
                        if not checkCollisions(items[j]['item'], getOppositeDirection(dir), False):
                            lerpItem(items[j]['item'], getOppositeDirection(dir))


def getOppositeDirection(dir):
    if dir == 'up':
        return 'down'
    if dir == 'down':
        return 'up'
    if dir == 'left':
        return 'right'
    if dir == 'right':
        return 'left'


def lerpItem(item, dir):
    if dir == 'up':
        for lerp in range(6):
            x = item.xcor()
            y = item.ycor() - 10
            item.setpos(x, y)

    if dir == 'down':
        for lerp in range(6):
            x = item.xcor()
            y = item.ycor() + 10
            item.setpos(x, y)

    if dir == 'left':
        for lerp in range(6):
            x = item.xcor() - 10
            y = item.ycor()
            item.setpos(x, y)

    if dir == 'right':
        for lerp in range(6):
            x = item.xcor() + 10
            y = item.ycor()
            item.setpos(x, y)


def getFuturePos(item, dir):
    x = item.xcor()
    y = item.ycor()
    if dir == 'up':
        x = item.xcor()
        y = item.ycor() - 60
    if dir == 'down':
        x = item.xcor()
        y = item.ycor() + 60
    if dir == 'left':
        x = item.xcor() - 60
        y = item.ycor()
    if dir == 'right':
        x = item.xcor() + 60
        y = item.ycor()
    return {'x': x, 'y': y}


def moveLeft():
    player.setheading(180)
    global moving
    if moving is False:
        moving = True
        if not checkCollisions(player, 'left', True):
            checkMovables(player, 'left')
            lerpItem(player, 'left')
    moving = False


def moveRight():
    player.setheading(0)
    global moving
    if moving is False:
        moving = True
        if not checkCollisions(player, 'right', True):
            checkMovables(player, 'right')
            lerpItem(player, 'right')
    moving = False


def moveUp():
    player.setheading(270)
    global moving
    if moving is False:
        moving = True
        if not checkCollisions(player, 'up', True):
            checkMovables(player, 'up')
            lerpItem(player, 'up')
    moving = False


def moveDown():
    player.setheading(90)
    global moving
    if moving is False:
        moving = True
        if not checkCollisions(player, 'down', True):
            checkMovables(player, 'down')
            lerpItem(player, 'down')
    moving = False


# Add keyboard listeners
window.listen()
window.onkeypress(moveLeft, "Left")
window.onkey(moveRight, "Right")
window.onkey(moveUp, "Up")
window.onkey(moveDown, "Down")

# Create the level
# P - Player
# W - Wall
# B - Blue Ball
# b - Blue Goal
# R - Red Ball
# r - Red Goal
with open('levels/1.json') as mapJson:
    mapData = json.load(mapJson)
    for i in range(len(mapData)):
        for j in range(len(mapData[0])):
            val = mapData[i][j]
            if val != ' ':
                xPos = (winX / 10) * (j + 1) - 30
                yPos = (winY / 8) * (i + 1) - 30
                if val != 'P':
                    item = turtle.Turtle()
                    item.speed(0)
                    item.penup()
                    item.setposition(xPos, yPos)
                if val == 'W':
                    item.color('grey')
                    item.turtlesize(3.2)
                    item.shape('square')
                    items.append({'type': val, 'item': item})
                if val == 'b':
                    item.color('lightblue')
                    item.turtlesize(2)
                    item.shape('square')
                    items.append({'type': val, 'item': item})
                if val == 'B':
                    item.color('blue')
                    item.turtlesize(1.5)
                    item.shape('circle')
                    items.append({'type': val, 'item': item})
                if val == 'R':
                    item.color('red')
                    item.turtlesize(1.5)
                    item.shape('circle')
                    items.append({'type': val, 'item': item})
                if val == 'r':
                    item.color('orange')
                    item.turtlesize(2)
                    item.shape('square')
                    items.append({'type': val, 'item': item})
                if val == 'P':
                    player.penup()
                    player.showturtle()
                    player.setposition(xPos, yPos)

input("Press Enter to continue...")
