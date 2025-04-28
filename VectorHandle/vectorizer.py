import fasttext

from constants import RU_VEC_MODEL_PATH
from VectorHandle import NAME_TO_FUNC
from VectorHandle.vector import Vector
from utils.word_weights import get_tag_weight

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
    
    def get_set_vector(self, words: list[str], aggregation_method: str = "mean", weigh = True) -> Vector:
        """
        Get vector for set of words.

        Args:
            words (list[str]): list of words to vectorize.

        Returns:
            Vector: the vector of words.
        """
        aggregation_method = NAME_TO_FUNC[aggregation_method]
        
        vectors = []
        tags_weights = []
        for tag in words:
            if " " in tag:
                weights = [get_tag_weight(word) for word in tag.split(" ")]
                tag_vector = aggregation_method([self.get_word_vector(word) for word in tag.split(" ")], weights=weights if weigh else None)
                vectors.append(tag_vector)
            else:
                vectors.append(self.get_word_vector(tag))
            tags_weights.append(get_tag_weight(tag))
        return aggregation_method(vectors, weights=tags_weights if weigh else None)