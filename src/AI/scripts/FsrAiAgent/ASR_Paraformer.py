#! /home/fsr/anaconda3/envs/yolo/bin python3
import os
import pyaudio
import time
from dashscope.audio.asr import RecognitionCallback, RecognitionResult
import colorama

# 初始化colorama
colorama.init(autoreset=True)

class ASRCallbackClass(RecognitionCallback):
    '''
    ASRCallbackClass 类定义了一个基于 RecognitionCallback 的回调类，用于处理语音识别器的打开、关闭事件以及识别结果的实时更新。
    - 在初始化时，设置麦克风和音频流对象为 None，并初始化存储识别文本、用户输入、唤醒词状态等相关变量。
    
    - `on_open` 方法在语音识别器打开时调用，初始化并启动音频流以接收麦克风输入。

    - `on_close` 方法在语音识别器关闭时调用，停止并关闭音频流，同时释放资源。

    - `on_event` 方法在识别器有新的识别结果时被调用。此方法主要处理识别出的文本内容，检查是否包含唤醒词，并根据唤醒状态截取有效用户输入。同时，它还实现了对控制台输出内容的动态更新与管理，包括清除已显示内容和限制最大字符显示数量。
    '''
    def __init__(self) -> None:
        super().__init__()
        self.mic = None
        self.stream = None
        self.asr_text: str = ''  # 用于存储识别出的文本
        self.max_chars: int = 50  # 最大字符限制
        self.clear_flag: bool = False  # 清除标志
        self.user_input: str = ''  # 用户输入
        self.awake_keyword = "你好"  # 唤醒词
        self.awoken = False  # 唤醒状态

    def on_open(self):
        """当语音识别器打开时调用"""
        print(colorama.Fore.GREEN + '语音识别器已打开。')
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=3200)

    def on_close(self):
        """当语音识别器关闭时调用"""
        print(colorama.Fore.RED + '语音识别器已关闭。')
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.mic.terminate()

    def on_event(self, result: RecognitionResult):
        """当语音识别器有事件发生时调用"""
        print(colorama.Fore.YELLOW + f"唤醒词 {self.awake_keyword}")
        sentence = result.get_sentence()
        is_end = result.is_sentence_end(sentence)
        if len(self.asr_text) > 0 or self.clear_flag:
            # \033[1A\033[K的作用是：
            # 首先将光标上移一行，然后清除那一行的内容。
            # 这个组合在命令行界面的动态输出中非常有用，例如在显示进度条或更新状态信息时，可以用它来重写当前行，而不是不断在终端中添加新行。
            print(colorama.Fore.CYAN + '\033[1A\033[K', end='')
            if self.clear_flag:
                self.clear_flag = False
                self.asr_text = ''
        self.asr_text = sentence['text']
        if not self.awoken and self.awake_keyword in self.asr_text:
            self.awoken = True
        if self.awoken:
            if is_end:
                # 这个用于规格化输入的语音, 使得唤醒词不会被当做输入一起进入agent.
                self.user_input = self.asr_text[self.asr_text.find(self.awake_keyword) + len(self.awake_keyword) + 1:]
                if len(self.asr_text) > self.max_chars:
                    self.clear_flag = True
                self.awoken = False  # 重置唤醒状态
