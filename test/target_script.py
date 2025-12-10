import sys

def main():
    # 获取传递的参数
    selected_file = sys.argv[1] if len(sys.argv) > 1 else ""
    selected_folder = sys.argv[2] if len(sys.argv) > 2 else ""

    print(f"=== 接收到的参数 ===")
    print(f"文件路径：{selected_file}")
    print(f"文件夹路径：{selected_folder}")

    # 此处替换为你的业务逻辑（示例：视频帧提取）
    try:
        import cv2
        import os
        def video_to_frames(video_path, output_dir):
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            cap = cv2.VideoCapture(video_path)
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_path = os.path.join(output_dir, f"frame_{frame_count:06d}.png")
                cv2.imwrite(frame_path, frame)
                frame_count += 1
            cap.release()
            return f"共提取 {frame_count} 帧图片"

        result = video_to_frames(selected_file, selected_folder)
        print(result)
    except Exception as e:
        print(f"业务逻辑执行出错：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()