# standard library import
from unittest.mock import patch, MagicMock

# application import
from indented_logs import log_call, log_call_cls
from indented_logs.decorators import get_all_args_str


@patch("indented_logs.decorators._log_call._log_time")
@patch("indented_logs.decorators._log_call._log_return")
@patch("indented_logs.decorators._log_call._log_start")
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

    result = method1(3, 4)  # no qa
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


def test_get_all_args_str():
    result = get_all_args_str(["a", "b", "c"], {"d": 1, "e": 2}, param_max_length=0)
    assert result == "a, b, c, d=1, e=2"
    result = get_all_args_str(
        ["a", "bbbbbb", "cccc"], {"d": 1, "e": 2}, param_max_length=2
    )
    assert result == "a, bb, cc, d=1, e=2"


def test_ouput():
    @log_call()
    def get_data():
        get_parameters()
        query_db(conn="sample_conn_str")

    @log_call()
    def get_parameters():
        pass

    @log_call()
    def query_db(conn):
        return covert_data("1", "2")

    @log_call()
    def covert_data(a, b):
        return (int(a), int(b))

    get_data()


def test_preserve_doc_and_properties():
    @log_call()
    def method1(arg1, arg2):
        """Sample doc"""
        pass

    # method1["custom"] = "value1"

    # print(method1["custom"])
    assert method1.__doc__ == "Sample doc"


def test_decorate_cls():
    captured = []

    def log_with_capture(msg):
        print(msg)
        captured.append(msg)

    @log_call_cls(indent="***", log_time=False, logger_func=log_with_capture)
    class MyClass:
        """MyClass doc"""

        def __init__(self, arg1, arg2):
            self.arg1 = arg1
            self.arg2 = arg2

        def method1(self, arg1, arg2):
            self.method2(arg1)

        def method2(self, arg1):
            pass

        @classmethod
        def class_method1(cls):
            print(cls)
            return "return of class_method1"

    obj = MyClass(5, arg2=10)
    obj.method1("aaaaa", "bbbbbbb")
    result = MyClass.class_method1()
    assert result == "return of class_method1"
    assert MyClass.__doc__ == "MyClass doc"
