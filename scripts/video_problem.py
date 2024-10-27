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
    input_path = r'D:/python_all/tracer-53e05801b2f2e12436b14246a1d0ebda604cd921/media/19546051318/a6c16d9868dcefbef43f1c3c7ed32430_try_try.mp4'
    # 输出文件路径
    output_path = r'D:/python_all/tracer-53e05801b2f2e12436b14246a1d0ebda604cd921/media/19546051318/a6c16d9868dcefbef43f1c3c7ed32430.mp4'


    old_name = input_path.split('/')[-1]
    new_name = output_path.split('/')[-1]

    reencode_video(input_path, output_path)
    os.remove(input_path)

    output_path = output_path.replace(new_name, old_name)