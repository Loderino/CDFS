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
