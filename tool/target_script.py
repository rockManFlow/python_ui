import cv2
import os
def target_script_fun(video_path,output_dir):
    print(f"=== 接收到的参数 ===")
    print(f"文件路径：{video_path}")
    print(f"文件夹路径：{output_dir}")

    # 此处替换为你的业务逻辑（示例：视频帧提取）
    try:
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
        return True, f"共提取 {frame_count} 帧图片"
    except Exception as e:
        return False,f"业务逻辑执行出错：{str(e)}"

if __name__ == "__main__":
    target_script_fun('','')