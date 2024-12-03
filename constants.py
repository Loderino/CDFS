import json

with open("configs.json", "r", encoding="utf-8") as f:
    CONFIGS = json.load(f)

RU_VEC_MODEL_PATH = CONFIGS["ru_vec_model_path"]
INDEX_PATH = CONFIGS["index_path"]
DB_PATH = CONFIGS["db_path"]
TRACKED_DIRECTORY = CONFIGS["tracked_directory"]
IMAGE_TAGGER_MODEL_PATH = CONFIGS["image_tagger_model_path"]
IMAGE_TAGGER_TOKENIZER_PATH = CONFIGS["image_tagger_tokenizer_path"]