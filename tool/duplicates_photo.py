# 重复图片校验
import os
import hashlib
from PIL import Image
import imagehash

def get_file_md5(file_path):
    """计算文件MD5哈希值"""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def get_image_phash(file_path):
    """计算感知哈希值"""
    with Image.open(file_path) as img:
        return imagehash.phash(img)

def del_file(path):
    try:
        os.remove(path)
        print(f"文件 {path} 已删除")
    except Exception as e:
        print(f"删除文件 {path} 时出错: {e}")

'去除指定文件夹下重复或相似的文件并删除-验证OK的'
if __name__ == '__main__':
    pre_url='E:/iPhone620231212-backup/2023__0'
    #从0到4
    for i in range(12):
        temp=pre_url+str(i+1)
        print(f"开始执行路径 {temp} 下图片判断")
        # find_duplicates(temp,0,None,None)  # 修改为你的图片目录
