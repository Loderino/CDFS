from tqdm import tqdm
from threading import Thread
from frontend import launch_frontend
from handlers import fw, handle_new_file, stop

try:
    api_thread = Thread(name="API", target=launch_frontend)
    api_thread.start()

    for ind, file in tqdm(enumerate(fw.get_current_files()), ncols=80, ascii=True, desc="Индексация имеющихся файлов"):
        handle_new_file(file)
except KeyboardInterrupt:
    api_thread.join()
    stop()