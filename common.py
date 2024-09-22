import os


def run_file_processing(func):
    folder = "files"
    keywords = ["abandon", "autonomy", "danger", "fate", "ownership", "workforce", "vulnerability", "wealth", "weather", "spectrum"]

    if not os.path.exists(folder):
        print("Directory does not exist")
        exit()
    
    files = [f"{folder}/{file}" for file in os.listdir(folder)]
    
    result = func(files, keywords)
    for keyword, files in result.items():
        print(f"Keyword '{keyword}' found in files: {', '.join(files)}")