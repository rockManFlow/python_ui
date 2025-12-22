'''
pyttsx3 是最经典的离线 TTS 库，直接调用系统内置的语音引擎（Windows 用 SAPI5、macOS 用 NSSpeechSynthesizer、Linux 用 eSpeak），无需联网、无需安装额外语音模型，开箱即用。
优点：跨平台、轻量、响应快、支持语速 / 音量 / 语音类型调整；
缺点：语音合成效果偏机械（无情感），支持的语音类型依赖系统内置引擎；
适配系统：Windows（最佳）、macOS、Linux。
'''

'''
中文变体‌：

zh-CN：简体中文（中国大陆）
zh-TW：繁体中文（台湾）
zh-HK：繁体中文（香港）
zh-MO：繁体中文（澳门）
‌英语变体‌：

en-US：美式英语
en-GB：英式英语
en-CA：加拿大英语
en-AU：澳大利亚英语
‌其他语言‌：
fr-FR：法语（法国）
fr-CA：法语（加拿大）
de-DE：德语（德国）
ja-JP：日语（日本）
ko-KR：韩语（韩国）
'''
import pyttsx3
import sys

#打印当前系统支持的语音类型
def print_support_voices(engine):
    voices = engine.getProperty('voices')
    # 遍历可用语音
    for idx, voice in enumerate(voices):
        # 打印当前系统支持的所有语言包
        print(f"语音{idx}：{voice.name}，语言：{voice.languages}")
    # 切换语音（Windows 多语音支持，macOS/Linux 需系统有对应语音包）

    # 切换为中文语音（需系统安装中文语音包，Windows 自带）
    # engine.setProperty('voice', voices[0].id)  # 根据实际索引调整


#校验当前系统类型
def check_system()->str:
    print(f"当前系统 {sys.platform} ")
    if sys.platform.startswith('win'):
        print("当前系统是Windows")
        return 'win'
    elif sys.platform.startswith('linux'):
        print("当前系统是Linux")
        return 'linux'
    elif sys.platform.startswith('darwin'):
        print("当前系统是macOS")
        return "mac"
    else:
        print(f"无法识别当前系统 {sys.platform} ")
        return "un"

#验证OK，可直接播放
def tts_run(context='你好，这是测试'):
    # 初始化引擎
    engine = pyttsx3.init()

    # 1. 基础文字转语音（直接播放）
    engine.say(context)
    engine.say("Hello, this is an offline TTS test")
    engine.runAndWait()  # 阻塞直到语音播放完成

    # 2. 调整参数（语速、音量、语音类型）
    # 语速：默认200，范围0-500
    engine.setProperty('rate', 150)
    # 音量：默认1.0，范围0.0-1.0
    engine.setProperty('volume', 0.8)

    engine.say(context)
    engine.say("Hello, this is an offline TTS test")
    engine.runAndWait()  # 阻塞直到语音播放完成

    sys_type=check_system()
    if 'win'==sys_type :
        # 3. 保存语音到文件（仅 Windows 支持直接保存，Linux/macOS 需配合 ffmpy）
        engine.save_to_file("保存到文件的测试语音", "output.wav")
        engine.runAndWait()
    else:
        print("非win系统，不支持保存")

    # 关闭引擎
    engine.stop()

if __name__ == "__main__":
    tts_run()