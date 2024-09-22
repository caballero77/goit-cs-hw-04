import threading
import time
from collections import defaultdict

from common import run_file_processing


def search_in_files(files, keywords, result):
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        result[keyword].append(file)
        except Exception as e:
            print(f"Error reading {file}: {e}")

def threaded_search(files, keywords, num_threads=8):
    result = defaultdict(list)
    threads = []
    chunk_size = len(files) // num_threads
    start_time = time.time()

    for i in range(num_threads):
        start = i * chunk_size
        end = None if i + 1 == num_threads else (i + 1) * chunk_size
        thread = threading.Thread(target=search_in_files, args=(files[start:end], keywords, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Threaded search took: {end_time - start_time:.4f} seconds")
    return result

if __name__ == "__main__":
    run_file_processing(threaded_search)