import numpy as np


def vizinhanca_4(shape1, shape2):
    n_groups = 1

    output = np.zeros((
        shape1["sizeY"]
        + shape2["sizeY"]
        + (shape2["offsetY"] - (shape1["sizeY"] + shape1["offsetY"]) if shape1["offsetY"] < shape2["offsetY"] else shape1["offsetY"] - (shape2["sizeY"] + shape2["offsetY"])),
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
    for j in range(0, len(output[0])):
        for i in range(0, len(output)):
            if (output[i][j]):
                max_neighbour = max(
                    output[i + 1][j] if i + 1 < len(output) else 0, output[i][j + 1] if j + 1 < len(output[0]) else 0, output[i - 1][j] if i - 1 >= 0 else 0, output[i][j - 1] if j - 1 >= 0 else 0)
                if (max_neighbour > 1):
                    output[i][j] = max_neighbour
                else:
                    output[i][j] = 2 ** n_groups
                    n_groups += 1
    print(output)
    return n_groups - 1


def vizinhanca_8(shape1, shape2):
    pass
