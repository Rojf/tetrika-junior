import inspect


def strict(func):
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for name, value in bound_args.arguments.items():
            expected_type = sig.parameters[name].annotation

            if expected_type is not inspect.Parameter.empty:
                if not isinstance(value, expected_type):
                    raise TypeError(
                        "Argument '{name}' must be {expected_type.__name__}," \
                        " got type(value).__name__"
                    )

        res = func(*args, **kwargs)

        return_type = sig.return_annotation
        if return_type is not inspect.Signature.empty:
            if not isinstance(res, return_type):
                raise TypeError(
                    f"Return value must be {return_type.__name__}," \
                        " got {type(res).__name__}"
                )

        return res

    return wrapper
