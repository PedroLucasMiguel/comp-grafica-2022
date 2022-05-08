import numpy as np


def __create_grid(shape1, shape2):
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


def __count_connected(shape1, shape2, check_neighbourhood):
    n_groups = 1

    grid = __create_grid(shape1, shape2)

    for j in range(0, len(grid[0])):
        for i in range(0, len(grid)):
            n_groups += 1 if check_neighbourhood(
                grid, i, j, pow(2, n_groups)) else 0

    return n_groups - 1


def count_connected_4(shape1, shape2):
    return __count_connected(shape1, shape2, __check_neighbourhood_4)


def count_connected_8(shape1, shape2):
    return __count_connected(shape1, shape2, __check_neighbourhood_8)
