from datetime import datetime


def pytest_configure():
    # 配置文件加载完毕之后执行此方法、测试用例执行之前执行此方法
    print(f"{datetime.now()} 现在开始执行测试用例")