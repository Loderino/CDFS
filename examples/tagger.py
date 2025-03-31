import time
from ImageHandle.tagger import Tagger

tagger = Tagger()
times = []
for i in range (1, 101):
    try:
        start = time.perf_counter()
        tagger.generate_desc(f"test_folder/benchmark/{i}.jpg")
        times.append(time.perf_counter()-start)
    except:
        pass
print(sum(times)/len(times))