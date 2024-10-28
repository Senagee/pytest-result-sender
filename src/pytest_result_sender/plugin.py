from datetime import datetime, timedelta

import pytest

data = {}


@pytest.hookimpl(hookwrapper=True)
def pytest_collection_finish(session: pytest.Session):
    print(session.items)


@pytest.hookimpl(hookwrapper=True)
def pytest_configure():
    # 配置文件加载完毕之后执行此方法、测试用例执行之前执行此方法
    data["start_time"] = datetime.now()
    print(f"{datetime.now()} 开始执行测试用例")


@pytest.hookimpl(hookwrapper=True)
def pytest_unconfigure():
    # 测试用例执行完之后执行此方法
    data["end_time"] = datetime.now()
    print(f"{datetime.now()} 测试结束")
    data["duration"] = data["end_time"] - data["start_time"]
    print(data["duration"])

    assert timedelta(seconds=3) > data["duration"] >= timedelta(seconds=2.5)
