import os
import magic

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
def is_image(file_path: str) -> bool:
    """
    Checks if a given file path is an image.

    This function checks first if given path is a file and not a directory,
    then it checks mime type of the file. If mime type is not recognized,
    it looks for the common image file extensions.

    Args:
        file_path (str): A path to a file.

    Returns:
        bool: True if the file is an image, False otherwise.
    """
    try:
        mime = magic.Magic(mime=True)
        if not os.path.isdir(file_path):
            file_mime = mime.from_file(file_path)
            return file_mime.startswith('image/')
        return False
    except FileNotFoundError:
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension in IMAGE_EXTENSIONS
    
    except Exception as e:
        print(type(e))
        print(e)
        return False