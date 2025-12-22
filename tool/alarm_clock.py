import datetime
import threading
import time
import sys


class AlarmClock:
    def __init__(self, target_time_str):
        # 解析目标时间字符串（格式：YYYY.MM.DD HH:MM）
        self.target_time = datetime.datetime.strptime(target_time_str, "%Y-%m-%d %H:%M")
        self.is_running = False  # 控制异步线程运行状态
        self.alarm_thread = None  # 闹钟线程对象

    def _alarm_task(self):
        """异步线程执行的闹钟任务"""
        # 等待直到到达目标时间
        while datetime.datetime.now() < self.target_time:
            if not self.is_running:  # 检测终止信号
                return
            time.sleep(1)  # 每秒检查一次时间

        # 到达目标时间后，循环打印信息直到主线程终止
        while self.is_running:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"【闹钟触发】当前时间：{current_time} | 已到达指定时间！", flush=True)
            time.sleep(1)  # 每秒打印一次

    def start(self):
        """启动闹钟"""
        self.is_running = True
        self.alarm_thread = threading.Thread(target=self._alarm_task, daemon=True)
        self.alarm_thread.start()
        print(f"闹钟已启动，将在 {self.target_time.strftime('%Y-%m-%d %H:%M')} 触发！")
        print("输入 'quit' 或 'exit' 并回车可终止闹钟\n")

    def stop(self):
        """终止闹钟"""
        self.is_running = False
        if self.alarm_thread and self.alarm_thread.is_alive():
            self.alarm_thread.join(timeout=2)  # 等待线程退出
        print("\n闹钟已终止！")


def main(target_time_input):
    # 获取用户输入的目标时间
    # target_time_input = input("请输入闹钟时间（格式：YYYY-MM-DD HH:MM，例如：2025-12-20 01:10）：")
    try:
        # 验证时间格式
        datetime.datetime.strptime(target_time_input, "%Y-%m-%d %H:%M")
    except ValueError:
        print("时间格式错误！请严格按照 YYYY-MM-DD HH:MM 格式输入\n")
        return
    # 初始化并启动闹钟
    alarm = AlarmClock(target_time_input)
    alarm.start()

    # 主线程监听终止指令
    while True:
        user_input = input().strip().lower()
        if user_input in ["quit", "exit"]:
            alarm.stop()
            sys.exit(0)
        else:
            print("无效指令！输入 'quit' 或 'exit' 可终止闹钟")

'''
验证闹钟OK
'''
if __name__ == "__main__":
    try:
        main('2025-12-19 18:25')
    except KeyboardInterrupt:
        # 处理Ctrl+C终止
        print("\n\n检测到强制终止信号，闹钟已退出！")
        sys.exit(0)