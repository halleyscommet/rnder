import turtle
from typedefs import Camera, Polygon, MAX_POLYS, Vec2
from levelinit import Init
from math import sin, cos

cam = Camera()
polys = [Polygon() for _ in range(MAX_POLYS)]

# setup
screen = turtle.Screen()
screen.tracer(0)

widthS = screen.window_width()
heightS = screen.window_height()

# Set the origin to the top-left corner
screen.setworldcoordinates(0, heightS, widthS, 0)

print(f"Width: {widthS}\nHeight: {heightS}")

t = turtle.Turtle()
t.ht()

# floor / ceil func
def draw_half(color, y_start):
    t.goto(0, y_start)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    
    for _ in range(2):
        t.forward(widthS)
        t.right(90)
        t.forward(heightS // 2)
        t.right(90)
        
    t.end_fill()
    t.penup()

# draw pixel
def put_pixel(x, y, hex):
    if x > widthS or y > heightS or x < 0 or y < 0:
        return
    
    t.goto(x, y)
    t.pen(pencolor=hex, pensize=0)
    t.fillcolor(hex)
    t.begin_fill()

    for _ in range(4):
        t.forward(1)
        t.right(90)
    
    t.end_fill()
    t.penup()
   
# line algo
def draw_line(x0, y0, x1, y1):
    start = (x0, y0)
    end = (x1, y1)
    
    t.pen(pencolor="#ff0000", pensize=1)
    t.goto(start)
    t.pendown()
    t.goto(end)
    t.penup()

def render():
    for polyIdx in range(MAX_POLYS):
        for vertIdx in range(polys[polyIdx].vertCnt - 1):
            p1: Vec2 = polys[polyIdx].vert[vertIdx]
            p2: Vec2 = polys[polyIdx].vert[vertIdx + 1]
            height: float = -polys[polyIdx].height
            
            distX1: float = p1.x - cam.camPos.x
            distY1: float = p1.y - cam.camPos.y
            z1: float = distX1 * cos(cam.camAngle) + distY1 * sin(cam.camAngle)
            
            distX2: float = p2.x - cam.camPos.x
            distY2: float = p2.y - cam.camPos.y
            z2: float = distX2 * cos(cam.camAngle) + distY2 * sin(cam.camAngle)
            
            distX1 = distX1 * sin(cam.camAngle) - distY1 * cos(cam.camAngle)
            distX2 = distX2 * sin(cam.camAngle) - distY2 * cos(cam.camAngle)
            
            widthRatio: float = widthS / 2
            heightRatio: float = (widthS * heightS) / 60.0
            centerHeight: float = heightS / 2
            centerWidth: float = widthS / 2
            
            x1: float = -distX1 * widthRatio / z1
            x2: float = -distX2 * widthRatio / z2
            y1a: float = (height - heightRatio) / z1
            y1b: float = heightRatio / z1
            y2a: float = (height - heightRatio) / z2
            y2b: float = heightRatio / z2
            
# draw here
draw_half("#6d7178", heightS // 2)
draw_half("#8c602a", heightS)

Init(cam, polys)

put_pixel(100, 100, "#0000ff")
draw_line(0, 0, widthS, heightS)

# draw to screen
screen.update()
screen.mainloop()