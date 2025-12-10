def target_2(selected_file,selected_folder):
    print(f"=== 接收到的参数 ===\n")
    print(f"文件路径：{selected_file}\n")
    print(f"文件夹路径：{selected_folder}\n")

    print(f"执行完成\n")
    # return False, "执行失败！"
    return True,"执行完成！"

if __name__ == "__main__":
    target_2('','')