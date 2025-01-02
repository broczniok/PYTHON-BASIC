from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import time
import os
import logging

today_date = "10-10-10"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def list_directories(base_path="files"):
    """
    Returns a list of directory names inside the specified `base_path`.

    Parameters:
    - base_path (str): The path to search for directories (default is `/files`).

    Returns:
    - list: A list of directory names within `base_path`.
    """
    try:
        if not os.path.exists(base_path):
            print(f"The path {base_path} does not exist.")
            return []

        directories = [name for name in os.listdir(base_path)
                       if os.path.isdir(os.path.join(base_path, name))]
        return directories
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def create_directories(base_path="files", num_dirs=100):
    """
    Creates `num_dirs` directories inside the specified `base_path`.

    Parameters:
    - base_path (str): The path where directories will be created.
    - num_dirs (int): The number of directories to create (default is 100).
    """
    try:
        os.makedirs(base_path, exist_ok=True)

        for i in range(1, num_dirs + 1):
            dir_path = os.path.join(base_path, f"dir_{i}")
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created: {dir_path}")

        print(f"Successfully created {num_dirs} directories in {base_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def multithread_schema_validation():
    print(today_date)
    adls_file_path = f"adls_file_path"
    error_file_path = f"adls_error_file_path"
    print(adls_file_path)
    print(error_file_path)
    file_paths = list_directories() # it should be list
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(schema_validation, file_path) for file_path in file_paths]
        print("Worker get job")

        for future in futures:
            try:
                future.result()
                logging.info("get future.result()")
            except Exception as e:
                logging.error(f"Error processing file {futures[future]}: {e}")
    end_time = time.time()
    logging.info(f"Total process time: {end_time - start_time:.2f} seconds")



def schema_validation(file):
    worker_pid = os.getpid()
    logging.info(f"Worker PID {worker_pid} started processing: {file}")
    time.sleep(1)
    logging.info(f"Worker PID {worker_pid} finished processing: {file}")

if __name__ == '__main__':
    multithread_schema_validation()