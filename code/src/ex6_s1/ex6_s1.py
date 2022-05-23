'''
    This module provides methods to check if shape1 and shape2 have connecting groups of pixels.
    It is assumed that both shapes are squares and they can be defined anywhere in a 2D space.
    For optimization purposes, it is also assumed the shapes are not overlapping each other.
'''


def __is_inside(point, corner):
    '''
        Check if point is inside the given shape.
        Since it was previously stablished that the shape is a square,
        it is only needed to be checked if the point is between the
        top-left and bottom-right corner in both the x and y axis.
    '''
    x, y = point
    '''
        corner[0] => top-left
        corner[1] => bottom-right
    '''
    py1, px1 = corner[0]
    py2, px2 = corner[1]
    return x >= px1 and x < px2 and y >= py1 and y < py2


def __check_neighbours(points, shape):
    '''
        Check for possible neighbours in the shape following a list of points.
        At this points it is expeted that the points have been validated to be inside the shape.
    '''
    for y, x in points:
        if shape["grid"][y - shape["offsetY"]][x - shape["offsetX"]]:
            return True
    return False


def __check_neighbours_4(point, shape, orientation):
    '''
        Create list of possible neighbours to be checked.
        Here it is applied an optmization strategy of only checking
        for possible coordinates that can be outside the shape of reference.
        In 4-neighbourhood there can only be 1 such possibility.

        Orientation isn't used in this case, but the parameter
        is kept to keep symmetry between the two functions.

        TODO: move __is_inside in here to keep symetry.
    '''
    return __check_neighbours([point], shape)


def __check_neighbours_8(point, shape, orientation):
    '''
        Create a list of possible neighbours to be checked.
        Here it is applied an optimization strategy of only checking
        for possible coordinates that can be outside the shape of reference.
        In 8-neighbourhood there are 3 possibilities.

        TODO: move __is_inside in here to be called for every point created.
    '''
    y, x = point
    points = []
    for i in range(-1, 2):
        '''
            Orientation 0 os horizontal and 1 is vertical.
        '''
        if orientation:
            points.append((y, x + i))
        else:
            points.append((y + i, x))
    return __check_neighbours(points, shape)


def __check_connectivity(shape1, shape2, neighbourhood_fn):
    '''
        Since the shapes are assumed to be squares, it is possible to check for
        connectivity by only checking the borders of the shapes.
        Additionally, since it is only checked for 4 and 8-neighbourhood,
        then it is unnecessary to check the borders of both shapes.
        As such, the shape1 is taken as the shape of reference.
        To further optimize this check of connectivity, a strategy of return-fast is utilized.
        Which means the code will stop as soon as the first confirmed neighbour is found.
    '''
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
    '''
        Check connectivity with 4-neighbourhood
    '''
    return __check_connectivity(shape1, shape2, __check_neighbours_4)


def check_connectivity_8(shape1, shape2):
    '''
        Check connectivity with 8-neighbourhood
    '''
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
    print(check_connectivity_4(s1, s3))  # expect False
    print(check_connectivity_4(s1, s4))  # expect False
    print(check_connectivity_8(s1, s2))  # expect True
    print(check_connectivity_8(s1, s3))  # expect True
    print(check_connectivity_8(s1, s4))  # expect False
