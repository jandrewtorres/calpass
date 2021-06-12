
def iterfy(iterable):
    if isinstance(iterable, str):
        yield iterable
    else:
        try:
            # need "iter()" here to force TypeError on non-iterable
            # as e.g. "yield from 1" doesn't throw until "next()"
            yield from iter(iterable)
        except TypeError:
            yield iterable