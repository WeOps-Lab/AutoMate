import time
from functools import partial, wraps

from core.logger import logger


def fn_performance(
    func=None,
    log=logger,
    threshold=0.5,
    stack_info=False,
    level="DEBUG",
    notify="",
    message="[fn: {fn_name}] [func: {func}] [timer: {time}]",
    show_param=True,
    open_sql=False,
    **kwargs,
):
    if func is None:
        return partial(
            fn_performance,
            log=log,
            level=level,
            message=message,
            notify=notify,
            threshold=threshold,
            stack_info=stack_info,
            show_param=show_param,
            open_sql=open_sql,
        )

    @wraps(func)
    def wrapper(*real_args, **real_kwargs):
        t0 = time.time()
        result = func(*real_args, **real_kwargs)

        interval = round(time.time() - t0, 5)

        nonlocal log
        nonlocal threshold

        log.log(
            level,
            "<Performance Log> {} {} ".format(notify, message.format(fn_name=func.__name__, time=interval, func=func)),
        )

        if interval >= threshold:
            if show_param:
                log.log(
                    "WARNING",
                    "The [func_name: {fn_name}] [func: {func}] "
                    "[args:{realfn_args}] [kwargs: {realfn_kwargs}] "
                    "[timer:{time}s] [threshold:{threshold}s], please timely optimize.".format(
                        fn_name=func.__name__,
                        func=func,
                        time=interval,
                        realfn_args=real_args,
                        realfn_kwargs=real_kwargs,
                        threshold=threshold,
                    ),
                )
            else:
                log.log(
                    "WARNING",
                    "The [func_name: {fn_name}] [func: {func}] "
                    "[timer:{time}s] [threshold:{threshold}s], please timely optimize.".format(
                        fn_name=func.__name__, func=func, time=interval, threshold=threshold
                    ),
                )
        return result

    return wrapper
