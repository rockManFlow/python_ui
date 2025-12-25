import os
from typing import Union


def convert_size(size_bytes: int) -> str:
    """
    将字节数转换为人性化的单位（B/KB/MB/GB/TB）
    :param size_bytes: 字节数
    :return: 带单位的大小字符串
    """
    if size_bytes == 0:
        return "0 B"
    # 单位换算系数
    size_names = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"


def get_file_size(file_path: str) -> Union[int, None]:
    """
    获取单个文件的大小（字节），处理异常
    :param file_path: 文件路径
    :return: 字节数 / None（失败时）
    """
    try:
        # 跳过符号链接，避免循环/错误
        if os.path.islink(file_path):
            print(f"⚠️  跳过符号链接: {file_path}")
            return 0
        return os.path.getsize(file_path)
    except PermissionError:
        print(f"❌ 权限不足，无法读取: {file_path}")
        return 0
    except FileNotFoundError:
        print(f"❌ 文件不存在: {file_path}")
        return 0
    except Exception as e:
        print(f"❌ 读取失败 {file_path}: {str(e)}")
        return 0


def get_dir_total_size(dir_path: str, show_detail: bool = True,show_size: int = 0) -> int:
    """
    递归计算文件夹总大小（含子文件夹），可选输出每个文件的大小明细
    :param dir_path: 文件夹路径
    :param show_detail: 是否显示每个文件的大小明细
    :return: 总字节数
    """
    total_size = 0
    # 遍历文件夹（递归）
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = get_file_size(file_path)
            if file_size is None:
                continue
            total_size += file_size
            # 输出单个文件明细
            if show_detail and file_size>show_size:
                print(f"📄 {file_path:<60} {convert_size(file_size)}")
    return total_size


def calculate_path_size(target_path: str, show_detail: bool = True,show_size: int = 0) -> None:
    """
    主函数：判断路径类型（文件/文件夹），计算并输出大小
    :param target_path: 目标文件/文件夹路径
    :param show_detail: 是否显示文件夹内文件明细
    """
    # 检查路径是否存在
    if not os.path.exists(target_path):
        print(f"❌ 路径不存在: {target_path}")
        return convert_size(0)

    # 处理单个文件
    if os.path.isfile(target_path):
        file_size = get_file_size(target_path)
        if file_size is not None and file_size>show_size:
            print(f"\n📌 单个文件大小：")
            print(f"文件路径: {target_path}")
            print(f"大小: {convert_size(file_size)}")
            return convert_size(file_size)
        else:
            return convert_size(0)
    # 处理文件夹
    elif os.path.isdir(target_path):
        print(f"\n📌 文件夹 '{target_path}' 及其子文件大小明细：")
        print("-" * 80)
        total_size = get_dir_total_size(target_path, show_detail=show_detail,show_size=show_size)
        print("-" * 80)
        print(f"📊 文件夹总大小: {convert_size(total_size)}")
        return convert_size(total_size)

'''
判断文件或者文件夹下文件大小 OK
查找大文件
'''
if __name__ == "__main__":
    target = 'C:\\Users\\Dell\\Downloads'

    # 执行计算（show_detail=False 可关闭文件明细，只输出总大小） 30m
    calculate_path_size(target, show_detail=True,show_size=31457280)