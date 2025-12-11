import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFileDialog, QMessageBox,
    QTextEdit, QGroupBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

# ====================== 统一样式常量（便于维护） ======================
PAGE_STYLE = "background-color: #ECF0F1; color: black;"  # 页面基础样式
TITLE_FONT = QFont("微软雅黑", 22, QFont.Bold)          # 大标题字体
SUBTITLE_FONT = QFont("微软雅黑", 16, QFont.Bold)       # 子标题字体
DESC_FONT = QFont("微软雅黑", 11)                       # 描述文字字体
BUTTON_FONT = QFont("微软雅黑", 11)                     # 按钮字体
LOG_FONT = QFont("Consolas", 10)                        # 日志字体

# ====================== 页面组件（统一样式） ======================
class HomePage(QWidget):
    """首页展示页面（统一样式）"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 统一页面样式
        self.setStyleSheet(PAGE_STYLE)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        # 大标题
        title = QLabel("多媒体工具集")
        title.setFont(TITLE_FONT)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: black;")
        layout.addWidget(title)

        # 功能介绍（统一文字格式）
        desc = QLabel("""
        欢迎使用多媒体工具集！
        \n功能说明：
        • 视频模块：支持视频帧提取为图片、视频格式转换等
        • 图片模块：支持图片去重、图片批量处理等
        \n使用方式：点击左侧菜单选择对应功能
        """)
        desc.setFont(DESC_FONT)
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #333333; line-height: 1.4;")
        desc.setMaximumWidth(800)  # 统一宽度限制
        layout.addWidget(desc)

class VideoFrame2PicPage(QWidget):
    """视频帧转图片页面（核心页面）"""
    def __init__(self):
        super().__init__()
        self.selected_video = ""
        self.selected_output = ""
        self.init_ui()

    def init_ui(self):
        # 统一页面样式
        self.setStyleSheet(PAGE_STYLE)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        # 1. 标题 + 功能介绍（居中）
        title_group = QWidget()
        title_layout = QVBoxLayout(title_group)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setAlignment(Qt.AlignCenter)

        # 大标题
        page_title = QLabel("视频帧提取工具")
        page_title.setFont(TITLE_FONT)
        page_title.setStyleSheet("color: black; margin-bottom: 8px;")
        page_title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(page_title)

        # 功能介绍（统一格式）
        page_desc = QLabel("""
        功能说明：将视频文件按帧提取为图片格式（PNG），支持主流视频格式（MP4/AVI/MOV/MKV）。
        使用步骤：1.选择视频文件 → 2.选择输出文件夹 → 3.点击开始提取 → 4.查看提取日志
        """)
        page_desc.setFont(DESC_FONT)
        page_desc.setWordWrap(True)
        page_desc.setStyleSheet("color: #333333; line-height: 1.4;")
        page_desc.setAlignment(Qt.AlignCenter)
        page_desc.setMaximumWidth(800)
        title_layout.addWidget(page_desc)

        main_layout.addWidget(title_group)

        # 2. 文件选择区域（居中）
        file_group = QGroupBox("文件选择")
        file_group.setStyleSheet("""
            QGroupBox {
                font: bold 14px 微软雅黑;
                color: black;
                border: 1px solid #DDDDDD;
                border-radius: 8px;
                padding: 15px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }
        """)
        file_layout = QVBoxLayout(file_group)
        file_layout.setSpacing(15)
        file_layout.setContentsMargins(10, 10, 10, 10)
        file_layout.setAlignment(Qt.AlignCenter)

        # 视频文件选择行
        video_row = QWidget()
        video_row_layout = QHBoxLayout(video_row)
        video_row_layout.setSpacing(10)
        video_row_layout.setAlignment(Qt.AlignCenter)
        video_row_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_video = QPushButton("选择视频文件")
        self.btn_video.setFixedSize(120, 35)
        self.btn_video.setFont(BUTTON_FONT)
        self.btn_video.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        self.btn_video.clicked.connect(self.select_video)
        video_row_layout.addWidget(self.btn_video)

        self.lbl_video = QLabel("未选择视频文件")
        self.lbl_video.setFont(DESC_FONT)
        self.lbl_video.setStyleSheet("color: black;")
        self.lbl_video.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.lbl_video.setMaximumWidth(500)
        video_row_layout.addWidget(self.lbl_video)

        file_layout.addWidget(video_row)

        # 输出文件夹选择行
        output_row = QWidget()
        output_row_layout = QHBoxLayout(output_row)
        output_row_layout.setSpacing(10)
        output_row_layout.setAlignment(Qt.AlignCenter)
        output_row_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_output = QPushButton("选择输出文件夹")
        self.btn_output.setFixedSize(120, 35)
        self.btn_output.setFont(BUTTON_FONT)
        self.btn_output.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        self.btn_output.clicked.connect(self.select_output)
        output_row_layout.addWidget(self.btn_output)

        self.lbl_output = QLabel("未选择输出文件夹")
        self.lbl_output.setFont(DESC_FONT)
        self.lbl_output.setStyleSheet("color: black;")
        self.lbl_output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.lbl_output.setMaximumWidth(500)
        output_row_layout.addWidget(self.lbl_output)

        file_layout.addWidget(output_row)

        main_layout.addWidget(file_group)

        # 3. 提取操作区域（按钮居中）
        btn_row = QWidget()
        btn_row_layout = QHBoxLayout(btn_row)
        btn_row_layout.setAlignment(Qt.AlignCenter)
        btn_row_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_run = QPushButton("开始提取")
        self.btn_run.setFixedSize(120, 40)
        self.btn_run.setFont(QFont("微软雅黑", 12, QFont.Bold))
        # 强化禁用样式：更明显的置灰效果
        self.btn_run.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #45A049;
                    }
                    QPushButton:disabled {
                        background-color: #95A5A6;  /* 置灰颜色 */
                        color: #EEEEEE;             /* 文字浅灰 */
                        border: 1px solid #7F8C8D;  /* 边框加深，更明显 */
                        cursor: not-allowed;        /* 鼠标禁用样式 */
                    }
                """)
        #点击执行哪个方法
        self.btn_run.clicked.connect(self.run_extract)
        btn_row_layout.addWidget(self.btn_run)
        main_layout.addWidget(btn_row)

        # 4. 日志输出框
        log_group = QGroupBox("提取日志")
        log_group.setStyleSheet("""
            QGroupBox {
                font: bold 14px 微软雅黑;
                color: black;
                border: 1px solid #DDDDDD;
                border-radius: 8px;
                padding: 10px;
                margin-top: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
            }
        """)
        log_layout = QVBoxLayout(log_group)
        log_layout.setContentsMargins(5, 5, 5, 5)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(LOG_FONT)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
                border: 1px solid #DDDDDD;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        self.log_text.setMinimumHeight(200)
        log_layout.addWidget(self.log_text)
        main_layout.addWidget(log_group, stretch=1)

    def select_video(self):
        """选择视频文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择视频文件",
            "",
            "视频文件 (*.mp4 *.avi *.mov *.mkv *.*)"
        )
        if file_path:
            self.selected_video = file_path
            self.lbl_video.setText(f"已选：{file_path}")
            self.append_log(f"✅ 选择视频文件：{file_path}")

    def select_output(self):
        """选择输出文件夹"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if folder_path:
            self.selected_output = folder_path
            self.lbl_output.setText(f"已选：{folder_path}")
            self.append_log(f"✅ 选择输出文件夹：{folder_path}")

    def append_log(self, msg):
        """追加日志到输出框"""
        from datetime import datetime
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        self.log_text.append(f"{timestamp} {msg}")
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

    def run_extract(self):
        """模拟提取"""
        if not self.selected_video:
            QMessageBox.warning(self, "提示", "请先选择视频文件！")
            return
        if not self.selected_output:
            QMessageBox.warning(self, "提示", "请先选择输出文件夹！")
            return

        # 禁用执行按钮，避免重复点击
        self.btn_run.setDisabled(True)
        self.btn_run.setText("提取中...")  # 按钮文字提示
        QApplication.processEvents()  # 强制刷新UI

        #在主线程执行
        # self.run_target()

        self.extract_thread = ExtractThread(self.selected_video, self.selected_output)
        #这两个方法用于接收线程中发射出来的信号信息
        self.extract_thread.log_signal.signatures.connect(self.append_log)
        self.extract_thread.finish_signal.signatures.connect(self.on_extract_finish)
        self.extract_thread.start()

    def on_extract_finish(self, success, msg):
        """提取完成回调"""
        self.btn_run.setDisabled(False)
        self.btn_run.setText("开始提取")  # 恢复按钮文字
        if success:
            self.append_log(f"🎉 {msg}")
            QMessageBox.information(self, "成功", msg)
        else:
            self.append_log(f"❌ {msg}")
            QMessageBox.critical(self, "失败", msg)

    def run_target(self):
        """提取逻辑"""
        try:
            from target_script import target_script_fun

            self.append_log("⏳ 正在提取帧，视频越大，需要的时间越长，请耐心等待...")
            result, msg = target_script_fun(self.selected_video, self.selected_output)
            if result:
                self.append_log(msg)
                self.on_extract_finish(True, f"提取完成，输出路径：{self.selected_output}")
            else:
                self.append_log(msg)
                self.on_extract_finish(False, f"提取失败，请检查输入文件和输出路径是否正确！")

        except Exception as e:
            self.on_extract_finish(False, str(e))

class VideoOtherToolsPage(QWidget):
    """视频其他工具页面（统一样式）"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 统一页面样式
        self.setStyleSheet(PAGE_STYLE)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        # 子标题（统一字体）
        title = QLabel("视频其他工具")
        title.setFont(SUBTITLE_FONT)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: black;")
        layout.addWidget(title)

        # 功能描述（统一格式）
        desc = QLabel("""
        待开发功能：
        • 视频格式转换（MP4 ↔ AVI ↔ MOV 等）
        • 视频剪辑（截取指定时间段）
        • 视频压缩（调整分辨率/码率）
        • 音频提取（从视频中提取音频文件）
        """)
        desc.setFont(DESC_FONT)
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #333333; line-height: 1.4;")
        desc.setMaximumWidth(800)
        layout.addWidget(desc)

class ImageDeduplicationPage(QWidget):
    """图片去重页面（统一样式）"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 统一页面样式
        self.setStyleSheet(PAGE_STYLE)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        # 子标题（统一字体）
        title = QLabel("图片去重工具")
        title.setFont(SUBTITLE_FONT)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: black;")
        layout.addWidget(title)

        # 功能描述（统一格式）
        desc = QLabel("""
        待开发功能：
        • 基于哈希值对比（精准去重）
        • 基于相似度对比（模糊去重）
        • 批量删除重复图片
        • 保留指定文件夹的图片（去重时忽略）
        """)
        desc.setFont(DESC_FONT)
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #333333; line-height: 1.4;")
        desc.setMaximumWidth(800)
        layout.addWidget(desc)

class ImageProcessPage(QWidget):
    """图片处理页面（统一样式）"""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 统一页面样式
        self.setStyleSheet(PAGE_STYLE)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        # 子标题（统一字体）
        title = QLabel("图片处理工具")
        title.setFont(SUBTITLE_FONT)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: black;")
        layout.addWidget(title)

        # 功能描述（统一格式）
        desc = QLabel("""
        待开发功能：
        • 批量图片压缩（调整大小/质量）
        • 图片格式转换（PNG ↔ JPG ↔ WEBP 等）
        • 图片裁剪（按比例/自定义尺寸）
        • 图片水印（添加文字/图片水印）
        """)
        desc.setFont(DESC_FONT)
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #333333; line-height: 1.4;")
        desc.setMaximumWidth(800)
        layout.addWidget(desc)

# ====================== 视频提取线程 ======================
class ExtractThread(QThread):
    log_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(bool, str)

    def __init__(self, video_path, output_dir):
        super().__init__()
        self.video_path = video_path
        self.output_dir = output_dir

    def run(self):
        """提取逻辑"""
        try:
            from target_script import target_script_fun

            def run_target():
                self.log_signal.emit("⏳ 正在提取帧（请稍候）...")
                result,msg=target_script_fun(self.video_path, self.output_dir)
                if result:
                    self.log_signal.emit(msg)
                    self.finish_signal.emit(True, f"提取完成，输出路径：{self.output_dir}")
                else:
                    self.log_signal.emit(msg)
                    self.finish_signal.emit(False, f"提取失败，请检查输入文件和输出路径是否正确！")
            run_target()
        except Exception as e:
            self.finish_signal.emit(False, str(e))

# ====================== 主窗口（复用逻辑） ======================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.video_menu_expanded = False
        self.image_menu_expanded = False
        self.current_selected_btn = None
        self.all_menu_btns = []
        self.init_main_ui()

    def init_main_ui(self):
        # 窗口基础设置
        self.setWindowTitle("多媒体工具集")
        self.setGeometry(100, 100, 1100, 700)
        self.setMinimumSize(900, 600)

        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 整体布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ---------------------- 左侧菜单栏 ----------------------
        left_menu_widget = QWidget()
        left_menu_widget.setStyleSheet("background-color: #2C3E50;")
        left_menu_widget.setFixedWidth(200)
        self.left_layout = QVBoxLayout(left_menu_widget)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(0)
        self.left_layout.setAlignment(Qt.AlignTop)

        # 1. 首页菜单
        self.home_btn = self.create_main_menu_btn("首页")
        self.home_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.home_page),
            self.set_selected_btn(self.home_btn)
        ])
        self.left_layout.addWidget(self.home_btn)
        self.all_menu_btns.append(self.home_btn)

        # 2. 视频菜单组
        self.video_btn = self.create_main_menu_btn("视频")
        self.video_btn.clicked.connect(self.toggle_video_submenu)
        self.left_layout.addWidget(self.video_btn)
        self.all_menu_btns.append(self.video_btn)

        # 视频二级菜单容器
        self.video_submenu_widget = QWidget()
        self.video_submenu_layout = QVBoxLayout(self.video_submenu_widget)
        self.video_submenu_layout.setContentsMargins(20, 0, 0, 0)
        self.video_submenu_layout.setSpacing(0)

        # 视频二级菜单-帧转图片
        self.video_frame_btn = self.create_sub_menu_btn("视频帧转图片")
        self.video_frame_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.video_frame_page),
            self.set_selected_btn(self.video_frame_btn)
        ])
        self.video_submenu_layout.addWidget(self.video_frame_btn)
        self.all_menu_btns.append(self.video_frame_btn)

        # 视频二级菜单-其他工具
        self.video_other_btn = self.create_sub_menu_btn("其他视频工具")
        self.video_other_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.video_other_page),
            self.set_selected_btn(self.video_other_btn)
        ])
        self.video_submenu_layout.addWidget(self.video_other_btn)
        self.all_menu_btns.append(self.video_other_btn)

        self.video_submenu_widget.setVisible(False)
        self.left_layout.addWidget(self.video_submenu_widget)

        # 3. 图片菜单组
        self.image_btn = self.create_main_menu_btn("图片")
        self.image_btn.clicked.connect(self.toggle_image_submenu)
        self.left_layout.addWidget(self.image_btn)
        self.all_menu_btns.append(self.image_btn)

        # 图片二级菜单容器
        self.image_submenu_widget = QWidget()
        self.image_submenu_layout = QVBoxLayout(self.image_submenu_widget)
        self.image_submenu_layout.setContentsMargins(20, 0, 0, 0)
        self.image_submenu_layout.setSpacing(0)

        # 图片二级菜单-去重
        self.image_dedup_btn = self.create_sub_menu_btn("图片去重")
        self.image_dedup_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.image_dedup_page),
            self.set_selected_btn(self.image_dedup_btn)
        ])
        self.image_submenu_layout.addWidget(self.image_dedup_btn)
        self.all_menu_btns.append(self.image_dedup_btn)

        # 图片二级菜单-处理
        self.image_process_btn = self.create_sub_menu_btn("图片处理")
        self.image_process_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.image_process_page),
            self.set_selected_btn(self.image_process_btn)
        ])
        self.image_submenu_layout.addWidget(self.image_process_btn)
        self.all_menu_btns.append(self.image_process_btn)

        self.image_submenu_widget.setVisible(False)
        self.left_layout.addWidget(self.image_submenu_widget)

        # 填充空白
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

        # 组装布局
        main_layout.addWidget(left_menu_widget)
        main_layout.addWidget(self.stacked_widget)

        # 默认选中首页
        self.set_selected_btn(self.home_btn)
        self.stacked_widget.setCurrentWidget(self.home_page)

    def create_main_menu_btn(self, text):
        """创建一级菜单按钮"""
        btn = QPushButton(text)
        btn.setFixedWidth(200)
        btn.setMinimumHeight(50)
        btn.setFont(QFont("微软雅黑", 14, QFont.Bold))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border: none;
                border-bottom: 1px solid #34495E;
                text-align: center;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            QPushButton:checked {
                background-color: #3498DB;
                color: white;
                border-left: 4px solid #FFFFFF;
            }
        """)
        btn.setCheckable(True)
        return btn

    def create_sub_menu_btn(self, text):
        """创建二级菜单按钮"""
        btn = QPushButton(text)
        btn.setFixedWidth(180)
        btn.setMinimumHeight(40)
        btn.setFont(QFont("微软雅黑", 12))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                color: #E0E0E0;
                border: none;
                text-align: left;
                padding-left: 10px;
            }
            QPushButton:hover {
                background-color: #34495E;
                color: white;
            }
            QPushButton:checked {
                background-color: #3498DB;
                color: white;
                border-left: 4px solid #FFFFFF;
                padding-left: 6px;
            }
        """)
        btn.setCheckable(True)
        return btn

    def toggle_video_submenu(self):
        """切换视频二级菜单"""
        self.video_menu_expanded = not self.video_menu_expanded
        self.video_submenu_widget.setVisible(self.video_menu_expanded)
        self.video_btn.setText("视频" if self.video_menu_expanded else "视频")
        if self.video_menu_expanded and not any([self.video_frame_btn.isChecked(), self.video_other_btn.isChecked()]):
            self.set_selected_btn(self.video_btn)

    def toggle_image_submenu(self):
        """切换图片二级菜单"""
        self.image_menu_expanded = not self.image_menu_expanded
        self.image_submenu_widget.setVisible(self.image_menu_expanded)
        self.image_btn.setText("图片" if self.image_menu_expanded else "图片")
        if self.image_menu_expanded and not any([self.image_dedup_btn.isChecked(), self.image_process_btn.isChecked()]):
            self.set_selected_btn(self.image_btn)

    def set_selected_btn(self, target_btn):
        """设置选中按钮高亮"""
        for btn in self.all_menu_btns:
            if btn != target_btn:
                btn.setChecked(False)
        target_btn.setChecked(True)
        self.current_selected_btn = target_btn

# ====================== 程序入口 ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("微软雅黑", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())