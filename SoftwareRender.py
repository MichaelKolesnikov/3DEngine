from sys import exit
from Object3D import Object3D
from Camera import Camera
import pygame
from Projection import Projection


class SoftwareRender:
    def __init__(self, width: int, height: int) -> None:
        pygame.init()
        pygame.mouse.set_visible(False)
        self.RES = self.WIDTH, self.HEIGHT = width, height
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.window = pygame.display.set_mode(self.RES, pygame.RESIZABLE)
        self.full_screen_mode = False
        self.clock = pygame.time.Clock()
        self.camera = Camera(self.HEIGHT, self.WIDTH, [-5, 6, -55])
        self.projection = Projection(self)
        self.objects: list[Object3D] = []

    def add_object(self, object3d: Object3D) -> None:
        self.objects.append(object3d)

    def draw(self) -> None:
        self.window.fill(pygame.Color('darkslategray'))
        for object3d in self.objects:
            object3d.draw()

    def change_screen_mode(self) -> bool:
        if self.full_screen_mode:
            self.window = pygame.display.set_mode(self.RES, pygame.RESIZABLE)
        else:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.full_screen_mode = not self.full_screen_mode
        return self.full_screen_mode

    def control(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x >= 1200:
            pygame.mouse.set_pos(1, mouse_y)
        elif mouse_x == 0:
            pygame.mouse.set_pos(1200 - 1, mouse_y)
        elif mouse_y >= 700:
            pygame.mouse.set_pos(mouse_x, 1)
        elif mouse_y == 0:
            pygame.mouse.set_pos(mouse_x, 700 - 1)
        mouse_dr = pygame.mouse.get_rel()
        self.camera.camera_yaw(self.camera.rotation_speed * mouse_dr[0])
        self.camera.camera_pitch(self.camera.rotation_speed * mouse_dr[1])

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        if key[pygame.K_F11]:
            self.change_screen_mode()
        if key[pygame.K_a]:
            self.camera.position -= self.camera.right * self.camera.moving_speed
        if key[pygame.K_d]:
            self.camera.position += self.camera.right * self.camera.moving_speed
        if key[pygame.K_w]:
            self.camera.position += self.camera.forward * self.camera.moving_speed
        if key[pygame.K_s]:
            self.camera.position -= self.camera.forward * self.camera.moving_speed
        if key[pygame.K_SPACE]:
            if key[pygame.K_LSHIFT]:
                self.camera.position -= self.camera.up * self.camera.moving_speed
            else:
                self.camera.position += self.camera.up * self.camera.moving_speed

    def run(self) -> None:
        while True:
            self.draw()
            self.control()
            pygame.display.set_caption(str(self.camera.position))
            pygame.display.flip()
            self.clock.tick(self.FPS)


def get_object_from_file(render: SoftwareRender, filename: str) -> Object3D:
    vertex, faces = [], []
    with open(filename) as f:
        for line in f:
            if line.startswith('v '):
                vertex.append([float(i) for i in line.split()[1:]] + [1])
            elif line.startswith('f'):
                faces_ = line.split()[1:]
                faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
    return Object3D(render, vertex, faces)
