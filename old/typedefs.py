from dataclasses import dataclass, field
from typing import List

MAX_POLYS = 10
MAX_VERTS = 8

@dataclass
class Vec2:
    x: float
    y: float

@dataclass
class LineSeg:
    p1: Vec2
    p2: Vec2

@dataclass
class Polygon:
    vert: List[Vec2] = field(default_factory=lambda: [Vec2(0, 0) for _ in range(MAX_VERTS)])
    vertCnt: int = 0
    height: float = 0.0
    curDist: float = 0.0

@dataclass
class ScreenSpacePoly:
    vert: List[Vec2] = field(default_factory=lambda: [Vec2(0, 0) for _ in range(4)])
    distFromCamera: float = 0.0
    planeIdInPoly: int = 0

@dataclass
class Camera:
    camAngle: float = 0.0
    stepWave: float = 0.0
    camPos: Vec2 = field(default_factory=lambda: Vec2(0, 0))
    oldCamPos: Vec2 = field(default_factory=lambda: Vec2(0, 0))