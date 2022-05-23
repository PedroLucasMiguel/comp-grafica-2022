import numpy as np


'''
    This module provides methods to count how many groups
    of pixels exist in a combined space of two square shapes.
    The shapes are assumed not to be overlapping.
'''


def __create_grid(shape1, shape2):
    '''
        Create a new grid or shape that is the union of the two privided shapes.
        To do such, first a zero-ed grid is created with a size that encompasses
        both shapes and then each pixel of each shape is checked and copied into this grid.
        This strategy takes into consideration that both shapes can be anywhere in a 2D space,
        not necessarily in contact, but can't be overlapping.
    '''
    output = np.zeros((
        shape1["sizeY"]
        + shape2["sizeY"]
        + (shape2["offsetY"] - (shape1["sizeY"] + shape1["offsetY"]) if shape1["offsetY"] <
           shape2["offsetY"] else shape1["offsetY"] - (shape2["sizeY"] + shape2["offsetY"])),
        shape1["sizeX"]
        + shape2["sizeX"]
        + (shape2["offsetX"] - (shape1["sizeX"] + shape1["offsetX"]) if shape1["offsetX"] <
           shape2["offsetX"] else shape1["offsetX"] - (shape2["sizeX"] + shape2["offsetX"]))))

    out_offsetX = min(shape1["offsetX"], shape2["offsetX"])
    out_offsetY = min(shape1["offsetY"], shape2["offsetY"])

    for j in range(shape1["offsetX"], shape1["offsetX"] + shape1["sizeX"]):
        for i in range(shape1["offsetY"], shape1["offsetY"] + shape1["sizeY"]):
            output[i - out_offsetY][j - out_offsetX] = shape1["grid"][i -
                                                                      shape1["offsetY"]][j - shape1["offsetX"]]
    for j in range(shape2["offsetX"], shape2["offsetX"] + shape2["sizeX"]):
        for i in range(shape2["offsetY"], shape2["offsetY"] + shape2["sizeY"]):
            output[i - out_offsetY][j - out_offsetX] = shape2["grid"][i -
                                                                      shape2["offsetY"]][j - shape2["offsetX"]]

    return output


def __check_neighbourhood_4(grid, i, j, value):
    '''
        Check all 4 neighbours of the current cell recursively.
        If there is a neighbour with value 1, that means it haven't been checked yet.
        As such it receives the current group ID value and the
        recursion is called for each of it's neighbours.
    '''
    if (grid[i][j] != 1):
        return False

    grid[i][j] = value
    for k in range(0, 2):
        x = i + 1 if k else i - 1
        y = j + 1 if k else j - 1
        if x < len(grid) and x > -1:
            __check_neighbourhood_4(grid, x, j, value)
        if y < len(grid[0]) and y > -1:
            __check_neighbourhood_4(grid, i, y, value)

    return True


def __check_neighbourhood_8(grid, i, j, value):
    '''
        Check all 8 neighbours of the current cell recursively.
        If there is a neighbour with value 1, that means it haven't been checked yet.
        As such it receives the current group ID value and the
        recursion is called for each of it's neighbours.
    '''
    if (grid[i][j] != 1):
        return False

    grid[i][j] = value
    for k in range(0, 2):
        for l in range(0, 2):
            x = i + 1 if k else i - 1
            y = j + 1 if l else j - 1
            if x < len(grid) and x > -1 and y < len(grid[0]) and y > -1:
                __check_neighbourhood_8(grid, x, y, value)
        x = i + 1 if k else i - 1
        y = j + 1 if k else j - 1
        if x < len(grid) and x > -1:
            __check_neighbourhood_8(grid, x, j, value)
        if y < len(grid[0]) and y > -1:
            __check_neighbourhood_8(grid, i, y, value)

    return True


def __count_connected(shape1, shape2, check_neighbourhood_fn):
    '''
        Create a combined grid of the two shapes and then call
        the check_neighbourhood_fn for every pixel in the grid.
        The groups are labelled given the value of n_groups and
        the result is found by subtracting 1 from n_groups in the end.
    '''
    n_groups = 1

    grid = __create_grid(shape1, shape2)

    for j in range(0, len(grid[0])):
        for i in range(0, len(grid)):
            n_groups += 1 if check_neighbourhood_fn(
                grid, i, j, pow(2, n_groups)) else 0

    return n_groups - 1


def count_connected_4(shape1, shape2):
    '''
        Count how many groups of pixel in the combined
        space of the two shapes there are with 4-neighbourhood.
    '''
    return __count_connected(shape1, shape2, __check_neighbourhood_4)


def count_connected_8(shape1, shape2):
    '''
        Count how many groups of pixel in the combined
        space of the two shapes there are with 8-neighbourhood.
    '''
    return __count_connected(shape1, shape2, __check_neighbourhood_8)
