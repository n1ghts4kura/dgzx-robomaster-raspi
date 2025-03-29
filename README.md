# dgzx-robomaster-raspi
一个\*开源\*的RoboMaster*__树莓派__*主控仓库。  

An **_open-source_** robomaster controlling library
**by Team EOR from DGZX.**


## 一、项目解读

### （一）项目结构

- *__assets__* 文件夹
- * *__log__* 文件夹 存放日志文件  
- * *__skills_conf__* 文件 技能槽位配置 文件格式：`<技能1名称> <换行> <技能2名称> <...>`  

<br>

- *__modules__* 文件夹 存放模块
- * *__utils__* 文件夹 存放一些功能分类比较杂的模块
- * - *__logger.py__* 模块 日志   
<br>
- *__robot__* 文件夹 存放和机器人相关模块
- * *__robot.py__* 模块 机器人连接模块
- * *__robot_state.py__* 模块 机器人状态重置模块  
<br>
- *__skill__* 文件夹 存放技能相关模块
- * *__skill_manager.py__* 模块 技能管理类
<br>

<br>

- *__skills__* 文件夹 存放技能逻辑模块
- * __...__

<br>

- ___main.py___ 程序入口 ( _使用 `python3.7 main.py` 启动_ )

### （二）代码解读
> **略**。
>
> **详情可以自行看每个文件里面的注释。**
>
> 万分注意在**多线程**场景内，一定要注意不同线程对于同一资源的操作，无论是读取还是修改。
>
> 建议都给与多线程有关的资源加上**线程锁**。
>
> （虽然好像还没有出现这种场景。）


## 二、环境配置指南（未完篇）

### （一）系统选择
在系统选择上，选用树莓派官方提供的imager安装工具。选择 **Raspberry Pi OS (64-bit)版本** 来安装，以方便后续统一环境配置细节；是否使用桌面版可自行考虑。
至于VNC、SSH等问题不再进行讨论，可自行在网上搜寻相关资料。

### （二）Python / OpenCV安装

#### 0. 准备工作
>一定要做这一步，不然后面编译出问题都不知道怎么解决的说是。T_T
##### (1) 扩大sd卡可用空间
```sh
$ sudo raspi-config
```
然后选择 Advanced Options -> Expand Filesystem ...  ，随后重启。

##### (2) 扩大虚拟内存
``` sh
$ sudo nano /etc/dphys-swapfile
```
将 *CONF_SWAPSIZE* 修改为 **1024 * n** 。
>具体视自己sd卡容量大小为定，这里推荐 **2048**。
```sh
# 重启使修改生效
$ sudo /etc/init.d/dphy-swapfile restart
```

##### (3) 换源
**apt** 换源不再赘述。

#### 1. Python
> __记得换源。__

由于目前（2025）所使用的系统为Python3.11，所以我们需要额外安装一个低版本Python以与robomaster sdk需求契合。

```sh
sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install build-essentials libsqlite3-dev sqlite3 bzip2 libbz2-dev
```
> 这一步是在安装后面编译Python所需要的库。

```sh
# 先切换到用户根目录以便文件统一管理
# 下载Python源代码
$ cd ~
$ mkdir python_installation
$ cd python_installation
$ wget https://www.python.org/ftp/python/3.7.8/Python-3.7.8.tgz

# 然后解压源代码
$ tar xzvf Python-3.7.8.tgz
$ cd Python-3.7.8

# 编译
$ sudo ./configure
$ sudo make
$ sudo make install 
# 如果在编译过程中出现报错请自行解决 Q_Q

# 升级pip
$ sudo python3.7 -m pip install upgrade pip
```
此时我们已经安装好了python3.7，下一步安装OpenCV以及相关依赖，譬如摄像头等。

#### 2. OpenCV
仍然是安装依赖来开头。
```sh
$ sudo apt-get install cmake git pkg-config -y
$ sudo apt-get install libjpeg8-dev -y
# 若上一步报错可以根据报错信息具体解决，也可以参考下一行命令（请自行解决依赖问题）
# $ sudo apt-get install libjpeg62-turbo-dev libjpeg62-turbo-dev:arm64
$ sudo apt-get install libtiff5-dev -y
$ sudo apt-get install libjasper-dev -y
```
如果在上一步最后一行的指令出现报错，那么请移步**项目文件夹**创建虚拟环境再执行下方指令。
```sh
$ cd my-project # or dgzx-robomaster-raspi
# 更新pip
$ pip3.7 install --upgrade pip
$ python3.7 -m venv ./venv
$ source ./venv/bin/activate
$ pip3 install https://github.com/google-coral/pycoral/releases/download/v1.0.1/tflite_runtime-2.5.0-cp37-cp37m-linux-aarch64.whl
```
执行完毕后继续执行下方指令。
```sh
$ sudo apt-get install libpng12-dev -y
$ sudo apt-get install libavcodec-dev libacformat-dev libswscale-dev libv4l-dev -y
$ sudo apt-get install libgtk2.0-dev -y
$ sudo apt-get install libatlas-base-dev gfortran -y
```
然后开始OpenCV的编译。
