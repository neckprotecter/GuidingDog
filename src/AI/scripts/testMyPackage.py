#!/home/neck/anaconda3/envs/yolov5/bin/python
import os
import sys
import time
import rospy
from std_msgs.msg import String
from collections import defaultdict

from dashscope.audio.asr import Recognition, RecognitionCallback, RecognitionResult
import dashscope
import pyaudio

# 导入本地模块
path = os.path.abspath(".")
sys.path.insert(0, path + "/src/AI/scripts")
from FsrAiAgent import QwenAgent, ASRCallbackClass, TTS_Sambert

# 设置 DashScope API Key
dashscope.api_key = 'sk-b71cf16967404a158f01b02286b81fef'
os.environ["DASHSCOPE_API_KEY"] = 'sk-b71cf16967404a158f01b02286b81fef'

# 初始化语音识别与AI对话
mic = None
stream = None
myASR = ASRCallbackClass()
ai = QwenAgent()
ai.set_api_key("sk-b71cf16967404a158f01b02286b81fef")
ai.agent_conversation(with_memory=True)

# 初始化TTS语音播报函数
def speak_chinese(text):
    print("语音播报:", text)
    TTS_Sambert.TTSsaveTextResult(text)
    # os.system("aplay src/AI/scripts/FsrAiAgent/TTSoutput.wav")  # 可按需修改为你的输出语音文件名

# 保存识别类别和数量
latest_detected = defaultdict(int)
last_detection_time = 0  # 最近一次检测到的时间戳
detection_valid_duration = 2  # 数据有效期，单位秒

# ROS回调函数：处理检测结果并统计
def callback_ros_msg(msg):
    global latest_detected, last_detection_time
    content = msg.data.lower().split(',')
    latest_detected.clear()
    for item in content:
        item = item.strip()
        if item == 'red':
            latest_detected['红灯'] += 1
        elif item == 'green':
            latest_detected['绿灯'] += 1
        elif item == 'yellow':
            latest_detected['黄灯'] += 1
        elif item == 'car':
            latest_detected['有车'] += 1
        elif item in ('people', 'person'):
            latest_detected['有人'] += 1
    last_detection_time = time.time()  # 更新时间戳

# 生成播报用的语句
def generate_report_text():
    if time.time() - last_detection_time > detection_valid_duration:
        return None  # 超时则不播报
    if not latest_detected:
        return None
    report = []
    for k, v in latest_detected.items():
        report.append(f"{k}{v}个")
    return "，".join(report)

# 初始化 ROS 节点并订阅
rospy.init_node('voice_alert_node', anonymous=True)
rospy.Subscriber('/yolov5/detected_classes', String, callback_ros_msg)

# 初始化语音识别
recognition = Recognition(model='paraformer-realtime-v1', format='pcm', sample_rate=16000, callback=myASR)
recognition.start()

# 语音聊天初始化提示
ai.chat("请你扮演一个名叫'笨笨'的机器狗与我进行对话!我的身份是你的主人!而另一个名叫OPlin的人创造了你!接下来与我对话的过程中,你的回答应该尽量精简并控制在30字内!请你扮演好这个角色!")

# 主循环：处理语音识别、AI对话、ROS播报
lastASRresult = ''
last_report_time = time.time()
report_interval = 5  # 秒为单位，定时播报间隔
last_spoken_report = ''  # 上一次播报的内容，防止重复播报

try:
    while not rospy.is_shutdown():
        # 语音识别对话部分
        if myASR.stream:
            data = myASR.stream.read(3200, exception_on_overflow=False)
            recognition.send_audio_frame(data)
            if myASR.user_input != lastASRresult:
                lastASRresult = myASR.user_input
                print(rf"你说: {lastASRresult}")
                aiResponse = ai.chat(lastASRresult)
                TTS_Sambert.TTSsaveTextResult(aiResponse)
                # os.system("aplay src/AI/scripts/FsrAiAgent/TTSoutput.wav")

        # 定时播报识别结果（不播报过期的）
        if time.time() - last_report_time >= report_interval:
            last_report_time = time.time()
            report_text = generate_report_text()
            if report_text and report_text != last_spoken_report:
                speak_chinese(report_text)
                last_spoken_report = report_text

        rospy.sleep(0.1)

except KeyboardInterrupt:
    recognition.stop()




# #! /home/fsr/anaconda3/envs/yolo/bin python3
# from dashscope.audio.asr import Recognition, RecognitionCallback, RecognitionResult
# import dashscope
# import os
# import sys

# path = os.path.abspath(".")
# sys.path.insert(0, path + "/src/AI/scripts")

# from FsrAiAgent import QwenAgent, ASRCallbackClass, TTS_Sambert
# import pyaudio
# dashscope.api_key='sk-b71cf16967404a158f01b02286b81fef'
# os.environ["DASHSCOPE_API_KEY"] = 'sk-b71cf16967404a158f01b02286b81fef' # 填入dashscope的apikey, dashscope是阿里云的https://help.aliyun.com/zh/dashscope/developer-reference/install-dashscope-sdk
# mic = None
# stream = None


# myASR = ASRCallbackClass()
# ai = QwenAgent()
# ai.set_api_key("sk-b71cf16967404a158f01b02286b81fef")
# ai.agent_conversation(with_memory=True)


# recognition = Recognition(model='paraformer-realtime-v1', format='pcm', sample_rate=16000, callback=myASR)
# recognition.start()  # 开始语音识别，不再需要按键控制
# lastASRresult: str = ''
# try:
#     ai.chat("请你扮演一个名叫'笨笨'的机器狗与我进行对话!我的身份是你的主人!而另一个名叫OPlin的人创造了你!接下来与我对话的过程中,你的回答应该尽量精简并控制在30字内!请你扮演好这个角色!")
#     while True:
#         if myASR.stream:
#             data = myASR.stream.read(3200, exception_on_overflow=False)
#             recognition.send_audio_frame(data)
#             if myASR.user_input != lastASRresult:
#                 lastASRresult = myASR.user_input
#                 print(rf"你说: {lastASRresult}")
#                 aiResponse = ai.chat(lastASRresult)
#                 TTS_Sambert.TTSsaveTextResult(aiResponse)

                
        
# except KeyboardInterrupt:  # 使用Ctrl+C来退出程序
#     recognition.stop()



# # print(ai.prompt.template)