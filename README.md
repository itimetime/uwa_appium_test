# UWA—APPIUM自动化测试框架

#### 需要环境

```
配置Appium环境（JDK1.8+node+Android SDK）并安装Appium
安装Allure
python 3.6以上
```

#### 执行步骤

1. 把测试用例excel文件放到testcase目录下。

2. cd进项目目录，在命令行分别输入以下命令

   ```
   pip install -r requirements.txt  (只在首次运行的时候)
   python testrun.py
   ```

3. 执行后从allure-report中获取报告。

#### 目录结构

```
uwa-appium-test
│  requirements.txt  - python依赖库
│  testrun.py   - 程序入口       
│─allure-report - 报告目录
│─allure-report - allure测试结果目录
├─config  - 配置文件目录
│  └─  config.py   -  配置文件
│ 
├─core_operations - 核心功能目录
│  └─  driver_operate.py - 浏览器核心操作
│
├─logs   - 日志目录      
├─screenshots - 截图目录
├─screenshots-error  - 失败用例截图目录
├─testcase  - 测试用例存放目录
│   └─ case.xlsx
│
└─tools  - 辅助脚本
   ├─appium_operata.py  - Appium启动脚本
   ├─folder_check.py  - 判断目录结构脚本
   ├─keycode_parse.py - 安卓keycode解析脚本
   ├─logger.py  - 日志模块
   └─ read_case.py - 测试用例读取脚本
```

#### 测试用例相关书写方法

##### 操作方法

| 方法名      | 值                                                           | 说明                                                         |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| setting     | {"appPackage":"com.uwa.mproduct"}                            | 可设置应用启动的参数，没有填写将使用预设设置                 |
| background  | 3                                                            | 设置后台驻留，值为秒数                                       |
| click       | xpath`|`//`*`[@text  = '同意']//*[@text  = '同意']           | 元素点击，查找元素可以选择css、xpath、id、class_name         |
| send_keys   | class_name`|`android.widget.EditText`|`15692326910           | 发送数据，执行过程是查找元素和发送值                         |
| swipe_left  | 0.20`|`5                                                     | 手指向左划，第一个值代表x轴的20%的时候往左滑，第二个值代表滑动次数。 |
| swipe_right | 同上                                                         |                                                              |
| swipe_up    | 同上                                                         |                                                              |
| swipe_down  | 同上                                                         |                                                              |
| keycode     | 20                                                           | 输入安卓keycode，可模拟音量加减、返回等操作                  |

##### 断言方法

| 方法名        | 值                                   | 说明                                                       |
| ------------- | ------------------------------------ | ---------------------------------------------------------- |
| get_activity  | None                                 | 返回当前应用的activity，可判断应用是否能打开               |
| get_text      | class_name`|`android.widget.EditText | 查找元素，返回当前元素显示文本                             |
| get_attribute | xpath`|`//*[@index = 0]`|`scrollable | 获取Android元素的attribute，最后一个元素可跟id，text等元素 |

##### 更新说明

- allure报告可查看用例执行步骤。
- 用例用字典形式进行传递，拿掉eval()函数。
- allure appium命令进行封装，执行py文件即可启动相应的应用。

##### 其它说明

appium的一些封装断言方法，例如ele.is_enable,请用 get_attribute  xpath`|`//*[@index = 0]`|enable 代替 本质是一样的。

如排版不清楚，建议下载个markdown编辑器，推荐Typora。

