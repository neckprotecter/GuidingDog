# 一键启动
- 克隆项目：
    ```shell
    git clone https://github.com/neckprotecter/GuidingDog.git
    ```
- 编译
    ```shell
    catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3
    ```
- 运行  
    ```shell
    source devel/setup.bash
    roslaunch guiding_dog run.launch
    ```

# 目标检测

## d435i相机
- 参考博客：https://blog.csdn.net/x3613389/article/details/120875669
- 安装ros包：
    ```shell
    sudo apt install ros-noetic-realsense2-camera
    sudo apt install ros-noetic-realsense2-description
    ```
- 更新环境：
    ```shell
    source ~/.bashrc
    source devel/setup.bash
    ```
- 测试使用：
    ```shell
    roslaunch realsense2_camera rs_camera.launch  # 启动相机
    roslaunch realsense2_camera demo_pointcloud.launch  # 点云deemo
    rqt_image_view  # rqt查看图像
    ```
- 话题查看：
    ```shell
    rostopic list
    ```

## yolov5模型
- 参考博客：https://blog.csdn.net/yangleikbd/article/details/127696119
- 安装yolov5_ros后，直接运行：```roslaunch yolov5_ros yolo_v5.launch```，会出现报错：```RuntimeError: Found no NVIDIA driver on your system. Please check that you have an NVIDIA GPU and installed a driver from http://www.nvidia.com/Download/index.aspx```  
    > 这是因为nuc上没有GPU，要修改yolo_v5.launch，将  
    ```<param name="use_cpu"           value="false" />```
    改为```<param name="use_cpu"           value="true" />```
    来调用CPU
- 简单修改要识别的类别classes的方法：通过命令行传参不方便的情况下，在 [detect.py](yolov5-master/detect.py) 文件的 248 行左右：
    ```    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')```
    修改为
    ```    parser.add_argument('--classes', nargs='+', type=int, default=[0, 49], help='filter by class: --classes 0, or --classes 0 2 3')```
    可以指定默认class值
    具体对应表根据使用的yaml来决定，默认是 [coco128.yaml](wksp/src/yolov5_ros/yolov5/data/coco128.yaml)

## 一键启动
- 修改 [yolo_v5.launch](src/Yolov5_ros/yolov5_ros/yolov5_ros/launch/yolo_v5.launch) 文件，增加：
    ```launch
    <!-- 启动 RealSense 相机 -->
    <include file="$(find realsense2_camera)/launch/rs_camera.launch" />
    ```
- 启动方法：
    ```shell
    source devel/setup.bash
    roslaunch yolov5_ros yolo_v5.launch
    ```

# 导航避障
- 克隆项目：
    ```shell
    git clone https://github.com/DedSecer/go1_navigation
    ```
- 更新子模块：
    ```shell
    cd go1_navigation
    git submodule update --init --recursive
    ```
- 安装depences  
  确保已安装并初始化 rosdep。如果遇到网络问题，请尝试使用 [rosdep](https://zhuanlan.zhihu.com/p/398754989)
    ```shell
    rosdep install --from-paths src --ignore-src -r -y 
    ```
- 编译
    ```shell
    # 在我使用的场景下，需要进入conda环境
    conda activate yolov5
    # 确保ROS使用conda环境里的python
    export PYTHONPATH=$CONDA_PREFIX/lib/python3.8/site-packages:$PYTHONPATH
    # 或者使用
    # catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3  
    catkin_make
    ```
- 运行  
  需要先对设备进行权限设置：
  ```shell
  sudo chmod 666 /dev/ttyUSB0
  ```
  然后运行roslaunch：
  ```shell
  roslaunch point_lio_unilidar mapping_move_base.launch
  ```

# 导航避障2