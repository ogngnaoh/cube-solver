from preprocess_image import preprocess_image
import os
from paths import image_dir
import kociemba


def cube_state(image_dir):
    cube_dict = {}

    # adding the colors of the faces in order to a dictionary as a data structure to represent cube state
    for filename in os.listdir(image_dir):
        orientation = os.path.splitext(filename)[0]
        ordered_colors = preprocess_image(os.path.join(image_dir, filename))
        cube_dict[orientation] = ordered_colors

    # ordering the cube state to match the one required by the kociemba library
    cube_order = ['up', 'right', 'front', 'down', 'left', 'back']
    ordered_cube_dict = {}

    for face in cube_order:
        ordered_cube_dict[face] = cube_dict[face]

    cube_state = ''
    for face in ordered_cube_dict:
        cube_state += ''.join(ordered_cube_dict[face])

    return cube_state


# uses kociemba library to solve cube given cube state representation as a string
def solve_cube(cube_state):
    solution = kociemba.solve(cube_state)
    return solution


if __name__ == '__main__':
    cube_state = cube_state(image_dir)
    print(f'solution: {solve_cube(cube_state)}')
