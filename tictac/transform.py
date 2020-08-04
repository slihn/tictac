import numpy as np


class Transform:
    def __init__(self, *operations):  # pass a list as if tuple arguments
        self.operations = operations  # a list of sequential transforms operations

    def transform(self, target):
        for op in self.operations:
            target = op.transform(target)
        return target

    def reverse(self, target):
        for op in reverse(self.operations):
            target = op.reverse(target)
        return target


class Identity:
    @staticmethod
    def transform(matrix2d):
        return matrix2d

    @staticmethod
    def reverse(matrix2d):
        return matrix2d


class Rotate90:
    def __init__(self, number_of_rotations):
        self.number_of_rotations = number_of_rotations
        self.op = np.rot90

    def transform(self, matrix2d):
        return self.op(matrix2d, self.number_of_rotations)

    def reverse(self, transformed_matrix2d):
        return self.op(transformed_matrix2d, -self.number_of_rotations)


class Flip:
    def __init__(self, op):
        self.op = op

    def transform(self, matrix2d):
        return self.op(matrix2d)

    def reverse(self, transformed_matrix2d):
        return self.transform(transformed_matrix2d)


def reverse(items):
    return items[::-1]


# all possible transformations for the 2d board
TRANSFORMATIONS = [Identity(),
                   Rotate90(1), Rotate90(2), Rotate90(3),
                   Flip(np.flipud),  # horizontal axis
                   Flip(np.fliplr),  # vertical axis
                   Transform(Rotate90(1), Flip(np.flipud)),  # -45 degree axis
                   Transform(Rotate90(1), Flip(np.fliplr))  # +45 degree axis
                   ]


def get_symmetrical_board_orientations(matrix2d):
    # returns list of tuple (transformed matrix2d, transform)
    return [(t.transform(matrix2d), t) for t in TRANSFORMATIONS]
