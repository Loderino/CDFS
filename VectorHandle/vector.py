from sklearn.preprocessing import normalize

class Vector:
    """
    Wrapper class for the 300-dimensional vector returned by the word2vec model.
    Contains useful methods for vector manipulation.
    """
    size = 300
    def __init__(self, vector: list) -> None:
        if len(vector) != Vector.size:
            raise ValueError(f"Vector must be of length {Vector.size}, got {len(vector)}")
        self.value = vector

    def normalize(self) -> None:
        """
        Normalizes the vector to have unit length.

        Modifies the vector in place by changing its values to be a unit vector,
        preserving its direction but with a magnitude of 1.
        """
        self.value = normalize(self.value.reshape(1, -1))[0]

    def __iter__(self):
        """Iterates over the vector's elements."""
        return self.value
