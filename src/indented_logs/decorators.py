import time
import functools

indent_arr = []


def get_all_args_str(args, kwargs, param_max_length):
    args_str = ", ".join(map(lambda a: repr_with_length(a, param_max_length), args))

    kwargs_str = ""
    if kwargs:
        kwargs_str = ", " + ", ".join(
            map(
                lambda k: f"{k}={repr_with_length(kwargs[k], param_max_length)}",
                kwargs,
            )
        )

    return f"{args_str}{kwargs_str}"


def log_call(logger_func=print, indent="...", param_max_length=1000, log_time=True):
    """Decorator that log function calls with parameters and indentation

    Args:
        logger_func (Callable, optional): Logging function. Defaults to print.
        indent (str, optional): Indentation string. Defaults to "...".
        param_max_length (int, optional): Parameters max length. Defaults to 1000.
        log_time (bool, optional): Whether log call time. Defaults to True.
    """

    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return _log_call(
                func=func,
                logger_func=logger_func,
                indent=indent,
                param_max_length=param_max_length,
            )(*args, **kwargs)

        # end wrapper

        return wrapper

    # end Inner

    return inner


class _log_call:
    """Inner decorator that actually do the logging"""

    def __init__(
        self, func, logger_func=print, indent="...", param_max_length=50, log_time=True
    ):
        self.func = func
        self.logger_func = logger_func
        self.indent = indent
        self.param_max_length = param_max_length
        self.log_time = log_time

    def __call__(self, *args, **kwargs):
        logger_func = self.logger_func
        func = self.func
        indent = self.indent
        log_time = self.log_time

        indent_arr.append(indent)
        indent_str = "".join(indent_arr)

        logger_func("")
        self._log_start(indent_str, func, args, kwargs)

        start_time = time.perf_counter()

        result = func(*args, *kwargs)

        end_time = time.perf_counter()
        run_time = end_time - start_time

        self._log_return(indent_str, func, result)
        if log_time:
            self._log_time(indent_str, func, run_time)
        logger_func("")

        indent_arr.pop()
        return result

    def _log_time(self, indent_str, func, run_time):
        self.logger_func(f"{indent_str}{func.__name__} FINISHED in {run_time:.6f} secs")

    def _log_return(self, indent_str, func, result):
        self.logger_func(
            f"{indent_str}{func.__name__} RETURN: {repr_with_length(result, self.param_max_length)}"
        )

    def _log_start(self, indent_str, func, args, kwargs):
        self.logger_func(
            f"{indent_str}CALL: {func.__name__}({get_all_args_str(args, kwargs, self.param_max_length)})"
        )


def repr_with_length(arg, length):
    return str(arg)[:length] if length else arg


def log_call_cls(logger_func=print, indent="...", param_max_length=50, log_time=True):
    def inner(cls):

        original_init = cls.__init__

        def new_init(self, *arg, **kwargs):
            print("new init")
            original_init(self, *arg, **kwargs)
            for func_name in dir(self):
                func = getattr(self, func_name)
                if (
                    not func_name.startswith("__")
                    and callable(func)
                    and hasattr(func, "__self__")
                    and func.__self__ != cls
                ):
                    print(func_name)
                    wrapper_func = log_call(
                        logger_func=logger_func,
                        indent=indent,
                        param_max_length=param_max_length,
                        log_time=log_time,
                    )
                    setattr(self, func_name, wrapper_func(func))

        cls.__init__ = new_init

        return cls

    # end inner

    return inner


# end log_call_cls
