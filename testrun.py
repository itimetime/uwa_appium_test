# coding:utf-8
import pytest
from tools.read_case import read_test_case
import allure
import os
from multiprocessing import Process
from tools import folder_check, appium_operata
from tools.logger import logger
from core_operations.driver_operate import DriverOperate


@allure.feature('在理APP测试')
class TestClass(object):
    case = read_test_case()
    head = []
    result_dict = {}
    id = None
    operator = None

    def setup_class(self):
        # 检查各文件夹是否存在，防止运行报错。
        folder_check.Floder_check()
        # 初始配置加载 如果存在即加载，不存在使用默认配置。
        logger.info("加载配置，并连接手机...")
        if "setting1" in self.case[0]["actions"].keys():
            self.operator = DriverOperate(self.case[0]["actions"]["setting1"][0])
        else:
            self.operator = DriverOperate()
        self.driver = self.operator.get_driver()
        self.result_dict = {}

    def teardown_class(self):
        os.system("allure generate ./allure_data -o ./allure-report --clean")
        self.driver.quit()


    @pytest.mark.parametrize("case", case)
    def test_run(self, case):
        logger.info(f"执行测试用例{case}")
        case_id = case["ID"]
        description = case["DESCRIPTION"]
        operations = case["actions"]
        assertion = case["assert"]
        allure.title(description)
        # 执行操作过程
        try:
            self.operator.operation_execute(operations)
            self.operator.get_screenshot(description, True)
        except Exception as e:
            self.operator.get_screenshot(description + "执行错误", False)
            logger.error(f"{case_id}执行错误，错误原因{e}")
            pytest.fail(f"本地case_id:{case_id}-{description}, {e}, 当前操作: {operations}")
        # 执行断言过程
        real_value, expect_value = self.operator.value_assert(assertion)
        if real_value != expect_value:
            self.operator.get_screenshot(description + "断言错误", False)
            logger.error(f"本地case_id{case_id}断言错误:{real_value}, {expect_value}")
        with allure.step("assert"):
            allure.attach(str(assertion), "断言内容")
            assert real_value == expect_value, f"本地case_id{case_id}:{description}, {assertion}"

def py_run():
    pytest.main(["-s", "testrun.py", "--maxfail=3", "--alluredir=./allure_data"])
if __name__ == '__main__':
    # pytest.main(["-s", "testrun.py", "--maxfail=3", "--alluredir=./allure_data"])
    appium_task = Process(target=appium_operata.run_appium_server)
    pytest_task = Process(target=py_run)
    appium_task.start()
    pytest_task.start()
    pytest_task.join()
    appium_task.terminate()
    appium_operata.kill_appium_server()



