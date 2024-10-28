from datetime import datetime

import pytest
import requests

data = {"passed": 0, "failed": 0}


def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == "call":
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    data["total"] = len(session.items)


def pytest_configure():
    # 配置文件加载完毕之后执行此方法、测试用例执行之前执行此方法
    data["start_time"] = datetime.now()
    print(f"{datetime.now()} 开始执行测试用例")


def pytest_unconfigure():
    # 测试用例执行完之后执行此方法
    data["end_time"] = datetime.now()
    print(f"{datetime.now()} 测试结束")
    data["duration"] = data["end_time"] - data["start_time"]
    print(data["duration"])

    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=006e8508-0f9d-4cdf-8be0-397968990e6f"

    content = f"""
    自动化测试结果

    测试时间：{data["end_time"]}
    测试用例：{data["total"]}
    执行时长：{data["duration"]}
    通过数量：<font color = "green">{data["passed"]}</font>
    失败数量：<font color = "red">{data["failed"]}</font>

    测试报告地址：www.baidu.com

    """

    requests.post(url, json={"msgtype": "markdown", "markdown": {"content": content}})
