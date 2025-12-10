import sys
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from target_2 import target_2


# ------------- 可选：多线程执行脚本（避免界面卡死） -------------
class ScriptRunnerThread(QThread):
    """子线程执行脚本，避免主线程阻塞"""
    finished_signal = pyqtSignal(bool, str)  # 执行结果信号：(是否成功, 输出信息)

    def __init__(self, script_path, file_path, folder_path):
        super().__init__()
        self.script_path = script_path
        self.file_path = file_path
        self.folder_path = folder_path

    def run(self):
        try:
            # 构造执行命令
            cmd = [
                sys.executable,
                self.script_path,
                self.file_path,
                self.folder_path
            ]
            # 执行脚本并捕获输出
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                timeout=300  # 超时时间（秒），按需调整
            )
            if result.returncode == 0:
                self.finished_signal.emit(True, f"执行成功！\n{result.stdout}")
            else:
                self.finished_signal.emit(False, f"执行失败！\n错误信息：{result.stderr}")
        except subprocess.TimeoutExpired:
            self.finished_signal.emit(False, "脚本执行超时！")
        except Exception as e:
            self.finished_signal.emit(False, f"执行异常：{str(e)}")


# ------------- 主窗口类 -------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化变量
        self.selected_file = ""
        self.selected_folder = ""
        self.script_thread = None  # 脚本执行线程

        # 窗口基础设置
        self.setWindowTitle("PyQt5 文件选择执行工具")
        self.setGeometry(200, 200, 800, 600)  # 位置(x,y) + 大小(宽,高)
        self.setMinimumSize(600, 300)  # 最小窗口尺寸

        # 初始化界面
        self.init_ui()

    def init_ui(self):
        """构建界面布局"""
        # 中心部件（QMainWindow 必须设置中心部件）
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 垂直布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 50, 50, 50)  # 内边距（左,上,右,下）

        # 1. 选择文件区域
        file_btn = QPushButton("选择文件", self)
        file_btn.setFont(QFont("Arial", 12))
        file_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        file_btn.clicked.connect(self.select_file)
        main_layout.addWidget(file_btn, alignment=Qt.AlignCenter)

        self.file_label = QLabel("已选文件：无", self)
        self.file_label.setFont(QFont("Arial", 10))
        self.file_label.setWordWrap(True)  # 自动换行
        main_layout.addWidget(self.file_label, alignment=Qt.AlignCenter)

        # 分隔线
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setStyleSheet("background-color: #E0E0E0;")
        main_layout.addWidget(line1)

        # 2. 选择文件夹区域
        folder_btn = QPushButton("选择文件夹", self)
        folder_btn.setFont(QFont("Arial", 12))
        folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        folder_btn.clicked.connect(self.select_folder)
        main_layout.addWidget(folder_btn, alignment=Qt.AlignCenter)

        self.folder_label = QLabel("已选文件夹：无", self)
        self.folder_label.setFont(QFont("Arial", 10))
        self.folder_label.setWordWrap(True)
        main_layout.addWidget(self.folder_label, alignment=Qt.AlignCenter)

        # 分隔线
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("background-color: #E0E0E0;")
        main_layout.addWidget(line2)

        # 3. 执行按钮
        run_btn = QPushButton("确定执行脚本", self)
        run_btn.setFont(QFont("Arial", 14, QFont.Bold))
        run_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        run_btn.clicked.connect(self.run_script)
        main_layout.addWidget(run_btn, alignment=Qt.AlignCenter)
        self.run_btn = run_btn  # 保存引用，用于控制禁用/启用

    def select_file(self):
        """弹出文件选择对话框"""
        # 自定义文件类型过滤：(显示名称, 后缀)，可添加多个
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择文件",
            "",  # 默认打开路径（空为当前目录）
            "所有文件 (*.*);;Python文件 (*.py);;视频文件 (*.mp4 *.avi *.mov)"
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.setFixedWidth(600)
            self.file_label.setFixedHeight(30)
            self.file_label.setText(f"已选文件：{file_path}")

    def select_folder(self):
        """弹出文件夹选择对话框"""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",
            ""
        )
        if folder_path:
            self.selected_folder = folder_path
            self.folder_label.setFixedWidth(600)
            self.folder_label.setFixedHeight(30)
            self.folder_label.setText(f"已选文件夹：{folder_path}")

    def get_resource_path(self,relative_path):
        """
        获取资源文件的绝对路径，兼容：
        1. 开发阶段：基于 main.py 所在目录
        2. 打包后：基于 exe 解压后的临时目录/文件夹目录
        """
        if hasattr(sys, '_MEIPASS'):
            # 打包后（-F/-D 模式），_MEIPASS 是临时/固定解压目录
            base_path = sys._MEIPASS
        else:
            # 开发阶段，取 main.py 所在目录的绝对路径
            base_path = os.path.abspath(os.path.dirname(__file__))
        # 拼接绝对路径
        return os.path.join(base_path, relative_path)

    def run_script(self):
        """执行指定Python脚本"""
        # 校验选择
        if not self.selected_file or not self.selected_folder:
            QMessageBox.warning(self, "提示", "请同时选择文件和文件夹！", QMessageBox.Ok)
            return

        # 禁用执行按钮，避免重复点击
        self.run_btn.setDisabled(True)

        try:
            result,message=target_2(self.selected_file, self.selected_folder)
            # 显示结果弹窗
            if result:
                # 页面标题：执行结果  message：目标程序print所有打印的信息
                QMessageBox.information(self, "执行结果", message, QMessageBox.Ok)
            else:
                QMessageBox.critical(self, "执行结果", message, QMessageBox.Ok)
        except ImportError:
            QMessageBox.critical(self, "错误", "找不到target_script.py模块！", QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"执行异常：{str(e)}", QMessageBox.Ok)
        finally:
            # 启用按钮
            self.run_btn.setDisabled(False)

        # 指定要调用的目标脚本路径（替换为你的脚本路径）
        # target_script = self.get_resource_path("target_2.py")

        # 创建并启动子线程
        # self.script_thread = ScriptRunnerThread(target_script, self.selected_file, self.selected_folder)
        # self.script_thread.finished_signal.connect(self.on_script_finished)
        # self.script_thread.start()
# ------------- 程序入口 -------------
if __name__ == "__main__":
    # 创建应用实例
    app = QApplication(sys.argv)
    # 设置全局字体（可选）
    font = QFont("Arial", 10)
    app.setFont(font)
    # 创建主窗口
    window = MainWindow()
    window.show()
    # 运行应用主循环
    sys.exit(app.exec_())