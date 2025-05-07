import turtle
from typedefs import Camera, Polygon, Vec2, ScreenSpacePoly
from levelinit import Init
from math import sin, cos
import keyboard
import time
import numpy as np

# constants
MOV_SPEED = 100000
ROT_SPEED = 500
MAX_POLYS = 10
MAX_VERTS = 8
SHOULD_RASTERIZE = 1
# decrease for better resolution; increase for better performance
RASTER_RESOLUTION = 4
RASTER_NUM_VERTS = 4

# setup
screen = turtle.Screen()
screen.tracer(0)

# globals
loop = True

delta_time: float = 0.0

cam = Camera()
polys = [Polygon() for _ in range(MAX_POLYS)]

screenSpaceVisiblePlanes: int = 0
screenSpacePolys = [[ScreenSpacePoly() for _ in range(MAX_VERTS)] for _ in range(MAX_POLYS)]

# screen info
widthS = screen.window_width()
heightS = screen.window_height()

# set the origin to the top-left corner
screen.setworldcoordinates(0, heightS, widthS, 0)

print(f"Width: {widthS}\nHeight: {heightS}")

t = turtle.Turtle()
t.ht()

# init the level
Init(cam, polys)

# floor / ceil func
# currently unused
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
# currently unused
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

# render shit
def render():
    t.clear()

    global screenSpaceVisiblePlanes
    
    if SHOULD_RASTERIZE:
        clear_raster_buffer()
        screenSpaceVisiblePlanes = 0
    
    for polyIdx in range(0, MAX_POLYS, 1):
        for i in range(0, min(polys[polyIdx].vertCnt - 1, MAX_VERTS), 1):
            p1: Vec2 = polys[polyIdx].vert[i]
            p2: Vec2 = polys[polyIdx].vert[i + 1]
            height: float = -polys[polyIdx].height
            
            if is_face_front(cam.camPos, p1, p2) > 0:
                continue
            
            distX1: float = p1.x - cam.camPos.x
            distY1: float = p1.y - cam.camPos.y
            z1: float = distX1 * cos(cam.camAngle) + distY1 * sin(cam.camAngle)
            
            distX2: float = p2.x - cam.camPos.x
            distY2: float = p2.y - cam.camPos.y
            z2: float = distX2 * cos(cam.camAngle) + distY2 * sin(cam.camAngle)
            
            distX1 = distX1 * sin(cam.camAngle) - distY1 * cos(cam.camAngle)
            distX2 = distX2 * sin(cam.camAngle) - distY2 * cos(cam.camAngle)
            
            if z1 > 0 or z2 > 0:
                i1: Vec2 = intersection(distX1, z1, distX2, z1, -0.0001, 0.0001, -20, 5)
                i2: Vec2 = intersection(distX1, z1, distX2, z1, 0.0001, 0.0001, 20, 5)
                
                if z1 <= 0:
                    if i1.y < 0:
                        distX1 = i1.x
                        z1 = i1.y
                    else:
                        distX1 = i2.x
                        z1 = i2.y
                elif z2 <= 0:
                    if i1.y > 0:
                        distX2 = i1.x
                        z2 = i1.y
                    else:
                        distX2 = i2.x
                        z2 = i2.y
            else:
                continue
            
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
            
            draw_line(centerWidth + x1, centerHeight + y1a, centerWidth + x2, centerHeight + y2a)
            draw_line(centerWidth + x1, centerHeight + y1b, centerWidth + x2, centerHeight + y2b)
            draw_line(centerWidth + x1, centerHeight + y1a, centerWidth + x1, centerHeight + y1b)
            draw_line(centerWidth + x2, centerHeight + y2a, centerWidth + x2, centerHeight + y2b)
            
            if SHOULD_RASTERIZE:
                if screenSpaceVisiblePlanes >= MAX_POLYS:
                    print("Error: Too many planes")
                    break
                
                planeIdx = screenSpaceVisiblePlanes
                print(f"PlaneIdx: {planeIdx}")
                print(f"VertCnt: {polys[polyIdx].vertCnt}")

                if i >= MAX_VERTS:
                    print("Error: Too many vertices")
                    break
                
                screenSpacePolys[planeIdx][i].vert[0].x = centerWidth + x2
                screenSpacePolys[planeIdx][i].vert[0].y = centerHeight + y2a
                screenSpacePolys[planeIdx][i].vert[1].x = centerWidth + x1
                screenSpacePolys[planeIdx][i].vert[1].y = centerHeight + y1a
                screenSpacePolys[planeIdx][i].vert[2].x = centerWidth + x1
                screenSpacePolys[planeIdx][i].vert[2].y = centerHeight + y1b
                screenSpacePolys[planeIdx][i].vert[3].x = centerWidth + x2
                screenSpacePolys[planeIdx][i].vert[3].y = centerHeight + y2b
                
                screenSpacePolys[planeIdx][i].planeIdInPoly = i
                screenSpaceVisiblePlanes += 1
                
    rasterize()

# cross product of 2D points
# fuck if i know how this works
def cross_2d_points(x1, y1, x2, y2) -> float:
    return x1 * y2 - y1 * x2

# same thing with cross product but i dont know what it does
def intersection(
    x1, y1, x2, y2,
    x3, y3, x4, y4) -> Vec2:
    p: Vec2 = Vec2(0, 0)
    
    p.x = cross_2d_points(x1, y1, x2, y2)
    p.y = cross_2d_points(x3, y3, x4, y4)
    
    det: float = cross_2d_points(x1 - x2, y1 - y2, x3 - x4, y3 - y4)
    
    p.x = cross_2d_points(p.x, x1 - x2, p.y, x3 - x4) / det
    p.y = cross_2d_points(p.x, y1 - y2, p.y, y3 - y4) / det
    
    return p

# check if front face
def is_face_front(Camera: Vec2, pointA: Vec2, pointB: Vec2) -> int:
    localA = Vec2(pointA.x - Camera.x, pointA.y - Camera.y)
    localB = Vec2(pointB.x - Camera.x, pointB.y - Camera.y)
    
    cross_product = localA.x * localB.y - localA.y * localB.x
    
    if cross_product > 0:
        return 1
    if cross_product < 0:
        return -1
    
    return 0

def camera_translate(delta_time: float):
    if keyboard.is_pressed("w"):
        cam.camPos.x += MOV_SPEED * cos(cam.camAngle) * delta_time
        cam.camPos.y += MOV_SPEED * sin(cam.camAngle) * delta_time
    elif keyboard.is_pressed("s"):
        cam.camPos.x -= MOV_SPEED * cos(cam.camAngle) * delta_time
        cam.camPos.y -= MOV_SPEED * sin(cam.camAngle) * delta_time
    
    if keyboard.is_pressed("a"):
        cam.camAngle -= ROT_SPEED * delta_time
    elif keyboard.is_pressed("d"):
        cam.camAngle += ROT_SPEED * delta_time
        
    # print(f"CamPos: {cam.camPos.x}, {cam.camPos.y}")
    # print(f"CamAngle: {cam.camAngle}")

def point_in_poly(nvert, vertx: float, verty: float, testx: float, testy: float) -> bool:
    i = 0
    j = 0
    is_point_inside = False
    
    for i in range(nvert):
        j = nvert - 1
        
        is_same_coordinates = False
        
        if (verty[i] > testy) == (verty[j] > testy):
            is_same_coordinates = True
        
        if not is_same_coordinates and (testx < (vertx[j] - vertx[i]) * (testy - verty[i]) / (verty[j] - verty[i]) + vertx[i]):
            is_point_inside = not is_point_inside
    
    return is_point_inside

def clear_raster_buffer():
    for polyIdx in range(MAX_POLYS):
        for i in range(polys[polyIdx].vertCnt):
            for vn in range(RASTER_NUM_VERTS):
                screenSpacePolys[polyIdx][i].vert[vn].x = 0
                screenSpacePolys[polyIdx][i].vert[vn].y = 0
                
def rasterize():
    global screenSpaceVisiblePlanes

    vx = [0.0] * 4
    vy = [0.0] * 4
    
    pixel_buff = np.zeros((heightS, widthS, 3), dtype=np.uint8)
    pixel_buff.fill(0)
    
    for polyIdx in range(screenSpaceVisiblePlanes - 1, -1, -1):
        for nextv in range(RASTER_NUM_VERTS):
            planeId = screenSpacePolys[polyIdx][nextv].planeIdInPoly
            
            vx[nextv] = screenSpacePolys[polyIdx][planeId].vert[nextv].x
            vy[nextv] = screenSpacePolys[polyIdx][planeId].vert[nextv].y
        
        for y in range(0, heightS - RASTER_RESOLUTION + 1, RASTER_RESOLUTION):
            for x in range(0, widthS, 1):
                if np.any(pixel_buff[y][x] != 0):
                    continue
                    
                if point_in_poly(RASTER_NUM_VERTS, vx, vy, x, y) == 1:
                    put_pixel(x, y, "#64FF00")
                    pixel_buff[y][x] = 1

while loop:
    if keyboard.is_pressed("esc"):
        loop = False
    
    # start time
    start: float = time.time()

    # translate camera
    camera_translate(delta_time)

    # render the scene
    render()

    # draw to screen
    screen.update()
    
    # end time
    end: float = time.time()
    delta_time = (end - start) / 1000.0
    
    # fps
    fps = 1 / delta_time if delta_time > 0 else 0
    print(f"FPS: {fps:.2f}")