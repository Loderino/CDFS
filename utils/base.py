import os
import base64
import mimetypes

def get_file_as_base64_url(file_path: str) -> str|None:
    """
    Преобразует файл в Data URL с кодировкой base64.

    Args:
        file_path (str): Путь к файлу

    Returns:
        str: Data URL в формате "data:mimetype;base64,{encoded_data}"
        или None, если файл не найден
    """
    try:
        if not os.path.isfile(file_path):
            return None
        
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        with open(file_path, 'rb') as file:
            file_content = file.read()

        encoded_content = base64.b64encode(file_content).decode('utf-8')

        data_url = f"data:{mime_type};base64,{encoded_content}"

        return data_url

    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {str(e)}")
        return None