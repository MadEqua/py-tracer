from collections import namedtuple
from PIL import Image
from vec import Vec2, Vec3
import math
import random

class Material:
    def __init__(self, color):
        self.color = color

class MirrorMaterial(Material):
    def __init__(self, color):
        super().__init__(color)

class DiffuseMaterial(Material):
    def __init__(self, color, specPower):
        super().__init__(color)
        self.specPower = specPower

Ray = namedtuple('Ray', 'origin dir')
Light = namedtuple('Light', 'dir color')
Sphere = namedtuple('Sphere', 'center r material')

RENDER_SIZE = Vec2.fromValues(100, 100)
CAMERA_POS = Vec3.fromValues(0, 1, -3)
CAMERA_LOOK_AT = Vec3.fromValue(0)

LIGHTS = (Light(Vec3.fromValues(1, -0.4, 0.7).normalize(), Vec3.fromValue(1)),)

MAT_DIFF_GREY = DiffuseMaterial(Vec3.fromValue(0.5), 10)
SCENE = [Sphere(Vec3.fromValues(0, -99999, 0), 99999, MAT_DIFF_GREY)]

class Solution:
    def __init__(self, isReal, root1 = -1, root2 = -1):
        self.isReal = isReal
        self.root1 = root1
        self.root2 = root2

class Intersection:
    def __init__(self, intersects, t = -1, point = Vec3.zero(), normal = Vec3.zero(), material = MAT_DIFF_GREY):
        self.intersects = intersects
        self.t = t
        self.point = point
        self.normal = normal
        self.material = material

def solveQuadratic(a, b, c):
    discr = b * b - 4 * a * c
    if(discr < 0):
        return Solution(False)
    elif discr == 0:
        root1 = root2 = -0.5 * b / a
    else:
        q = -0.5 * ((b + math.sqrt(discr)) if b > 0 else (b - math.sqrt(discr)))
        root1 = q / a
        root2 = c / q
    
    if(root1 > root2):
        root1, root2 = root2, root1
    return Solution(True, root1, root2)

def raySphereIntersection(ray, sphere):
    L = ray.origin - sphere.center
    a = ray.dir.sqrLength()
    b = 2 * ray.dir.dot(L)
    c = L.sqrLength() - (sphere.r * sphere.r)

    solution = solveQuadratic(a, b, c)
    if(not solution.isReal):
        return Intersection(False)
    
    if(solution.root1 < 0):
        solution.root1 = solution.root2
        if(solution.root1 < 0):
            return Intersection(False)

    point = ray.origin + ray.dir * solution.root1
    normal = (point - sphere.center).normalize()
    return Intersection(True, solution.root1, point, normal, sphere.material)

def scene(rayWorld):    
    FL_INF = float('+inf')
    minT = FL_INF
    for sphere in SCENE:
        inter = raySphereIntersection(rayWorld, sphere)
        if(inter.intersects and inter.t < minT):
            minT = inter.t
            minInter = inter

    if(minT < FL_INF):
        return minInter
    else:
        return Intersection(False)

def shade(intersection):
    col = Vec3.zero()
    for light in LIGHTS:
        L = -light.dir
        V = (CAMERA_POS - intersection.point).normalize()
        H = (L + V).normalize()

        if isinstance(intersection.material, DiffuseMaterial):
            diff = max(L.dot(intersection.normal), 0)
            spec = max(H.dot(intersection.normal), 0) ** intersection.material.specPower
            col = (diff * intersection.material.color + spec * Vec3.fromValue(1)) * light.color
        else:
            col = Vec3.fromValue(1)

        shadowRay = Ray(intersection.point + 0.01 * intersection.normal, L)
        if scene(shadowRay).intersects:
            col *= 0.3

    col += 0.01
    return col

def cameraToWorld(v):
    camInWorldZ = (CAMERA_LOOK_AT - CAMERA_POS).normalize()
    camInWorldY = Vec3.fromValues(0, 1, 0)
    camInWorldX = camInWorldY.cross(camInWorldZ).normalize()
    camInWorldY = camInWorldZ.cross(camInWorldX).normalize()

    return camInWorldX * v.x  + camInWorldY * v.y + camInWorldZ * v.z

def trace(rayWorld, depth = 0):
    if(depth > 3): return Vec3.fromValue(0)

    intersection = scene(rayWorld)
    if(intersection.intersects):
        if(isinstance(intersection.material, DiffuseMaterial)):
            return shade(intersection)
        elif(isinstance(intersection.material, MirrorMaterial)):
            return shade(intersection) * trace(Ray(intersection.point + 0.01 * intersection.normal, rayWorld.dir.reflect(intersection.normal)), depth + 1)
    else:
        return Vec3.fromValues(0.23, 0.30, 1)

def coordToIndex(x, y):
    return ((RENDER_SIZE.y - y - 1) * RENDER_SIZE.x + x) * 3

def render():
    buffer = bytearray(RENDER_SIZE.x * RENDER_SIZE.y * 3)

    for y in range(RENDER_SIZE.y):
        for x in range(RENDER_SIZE.x):

            #y -> [-0.5, 0.5], x -> [-A, A] A depending on ascpect ratio
            cameraDir = Vec3.fromVec2AndValue((Vec2.fromValues(x, y) - (RENDER_SIZE / 2)) / RENDER_SIZE.y, 1)
            rayWorld = Ray(CAMERA_POS, cameraToWorld(cameraDir))
            col = trace(rayWorld)
            
            idx = coordToIndex(x, y)

            #Global tone mapping and gamma correction
            col /= (col + 1)
            col **= (1 / 2.2)

            buffer[idx:idx + 3] = (int(c * 255.0) for c in col.toTuple())
            #buffer[idx + 0] = int(col.x * 255.0)
            #buffer[idx + 1] = int(col.y * 255.0)
            #buffer[idx + 2] = int(col.z * 255.0)

    image = Image.frombytes('RGB', RENDER_SIZE.toTuple(), bytes(buffer))
    image.save('render.png')

def generateScene():
    random.seed(39)
    for x in range(-5, 5):
        for z in range(-5, 5):
            matColor = Vec3.fromValues(random.random(), random.random(), random.random())
            if(random.random() < 0.2):
                mat = MirrorMaterial(matColor)
            else:
                mat = DiffuseMaterial(matColor, random.uniform(1.0, 100.0))
            r = random.uniform(0.1, 0.5)
            DISPLACEMENT_MAX = 0.22
            pos = Vec3.fromValues(x + random.uniform(-DISPLACEMENT_MAX, DISPLACEMENT_MAX), r, z + random.uniform(-DISPLACEMENT_MAX, DISPLACEMENT_MAX))
            SCENE.append(Sphere(pos, r, mat))


generateScene()
render()