import multiprocessing
from collections import defaultdict
import time

from common import run_file_processing


def search_in_files_multiprocessing(files, keywords, queue):
    result = defaultdict(list)
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        result[keyword].append(file)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    queue.put(result)

def multiprocessing_search(files, keywords, num_processes=8):
    result = defaultdict(list)
    processes = []
    queue = multiprocessing.Queue()
    chunk_size = len(files) // num_processes
    start_time = time.time()

    for i in range(num_processes):
        start = i * chunk_size
        end = None if i + 1 == num_processes else (i + 1) * chunk_size
        process = multiprocessing.Process(target=search_in_files_multiprocessing, args=(files[start:end], keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        process_result = queue.get()
        for keyword, files in process_result.items():
            result[keyword].extend(files)

    end_time = time.time()
    print(f"Multiprocessing search took: {end_time - start_time:.4f} seconds")
    return result

if __name__ == "__main__":
    run_file_processing(multiprocessing_search)
