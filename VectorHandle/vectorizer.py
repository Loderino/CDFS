import fasttext

from constants import RU_VEC_MODEL_PATH
from VectorHandle import NAME_TO_FUNC
from VectorHandle.vector import Vector

class Vectorizer:
    """
    Singleton class for vectorizing words. 
    """
    _instance = None
    model = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Vectorizer, cls).__new__(cls)
            cls.model = fasttext.load_model(RU_VEC_MODEL_PATH)
        return cls._instance

    def get_word_vector(self, word: str) -> Vector:
        """
        Get vector for word.

        Args:
            word (str): word to vectorize.

        Returns:
           Vector: the vector of word.
        """
        return Vector(self.model.get_word_vector(word))
    
    def get_set_vector(self, words: list[str], aggregation_method: str = "mean") -> Vector:
        """
        Get vector for set of words.

        Args:
            words (list[str]): list of words to vectorize.

        Returns:
            Vector: the vector of words.
        """
        aggregation_method = NAME_TO_FUNC[aggregation_method]
        
        return aggregation_method([self.get_word_vector(word) for word in words])