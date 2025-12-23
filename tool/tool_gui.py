import sys
import os
import datetime
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFileDialog, QMessageBox,
    QTextEdit, QGroupBox, QSizePolicy, QCheckBox, QLineEdit, QGridLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMetaObject, Q_ARG, QTimer
from PyQt5.QtGui import QFont, QColor, QIntValidator

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
        ## 连接信号到槽函数
        self.extract_thread.log_signal.connect(self.append_log)
        self.extract_thread.finish_signal.connect(self.on_extract_finish)
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

#图片去重页面
class ImageDeduplicationPage(QWidget):
    """图片去重工具页面（修复复选框弹窗问题）"""

    def __init__(self):
        super().__init__()
        self.selected_folder = ""  # 待去重的文件夹
        self.is_delete_dup = False  # 是否删除重复图片
        self.dedup_thread = None
        self.init_ui()

    def init_ui(self):
        # 统一页面样式
        self.setStyleSheet(PAGE_STYLE)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        # 1. 标题 + 功能介绍（居中，与视频页面一致）
        title_group = QWidget()
        title_layout = QVBoxLayout(title_group)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setAlignment(Qt.AlignCenter)

        page_title = QLabel("图片去重工具")
        page_title.setFont(TITLE_FONT)
        page_title.setStyleSheet("color: black; margin-bottom: 8px;")
        page_title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(page_title)

        page_desc = QLabel("""
        功能说明：扫描指定文件夹内的图片，识别重复图片（支持PNG/JPG/JPEG/WEBP格式）。
        使用步骤：1.选择待去重文件夹 → 2.选择是否删除重复图片 → 3.点击开始去重 → 4.查看去重日志
        """)
        page_desc.setFont(DESC_FONT)
        page_desc.setWordWrap(True)
        page_desc.setStyleSheet("color: #333333; line-height: 1.4;")
        page_desc.setAlignment(Qt.AlignCenter)
        page_desc.setMaximumWidth(800)
        title_layout.addWidget(page_desc)

        main_layout.addWidget(title_group)

        # 2. 文件夹选择 + 复选框区域（核心功能）
        file_group = QGroupBox("去重设置")
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
        file_layout.setSpacing(20)
        file_layout.setContentsMargins(10, 10, 10, 10)
        file_layout.setAlignment(Qt.AlignCenter)

        # 2.1 选择待去重文件夹行
        folder_row = QWidget()
        folder_row_layout = QHBoxLayout(folder_row)
        folder_row_layout.setSpacing(10)
        folder_row_layout.setAlignment(Qt.AlignCenter)
        folder_row_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_folder = QPushButton("去重文件夹")
        self.btn_folder.setFixedSize(150, 35)
        self.btn_folder.setFont(BUTTON_FONT)
        self.btn_folder.setStyleSheet("""
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
        self.btn_folder.clicked.connect(self.select_folder)
        folder_row_layout.addWidget(self.btn_folder)

        self.lbl_folder = QLabel("未选择文件夹")
        self.lbl_folder.setFont(DESC_FONT)
        self.lbl_folder.setStyleSheet("color: black;")
        self.lbl_folder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.lbl_folder.setMaximumWidth(500)
        folder_row_layout.addWidget(self.lbl_folder)

        file_layout.addWidget(folder_row)

        # 2.2 删除重复图片复选框（核心修复：改用click事件）
        checkbox_row = QWidget()
        checkbox_row_layout = QHBoxLayout(checkbox_row)
        checkbox_row_layout.setSpacing(10)
        checkbox_row_layout.setAlignment(Qt.AlignCenter)
        checkbox_row_layout.setContentsMargins(0, 0, 0, 0)

        self.cb_delete_dup = QCheckBox("删除重复图片（保留一张）")
        self.cb_delete_dup.setFont(DESC_FONT)
        self.cb_delete_dup.setStyleSheet("""
            QCheckBox {
                color: black;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:checked {
                background-color: #3498DB;
                border: 1px solid #2980B9;
            }
        """)
        # 核心修复：绑定click事件（而非stateChanged），确保每次点击都触发
        self.cb_delete_dup.clicked.connect(self.on_checkbox_click)
        checkbox_row_layout.addWidget(self.cb_delete_dup)

        file_layout.addWidget(checkbox_row)

        main_layout.addWidget(file_group)

        # 3. 开始去重按钮（与视频页面按钮样式一致）
        btn_row = QWidget()
        btn_row_layout = QHBoxLayout(btn_row)
        btn_row_layout.setAlignment(Qt.AlignCenter)
        btn_row_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_run = QPushButton("开始去重")
        self.btn_run.setFixedSize(120, 40)
        self.btn_run.setFont(QFont("微软雅黑", 12, QFont.Bold))
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
                background-color: #95A5A6;
                color: #EEEEEE;
                border: 1px solid #7F8C8D;
                cursor: not-allowed;
            }
        """)
        self.btn_run.clicked.connect(self.run_dedup)
        btn_row_layout.addWidget(self.btn_run)

        main_layout.addWidget(btn_row)

        # 4. 日志输出框（与视频页面一致）
        log_group = QGroupBox("去重日志")
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

    def select_folder(self):
        """选择待去重的文件夹"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择待去重文件夹")
        if folder_path:
            self.selected_folder = folder_path
            self.lbl_folder.setText(f"已选：{folder_path}")
            self.append_log(f"✅ 选择待去重文件夹：{folder_path}")

    def on_checkbox_click(self, checked):
        """核心修复：点击事件处理（替代stateChanged）"""
        if checked:  # 只有勾选时才弹窗
            # 显示提示弹窗
            reply = QMessageBox.question(
                self,
                "警告",
                "会删除重复图片，但会保留一张不重复图片！\n是否确认开启该功能？",
                QMessageBox.Cancel | QMessageBox.Ok,
                QMessageBox.Cancel  # 默认选中取消按钮
            )
            if reply == QMessageBox.Ok:
                # 确认：保持勾选状态
                self.is_delete_dup = True
                self.cb_delete_dup.setChecked(True)  # 强制设置勾选
                self.append_log("⚠️ 已开启「删除重复图片」功能（保留一张）")
            else:
                # 取消：强制取消勾选
                self.is_delete_dup = False
                self.cb_delete_dup.setChecked(False)  # 关键：强制取消
        else:
            # 取消勾选：直接更新状态，不弹窗
            self.is_delete_dup = False
            self.append_log("ℹ️ 已关闭「删除重复图片」功能")

    def append_log(self, msg):
        """追加日志（与视频页面逻辑一致）"""
        from datetime import datetime
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        full_msg = f"{timestamp} {msg}"

        QMetaObject.invokeMethod(
            self.log_text,
            "append",
            Qt.QueuedConnection,
            Q_ARG(str, full_msg)
        )
        QMetaObject.invokeMethod(
            self.log_text.verticalScrollBar(),
            "setValue",
            Qt.QueuedConnection,
            Q_ARG(int, self.log_text.verticalScrollBar().maximum())
        )

    def run_dedup(self):
        """开始图片去重"""
        # 前置校验
        if not self.selected_folder:
            QMessageBox.warning(self, "提示", "请先选择待去重文件夹！")
            return

        # 禁用按钮
        self.btn_run.setDisabled(True)
        self.btn_run.setText("去重中...")
        QApplication.processEvents()

        self.append_log("📌 开始图片去重扫描...")
        self.append_log(f"🔧 删除重复图片功能：{'开启' if self.is_delete_dup else '关闭'}")

        # 启动去重线程
        try:
            self.dedup_thread = ImageDedupThread(self.selected_folder, self.is_delete_dup)
            self.dedup_thread.log_signal.connect(self.append_log)
            self.dedup_thread.finish_signal.connect(self.on_dedup_finish)
            self.dedup_thread.start()
        except Exception as e:
            self.append_log(f"❌ 线程启动失败：{str(e)}")
            self.ensure_btn_enabled()

    def on_dedup_finish(self, success, msg):
        """去重完成回调"""
        self.btn_run.setDisabled(False)
        self.btn_run.setText("开始去重")
        QApplication.processEvents()

        if success:
            self.append_log(f"🎉 去重完成：{msg}")
            QMessageBox.information(self, "成功", msg)
        else:
            self.append_log(f"❌ 去重失败：{msg}")
            QMessageBox.critical(self, "失败", msg)

    def ensure_btn_enabled(self):
        """兜底恢复按钮"""
        if self.btn_run.isDisabled():
            self.btn_run.setDisabled(False)
            self.btn_run.setText("开始去重")
            QApplication.processEvents()
#图片其他页面
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

#文件或着文件夹大小工具页面
class FileSizeToolPage(QWidget):
    """文件大小工具页面"""

    def __init__(self):
        super().__init__()
        self.selected_path = ""
        self.size_thread = None
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(PAGE_STYLE)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        # 1. 标题 + 功能介绍
        title_group = QWidget()
        title_layout = QVBoxLayout(title_group)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setAlignment(Qt.AlignCenter)

        page_title = QLabel("文件大小工具")
        page_title.setFont(TITLE_FONT)
        page_title.setStyleSheet("color: black; margin-bottom: 8px;")
        page_title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(page_title)

        page_desc = QLabel("""
        功能说明：统计指定文件或文件夹的大小，支持递归统计文件夹内所有文件总大小。
        使用步骤：1.选择文件/文件夹 → 2.点击判断大小 → 3.查看大小统计日志
        """)
        page_desc.setFont(DESC_FONT)
        page_desc.setWordWrap(True)
        page_desc.setStyleSheet("color: #333333; line-height: 1.4;")
        page_desc.setAlignment(Qt.AlignCenter)
        page_desc.setMaximumWidth(800)
        title_layout.addWidget(page_desc)

        main_layout.addWidget(title_group)

        # 2. 文件/文件夹选择区域
        # 2. 文件/文件夹选择区域
        file_group = QGroupBox("路径选择")
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

        # 路径选择行（支持文件/文件夹）
        path_row = QWidget()
        path_row_layout = QHBoxLayout(path_row)
        path_row_layout.setSpacing(10)
        path_row_layout.setAlignment(Qt.AlignCenter)
        path_row_layout.setContentsMargins(0, 0, 0, 0)

        # 选择文件按钮
        self.btn_file = QPushButton("选择文件")
        self.btn_file.setFixedSize(100, 35)
        self.btn_file.setFont(BUTTON_FONT)
        self.btn_file.setStyleSheet("""
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
        self.btn_file.clicked.connect(self.select_file)
        path_row_layout.addWidget(self.btn_file)

        # 选择文件夹按钮
        self.btn_folder = QPushButton("选择文件夹")
        self.btn_folder.setFixedSize(100, 35)
        self.btn_folder.setFont(BUTTON_FONT)
        self.btn_folder.setStyleSheet("""
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
        self.btn_folder.clicked.connect(self.select_folder)
        path_row_layout.addWidget(self.btn_folder)

        self.lbl_path = QLabel("未选择文件/文件夹")
        self.lbl_path.setFont(DESC_FONT)
        self.lbl_path.setStyleSheet("color: black;")
        self.lbl_path.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.lbl_path.setMaximumWidth(400)
        path_row_layout.addWidget(self.lbl_path)

        file_layout.addWidget(path_row)

        # 新增：大小阈值输入行
        size_input_row = QWidget()
        size_input_row_layout = QHBoxLayout(size_input_row)
        size_input_row_layout.setSpacing(10)
        size_input_row_layout.setAlignment(Qt.AlignCenter)
        size_input_row_layout.setContentsMargins(0, 0, 0, 0)

        # 输入框标签
        lbl_size = QLabel("大小阈值（字节）：")
        lbl_size.setFont(DESC_FONT)
        size_input_row_layout.addWidget(lbl_size)

        # 整数输入框（仅允许输入整数）
        self.le_size = QLineEdit()
        self.le_size.setFixedWidth(120)
        self.le_size.setFont(DESC_FONT)
        self.le_size.setPlaceholderText("请输入整数（字节）")
        # 设置仅允许输入整数
        self.le_size.setValidator(QIntValidator(0, 2147483647))
        size_input_row_layout.addWidget(self.le_size)

        # 换算关系提示标签
        tip_label = QLabel("换算：1KB=1024B | 1MB=1024KB | 1GB=1024MB")
        tip_label.setFont(QFont("微软雅黑", 9))
        tip_label.setStyleSheet("color: #666666;")
        size_input_row_layout.addWidget(tip_label)

        file_layout.addWidget(size_input_row)

        main_layout.addWidget(file_group)

        # 3. 操作按钮区域
        btn_row = QWidget()
        btn_row_layout = QHBoxLayout(btn_row)
        btn_row_layout.setAlignment(Qt.AlignCenter)
        btn_row_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_calc = QPushButton("判断大小")
        self.btn_calc.setFixedSize(120, 40)
        self.btn_calc.setFont(QFont("微软雅黑", 12, QFont.Bold))
        self.btn_calc.setStyleSheet("""
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
                background-color: #95A5A6;
                color: #EEEEEE;
                border: 1px solid #7F8C8D;
                cursor: not-allowed;
            }
        """)
        self.btn_calc.clicked.connect(self.calc_size)
        btn_row_layout.addWidget(self.btn_calc)

        main_layout.addWidget(btn_row)

        # 4. 日志输出框
        log_group = QGroupBox("大小统计日志")
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

    def select_file(self):
        """选择单个文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择文件",
            "",
            "所有文件 (*.*)"
        )
        if file_path:
            self.selected_path = file_path
            self.lbl_path.setText(f"已选文件：{os.path.basename(file_path)}")
            self.append_log(f"✅ 选择文件：{file_path}")

    def select_folder(self):
        """选择文件夹"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.selected_path = folder_path
            self.lbl_path.setText(f"已选文件夹：{folder_path}")
            self.append_log(f"✅ 选择文件夹：{folder_path}")

    def append_log(self, msg):
        """追加日志"""
        from datetime import datetime
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        full_msg = f"{timestamp} {msg}"

        QMetaObject.invokeMethod(
            self.log_text,
            "append",
            Qt.QueuedConnection,
            Q_ARG(str, full_msg)
        )
        QMetaObject.invokeMethod(
            self.log_text.verticalScrollBar(),
            "setValue",
            Qt.QueuedConnection,
            Q_ARG(int, self.log_text.verticalScrollBar().maximum())
        )

    def calc_size(self):
        """计算文件/文件夹大小"""
        if not self.selected_path:
            QMessageBox.warning(self, "提示", "请先选择文件或文件夹！")
            return

        # 新增：获取用户输入的大小阈值（处理空值）
        user_size = 0
        if self.le_size.text().strip():
            try:
                user_size = int(self.le_size.text().strip())
            except ValueError:
                QMessageBox.warning(self, "提示", "大小阈值请输入有效整数！")
                return

        self.btn_calc.setDisabled(True)
        self.btn_calc.setText("计算中...")
        QApplication.processEvents()

        # 新增：日志输出用户输入的阈值
        self.append_log(f"📌 开始统计文件/文件夹大小（阈值：{user_size} 字节）...")
        self.append_log("📌 开始统计文件/文件夹大小...")

        try:
            self.size_thread = FileSizeThread(self.selected_path,user_size)
            self.size_thread.log_signal.connect(self.append_log)
            self.size_thread.finish_signal.connect(self.on_calc_finish)
            self.size_thread.start()
        except Exception as e:
            self.append_log(f"❌ 线程启动失败：{str(e)}")
            self.ensure_btn_enabled()

    def on_calc_finish(self, success, msg):
        """计算完成回调"""
        self.btn_calc.setDisabled(False)
        self.btn_calc.setText("判断大小")
        QApplication.processEvents()

        if success:
            self.append_log(f"🎉 统计完成：{msg}")
            QMessageBox.information(self, "成功", msg)
        else:
            self.append_log(f"❌ 统计失败：{msg}")
            QMessageBox.critical(self, "失败", msg)

    def ensure_btn_enabled(self):
        """兜底恢复按钮"""
        if self.btn_calc.isDisabled():
            self.btn_calc.setDisabled(False)
            self.btn_calc.setText("判断大小")
            QApplication.processEvents()


#智能闹钟工具页面
class SmartAlarmPage(QWidget):
    """智能闹钟工具页面"""

    def __init__(self):
        super().__init__()
        self.alarm_thread = None
        self.alarm_active = False
        # 初始化语音播报
        from pyttsx3_tts import TtsAlarmThread
        self.ttsThread=TtsAlarmThread
        self.init_ui()



    def init_ui(self):
        self.setStyleSheet(PAGE_STYLE)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        # 1. 标题 + 功能介绍
        title_group = QWidget()
        title_layout = QVBoxLayout(title_group)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setAlignment(Qt.AlignCenter)

        page_title = QLabel("智能闹钟工具")
        page_title.setFont(TITLE_FONT)
        page_title.setStyleSheet("color: black; margin-bottom: 8px;")
        page_title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(page_title)

        page_desc = QLabel("""
                功能说明：设置指定时间的闹钟提醒，支持自定义提醒内容，到点自动弹窗提示。
                使用步骤：1.设置年月日时分 → 2.输入提醒内容 → 3.点击确定闹钟 → 4.等待提醒（可终止）
                """)
        page_desc.setFont(DESC_FONT)
        page_desc.setWordWrap(True)
        page_desc.setStyleSheet("color: #333333; line-height: 1.4;")
        page_desc.setAlignment(Qt.AlignCenter)
        page_desc.setMaximumWidth(800)
        title_layout.addWidget(page_desc)

        main_layout.addWidget(title_group)

        # 2. 闹钟设置区域
        alarm_group = QGroupBox("闹钟设置")
        alarm_group.setStyleSheet("""
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
        alarm_layout = QVBoxLayout(alarm_group)
        alarm_layout.setSpacing(20)
        alarm_layout.setContentsMargins(10, 10, 10, 10)
        alarm_layout.setAlignment(Qt.AlignCenter)

        # 时间输入网格 - 核心修改：减小控件间距，调整输入框宽度
        time_grid = QWidget()
        time_grid_layout = QGridLayout(time_grid)
        time_grid_layout.setSpacing(0)  # 先重置全局间距
        time_grid_layout.setContentsMargins(0, 0, 0, 0)
        time_grid_layout.setAlignment(Qt.AlignCenter)

        now = datetime.datetime.now()
        year, month, day = now.year, now.month, now.day
        hour, minute = now.hour, now.minute

        # 年：标签与输入框紧贴，输入框与月标签间距加大
        lbl_year = QLabel("年：")
        lbl_year.setFont(DESC_FONT)
        self.le_year = QLineEdit(str(year))
        self.le_year.setFixedWidth(60)
        self.le_year.setFont(DESC_FONT)
        self.le_year.setValidator(QIntValidator(2000, 2100))
        time_grid_layout.addWidget(lbl_year, 0, 0)
        time_grid_layout.addWidget(self.le_year, 0, 1)
        time_grid_layout.setColumnMinimumWidth(2, 240)  # 年输入框与月标签之间加20px空白

        # 月：
        lbl_month = QLabel("月：")
        lbl_month.setFont(DESC_FONT)
        self.le_month = QLineEdit(str(month))
        self.le_month.setFixedWidth(60)
        self.le_month.setFont(DESC_FONT)
        self.le_month.setValidator(QIntValidator(1, 12))
        time_grid_layout.addWidget(lbl_month, 0, 3)
        time_grid_layout.addWidget(self.le_month, 0, 4)
        time_grid_layout.setColumnMinimumWidth(5, 240)  # 月输入框与日标签之间加20px空白

        # 日：
        lbl_day = QLabel("日：")
        lbl_day.setFont(DESC_FONT)
        self.le_day = QLineEdit(str(day))
        self.le_day.setFixedWidth(60)
        self.le_day.setFont(DESC_FONT)
        self.le_day.setValidator(QIntValidator(1, 31))
        time_grid_layout.addWidget(lbl_day, 0, 6)
        time_grid_layout.addWidget(self.le_day, 0, 7)

        # 时：
        lbl_hour = QLabel("时：")
        lbl_hour.setFont(DESC_FONT)
        self.le_hour = QLineEdit(str(hour))
        self.le_hour.setFixedWidth(60)
        self.le_hour.setFont(DESC_FONT)
        self.le_hour.setValidator(QIntValidator(0, 23))
        time_grid_layout.addWidget(lbl_hour, 1, 0)
        time_grid_layout.addWidget(self.le_hour, 1, 1)
        time_grid_layout.setColumnMinimumWidth(2, 240)  # 时输入框与分标签之间加20px空白

        # 分：
        lbl_minute = QLabel("分：")
        lbl_minute.setFont(DESC_FONT)
        self.le_minute = QLineEdit(str(minute))
        self.le_minute.setFixedWidth(60)
        self.le_minute.setFont(DESC_FONT)
        self.le_minute.setValidator(QIntValidator(0, 59))
        time_grid_layout.addWidget(lbl_minute, 1, 3)
        time_grid_layout.addWidget(self.le_minute, 1, 4)

        alarm_layout.addWidget(time_grid)

        # 提醒内容输入框（保留之前的宽度优化，仅调整间距）
        content_row = QWidget()
        content_row_layout = QHBoxLayout(content_row)
        content_row_layout.setSpacing(2)  # 提醒内容标签与输入框间距缩小为5px
        content_row_layout.setAlignment(Qt.AlignCenter)

        lbl_content = QLabel("提醒内容：")
        lbl_content.setFont(DESC_FONT)
        content_row_layout.addWidget(lbl_content)

        self.le_content = QLineEdit()
        self.le_content.setFixedWidth(550)  # 再增大输入框宽度
        self.le_content.setFont(DESC_FONT)
        self.le_content.setPlaceholderText("请输入闹钟提醒内容（如：开会、喝水、休息）")
        content_row_layout.addWidget(self.le_content)

        alarm_layout.addWidget(content_row)

        main_layout.addWidget(alarm_group)

        # 3. 操作按钮区域
        btn_row = QWidget()
        btn_row_layout = QHBoxLayout(btn_row)
        btn_row_layout.setSpacing(20)
        btn_row_layout.setAlignment(Qt.AlignCenter)
        btn_row_layout.setContentsMargins(0, 0, 0, 0)

        # 确定闹钟按钮
        self.btn_set_alarm = QPushButton("确定闹钟")
        self.btn_set_alarm.setFixedSize(120, 40)
        self.btn_set_alarm.setFont(QFont("微软雅黑", 12, QFont.Bold))
        self.btn_set_alarm.setStyleSheet("""
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
                background-color: #95A5A6;
                color: #EEEEEE;
                border: 1px solid #7F8C8D;
                cursor: not-allowed;
            }
        """)
        self.btn_set_alarm.clicked.connect(self.set_alarm)
        btn_row_layout.addWidget(self.btn_set_alarm)

        # 终止闹钟按钮
        self.btn_stop_alarm = QPushButton("终止闹钟")
        self.btn_stop_alarm.setFixedSize(120, 40)
        self.btn_stop_alarm.setFont(QFont("微软雅黑", 12, QFont.Bold))
        self.btn_stop_alarm.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
            QPushButton:disabled {
                background-color: #95A5A6;
                color: #EEEEEE;
                border: 1px solid #7F8C8D;
                cursor: not-allowed;
            }
        """)
        self.btn_stop_alarm.clicked.connect(self.stop_alarm)
        self.btn_stop_alarm.setDisabled(True)  # 默认禁用
        btn_row_layout.addWidget(self.btn_stop_alarm)

        main_layout.addWidget(btn_row)

        # 4. 日志输出框
        log_group = QGroupBox("闹钟日志")
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

    def append_log(self, msg):
        """追加日志"""
        from datetime import datetime
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        full_msg = f"{timestamp} {msg}"

        QMetaObject.invokeMethod(
            self.log_text,
            "append",
            Qt.QueuedConnection,
            Q_ARG(str, full_msg)
        )
        QMetaObject.invokeMethod(
            self.log_text.verticalScrollBar(),
            "setValue",
            Qt.QueuedConnection,
            Q_ARG(int, self.log_text.verticalScrollBar().maximum())
        )

    def set_alarm(self):
        """设置闹钟"""
        # 校验输入
        try:
            year = int(self.le_year.text())
            month = int(self.le_month.text())
            day = int(self.le_day.text())
            hour = int(self.le_hour.text())
            minute = int(self.le_minute.text())
            content = self.le_content.text().strip() or ""
        except ValueError:
            QMessageBox.warning(self, "提示", "请输入有效的年月日时分！")
            return

        # 校验日期合法性
        try:
            alarm_time = datetime.datetime(year, month, day, hour, minute)
        except ValueError:
            QMessageBox.warning(self, "提示", "输入的日期时间不合法！")
            return

        # 校验时间是否在未来
        now = datetime.datetime.now()
        if alarm_time < now:
            reply = QMessageBox.question(
                self,
                "提示",
                "设置的时间已过去，是否继续？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        # 启动闹钟线程
        self.alarm_active = True
        self.btn_set_alarm.setDisabled(True)
        self.btn_stop_alarm.setDisabled(False)
        self.append_log(f"📌 闹钟已启动，将在 {alarm_time.strftime('%Y-%m-%d %H:%M')} 触发！")
        self.append_log(f"📝 语音提醒内容：{content}")

        self.alarm_thread = AlarmThread(alarm_time, content)
        self.alarm_thread.log_signal.connect(self.append_log)
        self.alarm_thread.finish_signal.connect(self.on_alarm_finish)
        self.alarm_thread.start()

    def stop_alarm(self):
        """终止闹钟"""
        if self.alarm_active and self.alarm_thread:
            self.alarm_active = False
            self.alarm_thread.terminate()
            self.btn_set_alarm.setDisabled(False)
            self.btn_stop_alarm.setDisabled(True)
            self.append_log("🛑 已终止当前闹钟")
            QMessageBox.information(self, "提示", "已终止当前闹钟！")

    def on_alarm_finish(self, is_triggered, msg,alarm_context):
        """闹钟完成回调"""
        self.alarm_active = False
        self.btn_set_alarm.setDisabled(False)
        self.btn_stop_alarm.setDisabled(True)

        if is_triggered:
            self.append_log(f"⏰ {msg}")

            report_thread = threading.Thread(target=self.ttsThread.tts_run,args=(alarm_context, 60), daemon=True)
            self.ttsThread.start(report_thread)
            # 弹窗提醒
            reply =QMessageBox.information(
                self,
                "闹钟提醒",
                f"{msg}\n\n提醒内容：{self.le_content.text().strip() or '无提醒内容'}",
                QMessageBox.Ok
            )
            if reply == QMessageBox.Ok:
                self.ttsThread.stop()
        else:
            self.append_log(f"❌ {msg}")

#===========================线程=============================
#视频提取线程
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
                print(f"=== 线程开始执行 ===")
                # 发射信号
                self.log_signal.emit("⏳ 正在提取帧（请稍候）...")
                # result, msg = True,"success"
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

#图片去重线程
class ImageDedupThread(QThread):
    """图片去重线程"""
    log_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(bool, str)

    def __init__(self, folder_path, is_delete_dup):
        super().__init__()
        self.folder_path = folder_path
        self.is_delete_dup = is_delete_dup

    #核心去重逻辑
    def find_duplicates(self):
        from duplicates_photo import del_file, get_image_phash, get_file_md5
        md5_dict = {}
        phash_dict = {}

        # 总共满足的图片个数
        conform_count = 0
        # 删除个数
        del_count = 0
        # 重复或相似个数
        dup_count = 0
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    conform_count = conform_count + 1
                    path = os.path.join(root, file)
                    try:
                        # 第一层：MD5快速比对
                        file_md5 = get_file_md5(path)
                        if file_md5 in md5_dict:
                            dup_count = dup_count + 1
                            # print(f'完全重复文件: {path} <=> {md5_dict[file_md5]}')
                            self.log_signal.emit(f'完全重复文件: {path} <=> {md5_dict[file_md5]}')
                            if self.is_delete_dup:
                                del_count = del_count + 1
                                del_file(path)
                            continue

                        # 第二层：感知哈希比对
                        img_phash = get_image_phash(path)
                        for existing_phash in phash_dict:
                            if img_phash - existing_phash < 5:  # 汉明距离阈值
                                dup_count = dup_count + 1
                                # print(f'相似图片: {path} ≈ {phash_dict[existing_phash]}')
                                self.log_signal.emit(f'相似图片: {path} ≈ {phash_dict[existing_phash]}')
                                if self.is_delete_dup:
                                    del_count = del_count + 1
                                    del_file(path)
                                break
                        else:
                            phash_dict[img_phash] = path
                        md5_dict[file_md5] = path
                    except Exception as e:
                        print(f'处理失败 {path}: {str(e)}')
                        self.finish_signal.emit(False, f"去重异常：{str(e)}")
        if self.is_delete_dup and dup_count > 0:
            self.finish_signal.emit(True,
                               f"去重完成！满足条件的图片共 {conform_count}张， 共检测到 {dup_count + 1} 张重复图片，已删除 {dup_count} 张，保留1张")
        elif dup_count > 0:
            self.finish_signal.emit(True,
                               f"去重完成！满足条件的图片共 {conform_count}张，共检测到 {dup_count + 1} 张重复图片（未删除）")
        else:
            self.finish_signal.emit(True, f"去重完成！满足条件的图片共 {conform_count}张， 未检测到重复图片")

    def run(self):
        try:
            # 模拟去重流程
            self.log_signal.emit("🔍 正在检测文件夹内的png、jpg、jpeg重复图片")
            self.find_duplicates()
        except Exception as e:
            self.finish_signal.emit(False, f"去重异常：{str(e)}")

#文件大小线程
class FileSizeThread(QThread):
    """文件大小统计线程"""
    log_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(bool, str)

    def __init__(self, path,user_size):
        super().__init__()
        self.path = path
        self.user_size = user_size  # 接收用户输入的大小阈值

    def run(self):
        try:
            from file_size import calculate_path_size

            # 检查路径是否存在
            if not os.path.exists(self.path):
                print(f"❌ 路径不存在: {self.path}")
                self.finish_signal.emit(False,f"❌ 路径不存在: {self.path}")
                return

            self.log_signal.emit(f"程序处理中，请稍后...")
            result = calculate_path_size(self.path, True, self.user_size)

            if os.path.isfile(self.path):
                self.finish_signal.emit(True, f"文件 {os.path.basename(self.path)} 大小：{result}")
            else:
                self.finish_signal.emit(True, f"文件夹 {self.path} 总大小：{result}")
        except Exception as e:
            self.finish_signal.emit(False, f"统计异常：{str(e)}")

#闹钟线程
class AlarmThread(QThread):
    """闹钟线程"""
    log_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(bool, str, str)  # is_triggered, msg,alarm_context

    def __init__(self, alarm_time, content):
        super().__init__()
        self.alarm_time = alarm_time
        self.content = content

    def run(self):
        try:
            alarm_time_str = self.alarm_time.strftime("%Y-%m-%d %H:%M")
            from alarm_clock import run_clock

            result=run_clock(alarm_time_str)
            if result:
                self.finish_signal.emit(True,f"【闹钟触发】已到设置时间：{alarm_time_str}！语音内容：{self.content}",self.content)
            else:
                self.finish_signal.emit(False, f"闹钟任务执行异常!",self.content)
        except Exception as e:
            self.finish_signal.emit(False, f"闹钟异常：{str(e)}",self.content)

# ====================== 主窗口（复用逻辑） ======================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.video_menu_expanded = False
        self.image_menu_expanded = False
        self.other_menu_expanded = False  # 新增其他工具菜单展开状态
        self.current_selected_btn = None
        self.all_menu_btns = []
        self.init_main_ui()

    def init_main_ui(self):
        self.setWindowTitle("多媒体工具集")
        self.setGeometry(100, 100, 1100, 700)
        self.setMinimumSize(900, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 左侧菜单栏
        left_menu_widget = QWidget()
        left_menu_widget.setStyleSheet("background-color: #2C3E50;")
        left_menu_widget.setFixedWidth(200)
        self.left_layout = QVBoxLayout(left_menu_widget)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(0)
        self.left_layout.setAlignment(Qt.AlignTop)

        # 首页菜单
        self.home_btn = self.create_main_menu_btn("首页")
        self.home_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.home_page),
            self.set_selected_btn(self.home_btn)
        ])
        self.left_layout.addWidget(self.home_btn)
        self.all_menu_btns.append(self.home_btn)

        # 视频菜单组
        self.video_btn = self.create_main_menu_btn("视频 ▼")
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

        # 图片菜单组
        self.image_btn = self.create_main_menu_btn("图片 ▼")
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

        # 新增：其他工具菜单组
        self.other_btn = self.create_main_menu_btn("其他工具 ▼")
        self.other_btn.clicked.connect(self.toggle_other_submenu)
        self.left_layout.addWidget(self.other_btn)
        self.all_menu_btns.append(self.other_btn)

        # 其他工具二级菜单容器
        self.other_submenu_widget = QWidget()
        self.other_submenu_layout = QVBoxLayout(self.other_submenu_widget)
        self.other_submenu_layout.setContentsMargins(20, 0, 0, 0)
        self.other_submenu_layout.setSpacing(0)

        # 其他工具二级菜单-文件大小工具
        self.file_size_btn = self.create_sub_menu_btn("文件大小工具")
        self.file_size_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.file_size_page),
            self.set_selected_btn(self.file_size_btn)
        ])
        self.other_submenu_layout.addWidget(self.file_size_btn)
        self.all_menu_btns.append(self.file_size_btn)

        # 其他工具二级菜单-智能闹钟工具
        self.alarm_btn = self.create_sub_menu_btn("智能闹钟工具")
        self.alarm_btn.clicked.connect(lambda: [
            self.stacked_widget.setCurrentWidget(self.alarm_page),
            self.set_selected_btn(self.alarm_btn)
        ])
        self.other_submenu_layout.addWidget(self.alarm_btn)
        self.all_menu_btns.append(self.alarm_btn)

        self.other_submenu_widget.setVisible(False)
        self.left_layout.addWidget(self.other_submenu_widget)

        # 填充空白
        self.left_layout.addStretch()

        # 右侧内容区
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #ECF0F1;")

        # 注册所有页面
        self.home_page = HomePage()
        self.video_frame_page = VideoFrame2PicPage()
        self.video_other_page = VideoOtherToolsPage()
        self.image_dedup_page = ImageDeduplicationPage()
        self.image_process_page = ImageProcessPage()
        self.file_size_page = FileSizeToolPage()  # 新增文件大小页面
        self.alarm_page = SmartAlarmPage()        # 新增智能闹钟页面

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.video_frame_page)
        self.stacked_widget.addWidget(self.video_other_page)
        self.stacked_widget.addWidget(self.image_dedup_page)
        self.stacked_widget.addWidget(self.image_process_page)
        self.stacked_widget.addWidget(self.file_size_page)
        self.stacked_widget.addWidget(self.alarm_page)

        # 组装布局
        main_layout.addWidget(left_menu_widget)
        main_layout.addWidget(self.stacked_widget)

        # 默认选中首页
        self.set_selected_btn(self.home_btn)
        self.stacked_widget.setCurrentWidget(self.home_page)

    def create_main_menu_btn(self, text):
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
        self.video_menu_expanded = not self.video_menu_expanded
        self.video_submenu_widget.setVisible(self.video_menu_expanded)
        self.video_btn.setText("视频 ▲" if self.video_menu_expanded else "视频 ▼")
        if self.video_menu_expanded and not any([self.video_frame_btn.isChecked(), self.video_other_btn.isChecked()]):
            self.set_selected_btn(self.video_btn)

    def toggle_image_submenu(self):
        self.image_menu_expanded = not self.image_menu_expanded
        self.image_submenu_widget.setVisible(self.image_menu_expanded)
        self.image_btn.setText("图片 ▲" if self.image_menu_expanded else "图片 ▼")
        if self.image_menu_expanded and not any([self.image_dedup_btn.isChecked(), self.image_process_btn.isChecked()]):
            self.set_selected_btn(self.image_btn)

    # 新增：其他工具菜单展开/收起
    def toggle_other_submenu(self):
        self.other_menu_expanded = not self.other_menu_expanded
        self.other_submenu_widget.setVisible(self.other_menu_expanded)
        self.other_btn.setText("其他工具 ▲" if self.other_menu_expanded else "其他工具 ▼")
        if self.other_menu_expanded and not any([self.file_size_btn.isChecked(), self.alarm_btn.isChecked()]):
            self.set_selected_btn(self.other_btn)

    def set_selected_btn(self, target_btn):
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