def test_function2(a, b):
    pass


def test_function1(a, b):
    test_function2(a * 2, b * 2)


def _test_private_function1():
    pass
