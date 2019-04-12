import math


def get_vector(vector):

    magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    if magnitude is 0:
        return 0, 0
    else:
        return vector[0] / magnitude, vector[1] / magnitude


def get_average_vector(vector_A, vector_B):

    return get_vector(((vector_A[0] + vector_B[0]) / 2, (vector_A[1] + vector_B[1]) / 2))


def get_distance(object_A, object_B):

    return math.sqrt(math.pow((object_B.position[0] - object_A.position[0]), 2) + math.pow((object_B.position[1] - object_A.position[1]), 2))


def get_midpoint(object_A, object_B):

    return ((object_A.position[0] + object_B.position[0]) / 2), ((object_A.position[1] + object_B.position[1]) / 2)
