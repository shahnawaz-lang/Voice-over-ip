from contextlib import contextmanager
@contextmanager
def open_file(fname):
    f = open(fname)
    try: 
        yield f 
    finally:
        f.close()