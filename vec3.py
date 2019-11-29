

class Vec3(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return super().__init__(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return super().__init__(x, y, z)

    def __lt__(self, other):
        if self.x < other.x and self.y < other.y and self.z < other.z:
            return True
        else:
            return False

    def __le__(self, other):
        if self.x <= other.x and self.y <= other.y and self.z <= other.z:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.x > other.x and self.y > other.y and self.z > other.z:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.x >= other.x and self.y >= other.y and self.z >= other.z:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        else:
            return False

    def __ne__(self, other):
        return not(self.__eq__(self, other))

    @classmethod
    def axis_z_up(cls, point):
        return cls(x=point.x, y=-point.z, z=point.y)
