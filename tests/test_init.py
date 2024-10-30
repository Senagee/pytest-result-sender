from pathlib import Path

import pytest

pytest_plugins = "pytester"  # 我是测试开发


@pytest.mark.parametrize("send_when", ["on_fail", "every"])
def test_send_when(send_when, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")  # 获取一个临时文件
    config_path.write_text(
        f"""
        [pytest]
        send_when={send_when}
        send_where=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=006e8508-0f9d-4cdf-8be0-397968990e6f
        """
    )
    config = pytester.parseconfig(config_path)
    assert config.getini("send_when") == send_when


def test_send_where(): ...
