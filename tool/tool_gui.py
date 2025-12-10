import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QToolButton, QMenu, QAction, QStackedWidget,QPushButton,
    QLabel, QFrame, QSizePolicy, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QCursor

# ====================== 页面组件（复用原有页面，无修改） ======================
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
        btn_run.clicked.connect(self.run_extract)
        layout.addWidget(btn_run, alignment=Qt.AlignCenter)

    def select_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择视频文件",
            "",
            "视频文件 (*.mp4 *.avi *.mov *.mkv)"
        )
        if file_path:
            self.selected_video = file_path
            self.lbl_video.setText(f"已选视频：{file_path}")

    def select_output(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if folder_path:
            self.selected_output = folder_path
            self.lbl_output.setText(f"已选文件夹：{folder_path}")

    def run_extract(self):
        if not self.selected_video:
            QMessageBox.warning(self, "提示", "请先选择视频文件！")
            return
        if not self.selected_output:
            QMessageBox.warning(self, "提示", "请先选择输出文件夹！")
            return
        QMessageBox.information(self, "成功", f"开始提取 {self.selected_video} 的帧到 {self.selected_output}！")

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

# ====================== 主窗口（核心修改：下拉式二级菜单） ======================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

        # ---------------------- 左侧菜单栏（核心修改） ----------------------
        left_menu_widget = QWidget()
        left_menu_widget.setStyleSheet("background-color: #2C3E50;")
        left_menu_widget.setFixedWidth(200)
        left_layout = QVBoxLayout(left_menu_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        left_layout.setAlignment(Qt.AlignTop)

        # 1. 首页按钮（无下拉菜单，直接切换页面）
        self.home_btn = self.create_main_menu_btn("首页")
        self.home_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))
        left_layout.addWidget(self.home_btn)

        # 2. 视频按钮（带下拉二级菜单）
        self.video_btn = self.create_main_menu_btn("视频", has_dropdown=True)
        # 创建视频二级菜单
        video_menu = QMenu(self)
        video_menu.setStyleSheet("""
            QMenu {
                background-color: #34495E;
                color: white;
                font-size: 12px;
                border: none;
                padding: 5px 0;
            }
            QMenu::item {
                padding: 8px 20px;
                margin: 0;
            }
            QMenu::item:selected {
                background-color: #3498DB;
                color: white;
            }
        """)
        # 添加视频二级菜单项
        video_frame_action = QAction("视频帧转图片", self)
        video_frame_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.video_frame_page))
        video_other_action = QAction("其他视频工具", self)
        video_other_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.video_other_page))
        video_menu.addAction(video_frame_action)
        video_menu.addAction(video_other_action)
        # 绑定下拉菜单到视频按钮
        self.video_btn.setMenu(video_menu)
        # 设置下拉菜单弹出位置（按钮下方）
        self.video_btn.clicked.connect(lambda: self.show_menu_at_btn(self.video_btn, video_menu))
        left_layout.addWidget(self.video_btn)

        # 3. 图片按钮（带下拉二级菜单）
        self.image_btn = self.create_main_menu_btn("图片", has_dropdown=True)
        # 创建图片二级菜单
        image_menu = QMenu(self)
        image_menu.setStyleSheet("""
            QMenu {
                background-color: #34495E;
                color: white;
                font-size: 12px;
                border: none;
                padding: 5px 0;
            }
            QMenu::item {
                padding: 8px 20px;
                margin: 0;
            }
            QMenu::item:selected {
                background-color: #3498DB;
                color: white;
            }
        """)
        # 添加图片二级菜单项
        image_dedup_action = QAction("图片去重", self)
        image_dedup_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.image_dedup_page))
        image_process_action = QAction("图片处理", self)
        image_process_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.image_process_page))
        image_menu.addAction(image_dedup_action)
        image_menu.addAction(image_process_action)
        # 绑定下拉菜单到图片按钮
        self.image_btn.setMenu(image_menu)
        self.image_btn.clicked.connect(lambda: self.show_menu_at_btn(self.image_btn, image_menu))
        left_layout.addWidget(self.image_btn)

        # 填充左侧栏空白（避免按钮挤在一起）
        left_layout.addStretch()

        # ---------------------- 右侧内容区（无修改） ----------------------
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
        self.stacked_widget.setCurrentWidget(self.home_page)
        self.set_btn_selected(self.home_btn)

    def create_main_menu_btn(self, text, has_dropdown=False):
        """创建一级菜单按钮（支持是否带下拉箭头）"""
        btn = QToolButton()
        btn.setText(text)
        btn.setFixedWidth(200)
        btn.setMinimumHeight(50)
        btn.setFont(QFont("微软雅黑", 14, QFont.Bold))
        # 设置按钮样式
        btn_style = """
            QToolButton {
                background-color: #2C3E50;
                color: white;
                border: none;
                border-bottom: 1px solid #34495E;
                text-align: center;
                padding: 0;
            }
            QToolButton:hover {
                background-color: #34495E;
            }
            QToolButton:selected, QToolButton:pressed {
                background-color: #3498DB;
                color: white;
            }
        """
        if has_dropdown:
            # 带下拉箭头的按钮样式
            btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            btn.setArrowType(Qt.DownArrow)
            btn_style += """
                QToolButton::down-arrow {
                    image: none;
                    border: none;
                    color: white;
                }
            """
        btn.setStyleSheet(btn_style)
        # 允许按钮被选中
        btn.setCheckable(True)
        return btn

    def show_menu_at_btn(self, btn, menu):
        """在按钮下方弹出下拉菜单"""
        # 获取按钮在屏幕上的位置
        btn_rect = btn.rect()
        # 计算菜单弹出位置：按钮左下角，y轴偏移按钮高度
        menu_pos = btn.mapToGlobal(QPoint(0, btn_rect.height()))
        # 弹出菜单
        menu.exec_(menu_pos)
        # 取消按钮的选中状态（避免按钮一直高亮）
        btn.setChecked(False)

    def set_btn_selected(self, target_btn):
        """设置按钮为选中状态，取消其他按钮"""
        for btn in [self.home_btn, self.video_btn, self.image_btn]:
            btn.setChecked(btn == target_btn)

# ====================== 程序入口 ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("微软雅黑", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())