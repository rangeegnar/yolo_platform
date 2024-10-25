import torch
import yaml
from ultralytics.nn.tasks import parse_model

def load_yaml(yaml_path: str):
    """加载 YAML 文件并返回内容"""
    try:
        with open(yaml_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"YAML file not found: {yaml_path}")
        raise
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        raise
    except UnicodeDecodeError as e:
        print(f"Encoding error: {e}")
        raise
def debug_parse_model(yaml_path: str, channels: int, verbose: bool = True):
    # 加载模型配置
    model_structure = load_yaml(yaml_path)

    # 调用parse_model进行调试
    try:
        parsed_model = parse_model(model_structure, ch=channels, verbose=verbose)

        if verbose:
            print("Parsed Model Structure:")
            print(parsed_model)
    except Exception as e:
        print(f"Error parsing model: {e}")

if __name__ == "__main__":
    yaml_path = 'ultralytics/cfg/models/v8/yolov8.yaml'  # 替换为你的yaml模型配置文件路径
    channels = 3  # 输入通道数，通常是3（RGB）
    
    debug_parse_model(yaml_path, channels, verbose=True)
