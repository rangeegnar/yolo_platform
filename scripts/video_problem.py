import subprocess
import os

def reencode_video(input_file, output_file):
    # 确保输入文件存在
    if not os.path.isfile(input_file):
        print(f"输入文件不存在: {input_file}")
        return

    # FFmpeg 命令
    command = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'libx264',  # 视频编码为 H.264
        '-c:a', 'aac',      # 音频编码
        '-strict', 'experimental',  # 使用实验性功能
        output_file
    ]

    # 调用 FFmpeg
    try:
        subprocess.run(command, check=True)
        print(f"视频已成功重新编码: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"重新编码失败: {e}")

if __name__ == "__main__":
    # 输入文件路径
    input_path = r'D:/python_all/tracer-53e05801b2f2e12436b14246a1d0ebda604cd921/media/19546051318/range_index_try.mp4'
    # 输出文件路径
    output_path = r'D:/python_all/tracer-53e05801b2f2e12436b14246a1d0ebda604cd921/media/19546051318/1.mp4'

    # 调用重新编码函数
    reencode_video(input_path, output_path)

    # 删除输入文件
    if os.path.isfile(input_path):
        os.remove(input_path)
        print(f"已删除输入文件: {input_path}")

    # 将输出文件重命名为输入文件名
    if os.path.isfile(output_path):
        new_name = input_path.split('/')[-1]  # 获取输入文件名
        new_output_path = os.path.join(os.path.dirname(input_path), new_name)
        os.rename(output_path, new_output_path)
        print(f"输出文件已重命名为: {new_output_path}")