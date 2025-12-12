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

def find_duplicates(folder):
    md5_dict = {}
    phash_dict = {}

    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(root, file)
                try:
                    # 第一层：MD5快速比对
                    file_md5 = get_file_md5(path)
                    if file_md5 in md5_dict:
                        print(f'完全重复文件: {path} <=> {md5_dict[file_md5]}')
                        del_file(path)
                        continue

                    # 第二层：感知哈希比对
                    img_phash = get_image_phash(path)
                    for existing_phash in phash_dict:
                        if img_phash - existing_phash < 5:  # 汉明距离阈值
                            print(f'相似图片: {path} ≈ {phash_dict[existing_phash]}')
                            del_file(path)
                            break
                    else:
                        phash_dict[img_phash] = path

                    md5_dict[file_md5] = path
                except Exception as e:
                    print(f'处理失败 {path}: {str(e)}')

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
        find_duplicates(temp)  # 修改为你的图片目录
