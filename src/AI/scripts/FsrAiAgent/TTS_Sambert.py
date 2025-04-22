#! /home/fsr/anaconda3/envs/yolo/bin python3
from dashscope.audio.tts import SpeechSynthesizer
import os
import time
import dashscope
dashscope.api_key = '填入你的阿里云dashscope的api_key'

class TTS_Sambert():
    def TTSsaveTextResult(myText: str) -> bool: 
        """
        Input Text, the func will use DashScope TTS it and ave the result
        in the path which this file in.
        Success will return 1, else is 0
        """
        result = SpeechSynthesizer.call(model='sambert-zhimiao-emo-v1',
                                    text=myText,
                                    sample_rate=16000,
                                    rate=0.75,
                                    format='wav'
                                    )
        # # 记得改一下以下, 它们的作用是写入TTS输出的音频结果并播放
        if result.get_audio_data() is not None:
            with open(rf'./TTSoutput.wav', 'wb') as f:
                f.write(result.get_audio_data())
            os.system(rf"aplay ./TTSoutput.wav")
            return True
        else: return False