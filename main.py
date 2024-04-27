from SoftwareRender import SoftwareRender, get_object_from_file


def main() -> int:
    path_to_bear = r"objects/object_bear.obj"
    path_to_parallelepiped = r"objects/parallelepiped.obj"
    path_to_cube = r"objects/cube.obj"

    render = SoftwareRender(1200, 720)

    bear = get_object_from_file(render, path_to_bear)
    cube = get_object_from_file(render, path_to_cube)
    parallelepiped = get_object_from_file(render, path_to_parallelepiped)

    render.add_object(bear)
    render.add_object(parallelepiped)
    render.add_object(cube)

    render.run()
    return 0


if __name__ == "__main__":
    main()
