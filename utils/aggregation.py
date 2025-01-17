import numpy as np

from VectorHandle.vector import Vector

def mean_method(vectors: list[Vector]) -> Vector:
    """
    Computes the mean vector from a list of vectors.

    Args:
        vectors (list[Vector]): A list of Vector objects.

    Returns:
        np.ndarray: The mean vector calculated from the input vectors.
    """
    return Vector(np.mean([vector.value for vector in vectors], axis=0))

def max_pool_method(vectors: list[Vector]) -> Vector:
    """
    Computes the maximum vector from a list of vectors using max pooling.

    Args:
        vectors (List[Vector]): A list of Vector objects.

    Returns:
        Vector: The maximum vector calculated from the input vectors.

    Raises:
        ValueError: If the input list is empty.
    """
    vector_array = np.array([vector.value for vector in vectors])
    max_pooled = np.max(vector_array, axis=0)

    return Vector(max_pooled)

def min_pool_method(vectors: list[Vector]) -> Vector:
    """
    Computes the minimal vector from a list of vectors using min pooling.

    Args:
        vectors (List[Vector]): A list of Vector objects.

    Returns:
        Vector: The minimum vector calculated from the input vectors.
    """
    vector_array = np.array([vector.value for vector in vectors])
    min_pooled = np.min(vector_array, axis=0)

    return Vector(min_pooled)

def median_pooling(vectors: list[Vector]) -> Vector:
    """
    Computes the median vector from a list of vectors.

    Args:
        vectors (List[Vector]): A list of Vector objects.

    Returns:
        Vector: The median vector calculated from the input vectors.
    """
    vector_array = np.array([vector.value for vector in vectors])
    median_vector = np.median(vector_array, axis=0)

    return Vector(median_vector)

def sum_method(vectors: list[Vector]) -> Vector:
    """
    Computes the sum of a list of vectors.

    Args:
        vectors (list[Vector]): A list of Vector objects to be summed.

    Returns:
        Vector: The summed vector calculated from the input vectors.
    """
    vector_array = np.array([v.value for v in vectors])
    summed_vector = np.sum(vector_array, axis=0)
    return Vector(summed_vector)