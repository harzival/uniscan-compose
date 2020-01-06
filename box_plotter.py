import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from vec3 import Vec3


class BoxPlotter:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = plt.axes(projection="3d")

    def start(self):
        plt.show()

    def set_plot_size_limit_box(self, box):
        def largest_between(a, b, c):
            if (a >= b) and (a >= c):
                return a
            elif (b >= a) and (b >= c):
                return b
            else:
                return c

        center = box.get_center()
        size = largest_between(
            box.get_width(), box.get_depth(), box.get_height()
        )
        radius = round(size * (1.5 / 2), 5)
        self.ax.set_xlim(center.x - radius, center.x + radius)
        self.ax.set_ylim(center.y - radius, center.y + radius)
        self.ax.set_zlim(center.z - radius, center.z + radius)

    def draw_line(self, start=Vec3(0, 0, 0), end=Vec3(0, 0, 0), color="black"):
        self.ax.plot(
            [start.x, end.x], [start.y, end.y], [start.z, end.z], color=color
        )

    def draw_dist_lines(self, box):
        self.draw_line(box.center, box.x_bound_point, "red")
        self.draw_line(box.x_bound_point, box.y_bound_point, "green")
        self.draw_line(box.y_bound_point, box.z_bound_point, "blue")

    def draw_edges_from_corner_points(self, corner_points, color="grey"):
        pnts = corner_points
        self.draw_line(pnts[0], pnts[1], color)
        self.draw_line(pnts[1], pnts[3], color)
        self.draw_line(pnts[2], pnts[0], color)
        self.draw_line(pnts[3], pnts[2], color)
        self.draw_line(pnts[4], pnts[5], color)
        self.draw_line(pnts[5], pnts[7], color)
        self.draw_line(pnts[6], pnts[4], color)
        self.draw_line(pnts[7], pnts[6], color)
        self.draw_line(pnts[0], pnts[4], color)
        self.draw_line(pnts[1], pnts[5], color)
        self.draw_line(pnts[2], pnts[6], color)
        self.draw_line(pnts[3], pnts[7], color)

    def draw_edges(self, box, color="grey"):
        self.draw_edges_from_corner_points(
            box.calc_corner_points(box.min, box.max), color
        )
