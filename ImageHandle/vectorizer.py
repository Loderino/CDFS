import fasttext

from constants import RU_VEC_MODEL_PATH

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

    def get_vector(self, word: str) -> list:
        """
        Get vector for word.

        Args:
            word (str): word to vectorize.

        Returns:
           list: list of size 300.
        """
        return self.model.get_word_vector(word)