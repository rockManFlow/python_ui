# python_ui
基于python实现页面功能

可以实现通过页面直接调用对应的脚本程序

### python相关操作
创建虚拟环境 python -m venv python_ui_venv
激活虚拟环境 python_ui_venv\Scripts\activate
检测当前项目真实依赖自动检测生成 
pip install pipreqs
pipreqs ./ --encoding=utf8 --force --recursive(嵌套扫描子文件夹) 会生成在项目根目录生成依赖清单（requirements.txt）

### PyQt5实现页面
Qt Designer 可视化开发：
运行 designer.exe（Windows）/ designer（Linux）打开可视化编辑器，拖拽控件生成 .ui 文件；
通过 pyuic5 -x ui_file.ui -o ui_file.py 将 .ui 文件转为 Python 代码，直接集成到项目中，无需手写布局。

打包为可执行文件：用 PyInstaller 将代码打包为 exe（Windows）/app（Mac）/ 可执行文件（Linux），
无需安装 Python 环境即可运行：
![img.png](test/img.png)

注意：如果是虚拟环境，得在虚拟环境中进行安装pyinstaller，否则默认还是全局安装的这个包
pip install pyinstaller

示例
├── main.py          # 主GUI脚本
├── target_script.py # 被调用的目标脚本
├── icon.ico         # 图标文件
└── config.ini       # 配置文件（可选）

pyinstaller -F -w -i icon.ico -n "视频帧提取工具" ^
--add-data "target_script.py;." ^  # 将target_script.py打包到可执行文件同级目录
--add-data "config.ini;." ^        # 配置文件同理
main.py

示例1：
pyinstaller -D -w -i file_tool.ico -n "哈哈小工具" --add-data "target_2.py;" --clean refer_gui.py

示例2：打包成一个EXE文件
pyinstaller -F -w -i file_tool.ico 
--add-data "target_script.py;." 
--add-data "alarm_clock.py;." 
--clean   
--distpath exe_out  #指定输出存储路径
tool_gui.py

示例3：打包成文件夹
pyinstaller -D -w -i file_tool.ico --add-data "target_script.py;./python"  --add-data "alarm_clock.py;./python"  --add-data "pyttsx3_tts.py;./python" --add-data "file_size.py;./python" --add-data "duplicates_photo.py;./python" --clean   --distpath out tool_gui.py