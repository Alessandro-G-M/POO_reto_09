import math
import time

class Point:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def move(self, new_x: float, new_y: float):
        self.x = new_x
        self.y = new_y

    def reset(self):
        self.x = 0
        self.y = 0

    def compute_distance(self, point: "Point") -> float:
        return ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def lenght(self):
        return ((self.end.x - self.start.x)**2 + (self.end.y - self.start.y)**2)**0.5


class Shape:
    def __init__(self, vertices=None, edges=None, inner_angles=None, is_regular=False):
        self._vertices = vertices if vertices is not None else []
        self._edges = edges if edges is not None else []
        self._inner_angles = inner_angles if inner_angles is not None else []
        self._is_regular = is_regular

        if not self._edges and self._vertices:
            self.define_edges()
        elif not self._vertices and self._edges:
            self.define_vertices()

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, value):
        self._vertices = value

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, value):
        self._edges = value

    @property
    def inner_angles(self):
        return self._inner_angles

    @inner_angles.setter
    def inner_angles(self, value):
        self._inner_angles = value

    @property
    def is_regular(self):
        if not self.edges or not self.inner_angles:
            return False
        same_edges = all(edge.lenght() == self.edges[0].lenght() for edge in self.edges)
        same_inner_angles = all(angle == self.inner_angles[0] for angle in self.inner_angles)
        return same_edges and same_inner_angles

    @classmethod
    def create_shape(cls, shape_type, **kwargs):
        shape_classes = {
            "rectangle": Rectangle,
            "square": Square,
            "triangle": Triangle,
            "equilateral": Equilateral,
            "isosceles": Isosceles,
            "scalene": Scalene,
            "trirectangle": TriRectangle
        }
        if shape_type.lower() not in shape_classes:
            raise ValueError(f"Unsupported shape type: {shape_type}")
        return shape_classes[shape_type.lower()](**kwargs)

    @staticmethod
    def timer(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Computation time of {func.__name__}: {end_time - start_time:.6f} seconds")
            return result
        return wrapper

    def define_edges(self):
        pass

    def define_vertices(self):
        pass

    def compute_perimeter(self) -> float:
        pass

    def compute_area(self) -> float:
        pass


class Rectangle(Shape):
    def __init__(self, vertices=None, edges=None, inner_angles=None):
        super().__init__(vertices, edges, inner_angles or [90, 90, 90, 90])
        if len(self.vertices) != 4 or len(self.edges) != 4:
            raise ValueError("A rectangle has exactly 4 edges or 4 vertices")

    def define_edges(self):
        self.edges = [
            Line(self.vertices[0], self.vertices[1]),
            Line(self.vertices[1], self.vertices[2]),
            Line(self.vertices[2], self.vertices[3]),
            Line(self.vertices[3], self.vertices[0])
        ]

    def define_vertices(self):
        self.vertices = [
            self.edges[0].start,
            self.edges[0].end,
            self.edges[1].end,
            self.edges[2].end
        ]

    def compute_perimeter(self) -> float:
        return sum(edge.lenght() for edge in self.edges)

    @Shape.timer
    def compute_area(self) -> float:
        return self.edges[0].lenght() * self.edges[1].lenght()


class Square(Rectangle):
    def __init__(self, vertices=None, edges=None):
        super().__init__(vertices, edges)
        if any(edge.lenght() != self.edges[0].lenght() for edge in self.edges):
            raise ValueError("All edges must be equal in a square")


class Triangle(Shape):
    def __init__(self, vertices=None, edges=None, inner_angles=None, is_regular=False):
        super().__init__(vertices, edges, inner_angles, is_regular)
        if len(self.vertices) != 3 or len(self.edges) != 3:
            raise ValueError("A triangle has exactly 3 edges or 3 vertices")

    def define_edges(self):
        self.edges = [
            Line(self.vertices[0], self.vertices[1]),
            Line(self.vertices[1], self.vertices[2]),
            Line(self.vertices[2], self.vertices[0])
        ]

    def define_vertices(self):
        self.vertices = [
            self.edges[0].start,
            self.edges[0].end,
            self.edges[1].end
        ]

    def compute_perimeter(self):
        return sum(edge.lenght() for edge in self.edges)

    @Shape.timer
    def compute_area(self):
        a, b, c = [edge.lenght() for edge in self.edges]
        s = (a + b + c) / 2
        return (s * (s - a) * (s - b) * (s - c)) ** 0.5


class Equilateral(Triangle):
    def __init__(self, vertices=None, edges=None):
        super().__init__(vertices, edges, [60, 60, 60], True)


class Isosceles(Triangle):
    def __init__(self, vertices=None, edges=None):
        super().__init__(vertices, edges)
        self.compute_inner_angles()

    def compute_inner_angles(self):
        a, b, c = [edge.lenght() for edge in self.edges]
        if a == b or a == c or b == c:
            equal_sides = a if a == b else c
            base = c if a == b else a
            angle_base = math.degrees(math.acos((2 * equal_sides**2 - base**2) / (2 * equal_sides**2)))
            self._inner_angles = [(180 - angle_base)/2, (180 - angle_base)/2, angle_base]
        else:
            raise ValueError("Not an isosceles triangle")


class Scalene(Triangle):
    def __init__(self, vertices=None, edges=None):
        super().__init__(vertices, edges)
        self.compute_inner_angles()

    def compute_inner_angles(self):
        a, b, c = [edge.lenght() for edge in self.edges]
        angle_a = math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c)))
        angle_b = math.degrees(math.acos((a**2 + c**2 - b**2) / (2 * a * c)))
        angle_c = 180 - angle_a - angle_b
        self._inner_angles = [angle_a, angle_b, angle_c]


class TriRectangle(Triangle):
    def __init__(self, vertices=None, edges=None):
        super().__init__(vertices, edges)
        self.compute_inner_angles()

    def compute_inner_angles(self):
        sides = sorted([edge.lenght() for edge in self.edges])
        angle1 = math.degrees(math.asin(sides[0]/sides[2]))
        self._inner_angles = [angle1, 90 - angle1, 90]
