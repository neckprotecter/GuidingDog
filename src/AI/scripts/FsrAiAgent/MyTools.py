#! /home/fsr/anaconda3/envs/yolo/bin python3
from datetime import datetime
from langchain.agents import tool, load_tools, Tool
import os
import rospy
from geometry_msgs.msg import Twist

@tool
def get_word_length_op(word: str) -> int:
    """input a word Returns the length of a word."""
    return len(word)

from datetime import datetime
# first tool to get time
@tool(return_direct=True)
def get_current_time_op(format: str) -> str: 
    """Input a format and Returns the current time in the specified format.
    Format can be one of the following values: iso, rfc, local """ 
    print(format)
    if format == "iso": 
        return datetime.now().isoformat() 
    elif format == "rfc": 
        return datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z") 
    elif format == "local": 
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    else:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        # return "Invalid format"


# 机械狗工具定义
@tool
def Robot_GoForward(planTime: str) -> None:
    """输入一个时间planTime, 控制机器狗向前走planTime秒"""
    result = ""
    for char in planTime:
        if char.isdigit():
            result += char
    print(rf"result: {result}")
    # """Control the robot to move forward for planTime seconds"""
    plan_time =int(result)
    print("plan_time: ", plan_time)
    try:
        rospy.init_node('robot_retreat_node')
    except rospy.ROSInitException as e:
        print(f"Failed to initialize ROS node: {e}")
    print("000\n")
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    print("111\n")
    rate = rospy.Rate(500)  # 500Hz
    twist = Twist()
    twist.linear.x = 0.5  # 设置线速度为正值，表示向前
    start_time = rospy.Time.now().to_sec()
    while (rospy.Time.now().to_sec() - start_time) < plan_time:
        pub.publish(twist)
        rate.sleep()
    twist.linear.x = 0.0
    pub.publish(twist)
    print(f"Moving forward for {plan_time} seconds.")
    # os.system(rf'/home/unitree/Documents/opsLab/Go1_Control/bins/Go1_Control {50*int(result)}')
    # if final == 0:
    #     return True
    # else: return False

@tool
def Robot_Retreat(planTime: str) -> None:
    """输入一个数字时间planTime, 控制机器狗后退planTime秒"""
    result = ""
    for char in planTime:
        if char.isdigit():
            result += char
    print(rf"result: {result}")
    # """Control the robot to move forward for planTime seconds"""
    plan_time =int(result)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(500)  # 500Hz
    twist = Twist()
    twist.linear.x = -0.5  # 设置线速度为正值，表示向前
    start_time = rospy.Time.now().to_sec()
    while (rospy.Time.now().to_sec() - start_time) < plan_time:
        pub.publish(twist)
        rate.sleep()
    # 停止机器人
    twist.linear.x = 0.0
    pub.publish(twist)
    print(f"Retreating for {plan_time} seconds.")

    # os.system(rf'/home/unitree/Documents/opsLab/Go1_Control/bins/backward {50*int(result)}')
    # if final == 0:
    #     return True
    # else: return False
    
@tool
def PlayMusic(planTime: str) -> None:
    """输入一个时间planTime, 就可以播放本地音乐"""
    result = ""
    for char in planTime:
        if char.isdigit():
            result += char
    print(rf"result: {result}")
    # """Control the robot to move forward for planTime seconds"""
    os.system(rf'open /Users/oplin/Music/网易云音乐/我没意见.wav')
    # if final == 0:
    #     return True
    # else: return False


#TODO 以下是更规范的工具定义方式
from pydantic.v1 import BaseModel, Field
# 函数定义
def get_time(format: str) -> str:
    print(format)
    if format == "iso": 
        return datetime.now().isoformat() 
    elif format == "rfc": 
        return datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z") 
    elif format == "local": 
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    else:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 


time_tool = Tool(
    name="GetTimeNow",
    description="向工具内输入一个字符串format, 工具会返回对应格式的当前时间, 字符串format的值可以是[iso, rfc, local]中的其中一种.",
    func=get_time
)

#TODO 以下是更更规范的工具定义方式

# Chinese 工具
class TimeInputFormat(BaseModel):
    format: str = Field(default="local", 
                        description="返回的时间的格式,值可以是:'iso', 'rfc', or 'local'.",
                        enum=["iso", "rfc", "local"])

@tool(args_schema=TimeInputFormat)
def getTime(format: str) -> str:
    """输入一个格式,然后会返回这个格式的当前时间.格式的值可以是:iso, rfc, or local. 
    """
    if format == "iso": 
        return datetime.now().isoformat() 
    elif format == "rfc": 
        return datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z") 
    else: 
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
