import math


# قانون الجداء الداخلي = طويلة الاول المتجه الاول جداء الثاني
def multiply_inner(v1, v2):
    num = len(v1)
    result = 0
    for i in range(num):
        result += v1[i] * v2[i]
    return result


def calculate_length_vector(v):
    result = 0
    for i in range(len(v)):
        result += math.pow(v[i], 2)
    return result


def get_corner_between_tow_vector(v1, v2):
    cos_theta = multiply_inner(v1, v2) / (calculate_length_vector(v1) * calculate_length_vector(v2))
    theta = math.acos(cos_theta)
    theta = 180 * theta / math.pi
    return theta
