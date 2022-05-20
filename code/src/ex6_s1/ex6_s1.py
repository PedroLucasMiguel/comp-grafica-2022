def __is_inside(point, corner):
    x, y = point
    '''
        corner[0] => top-left
        corner[1] => bottom-right
    '''
    py1, px1 = corner[0]
    py2, px2 = corner[1]
    return x >= px1 and x < px2 and y >= py1 and y < py2


def __check_neighbours(points, shape):
    for y, x in points:
        if shape["grid"][y - shape["offsetY"]][x - shape["offsetX"]]:
            return True
    return False


def __check_neighbours_4(point, shape, orientation):
    '''
        orientation isn't used in this case, but the parameter
        is kept to keep symmetry between the two functions
    '''
    return __check_neighbours([point], shape)


def __check_neighbours_8(point, shape, orientation):
    y, x = point
    points = []
    for i in range(-1, 2):
        '''
            orientation 0 os horizontal and 1 is vertical
        '''
        if orientation:
            points.append((y, x + i))
        else:
            points.append((y + i, x))
    return __check_neighbours(points, shape)


def __check_connectivity(shape1, shape2, neighbourhood_fn):
    s2_corners = [
        (shape2["offsetX"], shape2["offsetY"]),
        (shape2["offsetX"] + shape2["sizeX"],
         shape2["offsetY"] + shape2["sizeY"])
    ]
    for i in range(len(shape1["grid"][0])):
        if shape1["grid"][0][i] and __is_inside((-1, i), s2_corners) and neighbourhood_fn((-1, i), shape2, 0):
            return True
    for i in range(len(shape1["grid"])):
        if shape1["grid"][i][len(shape1["grid"][0]) - 1] and __is_inside((i, len(shape1["grid"][0])), s2_corners) and neighbourhood_fn((i, len(shape1["grid"][0])), shape2, 1):
            return True
    for i in range(len(shape1["grid"][0])):
        if shape1["grid"][len(shape1["grid"]) - 1][i] and __is_inside((len(shape1["grid"]), i), s2_corners) and neighbourhood_fn((len(shape1["grid"]), i), shape2, 0):
            return True
    for i in range(len(shape1["grid"])):
        if shape1["grid"][i][0] and __is_inside((i, -1), s2_corners) and neighbourhood_fn((i, -1), shape2, 1):
            return True
    return False


def check_connectivity_4(shape1, shape2):
    return __check_connectivity(shape1, shape2, __check_neighbours_4)


def check_connectivity_8(shape1, shape2):
    return __check_connectivity(shape1, shape2, __check_neighbours_8)


'''
    Code used for testing during development
'''
if __name__ == "__main__":
    s1, s2, s3, s4 = ({
        "grid": [
            [0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0],
            [1, 0, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0]
        ],
        "sizeX": 6,
        "sizeY": 5,
        "offsetX": 0,
        "offsetY": 0
    }, {
        "grid": [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [1, 1, 0, 1],
            [0, 0, 1, 0],
            [1, 0, 0, 0]
        ],
        "sizeX": 4,
        "sizeY": 5,
        "offsetX": 6,
        "offsetY": 0
    }, {
        "grid": [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [1, 0, 0, 0]
        ],
        "sizeX": 4,
        "sizeY": 5,
        "offsetX": 6,
        "offsetY": 0
    }, {
        "grid": [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [1, 1, 0, 1],
            [0, 0, 1, 0],
            [1, 0, 0, 0]
        ],
        "sizeX": 4,
        "sizeY": 5,
        "offsetX": 7,
        "offsetY": 0
    })
    print(check_connectivity_4(s1, s2))  # expect True
    #print(check_connectivity_4(s1, s3))  # expect False
    #print(check_connectivity_4(s1, s4))  # expect False
    print(check_connectivity_8(s1, s2))  # expect True
    #print(check_connectivity_8(s1, s3))  # expect True
    #print(check_connectivity_8(s1, s4))  # expect False
