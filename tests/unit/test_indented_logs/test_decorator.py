# standard library import
from unittest.mock import patch, MagicMock

# application import
from indented_logs import log_call, log_call_cls, get_all_args_str


@patch("indented_logs._log_call._log_time")
@patch("indented_logs._log_call._log_return")
@patch("indented_logs._log_call._log_start")
def test_decorate_method(
    mock_log_start: MagicMock, mock_log_return: MagicMock, mock_log_time: MagicMock
):
    @log_call(indent="___")
    def method1(arg1, arg2):
        method2()
        return arg1 + arg2

    @log_call(indent="___")
    def method2():
        pass

    result = method1(3, 4)
    assert mock_log_start.call_count == 2
    assert mock_log_return.call_count == 2
    assert mock_log_time.call_count == 2


def test_customize_indent_and_logger():
    captured = []

    def log_with_capture(msg):
        captured.append(msg)

    @log_call(indent="***", log_time=False, logger_func=log_with_capture)
    def method1(arg1, arg2):
        pass

    method1({"a": 1, "b": 2}, "test")

    result = [msg for msg in captured if msg.startswith("***")]
    assert len(result) > 0


def test_decorate_cls():
    captured = []

    def log_with_capture(msg):
        print(msg)
        captured.append(msg)

    @log_call_cls(indent="***", log_time=False, logger_func=log_with_capture)
    class MyClass:
        def method1(self, arg1, arg2):
            self.method2(arg1)

        def method2(self, arg1):
            pass

    obj = MyClass()
    obj.method1("aaaaa", "bbbbbbb")


def test_get_all_args_str():
    result = get_all_args_str(["a", "b", "c"], {"d": 1, "e": 2}, param_max_length=0)
    assert result == "a, b, c, d=1, e=2"
    result = get_all_args_str(
        ["a", "bbbbbb", "cccc"], {"d": 1, "e": 2}, param_max_length=2
    )
    assert result == "a, bb, cc, d=1, e=2"
