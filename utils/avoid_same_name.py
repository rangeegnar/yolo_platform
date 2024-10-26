import os

def get_unique_file_name(directory, file_name):
    # 分离文件名和扩展名
    file_base, file_extension = os.path.splitext(file_name)

    # 初始文件名
    new_file_name = file_name
    new_file_path = os.path.join(directory, new_file_name)

    # 检查文件名是否已经存在，如果存在则递增数字
    counter = 1
    while os.path.exists(new_file_path):
        new_file_name = f"{file_base}_{counter}{file_extension}"
        new_file_path = os.path.join(directory, new_file_name)
        counter += 1

    return new_file_name, new_file_path


def detect_get_unique_file_name(directory, file_name, file_extension):
    """需要拓展名"""
    # 初始文件名
    new_file_name = f"{file_name}_try{file_extension}"
    new_file_path = os.path.join(directory, new_file_name)

    # 检查文件名是否已经存在，如果存在则递增数字
    counter = 1
    while os.path.exists(new_file_path):
        new_file_name = f"{file_name}_try_{counter}{file_extension}"
        new_file_path = os.path.join(directory, new_file_name)
        counter += 1

    return new_file_name, new_file_path
