import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from target_2 import target_2
# ====================== 页面组件（复用，无修改） ======================
class HomePage(QWidget):
    """首页展示页面"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("多媒体工具集")
        title.setFont(QFont("微软雅黑", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        desc = QLabel("""
        欢迎使用多媒体工具集！
        \n功能说明：
        • 视频模块：支持视频帧提取为图片、视频格式转换等
        • 图片模块：支持图片去重、图片批量处理等
        \n使用方式：点击左侧菜单选择对应功能
        """)
        desc.setFont(QFont("微软雅黑", 12))
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)

        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(desc)

class VideoFrame2PicPage(QWidget):
    """视频帧转图片页面"""
    def __init__(self):
        super().__init__()
        self.selected_video = ""
        self.selected_output = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("视频帧提取为图片")
        title.setFont(QFont("微软雅黑", 18, QFont.Bold))
        layout.addWidget(title)
        layout.addSpacing(20)

        btn_video = QPushButton("选择视频文件")
        btn_video.setFont(QFont("微软雅黑", 12))
        btn_video.clicked.connect(self.select_video)
        layout.addWidget(btn_video)

        self.lbl_video = QLabel("已选视频：无")
        self.lbl_video.setFont(QFont("微软雅黑", 10))
        layout.addWidget(self.lbl_video)
        layout.addSpacing(10)

        btn_output = QPushButton("选择输出文件夹")
        btn_output.setFont(QFont("微软雅黑", 12))
        btn_output.clicked.connect(self.select_output)
        layout.addWidget(btn_output)

        self.lbl_output = QLabel("已选文件夹：无")
        self.lbl_output.setFont(QFont("微软雅黑", 10))
        layout.addWidget(self.lbl_output)
        layout.addSpacing(20)

        btn_run = QPushButton("开始提取")
        btn_run.setFont(QFont("微软雅黑", 12))
        btn_run.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 5px;")
        btn_run.clicked.connect(self.run_script)
        layout.addWidget(btn_run, alignment=Qt.AlignCenter)
        self.btn_run = btn_run  # 保存引用，用于控制禁用/启用

    def select_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择视频文件",
            "",
            "视频文件 (*.mp4 *.avi *.mov *.mkv *.*)"
        )
        if file_path:
            self.selected_video = file_path
            self.lbl_video.setText(f"已选视频：{file_path}")

    def select_output(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if folder_path:
            self.selected_output = folder_path
            self.lbl_output.setText(f"已选文件夹：{folder_path}")

    def run_script(self):
        """执行指定Python脚本"""
        if not self.selected_video:
            QMessageBox.warning(self, "提示", "请先选择视频文件！")
            return
        if not self.selected_output:
            QMessageBox.warning(self, "提示", "请先选择输出文件夹！")
            return

        # 禁用执行按钮，避免重复点击
        self.btn_run.setDisabled(True)

        try:
            result,message=target_2(self.selected_video, self.selected_output)
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
            self.btn_run.setDisabled(False)
class VideoOtherToolsPage(QWidget):
    """视频其他工具页面"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        lbl = QLabel("视频其他工具（格式转换/剪辑等）")
        lbl.setFont(QFont("微软雅黑", 16))
        layout.addWidget(lbl)

class ImageDeduplicationPage(QWidget):
    """图片去重页面"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        lbl = QLabel("图片去重工具（相似度对比/重复删除）")
        lbl.setFont(QFont("微软雅黑", 16))
        layout.addWidget(lbl)

class ImageProcessPage(QWidget):
    """图片处理页面"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        lbl = QLabel("图片处理工具（压缩/裁剪/格式转换等）")
        lbl.setFont(QFont("微软雅黑", 16))
        layout.addWidget(lbl)

# ====================== 主窗口（核心：多级菜单高亮） ======================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 状态变量
        self.video_menu_expanded = False  # 视频二级菜单展开状态
        self.image_menu_expanded = False  # 图片二级菜单展开状态
        self.current_selected_btn = None  # 当前选中的菜单按钮（一级/二级）
        self.all_menu_btns = []           # 所有菜单按钮列表（用于批量取消选中）
        self.init_main_ui()

    def init_main_ui(self):
        # 窗口基础设置
        self.setWindowTitle("多媒体工具集")
        self.setGeometry(100, 100, 1000, 600)
        self.setMinimumSize(800, 500)

        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 整体布局：左侧菜单 + 右侧内容
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ---------------------- 左侧菜单栏（核心优化） ----------------------
        left_menu_widget = QWidget()
        left_menu_widget.setStyleSheet("background-color: #2C3E50;")
        left_menu_widget.setFixedWidth(200)
        # 左侧布局：垂直、顶部对齐、动态调整
        self.left_layout = QVBoxLayout(left_menu_widget)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(0)
        self.left_layout.setAlignment(Qt.AlignTop)

        # 1. 首页菜单（一级）
        self.home_btn = self.create_main_menu_btn("首页")
        self.home_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.home_page),
            self.set_selected_btn(self.home_btn)  # 选中首页按钮
        ])
        self.left_layout.addWidget(self.home_btn)
        self.all_menu_btns.append(self.home_btn)  # 加入全局按钮列表

        # 2. 视频菜单组（一级按钮 + 二级菜单）
        self.video_btn = self.create_main_menu_btn("视频")
        self.video_btn.clicked.connect(self.toggle_video_submenu)
        self.left_layout.addWidget(self.video_btn)
        self.all_menu_btns.append(self.video_btn)  # 加入全局按钮列表

        # 视频二级菜单容器（初始隐藏）
        self.video_submenu_widget = QWidget()
        self.video_submenu_layout = QVBoxLayout(self.video_submenu_widget)
        self.video_submenu_layout.setContentsMargins(20, 0, 0, 0)
        self.video_submenu_layout.setSpacing(0)

        # 视频二级菜单-帧转图片
        self.video_frame_btn = self.create_sub_menu_btn("视频帧转图片")
        self.video_frame_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.video_frame_page),
            self.set_selected_btn(self.video_frame_btn)  # 选中二级按钮
        ])
        self.video_submenu_layout.addWidget(self.video_frame_btn)
        self.all_menu_btns.append(self.video_frame_btn)

        # 视频二级菜单-其他工具
        self.video_other_btn = self.create_sub_menu_btn("其他视频工具")
        self.video_other_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.video_other_page),
            self.set_selected_btn(self.video_other_btn)  # 选中二级按钮
        ])
        self.video_submenu_layout.addWidget(self.video_other_btn)
        self.all_menu_btns.append(self.video_other_btn)

        # 初始隐藏二级菜单
        self.video_submenu_widget.setVisible(False)
        self.left_layout.addWidget(self.video_submenu_widget)

        # 3. 图片菜单组（一级按钮 + 二级菜单）
        self.image_btn = self.create_main_menu_btn("图片")
        self.image_btn.clicked.connect(self.toggle_image_submenu)
        self.left_layout.addWidget(self.image_btn)
        self.all_menu_btns.append(self.image_btn)  # 加入全局按钮列表

        # 图片二级菜单容器（初始隐藏）
        self.image_submenu_widget = QWidget()
        self.image_submenu_layout = QVBoxLayout(self.image_submenu_widget)
        self.image_submenu_layout.setContentsMargins(20, 0, 0, 0)
        self.image_submenu_layout.setSpacing(0)

        # 图片二级菜单-去重
        self.image_dedup_btn = self.create_sub_menu_btn("图片去重")
        self.image_dedup_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.image_dedup_page),
            self.set_selected_btn(self.image_dedup_btn)  # 选中二级按钮
        ])
        self.image_submenu_layout.addWidget(self.image_dedup_btn)
        self.all_menu_btns.append(self.image_dedup_btn)

        # 图片二级菜单-处理
        self.image_process_btn = self.create_sub_menu_btn("图片处理")
        self.image_process_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.image_process_page),
            self.set_selected_btn(self.image_process_btn)  # 选中二级按钮
        ])
        self.image_submenu_layout.addWidget(self.image_process_btn)
        self.all_menu_btns.append(self.image_process_btn)

        # 初始隐藏二级菜单
        self.image_submenu_widget.setVisible(False)
        self.left_layout.addWidget(self.image_submenu_widget)

        # 填充左侧栏空白
        self.left_layout.addStretch()

        # ---------------------- 右侧内容区 ----------------------
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #ECF0F1;")

        # 注册所有页面
        self.home_page = HomePage()
        self.video_frame_page = VideoFrame2PicPage()
        self.video_other_page = VideoOtherToolsPage()
        self.image_dedup_page = ImageDeduplicationPage()
        self.image_process_page = ImageProcessPage()

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.video_frame_page)
        self.stacked_widget.addWidget(self.video_other_page)
        self.stacked_widget.addWidget(self.image_dedup_page)
        self.stacked_widget.addWidget(self.image_process_page)

        # ---------------------- 组装布局 ----------------------
        main_layout.addWidget(left_menu_widget)
        main_layout.addWidget(self.stacked_widget)

        # 默认选中首页
        self.set_selected_btn(self.home_btn)
        self.stacked_widget.setCurrentWidget(self.home_page)

    def create_main_menu_btn(self, text):
        """创建一级菜单按钮（文字居中，含选中样式）"""
        btn = QPushButton(text)
        btn.setFixedWidth(200)
        btn.setMinimumHeight(50)
        btn.setFont(QFont("微软雅黑", 14, QFont.Bold))
        # 核心：一级菜单样式（默认态 + hover + 选中态）
        btn.setStyleSheet("""
            /* 默认态 */
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border: none;
                border-bottom: 1px solid #34495E;
                text-align: center;  /* 文字居中 */
                padding: 0;
            }
            /* 悬浮态 */
            QPushButton:hover {
                background-color: #34495E;
            }
            /* 选中态（高亮） */
            QPushButton:checked {
                background-color: #3498DB;  /* 一级菜单高亮色 */
                color: white;
                border-left: 4px solid #FFFFFF;  /* 左侧高亮条，增强视觉 */
            }
        """)
        btn.setCheckable(True)  # 允许选中状态
        return btn

    def create_sub_menu_btn(self, text):
        """创建二级菜单按钮（含选中样式）"""
        btn = QPushButton(text)
        btn.setFixedWidth(180)
        btn.setMinimumHeight(40)
        btn.setFont(QFont("微软雅黑", 12))
        # 核心：二级菜单样式（默认态 + hover + 选中态）
        btn.setStyleSheet("""
            /* 默认态 */
            QPushButton {
                background-color: #2C3E50;
                color: #E0E0E0;
                border: none;
                text-align: left;
                padding-left: 15px;
            }
            /* 悬浮态 */
            QPushButton:hover {
                background-color: #34495E;
                color: white;
            }
            /* 选中态（高亮） */
            QPushButton:checked {
                background-color: #2980B9;  /* 二级菜单高亮色（比一级浅） */
                color: white;
                border-left: 3px solid #FFFFFF;  /* 左侧短高亮条，区分层级 */
            }
        """)
        btn.setCheckable(True)  # 允许选中状态
        return btn

    def toggle_video_submenu(self):
        """切换视频二级菜单的展开/收起"""
        self.video_menu_expanded = not self.video_menu_expanded
        self.video_submenu_widget.setVisible(self.video_menu_expanded)
        self.video_btn.setText("视频" if self.video_menu_expanded else "视频")
        # 点击一级菜单但未选中二级时，选中一级菜单
        if not self.video_menu_expanded:
            self.set_selected_btn(self.video_btn)

    def toggle_image_submenu(self):
        """切换图片二级菜单的展开/收起"""
        self.image_menu_expanded = not self.image_menu_expanded
        self.image_submenu_widget.setVisible(self.image_menu_expanded)
        self.image_btn.setText("图片" if self.image_menu_expanded else "图片")
        # 点击一级菜单但未选中二级时，选中一级菜单
        if not self.image_menu_expanded:
            self.set_selected_btn(self.image_btn)

    def set_selected_btn(self, target_btn):
        """核心：设置目标按钮为选中态，取消所有其他按钮的选中态"""
        # 1. 取消所有菜单按钮的选中态
        for btn in self.all_menu_btns:
            btn.setChecked(False)
        # 2. 设置目标按钮为选中态
        target_btn.setChecked(True)
        # 3. 更新当前选中按钮状态
        self.current_selected_btn = target_btn
        # 4. 若选中二级菜单，自动展开对应一级菜单
        if target_btn in [self.video_frame_btn, self.video_other_btn]:
            self.video_menu_expanded = True
            self.video_submenu_widget.setVisible(True)
            self.video_btn.setText("视频")
        elif target_btn in [self.image_dedup_btn, self.image_process_btn]:
            self.image_menu_expanded = True
            self.image_submenu_widget.setVisible(True)
            self.image_btn.setText("图片")

# ====================== 程序入口 ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("微软雅黑", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())