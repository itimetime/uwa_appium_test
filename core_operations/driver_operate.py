# -*- coding: utf-8 -*-
# @time    : 2020/5/18 18:00
# @author  : CK
# @file    : driver_init.py
import os
import time
import re
import json
from appium import webdriver
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction
from tools import keycode_parse
from tools.logger import logger
import allure
from config import config


class DriverOperate(object):
    def __init__(self, update_dict=None):
        # self.uwa_logger = logger.Logger().get_log()
        if update_dict is None:
            update_dict = {}
        desired_caps = dict()
        # 默认参数，可进行配置
        # 手机参数
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6'
        desired_caps['deviceName'] = '192.168.56.101:5555'
        # 应用参数
        desired_caps['appPackage'] = 'com.uwa.mproduct'
        desired_caps['appActivity'] = 'com.uwa.mproduct.MainActivity'
        # 重置应用
        desired_caps['noReset'] = False
        # 默认设置跳过服务安装
        desired_caps['skipServerInstallation'] = True
        desired_caps['skipDeviceInitialization'] = True
        # desired_caps["unicodeKeyboard"] = True
        # desired_caps["resetKeyboard"] = True
        desired_caps.update(json.loads(update_dict))
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


    def get_driver(self):
        self.driver.implicitly_wait(10)
        time.sleep(3)
        return self.driver

    # 此方法将执行用例的所有操作
    def operation_execute(self, operations):
        for key in operations.keys():
            # 执行操作
            operation = (re.search("\D+", key)).group(0)
            logger.info(f"{operation}:{operations[key]}")
            # 添加执行步骤
            with allure.step(operation):
                allure.attach(str(operations[key]), "操作参数")
                if operation == "click":
                    time.sleep(1)
                    operate_ele = self.find_element_uwa(operations[key][0], operations[key][1])
                    operate_ele.click()
                    time.sleep(5)

                # 发送值 两种方法，如果send_keys方法失败，将转换为keycode输入。
                elif operation == "send_keys":
                    operate_ele = self.find_element_uwa(operations[key][0], operations[key][1])
                    try:
                        operate_ele.send_keys(operations[key[2]])
                    except Exception as e:
                        operate_ele.click()
                        keycode_parse.send_keycode(self.driver, operations[key][2])
                # 后台驻留操作
                elif operation == "background":
                    self.driver.background_app(operations[key][0])
                elif operation == "swipe_left":
                    self.swipe(0.75, float(operations[key][0]), 0.25, float(operations[key][0]),
                               int(operations[key][1]))
                elif operation == "swipe_right":
                    self.swipe(0.25, float(operations[key][0]), 0.75, float(operations[key][0]),
                               int(operations[key][1]))
                elif operation == "swipe_down":
                    self.swipe(float(operations[key][0]), 0.30, float(operations[key][0]), 0.75,
                               int(operations[key][1]))
                elif operation == "swipe_up":
                    self.swipe(float(operations[key][0]), 0.75, float(operations[key][0]), 0.30,
                               int(operations[key][1]))
                elif operation == "new_activity":
                    self.driver.start_activity(operations[0], operations[1])
                elif operation == "keycode":
                    self.driver.press_keycode(int(operations[key][0]))

    def zoom(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        action1 = TouchAction(self.driver)
        action2 = TouchAction(self.driver)
        zoom_action = MultiAction(self.driver)
        action1.press(x=x * 0.4, y=y * 0.4).move_to(x=x * 0.1, y=y * 0.1).wait(500).release()
        action2.press(x=x * 0.6, y=y * 0.6).move_to(x=x * 0.8, y=y * 0.8).wait(500).release()
        print('start zoom...')
        zoom_action.add(action1, action2)
        zoom_action.perform()

    def pinch(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        action1 = TouchAction(self.driver)
        action2 = TouchAction(self.driver)
        pinch_action = MultiAction(self.driver)
        action1.press(x=x * 0.1, y=y * 0.1).move_to(x=x * 0.4, y=y * 0.4).wait(500).release()
        action2.press(x=x * 0.8, y=y * 0.8).move_to(x=x * 0.6, y=y * 0.6).wait(500).release()
        print("start pinch...")
        pinch_action.add(action1, action2)
        pinch_action.perform()



    # 编写测试用例的时候必须传入两个值，一、滑动位置（举例：上下滑动时，第一个值传入0.1将在屏幕左边滑动，0.8将从屏幕右边滑动）二 滑动次数

    def swipe(self, start_x, start_y, stop_x, stop_y, n):

        time.sleep(3)
        # 获取手机屏幕宽、高
        x = self.driver.get_window_size()["width"]
        y = self.driver.get_window_size()["height"]
        x1 = int(x * start_x)
        y1 = int(y * start_y)
        x2 = int(x * stop_x)
        y2 = int(y * stop_y)
        for i in range(n):
            self.driver.swipe(x1, y1, x2, y2)
            time.sleep(2)

    def value_assert(self, assertion):
        # try:
        checkpoint = assertion["checkpoint"]
        assert_ele = assertion["assert_element"]
        expect_value = assertion["expect_value"]
        with allure.step(checkpoint):
            allure.attach(str(assert_ele), "操作参数")
            if checkpoint == "get_activity":
                real_value =  self.driver.current_activity
            elif checkpoint == "get_text":
                by = assert_ele.split("|")[0]
                ele = assert_ele.split("|")[1]
                real_value = self.find_element_uwa(by,ele).text
            elif checkpoint == "get_attribute":
                by = assert_ele.split("|")[0]
                ele = assert_ele.split("|")[1]
                attribute_value = assert_ele.split("|")[2]
                real_value =  self.find_element_uwa(by, ele).get_attribute(attribute_value)
            else:
                real_value = None
        logger.info(f"进行断言,{real_value}?{expect_value}")
        return real_value, expect_value

    # 元素定位
    def find_element_uwa(self, by, value):
        if by == "class_name" or by == "By_CLASS_NAME":
            return self.driver.find_element_by_class_name(value)  # 类名定位
        elif by == "xpath" or by == "By.XPATH":
            return self.driver.find_element_by_xpath(value)  # 路径定位
        elif by == "css" or by == "By_CSS_SELECT":
            return self.driver.find_element_by_css_selector(value)  # css选择器定位
        elif by == "id" or by == "By_ID":
            return self.driver.find_element_by_id(value)  # id定位
        elif by == "link_text" or by == "By_LINK_TEXT":
            return self.driver.find_element_by_link_text(value)  # 链接名定位

        else:
            print("该方法还未添加，请检查用例编写或者测试框架配置")
            raise Exception("该方法还未添加，请检查用例编写或者测试框架配置")

    def find_elements_uwa(self, by, value, n):
        if by == "class_name" or by == "By_CLASS_NAME":
            return self.driver.find_elements_by_class_name(value)  # 类名定位
        elif by == "xpath" or by == "By.XPATH":
            return self.driver.find_elements_by_xpath(value)  # 路径定位
        elif by == "css" or by == "By_CSS_SELECT":
            return self.driver.find_elements_by_css_selector(value)  # css选择器定位
        elif by == "id" or by == "By_ID":
            return self.driver.find_elements_by_id(value)  # id定位
        elif by == "link_text" or by == "By_LINK_TEXT":
            return self.driver.find_elements_by_link_text(value)  # 链接名定位
        else:
            raise Exception("元素查找方法不存在，请检查用例编写或者测试框架配置")

    def get_screenshot(self, img_name, is_succeed):
        try:
            if is_succeed:
                img_folder = config.project_path + '//screenshots//'
            else:
                img_folder = config.project_path + '//screenshots-error//'
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            screen_save_path = img_folder + now_time + img_name + '.png'
            self.driver.get_screenshot_as_file(screen_save_path)
            if not is_succeed:
                with open(screen_save_path, 'rb') as f:
                    allure.attach(f.read(
                    ), img_name, attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            raise Exception(e)


if __name__ == '__main__':
    pass
