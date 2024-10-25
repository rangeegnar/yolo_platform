import os
from PIL import Image

def convert_to_jpg(input_file, output_file):
    with Image.open(input_file) as img:
        rgb_img = img.convert('RGB')
        rgb_img.save(output_file, 'JPEG')

def convert_files_in_directory(directory):
    for filename in os.listdir(directory):
        input_path = os.path.join(directory, filename)
        
        # 检查文件是否为图像文件
        if os.path.isfile(input_path):
            try:
                # 生成输出文件名
                output_file = os.path.splitext(input_path)[0] + '.jpg'
                convert_to_jpg(input_path, output_file)
                print(f'Converted {input_path} to {output_file}')
                
                # 删除原文件
                os.remove(input_path)
                print(f'Deleted original file: {input_path}')
            except Exception as e:
                print(f'Failed to convert {input_path}: {e}')

if __name__ == '__main__':
    directory = 'dataset/VOCdevkit/JPEGImages'  
    convert_files_in_directory(directory)
