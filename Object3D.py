import pygame
from matrix_functions import *
from numba import njit


@njit(fastmath=True)
def any_func(arr, a, b) -> bool:
    return numpy.any((arr == a) | (arr == b))


class Object3D:
    def __init__(self, render, vertices='', faces='') -> None:
        self.render = render
        self.vertices = numpy.array(vertices)
        self.faces = faces
        self.translate([0.0001, 0.0001, 0.0001])

        self.font = pygame.font.SysFont('Arial', 30, bold=True)
        self.color_faces = [(pygame.Color('orange'), face) for face in self.faces]
        self.draw_vertices = False
        self.label = ''

    def draw(self) -> None:
        self.screen_projection()

    def screen_projection(self) -> None:
        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertices[face]
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pygame.draw.polygon(self.render.window, color, polygon, 1)
                if self.label:
                    text = self.font.render(self.label[index], True, pygame.Color('white'))
                    self.render.window.blit(text, polygon[-1])

        if self.draw_vertices:
            for vertex in vertices:
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pygame.draw.circle(self.render.window, pygame.Color('white'), vertex, 2)

    def translate(self, pos) -> None:
        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to: float) -> None:
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle: float) -> None:
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle: float) -> None:
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle: float) -> None:
        self.vertices = self.vertices @ rotate_z(angle)


class Axes(Object3D):
    def __init__(self, render) -> None:
        super().__init__(render)
        self.vertices = numpy.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = numpy.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pygame.Color('red'), pygame.Color('green'), pygame.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False
        self.label = 'XYZ'
