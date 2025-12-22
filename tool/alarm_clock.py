import datetime
import time
import sys

def _alarm_task(target_time_str):
    target_time = datetime.datetime.strptime(target_time_str, "%Y-%m-%d %H:%M")
    """异步线程执行的闹钟任务"""
    # 等待直到到达目标时间
    while datetime.datetime.now() <target_time:
        time.sleep(1)  # 每秒检查一次时间
    # 到达目标时间后
    return True

def run_clock(target_time_input):
    # 获取用户输入的目标时间 格式：YYYY-MM-DD HH:MM，例如：2025-12-20 01:10
    try:
        # 验证时间格式
        datetime.datetime.strptime(target_time_input, "%Y-%m-%d %H:%M")
    except ValueError:
        print("时间格式错误！请严格按照 YYYY-MM-DD HH:MM 格式输入\n")
        return False
    # 初始化并启动闹钟
    return _alarm_task(target_time_input)
'''
验证闹钟OK
'''
if __name__ == "__main__":
    try:
        run_clock('2025-12-19 18:25')
    except KeyboardInterrupt:
        # 处理Ctrl+C终止
        print("\n\n检测到强制终止信号，闹钟已退出！")
        sys.exit(0)