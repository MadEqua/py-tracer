import math

class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def fromValue(v):
        return Vec3(v, v, v)

    @staticmethod
    def fromValues(x, y, z):
        return Vec3(x, y, z)

    @staticmethod
    def fromVec2AndValue(vec2, z):
        return Vec3(vec2.x, vec2.y, z)

    @staticmethod
    def zero():
        return Vec3(0, 0, 0)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, (int, float)):
            return Vec3(self.x + other, self.y + other, self.z + other)
        else:
            raise TypeError("Vec3 add not implemented for {}".__format__(other.__class__))

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, (int, float)):
            return Vec3(self.x - other, self.y - other, self.z - other)
        else:
            raise TypeError("Vec3 sub not implemented for {}".__format__(other.__class__))

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (int, float)):
            return Vec3(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError("Vec3 mul not implemented for {}".__format__(other.__class__))

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        elif isinstance(other, (int, float)):
            return Vec3(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError("Vec3 div not implemented for {}".__format__(other.__class__))

    def __pow__(self, other):
        if isinstance(other, self.__class__):
            return Vec3(self.x ** other.x, self.y ** other.y, self.z ** other.z)
        elif isinstance(other, (int, float)):
            return Vec3(self.x ** other, self.y ** other, self.z ** other)
        else:
            raise TypeError("Vec3 pow not implemented for {}".__format__(other.__class__))

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def sqrLength(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalize(self):
        len = self.length()
        self.x /= len
        self.y /= len
        self.z /= len
        return self

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vec3.fromValues(self.y * other.z - self.z * other.y, 
                               self.z * other.x - self.x * other.z,
                               self.x * other.y - self.y * other.x)

    def reflect(self, n):
        return self - 2 * self.dot(n) * n

    def toTuple(self):
        return (self.x, self.y, self.z)

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def fromValue(v):
        return Vec2(v, v)

    @staticmethod
    def fromValues(x, y):
        return Vec2(x, y)

    @staticmethod
    def zero():
        return Vec2(0, 0)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vec2(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Vec2(self.x + other, self.y + other)
        else:
            raise TypeError("Vec2 add not implemented for {}".__format__(other.__class__))

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vec2(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return Vec2(self.x - other, self.y - other)
        else:
            raise TypeError("Vec2 sub not implemented for {}".__format__(other.__class__))

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vec2(self.x * other.x, self.y * other.y)
        elif isinstance(other, (int, float)):
            return Vec2(self.x * other, self.y * other)
        else:
            raise TypeError("Vec2 mul not implemented for {}".__format__(other.__class__))

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vec2(self.x / other.x, self.y / other.y)
        elif isinstance(other, (int, float)):
            return Vec2(self.x / other, self.y / other)
        else:
            raise TypeError("Vec2 div not implemented for {}".__format__(other.__class__))

    def __pow__(self, other):
        if isinstance(other, self.__class__):
            return Vec3(self.x ** other.x, self.y ** other.y)
        elif isinstance(other, (int, float)):
            return Vec3(self.x ** other, self.y ** other)
        else:
            raise TypeError("Vec2 pow not implemented for {}".__format__(other.__class__))

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def sqrLength(self):
        return self.x * self.x + self.y * self.y

    def normalize(self):
        len = self.length()
        self.x /= len
        self.y /= len
        return self

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - other.x * self.y

    def reflect(self, n):
        return self - 2 * self.dot(n) * n

    def toTuple(self):
        return (self.x, self.y)