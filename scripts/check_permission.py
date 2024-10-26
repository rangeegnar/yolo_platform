import os

# 假设 source_file_path 和 to_file_path 已经定义
source_file_path = r"D:\python_all\tracer-53e05801b2f2e12436b14246a1d0ebda604cd921\media\19546051318\1 (2).txt"  # 源文件路径
to_file_path = r"C:\Users\24666\Desktop\1\file.txt"  # 目标文件路径

# 确保目标目录存在
target_directory = os.path.dirname(to_file_path)
os.makedirs(target_directory, exist_ok=True)

# 将源文件内容写入到目标路径
try:
    with open(source_file_path, 'rb') as source_file:  # 以二进制模式打开源文件
        with open(to_file_path, 'wb') as target_file:  # 以二进制模式打开目标文件
            target_file.write(source_file.read())  # 读取源文件内容并写入目标文件
    print("文件已成功复制。")
except Exception as e:
    print(f"无法复制文件: {e}")
