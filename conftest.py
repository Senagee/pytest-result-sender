import logging
from datetime import datetime

import pytest
import requests

data = {"passed": 0, "failed": 0}


def pytest_addoption(parser: pytest.Parser):
    parser.addini(
        name="send_when",
        help="什么时候发送，on_fail：有失败的就发送/every任何时候都发送",
    )
    parser.addini(name="send_where", help="发送到什么位置")


def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == "call":
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    data["total"] = len(session.items)


def pytest_configure(config: pytest.Config):
    # 配置文件加载完毕之后执行此方法、测试用例执行之前执行此方法
    data["start_time"] = datetime.now()
    data["send_when"] = config.getini("send_when")
    data["send_where"] = config.getini("send_where")


def pytest_unconfigure():
    # 测试用例执行完之后执行此方法
    data["end_time"] = datetime.now()
    print(f"{datetime.now()} 测试结束")
    data["duration"] = data["end_time"] - data["start_time"]
    print(data["duration"])
    send_result()


def send_result():
    if data["send_when"] == "fail" and data["failed"] == 0:
        return
    if not data["send_when"] or data["send_where"]:
        logging.warning("未配置send_when或send_where")
        return
    url = data["send_where"]  # 动态指定发送位置
    content = f"""
    自动化测试结果

    测试时间：{data["end_time"]}
    测试用例：{data["total"]}
    执行时长：{data["duration"]}
    通过数量：<font color = "green">{data["passed"]}</font>
    失败数量：<font color = "red">{data["failed"]}</font>

    测试报告地址：www.baidu.com

    """
    try:
        requests.post(
            url, json={"msgtype": "markdown", "markdown": {"content": content}}
        )
    except Exception:
        pass
