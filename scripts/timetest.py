import time

MIN_SECONDS = 0.1

# Via https://stackoverflow.com/a/26151604
def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


@parametrized
def time_test(func, name):
    def aux(*xs, **kws):
        t1 = time.monotonic()
        result = func(*xs, **kws)
        t2 = time.monotonic()
        if t2 - t1 > MIN_SECONDS:
            print(f"{name} executed in {(t2-t1)}\n(arguments {list(xs)} {dict(kws)})\n\n")
        return result
    return aux