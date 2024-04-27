from matrix_functions import *


class Camera:
    def __init__(self, render_height: int, render_width: int, position, rotation_speed=0.005) -> None:
        self.position = numpy.array([*position, 1.0])
        self.forward = numpy.array([0, 0, 1, 1])
        self.up = numpy.array([0, 1, 0, 1])
        self.right = numpy.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render_height / render_width)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 0.3
        self.rotation_speed = rotation_speed

        self.anglePitch = 0
        self.angleYaw = 0
        self.angleRoll = 0

    def camera_yaw(self, angle) -> None:
        self.angleYaw += angle

    def camera_pitch(self, angle) -> None:
        self.anglePitch += angle

    def axii_identity(self) -> None:
        self.forward = numpy.array([0, 0, 1, 1])
        self.up = numpy.array([0, 1, 0, 1])
        self.right = numpy.array([1, 0, 0, 1])

    def camera_update_axii(self) -> None:
        rotate = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)
        self.axii_identity()
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_matrix(self) -> numpy.array:
        self.camera_update_axii()
        return self.translate_matrix() @ self.rotate_matrix()

    def translate_matrix(self) -> numpy.array:
        x, y, z, w = self.position
        return numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self) -> numpy.array:
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return numpy.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
